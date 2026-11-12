"""Katalog over artiklene i Navs tidsskrift Arbeid og velferd (nav.no, 2007 og framover).

Bruk: python3 -I forskning/verktoy/arbeid_og_velferd.py
Skriver forskning/katalog/arbeid-og-velferd.jsonl, én artikkel per linje:
id (AV-<år>-<nr>-<løpenr>), tittel, ar, nr, forfattere, sammendrag (ingressen på nav.no), url, pdf.
Henter ikke fulltekst. Artiklene er ikke i OpenAlex eller vitenarkivet, så spørsmålsløypa søker her i tillegg.
"""
import html, json, os, re, sys, time, urllib.request

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAV = "https://www.nav.no"
ARKIV = ["/no/nav-og-samfunn/kunnskap/analyser-fra-nav/arbeid-og-velferd",
         "/no/nav-og-samfunn/kunnskap/analyser-fra-nav/arbeid-og-velferd/arkiv-arbeid-og-velferd",
         "/no/nav-og-samfunn/kunnskap/analyser-fra-nav/arbeid-og-velferd/arkiv-arbeid-og-velferd_kap"]
UA = "Mozilla/5.0 (kunnskapsoversikt)"


def hent(sti):
    for forsok in range(4):
        try:
            req = urllib.request.Request(NAV + sti if sti.startswith("/") else sti, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            print(f"{type(e).__name__}: {sti}", flush=True)
            time.sleep(5 * (forsok + 1))
    return ""


def ren(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def artikkel(sti):
    s = hent(sti)
    m = re.search(r"<article.*?</article>", s, re.S)
    a = m.group(0) if m else s
    pdf = re.findall(r'href="(/_/attachment/download/[^"]+\.pdf)"', a)
    avsnitt = [ren(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", a, re.S)]
    avsnitt = [p for p in avsnitt if p and not p.startswith("Publisert")]
    forf = next((p[3:] for p in avsnitt if p.startswith("Av ")), "")
    tekst = [p for p in avsnitt if not p.startswith("Av ") and not p.lower().endswith("(pdf)") and not re.match(r"Arbeid og velferd nr", p)]
    return {"forfattere": [f.strip() for f in re.split(r",| og ", forf) if f.strip()], "tekst_tegn": len(" ".join(tekst)),
            "sammendrag": " ".join(tekst)[:4000], "pdf": NAV + pdf[0] if pdf else ""}


def main():
    utgaver = set()
    for a in ARKIV:
        utgaver |= set(re.findall(r'href="(/no/nav-og-samfunn/kunnskap/analyser-fra-nav/arbeid-og-velferd/arbeid-og-velferd/arbeid-og-velferd-nr[^"]+)"', hent(a)))
    print(f"{len(utgaver)} utgaver", flush=True)
    rader, sett = [], set()
    for u in sorted(utgaver):
        s = hent(u)
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        m = re.search(r"nr\.?\s*(\d)\s*[-–]\s*(\d{2,4})", ren(h1.group(1)) if h1 else "") or re.search(r"nr\.(\d)-(20\d\d|\d\d)", u)
        nr, ar = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
        ar = ar + 2000 if ar < 100 else ar
        heftepdf = re.findall(r'href="(/_/attachment/download/[^"]+\.pdf)"', s)
        # Artikkellista står mellom tittelen og «Hele publikasjonen» (overskrift eller avsnitt, ulikt mellom årganger)
        i = s.find("</h1>"); j = s.find("Hele publikasjonen", i)
        liste = s[i:j if j > i else i + 20000] if i > 0 else ""
        k = 0
        for sti, tittel in re.findall(r'<a[^>]+href="(/no/nav-og-samfunn/kunnskap/analyser-fra-nav/arbeid-og-velferd/[^"]+)"[^>]*>(.*?)</a>', liste, re.S):
            tittel = ren(tittel)
            if sti in sett or not tittel or re.search(r"arbeid-og-velferd-nr[^/]*$", sti) or "arkiv" in sti:
                continue
            sett.add(sti); k += 1
            r = {"id": f"AV-{ar}-{nr}-{k:02d}", "tittel": tittel, "ar": ar, "nr": nr, "url": NAV + sti,
                 "hefte_pdf": NAV + heftepdf[0] if heftepdf else "", "kilde": f"Arbeid og velferd nr. {nr}-{ar}"}
            r.update(artikkel(sti))
            rader.append(r)
            time.sleep(0.3)
        print(f"{ar} nr. {nr}: {k} artikler{'' if k else '  ' + u}", flush=True)
    rader.sort(key=lambda r: r["id"])
    ut = os.path.join(ROT, "katalog", "arbeid-og-velferd.jsonl")
    with open(ut, "w", encoding="utf-8") as f:
        for r in rader:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"{len(rader)} artikler, {sum(bool(r['pdf']) for r in rader)} med pdf, {sum(bool(r['sammendrag']) for r in rader)} med ingress")


if __name__ == "__main__":
    sys.exit(main())
