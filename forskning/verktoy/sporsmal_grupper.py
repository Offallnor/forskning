"""Deler de valgte kildene i grupper til uttrekket, og sjekker etterpå at ingen falt mellom.

Bruk: python3 -I forskning/verktoy/sporsmal_grupper.py <mappe> [--storrelse 25] [--kjerne]
       python3 -I forskning/verktoy/sporsmal_grupper.py <mappe> --sjekk

Uten --sjekk skrives <mappe>/grupper.tsv med én rad per kilde i valgt.txt:
  id, lest (tekst, sammendrag eller ingen), gruppe, tittel
Kilder med tekst eller sammendrag fordeles i grupper på høyst --storrelse kilder, i rekkefølgen
oversikter, nordiske kilder og resten (kilder med tekst først innenfor hver del). Kilder uten tekst og
uten sammendrag får gruppen «ikke uttrekk»: de gir ingen tall, og kildeoversikt.py lister dem i
vedlegg A som kilder som ikke kunne leses. Hver gruppe gis til én uttrekkskjøring.

Med --kjerne tas bare kjernen med i uttrekket: oversikter, nordiske kilder og kilder med kategori 1–3, slik kategorien
står først i kommentaren i valgt.txt («W123  # 3, SE, nivå, ...»). Kilder uten kategori i kommentaren tas med (ved
tvil med). Resten får gruppen «ikke uttrekk (utenfor kjernen)» og listes bare. Brukes når utvalget er over om lag
300 studier og bestilleren har valgt å avgrense (LOYPE.md, steg 4).

Med --sjekk listes kilder med tekst eller sammendrag som ikke har noen rad i estimater.tsv
(eller estimater-b.tsv). Kjør den etter uttrekket og før svaret skrives.
"""
import csv, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kilder  # noqa: E402
from kilder_oversikt import valgte  # noqa: E402

NORDISK = {"NO", "SE", "DK", "FI", "IS"}


def status(mappe):
    sti = os.path.join(kilder.ROT, "sporsmal", mappe)
    kand = {}
    for l in open(os.path.join(sti, "kandidater.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        kand[r["id"]] = r
    ut = []
    for wid in dict.fromkeys(valgte(mappe)):
        r = kand.get(wid) or {}
        lest = "tekst" if kilder.har_tekst(wid) else ("sammendrag" if (r.get("sammendrag") or "").strip() else "ingen")
        ut.append({"id": wid, "lest": lest, "oversikt": bool(r.get("oversikt")),
                   "nordisk": bool(NORDISK & set(r.get("land") or [])) or wid.startswith(("AV-", "KU-", "NB-", "LI-", "FI-")) or wid[:4].isdigit(),
                   "tittel": (r.get("tittel") or "").replace("\t", " ")[:120]})
    return sti, ut


def kategorier(sti):
    """Kategorien først i kommentaren i valgt.txt, per id (første forekomst). None når den mangler."""
    kat = {}
    for l in open(os.path.join(sti, "valgt.txt"), encoding="utf-8"):
        wid, _, kommentar = l.partition("#")
        wid = wid.strip()
        if wid and not wid.startswith(("url:", "tittel:")) and wid not in kat:
            m = re.match(r"\s*(?:kategori\s*)?([1-5])\b", kommentar)
            kat[wid] = int(m.group(1)) if m else None
    return kat


def grupper(mappe, storrelse, kjerne=False):
    sti, ut = status(mappe)
    if kjerne:
        kat = kategorier(sti)
        uten = 0
        for k in ut:
            c = kat.get(k["id"])
            uten += c is None
            if not (k["oversikt"] or k["nordisk"] or c is None or c <= 3):
                k["gruppe"] = "ikke uttrekk (utenfor kjernen)"
        ute = sum(k.get("gruppe", "").endswith("kjernen)") for k in ut)
        print(f"Kjerne: {len(ut) - ute} kilder i kjernen, {ute} utenfor. {uten} uten kategori i kommentaren er tatt med i kjernen"
              + (" (sett kategorien først i kommentaren i valgt.txt og kjør på nytt)." if uten else "."))
    lesbare = [k for k in ut if k["lest"] != "ingen" and "gruppe" not in k]
    lesbare.sort(key=lambda k: (not k["oversikt"], not k["nordisk"], k["lest"] != "tekst"))
    for i, k in enumerate(lesbare):
        k["gruppe"] = str(i // storrelse + 1)
    for k in ut:
        k.setdefault("gruppe", "ikke uttrekk")
    with open(os.path.join(sti, "grupper.tsv"), "w", encoding="utf-8") as fh:
        fh.write("id\tlest\tgruppe\ttittel\n")
        for k in sorted(ut, key=lambda k: (k["gruppe"].startswith("ikke uttrekk"), int(k["gruppe"]) if k["gruppe"].isdigit() else 0)):
            fh.write(f"{k['id']}\t{k['lest']}\t{k['gruppe']}\t{k['tittel']}\n")
    n = {s: sum(k["lest"] == s for k in ut) for s in ("tekst", "sammendrag", "ingen")}
    print(f"{len(ut)} kilder: {n['tekst']} med tekst, {n['sammendrag']} bare sammendrag, {n['ingen']} uten noe "
          f"(ikke uttrekk). {(len(lesbare) + storrelse - 1) // storrelse} grupper i grupper.tsv.")


def sjekk(mappe):
    sti, ut = status(mappe)
    med_rad = set()
    for navn in ("estimater.tsv", "estimater-b.tsv"):
        p = os.path.join(sti, navn)
        if os.path.exists(p):
            med_rad |= {r["id"] for r in csv.DictReader(open(p, encoding="utf-8"), delimiter="\t")}
    gp = os.path.join(sti, "grupper.tsv")   # kilder som grupper.tsv har holdt utenfor uttrekket, telles ikke
    utenfor = {r["id"] for r in csv.DictReader(open(gp, encoding="utf-8"), delimiter="\t")
               if r["gruppe"].startswith("ikke uttrekk")} if os.path.exists(gp) else set()
    mangler = [k for k in ut if k["lest"] != "ingen" and k["id"] not in med_rad and k["id"] not in utenfor]
    for k in mangler:
        print(f"{k['id']}\t{k['lest']}\t{k['tittel']}")
    print(f"{len(mangler)} kilder med tekst eller sammendrag uten rad i uttrekket.")
    return 1 if mangler else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if "--sjekk" in sys.argv:
        sys.exit(sjekk(sys.argv[1]))
    grupper(sys.argv[1], int(sys.argv[sys.argv.index("--storrelse") + 1]) if "--storrelse" in sys.argv else 25,
            kjerne="--kjerne" in sys.argv)
