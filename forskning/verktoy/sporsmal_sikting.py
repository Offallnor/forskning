"""Grov sikting av kandidater med en lett modell før de blinde utvalgene (steg 2 punkt 3 i LOYPE.md).

Bruk: python3 -I forskning/verktoy/sporsmal_sikting.py <mappe> --del <arbeidsmappe> [--bolk=300] [--alle]
       python3 -I forskning/verktoy/sporsmal_sikting.py <mappe> --samle <arbeidsmappe>

--del   deler alle kandidater (kandidater.jsonl og treff som bare står i de nordiske listene) i bolker
        <arbeidsmappe>/b01/, b02/ ... med kriterier.md og en kandidater.tsv med id, år, type, kilde, oversikt,
        land, tittel og sammendrag (avkortet til 600 tegn). Rekkefølgen stokkes med fast frø, så bolkene blir
        like og kjøringen kan gjentas. Hver bolk siktes av én kjøring etter verktoy/SIKTING.md.
--samle leser <arbeidsmappe>/b*/sikting.tsv og kontrollerer at hver kandidat har nøyaktig én beslutning.
        En forkortet id rettes når bare én kandidat i bolken begynner slik, og står da som varsel. Mangler
        en beslutning, regnes kandidaten som beholdt. Skriver sporsmal/<mappe>/sikting.tsv (id, beslutning,
        grunn, bolk) og en mappe <arbeidsmappe>/blind/ med inndataene til de blinde utvalgene, filtrert til
        de beholdte: kriterier.md, kandidater.jsonl, kandidater.tsv (prioritert rekkefølge),
        referanser*.tsv og de nordiske listene.

Finnes sporsmal/<mappe>/sikting.tsv fra før (en tidligere sikting), deler --del bare opp kandidatene som ikke er
siktet, og --samle legger de nye beslutningene til de gamle. Etter en ny referanserunde siktes da bare de nye
kandidatene. --alle med --del sikter alle på nytt.

Testet 10.11.2026: i aktivitetskravet (5 718
kandidater) beholdt Haiku 123 av 124 sterke kilder, og Opus-utvalget etter siktingen fant 79 prosent av dem
mot 63 prosent uten. I gradert sykmelding (754 kandidater) ga siktingen ingen gevinst.
"""
import csv, glob, json, os, random, shutil, sys

csv.field_size_limit(10**9)
ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LISTER = ("norske-kandidater.tsv", "svenske-kandidater.tsv", "finske-kandidater.tsv")
FRO = 20261110
TEGN = 600


def ren(t):
    return (t or "").replace("\t", " ").replace("\n", " ").replace("\r", " ")


