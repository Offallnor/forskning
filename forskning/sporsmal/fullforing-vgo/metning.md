# Metning: fullføring i videregående opplæring

Vurdert 20.11.2026, etter tre referanserunder og to blinde utvalg (forenklet blindtest, se under).

## Omfanget

Spørsmålet er bredt (alle tiltak for fullføring i OECD, med vekt på yrkesfag, og utfall i arbeid, inntekt og ytelser), og kandidatmengden vokste raskt:

| Trinn | Kandidater | Nye | Beholdt i grovsikting | Valgt |
|---|---|---|---|---|
| Søk | 6 353 | 6 353 | 2 894 | 560 |
| Referanserunde 1 (`referanser-1.tsv`) | 4 853 rader | 4 386 | 2 288 | 304 |
| Referanserunde 2 (`referanser-2.tsv`) | 12 117 rader | 7 375 | 3 599 | 233 |
| Blindt utvalg av runde 2 | | | | 56 |
| Referanserunde 3 (`referanser-3.tsv`), fra de 56 | | 2 739 | 975 | 52 |
| Blindt utvalg av runde 3 | | | | 24 |

Grovsiktingen er gjort med Haiku etter `verktoy/SIKTING.md`. Utvalget er lest i bolker på Opus.

## Krav 1: under 5 prosent nye i kategori 1–4 i siste referanserunde

- **Referanserunde 1:** 278 av de 4 386 nye kandidatene ble valgt i kategori 1–4, om lag 6 prosent. Kravet var ikke oppfylt.
- **Referanserunde 2:** 177 av de 7 375 nye ble valgt i kategori 1–4 i Opus-utvalget (2,4 prosent). Med de 42 kildene i kategori 1–3 som det blinde utvalget la til, er andelen om lag 3 prosent.

- **Referanserunde 3:** 27 av de 2 739 nye ble valgt i kategori 1–4 i Opus-utvalget (1,0 prosent). Med de 18 i kategori 1–4 som det blinde utvalget la til, er andelen 1,6 prosent.

Krav 1 er oppfylt i runde 2 og 3.

## Krav 2: det blinde utvalget finner ikke nye kilder i kategori 1–3

**Avvik fra løypa:** Løypa sier to blinde utvalg på hele kandidatmengden (Opus og Sonnet). Med over 18 000 kandidater er det gjort ett blindt utvalg på Sonnet, bare av de 3 599 kandidatene fra referanserunde 2 som grovsiktingen beholdt, lest i åtte bolker med samme instruks som Opus-utvalget.

- Det blinde utvalget valgte 191 kilder. 135 av dem var allerede valgt, og 56 var nye. 42 av de nye er i kategori 1–3 etter Sonnets egen merking.
- Mange av de 42 er utenfor omfanget eller grensetilfeller: Job Corps (tiltak for unge utenfor skolen), skoletiltak mot eksklusjon, early college og skolevalg med utfall bare i høyere utdanning, og rene titler uten sammendrag. Noen er relevante og manglet, blant dem en norsk studie av skjerpede aktivitetskrav i sosialhjelpen med effekt på frafall, et dansk naturlig eksperiment med matematikkvalg i videregående, randomiserte forsøk med dual credit og early college, metaanalyser av skolebasert mentoring og diskontinuitetsstudier av avgangsprøver og dobbel algebra.
- Alle 56 er tatt inn i `valgt.txt` foreløpig. Kilder utenfor omfanget siles ut i det strenge utvalget og føres i `utelatt.tsv`.

Krav 2 var ikke oppfylt etter runde 2. Etter løypa ble referanserunde 3 kjørt fra de 56 kildene, og et nytt blindt utvalg (Sonnet, tre bolker) ble gjort bare på de 975 nye kandidatene som grovsiktingen beholdt. Opus-utvalget av de samme kandidatene valgte 52.

- Det blinde utvalget valgte 52 kilder. 28 av dem var valgt av Opus, og 24 var nye. 17 av de nye er i kategori 1–3 etter Sonnets merking.
- De fleste av de 17 er utenfor omfanget: oversikter og forsøk med fravær eller eksklusjon som utfall, Job Corps, PROGRESA med påmelding på grunnskolenivå, pengeinsentiver i Argentina (utenfor OECD) og oversikter over tiltak for unge utenfor skole og arbeid. Innenfor omfanget, eller nær det, er Teenage Parent Welfare Demonstration (randomisert, skolefremmøte), New York Small Schools of Choice (bare tittel) og No Pass No Drive-lovene (variasjon mellom delstater, utdanningsnivå).
- Alle 24 er tatt inn i `valgt.txt` foreløpig og siles i det strenge utvalget.

Krav 2 er strengt tatt ikke oppfylt etter runde 3 heller. Løypa sier at det da skal noteres som svakhet. Det er ikke kjørt en fjerde runde, fordi nesten alle de nye sterke kildene er utenfor mandatet, og fordi andelen nye i kategori 1–4 er godt under grensen i krav 1.

**Avgrensning som må avklares i det strenge utvalget:** Opus- og Sonnet-utvalgene fant flere studier av avgangsprøver og krav til vitnemål (exit exams, GED, No Pass No Drive) med sterkt design og fullføring som utfall. De passer ikke klart i tiltaksgruppe 1–5. Tas de med i gruppe 5, bør de hentes inn fra kandidatlista.

## Svakheter

- **Ett blindt utvalg per runde, ikke to fulle,** og bare på runde 2 og 3. Kilder som både første utvalg og referanserunde 1 overså, fanges bare opp hvis de siteres av noe som er valgt senere.
- **Grovsiktingen med Haiku** har forkastet om lag halvparten av kandidatene på tittel og sammendrag. Kilder med bare tittel er mer utsatt.
- **Læreplasser og lærlingtilskudd** er tynt dekket med effektstudier, særlig i Norden. Det meste er tysk og sveitsisk.
- **Nordiske effektstudier** av fullføringstiltak er få. Mye av det norske materialet er evalueringer uten effektmål (kategori F), blant annet Ny GIV og oppfølgingstjenesten.
- **Det finske søket i Finna ga null treff.** Finland er derfor bare dekket gjennom OpenAlex.
- **Referansesøket følger bare OpenAlex-kilder.** Norske, svenske og danske rapporter uten OpenAlex-id kan ikke følges med skriptet.
- **Referanserunde 3 måtte kjøres fire ganger.** Første gang gikk den ut på tid, og to ganger stoppet den på OpenAlex-kvoten. Skriptet er rettet, så en runde som stopper på kvoten, ikke lagres som om den var tom.
