#!/usr/bin/env python3
"""Lager vedlegg B og C til et forskningssvar.

Bruk: python3 -I forskning/verktoy/vedlegg_bc.py <mappe>

Vedlegg B (<mappe>/vedlegg-b.md): kilder som ikke er lest eller er utelatt.
  - Sentrale valgte kilder uten fulltekst: oversikter og kategori 1-3 (kategorien først i kommentaren i
    valgt.txt), delt i «ikke lest» og «bare sammendrag», med lenke. Antallet er det forbeholdene i svaret
    skal oppgi (kontroll 10 i sporsmal_kontroll.py).
  - Kilder utenfor kjernen (grupper.tsv), talt etter kategori.
  - Utelatte kandidater (utelatt.tsv): utelatte oversikter enkeltvis, resten gruppert etter begrunnelse.

Vedlegg C (<mappe>/vedlegg-metode.md): kort metode, med tall hentet fra filene i mappen: søkene
(sok-logg.tsv), kandidater etter kilde, referanserunder, grovsikting, blinde utvalg, valgte kilder,
uttrekk, innholdskontroll og automatiske kontroller. Vurderingene står i utvalg.md og metning.md, og
vedlegget viser til dem.

Ingen tall skrives inn for hånd. Kjør skriptet på nytt etter hver endring i utvalget eller uttrekket.
"""
import collections
import csv
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kilder  # noqa: E402
from sporsmal_grupper import kategorier, status  # noqa: E402

csv.field_size_limit(10**9)
KILDE = [("W", "OpenAlex"), ("AV-", "Arbeid og velferd"), ("KU-", "Kudos"), ("NB-", "Navs bibliotek"),
         ("LI-", "LIBRIS"), ("FI-", "Finna"), ("R-", "lagt inn med adresse")]


def kildenavn(wid):
    for p, navn in KILDE:
        if wid.startswith(p) and (p != "W" or wid[1:].isdigit()):
            return navn
    return "Nasjonalt vitenarkiv"


def lenke(wid, k):
    if re.fullmatch(r"W\d+", wid):
        return f"https://openalex.org/{wid}"
    return k.get("apen_url") or k.get("doi") or ""


def tsv(sti):
    return list(csv.DictReader(open(sti, encoding="utf-8"), delimiter="\t")) if os.path.exists(sti) else []


def uleste(mappe):
    """Sentrale valgte kilder uten fulltekst: (ikke lest, bare sammendrag), hver liste med (kategori, id, kandidat)."""
    sti, ut = status(mappe)
    kat = kategorier(sti)
    kand = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(sti, "kandidater.jsonl"), encoding="utf-8") if l.strip()}
    utenfor = {r["id"] for r in tsv(os.path.join(sti, "grupper.tsv")) if r["gruppe"].startswith("ikke uttrekk (")}
    # Versjoner: en kilde regnes som lest når en annen versjon av samme studie har tekst. Koblingen finnes i
    # kommentarene i valgt.txt («åpen versjon av <id>», «samme materiale som <id>») og i versjoner.tsv.
    ID = r"W\d+|AV-[\d-]+|R-[0-9a-f]{10}|KU-[0-9a-f-]{36}|NB-\d+|LI-[0-9a-z]+|FI-[0-9A-Za-z._-]+"
    par = collections.defaultdict(set)
    for l in open(os.path.join(sti, "valgt.txt"), encoding="utf-8"):
        wid, _, kommentar = l.partition("#")
        wid = wid.strip()
        for annen in re.findall(ID, kommentar):
            if wid and annen != wid:
                par[wid].add(annen)
                par[annen].add(wid)
    for r in tsv(os.path.join(sti, "versjoner.tsv")):
        par[r.get("valgt", "")].add(r.get("versjon", ""))
        par[r.get("versjon", "")].add(r.get("valgt", ""))
    ikke, bare = [], []
    for k in ut:
        wid = k["id"]
        if wid in utenfor or kilder.har_tekst(wid, streng=True):
            continue
        if any(a and kilder.har_tekst(a, streng=True) for a in par.get(wid, ())):
            continue
        c = kat.get(wid)
        if not (k["oversikt"] or (c is not None and c <= 3)):
            continue
        (bare if k["lest"] == "sammendrag" else ikke).append((1 if k["oversikt"] else c, wid, kand.get(wid, {})))
    return sorted(ikke, key=lambda r: (r[0], r[1])), sorted(bare, key=lambda r: (r[0], r[1]))


