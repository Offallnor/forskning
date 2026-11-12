"""Lager arbeidsområdet til et uavhengig uttrekk eller en blind innholdskontroll.

Bruk: python3 -I forskning/verktoy/sporsmal_kopi.py <mappe> <målmappe>

Kopierer bare det kjøringen skal se, med samme mappestruktur, så kontrollskriptet virker i kopien:
forskning/kilder/<id>/ for kildene i valgt.txt, sporsmal/<mappe>/{kandidater.jsonl, valgt.txt, kriterier.md},
en tom svar.md og en tom estimater.tsv med kolonnenavn, katalog/poster.jsonl og verktoy/ (skript og
instrukser). svar.md, estimater.tsv og budskap.tsv fra spørsmålet kopieres ikke.
"""
import os, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kilder  # noqa: E402
from kilder_oversikt import valgte  # noqa: E402

KOL = "id\tdesign\tland\tgruppe\tutfall\tsammenligning\tmal\testimat\tki_lav\tki_hoy\tn\tside\tsitat\n"


def main(mappe, mal):
    ut = os.path.join(os.path.abspath(mal), "forskning")
    fra = os.path.join(kilder.ROT, "sporsmal", mappe)
    til = os.path.join(ut, "sporsmal", mappe)
    os.makedirs(til, exist_ok=True)
    for navn in ("kandidater.jsonl", "valgt.txt", "kriterier.md"):
        if os.path.exists(os.path.join(fra, navn)):
            shutil.copy(os.path.join(fra, navn), til)
    open(os.path.join(til, "svar.md"), "w").close()
    open(os.path.join(til, "estimater.tsv"), "w", encoding="utf-8").write(KOL)
    n = 0
    for w in set(valgte(mappe)):
        if os.path.isdir(kilder.mappe(w)):
            shutil.copytree(kilder.mappe(w), os.path.join(ut, "kilder", w), dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("*.pdf"))
            n += 1
    os.makedirs(os.path.join(ut, "katalog"), exist_ok=True)
    shutil.copy(os.path.join(kilder.ROT, "katalog", "poster.jsonl"), os.path.join(ut, "katalog"))
    shutil.copytree(os.path.join(kilder.ROT, "verktoy"), os.path.join(ut, "verktoy"), dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__"))
    print(f"{ut}: {n} kilder")


if __name__ == "__main__":
    main(*sys.argv[1:3])
