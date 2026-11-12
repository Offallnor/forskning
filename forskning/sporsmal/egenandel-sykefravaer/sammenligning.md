# Dobbelt uttrekk: egenandel ved sykefravær

Første uttrekk: `estimater.tsv`. Andre uttrekk, uavhengig, av en mindre modell (Sonnet) med den strammere instruksen: `estimater-b.tsv`.

- **Like tall:** De 12 tallene som står i begge uttrekkene, er like.
- **Ingen formfeil:** Andre uttrekk besto alle 250 kontrollene. Instruksen som ble strammet inn etter første test, virket.
- **Andre uttrekk fant mer**, blant annet:
  - **Motstridende tall i Böheim og Leoni 2011:** Sammendraget gir 8 og 11 prosent, mens hovedestimatet (små mot store bedrifter) gir 6,3 og 7 prosent. Begge tallene står nå i svaret.
  - **Størrelsen på den indirekte effekten hos Nilsson 2015:** 17 og 10 prosent.
  - **Effekten for alle ansatte hos Häll mfl. 2023:** 0,143 dager per kvartal.
- **Andre funn:** Andre uttrekk merket også at Pertold 2018 oppgir 2,3 dager i sammendraget og 2,2 dager i brødteksten.
- **Kostnad:** Om lag 237 000 tokens og 7,5 minutter for 17 fulltekster og 11 sammendrag.

## Kaldtest 7.11.2026: 41 nye kilder

Begge uttrekkene ble kjørt på nytt for kildene som kom inn gjennom referanser, det blinde utvalget og åpne versjoner. Første uttrekk er lagt til i `estimater.tsv`, andre i `estimater-b.tsv`.

- **Omfang:** 30 av 41 kilder har tall. Første uttrekk har 68 tall, andre 56. 42 tall står i begge, og i 26 av 30 kilder har uttrekkene minst ett tall felles.
- **Sprik som ble lest for hånd:**
  - Puhani og Sonderhof 2009: første uttrekk har 2 og 1,2 dager (hele utvalget, side 17), andre har 2,4 dager (dem som ble i samme bedrift, side 6). Begge stemmer. 2,4 er lagt til i `estimater.tsv` og i svaret.
  - Pichler og Ziebarth 2016: 20 prosent i sammendraget, 22 prosent i brødteksten. Begge står i kildene. Svaret bruker 20.
  - van Sonsbeek og Gradus 2012: første uttrekk oppgir 13 som prosent (side 16), andre som prosentpoeng (side 21). Kilden bruker begge. Svaret bruker prosent, som stemmer med utregningen på side 16.
  - Ziebarth 2009: andre uttrekk beskriver reformen som kutt fra 100 til 80 prosent, men kuttet som studeres er fra 80 til 70 prosent fra sjuende uke (side 2–3). Tallene er like.
  - Boss 2000: andre uttrekk tok med et sitert tall fra en annen studie (27 prosent), første gjorde det ikke. Ikke brukt i svaret.
- **Ingen oppdiktede tall** ble funnet i stikkprøvene.