def vedlegg_b(mappe):
    sti = os.path.join(kilder.ROT, "sporsmal", mappe)
    ikke, bare = uleste(mappe)
    ut = [f"# Vedlegg B: kilder som ikke er lest eller er utelatt ({mappe})", "",
          f"Laget med `vedlegg_bc.py`. Sentrale kilder er oversikter og studier i kategori 1–3. "
          f"{len(ikke) + len(bare)} sentrale valgte kilder er ikke lest i fulltekst: {len(ikke)} ikke lest, "
          f"{len(bare)} bare i sammendrag. Hvordan de kan hentes, står i `mangler.md`.", ""]
    for overskrift, rader in (("Sentrale kilder som ikke er lest", ikke), ("Sentrale kilder som bare er lest i sammendrag", bare)):
        ut += [f"## {overskrift} ({len(rader)})", ""]
        for c, wid, k in rader:
            forf = k.get("forfattere") or []
            forf = ", ".join(forf[:3]) if isinstance(forf, list) else str(forf)
            adr = lenke(wid, k)
            tittel = k.get("tittel") or wid
            ut.append(f"- kategori {c}: {'[' + tittel + '](' + adr + ')' if adr else tittel} ({forf}, {k.get('ar') or ''})")
        ut.append("")
    utenfor = [r["id"] for r in tsv(os.path.join(sti, "grupper.tsv")) if r["gruppe"].startswith("ikke uttrekk (")]
    if utenfor:
        kat = kategorier(sti)
        n = collections.Counter(kat.get(w) for w in utenfor)
        ut += [f"## Valgt, men utenfor kjernen ({len(utenfor)})", "",
               "Uttrekket ble avgrenset til en kjerne. Disse kildene er valgt, men ikke hentet ut tall fra: "
               + ", ".join(f"{n[c]} i kategori {c}" for c in sorted(x for x in n if x)) + ". De står i `valgt.txt`.", ""]
    utelatt = tsv(os.path.join(sti, "utelatt.tsv"))
    if utelatt:
        kand = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(sti, "kandidater.jsonl"), encoding="utf-8") if l.strip()}
        oversikter = [r for r in utelatt if (kand.get(r["id"]) or {}).get("oversikt")]
        ut += [f"## Utelatte sentrale kandidater ({len(utelatt)})", "",
               "Sentrale kandidater (oversikter, høyt siterte) som ikke er valgt, med begrunnelse fra `utelatt.tsv`.", "",
               f"### Utelatte oversikter ({len(oversikter)})", ""]
        for r in sorted(oversikter, key=lambda r: -((kand[r["id"]].get("ar")) or 0)):
            k = kand[r["id"]]
            ut.append(f"- {k.get('tittel')} ({k.get('ar') or ''}): {r['begrunnelse']}")
        grupper = collections.Counter(r["begrunnelse"].strip() for r in utelatt if r not in oversikter)
        ut += ["", "### Andre utelatte, etter begrunnelse", "", "| Antall | Begrunnelse |", "|---|---|"]
        for b, n in grupper.most_common(40):
            ut.append(f"| {n} | {b.replace('|', '/')} |")
        rest = len(grupper) - 40
        if rest > 0:
            ut.append(f"| {sum(n for _, n in grupper.most_common()[40:])} | {rest} andre begrunnelser (se `utelatt.tsv`) |")
        ut.append("")
    open(os.path.join(sti, "vedlegg-b.md"), "w", encoding="utf-8").write("\n".join(ut))
    return len(ikke) + len(bare)


