"""Leser PDF-er som er lastet opp i forskning/innboks/ og finner ut hvilken kilde de er.

Filnavnet brukes ikke. Kilden finnes ut fra innholdet: først DOI i teksten, ellers
hvor stor del av tittelordene til hver kandidat som står i starten av teksten.
Teksten og selve PDF-en lagres i kildebiblioteket, forskning/kilder/<id>/tekst.txt og fil.pdf
(se kilder.py), så alle spørsmål kan bruke dem og brukeren kan lese fila selv.
Resultatet skrives i innboks/logg.md.
Brukes av .github/workflows/forskning-innboks.yml.
"""
import glob, json, os, re, shutil, subprocess, sys, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kilder  # noqa: E402

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INN = os.path.join(ROT, "innboks")
GRENSE, AVSTAND, MINTEKST = 0.7, 0.15, 2000


def kandidater():
    k = {}
    for f in glob.glob(os.path.join(ROT, "sporsmal", "*", "kandidater.jsonl")):
        mappe = os.path.basename(os.path.dirname(f))
        for l in open(f, encoding="utf-8"):
            if not l.strip():
                continue
            d = json.loads(l)
            wid = d["id"].split("/")[-1]
            post = k.setdefault(wid, {"tittel": d.get("tittel") or "", "doi": (d.get("doi") or "").lower().replace("https://doi.org/", ""), "ar": d.get("ar"), "mapper": set(), "rad": d})
            post["mapper"].add(mappe)
    valgt = set()
    valgt_i = {}
    for f in glob.glob(os.path.join(ROT, "sporsmal", "*", "valgt.txt")):
        mappe = os.path.basename(os.path.dirname(f))
        for w in re.findall(r"^((?:W\d+|AV-[\d-]+|R-[0-9a-f]{10}|KU-[0-9a-f-]{36}|NB-\d+|LI-[0-9a-z]+|FI-[0-9A-Za-z._-]+|[0-9a-f]{12}-[0-9a-f-]{8,}))", open(f, encoding="utf-8").read(), re.M):
            valgt.add(w); valgt_i.setdefault(w, set()).add(mappe)
    for wid in k:
        k[wid]["valgt"] = wid in valgt
        # Tekst legges bare der kilden er valgt; er den ikke valgt noe sted, i alle spørsmål der den er kandidat
        if wid in valgt_i:
            k[wid]["mapper"] = valgt_i[wid] & k[wid]["mapper"] or k[wid]["mapper"]
    return k


def tittelord(t):
    return set(re.findall(r"[a-zæøåäöü]{4,}", t.lower()))


def norm(t):
    return " ".join(re.findall(r"[a-z0-9æøåäöü]+", t.lower()))


def finn(tekst, kand):
    """Finner kilden ut fra forsiden: DOI, deretter hele tittelen, deretter tittelordene."""
    forside = tekst[:4000].lower()
    nf = norm(tekst[:6000])
    for doi in set(re.findall(r"10\.\d{4,9}/[^\s\"<>]+", forside)):
        doi = doi.rstrip(".,;)")
        for wid, k in kand.items():
            if k["doi"] and k["doi"] == doi:
                return wid, 1.0, "doi"
    hele = [(len(norm(k["tittel"])), wid) for wid, k in kand.items() if len(norm(k["tittel"]).split()) >= 4 and norm(k["tittel"]) in nf]
    if hele:
        hele.sort(key=lambda h: (h[0], kand[h[1]]["valgt"]), reverse=True)
        return hele[0][1], 1.0, "hele tittelen"
    ordene = set(re.findall(r"[a-z0-9æøåäöü]+", forside))
    poeng = []
    for wid, k in kand.items():
        o = tittelord(k["tittel"])
        if len(o) < 3:
            continue
        poeng.append((sum(w in ordene for w in o) / len(o), len(o), wid))
    poeng.sort(reverse=True)
    if not poeng:
        return None, 0, ""
    beste = poeng[0]
    andre = next((p for p in poeng[1:] if norm(kand[p[2]]["tittel"]) != norm(kand[beste[2]]["tittel"])), (0, 0, None))
    if beste[0] >= GRENSE and (beste[0] - andre[0] >= AVSTAND or (beste[0] - andre[0] < 0.01 and beste[1] >= andre[1] + 3)):
        return beste[2], beste[0], "tittelord"
    return None, beste[0], f"usikker: {kand[beste[2]]['tittel'][:60]} ({beste[0]:.0%})" + (f" eller {kand[andre[2]]['tittel'][:60]} ({andre[0]:.0%})" if andre[2] else "")


def main():
    kand = kandidater()
    filer = [f for f in glob.glob(os.path.join(INN, "*")) if f.lower().endswith(".pdf")]
    if not filer:
        return
    nu = datetime.date.today().isoformat()
    linjer = []
    for f in filer:
        navn = os.path.basename(f)
        tp = f + ".txt"
        subprocess.run(["pdftotext", f, tp])
        tekst = open(tp, encoding="utf-8", errors="replace").read() if os.path.exists(tp) else ""
        if len(tekst.strip()) < MINTEKST:
            os.remove(f)
            linjer.append(f"| {nu} | {navn} | Kan ikke leses (trolig skannet). Last opp en versjon med tekst. | | |")
            if os.path.exists(tp):
                os.remove(tp)
            continue
        wid, treff, hvordan = finn(tekst, kand)
        if not wid:
            os.remove(f)
            os.makedirs(os.path.join(INN, "ukjent"), exist_ok=True)
            os.replace(tp, os.path.join(INN, "ukjent", os.path.splitext(navn)[0] + ".txt"))
            linjer.append(f"| {nu} | {navn} | Ikke gjenkjent. {hvordan} | | |")
            continue
        k = kand[wid]
        # Fila lagres alltid, så brukeren kan lese den. Teksten erstattes bare når den gamle var for kort
        # (bare ingress eller skannet), fordi uttrekkene viser til sidene i den teksten som ligger der.
        gammel = kilder.les_tekst(wid)
        if kilder.har_tekst(wid, streng=True):
            kilder.lagre_meta(wid, k["rad"])
            resultat = "Fil lagret, teksten fantes fra før"
        else:
            kilder.lagre_tekst(wid, tekst, k["rad"], hentet_fra=f"opplastet: {navn}", hvordan="opplastet",
                               merknad="erstattet kort tekst" if gammel.strip() else "")
            resultat = "Lagt inn"
        shutil.move(f, os.path.join(kilder.mappe(wid), "fil.pdf"))
        kilder.lagre_meta(wid, fil="fil.pdf", opplastet=nu)
        os.remove(tp)
        linjer.append(f"| {nu} | {navn} | {resultat} ({hvordan}, {treff:.0%}) | {k['tittel'][:90]} ({k['ar']}), {wid} | {', '.join(sorted(k['mapper']))} |")
    logg = os.path.join(INN, "logg.md")
    if not os.path.exists(logg):
        open(logg, "w", encoding="utf-8").write("# Logg for innboksen\n\n| Dato | Fil | Resultat | Kilde | Spørsmål |\n|---|---|---|---|---|\n")
    open(logg, "a", encoding="utf-8").write("\n".join(linjer) + "\n")
    print("\n".join(linjer))


if __name__ == "__main__":
    main()
