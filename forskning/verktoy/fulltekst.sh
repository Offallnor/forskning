#!/bin/bash
# Fulltekst og PDF-er ligger i det private repoet Offallnor/forskning-tekst, med samme stier som her:
# forskning/kilder/<id>/tekst.txt, forskning/kilder/<id>/fil.pdf og forskning/innboks/.
# Det åpne repoet har resten, og .gitignore holder fulltekstene utenfor.
#
# Bruk (fra roten av det åpne repoet):
#   bash forskning/verktoy/fulltekst.sh hent <mappe>             kopier fulltekst fra en klon av Offallnor/forskning-tekst inn hit
#   bash forskning/verktoy/fulltekst.sh lagre <mappe> "<melding>"  kopier ny fulltekst tilbake, commit og push
# <mappe> er en lokal klon av Offallnor/forskning-tekst. Skriv aldri fulltekst til loggen: loggene i det åpne repoet er åpne.
set -euo pipefail
cmd=${1:?hent eller lagre}; dir=${2:?mappe med klon av Offallnor/forskning-tekst}
# Kopierer tekst.txt og fil.pdf i kildebiblioteket fra $1 til $2 (bare nye eller endrede filer).
kopier_kilder() {
  (cd "$1" && find forskning/kilder -mindepth 2 -maxdepth 2 \( -name tekst.txt -o -name fil.pdf \) -print0) |
    while IFS= read -r -d '' f; do
      if ! cmp -s "$1/$f" "$2/$f"; then mkdir -p "$2/$(dirname "$f")"; cp -p "$1/$f" "$2/$f"; fi
    done
}
# Gjør innboksen i $2 lik den i $1 (README.md står i begge repoene og røres ikke).
speil_innboks() {
  find "$2/forskning/innboks" -mindepth 1 ! -name README.md -delete
  (cd "$1/forskning/innboks" && find . -mindepth 1 ! -name README.md -print0) |
    while IFS= read -r -d '' f; do
      if [ -d "$1/forskning/innboks/$f" ]; then mkdir -p "$2/forskning/innboks/$f"; else cp -p "$1/forskning/innboks/$f" "$2/forskning/innboks/$f"; fi
    done
}
mkdir -p "$dir/forskning/kilder" "$dir/forskning/innboks" forskning/kilder forskning/innboks
case "$cmd" in
  hent)
    kopier_kilder "$dir" .
    speil_innboks "$dir" .
    echo "Fulltekst hentet: $(find forskning/kilder -name tekst.txt | wc -l) tekster" ;;
  lagre)
    melding=${3:-"Fulltekst"}
    kopier_kilder . "$dir"
    speil_innboks . "$dir"
    cd "$dir"
    git add -A forskning
    if git diff --cached --quiet; then echo "Ingen ny fulltekst"; exit 0; fi
    git -c user.name="github-actions[bot]" -c user.email="41898282+github-actions[bot]@users.noreply.github.com" commit -qm "$melding"
    for forsok in 1 2 3 4 5; do
      # Én fil per kilde, så en konflikt gjelder samme kilde hentet to ganger. Da beholdes denne kjøringens versjon.
      git pull -q --rebase -X theirs && git push -q && { echo "Fulltekst lagret"; exit 0; }
      sleep $((forsok * 10 + RANDOM % 10))
    done
    exit 1 ;;
  *) echo "Ukjent kommando: $cmd"; exit 2 ;;
esac
