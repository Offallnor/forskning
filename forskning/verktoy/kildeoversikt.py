#!/usr/bin/env python3
"""Lager vedlegg A til et forskningssvar: oversikt over alle kildene svaret bygger på.

Bruk: python3 -I forskning/verktoy/kildeoversikt.py <mappe>

Leser <mappe>/estimater.tsv, <mappe>/budskap.tsv (når den finnes) og
kildebiblioteket (forskning/kilder/<id>/kilde.json og tekst.txt). Skriver
<mappe>/vedlegg-kilder.md.

Én rad per kilde i estimater.tsv, gruppert etter design i rekkefølgen
oversikter, randomiserte forsøk, reformer og naturlige eksperimenter,
registerstudier og beskrivende kilder. Innenfor hver gruppe kommer Norge og
Norden først, deretter nyeste først.

Tallene skrives slik de står i estimater.tsv, bare med desimalkomma. Ingen
tall regnes om, så vedlegget har samme kontroll som uttrekket (sitat og side).
Forbehold tas fra budskap.tsv (forfatternes egne forbehold) når kilden er med
der. Ellers står feltet tomt.
"""
import csv
import json
import os
import re
import sys

GRUPPER = [
    ("oversikt", "Oversikter og metaanalyser"),
    ("rct", "Randomiserte forsøk"),
    ("kvasi", "Reformer, naturlige eksperimenter og diskontinuiteter"),
    ("register", "Registerstudier"),
    ("beskrivende", "Beskrivende kilder"),
    ("forvaltning", "Evalueringer av forvaltningen (uten effektmål)"),
]
NORDEN = ("Norge", "Sverige", "Danmark", "Finland", "Island", "Norden")
MAL = {"pp": "prosentpoeng", "prosent": "prosent", "dager": "dager", "HR": "(hasardrate)",
       "koeffisient": "(koeffisient)", "annet": ""}


def komma(v):
    v = (v or "").strip()
    return re.sub(r"(\d)\.(\d)", r"\1,\2", v).replace("-", "−") if re.search(r"\d", v) else v


INSTITUSJON = re.compile(r"Universit|Bank|Institut|Commission|Ministry|Directorate|Foundation|\bRWI\b|^OECD$|^[A-ZÆØÅ]{2,}$")


def etternavn(f):
    deler = f.split()
    j = len(deler) - 1
    # «von Simson», «van den Berg»: ta med små forledd
    while j > 0 and (deler[j - 1][:1].islower() or deler[j - 1] in ("Van", "Von", "De", "Der", "Den")):
        j -= 1
    return " ".join(deler[j:])


def navn(forf, ar):
    forf = [f.strip() for f in forf if f.strip()]
    personer = [f for f in forf if not INSTITUSJON.search(f)]
    etter = [etternavn(f) for f in personer] if personer else forf
    if not etter:
        return f"Ukjent {ar}"
    if len(etter) <= 3:
        return (", ".join(etter[:-1]) + " og " + etter[-1] if len(etter) > 1 else etter[0]) + f" {ar}"
    return f"{etter[0]} mfl. {ar}"


def celle(t):
    return (t or "").replace("|", "/").replace("\n", " ").strip()


