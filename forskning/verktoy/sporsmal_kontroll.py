"""Automatiske kontroller av et svar bygd på forskning.

Bruk: python3 -I forskning/verktoy/sporsmal_kontroll.py <mappe>
Leser forskning/sporsmal/<mappe>/{kandidater.jsonl, estimater.tsv, svar.md, utelatt.tsv}, teksten i kildebiblioteket
forskning/kilder/<id>/tekst.txt
og forskning/katalog/poster.jsonl. Skriver <mappe>/kontroll.md. Avslutter med kode 1 ved feil.

1 Kildene finnes   2 Sitatet står i teksten på oppgitt side   3 Tallene står i sitatet
4 Tallene henger sammen   5 Tallene i svaret finnes i estimat- eller statistikktabellen   6 Utelatte kilder er begrunnet
7 Statistikk: hvert tall i statistikk.tsv står i den lagrede uttrekksfila (eller er en utregning med formel)
8 Figurer: hvert tall i figurer.tsv står i den lagrede fila, og hver figur er laget og lenket i svaret
9 Innholdskontrollen er gjort   10 Påminnelse (ikke feil): antall uleste sentrale kilder, som forbeholdene skal oppgi
"""
import csv, json, math, os, re, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kilder  # noqa: E402
import figur  # noqa: E402

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def vask(s, lig=False):
    s = unicodedata.normalize("NFKC", s or "").replace("−", "-").replace("–", "-").replace("—", "-")
    if lig:   # ligaturene fi, ff, fl, ffi og ffl er i noen PDF-er lagret som kontrolltegn (\x1b, \x1c): sammenlign uten dem
        s = re.sub(r"[\x00-\x08\x0e-\x1f\x7f]", "\x00", s)
        s = re.sub(r"ff[il]|f[fil]", "\x00", s.lower())
    s = re.sub(r"-\s*\n\s*", "", s)              # orddeling over linjeskift
    s = re.sub(r"[‘’“”«»\"']", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def tall(s, kilde=False):
    s = (s or "").replace("−", "-")
    s = re.sub(r"(^|[\s(\[])[–—](?=\d)", r"\1-", s)   # tankestrek brukt som minustegn foran et tall
    s = re.sub(r"(^|[(\[=:,;]|[^\d\s]\s)-\s+(?=\d)", r"\1-", s)   # minustegn med mellomrom foran tallet («− 2.91»), ikke spenn
    if kilde:   # engelsk kildetekst: 24,466 er tusenskille; norsk kildetekst: 0,075 er desimaltall. Begge lesningene godtas
        ekstra = re.findall(r"-?\d+,\d+", re.sub(r"(\d)\s*[-–]\s*(\d)", r"\1 \2", s))
        s = re.sub(r"\b(\d{1,3})((?:,\d{3})+)(?![\d.])", lambda m: m.group(1) + m.group(2).replace(",", ""), s)
        return nuller(re.findall(TALL, re.sub(r"(\d)\s*[-–]\s*(\d)", r"\1 \2", s))) + ekstra
    else:       # norsk svartekst: 24 466 er tusenskille
        s = re.sub(r"\b(\d{1,3})((?:[ \u00a0\u202f]\d{3})+)(?!\d)", lambda m: m.group(1) + re.sub(r"\D", "", m.group(2)), s)
    s = re.sub(r"(\d)\s*[-–]\s*(\d)", r"\1 \2", s)   # spenn som 12-14 eller 1.22–1.37
    return nuller(re.findall(TALL, s))


# Tall, også uten null foran desimaltegnet («.32», «-.05»), som ellers ble lest som 32 og 5
TALL = r"-?(?:\d+(?:[.,]\d+)?|(?<![\d.,])\.\d+)"


def nuller(liste):
    return [re.sub(r"^(-?)\.", r"\g<1>0.", t) for t in liste]


def f(x):
    x = str(x or "").strip().replace(",", ".").replace("−", "-")
    if x in ("", "–", "-"):
        return None
    try:
        return float(x)
    except ValueError:
        return "format"


def main():
    mappe = os.path.join(ROT, "sporsmal", sys.argv[1])
    kand = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(mappe, "kandidater.jsonl"), encoding="utf-8")}
    # Manglende poster.jsonl, estimater.tsv eller svar.md gir tomme tabeller, så skriptet kan kjøres før uttrekket
    # (for eksempel for å få utelatt-mangler.tsv)
    pp, ep, sp = os.path.join(ROT, "katalog", "poster.jsonl"), os.path.join(mappe, "estimater.tsv"), os.path.join(mappe, "svar.md")
    nva = {json.loads(l)["id"]: json.loads(l) for l in open(pp, encoding="utf-8") if l.strip()} if os.path.exists(pp) else {}
    est = list(csv.DictReader(open(ep, encoding="utf-8"), delimiter="\t")) if os.path.exists(ep) else []
    svar = open(sp, encoding="utf-8").read() if os.path.exists(sp) else ""
    ut_p = os.path.join(mappe, "utelatt.tsv")
    utelatt = {r["id"]: r["begrunnelse"] for r in csv.DictReader(open(ut_p, encoding="utf-8"), delimiter="\t")} if os.path.exists(ut_p) else {}
    funn, feil = [], 0

    def meld(ok, tekst):
        nonlocal feil
        feil += 0 if ok else 1
        funn.append(("OK  " if ok else "FEIL") + " " + tekst)

    # 1 Kildene finnes
    lenker = set(re.findall(r"openalex\.org/(W\d+)", svar)) | set(re.findall(r"nva\.sikt\.no/registration/([0-9a-f-]+)", svar))
    # Artikler i Arbeid og velferd lenkes til nav.no; id-en finnes via adressen i kandidatene
    nav_url = {r.get("apen_url"): k for k, r in kand.items() if k.startswith(("AV-", "R-", "KU-", "NB-", "LI-", "FI-"))}
    for u in re.findall(r"\((https://www\.nav\.no/[^)\s]+)\)", svar):
        lenker.add(nav_url.get(u, u))
    lenker |= {k for u, k in nav_url.items() if k.startswith(("R-", "KU-", "NB-", "LI-", "FI-")) and u and u in svar}   # rapporter lagt inn med url:
    brukt = set()
    for l in sorted(lenker):
        ok = l in kand or l in nva
        brukt.add(l)
        meld(ok, f"1 kilde {l} {'finnes' if ok else 'finnes IKKE i søket eller katalogen'}")
    for r in est:
        ok = r["id"] in kand or r["id"] in nva
        meld(ok, f"1 estimat-kilde {r['id']} {'finnes' if ok else 'finnes IKKE'}")

    # 1b Forfatternavnet i lenketeksten står blant forfatterne i metadata eller i starten av teksten
    def uten(x):
        return "".join(c for c in unicodedata.normalize("NFKD", (x or "").lower()) if not unicodedata.combining(c))
    for tekst, url in re.findall(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", svar):
        m = re.search(r"openalex\.org/(W\d+)|nva\.sikt\.no/registration/([0-9a-f-]+)", url)
        kid = (m.group(1) or m.group(2)) if m else nav_url.get(url)
        k = kand.get(kid) or nva.get(kid) if kid else None
        if not k:
            continue
        navn = re.split(r"\s+(?:mfl\.?|m\.fl\.?|et al\.?|og|and|&)\s+|,|\s+\d{4}|\s*\*", re.sub(r"[*_]", "", tekst).strip())[0].strip()
        if not re.search(r"\b(?:19|20)\d\d\b", tekst) or not navn or not re.match(r"[A-ZÆØÅÄÖÜ]", navn) or len(navn.split()) > 3 or navn.lower().startswith(("nav", "fhi", "ssb", "isf")):
            continue   # lenketekst som ikke er et forfatternavn (tittel, institusjon)
        forf = k.get("forfattere") or []
        forf = " ".join(forf) if isinstance(forf, list) else str(forf)
        start = kilder.les_tekst(kid)[:20000] if kid else ""
        ok1 = all(uten(d) in uten(forf) or uten(d) in uten(start) for d in re.findall(r"[^\s-]{2,}", navn))
        meld(ok1, f"1 forfatter «{navn}» for {kid} {'står i metadata eller på tittelsiden' if ok1 else 'står IKKE i metadata eller på tittelsiden'}")

    # 2-4 per estimat
    for i, r in enumerate(est, 1):
        tag = f"rad {i} ({r['id']}, {r['utfall'][:40]})"
        if not r.get("sitat", "").strip() and not r.get("estimat", "").strip():
            continue   # linje som bare sier at kilden mangler tall
        p = kilder.tekst_sti(r["id"])
        if r.get("side", "").strip().lower() == "sammendrag":
            tekst_side = kand.get(r["id"], nva.get(r["id"], {})).get("sammendrag", "")
        elif os.path.exists(p):
            sider = open(p, encoding="utf-8", errors="replace").read().split("\f")
            try:
                n = int(r["side"])
                tekst_side = " ".join(sider[max(0, n - 2):n + 1])   # side ±1 pga. ulik nummerering
            except ValueError:
                tekst_side = " ".join(sider)
        else:
            tekst_side = ""
        ok2 = bool(tekst_side) and (vask(r["sitat"]) in vask(tekst_side) or vask(r["sitat"], lig=True) in vask(tekst_side, lig=True))
        meld(ok2, f"2 sitat {tag} {'står på oppgitt side' if ok2 else 'ble IKKE funnet på oppgitt side'}")
        sitat_tall = {t.replace(",", ".") for t in tall(r["sitat"], kilde=True)} | set(tall(r["sitat"]))   # også 899 730 med mellomrom som tusenskille
        for felt in ("estimat", "ki_lav", "ki_hoy"):
            v = r.get(felt, "").strip()
            if v and v not in ("–", "-"):
                ok3 = v.replace(",", ".") in sitat_tall
                if not ok3 and not sitat_tall and "med ord" in r.get("utfall", ""):
                    ok3 = True   # tallet står med ord i sitatet (UTTREKK.md); kontrolleres for hånd
                meld(ok3, f"3 {felt}={v} {tag} {'står i sitatet' if ok3 else 'står IKKE i sitatet'}")
        e, lo, hi = f(r.get("estimat")), f(r.get("ki_lav")), f(r.get("ki_hoy"))
        if "format" in (e, lo, hi):
            meld(False, f"4 {tag} estimat eller KI er ikke ett tall (skriv ett tall per felt, spenn og tekst i utfall)")
            continue
        if e is not None and lo is not None and hi is not None:
            meld(lo <= e <= hi, f"4 {tag} estimat {'innenfor' if lo <= e <= hi else 'UTENFOR'} KI")
            if r.get("mal", "").upper() in ("RR", "OR", "HR") and lo > 0 and e > 0:
                skjevhet = abs((math.log(hi) - math.log(e)) - (math.log(e) - math.log(lo)))
                meld(skjevhet < 0.15, f"4 {tag} KI {'symmetrisk' if skjevhet < 0.15 else 'IKKE symmetrisk'} på log-skala (avvik {skjevhet:.2f})")

    # 7 Statistikk (tilvalg): statistikk.tsv med tall fra SSB, Nav, Eurostat, OECD o.l.
    st_p = os.path.join(mappe, "statistikk.tsv")
    stat = list(csv.DictReader(open(st_p, encoding="utf-8"), delimiter="\t")) if os.path.exists(st_p) else []
    for i, r in enumerate(stat, 1):
        tag = f"statistikk rad {i} ({r.get('kilde', '')} {r.get('tabell', '')}, {r.get('beskrivelse', '')[:40]})"
        mangler = [k for k in ("kilde", "tabell", "periode", "verdi", "enhet", "definisjon", "adresse", "hentet") if not (r.get(k) or "").strip()]
        meld(not mangler, f"7 {tag} {'har alle felt' if not mangler else 'mangler ' + ', '.join(mangler)}")
        if (r.get("utregning") or "").strip():
            meld(True, f"7 {tag} er utregnet: {r['utregning'][:80]}")
            continue
        fp = os.path.join(mappe, r.get("fil") or "")
        if not (r.get("fil") or "").strip() or not os.path.isfile(fp):
            meld(False, f"7 {tag} uttrekksfila «{r.get('fil', '')}» finnes IKKE"); continue
        innhold = open(fp, encoding="utf-8", errors="replace").read()
        tallene = {t.replace(",", ".").lstrip("-") for t in tall(innhold, kilde=True) + tall(innhold)}
        v = (r.get("verdi") or "").replace(",", ".").replace(" ", "").replace("\u00a0", "").lstrip("-")
        ok7 = v in tallene or (v.endswith(".0") and v[:-2] in tallene) or (v + ".0") in tallene
        meld(ok7, f"7 {tag} verdien {r.get('verdi')} {'står' if ok7 else 'står IKKE'} i {r.get('fil')}")

    # 8 Figurer (tilvalg): figurer.tsv, laget med figur.py
    fig = figur.les(mappe) if os.path.exists(os.path.join(mappe, "figurer.tsv")) else []
    if fig:
        _, meldinger = figur.kontroller(mappe, fig)
        for m in meldinger:
            meld(m.startswith("- OK"), "8 " + m[2:].replace("FEIL", "").replace("OK", "", 1).strip())
        for navn in dict.fromkeys(r["figur"] for r in fig):
            png = f"figurer/{navn}.png"
            meld(os.path.isfile(os.path.join(mappe, png)), f"8 figuren {png} {'er laget' if os.path.isfile(os.path.join(mappe, png)) else 'er IKKE laget (kjør figur.py)'}")
            meld(png in svar, f"8 figuren {png} {'er lenket' if png in svar else 'er IKKE lenket'} i svaret")

    # 5 Tall i svaret
    tabell = set()
    for r in fig:
        tabell |= {t.replace(",", ".").lstrip("-") for t in tall(r.get("verdi", "")) + tall(r.get("verdi", ""), kilde=True)}
    for r in stat:
        for felt in ("verdi", "periode", "tabell"):
            tabell |= {t.replace(",", ".").lstrip("-") for t in tall(r.get(felt, "")) + tall(r.get(felt, ""), kilde=True)}
    for r in est:
        for felt in ("estimat", "ki_lav", "ki_hoy", "n", "sitat"):
            tabell |= {t.replace(",", ".").lstrip("-") for t in tall(r.get(felt, ""), kilde=True) + tall(r.get(felt, ""))}   # fortegn uttrykkes ofte med ord i svaret
    # Innledningen før første overskrift på nivå 2 (status, kildegrunnlag, reproduserbarhet) teller kilder og runder i
    # løypa, ikke funn. Tall over tolv skrives der med siffer (Språkrådet), så den sjekkes ikke mot tabellene.
    prosa = re.sub(r"\A.*?(?=^## )", "", svar, flags=re.S | re.M)
    prosa = re.sub(r"\[[^\]]*\]\([^)]*\)", "", prosa)           # fjern lenker
    # Antall og tidsrom som beskriver studiene (15 forsøk, 96 kommuner, etter 18 måneder, 192 bare i sammendrag) er ikke
    # funn. Før 14.11.2026 sto de med bokstaver og ble ikke sjekket; nå står tall over tolv med siffer.
    prosa = re.sub(r"(?<![\d,.])\b\d+(?= (?:(?:av (?:dem|disse|kjernekildene) )?(?:er )?bare (?:lest )?i sammendrag|(?:nye |valgte |norske |nordiske |randomiserte |andre )?(?:studier|studiene|kilder|kildene|oppføringer|forsøk|land|kommuner|artikler|rapporter|evalueringer|metaanalyser|oversikter|estimater|programmer|måneder|uker|dager|år)\b))", "", prosa)
    prosa = re.sub(r"`[^`\n]*`", "", prosa)                       # kode og filnavn i backticks
    prosa = re.sub(r"\b(?=[0-9a-f]*[a-f])(?=[0-9a-f]*\d)[0-9a-f]{7,40}\b", "", prosa)   # commit-hasher
    prosa = re.sub(r"\b\d{1,2}\.\d{1,2}\.(?:19|20)\d\d\b", "", prosa)   # datoer som 7.11.2026
    prosa = re.sub(r"\((?:19|20)\d\d\)|\b(?:19|20)\d\d\b", "", prosa)   # årstall
    for t in sorted({t.replace(",", ".").lstrip("-") for t in tall(prosa)} - {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10"}):
        meld(t in tabell, f"5 tallet {t} i svaret {'finnes i estimat- eller statistikktabellen' if t in tabell else 'finnes IKKE i estimat- eller statistikktabellen'}")

    # 6 Utelatte sentrale kilder
    brukt |= {r["id"] for r in est}
    vp = os.path.join(mappe, "valgt.txt")
    if os.path.exists(vp):   # valgte kilder (også de uten egne tall, f.eks. når en annen versjon er brukt) er ikke utelatt
        brukt |= {l.split("#")[0].strip() for l in open(vp, encoding="utf-8") if l.split("#")[0].strip()}
    mangler6 = []
    sentrale = [k for k in kand.values() if k["oversikt"] or (k.get("persentil") or 0) >= 0.9 or (k.get("siteringer") or 0) >= 50]
    for k in sentrale:
        if k["id"] in brukt:
            continue
        ok6 = k["id"] in utelatt
        if not ok6:
            mangler6.append(k)
        meld(ok6, f"6 utelatt {k['id']} «{k['tittel'][:70]}» ({k['ar']}) {'– ' + utelatt[k['id']] if ok6 else 'mangler begrunnelse'}")

    # 9 Innholdskontrollen er gjort (obligatorisk fra 9.11.2026, også i raskt svar)
    bp = os.path.join(mappe, "budskap.tsv")
    budskap = {r["id"] for r in csv.DictReader(open(bp, encoding="utf-8"), delimiter="\t")} if os.path.exists(bp) else set()
    ik = set()
    for fn in sorted(os.listdir(mappe)):
        if re.fullmatch(r"innholdskontroll(-\d+)?\.tsv", fn):
            ik |= {r["id"].strip() for r in csv.DictReader(open(os.path.join(mappe, fn), encoding="utf-8"), delimiter="\t")}
    meld(os.path.exists(os.path.join(mappe, "kort-svar-blind.md")), "9 kort-svar-blind.md " + ("finnes" if os.path.exists(os.path.join(mappe, "kort-svar-blind.md")) else "MANGLER (blind lesing, steg 1b)"))
    meld("kort svar" in ik, "9 innholdskontroll " + ("har raden «kort svar»" if "kort svar" in ik else "MANGLER raden «kort svar» (eller innholdskontroll.tsv mangler)"))
    for l in sorted(lenker):
        lid = l if l in kand or l in nva else None
        if not lid:
            continue
        ok9 = lid in budskap
        meld(ok9, f"9 blind lesing {lid} " + ("i budskap.tsv" if ok9 else "MANGLER i budskap.tsv"))

    # 10 Uleste sentrale kilder (påminnelse, teller ikke som feil): forbeholdene skal si hvor mange oversikter og
    # studier i kategori 1-3 som ikke er lest i fulltekst (LOYPE.md, steg 5). Antallet er det samme som i vedlegg B.
    obs = []
    if svar.strip() and os.path.exists(os.path.join(mappe, "valgt.txt")):
        import vedlegg_bc
        ikke, bare = vedlegg_bc.uleste(sys.argv[1])
        if ikke or bare:
            m = re.search(r"^#+\s*Forbehold.*?(?=^#+\s|\Z)", svar, re.S | re.M | re.I)
            nevnt = bool(m) and re.search(r"ikke (er )?lest|bare (lest )?i sammendrag|bare sammendrag|ikke tilgjengelig", m.group(0), re.I)
            obs.append(f"OBS  10 {len(ikke) + len(bare)} sentrale valgte kilder er ikke lest i fulltekst ({len(ikke)} ikke lest, {len(bare)} bare sammendrag; "
                       f"se vedlegg_bc.py). Forbeholdene {'nevner uleste kilder' if nevnt else 'NEVNER IKKE uleste kilder'}: sjekk at antallet stemmer.")

    # Sentrale kandidater uten begrunnelse listes i utelatt-mangler.tsv, klar til å fylles ut og flyttes til utelatt.tsv
    um = os.path.join(mappe, "utelatt-mangler.tsv")
    if mangler6:
        with open(um, "w", encoding="utf-8") as fh:
            fh.write("id\tbegrunnelse\tar\tsiteringer\toversikt\ttittel\n")
            for k in mangler6:
                fh.write(f"{k['id']}\t\t{k.get('ar')}\t{k.get('siteringer')}\t{k.get('oversikt')}\t{k['tittel']}\n")
    elif os.path.exists(um):
        os.remove(um)

    with open(os.path.join(mappe, "kontroll.md"), "w", encoding="utf-8") as fh:
        import datetime
        fh.write(f"# Kontroll: {sys.argv[1]}\n\nKjørt {datetime.date.today().isoformat()}.\n\n{feil} feil av {len(funn)} kontroller.\n\n")
        fh.write("\n".join("- " + x for x in obs + funn) + "\n")
    print(f"{feil} feil av {len(funn)} kontroller")
    print("\n".join(obs))
    print("\n".join(x for x in funn if x.startswith("FEIL")))
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(main())
