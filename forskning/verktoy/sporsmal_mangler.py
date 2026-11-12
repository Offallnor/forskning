"""Lager mangler.md: valgte kilder uten fulltekst, med lenker for å hente dem for hånd.

Bruk: python3 sporsmal_mangler.py <mappe> [<gren>]
"""
import csv, json, os, re, sys, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kilder  # noqa: E402

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "https://github.com/Offallnor/forskning-tekst"
RANG = {"oversikt": 1, "rct": 2, "kvasi": 3, "register": 4}


def main(mappe, gren="main"):
    d = os.path.join(ROT, "sporsmal", mappe)
    valgt = re.findall(r"^((?:W\d+|AV-[\d-]+|R-[0-9a-f]{10}|KU-[0-9a-f-]{36}|NB-\d+|LI-[0-9a-z]+|FI-[0-9A-Za-z._-]+|[0-9a-f]{12}-[0-9a-f-]{8,}))\s*#?\s*(.*)$", open(os.path.join(d, "valgt.txt"), encoding="utf-8").read(), re.M)
    kand = {}
    for l in open(os.path.join(d, "kandidater.jsonl"), encoding="utf-8"):
        if l.strip():
            r = json.loads(l); kand[r["id"].split("/")[-1]] = r
    design, abstrakt = {}, set()
    ep = os.path.join(d, "estimater.tsv")   # finnes ikke før uttrekket; da sorteres lista uten design
    for r in (csv.DictReader(open(ep, encoding="utf-8"), delimiter="\t") if os.path.exists(ep) else []):
        design.setdefault(r["id"], r["design"])
        if r["side"] == "sammendrag":
            abstrakt.add(r["id"])
    versjoner = {}
    vp = os.path.join(d, "versjoner.tsv")
    if os.path.exists(vp):
        for r in csv.DictReader(open(vp, encoding="utf-8"), delimiter="\t"):
            a = set(re.findall(r"[a-zæøå]{4,}", (kand.get(r["valgt"], {}).get("tittel") or "").lower()))
            b = set(re.findall(r"[a-zæøå]{4,}", (r.get("tittel") or "").lower()))
            if a and len(a & b) / len(a) >= 0.7:
                versjoner.setdefault(r["valgt"], []).append(r["versjon"])
    # Versjoner koblet for hånd i kommentarene i valgt.txt («samme materiale som <id>», «publisert versjon av <id>»).
    # Uten dette sto en studie som «ikke lest» selv om en annen versjon av den hadde tekst (lønnstilskudd for unge 11.11.2026).
    ID = r"W\d+|AV-[\d-]+|R-[0-9a-f]{10}|KU-[0-9a-f-]{36}|NB-\d+|LI-[0-9a-z]+|FI-[0-9A-Za-z._-]+|[0-9a-f]{12}-[0-9a-f-]{8,}"
    for l in open(os.path.join(d, "valgt.txt"), encoding="utf-8"):
        w, _, kommentar = l.partition("#")
        w = w.strip()
        for a in re.findall(ID, kommentar):
            if w and a != w:
                versjoner.setdefault(w, []).append(a)
                versjoner.setdefault(a, []).append(w)

    def har_tekst(w):
        return kilder.har_tekst(w, streng=True)

    ikke, bare, annen = [], [], []
    sett = set()
    for wid, kommentar in valgt:
        if wid in sett:
            continue
        sett.add(wid)
        if har_tekst(wid):
            continue
        k = kand.get(wid, {})
        rad = (RANG.get(design.get(wid, ""), 5), wid, k, kommentar, design.get(wid, ""))
        if any(har_tekst(v) for v in versjoner.get(wid, [])):
            annen.append(rad)
        else:
            (bare if wid in abstrakt else ikke).append(rad)
    opp = f"{REPO}/upload/{gren}/forskning/innboks"
    ut = [f"# Kilder som må hentes for hånd: {mappe}", "",
          f"Opplastingssiden: {opp}", "",
          "Slik henter du en kilde:", "",
          "1. Prøv lenken til forlaget først. Den virker ofte gjennom abonnementet til arbeidsplassen eller biblioteket.",
          "2. Prøv Google Scholar etterpå. Der ligger det ofte en åpen versjon hos forfatteren eller i et arkiv (se etter «[PDF]» til høyre).",
          f"3. Last ned PDF-en og dra den inn på [opplastingssiden]({opp}). Filnavnet spiller ingen rolle; kilden kjennes igjen på DOI eller tittel, og teksten kommer med neste gang svaret oppdateres.",
          "4. Finnes kilden ikke, eller er den bak betalingsmur, si fra. Da står den som ikke tilgjengelig i forbeholdene.", ""]
    for overskrift, rader in (("Ikke lest i det hele tatt", ikke), ("Bare sammendraget er lest", bare), ("En annen versjon er lest (lav prioritet)", annen)):
        ut += [f"## {overskrift} ({len(rader)})", ""]
        for _, wid, k, kommentar, ds in sorted(rader, key=lambda r: (r[0], r[1])):
            tittel = k.get("tittel") or kommentar
            forf = ", ".join((k.get("forfattere") or [])[:3]) if isinstance(k.get("forfattere"), list) else (k.get("forfattere") or "")
            lenker = []
            if k.get("doi"):
                lenker.append(f"[forlaget]({k['doi']})")
            lenker.append(f"[Google Scholar](https://scholar.google.com/scholar?q={urllib.parse.quote(tittel)})")
            if wid.startswith("W"):
                lenker.append(f"[OpenAlex](https://openalex.org/{wid})")
            elif k.get("apen_url"):
                navn = {"AV-": "nav.no", "KU-": "Kudos", "NB-": "Navs bibliotek", "LI-": "LIBRIS", "FI-": "Finna", "R-": "nettsiden"}.get(wid[:3] if wid[:3] in ("AV-", "KU-", "NB-", "LI-", "FI-") else wid[:2], "vitenarkivet")
                lenker.append(f"[{navn}]({k['apen_url']})")
            ut.append(f"- **{tittel}** ({forf}, {k.get('ar', '')}){', ' + ds if ds else ''}. {kommentar}  \n  {' · '.join(lenker)}")
        ut.append("")
    open(os.path.join(d, "mangler.md"), "w", encoding="utf-8").write("\n".join(ut))
    print(mappe, len(ikke), len(bare), len(annen))


if __name__ == "__main__":
    main(*sys.argv[1:])
