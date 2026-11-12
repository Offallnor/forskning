#!/usr/bin/env python3
"""Lager figurer til statistikkdelen av et forskningssvar og kontrollerer tallene.

Bruk: python3 -I forskning/verktoy/figur.py <mappe>   (krever matplotlib: pip install matplotlib)

Leser <mappe>/figurer.tsv med ett tallpunkt per linje og kolonnene
  figur   kort navn, blir filnavnet figurer/<figur>.png
  type    linje eller soyle
  tittel  figurtittel
  enhet   tekst på y-aksen
  serie   navn på linja eller søylegruppa (for eksempel «Norge» eller «20–24 år»)
  x       år, måned eller kategori, i den rekkefølgen punktene skal vises
  verdi   tallet slik det står i fila (punktum eller komma)
  fil     uttrekket tallet er hentet fra, relativt til mappen (statistikk/...)
  kilde   kildelinja under figuren (kilde, tabell, hentedato)

Kontroll: hvert tall må stå i fila det er hentet fra. Finnes et tall ikke,
lages ingen figurer, og skriptet avslutter med feil. Resultatet skrives til
<mappe>/figurer/kontroll.md.

Figurene lagres som PNG, som vises i GitHub, kan limes inn i Word og kan
leses av Claude. Lim dem inn i svar.md med ![tittel](figurer/<figur>.png).
"""
import csv
import os
import re
import sys

FARGER = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#52514e"]
KOLONNER = ["figur", "type", "tittel", "enhet", "serie", "x", "verdi", "fil", "kilde"]


def norm(v):
    v = v.strip().replace("−", "-").replace("–", "-").replace(" ", "").replace(" ", "")
    return v.replace(",", ".")


def tall_i_fil(sti):
    tekst = open(sti, encoding="utf-8").read()
    funnet = set()
    for t in re.findall(r"-?\d+(?:[.,]\d+)?", tekst.replace(" ", "")):
        t = norm(t)
        funnet.add(t)
        try:
            funnet.add(repr(float(t)))
        except ValueError:
            pass
    return funnet


def les(mappe):
    sti = os.path.join(mappe, "figurer.tsv")
    with open(sti, encoding="utf-8") as fh:
        rader = list(csv.DictReader(fh, delimiter="\t"))
    mangler = [k for k in KOLONNER if rader and k not in rader[0]]
    if mangler:
        sys.exit(f"figurer.tsv mangler kolonnene {', '.join(mangler)}")
    return rader


def kontroller(mappe, rader):
    meldinger, feil, cache = [], 0, {}
    for i, r in enumerate(rader, start=2):
        fil = os.path.join(mappe, r["fil"])
        if not os.path.exists(fil):
            feil += 1
            meldinger.append(f"- FEIL linje {i}: fila {r['fil']} finnes ikke")
            continue
        if fil not in cache:
            cache[fil] = tall_i_fil(fil)
        v = norm(r["verdi"])
        try:
            alt = repr(float(v))
        except ValueError:
            feil += 1
            meldinger.append(f"- FEIL linje {i}: «{r['verdi']}» er ikke et tall")
            continue
        if v in cache[fil] or alt in cache[fil]:
            meldinger.append(f"- OK   {r['figur']}: {r['serie']} {r['x']} = {r['verdi']} står i {r['fil']}")
        else:
            feil += 1
            meldinger.append(f"- FEIL {r['figur']}: {r['serie']} {r['x']} = {r['verdi']} står ikke i {r['fil']}")
    return feil, meldinger