def vedlegg_c(mappe):
    sti = os.path.join(kilder.ROT, "sporsmal", mappe)
    kand = [json.loads(l) for l in open(os.path.join(sti, "kandidater.jsonl"), encoding="utf-8") if l.strip()]
    ut = [f"# Vedlegg C: kort metode ({mappe})", "",
          "Laget med `vedlegg_bc.py` fra filene i mappen. Mandat og kriterier står i `kriterier.md`, vurderingene av "
          "utvalg og metning i `utvalg.md` og `metning.md`, og fremgangsmåten i `forskning/LOYPE.md`.", "", "## Søk", ""]
    for r in tsv(os.path.join(sti, "sok-logg.tsv")):
        ord_ = [o.strip() for o in r["ord"].split("|") if o.strip() and not o.strip().startswith("--")]
        ut.append(f"- {r['dato']}, {r['modus'].lstrip('-')}: {len(ord_)} uttrykk")
    n = collections.Counter("referanser" if (r.get("sok") or [""])[0] == "referanse" else kildenavn(r["id"]) for r in kand)
    ut += ["", f"{len(kand)} kandidater i alt: " + ", ".join(f"{v} fra {k}" for k, v in n.most_common()) + ".", ""]
    runder = sorted(glob.glob(os.path.join(sti, "referanser-[0-9]*.tsv")), key=lambda p: int(re.findall(r"\d+", os.path.basename(p))[0]))
    if runder:
        ut += ["## Referanser", ""]
        for p in runder:
            rader = tsv(p)
            nye = sum(r.get("allerede_kandidat") == "False" for r in rader)
            ut.append(f"- runde {re.findall(r'\d+', os.path.basename(p))[0]}: {len(rader)} referansekandidater, {nye} nye")
        ut.append("")
    sikt = tsv(os.path.join(sti, "sikting.tsv"))
    if sikt:
        beholdt = sum(r["beslutning"] == "behold" for r in sikt)
        ut += ["## Grov sikting", "", f"{len(sikt)} kandidater siktet, {beholdt} beholdt ({round(100 * beholdt / len(sikt))} prosent).", ""]
    valgt = list(dict.fromkeys(l.split("#")[0].strip() for l in open(os.path.join(sti, "valgt.txt"), encoding="utf-8") if l.split("#")[0].strip()))
    ut += ["## Utvalg", "", f"{len(valgt)} linjer i `valgt.txt` (versjoner av samme studie telles hver for seg)."]
    for p in sorted(glob.glob(os.path.join(sti, "valgt-blind*.tsv"))):
        rader = tsv(p)
        funnet = sum(r["id"] in valgt for r in rader)
        ut.append(f"- blindt utvalg `{os.path.basename(p)}`: {len(rader)} kilder, {funnet} av dem i `valgt.txt`")
    ut.append("")
    _, st = status(mappe)
    lest = collections.Counter(k["lest"] for k in st)
    ut += ["## Uttrekk", "", f"Av de valgte har {lest['tekst']} fulltekst, {lest['sammendrag']} bare sammendrag og {lest['ingen']} ingen av delene."]
    for navn in ("estimater.tsv", "estimater-b.tsv"):
        rader = tsv(os.path.join(sti, navn))
        if rader:
            ut.append(f"- `{navn}`: {len(rader)} rader fra {len({r['id'] for r in rader})} kilder")
    ut.append("")
    ik = []
    for p in sorted(glob.glob(os.path.join(sti, "innholdskontroll*.tsv"))):
        ik += tsv(p)
    kontroll = os.path.join(sti, "kontroll.md")
    ut += ["## Kontroller", ""]
    if os.path.exists(kontroll):
        m = re.search(r"Kjørt (\S+)\.\s+(\d+) feil av (\d+) kontroller", open(kontroll, encoding="utf-8").read())
        if m:
            ut.append(f"- automatiske kontroller {m.group(1)}: {m.group(2)} feil av {m.group(3)} (`kontroll.md`)")
    budskap = tsv(os.path.join(sti, "budskap.tsv"))
    if budskap:
        ut.append(f"- blind lesing av {len({r['id'] for r in budskap})} kilder (`budskap.tsv`)")
    if ik:
        ut.append(f"- innholdskontroll: {len(ik)} punkter (`innholdskontroll*.tsv`)")
    if os.path.exists(os.path.join(sti, "sammenligning.md")):
        ut.append("- sammenligning av de to uttrekkene: `sammenligning.md`")
    ut.append("")
    open(os.path.join(sti, "vedlegg-metode.md"), "w", encoding="utf-8").write("\n".join(ut))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    n = vedlegg_b(sys.argv[1])
    vedlegg_c(sys.argv[1])
    print(f"Skrev vedlegg-b.md og vedlegg-metode.md. {n} sentrale valgte kilder er ikke lest i fulltekst.")
