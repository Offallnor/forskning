"""Stopper navn og interne spor i håndskrevet tekst før de blir offentlige.

Bruk: python3 -I forskning/verktoy/sjekk_spor.py [filer ...]   (uten filer: hele repoet)

Sjekker .md, .py, .yml, .sh og .tsv utenfor katalogene, kandidatlistene og kildebibliotekets data,
som er kildenes eget innhold. Ordene som stoppes, står som sjekksummer, så lista ikke selv blir et spor.
Kjøres av sjekk-spor.yml ved hver push.
"""
import hashlib, os, re, sys

STOPP = {  # sha256 av ord med små bokstaver
    "65a65f170bbe76c600f0551f17ba7c40fac0a14aa3c6bfbccd715f621a525147",
    "9313d4bfe1b640eebc588cc15906f6bb20d06552779da298ae91b0035680ae75",
    "ad743fa97a2e603709d5e5805bbbb536ea6a952b9befddc762722495077e7b87",
    "7d87390396e779c76832860daa64d14b14d48d4978fc726b97ceb377288aa7c1",
    "9eaa9588c074f4a8d74c96586b5cfe84d75fdd6168844f4f4b84978bad19fb70",
    "576ba7c2e4abb7184ca409154dbbbd5306c1a80747fbce4148ea6271fd21e776",
    "871d604893151d0050e5d7af7b6af5e4ff0936c7c9ef17625f6c93da26c0d0de",
}
MONSTER = [
    (re.compile(r"/mnt/project-files"), "sti til prosjektmappe"),
    (re.compile(r"\b(?:i|fra) departementet\b(?! (?:kan|skal|gir))"), "«departementet» som bestiller eller avsender"),
    (re.compile(r"råd oppover|for saksbehandlere i\b"), "intern mottaker"),
    (re.compile(r"regjeringens politikk|internt arbeidsdokument", re.I), "tekst som viser at svaret er laget for et departement"),
    (re.compile(r"\b[A-ZÆØÅ]{2,4}/[A-ZÆØÅ]{3}\b"), "mulig seksjonskode"),
    (re.compile(r"[\w.+-]+@(?!users\.noreply\.github\.com)[\w-]+\.[a-z]{2,}"), "e-postadresse"),
]
UNNTAK = re.compile(r"(^|/)(katalog/|kilder/|.*kandidater|.*referanser|versjoner\.tsv|sikting.*\.tsv|kontroll\.md|utelatt\.tsv|pdf-logg\.tsv|grupper\.tsv|budskap\.tsv|tidligere-budskap\.tsv|estimater.*\.tsv|valgt.*|vedlegg-kilder\.md|mangler\.md)")
TYPER = (".md", ".py", ".yml", ".yaml", ".sh", ".tsv")
OK_KODER = {"SSB/NAV"}

def filer(args):
    if args:
        return [f for f in args if os.path.isfile(f)]
    ut = []
    for rot, dirs, fs in os.walk("."):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        ut += [os.path.relpath(os.path.join(rot, f)) for f in fs]
    return ut

funn = 0
for f in filer(sys.argv[1:]):
    if not f.endswith(TYPER) or UNNTAK.search(f) or f.endswith("sjekk_spor.py"):
        continue
    for nr, linje in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
        for ord_ in re.findall(r"[a-zæøå0-9]+", linje.lower()):
            if hashlib.sha256(ord_.encode()).hexdigest() in STOPP:
                print(f"{f}:{nr}: ord som ikke skal stå i det åpne repoet"); funn += 1
        for m, hva in MONSTER:
            for t in m.findall(linje):
                if t in OK_KODER: continue
                print(f"{f}:{nr}: {hva}: {t}"); funn += 1
print(f"{funn} funn") if funn else print("Ingen spor funnet")
sys.exit(1 if funn else 0)
