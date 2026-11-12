"""Henter metadata og sammendrag fra NVA (Nasjonalt vitenarkiv, api.nva.unit.no) for temaene i forskning/temaer.tsv.

Skriver forskning/katalog/poster.jsonl (én post per linje, med feltet temaer) og forskning/katalog/telling.tsv.
En post som treffes av flere temaer, står én gang.
Henter ikke fulltekst. Bare forskningstyper (rapporter, artikler, kapitler, bøker, oversikter, doktorgrader) fra 2010.
Kjøres hver uke av .github/workflows/forskning-hent.yml.
"""
import csv, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

API = "https://api.nva.unit.no"
UA = "Mozilla/5.0 (kunnskapsoversikt; github.com/Offallnor/forskning)"
ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPER = ("ReportResearch,ReportBasic,ReportWorkingPaper,ReportPolicy,AcademicArticle,AcademicChapter,"
         "AcademicMonograph,AcademicLiteratureReview,DegreePhd")
FRA_AR = 2010
MAKS_PER_SOK = 300
OVERSIKT = re.compile(r"systematisk[e]? (oversikt|kartlegging)|systematic (review|mapping)|meta-?analy|kunnskapsoppsummering|"
                      r"scoping review|umbrella review|oversikt over oversikter|hurtigoversikt|rapid review|forskningskart|evidence and gap map", re.I)


def hent(url):
    for forsok in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(10 * (forsok + 1))
                continue
            raise
        except (urllib.error.URLError, TimeoutError):
            time.sleep(10 * (forsok + 1))
    raise RuntimeError(f"Fikk ikke hentet {url}")


def post(h):
    ed = h.get("entityDescription") or {}
    ref = ed.get("reference") or {}
    ctx = ref.get("publicationContext") or {}
    orgs = {(a.get("labels") or {}).get("nb") or (a.get("labels") or {}).get("en")
            for c in ed.get("contributors") or [] for a in c.get("affiliations") or [] if a.get("labels")}
    filer = [a for a in h.get("associatedArtifacts") or [] if a.get("type") == "OpenFile"]
    tittel = re.sub(r"\s+", " ", ed.get("mainTitle") or "").strip()
    sammendrag = (ed.get("abstract") or "").strip()
    return {
        "id": h["identifier"],
        "nva": f"https://nva.sikt.no/registration/{h['identifier']}",
        "tittel": tittel,
        "ar": (ed.get("publicationDate") or {}).get("year"),
        "type": (ref.get("publicationInstance") or {}).get("type"),
        "oversikt": bool(OVERSIKT.search(tittel + " " + sammendrag)) or (ref.get("publicationInstance") or {}).get("type") == "AcademicLiteratureReview",
        "doi": ref.get("doi") or h.get("doi"),
        "kanal": ctx.get("name") or (ctx.get("series") or {}).get("name") or (ctx.get("publisher") or {}).get("name"),
        "sprak": (ed.get("language") or "").rsplit("/", 1)[-1],
        "forfattere": [(c.get("identity") or {}).get("name") for c in ed.get("contributors") or []][:12],
        "institusjoner": sorted(o for o in orgs if o),
        "emneord": ed.get("tags") or [],
        "sammendrag": sammendrag,
        "apen_fil": bool(filer),
        "lisens": sorted({(f.get("license") or {}).get("name") for f in filer if f.get("license")}),
    }


def treffer(p, sok):
    """NVA-søket gir også treff der ordene bare står spredt eller i fulltekst. Behold bare poster
    der søkeordet (eller hele uttrykket) står i tittel, sammendrag eller emneord."""
    tekst = " ".join([p["tittel"], p["sammendrag"], " ".join(p["emneord"])]).lower()
    return sok.strip('"').lower() in tekst


def main():
    temaer = list(csv.DictReader(open(os.path.join(ROT, "temaer.tsv"), encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE))
    katalog = os.path.join(ROT, "katalog")
    os.makedirs(katalog, exist_ok=True)
    poster = {}
    for t in temaer:
        for sok in [s.strip() for s in t["sok"].split(";") if s.strip()]:
            fra, total = 0, None
            while fra < MAKS_PER_SOK:
                q = urllib.parse.urlencode({"query": sok, "instanceType": TYPER, "publicationYearSince": FRA_AR,
                                            "results": 100, "from": fra})
                d = hent(f"{API}/search/resources?{q}")
                total = d.get("totalHits")
                hits = d.get("hits") or []
                for h in hits:
                    p = poster.get(h["identifier"]) or post(h)
                    if not treffer(p, sok):
                        continue
                    p.setdefault("temaer", [])
                    p.setdefault("sok", [])
                    if t["id"] not in p["temaer"]:
                        p["temaer"].append(t["id"])
                    if sok not in p["sok"]:
                        p["sok"].append(sok)
                    poster[h["identifier"]] = p
                fra += 100
                if len(hits) < 100:
                    break
                time.sleep(1)
            print(f"{t['id']}\t{sok}\t{total} treff", flush=True)
    rader = sorted(poster.values(), key=lambda p: (str(p.get("ar") or ""), p["id"]), reverse=True)
    with open(os.path.join(katalog, "poster.jsonl"), "w", encoding="utf-8") as f:
        for p in rader:
            f.write(json.dumps(p, ensure_ascii=False, sort_keys=True) + "\n")
    for navn in os.listdir(katalog):
        if navn.endswith(".jsonl") and navn not in ("poster.jsonl", "arbeid-og-velferd.jsonl"):
            os.remove(os.path.join(katalog, navn))
    telling = []
    for t in temaer:
        r = [p for p in rader if t["id"] in p["temaer"]]
        telling.append([t["id"], len(r), sum(1 for p in r if p["sammendrag"]), sum(1 for p in r if p["oversikt"]),
                        sum(1 for p in r if p["apen_fil"]), sum(1 for p in r if len(p["temaer"]) > 1)])
    telling.append(["alle", len(rader), sum(1 for p in rader if p["sammendrag"]), sum(1 for p in rader if p["oversikt"]),
                    sum(1 for p in rader if p["apen_fil"]), sum(1 for p in rader if len(p["temaer"]) > 1)])
    with open(os.path.join(katalog, "telling.tsv"), "w", encoding="utf-8") as f:
        f.write("tema\tposter\tmed_sammendrag\toversikter\tmed_apen_fil\ti_flere_temaer\n")
        for r in telling:
            f.write("\t".join(map(str, r)) + "\n")
    print("\n".join("\t".join(map(str, r)) for r in telling))


if __name__ == "__main__":
    sys.exit(main())
