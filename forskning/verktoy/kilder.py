"""Felles kildebibliotek for forskningsspørsmålene: forskning/kilder/<id>/.

Hver kilde har én mappe, uansett hvor mange spørsmål som bruker den:

    kilde.json   metadata: tittel, forfattere, år, doi, lenke (oppføringen),
                 hentet_fra (adressen teksten eller fila ble hentet fra), hentet (dato),
                 hvordan (pdf, nav.no, Europe PMC, vitenarkivet, opplastet), merknad
                 (varsel fra tekstkontrollen) og fil (fil.pdf når fila er lagret)
    tekst.txt    teksten, med sideskift (\\f) når den kommer fra PDF
    fil.pdf      fila, bare når den er lastet opp for hånd

Brukes av sporsmal_sok.py, sporsmal_kontroll.py, sporsmal_mangler.py og forskning_innboks.py.
"""
import datetime, json, os

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KILDER = os.path.join(ROT, "kilder")
FELT = ("id", "tittel", "forfattere", "ar", "type", "kilde", "doi", "apen_url", "oversikt", "sammendrag")


def mappe(wid):
    return os.path.join(KILDER, wid)


def tekst_sti(wid):
    return os.path.join(mappe(wid), "tekst.txt")


def har_tekst(wid, streng=False):
    """Finnes teksten? Med streng=True: minst 2000 tegn, og sideskift eller minst 5000 tegn
    (en nettside uten sideskift med under 5000 tegn er trolig bare ingressen)."""
    p = tekst_sti(wid)
    if not os.path.exists(p):
        return False
    if not streng:
        return True
    t = open(p, encoding="utf-8", errors="replace").read().strip()
    return len(t) >= 2000 and ("\f" in t or len(t) >= 5000)


def les_tekst(wid):
    p = tekst_sti(wid)
    return open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else ""


def les_meta(wid):
    p = os.path.join(mappe(wid), "kilde.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def lenke(r):
    """Oppføringen brukeren kan åpne: OpenAlex, vitenarkivet eller nav.no."""
    wid = r.get("id", "")
    if wid.startswith("W"):
        return f"https://openalex.org/{wid}"
    if wid.startswith(("AV-", "R-", "KU-", "NB-", "LI-", "FI-")):
        return r.get("apen_url") or ""
    return f"https://nva.sikt.no/registration/{wid}"


def lagre_meta(wid, r=None, **nytt):
    """Skriver kilde.json. Felt fra kandidaten (r) fylles inn der de mangler; nytt overskriver."""
    os.makedirs(mappe(wid), exist_ok=True)
    m = les_meta(wid)
    for k in FELT:
        if r and r.get(k) not in (None, "", []) and not m.get(k):
            m[k] = r[k]
    m["id"] = wid
    if r and not m.get("lenke"):
        m["lenke"] = lenke(r)
    m.update({k: v for k, v in nytt.items() if v is not None})
    json.dump(m, open(os.path.join(mappe(wid), "kilde.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    return m


def lagre_tekst(wid, tekst, r=None, hentet_fra="", hvordan="", merknad=""):
    os.makedirs(mappe(wid), exist_ok=True)
    open(tekst_sti(wid), "w", encoding="utf-8").write(tekst)
    return lagre_meta(wid, r, hentet_fra=hentet_fra, hvordan=hvordan, merknad=merknad.strip(" ;"),
                      hentet=datetime.date.today().isoformat())
