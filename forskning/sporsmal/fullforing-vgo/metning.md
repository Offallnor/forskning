# Metning: fullføring i videregående opplæring

Foreløpig vurdering 18.11.2026, etter to referanserunder og ett blindt utvalg. Referanserunde 3 er satt i gang fra kildene det blinde utvalget fant. Filen oppdateres når den er gjennomgått.

## Omfanget

Spørsmålet er bredt (alle tiltak for fullføring i OECD, med vekt på yrkesfag, og utfall i arbeid, inntekt og ytelser), og kandidatmengden vokste raskt:

| Trinn | Kandidater | Nye | Beholdt i grovsikting | Valgt |
|---|---|---|---|---|
| Søk | 6 353 | 6 353 | 2 894 | 560 |
| Referanserunde 1 (`referanser-1.tsv`) | 4 853 rader | 4 386 | 2 288 | 304 |
| Referanserunde 2 (`referanser-2.tsv`) | 12 117 rader | 7 375 | 3 599 | 233 |
| Blindt utvalg av runde 2 | | | | 56 |

Grovsiktingen er gjort med Haiku etter `verktoy/SIKTING.md`. Utvalget er lest i bolker på Opus.

## Krav 1: under 5 prosent nye i kategori 1–4 i siste referanserunde

- **Referanserunde 1:** 278 av de 4 386 nye kandidatene ble valgt i kategori 1–4, om lag 6 prosent. Kravet var ikke oppfylt.
- **Referanserunde 2:** 177 av de 7 375 nye ble valgt i kategori 1–4 i Opus-utvalget (2,4 prosent). Med de 42 kildene i kategori 1–3 som det blinde utvalget la til, er andelen om lag 3 prosent.

Krav 1 er oppfylt i runde 2.

## Krav 2: det blinde utvalget finner ikke nye kilder i kategori 1–3

**Avvik fra løypa:** Løypa sier to blinde utvalg på hele kandidatmengden (Opus og Sonnet). Med over 18 000 kandidater er det gjort ett blindt utvalg på Sonnet, bare av de 3 599 kandidatene fra referanserunde 2 som grovsiktingen beholdt, lest i åtte bolker med samme instruks som Opus-utvalget.

- Det blinde utvalget valgte 191 kilder. 135 av dem var allerede valgt, og 56 var nye. 42 av de nye er i kategori 1–3 etter Sonnets egen merking.
- Mange av de 42 er utenfor omfanget eller grensetilfeller: Job Corps (tiltak for unge utenfor skolen), skoletiltak mot eksklusjon, early college og skolevalg med utfall bare i høyere utdanning, og rene titler uten sammendrag. Noen er relevante og manglet, blant dem en norsk studie av skjerpede aktivitetskrav i sosialhjelpen med effekt på frafall, et dansk naturlig eksperiment med matematikkvalg i videregående, randomiserte forsøk med dual credit og early college, metaanalyser av skolebasert mentoring og diskontinuitetsstudier av avgangsprøver og dobbel algebra.
- Alle 56 er tatt inn i `valgt.txt` foreløpig. Kilder utenfor omfanget siles ut i det strenge utvalget og føres i `utelatt.tsv`.

Krav 2 er ikke oppfylt. Etter løypa kjøres derfor referanserunde 3 fra de 56 kildene (`kjor.sh`, runde 4), og et nytt blindt utvalg gjøres bare på de nye kandidatene.

## Svakheter

- **Ett blindt utvalg, ikke to,** og bare på siste runde. Kilder som både første utvalg og referanserunde 1 overså, fanges bare opp hvis de siteres av noe som er valgt senere.
- **Grovsiktingen med Haiku** har forkastet om lag halvparten av kandidatene på tittel og sammendrag. Kilder med bare tittel er mer utsatt.
- **Læreplasser og lærlingtilskudd** er tynt dekket med effektstudier, særlig i Norden. Det meste er tysk og sveitsisk.
- **Nordiske effektstudier** av fullføringstiltak er få. Mye av det norske materialet er evalueringer uten effektmål (kategori F), blant annet Ny GIV og oppfølgingstjenesten.
- **Det finske søket i Finna ga null treff.** Finland er derfor bare dekket gjennom OpenAlex.
- **Referansesøket følger bare OpenAlex-kilder.** Norske, svenske og danske rapporter uten OpenAlex-id kan ikke følges med skriptet.
