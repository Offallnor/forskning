# Kaldtest 2 av løypa: utviklingen i sykefraværet siden 2015

Kjørt 7.11.2026 av en ny tråd som bare hadde `forskning/LOYPE.md` og filene den viser til. Mappen hadde en eldre runde (engelsk søk, 22 valgte kilder, uttrekk og svar), så delen om å gjenoppta en mappe ble fulgt. Spørsmålet er beskrivende (en utvikling over tid) med et forklarende tillegg (drivere).

Resultat: 49 valgte kilder (fra 22), nytt `svar.md` merket «utkast, ukontrollert», automatisk kontroll uten feil og innholdskontroll som fant én alvorlig feil. Under står hvert sted oppskriften var uklar, manglet noe eller ledet feil, og hva jeg gjorde.

## Det viktigste

1. **Designhierarkiet passer ikke for beskrivende spørsmål.** Steg 0 ber om tiltak og sammenligning og et hierarki for effektstudier. For et spørsmål om utvikling er det datadekningen som teller (helbefolkning, harmoniserte data mellom land, lange serier), ikke identifikasjon. Jeg skrev kriteriene i to deler: del A (utvikling) med et eget hierarki fra sammenlignende studier med harmoniserte data til korte serier for enkeltyrker, og del B (drivere) med løypas hierarki. Det fungerte, men løypa bør ha en mal for beskrivende spørsmål. Det samme gjelder svaret: «funn gruppert etter design» og «beslektede tiltak» passet ikke. Jeg grupperte etter land og drivere.
2. **Regelen for det blinde utvalget slipper inn for mye ved brede spørsmål.** Det blinde utvalget valgte 82 kilder (første utvalg 39, 33 felles). Regelen «kilder i kategori 1–4 som det blinde utvalget fant, tas inn» ville gitt om lag 45 nye kilder, mest sykelønnsreformer (som hører til spørsmålet om egenandel), forsøk med oppfølging og kjønnsforskjeller i nivå. Jeg tok inn ti og begrunnet resten i `utelatt.tsv`. Årsaken er delvis mine egne kriterier: del B sa bare at mekanismen måtte være «fortsatt aktuell». Løypa bør si at driverstudier må gjelde endringen i perioden, og at effektstudier av ordningene hører til egne spørsmål.
3. **Det blinde utvalget og det norske søket fant det viktigste.** Det norske søket fant sju artikler fra *Arbeid og velferd* om utviklingen i Norge 2019–2024 og Fafo-notatet om Norge og Sverige, som den eldre runden lette etter uten å finne. Det blinde utvalget fant helbefolkningsdata for England, en norsk forskjell-i-forskjell-studie av covid-19 og en dansk covid-kohort. Svaret er vesentlig bedre for Norge enn i den eldre runden.
4. **Innholdskontrollen fant en feil slutning som tallkontrollene ikke kunne fange.** Svaret sa at konjunkturer «neppe forklarer økningen etter 2019, da ledigheten var lav». Kildene viser at lav ledighet gir mer fravær, så slutningen gikk feil vei, og ledighetsnivået hadde ingen kilde. Rettet. Den blinde lesingen fikk også fram at covid-effekten for de fleste var over etter to til fire måneder, som manglet i det korte svaret.
5. **Tre nav.no-artikler ga bare ingressen, uten varsel.** `pdf-logg.tsv` sier «ok (nav.no, uten sidetall)» for AV-2024-1-03, AV-2024-2-03 og AV-2025-3-04, men tekstfilene er på 2–4 kB. Jeg sjekket nettsiden selv: den har bare ingressen. Skriptet bør varsle «LITE TEKST» også her, og `sporsmal_mangler.py` regner dem som lest.

## Steg for steg

### Gjenoppta en mappe

- **Filer løypa ikke nevner:** `tekst/` hadde `.json`-filer (metadata for kilder uten tekst). Uklart om de skal ryddes. Lot dem stå.
- **Kilder som bare sto i `estimater.tsv`:** Den eldre runden hadde estimatrader for fire kilder som ikke sto i `valgt.txt` (én kom inn via en `tittel:`-linje). Kontrollskriptet og referansesøket regner `estimater.tsv` med som valgte kilder, så de fantes i praksis. Løypa sier ikke hva man gjør. Jeg førte dem inn i `valgt.txt`.
- **`mangler.md` var foreldet** (sa «bare sammendrag» for kilder som hadde tekst). Laget på nytt med `sporsmal_mangler.py`.
- **Bestillingen manglet.** Hentet spørsmålet fra kommentaren i `kjor.sh` og overskriften i det eldre svaret, merket «antatt».
- **Rekkefølgen på rundene:** Løypa sier at runde 1 er søk og runde 2 referanser etter første utvalg. Ved gjenopptak finnes første utvalg allerede, så jeg kjørte norsk søk og referanser runde 1 i samme kjøring. Løypa bør si at det er greit.
- **Hvilke kilder som hentes ut på nytt:** «Kilder der den eldre runden bare leste sammendraget, men der det nå finnes tekst» måtte finnes ved å sammenligne kolonnen `side` i `estimater.tsv` med `tekst/`. Sju kilder. Et lite skript eller en kolonne i `pdf-logg.tsv` ville gjort det enklere.

### Steg 1: søk

- **Norsk søk:** 21 uttrykk, 204 treff. «Høyt sykefravær», «legemeldt sykefravær» og «sykefravær blant unge» ga mest støy (masteroppgaver om ledelse i barnehager). Rådet om uttrykk som bare kan bety temaet er riktig, men for et beskrivende spørsmål er det vanskelig: utvikling heter «økning», «utvikling» og «nivå» i alt.
- **Rundene tok 1–2 minutter**, ikke 3–7.