def kandidater(sp):
    rader, sett = [], set()
    for l in open(os.path.join(sp, "kandidater.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        sett.add(r["id"])
        rader.append([r["id"], str(r.get("ar") or ""), r.get("type") or "", ren(r.get("kilde"))[:80],
                      str(bool(r.get("oversikt"))), ",".join(r.get("land") or []), ren(r.get("tittel")),
                      ren(r.get("sammendrag"))[:TEGN]])
    for navn in LISTER:
        sti = os.path.join(sp, navn)
        if not os.path.exists(sti):
            continue
        for r in csv.DictReader(open(sti, encoding="utf-8"), delimiter="\t"):
            if r["id"] not in sett:
                sett.add(r["id"])
                rader.append([r["id"], r.get("ar") or "", r.get("type") or "", ren(r.get("kilde"))[:80],
                              r.get("oversikt") or "", "", ren(r.get("tittel")), ""])
    return rader


def tidligere(sp):
    """Beslutninger fra en tidligere sikting: id -> (beslutning, grunn, bolk)."""
    sti = os.path.join(sp, "sikting.tsv")
    if not os.path.exists(sti):
        return {}
    return {r["id"]: (r["beslutning"], r["grunn"], r["bolk"]) for r in csv.DictReader(open(sti, encoding="utf-8"), delimiter="\t")}


def del_opp(sp, arb, bolk, alle=False):
    rader = kandidater(sp)
    gamle = {} if alle else tidligere(sp)
    if gamle:
        rader = [r for r in rader if r[0] not in gamle]
        print(f"{len(gamle)} kandidater er siktet før (sikting.tsv) og tas ikke med igjen")
    random.Random(FRO).shuffle(rader)
    n = -(-len(rader) // bolk)
    for i in range(n):
        d = os.path.join(arb, f"b{i + 1:02d}")
        os.makedirs(d, exist_ok=True)
        shutil.copy(os.path.join(sp, "kriterier.md"), d)
        with open(os.path.join(d, "kandidater.tsv"), "w", encoding="utf-8", newline="") as f:
            wr = csv.writer(f, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\")
            wr.writerow(["id", "ar", "type", "kilde", "oversikt", "land", "tittel", "sammendrag"])
            wr.writerows(rader[i * bolk:(i + 1) * bolk])
    print(f"{len(rader)} kandidater i {n} bolker under {arb}")


def les(sti):
    return [r for r in csv.reader(open(sti, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE) if r]


def skriv_prioritert(blind):
    """kandidater.tsv i prioritert rekkefølge for de beholdte, som sporsmal_sok.py --prioriter."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import sporsmal_sok
    gammel = sporsmal_sok.ROT
    os.makedirs(os.path.join(blind, "sporsmal", "x"), exist_ok=True)
    shutil.copy(os.path.join(blind, "kandidater.jsonl"), os.path.join(blind, "sporsmal", "x"))
    try:
        sporsmal_sok.ROT = blind
        sporsmal_sok.skriv_kandidater_tsv("x")
    finally:
        sporsmal_sok.ROT = gammel
    shutil.move(os.path.join(blind, "sporsmal", "x", "kandidater.tsv"), os.path.join(blind, "kandidater.tsv"))
    shutil.rmtree(os.path.join(blind, "sporsmal"))


def samle(mappe, sp, arb):
    utfall, varsler, alle = {}, [], set()
    for d in sorted(glob.glob(os.path.join(arb, "b[0-9]*"))):
        b = os.path.basename(d)
        ids = [r[0] for r in les(os.path.join(d, "kandidater.tsv"))[1:]]
        alle |= set(ids)
        sti = os.path.join(d, "sikting.tsv")
        if not os.path.exists(sti):
            varsler.append(f"{b}: sikting.tsv mangler, hele bolken regnes som beholdt")
            continue
        for r in les(sti)[1:]:
            i, beslutning = r[0].strip(), (r[1] if len(r) > 1 else "").strip().lower()
            grunn = r[2].strip() if len(r) > 2 else ""
            if i not in ids:
                treff = [x for x in ids if x.startswith(i)] if len(i) >= 8 else []
                if len(treff) != 1:
                    varsler.append(f"{b}: ukjent id {i}, ikke brukt")
                    continue
                varsler.append(f"{b}: forkortet id {i} rettet til {treff[0]}")
                i = treff[0]
            if i in utfall:
                varsler.append(f"{b}: {i} har to beslutninger, den første brukes")
                continue
            utfall[i] = ("behold" if beslutning.startswith("behold") else "forkast", grunn, b)
    for i in sorted(alle - set(utfall)):
        varsler.append(f"{i}: ingen beslutning, regnes som beholdt")
        utfall[i] = ("behold", "ingen beslutning", "")
    gamle = {i: v for i, v in tidligere(sp).items() if i not in utfall}
    if gamle:
        print(f"{len(gamle)} beslutninger fra en tidligere sikting er tatt med")
        utfall.update(gamle)
        alle |= set(gamle)
    beholdt = {i for i, (b, _, _) in utfall.items() if b == "behold"}
    with open(os.path.join(sp, "sikting.tsv"), "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, delimiter="\t")
        wr.writerow(["id", "beslutning", "grunn", "bolk"])
        for i in sorted(utfall):
            wr.writerow([i, *utfall[i]])
    blind = os.path.join(arb, "blind")
    os.makedirs(blind, exist_ok=True)
    shutil.copy(os.path.join(sp, "kriterier.md"), blind)
    with open(os.path.join(blind, "kandidater.jsonl"), "w", encoding="utf-8") as g:
        for l in open(os.path.join(sp, "kandidater.jsonl"), encoding="utf-8"):
            if json.loads(l)["id"] in beholdt:
                g.write(l)
    skriv_prioritert(blind)
    navn = [*LISTER] + sorted(os.path.basename(p) for p in glob.glob(os.path.join(sp, "referanser*.tsv")))
    for fn in navn:
        sti = os.path.join(sp, fn)
        if not os.path.exists(sti):
            continue
        linjer = open(sti, encoding="utf-8").read().split("\n")
        ut = [linjer[0]] + [l for l in linjer[1:] if l and l.split("\t")[0] in beholdt]
        open(os.path.join(blind, fn), "w", encoding="utf-8").write("\n".join(ut) + "\n")
    for v in varsler:
        print("VARSEL", v)
    print(f"{len(beholdt)} av {len(alle)} beholdt ({round(100 * len(beholdt) / max(len(alle), 1))} %). "
          f"Skrev sporsmal/{mappe}/sikting.tsv og {blind}/")


def main():
    if len(sys.argv) < 4 or sys.argv[2] not in ("--del", "--samle"):
        sys.exit(__doc__)
    mappe, modus, arb = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3])
    sp = os.path.join(ROT, "sporsmal", mappe)
    bolk = next((int(a.split("=", 1)[1]) for a in sys.argv[4:] if a.startswith("--bolk=")), 300)
    if modus == "--del":
        del_opp(sp, arb, bolk, alle="--alle" in sys.argv[4:])
    else:
        samle(mappe, sp, arb)


if __name__ == "__main__":
    main()
