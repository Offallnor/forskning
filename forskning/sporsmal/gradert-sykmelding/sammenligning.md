# Dobbelt uttrekk: gradert sykmelding

Første uttrekk: `estimater.tsv`. Andre uttrekk, gjort uavhengig av en mindre modell (Sonnet) med samme instruks og samme filer: `estimater-b.tsv`.

## Resultat

- **Tallene stemmer.** Alle tallene som står i begge uttrekkene, er like, også konfidensintervallene. Ingen tall er i strid med hverandre.
- **Sitatene holder.** Alle sitatene i andre uttrekk stod ordrett i teksten på oppgitt side.
- **Andre uttrekk fant flere tall.** Fire av dem var viktige og er lagt inn i første uttrekk etter at sitatene ble kontrollert:
  - full og gradert uførepensjon i Viikari-Juntura mfl. 2017
  - effekten for psykiske lidelser i Kausto mfl. 2014
  - det ujusterte nederlandske resultatet (1,40 ganger lengre fravær)
- **Flere formfeil i andre uttrekk.** Tekst og prosenttegn stod i tallfeltene, for eksempel «70 / 68 / 71», «8.0%» og «four of them», og ett tall gjaldt en holdning, ikke en effekt. Kontrollene fanget alle disse. Instruksen er nå strammet inn.
- **Fortegn.** Begge uttrekkene skrev kostnadsreduksjonen ulikt (2395 og -2395). Kontrollen sammenligner nå tall uten fortegn i svaret, fordi retningen står i ord.

## Kostnad

Andre uttrekk brukte om lag 141 000 tokens og 3,5 minutter med Sonnet for 12 fulltekster og 14 sammendrag.

## Full gjennomkjøring 9.11.2026, parti 1 (elleve kilder)

Uttrekk A (samme modell som tråden, 31 rader, flyttet til `estimater.tsv`) og uttrekk B (Sonnet, 33 rader, lagt til i `estimater-b.tsv`). Seks kilder som før bare var lest i sammendrag, er hentet ut på nytt fra fulltekst, og de gamle sammendragsradene er tatt ut av `estimater.tsv`. `estimater.tsv` har fått kolonnen `gruppe` (tom for eldre rader).

- Felles tall var like i alle elleve kilder. Ingen tall i A manglet i kilden.
- B fant i tillegg: Maas mfl. 2021 −85,7 dager ved 70. persentil når varig gradert retur regnes som retur, og 21,8 ved 10. persentil (står i samme sitat som A); Kristoffersen 2019 0,312 (effektiv fraværslengde, fravær over 14 dager); FHI-forskermøtet 2013 63 prosent økt returrate (gjengitt fra Viikari-Juntura mfl. 2012, som er lest direkte og derfor ikke brukes).
- A fant i tillegg: Lie 2014 12 uker (tidspunktet der en liten positiv effekt viser seg), Lie 2010 13 dager, Kausto 2014 18,9.
- Lie 2014 er den norske studien FHI-oversikten fra 2018 omtaler med HR 0,37. Begge uttrekkene leser 0,37 (kausal modell) og 0,27 (ujustert) for gradert start, side 27.

## Parti 2 (9.11.2026): Brage, Kann og Nossen 2013, Hartikainen 2025, Viikari-Juntura mfl. 2011

Uttrekk A 23 rader (flyttet til `estimater.tsv`), B 15 rader (`estimater-b.tsv`). Alle felles tall er like. A har i tillegg beskrivende tall om bruken (Nav 2013: 15 og 57 prosent), effekten etter reformen 2004 (−1,26 prosent), kostnad i det finske forsøket (1882 euro) og forløp etter delvis sykmelding hos Hartikainen. B har i tillegg tapte arbeidsår ved arbeidsledighet hos Hartikainen (−1,47 og −0,64 år). HR i den finske sluttrapporten er 1,76 (KI 1,20–2,82), mens artikkelen fra 2012 oppgir 1,76 (KI 1,21–2,56); begge står i kildene, og svaret bruker artikkelen.

## Nye kilder 10.11.2026

Elleve kilder fra to nye blinde utvalg er hentet ut to ganger: første uttrekk med samme modell som tråden (15 rader), andre med Sonnet (34 rader).

- **Samme tall der begge har hentet ut:** de svenske instrumentstudiene (Andrén og Andrén 2009, Andrén 2011 om arbeidsledige og arbeidstakere, Andrén og Andrén 2008) har de samme verdiene for effekten for dem som ble gradert (−0,130, 0,346, 10 prosentpoeng), på samme side.
- **Forskjellen i antall rader skyldes oversiktene.** Det andre uttrekket gjengir tall fra primærstudiene slik Sabariego mfl. 2018, Derbyshire mfl. 2024 og Nogawa og Kojimahara 2018 refererer dem. Det første følger `UTTREKK.md` og henter ikke tall fra en oversikt når primærstudien selv er valgt og lest. Oversiktene gjengir samme studie med ulike tall (det finske forsøket: HR 1,84, 1,76 og 1,60), og Sabariego skriver «16-fold» om Markussen 2010, som trolig er feil. Svaret bruker tallene fra primærstudiene.
- **Ingen oppdiktede tall** i noen av uttrekkene. Begge kontrollerte sitatene mot teksten.
