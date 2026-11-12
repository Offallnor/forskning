"""Oversikter over kildebiblioteket og spørsmålene, og gjenbruk av tidligere uttrekk.

Bruk: python3 -I forskning/verktoy/kilder_oversikt.py            (skriver begge oversiktene)
      python3 -I forskning/verktoy/kilder_oversikt.py <mappe>    (skriver også tidligere-*.tsv for mappen)

forskning/kilder/oversikt.tsv: én linje per kilde med tekst, fil, lenker, hvilke spørsmål som har valgt
den og hvor mange tall og budskap som er hentet ut.
forskning/sporsmal/oversikt.tsv: én linje per spørsmål med spørsmålet, status og antall kilder.
forskning/kilder/<id>/funn.tsv: alle funn fra kilden på tvers av spørsmålene (like funn slått sammen), med
spørsmålene som har brukt funnet og datoen da spørsmålets kontroll sist ga 0 feil.
forskning/kilder/<id>/budskap.tsv: forfatternes budskap, identifikasjon og forbehold, én linje per spørsmål som har lest kilden.
forskning/kilder/funn.tsv: alle funn i hele biblioteket i én tabell, for søk på tvers.
<mappe>/tidligere-estimater.tsv og tidligere-budskap.tsv: rader fra andre spørsmål for kildene i
<mappe>/valgt.txt, med kolonnen sporsmal først. De er et utgangspunkt for uttrekket, ikke ferdige rader.
"""
import csv, glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kilder  # noqa: E402

ROT = kilder.ROT
SP = os.path.join(ROT, "sporsmal")
ID = r"(?:W\d+|AV-[\d-]+|R-[0-9a-f]{10}|KU-[0-9a-f-]{36}|NB-\d+|LI-[0-9a-z]+|FI-[0-9A-Za-z._-]+|[0-9a-f]{12}-[0-9a-f-]{8,})"


def valgte(mappe):
    p = os.path.join(SP, mappe, "valgt.txt")
    return re.findall(rf"^({ID})", open(p, encoding="utf-8").read(), re.M) if os.path.exists(p) else []


def rader(mappe, navn):
    p = os.path.join(SP, mappe, navn)
    return list(csv.DictReader(open(p, encoding="utf-8"), delimiter="\t")) if os.path.exists(p) else []


FUNN = ["utfall", "gruppe", "design", "land", "sammenligning", "mal", "estimat", "ki_lav", "ki_hoy", "n", "side", "sitat"]
BUDSKAP = ["budskap", "hovedresultat", "identifikasjon", "id_sitat", "side", "forbehold", "antakelse", "belegg", "troverdighet"]


def kontrollert(m):
    """Dato da spørsmålets kontroll sist ga 0 feil (fra kontroll.md), ellers tomt."""
    p = os.path.join(SP, m, "kontroll.md")
    t = open(p, encoding="utf-8").read(600) if os.path.exists(p) else ""
    d = re.search(r"Kjørt (\d{4}-\d{2}-\d{2})", t)
    return d.group(1) if d and re.search(r"^0 feil av", t, re.M) else ""


def skriv_tsv(p, kol, rader_):
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(kol)
        for r in rader_:
            w.writerow([str(r.get(k, "") or "").replace("\n", " ") for k in kol])


def skriv_funn(mapper, est, bud):
    dato = {m: kontrollert(m) for m in mapper}
    alle = []
    for w, rr in sorted(est.items()):
        samlet = {}
        for m, r in rr:
            if not (r.get("sitat") or r.get("estimat")):
                continue
            sitat = re.sub(r"[^a-z0-9æøåäöü]+", " ", r.get("sitat", "").lower()).strip()
            # Samme funn når estimatet er likt og det ene sitatet står i det andre (ulike spørsmål klipper sitatet ulikt)
            nokkel = next((n for n in samlet if n[1] == r.get("estimat", "").strip() and (sitat in n[0] or n[0] in sitat)), None)
            if nokkel and len(sitat) > len(nokkel[0]):
                samlet[(sitat, nokkel[1])] = samlet.pop(nokkel); nokkel = (sitat, nokkel[1])
            nokkel = nokkel or (sitat, r.get("estimat", "").strip())
            f = samlet.setdefault(nokkel, {**{k: r.get(k, "") for k in FUNN}, "sporsmal": [], "kontrollert": ""})
            if len(r.get("sitat", "")) > len(f["sitat"]):
                f["sitat"], f["side"] = r.get("sitat", ""), r.get("side", "")
            if m not in f["sporsmal"]:
                f["sporsmal"].append(m)
            f["kontrollert"] = max(f["kontrollert"], dato.get(m, ""))
            for k in FUNN:   # første spørsmål som fylte ut et felt, vinner
                f[k] = f[k] or r.get(k, "")
        if not samlet or not os.path.isdir(kilder.mappe(w)):
            continue
        funn = [{**f, "sporsmal": ",".join(f["sporsmal"])} for f in samlet.values()]
        skriv_tsv(os.path.join(kilder.mappe(w), "funn.tsv"), FUNN + ["sporsmal", "kontrollert"], funn)
        alle += [{"id": w, **f} for f in funn]
    skriv_tsv(os.path.join(kilder.KILDER, "funn.tsv"), ["id"] + FUNN + ["sporsmal", "kontrollert"], alle)
    for w, rr in bud.items():
        if os.path.isdir(kilder.mappe(w)):
            skriv_tsv(os.path.join(kilder.mappe(w), "budskap.tsv"), ["sporsmal"] + BUDSKAP, [{"sporsmal": m, **r} for m, r in rr])


