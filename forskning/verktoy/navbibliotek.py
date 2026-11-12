"""Henter katalogen i Navs bibliotek (bibliotek.nav.no, Invenio) som JSON-linjer. Fra 9.11.2026.

Bruk: python3 -I forskning/verktoy/navbibliotek.py [utfil.jsonl]   (standard: forskning/katalog/navbibliotek.jsonl)

Kjøres hver uke av forskning-hent.yml. Biblioteket er mest fagbøker, så bare poster med lenke til
fulltekst tas med (om lag 700 av 5 200): Navs rapportserie, Fafo, NOVA, Oxford Research, Proba m.fl.
Blar gjennom alle poster med søket search?p=&of=xm (MARCXML, 200 per side) og skriver én linje per post:
id (NB-<nr>), tittel, ar, forfattere, korporasjon, utgiver, serie, sammendrag, emner, lenker (856u), side.
bibliotek.nav.no nås fra GitHub Actions, ikke fra skymiljøet.
"""
import json, re, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

BASE = "https://bibliotek.nav.no"
UA = "Mozilla/5.0 (kunnskapsoversikt; github.com/Offallnor/forskning)"
M = "{http://www.loc.gov/MARC21/slim}"


def hent(url):
    for forsok in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=120) as r:
                return r.read()
        except Exception as e:
            print(f"{type(e).__name__} ({forsok + 1}): {url}", flush=True)
            time.sleep(5 * (forsok + 1))
    return None


def felt(rec, tag, kode):
    return [sf.text.strip() for df in rec.findall(f"{M}datafield[@tag='{tag}']")
            for sf in df.findall(f"{M}subfield[@code='{kode}']") if sf.text and sf.text.strip()]


def post(rec):
    nr = (rec.findtext(f"{M}controlfield[@tag='001']") or "").strip()
    tittel = " : ".join(felt(rec, "245", "a")[:1] + felt(rec, "245", "b")[:1]).strip(" /:")
    ar = next((m.group(0) for t in felt(rec, "269", "a") + felt(rec, "264", "c") + felt(rec, "260", "c")
               for m in [re.search(r"(19|20)\d\d", t)] if m), None)
    return {"id": f"NB-{nr}", "tittel": tittel, "ar": int(ar) if ar else None,
            "forfattere": felt(rec, "100", "a") + felt(rec, "700", "a"),
            "korporasjon": felt(rec, "110", "a") + felt(rec, "710", "a"),
            "utgiver": (felt(rec, "264", "b") + felt(rec, "260", "b"))[:1],
            "serie": felt(rec, "490", "a") + felt(rec, "830", "a"),
            "sammendrag": " ".join(felt(rec, "520", "a")),
            "emner": felt(rec, "650", "a") + felt(rec, "653", "a"),
            "lenker": felt(rec, "856", "u"),
            "side": f"{BASE}/record/{nr}"}


def main(ut):
    alle, jrec = {}, 1
    while True:
        data = hent(f"{BASE}/search?" + urllib.parse.urlencode({"p": "", "of": "xm", "rg": 200, "jrec": jrec}))
        if not data:
            break
        recs = ET.fromstring(data).findall(f"{M}record")
        if not recs:
            break
        nye = 0
        for r in recs:
            p = post(r)
            if p["id"] not in alle:
                alle[p["id"]] = p
                nye += 1
        print(f"jrec {jrec}: {len(recs)} poster, {nye} nye, {len(alle)} til sammen", flush=True)
        if nye == 0:
            break
        jrec += len(recs)
        time.sleep(1)
    if len(alle) < 3000:   # biblioteket hadde 5 199 poster 9.11.2026; færre tyder på feil i hentingen
        sys.exit(f"Bare {len(alle)} poster hentet; katalogen skrives ikke over")
    med = [p for p in alle.values() if p["lenker"]]
    with open(ut, "w", encoding="utf-8") as fh:
        for p in sorted(med, key=lambda p: int(p["id"][3:] or 0)):
            fh.write(json.dumps(p, ensure_ascii=False) + "\n")
    print(f"{ut}: {len(med)} av {len(alle)} poster (de med lenke)")


if __name__ == "__main__":
    import os
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "katalog", "navbibliotek.jsonl"))