def resultat(e):
    tall = komma(e["estimat"])
    if not tall:
        return f"{celle(e['utfall'])}: *ingen tall*" + (f" [s. {e['side']}]" if e.get("side") else "")
    enhet = MAL.get(e["mal"], e["mal"])
    s = f"**{tall}** {enhet}".rstrip()
    if e.get("ki_lav") and e.get("ki_hoy"):
        s += f" (KI {komma(e['ki_lav'])} til {komma(e['ki_hoy'])})"
    hvor = []
    if e.get("n"):
        hvor.append(f"n = {komma(e['n'])}" if re.fullmatch(r"[\d .,]+", e["n"]) else e["n"])
    if e.get("side"):
        hvor.append(f"s. {e['side']}")
    utfall = celle(e["utfall"])
    if e.get("sammenligning"):
        utfall += f"; {celle(e['sammenligning'])}"
    return f"{utfall}: {s}" + (f" [{', '.join(hvor)}]" if hvor else "")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    mappe = sys.argv[1].rstrip("/")
    if not os.path.isdir(mappe):
        # Godta bare mappenavnet, som sporsmal_kontroll.py
        mappe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sporsmal", mappe)
    rot = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    with open(os.path.join(mappe, "estimater.tsv"), encoding="utf-8") as fh:
        est = [r for r in csv.DictReader(fh, delimiter="\t") if r.get("id")]
    budskap = {}
    bsti = os.path.join(mappe, "budskap.tsv")
    if os.path.exists(bsti):
        with open(bsti, encoding="utf-8") as fh:
            budskap = {r["id"]: r for r in csv.DictReader(fh, delimiter="\t")}

    kilder = {}
    for e in est:
        k = kilder.setdefault(e["id"], {"est": [], "design": [], "land": []})
        k["est"].append(e)
        if e["design"] not in k["design"]:
            k["design"].append(e["design"])
        if e["land"] not in k["land"]:
            k["land"].append(e["land"])

    rangering = {g: i for i, (g, _) in enumerate(GRUPPER)}
    for kid, k in kilder.items():
        meta = {}
        msti = os.path.join(rot, "kilder", kid, "kilde.json")
        if os.path.exists(msti):
            meta = json.load(open(msti, encoding="utf-8"))
        k["meta"] = meta
        k["ar"] = meta.get("ar") or 0
        k["navn"] = navn(meta.get("forfattere") or [], meta.get("ar") or "u.å.")
        k["lenke"] = meta.get("lenke") or ""
        k["fulltekst"] = os.path.exists(os.path.join(rot, "kilder", kid, "tekst.txt"))
        # Sterkeste design kilden har, avgjør gruppen
        k["gruppe"] = min(k["design"], key=lambda d: rangering.get(d, 99))
        k["norden"] = any(n in l for l in k["land"] for n in NORDEN)

    ut = [f"# Vedlegg A: kildeoversikt\n",
          f"Alle {len(kilder)} kildene svaret bygger på, med tallene som er hentet ut av hver kilde. "
          "Tallene står slik de er hentet ut, med side i kilden. KI er 95 prosent konfidensintervall når "
          "kilden oppgir det. Forbehold er forfatternes egne, slik de er oppsummert i kontrollen av "
          "hovedbudskapene, og står bare for kildene som var med i den. «Sammendrag» betyr at teksten ikke "
          "var tilgjengelig og at tallene er hentet fra sammendraget.\n",
          "Innenfor hver gruppe står studier fra Norden først, deretter nyeste først. En kilde med flere "
          "design står i gruppen for det sterkeste.\n"]
    for g, tittel in GRUPPER + [("annet", "Andre kilder")]:
        rader = [(kid, k) for kid, k in kilder.items()
                 if (k["gruppe"] == g) or (g == "annet" and k["gruppe"] not in rangering)]
        if not rader:
            continue
        rader.sort(key=lambda x: (not x[1]["norden"], -int(x[1]["ar"] or 0), x[1]["navn"]))
        ut.append(f"\n## {tittel} ({len(rader)})\n")
        ut.append("| Kilde | Land | Hva er målt, og resultat | Lest | Forfatternes forbehold |")
        ut.append("|---|---|---|---|---|")
        for kid, k in rader:
            kilde = f"[{k['navn']}]({k['lenke']})" if k["lenke"] else k["navn"]
            tittel_k = celle(k["meta"].get("tittel", ""))
            if tittel_k:
                kilde += f"<br>*{tittel_k}*"
            land = "<br>".join(celle(l) for l in k["land"])
            res = "<br>".join("• " + resultat(e) for e in k["est"])
            lest = "fulltekst" if k["fulltekst"] else "sammendrag"
            forb = celle(budskap.get(kid, {}).get("forbehold", ""))
            ut.append(f"| {kilde} | {land} | {res} | {lest} | {forb} |")
    # Valgte kilder uten tekst og uten sammendrag er ikke med i uttrekket (se sporsmal_grupper.py)
    uleste = []
    vp, kp = os.path.join(mappe, "valgt.txt"), os.path.join(mappe, "kandidater.jsonl")
    if os.path.exists(vp) and os.path.exists(kp):
        kand = {}
        for l in open(kp, encoding="utf-8"):
            r = json.loads(l)
            kand[r["id"]] = r
        for l in open(vp, encoding="utf-8"):
            kid = l.split("#")[0].strip()
            r = kand.get(kid)
            if not r or kid in kilder or (r.get("sammendrag") or "").strip() \
                    or os.path.exists(os.path.join(rot, "kilder", kid, "tekst.txt")):
                continue
            n = navn(r.get("forfattere") or [], r.get("ar") or "u.å.")
            lenke = r.get("doi") or r.get("apen_url") or ""
            uleste.append(f"- {'[' + n + '](' + lenke + ')' if lenke else n}: *{celle(r.get('tittel', ''))}*")
    if uleste:
        ut.append(f"\n## Kilder som ikke kunne leses ({len(uleste)})\n")
        ut.append("Valgt ut fra tittel eller referanser, men verken teksten eller et sammendrag var tilgjengelig. "
                  "De er ikke brukt i svaret.\n")
        ut += sorted(uleste)
    sti = os.path.join(mappe, "vedlegg-kilder.md")
    with open(sti, "w", encoding="utf-8") as fh:
        fh.write("\n".join(ut) + "\n")
    print(f"Skrev {sti}: {len(kilder)} kilder, {len(est)} tall.")


if __name__ == "__main__":
    main()