def main(mappe=None):
    mapper = sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(SP, "*", "valgt.txt")))
    brukt, est, bud = {}, {}, {}
    for m in mapper:
        for w in valgte(m):
            brukt.setdefault(w, []).append(m) if m not in brukt.get(w, []) else None
        for r in rader(m, "estimater.tsv"):
            est.setdefault(r["id"], []).append((m, r))
        for r in rader(m, "budskap.tsv"):
            bud.setdefault(r["id"], []).append((m, r))

    skriv_funn(mapper, est, bud)

    linjer = ["id\ttittel\tar\ttekst\tfil\tlenke\thentet_fra\tsporsmal\testimater\tbudskap"]
    for d in sorted(glob.glob(os.path.join(kilder.KILDER, "*", "kilde.json"))):
        w = os.path.basename(os.path.dirname(d))
        k = kilder.les_meta(w)
        tekst = "ja" if kilder.har_tekst(w, streng=True) else "kort" if kilder.har_tekst(w) else "nei"
        felt = [w, (k.get("tittel") or "").replace("\t", " ")[:150], str(k.get("ar") or ""), tekst,
                f"kilder/{w}/{k['fil']}" if k.get("fil") else "", k.get("lenke") or "", k.get("hentet_fra") or "",
                ",".join(brukt.get(w, [])), str(len(est.get(w, []))), str(len(bud.get(w, [])))]
        linjer.append("\t".join(felt))
    open(os.path.join(kilder.KILDER, "oversikt.tsv"), "w", encoding="utf-8").write("\n".join(linjer) + "\n")

    sp = ["mappe\tsporsmal\tstatus\tkilder\testimater"]
    for m in mapper:
        p = os.path.join(SP, m, "svar.md")
        svar = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
        tittel = re.search(r"^# (.+)$", svar, re.M)
        status = re.search(r"^(Utkast[^.]*|Kontrollert[^.]*|Godkjent[^.]*)\.", svar, re.M)
        sp.append("\t".join([m, tittel.group(1) if tittel else "", status.group(1) if status else ("uten svar" if not svar else ""),
                             str(len(set(valgte(m)))), str(len(rader(m, "estimater.tsv")))]))
    open(os.path.join(SP, "oversikt.tsv"), "w", encoding="utf-8").write("\n".join(sp) + "\n")
    print(f"{len(linjer) - 1} kilder, {len(mapper)} spørsmål")

    if mappe:
        mine = set(valgte(mappe))
        for navn, kilde in (("tidligere-estimater.tsv", est), ("tidligere-budskap.tsv", bud)):
            ut = [(m, r) for w in sorted(mine) for m, r in kilde.get(w, []) if m != mappe]
            p = os.path.join(SP, mappe, navn)
            if not ut:
                if os.path.exists(p):
                    os.remove(p)
                continue
            kol = list(ut[0][1].keys())
            with open(p, "w", encoding="utf-8", newline="") as f:
                skriv = csv.writer(f, delimiter="\t", lineterminator="\n")
                skriv.writerow(["sporsmal"] + kol)
                for m, r in ut:
                    skriv.writerow([m] + [r.get(k, "") for k in kol])
            print(f"{navn}: {len(ut)} rader fra {len({m for m, _ in ut})} andre spørsmål")


if __name__ == "__main__":
    main(*sys.argv[1:2])