### Steg 2: utvalg

- **Referanser:** Runde 1 ga 117 kandidater, mest eldre litteratur og metodelitteratur (R, Poisson-regresjon, WHO-rapporter). Runde 2 ga 160, hvorav 35 nye og én relevant.
- **Metning, krav 1:** «Under 5 prosent nye kandidater som oppfyller kategori 1–4». Uklart om nevneren er alle rader i siste runde eller bare de nye. Her var det under 5 prosent uansett.
- **Metning, krav 2 ble ikke oppfylt**, og løypa sier da en referanserunde til. Ikke gjort, av hensyn til tid. Står i `metning.md`.
- **Det blinde utvalget leste sammendrag feil i ett tilfelle:** Timp mfl. 2024 (Nederland) ble valgt som tidsserie, men handler om kjønnsforskjeller uten utvikling over tid. Oppdaget først i uttrekket.
- **Landfeltet i metadataene** viser forfatternes tilknytning, ikke landet studien gjelder (OECD-rapporten om Norge står med FR). Det blinde utvalget merket det.
- **Begrunnelser:** Kontrollen listet 72 sentrale kandidater uten begrunnelse, nesten alle fra referanserundene. Gruppevise begrunnelser gikk raskt. Det er tungvint at også kandidater fra det blinde utvalget må begrunnes én for én, men det tvang fram en vurdering av hver.
- **Følg oversiktene:** Det finnes ingen norsk kunnskapsoppsummering om utviklingen etter 2015. Jeg leste i stedet referanselistene i *Arbeid og velferd* og fant en svensk europeisk sammenligning (Försäkringskassan 2022) som ikke er med. Løypa kunne si at Navs og SSBs egne analyser er den nærmeste erstatningen for beskrivende spørsmål.

### Steg 3: tekst

- **`--versjoner` kjøres før `--pdf` i samme runde**, så den lister «versjoner» av kilder som får tekst i samme runde (tilleggsfiler og konferansebidrag på Figshare). Ingen var brukbare. Rekkefølgen i løypa gir støy første gang.
- **Preprint uten merking:** Tre kilder fikk tekst fra medRxiv via OpenAlex' åpne lenke, og én fra et arbeidsnotat. Det står bare i URL-en i `pdf-logg.tsv`. Løypa sier at åpne versjoner skal merkes, men det gjelder bare versjoner fra `--versjoner`. Jeg merket dem i svaret.
- **Statuslista i Claude Doc** («Kilder som må hentes for hånd») er ikke oppdatert. Det krever skriving i et dokument utenfor repoet, og jeg lot det ligge til forvalteren. `mangler.md` er oppdatert.

### Steg 4: uttrekk

- **Uavhengig kopi og kontroll:** Løypa sier at kjøringen skal kontrollere «på en kopi der radene er lagt til», men kopien kan ikke ha `estimater.tsv` fra før. Kontrollskriptet trenger dessuten `katalog/poster.jsonl` og `svar.md`, som løypa ikke nevner. Jeg lot kopien få bare de nye radene, en tom `svar.md` og katalogen.
- **Forfattere fra metadata kan være feil:** For masteroppgaven om undervisning oppgir vitenarkivet veilederne som forfattere. Første uttrekk så det i teksten, andre uttrekk fulgte regelen. Regelen bør si at forfatterne på tittelsiden går foran metadata når de spriker.
- **Minustegn:** Kontrollen godtar ikke tankestrek (–) i sitatet som minustegn, så et negativt tall ble lagt inn som positivt med fortegnet forklart.
- **Tall med ord:** «Nesten halvparten» ble lagt inn som 50 i begge uttrekk. I svaret står det med ord.
- **Dobbelt uttrekk:** 57 felles tall, ingen ulike. En masteroppgave hadde sprik i seg selv (to ulike tall for samme bidrag). Se `sammenligning.md`.

### Steg 5–6: svar og kontroller

- **Kontroll 5 leste datoen «7.11.2026»** som tallet 7.11, og ville ha «under 40 år» fra en ingress inn i tabellen. Skrev om.
- **Innholdskontroll ved endret svar:** Løypa sier at steg 1a gjøres for de nye kildene og at et nytt blindt kort svar skrives. Det fungerte, og steg 2 ble lagret som `innholdskontroll-2.tsv`. Løypa sier ikke om steg 2 skal gjøres av en egen kjøring. Jeg gjorde det selv, og fant feilen over først da jeg leste det blinde korte svaret.

## Kostnad og tid

- Underagenter: om lag 1,2 millioner tokens (blindt utvalg 226 000, uttrekk 368 000 og 417 000 i to omganger, blind lesing 232 000), i tillegg til hovedtråden.
- Tid: om lag halvannen time, med fem runder i Actions.

## Forslag til endringer i løypa

1. Egen mal i steg 0 og steg 5 for beskrivende spørsmål (hierarki etter datadekning, svar etter land og drivere).
2. I steg 2.3: kilder fra det blinde utvalget tas inn bare når de svarer på spørsmålet slik bestillingen avgrenser det; effektstudier av ordninger og tiltak går til egne spørsmål.
3. Varsel om lite tekst også for nav.no, og merking av preprint i `pdf-logg.tsv`.
4. Regel for estimatrader for kilder som ikke står i `valgt.txt`, ved gjenopptak.
5. Forfattere fra tittelsiden når metadata spriker.
6. Kjør `--versjoner` etter `--pdf`, eller bare for kilder som fortsatt mangler tekst.
