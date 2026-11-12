# Utvalg: dagpengenes varighet og nivå og overgang til arbeid

Skrevet 10.11.2026.

## Søk

- Engelsk søk i OpenAlex fra 1990 (44 uttrykk, også svenske og danske ord), norsk søk (vitenarkivet, *Arbeid og velferd*, Kudos, Navs bibliotek), svensk søk i LIBRIS og finsk søk i Finna. Ordene står i `kjor.sh` og `sok-logg.tsv`.
- Søket ga 4 042 kandidater: 2 308 fra OpenAlex, 624 fra LIBRIS, 987 fra Finna og 123 norske.

## Første utvalg

- Ni kjøringer leste hver sin del av kandidatlista (seks OpenAlex-bolker med sammendrag for prioritet 1 og høyere, én med titler for prioritet 0 og lavere sammen med de norske, én svensk og én finsk). Svenske og finske kilder er valgt på tittel og utgiver, fordi katalogene nesten aldri har sammendrag. I den finske lista ble om lag 400 titler bare skummet etter at arkivposter, bilder og sykepengetitler var sortert bort.
- 628 kilder ble valgt.

## Referanser

- Tre runder (`referanser-1.tsv` til `referanser-3.tsv`). Fra runde 2 sto kildene som var fulgt før i `referanser-fulgt.txt`, så hver runde fulgte bare nye kilder.
- Runde 1 ga 4 722 nye kandidater, runde 2 1 952 og runde 3 345.
- Fordi mappen fikk over 2 000 kandidater, ble de grovsiktet med Haiku etter `verktoy/SIKTING.md` før utvalget: 4 135 av 8 798 beholdt etter runde 1 (30 bolker), og 460 av 1 952 etter runde 2 (sju bolker). Runde 3 ble lest direkte. Siktingen beholdt 618 av de 628 kildene i første utvalg. Én av de forkastede, Card m.fl. om generalisert regression kink i Østerrike (W3122336779), sto allerede i utvalget og er beholdt.
- Kjente avvik i siktingen: to bolker forkastet studier fra utviklingsland og en bolk skrev at den forkastet alt før 1990, mot instruksen. Begge grupper er utenfor kriteriene, så det har trolig liten betydning.
- Første utvalg tok inn 296 kilder fra runde 1, 44 fra runde 2 og 3 fra runde 3.

## Blinde utvalg

- Utvalg A (Opus) valgte 240 studier, utvalg B (Sonnet) 171, begge fra de grovsiktede kandidatene etter runde 2. 94 og 96 prosent fantes i første utvalg.
- Seksten kilder ble tatt inn fra de blinde utvalgene, blant dem sju i kategori 1–3. Fem ble begrunnet i `utelatt.tsv`.
- Et nytt blindt utvalg (Sonnet) på de 64 nye kandidatene fra runde 3 fant ingen nye kilder i kategori 1–3 innenfor kriteriene.

## Metning

Se `metning.md`. Begge krav er oppfylt etter tre referanserunder.

## Begrunnelse for utelatte

- 3 664 sentrale kandidater (oversikter, persentil minst 0,9 eller minst 50 siteringer) var ikke valgt.
- 335 er publisert før 1990, og 2 419 nevner ikke dagpenger eller arbeidsledighetstrygd i tittel eller sammendrag. De er begrunnet gruppevis med skript etter tema.
- 910 nevner dagpenger. De er begrunnet enkeltvis av fire kjøringer (Sonnet). Fire ble merket for ny vurdering; tre ble tatt inn (en dansk studie av lovendringer i dagpengeperioden, en spansk strukturell studie og en norsk beskrivelse av koronaendringene), og én ble utelatt som kalibrert modell.

## Utvalget

- 993 linjer i `valgt.txt`, hvorav om lag 110 er andre versjoner av samme studie. Det gir om lag 880 studier.
- Kategori etter første utvalg (foreløpig, settes på nytt etter blind lesing): om lag 45 oversikter, 28 randomiserte forsøk (de fleste bonusforsøk, beslektet tiltak), 370 i kategori 3, 350 i kategori 4, 110 i kategori 5 og åtte evalueringer av forvaltningen.

## Norske oversikter

Det finnes ingen norsk kunnskapsoppsummering om dagpengenes varighet og nivå i utvalget. Nærmest kommer Fevangs diskusjon av helserelaterte ytelser og skjult ledighet (W3088312345) og Nordisk ministerråds rapport om dagpengesystemene i Norden fra 1999 (bare tittel). Litteraturlistene i de norske reformstudiene (Falch mfl. 2011 og 2012, Røed og Westlie 2007) er dekket gjennom referanserundene.

## Sentrale kilder uten tekst

Tolv sentrale kilder i kjernen er bare lest i sammendrag og står øverst i `mangler.md`, blant dem Røed mfl. 2007, Røed og Westlie 2012, Røed og Zhang 2002, Carling mfl. 2001 og flere finske studier av Kyyrä og medforfattere.

## Avgrensning av uttrekket (bestilleren 10.11.2026)

Utvalget er tre til fire ganger større enn i tidligere spørsmål. Bestilleren valgte at uttrekket gjøres to ganger (Opus og Sonnet) for oversikter, studier i kategori 1–3 og alle nordiske studier. Studier i kategori 4–5 utenfor Norden hentes ikke ut og står bare i vedlegget med tittel og lenke. Avviket fra løypa skrives i forbeholdene i svaret.

## Feil dokument fra vitenarkivet

W2283885892 (Brisson 2015) og W1506616408 (Gutierrez 2013) har generiske titler («Three empirical essays in labor economics», «Essays in Labor Economics»). Tekstinnhentingen fant norske avhandlinger med lignende titler i vitenarkivet (Knutsen 2022 og Ellingsen 2023). Tekstene ble slettet 10.11, men hentet på nytt av neste `--pdf`-runde, og er slettet igjen. De to kildene er lest bare i sammendrag. En ny `--pdf`-runde vil hente dem på nytt med mindre tittelkontrollen i `sporsmal_sok.py` strammes inn.

Katalogene som ble brukt i søket, er fra commit `41c0795` (`git log -1 --format=%h -- forskning/katalog`).