def tegn(mappe, rader):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter, MaxNLocator

    plt.rcParams.update({
        "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#999999", "axes.grid": True, "grid.color": "#e5e5e5",
        "axes.axisbelow": True, "axes.formatter.use_locale": False,
    })
    komma = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))
    figurer = {}
    for r in rader:
        figurer.setdefault(r["figur"], []).append(r)
    ut = os.path.join(mappe, "figurer")
    os.makedirs(ut, exist_ok=True)
    laget = []
    for navn, rr in figurer.items():
        type_, tittel, enhet = rr[0]["type"], rr[0]["tittel"], rr[0]["enhet"]
        kilder = list(dict.fromkeys(r["kilde"] for r in rr))
        serier = list(dict.fromkeys(r["serie"] for r in rr))
        xer = list(dict.fromkeys(r["x"] for r in rr))
        fig, ax = plt.subplots(figsize=(8, 4.5))
        if type_ == "linje":
            numerisk = all(re.fullmatch(r"\d{4}", x) for x in xer)
            ender = []
            for i, s in enumerate(serier):
                pkt = [(r["x"], float(norm(r["verdi"]))) for r in rr if r["serie"] == s]
                xs = [int(x) if numerisk else xer.index(x) for x, _ in pkt]
                ys = [y for _, y in pkt]
                ax.plot(xs, ys, color=FARGER[i % len(FARGER)], lw=2.6 if i == 0 else 1.7,
                        marker="o" if len(xs) <= 15 else None, ms=3.5)
                ender.append([ys[-1], xs[-1], s])
            if numerisk:
                ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                lo, hi = int(xer[0]), int(xer[-1])
                ax.set_xlim(lo, hi + max(2, (hi - lo) * 0.18))
            else:
                ax.set_xticks(range(len(xer)), xer)
                ax.set_xlim(-0.3, len(xer) - 1 + max(1.5, len(xer) * 0.18))
            ax.set_ylim(0, None)
            # Navn ved enden av hver linje, flyttet fra hverandre så de ikke overlapper
            lo, hi = ax.get_ylim()
            avstand = (hi - lo) * 0.045
            ender.sort()
            plass = []
            for y, x, navn_s in ender:
                ny = y if not plass else max(y, plass[-1] + avstand)
                plass.append(ny)
                ax.annotate("  " + navn_s, xy=(x, y), xytext=(x, ny), va="center", fontsize=9,
                            annotation_clip=False)
        elif type_ == "soyle":
            n = len(serier)
            b = 0.8 / n
            for i, s in enumerate(serier):
                verdi = {r["x"]: float(norm(r["verdi"])) for r in rr if r["serie"] == s}
                pos = [xer.index(x) + (i - (n - 1) / 2) * b for x in xer if x in verdi]
                ax.bar(pos, [verdi[x] for x in xer if x in verdi], b * 0.92,
                       color=FARGER[i % len(FARGER)], label=s)
            ax.set_xticks(range(len(xer)), xer)
            ax.grid(axis="x", visible=False)
            if n > 1:
                ax.legend(frameon=False, loc="best")
        else:
            sys.exit(f"Ukjent figurtype «{type_}» i {navn} (bruk linje eller soyle)")
        ax.yaxis.set_major_formatter(komma)
        ax.set_ylabel(enhet)
        ax.set_title(tittel, loc="left", fontsize=12, fontweight="bold")
        fig.text(0.01, 0.01, "Kilde: " + "; ".join(kilder), fontsize=8, color="#52514e")
        fig.tight_layout(rect=(0, 0.04, 1, 1))
        sti = os.path.join(ut, f"{navn}.png")
        fig.savefig(sti, dpi=150)
        plt.close(fig)
        laget.append(sti)
    return laget


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    mappe = sys.argv[1].rstrip("/")
    if not os.path.isdir(mappe):
        # Godta bare mappenavnet, som sporsmal_kontroll.py
        mappe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sporsmal", mappe)
    rader = les(mappe)
    feil, meldinger = kontroller(mappe, rader)
    os.makedirs(os.path.join(mappe, "figurer"), exist_ok=True)
    with open(os.path.join(mappe, "figurer", "kontroll.md"), "w", encoding="utf-8") as fh:
        fh.write(f"# Kontroll av figurtall: {os.path.basename(os.path.abspath(mappe))}\n\n")
        fh.write(f"{feil} feil av {len(rader)} tall.\n\n" + "\n".join(meldinger) + "\n")
    if feil:
        print("\n".join(m for m in meldinger if "FEIL" in m))
        sys.exit(f"{feil} tall står ikke i fila de er hentet fra. Ingen figurer laget.")
    for sti in tegn(mappe, rader):
        print("Laget", sti)
    print(f"0 feil av {len(rader)} tall.")


if __name__ == "__main__":
    main()
