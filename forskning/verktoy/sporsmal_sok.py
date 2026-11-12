"""Søker OpenAlex etter forskning på ett spørsmål og lagrer kandidater med sammendrag.

Bruk: python3 -I forskning/verktoy/sporsmal_sok.py <mappe> 'søk 1' 'søk 2' ...
       python3 -I forskning/verktoy/sporsmal_sok.py <mappe> --pdf   (henter tekst for id-ene i <mappe>/valgt.txt;
           id-er med «ingen pdf» i forrige pdf-logg.tsv hoppes over)
       python3 -I forskning/verktoy/sporsmal_sok.py <mappe> --pdf-alle   (som --pdf, men prøver alle id-er uten tekst på nytt)
       python3 -I forskning/verktoy/sporsmal_sok.py <mappe> --referanser 'uttrykk 1' ...   (følger referanser fra valgte kilder)
       python3 -I forskning/verktoy/sporsmal_sok.py <mappe> --norsk 'ord 1' ...   (søker i vitenarkivet og Arbeid og velferd med norske ord)
       python3 -I forskning/verktoy/sporsmal_sok.py <mappe> --svensk 'ord 1' ...   (søker i LIBRIS med svenske ord, blant annet rapportene fra IFAU og ISF)
       python3 -I forskning/verktoy/sporsmal_sok.py <mappe> --finsk 'ord 1' ...   (søker i Finna med finske eller svenske ord, blant annet rapportene fra Kela og THL)
       python3 -I forskning/verktoy/sporsmal_sok.py <mappe> --ssb <tabell> 'valueCodes[Tid]=top(5)&valueCodes[Region]=0' ...
           (henter en SSB-tabell som CSV til <mappe>/statistikk/ssb-<tabell>.csv; SSB nås bare fra Actions)
Skriver forskning/sporsmal/<mappe>/kandidater.jsonl og kandidater.tsv. Tekst og lenke legges i det felles
kildebiblioteket forskning/kilder/<id>/ (se kilder.py), og kilder som finnes der fra før, hentes ikke på nytt.
"""
import csv, json, os, re, subprocess, sys, tempfile, time, urllib.error, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kilder  # noqa: E402

API = "https://api.openalex.org"
UA = "Mozilla/5.0 (kunnskapsoversikt; github.com/Offallnor/forskning)"
ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOKKEL = os.environ.get("OPENALEX_API_KEY", "").strip()
OVERSIKT = re.compile(r"systematic review|meta-?analy|scoping review|literature review|systematisk|kunnskapsoppsummering|mapping review", re.I)


STERKT_DESIGN = re.compile(r"randomi[sz]|controlled trial|natural experiment|quasi-experiment|instrumental variable|"
                           r"regression discontinuity|discontinuity design|difference-in-difference|event stud|"
                           r"reform|policy change|lovendring|forsøk|randomiser|kvasi-eksperiment|naturlig eksperiment", re.I)
KANAL_OVERSIKT = re.compile(r"cochrane|campbell systematic", re.I)


def prioritet(r):
    """Rekkefølge for lesing av kandidater (kvalitet først, ingen tak). Bare rekkefølge,
    ikke utvalg: alle kandidater kan velges, men de sterkeste leses først. Forfatterrangering brukes ikke."""
    tekst = (r.get("tittel") or "") + " " + (r.get("sammendrag") or "")[:1500]
    tittel = (r.get("tittel") or "").lower()
    ord_ = [re.sub(r'"', "", o).lower() for o in r.get("sok") or [] if o not in ("referanse", "valgt", "versjon")]
    grunner = []
    if r.get("oversikt"):
        grunner.append(("oversikt", 3))
    if STERKT_DESIGN.search(tekst):
        grunner.append(("design", 3))
    if any(o and o in tittel for o in ord_):
        grunner.append(("ord i tittel", 2))
    if KANAL_OVERSIKT.search((r.get("kilde") or "") + " " + tittel):
        grunner.append(("Cochrane/Campbell", 2))
    if set(r.get("land") or []) & {"NO", "SE", "DK", "FI", "IS"}:
        grunner.append(("nordisk", 1))
    if (r.get("persentil") or 0) >= 0.9 or (r.get("siteringer") or 0) >= 50:
        grunner.append(("sitert", 1))
    if svakt_treff(r):
        grunner.append(("svak", -3))
    return sum(v for _, v in grunner), ", ".join(g for g, _ in grunner)


