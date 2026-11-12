"""Katalog over kunnskapsdokumenter fra offentlig sektor i Kudos (DFØ, kudos.dfo.no).

Bruk: python3 -I forskning/verktoy/kudos.py
Laster ned DFØs daglige CSV-eksport (ett kall, åpne data) og skriver katalogen med
dokumenttypene som kan være kilder til forskningsspørsmål: evalueringer, studier, kartlegginger,
kunnskapsoppsummeringer, NOU-er, områdegjennomganger og forhåndsutredninger, én fil per dokumenttype
(forskning/katalog/kudos/<type>.jsonl, så ingen fil blir for stor). Én linje per dokument:
id (KU-<uuid>, dokumentsiden er kudos.dfo.no/dokument/<uuid>), tittel, ar, type, forfattere, eiere, utforere, sammendrag,
pdf (fila i Kudos), kilde_url (fila hos eieren, ofte regjeringen.no).
Søket gjøres ikke mot Kudos-API-et, fordi det stenger etter noen raske kall. Henter ikke fulltekst.
"""
import csv, gzip, io, json, os, sys, time, urllib.request

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://kudos.dfo.no/api/v0/documents/download/csv"
UA = "Mozilla/5.0 (kunnskapsoversikt)"
TYPER = {"Evaluering", "Studie", "Kartlegging", "Kunnskapsoppsummering", "NOU", "Områdegjennomgang",
         "Forhåndsutredning", "Utredning", "Analyse"}


def hent():
    for forsok in range(4):
        try:
            req = urllib.request.Request(URL, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=300) as r:
                data = r.read()
            return gzip.decompress(data) if data[:2] == b"\x1f\x8b" else data
        except Exception as e:
            print(f"{type(e).__name__}: {URL}", flush=True)
            time.sleep(40 * (forsok + 1))   # grense: 2 kall i minuttet for eksporten
    return b""


def liste(s):
    return [x.strip() for x in (s or "").split("|") if x.strip()]


def main():
    data = hent()
    if not data:
        print("Fikk ikke hentet eksporten fra Kudos")
        return 1
    rader = csv.DictReader(io.StringIO(data.decode("utf-8-sig", "replace")), delimiter=";")
    typer, ut = {}, []
    for r in rader:
        typer[r.get("type")] = typer.get(r.get("type"), 0) + 1
        if r.get("type") not in TYPER:
            continue
        filer = liste(r.get("file_urls"))
        ut.append({"id": "KU-" + r["uuid"], "tittel": r.get("title") or "", "ar": int((r.get("publish_date") or "0")[:4] or 0) or None,
                   "type": r["type"], "forfattere": liste(r.get("authors"))[:8], "eiere": liste(r.get("owners")),
                   "utforere": liste(r.get("authoring_actors")), "sammendrag": (r.get("abstract") or "")[:4000],
                   "pdf": next((f for f in filer if f.lower().endswith(".pdf")), ""),
                   "kilde_url": (liste(r.get("source_file_urls")) or [r.get("external_public_url") or ""])[0]})
    if len(ut) < 1000:   # eksporten har over 20 000 dokumenter av disse typene; færre betyr trolig feil
        print(f"Bare {len(ut)} dokumenter, skriver ikke over katalogen. Typer: {typer}")
        return 1
    ut.sort(key=lambda r: r["id"])
    mappe = os.path.join(ROT, "katalog", "kudos")
    os.makedirs(mappe, exist_ok=True)
    for t in TYPER:
        p = os.path.join(mappe, t.lower().replace("ø", "o").replace("å", "a").replace("æ", "ae") + ".jsonl")
        mine = [r for r in ut if r["type"] == t]
        if not mine:
            continue
        with open(p, "w", encoding="utf-8") as f:
            for r in mine:
                f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"{len(ut)} dokumenter skrevet til {mappe}. Alle typer: {dict(sorted(typer.items(), key=lambda t: -t[1])[:25])}")


if __name__ == "__main__":
    sys.exit(main())
