# Kaldtest: raskt svar (gradert sykmelding ved psykiske lidelser)

8.11.2026. En ny tråd kjørte løypa bare ut fra `skills/felles-forskning/SKILL.md` og `forskning/LOYPE.md`, med prosjektlederen som bestiller. Målet var å prøve mandatsamtalen, regelen for når raskt svar tilbys, og selve raskt svar-varianten.

## Resultat

- Mandatsamtalen tok sju spørsmål og om lag fire minutter. Bestilleren rettet ett punkt («ikke bare om det virker annerledes, men om det virker og ev. hvor mye»), slik oppskriften legger opp til.
- Alle tre krav for raskt svar var oppfylt, og raskt svar ble anbefalt og valgt.
- Elleve kilder fra `gradert-sykmelding`, 18 rader i `estimater.tsv`, 18 rader i `statistikk.tsv`. Automatisk kontroll: 0 feil av 149 etter to rettinger. Innholdskontrollen er ikke kjørt (valgfri).
- Tid: om lag fem minutter fra godkjent mandat (08.51) til commit med bestått kontroll (08.56), og om lag ti minutter med mandatsamtalen. Oppskriften anslår en halvtime. Først rapportert som 35 minutter, som var et feilanslag.

## Funn om oppskriften

### Regelen for raskt svar

1. **Krav 1 kan ikke sjekkes slik det står.** Kravet viser til søkeordene i `kjor.sh`, men `gradert-sykmelding/kjor.sh` har ikke den første engelske OpenAlex-søkelinja (søket ble gjort før `kjor.sh` fantes). Bare `--norsk` og `--referanser` står der. Forslag: si at søkeordene kan finnes i `kjor.sh`, feltet `sok` i `kandidater.jsonl` eller `utvalg.md`.
2. **Krav 2 sier ikke hvordan «passer mandatet» avgjøres.** Titlene nevner sjelden undergruppen (her psykiske lidelser). Tråden telte kilder med tekst og minst fem treff på «mental/psykisk» i `tekst.txt` (27 kilder), og leste så de aktuelle avsnittene. Forslag: beskriv et slikt søk i teksten som første sortering.
3. **Regelen sier ikke om undergruppen må ha vært en del av søket.** Søket i `gradert-sykmelding` var ikke rettet mot psykiske lidelser, så studier som bare handler om psykiske lidelser og bruker andre ord, kan mangle. Kravene var oppfylt, men det er den største svakheten ved svaret. Forslag: ta det med i forbeholdene som fast punkt når spørsmålet er en undergruppe.

### Utvalg og uttrekk

4. **«Hver kilde leses på nytt» er uklart for en undergruppe.** Å lese elleve kilder i sin helhet tar lang tid. Tråden leste avsnittene om psykiske lidelser (søk i teksten) og brukte de tidligere radene som sjekkliste etterpå. Forslag: si at målrettet lesing av avsnittene om undergruppen er nok i raskt svar.
5. **`tittel:`-linjer i `valgt.txt`** fra det nære spørsmålet (tre i `gradert-sykmelding`) finnes ikke i `kilder/oversikt.tsv`. Oppskriften sier ikke hva raskt svar gjør med dem. De ble utelatt.
6. **Statistikk i raskt svar er ikke nevnt** i avsnittet om raskt svar, selv om mandatet kan be om det. Tråden fulgte «Tilvalg: statistikk». Nav-tabellen lå i datakatalogen, så det gikk greit.

### Kontrollene

7. **Feil forfatternavn ble ikke fanget av kontrollen.** Tråden skrev først et oppdiktet forfatternavn for scoping-oversikten fra 2024 (riktig: Grønstad). Feilen ble funnet ved en manuell sjekk mot `kandidater.jsonl`. Kontrollskriptet sjekker ikke navnene i lenketeksten. Forslag: kontroll 1 bør sjekke at etternavnet i lenketeksten står blant forfatterne i metadata eller på tittelsiden.
8. **Avrundede statistikktall** (37,4 i svaret, 37.412118 i fila) må føres som egne rader med `utregning`, ellers feiler kontroll 5. Oppskriften sier det ikke. Forslag: én setning under «Tilvalg: statistikk».
9. **Tabellkoder i teksten** (SYFRA2501) feiler kontroll 5, fordi feltet `tabell` ikke leses. Enten bør kontrollen lese `tabell`, eller oppskriften si at koden ikke skrives i svaret.
10. **Årstall:** Hartikainen mfl. har 2022 i metadata og 2023 på tittelsiden (tidsskriftets trykte utgave). Regelen om at tittelsiden går foran, gjelder navn. Det er uklart om den gjelder årstall. 2022 er brukt, som i `gradert-sykmelding`.

### Kjøremiljø

11. **Grenen er ikke nevnt.** Skillen og oppskriften sier at alt ligger under `forskning/`, men spørsmålene og kildebiblioteket finnes bare på grenen `claude/project-thread-l50ud0`, ikke på main. En ny bruker på main finner ikke `sporsmal/`. Løses ved fletting, men bør stå i skillen til da.
12. **Raskt svar trenger ikke Actions.** Ingen runde ble kjørt i Actions. Raskt svar kan derfor trolig lages uten skrivetilgang til Actions-grenen, så lenge mappen kan skrives et sted. Det kan gjøre varianten lettere å tilby i flere kjøremiljøer.

## Det som virket

- Mandatet med forslag til formuleringer gikk raskt. Bestilleren svarte med ett ord på fem av sju spørsmål.
- Rekkefølgen «vis det som finnes først» fikk fram at det nære svaret allerede hadde et avsnitt om psykiske lidelser.
- `kilder_oversikt.py` og kontrollskriptet virket uten endringer på en ny mappe.