def skriv_kandidater_tsv(mappe):
    """kandidater.tsv med alle kandidater fra alle søk og referanser, sortert etter prioritet."""
    ut = os.path.join(ROT, "sporsmal", mappe)
    sti = os.path.join(ut, "kandidater.jsonl")
    if not os.path.exists(sti):
        return
    rader = [json.loads(l) for l in open(sti, encoding="utf-8")]
    med = [(prioritet(r), r) for r in rader]
    med.sort(key=lambda x: (-x[0][0], -((x[1].get("persentil") or 0)), -(x[1].get("siteringer") or 0)))
    with open(os.path.join(ut, "kandidater.tsv"), "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, delimiter="\t")
        wr.writerow(["id", "prioritet", "grunn", "kildebase", "ar", "oversikt", "siteringer", "persentil", "apen", "land", "tittel", "kilde", "doi"])
        for (p, g), r in med:
            wr.writerow([r["id"], p, g, r.get("kildebase") or ("OpenAlex" if r["id"].startswith("W") else ""), r.get("ar"), r.get("oversikt"),
                         r.get("siteringer"), r.get("persentil"), r.get("apen"), ",".join(r.get("land") or []), r.get("tittel"), r.get("kilde"), r.get("doi")])


def logg_sok(mappe, modus, ordene):
    """Lagrer søkeordene for hver kjøring i sok-logg.tsv, så søket kan gjentas nøyaktig (stegtest 10.11.2026:
    det første søket i de eldste mappene sto ikke i kjor.sh)."""
    import datetime
    ut = os.path.join(ROT, "sporsmal", mappe)
    os.makedirs(ut, exist_ok=True)
    sti = os.path.join(ut, "sok-logg.tsv")
    ny = not os.path.exists(sti)
    with open(sti, "a", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, delimiter="\t")
        if ny:
            wr.writerow(["dato", "modus", "ord"])
        wr.writerow([datetime.date.today().isoformat(), modus, " | ".join(ordene)])


DODE_VERTER = set()   # verter som ikke svarte (tidsavbrudd, DNS, nektet tilkobling) i denne kjøringen


def hent(url, raa=False):
    vert = urllib.parse.urlparse(url).netloc
    api = vert.startswith("api.") or "openalex" in vert or "ebi.ac.uk" in vert
    if vert in DODE_VERTER:
        print(f"hopper over (verten svarte ikke tidligere i kjøringen): {url[:150]}", flush=True)
        return None
    if NOKKEL and "openalex" in url:
        url += ("&" if "?" in url else "?") + "api_key=" + urllib.parse.quote(NOKKEL)
    for forsok in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,text/html;q=0.9,*/*;q=0.8"})
            with urllib.request.urlopen(req, timeout=60 if api else 30) as r:
                data = r.read()
                return data if raa else json.loads(data)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                if e.code == 429:   # logges, så en brukt opp OpenAlex-kvote synes i loggen
                    print(f"HTTP 429 (forsøk {forsok + 1}): {url.split('api_key=')[0][:150]}", flush=True)
                time.sleep(3 * (forsok + 1)); continue
            print(f"HTTP {e.code}: {url.split('api_key=')[0][:150]}", flush=True)
            return None
        except Exception as e:
            print(f"{type(e).__name__}: {url.split('api_key=')[0][:150]}", flush=True)
            if not api:
                # Nettsider som ikke svarer, prøves ikke på nytt: fem forsøk à 60 sekunder tok mye av tiden i Actions
                DODE_VERTER.add(vert)
                return None
            time.sleep(3)
    return None


def sammendrag(w):
    inv = w.get("abstract_inverted_index") or {}
    pos = [(i, ord_) for ord_, ix in inv.items() for i in ix]
    return " ".join(o for _, o in sorted(pos))


def rad(w, sok):
    bo = w.get("best_oa_location") or {}
    pl = w.get("primary_location") or {}
    abs_ = sammendrag(w)
    pdfs = [l.get("pdf_url") for l in w.get("locations") or [] if l.get("pdf_url")]
    return {
        "id": w["id"].rsplit("/", 1)[1], "tittel": w.get("title") or "", "ar": w.get("publication_year"),
        "type": w.get("type"), "kilde": (pl.get("source") or {}).get("display_name") or "",
        "doi": w.get("doi") or "", "forfattere": [a["author"]["display_name"] for a in w.get("authorships") or []][:8],
        "land": sorted({c for a in w.get("authorships") or [] for c in a.get("countries") or []}),
        "siteringer": w.get("cited_by_count"), "persentil": (w.get("citation_normalized_percentile") or {}).get("value"),
        "oversikt": bool(OVERSIKT.search((w.get("title") or "") + " " + abs_[:600])) or w.get("type") == "review",
        "apen": bool((w.get("open_access") or {}).get("is_oa")),
        "apen_url": bo.get("pdf_url") or bo.get("landing_page_url") or "", "pdf_urler": pdfs,
        "sammendrag": abs_, "sok": [sok],
    }


def sok_modus(mappe, sokene):
    ut = os.path.join(ROT, "sporsmal", mappe)
    os.makedirs(ut, exist_ok=True)
    alle = {}
    fra = 1994
    for s in [s for s in sokene if s.startswith("--fra=")]:
        fra = int(s[6:]) - 1
    sokene = [s for s in sokene if not s.startswith("--fra=")]
    for s in sokene:
        # Alle fraser i anførselstegn må stå i tittel eller sammendrag; uten anførselstegn gjelder hele søket
        fraser = [f.lower() for f in re.findall(r'"([^"]+)"', s)] or [s.lower()]
        for side in (1, 2):
            q = urllib.parse.urlencode({"search": s, "per_page": 100, "page": side, "filter": f"publication_year:>{fra}"})
            d = hent(f"{API}/works?{q}") or {}
            n = 0
            for w in d.get("results") or []:
                r = rad(w, s)
                tekst = (r["tittel"] + " " + r["sammendrag"]).lower()
                if not all(f in tekst for f in fraser):
                    continue
                n += 1
                if r["id"] in alle:
                    alle[r["id"]]["sok"].append(s)
                else:
                    alle[r["id"]] = r
            print(f"{s} side {side}: {len(d.get('results') or [])} treff, {n} med uttrykket i tittel/sammendrag", flush=True)
            time.sleep(0.5)
    # Flettes med kandidatene som finnes fra før, så et nytt engelsk søk i en gjenopptatt mappe ikke sletter
    # norske, svenske og finske treff eller referanser (feil funnet 9.11.2026).
    sti = os.path.join(ut, "kandidater.jsonl")
    gamle = [json.loads(l) for l in open(sti, encoding="utf-8")] if os.path.exists(sti) else []
    ider = {r["id"]: r for r in gamle}
    nye = []
    for r in sorted(alle.values(), key=lambda r: (-r["oversikt"], -(r["siteringer"] or 0))):
        if r["id"] in ider:
            ider[r["id"]]["sok"] = list(dict.fromkeys((ider[r["id"]].get("sok") or []) + r["sok"]))
        else:
            nye.append(r)
    rader = gamle + nye
    with open(sti, "w", encoding="utf-8") as f:
        for r in rader:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{len(alle)} treff, {len(nye)} nye kandidater, {len(rader)} kandidater i alt")


def hent_json(url):
    """JSON fra API-er som ikke er OpenAlex (Europe PMC, NVA)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"{type(e).__name__}: {url[:150]}", flush=True)
        return None


def tittel_treff(tittel, tekst):
    ordene = re.findall(r"[a-zæøåäöü]{4,}", tittel.lower())
    start = tekst[:20000].lower()
    return sum(o in start for o in ordene) / max(1, len(ordene))


APNE_VERSJONER = ("medrxiv", "biorxiv", "arxiv", "ssrn", "repec", "iza.org", "nber.org", "econstor", "osf.io", "researchgate", "cepr.org", "ifau.se", "workingpaper", "working-paper", "discussion")


def tekst_merknad(tp, r, url=""):
    """Varsler om tekst som trolig er skannet (lite tekst per side) eller kan være feil dokument
    (førsteforfatterens etternavn står ikke i starten). Teksten beholdes; se pdf-logg.tsv og sjekk for hånd."""
    t = open(tp, encoding="utf-8", errors="replace").read()
    sider = t.count("\f") + 1
    merk = []
    if len(t.strip()) < 2000 or len(t.strip()) / sider < 500:
        merk.append(f"LITE TEKST: {len(t.strip())} tegn på {sider} sider, trolig skannet")
    elif sider == 1 and len(t.strip()) < 5000:
        merk.append(f"LITE TEKST: {len(t.strip())} tegn, trolig bare ingress eller sammendrag")
    utgiver = r.get("kildebase") == "LIBRIS" and "ifau" in url.lower() and re.search(r"IFAU|arbetsmarknadspolitisk utvärdering", r.get("kilde", ""), re.I)
    if url and any(v in url.lower() for v in APNE_VERSJONER) and not utgiver:   # IFAUs egen rapport er ikke en åpen versjon
        merk.append("ÅPEN VERSJON (preprint eller arbeidsnotat), merkes i svaret")
    forf = [f for f in r.get("forfattere") or [] if f]
    if forf:
        import unicodedata
        uten = lambda x: "".join(c for c in unicodedata.normalize("NFKD", x.lower()) if not unicodedata.combining(c))
        etternavn = re.findall(r"[a-zøæ-]{3,}", uten(forf[0]))
        if etternavn and etternavn[-1] not in uten(t[:20000]):
            merk.append(f"SJEKK DOKUMENT: «{forf[0]}» står ikke i starten")
    return (" (" + "; ".join(merk) + ")") if merk else ""

def europepmc_tekst(doi, pmcid):
    """Fulltekst som XML fra Europe PMC (åpne artikler i PubMed Central), gjort om til ren tekst.
    Teksten får ikke sidetall; hele artikkelen er side 1."""
    if not pmcid and doi:
        d = hent_json("https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(
            {"query": f'DOI:"{doi}"', "format": "json", "resultType": "lite"})) or {}
        for r in (d.get("resultList") or {}).get("result") or []:
            if r.get("pmcid"):
                pmcid = r["pmcid"]; break
    if not pmcid:
        return None, None
    pmcid = pmcid if pmcid.upper().startswith("PMC") else "PMC" + pmcid
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
    data = hent(url, raa=True)
    if not data or b"<body" not in data:
        return None, url
    x = data.decode("utf-8", "replace")
    x = re.sub(r"<(ref-list|back)[\s>].*?</\1>", " ", x, flags=re.S)
    x = re.sub(r"</(p|title|sec|tr|caption|abstract|article-title)>", "\n", x)
    x = re.sub(r"</t[dh]>", "\t", x)
    x = re.sub(r"<[^>]+>", "", x)
    import html as _h
    x = _h.unescape(x)
    x = re.sub(r"[ \t]+\n", "\n", re.sub(r"\n{3,}", "\n\n", x)).strip()
    return x, url


def nva_pdf(tittel, doi):
    """PDF fra Nasjonalt vitenarkiv (tidligere Brage), slått opp på DOI eller tittel."""
    api = "https://api.nva.unit.no"
    for q in [doi, tittel]:
        if not q:
            continue
        d = hent_json(f"{api}/search/resources?" + urllib.parse.urlencode({"query": q, "results": 5})) or {}
        for h in d.get("hits") or []:
            t = (h.get("entityDescription") or {}).get("mainTitle") or ""
            # Vitenarkivet har ofte undertittel med; alle ordene i vår tittel må finnes der, ikke omvendt
            if tittel_treff(tittel, t) < 0.8 or tittel_treff(t, tittel) < 0.5:
                continue
            ident = h.get("identifier")
            for a in h.get("associatedArtifacts") or []:
                if a.get("type") != "OpenFile" or not a.get("identifier"):
                    continue
                link = hent_json(f"{api}/publication/{ident}/filelink/{a['identifier']}") or {}
                url = link.get("id") or link.get("url") or next((v for v in link.values() if isinstance(v, str) and v.startswith("http")), None)
                if url:
                    data = hent(url, raa=True)
                    if data and data[:4] == b"%PDF":
                        return data, f"https://nva.sikt.no/registration/{ident}"
    return None, None


def finn_pdf(url, dybde=0):
    """Henter url. Er svaret en nettside, følges citation_pdf_url og pdf-lenker (ett nivå)."""
    data = hent(url, raa=True)
    if not data:
        return None, url
    if data[:4] == b"%PDF":
        return data, url
    if dybde > 0:
        return None, url
    html = data.decode("utf-8", "replace")
    lenker = re.findall(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', html, re.I)
    lenker += re.findall(r'href=["\']([^"\']+(?:\.pdf|/bitstream/[^"\']+|download[^"\']*))["\']', html, re.I)
    sett = []
    for l in lenker:
        l = urllib.parse.urljoin(url, l.replace("&amp;", "&"))
        if l not in sett:
            sett.append(l)
    for l in sett[:4]:
        d, u = finn_pdf(l, 1)
        if d:
            return d, u
    print(f"ingen pdf på {url[:120]} ({len(sett)} lenker prøvd)", flush=True)
    return None, url


def pdf_modus(mappe, alle=False):
    ut = os.path.join(ROT, "sporsmal", mappe)
    # Id-er som ikke ga tekst forrige gang, prøves ikke på nytt (lange tekstrunder ga tidsavbrudd i køen)
    forrige = {}
    if not alle and os.path.exists(os.path.join(ut, "pdf-logg.tsv")):
        for l in open(os.path.join(ut, "pdf-logg.tsv"), encoding="utf-8"):
            d = l.rstrip("\n").split("\t")
            if len(d) > 1 and d[1].startswith("ingen pdf"):
                forrige[d[0]] = l.rstrip("\n")
    # avvist.txt (valgfri): kilder der en hentet tekst var feil dokument og er slettet. De hentes ikke automatisk
    # igjen, men en tekst som lastes opp i innboksen, brukes. Én id per linje, gjerne med grunn etter #.
    avvist_fil = os.path.join(ut, "avvist.txt")
    avvist = {l.split("#")[0].strip() for l in open(avvist_fil, encoding="utf-8")} - {""} if os.path.exists(avvist_fil) else set()
    tekst = tempfile.mkdtemp()   # arbeidsmappe for PDF og pdftotext; teksten lagres i kildebiblioteket
    kand = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(ut, "kandidater.jsonl"), encoding="utf-8")}
    logg = []

    def lagre(wid, tp, r, url, hvordan):
        merk = tekst_merknad(tp, r, url)
        kilder.lagre_tekst(wid, open(tp, encoding="utf-8", errors="replace").read(), r, url, hvordan, merk.strip(" ()"))
        os.remove(tp)
        return merk

    for linje in open(os.path.join(ut, "valgt.txt"), encoding="utf-8"):
        wid = linje.split("#")[0].strip()
        if not wid:
            continue
        # Åpen versjon funnet for hånd, f.eks. på forfatterens hjemmeside: «W123  # ... pdf: <adresse>».
        # Adressen prøves først, også når kilden ga «ingen pdf» før. Tittelkontrollen gjelder som ellers.
        ekstra = re.findall(r"pdf:\s*(https?://\S+)", linje.partition("#")[2])
        if wid.startswith("url:"):
            # Rapport som ikke finnes i databasene (regjeringen.no o.l.):
            # url: <adresse> | <tittel> | <forfattere, kommaseparert> | <år>
            import hashlib
            deler = [d.strip() for d in linje.split("#")[0][4:].split("|")]
            adr = deler[0]
            wid = "R-" + hashlib.sha1(adr.encode()).hexdigest()[:10]
            if wid not in kand:
                kand[wid] = {"id": wid, "tittel": deler[1] if len(deler) > 1 else adr, "ar": int(deler[3]) if len(deler) > 3 and deler[3].isdigit() else None,
                             "type": "report", "kilde": urllib.parse.urlparse(adr).netloc, "doi": "",
                             "forfattere": [f.strip() for f in deler[2].split(",")] if len(deler) > 2 and deler[2] else [],
                             "land": ["NO"], "siteringer": None, "persentil": None, "oversikt": False, "apen": True,
                             "apen_url": adr, "pdf_urler": [adr] if adr.lower().endswith(".pdf") else [], "sammendrag": "", "sok": ["url"]}
                with open(os.path.join(ut, "kandidater.jsonl"), "a", encoding="utf-8") as f:
                    f.write(json.dumps(kand[wid], ensure_ascii=False) + "\n")
            print(f"{adr} har id {wid}", flush=True)
        if wid.startswith("tittel:"):
            # Kilde som søket ikke fant: slå opp på tittel og ta første treff med tittelen
            t = wid[7:].strip()
            d = hent(f"{API}/works?" + urllib.parse.urlencode({"filter": "title.search:" + t, "per_page": 5})) or {}
            treff = [w for w in d.get("results") or [] if t.lower() in (w.get("title") or "").lower()]
            if not treff:
                logg.append(f"{wid}\tfinnes ikke"); continue
            r = rad(treff[0], "valgt")
            wid = r["id"]
            if wid not in kand:
                kand[wid] = r
                with open(os.path.join(ut, "kandidater.jsonl"), "a", encoding="utf-8") as f:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
        har_tekst = kilder.har_tekst(wid)
        if har_tekst and wid in kand:
            kilder.lagre_meta(wid, kand[wid])
            logg.append(f"{wid}\tok\t(i kildebiblioteket){kilder.les_meta(wid).get('hentet_fra') and ' ' + kilder.les_meta(wid)['hentet_fra'] or ''}"); continue
        if wid in avvist and not ekstra:
            logg.append(f"{wid}\tingen pdf (avvist.txt: feil dokument før, last opp for hånd)"); continue
        if wid in forrige and not ekstra:
            logg.append(forrige[wid] if "forrige runde" in forrige[wid] else forrige[wid].replace("ingen pdf", "ingen pdf (forrige runde)", 1))
            continue
        r = kand.get(wid)
        w = (hent(f"{API}/works/{wid}") or {}) if re.fullmatch(r"W\d+", wid) else {}
        urler = []
        for loc in w.get("locations") or []:
            urler += [loc.get("pdf_url"), loc.get("landing_page_url")]
        pmc = ((w.get("ids") or {}).get("pmcid") or "").rsplit("/", 1)[-1]
        if pmc:
            urler.append(f"https://europepmc.org/backend/ptpmcrender.fcgi?accid={pmc}&blobtype=pdf")
        if not r:
            r = rad(w, "valgt") if w else None
            if r:
                kand[wid] = r
                with open(os.path.join(ut, "kandidater.jsonl"), "a", encoding="utf-8") as f:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
        if not r:
            logg.append(f"{wid}\tfinnes ikke"); continue
        if wid.startswith(("LI-", "FI-")):   # lenkene i LIBRIS og Finna er ofte gamle: let også hos IFAU og i OpenAlex på tittelen
            urler += libris_reserve(r)
        if har_tekst:   # teksten finnes, men metadata manglet i kandidatene
            kilder.lagre_meta(wid, r)
            logg.append(f"{wid}\tok\t(hentet før, metadata lagt til)"); continue
        ok = False
        prov = []
        for u in ekstra + r["pdf_urler"] + ([r["apen_url"]] if r["apen_url"] else []) + urler:
            if u and u not in prov:
                prov.append(u)
        for url in prov:
            data, url = finn_pdf(url)
            if data:
                p = os.path.join(tekst, wid + ".pdf")
                open(p, "wb").write(data)
                tp = os.path.join(tekst, wid + ".txt")
                subprocess.run(["pdftotext", p, tp])
                os.remove(p)
                # Kontroll: teksten må handle om riktig kilde (ordene i tittelen står i starten av teksten)
                ordene = re.findall(r"[a-zæøåäöü]{4,}", r["tittel"].lower())
                start = open(tp, encoding="utf-8", errors="replace").read()[:20000].lower() if os.path.exists(tp) else ""
                treff = sum(o in start for o in ordene) / max(1, len(ordene))
                if treff < 0.7:
                    if os.path.exists(tp):
                        os.remove(tp)
                    logg.append(f"{wid}\tfeil dokument ({treff:.0%} av tittelordene)\t{url}")
                    continue
                logg.append(f"{wid}\tok{lagre(wid, tp, r, url, 'pdf')}\t{url}"); ok = True; break
        if not ok and wid.startswith("AV-"):
            # Arbeid og velferd uten egen PDF: artikkelen står som tekst på nav.no
            side = (hent(r["apen_url"], raa=True) or b"").decode("utf-8", "replace")
            m = re.search(r"<article.*?</article>", side, re.S)
            if m:
                import html as _h
                t = _h.unescape(re.sub(r"<[^>]+>", "\n", re.sub(r"<(script|style).*?</\1>", "", m.group(0), flags=re.S)))
                t = re.sub(r"\n\s*\n+", "\n", t).strip()
                if len(t) >= 2000 and tittel_treff(r["tittel"], t) >= 0.7:
                    open(os.path.join(tekst, wid + ".txt"), "w", encoding="utf-8").write(t)
                    logg.append(f"{wid}\tok (nav.no, uten sidetall){lagre(wid, os.path.join(tekst, wid + '.txt'), r, r['apen_url'], 'nav.no')}\t{r['apen_url']}"); ok = True
        if not ok:
            # Reserve 1: fulltekst fra Europe PMC (mange åpne artikler stenger for skript hos forlaget)
            t, url = europepmc_tekst((r.get("doi") or "").replace("https://doi.org/", ""), pmc)
            if t and tittel_treff(r["tittel"], t) >= 0.7:
                open(os.path.join(tekst, wid + ".txt"), "w", encoding="utf-8").write(t)
                logg.append(f"{wid}\tok (Europe PMC, uten sidetall){lagre(wid, os.path.join(tekst, wid + '.txt'), r, url, 'Europe PMC')}\t{url}"); ok = True
        if not ok:
            # Reserve 2: Nasjonalt vitenarkiv (Brage-lenkene virker ikke lenger)
            data, url = nva_pdf(r["tittel"], (r.get("doi") or "").replace("https://doi.org/", ""))
            if data:
                p = os.path.join(tekst, wid + ".pdf"); tp = p[:-4] + ".txt"
                open(p, "wb").write(data); subprocess.run(["pdftotext", p, tp]); os.remove(p)
                if os.path.exists(tp) and tittel_treff(r["tittel"], open(tp, encoding="utf-8", errors="replace").read()) >= 0.7:
                    logg.append(f"{wid}\tok (vitenarkivet){lagre(wid, tp, r, url, 'vitenarkivet')}\t{url}"); ok = True
                elif os.path.exists(tp):
                    os.remove(tp)
        if not ok:   # metadata lagres likevel, så kilden kan leses inn fra innboksen senere
            logg.append(f"{wid}\tingen pdf\t{r['tittel'][:80]}")
            kilder.lagre_meta(wid, r)
    open(os.path.join(ut, "pdf-logg.tsv"), "w", encoding="utf-8").write("\n".join(logg) + "\n")
    print("\n".join(logg))


NVA_TYPER = ("ReportResearch,ReportBasic,ReportWorkingPaper,ReportPolicy,AcademicArticle,AcademicChapter,"
             "AcademicMonograph,AcademicLiteratureReview,DegreePhd,DegreeMaster")


def norm_tittel(t):
    return " ".join(re.findall(r"[a-zæøåäöü0-9]+", (t or "").lower()))


def etternavn(r):
    return {re.split(r"[ ,]+", f.strip())[-1].lower() for f in r.get("forfattere") or [] if f and f.strip()} | \
           {re.split(r",", f)[0].strip().lower() for f in r.get("forfattere") or [] if f and "," in f}


def samme_kilde(a, b):
    """Samme tittel er nok for lange titler. Korte titler (under fire ord, som «Gradert sykmelding») må også ha
    samme år og minst ett felles etternavn når begge har det (9.11.2026: en Nav-rapport ble koblet til en
    artikkel i Tannlegetidende med samme tittel)."""
    ta = norm_tittel(a.get("tittel"))
    if not ta or ta != norm_tittel(b.get("tittel")):
        return False
    if len(ta.split()) >= 4:
        return True
    if a.get("ar") and b.get("ar") and abs(a["ar"] - b["ar"]) > 1:
        return False
    ea, eb = etternavn(a), etternavn(b)
    return not (ea and eb) or bool(ea & eb)


def finn_kjent(r, kand):
    """Id-en til en kjent kandidat som er samme kilde som r, ellers tom streng."""
    t = norm_tittel(r.get("tittel"))
    return next((k["id"] for k in kand if norm_tittel(k.get("tittel")) == t and samme_kilde(r, k)), "") if t else ""


def nva_rad(h, sok):
    ed = h.get("entityDescription") or {}
    ref = ed.get("reference") or {}
    ctx = ref.get("publicationContext") or {}
    tittel = re.sub(r"\s+", " ", ed.get("mainTitle") or "").strip()
    abs_ = (ed.get("abstract") or "").strip()
    typ = (ref.get("publicationInstance") or {}).get("type")
    filer = [a for a in h.get("associatedArtifacts") or [] if a.get("type") == "OpenFile"]
    return {
        "id": h["identifier"], "tittel": tittel, "ar": int((ed.get("publicationDate") or {}).get("year") or 0) or None,
        "type": typ, "kilde": ctx.get("name") or (ctx.get("series") or {}).get("name") or (ctx.get("publisher") or {}).get("name") or "",
        "doi": ref.get("doi") or h.get("doi") or "", "forfattere": [(c.get("identity") or {}).get("name") for c in ed.get("contributors") or []][:8],
        "land": ["NO"], "siteringer": None, "persentil": None,
        "oversikt": bool(OVERSIKT.search(tittel + " " + abs_[:600])) or typ == "AcademicLiteratureReview",
        "apen": bool(filer), "apen_url": f"https://nva.sikt.no/registration/{h['identifier']}", "pdf_urler": [],
        "sammendrag": abs_, "sok": [sok], "kildebase": "vitenarkivet",
    }


def norsk_modus(mappe, ordene):
    """Norske kilder som OpenAlex mangler: Nasjonalt vitenarkiv (rapporter fra FHI, ISF, Frisch, NORCE m.fl.,
    masteroppgaver), Kudos (evalueringer, utredninger, NOU-er og områdegjennomganger fra offentlig sektor),
    Navs bibliotek (rapporter med lenke, katalog/navbibliotek.jsonl) og Navs tidsskrift Arbeid og velferd (katalog/arbeid-og-velferd.jsonl).
    Et ord må stå i tittel, sammendrag eller emneord. Nye kilder legges til i kandidater.jsonl,
    og alle treff listes i norske-kandidater.tsv."""
    ut = os.path.join(ROT, "sporsmal", mappe)
    kand = [json.loads(l) for l in open(os.path.join(ut, "kandidater.jsonl"), encoding="utf-8")]
    treff = {}
    for o in ordene:
        n = 0
        for fra in range(0, 300, 100):
            d = hent_json("https://api.nva.unit.no/search/resources?" + urllib.parse.urlencode(
                {"query": o, "instanceType": NVA_TYPER, "results": 100, "from": fra})) or {}
            hits = d.get("hits") or []
            for h in hits:
                r = nva_rad(h, o)
                tekst = " ".join([r["tittel"], r["sammendrag"], " ".join((h.get("entityDescription") or {}).get("tags") or [])]).lower()
                if o.lower() not in tekst:
                    continue
                n += 1
                if r["id"] in treff:
                    treff[r["id"]]["sok"].append(o)
                else:
                    treff[r["id"]] = r
            if len(hits) < 100:
                break
            time.sleep(1)
        print(f"vitenarkivet: {o}: {n} treff med ordet", flush=True)
    for r in kudos_sok(ordene):
        if r["id"] in treff:
            treff[r["id"]]["sok"] += r["sok"]
        else:
            treff[r["id"]] = r
    kudos = list(treff.values())
    for r in navbibliotek_sok(ordene):   # samme rapport står ofte også i Kudos: Kudos-posten beholdes
        if not finn_kjent(r, kudos):
            treff[r["id"]] = r
    av = os.path.join(ROT, "katalog", "arbeid-og-velferd.jsonl")
    for l in open(av, encoding="utf-8") if os.path.exists(av) else []:
        a = json.loads(l)
        tekst = (a["tittel"] + " " + a.get("sammendrag", "")).lower()
        for o in ordene:
            if o.lower() in tekst:
                if a["id"] in treff:
                    treff[a["id"]]["sok"].append(o)
                else:
                    treff[a["id"]] = {
                        "id": a["id"], "tittel": a["tittel"], "ar": a["ar"], "type": "article", "kilde": a["kilde"], "doi": "",
                        "forfattere": a.get("forfattere", [])[:8], "land": ["NO"], "siteringer": None, "persentil": None,
                        "oversikt": bool(OVERSIKT.search(tekst[:800])), "apen": bool(a.get("pdf")), "apen_url": a["url"],
                        "pdf_urler": [a["pdf"]] if a.get("pdf") else [], "sammendrag": a.get("sammendrag", ""), "sok": [o],
                        "kildebase": "Arbeid og velferd"}
    nye = []
    ider = {k["id"] for k in kand}
    for r in treff.values():
        r["finnes_fra_for"] = "" if r["id"] in ider else finn_kjent(r, kand)
        if not r["finnes_fra_for"] and r["id"] not in ider:
            nye.append(r)
    with open(os.path.join(ut, "kandidater.jsonl"), "a", encoding="utf-8") as f:
        for r in nye:
            f.write(json.dumps({k: v for k, v in r.items() if k != "finnes_fra_for"}, ensure_ascii=False) + "\n")
    with open(os.path.join(ut, "norske-kandidater.tsv"), "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, delimiter="\t")
        wr.writerow(["id", "kildebase", "ar", "type", "oversikt", "apen", "finnes_fra_for", "antall_sok", "svak", "tittel", "kilde", "forfattere"])
        for r in sorted(treff.values(), key=lambda r: (svakt_treff(r), -len(r["sok"]), -(r["ar"] or 0))):
            wr.writerow([r["id"], r["kildebase"], r["ar"], r["type"], r["oversikt"], r["apen"], r["finnes_fra_for"], len(r["sok"]),
                         "ja" if svakt_treff(r) else "", r["tittel"], r["kilde"], "; ".join(x for x in r["forfattere"] if x)])
    print(f"{len(treff)} norske treff, {len(nye)} nye kandidater")


def svakt_treff(r):
    """Treff fra Kudos eller Navs bibliotek der bare ett enkeltord står i sammendraget, ikke i tittelen.
    Kudos dekker hele staten, så korte ord som «egenandel» eller «dekningsgrad» gir mange treff fra andre sektorer.
    Slike treff beholdes, men sorteres sist og merkes «svak» i norske-kandidater.tsv (testet 9.11.2026: de fleste
    var støy, men evalueringen av skjermingsordningen kom bare inn slik)."""
    if r.get("kildebase") == "Finna":
        # Finna søker i emneord for hele nasjonalbiblioteket, så sammensatte finske ord gir mye støy
        # (gradert sykmelding 9.11.2026: 317 Finna-treff, fem valgt). Svak når ingen av søkeordene står i tittelen.
        return not any(o.lower() in (r["tittel"] or "").lower() for o in r["sok"])
    if r.get("kildebase") not in ("Kudos", "Navs bibliotek") or len(r["sok"]) > 1:
        return False
    o = r["sok"][0]
    return " " not in o.strip() and o.lower() not in (r["tittel"] or "").lower()


def navbibliotek_sok(ordene):
    """Navs bibliotek (bibliotek.nav.no): rapporter med lenke til fulltekst, blant annet Navs rapportserie, Fafo,
    NOVA, Oxford Research og Proba, fra katalogen katalog/navbibliotek.jsonl (verktoy/navbibliotek.py).
    Ordet må stå i tittel, sammendrag eller emneord."""
    p = os.path.join(ROT, "katalog", "navbibliotek.jsonl")
    if not os.path.exists(p):
        print("Navs bibliotek: katalogen mangler (kjør verktoy/navbibliotek.py)", flush=True)
        return []
    treff = {}
    for l in open(p, encoding="utf-8"):
        k = json.loads(l)
        if re.match(r"\s*årsrapport", k["tittel"] or "", re.I):   # Navs årsrapporter er ikke forskning og ga treff i nesten alle spørsmål
            continue
        tekst = " ".join([k["tittel"], k.get("sammendrag", ""), " ".join(k.get("emner") or [])]).lower()
        for o in ordene:
            if o.lower() not in tekst:
                continue
            if k["id"] in treff:
                treff[k["id"]]["sok"].append(o); continue
            lenker = k.get("lenker") or []
            pdf = [u for u in lenker if u.lower().endswith(".pdf") or "/files/" in u]
            treff[k["id"]] = {
                "id": k["id"], "tittel": k["tittel"], "ar": k.get("ar"), "type": "report",
                "kilde": "Navs bibliotek: " + ", ".join((k.get("utgiver") or []) + (k.get("korporasjon") or [])[:1]),
                "doi": next((u for u in lenker if "doi.org/" in u), ""),
                "forfattere": (k.get("forfattere") or [])[:8], "land": ["NO"], "siteringer": None, "persentil": None,
                "oversikt": bool(OVERSIKT.search(tekst[:800])), "apen": True, "apen_url": k["side"],
                "pdf_urler": pdf + [u for u in lenker if u not in pdf], "sammendrag": k.get("sammendrag", ""),
                "sok": [o], "kildebase": "Navs bibliotek"}
    for o in ordene:
        print(f"Navs bibliotek: {o}: {sum(o in r['sok'] for r in treff.values())} treff med ordet", flush=True)
    return list(treff.values())


def kudos_sok(ordene):
    """Kudos (DFØ): evalueringer, utredninger, NOU-er, områdegjennomganger og andre kunnskapsdokumenter fra
    offentlig sektor, fra katalogen katalog/kudos/*.jsonl (verktoy/kudos.py). Ordet må stå i tittel eller sammendrag."""
    import glob
    filer = sorted(glob.glob(os.path.join(ROT, "katalog", "kudos", "*.jsonl")))
    treff = {}
    for l in (l for p in filer for l in open(p, encoding="utf-8")):
        k = json.loads(l)
        tekst = (k["tittel"] + " " + k.get("sammendrag", "")).lower()
        for o in ordene:
            if o.lower() not in tekst:
                continue
            if k["id"] in treff:
                treff[k["id"]]["sok"].append(o); continue
            pdf = [u for u in (k.get("pdf"), k.get("kilde_url")) if u and u.lower().endswith(".pdf")]
            treff[k["id"]] = {
                "id": k["id"], "tittel": k["tittel"], "ar": k.get("ar"), "type": k.get("type") or "",
                "kilde": "Kudos: " + (", ".join(k.get("eiere") or []) or "offentlig dokument"), "doi": "",
                "forfattere": k.get("forfattere") or [], "land": ["NO"], "siteringer": None, "persentil": None,
                "oversikt": bool(OVERSIKT.search(tekst[:800])) or k.get("type") == "Kunnskapsoppsummering",
                "apen": bool(pdf), "apen_url": "https://kudos.dfo.no/dokument/" + k["id"][3:], "pdf_urler": pdf, "sammendrag": k.get("sammendrag", ""),
                "sok": [o], "kildebase": "Kudos"}
    for o in ordene:
        print(f"Kudos: {o}: {sum(o in r['sok'] for r in treff.values())} treff med ordet", flush=True)
    if not filer:
        print("Kudos: katalogen mangler (kjør verktoy/kudos.py)", flush=True)
    return list(treff.values())


def libris_rad(p, sok):
    """Én post fra LIBRIS Xsearch (format_level=full). LIBRIS har sjelden sammendrag, så treffet bygger på katalogfeltene."""
    def liste(v):
        return v if isinstance(v, list) else [v] if v else []
    bib = (p.get("identifier") or "").rstrip("/").rsplit("/", 1)[-1]
    tittel = re.sub(r"\s+", " ", " ".join(liste(p.get("title")))).strip(" /:")
    ar = next((int(m) for m in re.findall(r"(?:19|20)\d\d", " ".join(map(str, liste(p.get("date")))))), None)
    lenker = [u for v in p.values() for u in (liste(v) if not isinstance(v, dict) else []) if isinstance(u, str) and u.startswith("http")]
    pdf = [u for u in lenker if u.lower().endswith(".pdf") or "urn.kb.se" in u or "/bitstream/" in u]
    andre = [u for u in lenker if u not in pdf and "libris.kb.se" not in u]
    sammendrag = " ".join(map(str, liste(p.get("summary")) + liste(p.get("description")) + liste(p.get("subject"))))
    return {
        "id": "LI-" + bib, "tittel": tittel, "ar": ar, "type": p.get("type") or "",
        "kilde": "LIBRIS: " + "; ".join(map(str, liste(p.get("publisher"))))[:200], "doi": "",
        "forfattere": [re.sub(r",\s*\d{4}-?(\d{4})?$", "", str(c)).strip() for c in liste(p.get("creator"))][:8],
        "land": ["SE"], "siteringer": None, "persentil": None,
        "oversikt": bool(OVERSIKT.search(tittel + " " + sammendrag) or re.search(r"forskningsöversikt|kunskapsöversikt|litteraturöversikt", tittel, re.I)),
        "apen": bool(pdf or andre), "apen_url": p.get("identifier") or "", "pdf_urler": pdf + andre,
        "sammendrag": sammendrag[:4000], "sok": [sok], "kildebase": "LIBRIS"}


def libris_reserve(r):
    """Andre adresser for en LIBRIS-post: IFAUs nettsøk (rapporter og working papers) og OpenAlex-treff på tittelen."""
    base = re.split(r" : |\. |\? ", r["tittel"])[0].strip()
    fold = lambda t: norm_tittel(t).translate(str.maketrans("åäöæø", "aaoao"))
    ordene = [o for o in fold(base).split() if len(o) > 3]
    urler = []
    if re.search(r"IFAU|arbetsmarknadspolitisk utvärdering", r.get("kilde", ""), re.I):
        side = (hent("https://www.ifau.se/Sok/?" + urllib.parse.urlencode({"q": base}), raa=True) or b"").decode("utf-8", "replace")
        for l in dict.fromkeys(re.findall(r'href="([^"]+)"', side)):
            slug = fold(l.rsplit("/", 2)[-2] if l.endswith("/") else l.rsplit("/", 1)[-1]).replace("-", " ")
            if ordene and sum(o in slug for o in ordene) / len(ordene) >= 0.6:
                urler.append(urllib.parse.urljoin("https://www.ifau.se/", l))
    d = hent(f"{API}/works?" + urllib.parse.urlencode({"filter": "title.search:" + base, "per_page": 5})) or {}
    for w in d.get("results") or []:
        if tittel_treff(base, w.get("title") or "") >= 0.8 and (not r.get("ar") or abs((w.get("publication_year") or 0) - r["ar"]) <= 1):
            for loc in w.get("locations") or []:
                urler += [loc.get("pdf_url"), loc.get("landing_page_url")]
    return [u for u in urler if u]


def svensk_modus(mappe, ordene):
    """Svenske rapporter som OpenAlex mangler: LIBRIS (Kungliga biblioteket), som har rapportseriene til IFAU,
    ISF, Försäkringskassan og andre myndigheter. Nye kilder legges til i kandidater.jsonl, og alle treff listes
    i svenske-kandidater.tsv. Søkeordene bør være svenske uttrykk med to ord eller mer. Med --fra=ÅR tas bare
    poster fra det året og senere med. Trykt og elektronisk utgave med samme tittel og år slås sammen."""
    fra = next((int(o[6:]) for o in ordene if o.startswith("--fra=")), 1995)
    ordene = [o for o in ordene if not o.startswith("--fra=")]
    ut = os.path.join(ROT, "sporsmal", mappe)
    kand = [json.loads(l) for l in open(os.path.join(ut, "kandidater.jsonl"), encoding="utf-8")]
    treff = {}
    for o in ordene:
        n = 0
        for start in (1, 201):
            d = hent_json("http://libris.kb.se/xsearch?" + urllib.parse.urlencode(
                {"query": o, "format": "json", "format_level": "full", "n": 200, "start": start})) or {}
            poster = (d.get("xsearch") or {}).get("list") or []
            for p in poster:
                r = libris_rad(p, o)
                if not r["tittel"] or r["id"] == "LI-" or (fra and (r["ar"] or 0) < fra):
                    continue
                n += 1
                nokkel = (norm_tittel(re.split(r" : |\. |\? ", r["tittel"])[0]), r["ar"])
                f = treff.get(r["id"]) or next((t for t in treff.values() if t["_nokkel"] == nokkel), None)
                if f:   # samme post, eller trykt og elektronisk utgave: behold den med lenke
                    if o not in f["sok"]:
                        f["sok"].append(o)
                    if r["pdf_urler"] and not f["pdf_urler"]:
                        f.update({k: r[k] for k in ("id", "apen", "apen_url", "pdf_urler")})
                    continue
                r["_nokkel"] = nokkel
                treff[r["id"]] = r
            if len(poster) < 200:
                break
            time.sleep(1)
        print(f"LIBRIS: {o}: {n} treff", flush=True)
        time.sleep(1)
    skriv_treff(ut, kand, treff, "svenske-kandidater.tsv", "svenske")


def skriv_treff(ut, kand, treff, filnavn, navn):
    """Legger nye treff til i kandidater.jsonl og skriver alle treff til <filnavn> (svensk og finsk søk)."""
    treff = {r["id"]: {k: v for k, v in r.items() if k != "_nokkel"} for r in treff.values()}
    nye = []
    ider = {k["id"] for k in kand}
    for r in treff.values():
        r["finnes_fra_for"] = "" if r["id"] in ider else finn_kjent(r, kand)
        if not r["finnes_fra_for"] and r["id"] not in ider:
            nye.append(r)
    with open(os.path.join(ut, "kandidater.jsonl"), "a", encoding="utf-8") as f:
        for r in nye:
            f.write(json.dumps({k: v for k, v in r.items() if k != "finnes_fra_for"}, ensure_ascii=False) + "\n")
    with open(os.path.join(ut, filnavn), "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, delimiter="\t")
        wr.writerow(["id", "ar", "type", "oversikt", "apen", "finnes_fra_for", "antall_sok", "svak", "tittel", "kilde", "forfattere"])
        for r in sorted(treff.values(), key=lambda r: (svakt_treff(r), -len(r["sok"]), -(r["ar"] or 0))):
            wr.writerow([r["id"], r["ar"], r["type"], r["oversikt"], r["apen"], r["finnes_fra_for"], len(r["sok"]),
                         "ja" if svakt_treff(r) else "", r["tittel"], r["kilde"], "; ".join(x for x in r["forfattere"] if x)])
    print(f"{len(treff)} {navn} treff, {len(nye)} nye kandidater")


def finna_rad(p, sok):
    """Én post fra Finna (det finske nasjonalbibliotekets søk, åpent API under CC0). Feltene kan være tekst eller objekter."""
    navn = lambda x: (x if isinstance(x, str) else (x or {}).get("name") or (x or {}).get("translated") or "") if not isinstance(x, list) else " ".join(map(str, x))
    tittel = re.sub(r"\s+", " ", p.get("title") or "").strip(" /:")
    ar = int(p["year"]) if str(p.get("year") or "").isdigit() else None
    lenker = [u.get("url") if isinstance(u, dict) else u for u in (p.get("onlineUrls") or []) + (p.get("urls") or [])]
    lenker = [u for u in lenker if isinstance(u, str) and u.startswith("http")]
    pdf = [u for u in lenker if u.lower().endswith(".pdf")] + [u for u in lenker if not u.lower().endswith(".pdf")]
    emner = " ".join(navn(e) for e in p.get("subjects") or [])
    sammendrag = " ".join(navn(x) for x in p.get("summary") or [])
    utgiver = "; ".join(navn(x) for x in p.get("publishers") or []) or "; ".join(navn(x) for x in p.get("series") or [])
    forf = [navn(a) for a in (p.get("primaryAuthors") or p.get("nonPresenterAuthors") or [])]
    forf = [f for f in forf if f]
    format_ = navn((p.get("formats") or [""])[-1])
    return {
        "id": "FI-" + re.sub(r"[^0-9A-Za-z._-]", "_", p.get("id") or ""), "tittel": tittel, "ar": ar, "type": format_,
        "kilde": ("Finna: " + utgiver)[:200], "doi": "", "forfattere": forf[:8], "land": ["FI"], "siteringer": None, "persentil": None,
        "oversikt": bool(OVERSIKT.search(tittel + " " + sammendrag) or re.search(r"katsaus|kirjallisuuskatsaus|forskningsöversikt", tittel, re.I)),
        "apen": bool(pdf), "apen_url": "https://www.finna.fi/Record/" + urllib.parse.quote(p.get("id") or ""), "pdf_urler": pdf,
        "sammendrag": (sammendrag + (" Emneord: " + emner if emner else ""))[:4000], "sok": [sok], "kildebase": "Finna"}


def finsk_modus(mappe, ordene):
    """Finske rapporter og artikler som OpenAlex mangler: Finna, med blant annet Kelas og THLs rapporter.
    Søkeordene kan være finske eller svenske. Med --fra=ÅR tas bare poster fra det året og senere med.
    Avisartikler, bacheloroppgaver (AMK og kandidat) og lyd og video tas ikke med."""
    fra = next((int(o[6:]) for o in ordene if o.startswith("--fra=")), 1995)
    ordene = [o for o in ordene if not o.startswith("--fra=")]
    ut = os.path.join(ROT, "sporsmal", mappe)
    kand = [json.loads(l) for l in open(os.path.join(ut, "kandidater.jsonl"), encoding="utf-8")]
    felt = ["id", "title", "year", "formats", "languages", "nonPresenterAuthors", "primaryAuthors", "publishers", "series",
            "subjects", "summary", "onlineUrls", "urls"]
    treff = {}
    for o in ordene:
        n = 0
        for side in (1, 2, 3):
            d = hent_json("https://api.finna.fi/v1/search?" + urllib.parse.urlencode(
                [("lookfor", o), ("limit", 100), ("page", side), ("filter[]", f'search_daterange_mv:"[{fra} TO 2100]"')] + [("field[]", f) for f in felt])) or {}
            poster = d.get("records") or []
            for p in poster:
                r = finna_rad(p, o)
                if not r["tittel"] or r["id"] == "FI-" or (fra and (r["ar"] or 0) < fra) or re.search(r"sanomalehti|avis|newspaper|AMK-opinnäytetyö|Kandityö|^CD$|Äänite|Video|Elokuva|Film|Peli|Kartta|Nuotti|Musiikki|Lehti$|Tidskrift$|Journal$", r["type"], re.I):
                    continue
                n += 1
                nokkel = (norm_tittel(r["tittel"]), r["ar"])
                f = treff.get(r["id"]) or next((t for t in treff.values() if t["_nokkel"] == nokkel), None)
                if f:
                    if o not in f["sok"]:
                        f["sok"].append(o)
                    if r["pdf_urler"] and not f["pdf_urler"]:
                        f.update({k: r[k] for k in ("id", "apen", "apen_url", "pdf_urler")})
                    continue
                r["_nokkel"] = nokkel
                treff[r["id"]] = r
            if len(poster) < 100:
                break
            time.sleep(1)
        print(f"Finna: {o}: {n} treff", flush=True)
        time.sleep(1)
    skriv_treff(ut, kand, treff, "finske-kandidater.tsv", "finske")


def valgte_id(ut):
    ids = []
    for linje in open(os.path.join(ut, "valgt.txt"), encoding="utf-8"):
        wid = linje.split("#")[0].strip()
        if re.fullmatch(r"W\d+", wid):
            ids.append(wid)
    est = os.path.join(ut, "estimater.tsv")
    if os.path.exists(est):
        ids += [r["id"] for r in csv.DictReader(open(est, encoding="utf-8"), delimiter="\t") if re.fullmatch(r"W\d+", r["id"])]
    return sorted(set(ids))


def referanse_modus(mappe, uttrykk):
    """Følger referanser bakover (det de valgte kildene viser til) og forover (det som viser til dem).
    En kandidat tas med når minst to valgte kilder peker på den, eller når ett av uttrykkene står i tittel/sammendrag."""
    ut = os.path.join(ROT, "sporsmal", mappe)
    valgt = valgte_id(ut)
    kand = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(ut, "kandidater.jsonl"), encoding="utf-8")}
    # referanser-fulgt.txt (valgfri, eldre ordning): kilder som er fulgt i en tidligere runde, hoppes over helt, også
    # pekerne deres. Trengs ikke lenger, fordi referanser-hentet.jsonl under gjør det samme uten å miste pekere.
    # Filen utvides med kildene som følges nå, bare når den finnes.
    fulgt_fil = os.path.join(ut, "referanser-fulgt.txt")
    fulgt = set(open(fulgt_fil, encoding="utf-8").read().split()) if os.path.exists(fulgt_fil) else set()
    if fulgt:
        print(f"hopper over {len(fulgt & set(valgt))} kilder som er fulgt før (referanser-fulgt.txt)", flush=True)
    bak, fram = {}, {}
    # referanser-hentet.jsonl: lager over referansene til hver kilde som er fulgt. Hver kilde skrives dit så snart
    # referansene er hentet, så en runde som stopper på tidsgrensen eller på kvoten, fortsetter der den slapp, og en
    # ny runde slår bare opp de nye kildene. Pekerne fra de gamle kildene telles likevel med, så regelen om to
    # pekere virker som før. Kilder der et oppslag feilet, lagres ikke og prøves igjen. Fila beholdes mellom rundene.
    mellom = os.path.join(ut, "referanser-hentet.jsonl")
    hentet = {}
    if os.path.exists(mellom):
        for l in open(mellom, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                hentet[r["id"]] = r
        print(f"{len(hentet)} kilder er hentet før og slås ikke opp på nytt (referanser-hentet.jsonl)", flush=True)
    for wid in [v for v in valgt if v not in fulgt]:
        if wid in hentet:
            rb, rf = hentet[wid]["bakover"], hentet[wid]["forover"]
        else:
            w = hent(f"{API}/works/{wid}?select=id,referenced_works")
            ok = w is not None
            rb = [r.rsplit("/", 1)[1] for r in (w or {}).get("referenced_works") or []]
            rf = []
            for side in (1, 2, 3):
                d = hent(f"{API}/works?filter=cites:{wid}&per_page=200&page={side}&select=id")
                ok = ok and d is not None
                res = (d or {}).get("results") or []
                rf += [r["id"].rsplit("/", 1)[1] for r in res]
                if len(res) < 200:
                    break
            if ok:
                with open(mellom, "a", encoding="utf-8") as f:
                    f.write(json.dumps({"id": wid, "bakover": rb, "forover": rf}) + "\n")
            time.sleep(0.2)
        for r in rb:
            bak.setdefault(r, set()).add(wid)
        for r in rf:
            fram.setdefault(r, set()).add(wid)
    if os.path.exists(fulgt_fil):
        open(fulgt_fil, "w", encoding="utf-8").write("\n".join(sorted(fulgt | set(valgt))) + "\n")
    alle = (set(bak) | set(fram)) - set(valgt)
    print(f"{len(valgt)} valgte kilder, {len(bak)} referanser bakover, {len(fram)} forover, {len(alle)} nye", flush=True)
    meta = {}
    liste = sorted(alle)
    for i in range(0, len(liste), 50):
        d = hent(f"{API}/works?filter=openalex:{'|'.join(liste[i:i+50])}&per_page=50") or {}
        for w in d.get("results") or []:
            r = rad(w, "referanse")
            meta[r["id"]] = r
        time.sleep(0.2)
    fraser = [u.lower() for u in uttrykk]
    rader = []
    for wid, r in meta.items():
        nb, nf = len(bak.get(wid, ())), len(fram.get(wid, ()))
        tekst = (r["tittel"] + " " + r["sammendrag"]).lower()
        treff = [f for f in fraser if f in tekst]
        if nb >= 2 or nf >= 2 or treff:
            r["bakover"], r["forover"], r["uttrykk"] = nb, nf, treff
            rader.append(r)
    rader.sort(key=lambda r: (-(r["bakover"] + r["forover"]), -(r["siteringer"] or 0)))
    with open(os.path.join(ut, "referanser.tsv"), "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, delimiter="\t")
        wr.writerow(["id", "bakover", "forover", "uttrykk", "ar", "oversikt", "siteringer", "persentil", "sammendrag", "allerede_kandidat", "tittel", "kilde"])
        for r in rader:
            wr.writerow([r["id"], r["bakover"], r["forover"], ";".join(r["uttrykk"]), r["ar"], r["oversikt"], r["siteringer"], r["persentil"],
                         bool(r["sammendrag"]), r["id"] in kand, r["tittel"], r["kilde"]])
    # Hver runde tas vare på som referanser-<n>.tsv; referanser.tsv er alltid siste runde
    n = 1
    while os.path.exists(os.path.join(ut, f"referanser-{n}.tsv")):
        n += 1
    import shutil
    shutil.copy(os.path.join(ut, "referanser.tsv"), os.path.join(ut, f"referanser-{n}.tsv"))
    nye = [r for r in rader if r["id"] not in kand]
    with open(os.path.join(ut, "kandidater.jsonl"), "a", encoding="utf-8") as f:
        for r in nye:
            f.write(json.dumps({k: v for k, v in r.items() if k not in ("bakover", "forover", "uttrykk")}, ensure_ascii=False) + "\n")
    print(f"{len(rader)} referansekandidater, {len(nye)} nye i kandidatlisten")


def versjon_modus(mappe):
    """For valgte kilder uten tekst: finn andre oppføringer i OpenAlex med samme tittel (arbeidsnotat, preprint)."""
    ut = os.path.join(ROT, "sporsmal", mappe)
    kand = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(ut, "kandidater.jsonl"), encoding="utf-8")}
    linjer = []
    for wid in valgte_id(ut):
        if kilder.har_tekst(wid) or wid not in kand:
            continue
        t = re.sub(r"[^\w\s-]", " ", kand[wid]["tittel"]).strip()
        kort = " ".join(t.split()[:10])
        d = hent(f"{API}/works?" + urllib.parse.urlencode({"filter": "title.search:" + kort, "per_page": 10})) or {}
        for w in d.get("results") or []:
            vid = w["id"].rsplit("/", 1)[1]
            if vid == wid:
                continue
            r = rad(w, "versjon")
            pdf = bool(r["pdf_urler"] or r["apen_url"])
            linjer.append(f"{wid}\t{vid}\t{r['ar']}\t{r['type']}\t{pdf}\t{bool(r['sammendrag'])}\t{r['kilde'][:60]}\t{r['tittel'][:100]}")
            if vid not in kand:
                kand[vid] = r
                with open(os.path.join(ut, "kandidater.jsonl"), "a", encoding="utf-8") as f:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
        time.sleep(0.2)
    open(os.path.join(ut, "versjoner.tsv"), "w", encoding="utf-8").write("valgt\tversjon\tar\ttype\tpdf\tsammendrag\tkilde\ttittel\n" + "\n".join(linjer) + "\n")
    print("\n".join(linjer))


def ssb_modus(mappe, tabell, sporring=""):
    """Henter en tabell fra SSBs PxWebApi v2 som CSV, med adresse og hentedato øverst."""
    import datetime
    url = f"https://data.ssb.no/api/pxwebapi/v2/tables/{tabell}/data?lang=no&outputFormat=csv" + ("&" + sporring if sporring else "")
    data = hent(url, raa=True)
    ut = os.path.join(ROT, "sporsmal", mappe, "statistikk")
    os.makedirs(ut, exist_ok=True)
    p = os.path.join(ut, f"ssb-{tabell}.csv")
    if not data:
        print(f"SSB-tabell {tabell}: ingen data ({url})"); return
    open(p, "w", encoding="utf-8").write(f"# Kilde: SSB, tabell {tabell}\n# Adresse: {url}\n# Hentet: {datetime.date.today().isoformat()}\n" + data.decode("utf-8-sig", "replace"))
    print(f"{p}: {len(data)} byte")


if __name__ == "__main__":
    if sys.argv[2] == "--ssb":
        ssb_modus(sys.argv[1], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
    elif sys.argv[2] in ("--pdf", "--pdf-alle"):
        pdf_modus(sys.argv[1], alle=sys.argv[2] == "--pdf-alle")
    elif sys.argv[2] == "--versjoner":
        versjon_modus(sys.argv[1])
    elif sys.argv[2] in ("--norsk", "--svensk", "--finsk", "--referanser"):
        logg_sok(sys.argv[1], sys.argv[2], sys.argv[3:])
        {"--norsk": norsk_modus, "--svensk": svensk_modus, "--finsk": finsk_modus, "--referanser": referanse_modus}[sys.argv[2]](sys.argv[1], sys.argv[3:])
        skriv_kandidater_tsv(sys.argv[1])
    elif sys.argv[2] == "--prioriter":
        skriv_kandidater_tsv(sys.argv[1])
    else:
        logg_sok(sys.argv[1], "engelsk", sys.argv[2:])
        sok_modus(sys.argv[1], sys.argv[2:])
        skriv_kandidater_tsv(sys.argv[1])
