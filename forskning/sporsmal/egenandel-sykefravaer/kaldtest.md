# Kaldtest av løypa: egenandel ved sykefravær (7.11.2026)

Løypa i `forskning/LOYPE.md` ble kjørt for egenandel ved sykefravær av en ny tråd som bare hadde LOYPE.md og filene den viser til. Mappen hadde resultater fra en eldre, enklere runde (søk, utvalg av 28 kilder, uttrekk, svar og innholdskontroll). Svaret er merket «utkast, ukontrollert».

## Resultat

- Utvalget gikk fra 28 til 71 kilder (pluss åpne og publiserte versjoner). Svaret bygger nå på 54 kilder, 40 i fulltekst.
- Referansesporingen og det blinde utvalget fant flere sterke reformstudier som manglet: Puhani og Sonderhof, Pichler og Ziebarth, Ziebarth 2009, De Paola mfl., Scognamiglio, Marie og Vall Castelló, Halla mfl., Fevang mfl. 2015, og åpne versjoner av Koning, de Groot og Koning, Kyyrä og Paukkeri, Westergaard-Nielsen og Pertold og The Sick Pay Trap.
- Innholdskontrollen fant én alvorlig feil i svaret: den norske studien av arbeidsgiverperioden konkluderer med at den nesten ikke reduserer det samlede fraværet, mens svaret ga inntrykk av at arbeidsgivers egenandel virker. Det var også med i den eldre runden, men den bygde bare på sammendraget. Rettet etter lesing av kilden.
- Automatiske kontroller: 0 feil av 815.
- Tid: om lag en time, med fem runder i GitHub Actions. Underagenter brukte om lag 1,4 millioner tokens (blindt utvalg 225 000, uttrekk i tre omganger 940 000, blind lesing 245 000), i tillegg til hovedtråden.

## Der oppskriften var uklar, manglet noe eller ledet feil

### Oppsett og gjenopptak

1. **Gjenopptak av en mappe med eldre runde er ikke beskrevet.** LOYPE sier ikke hvilke steg som skal gjøres på nytt. Jeg skrev kriterier, gjorde ikke nytt engelsk søk, kjørte norsk søk og referanser, og bygde videre på eksisterende uttrekk og svar.
2. **Workflowen kjører alle `kjor.sh` i alle mapper.** Mappene for gradert sykmelding og utvikling har aktive `--pdf`-linjer, så de kjøres hver gang. Det er ikke farlig (hentet tekst hoppes over), men koster tid og kall. Forslag: kjør bare `kjor.sh` som er endret i pushen.
3. **Hvordan man venter på Actions, står ikke.** Jeg ventet på en ny commit «Spørsmålssøk: resultat» på grenen. Det står heller ikke hva man gjør hvis kjøringen feiler, eller hvor loggen er.
4. **En kjøring tar 3–7 minutter.** Hver runde (referanser, tekst, versjoner, tekst for versjoner) krever en ny kjøring. LOYPE bør si hvilke steg som kan kjøres i samme runde.

### Steg 0: kriterier

5. **«Spørsmålet slik bestilleren stilte det, og hva svaret skal brukes til» fantes ikke.** Bare kommentaren i `kjor.sh`. Jeg antok bruken. LOYPE bør si hvor bestillingen skal stå.
6. **«Kriteriene skrives før utvalget» lot seg ikke gjøre** når mappen hadde en eldre runde. Eksempelet for gradert sykmelding sier selv «skrevet etter første utvalg».

### Steg 1: søk

7. **Norsk søk med enkeltord gir mest støy.** LOYPE sier «hele norske uttrykk», men jeg brukte enkeltord som «egenandel», «dekningsgrad» og «sykelønn». Det ga 242 treff, mest botanikk, byggeprosjekter og helsetjenester. Bare to ble valgt. LOYPE bør gi eksempler på gode og dårlige ord.

### Steg 2: utvalg

8. **Hva `uttrykk` gjør i `--referanser`, står bare i skriptet.** En kilde tas med når minst to valgte kilder peker på den, eller når uttrykket står i tittel eller sammendrag.
9. **To-peker-regelen slipper inn mye metodelitteratur** (Mostly Harmless Econometrics, DiD-inferens, RD-guider) og studier av lovpålagt sykelønn i USA. 368 rader i runde 1.
10. **`referanser.tsv` overskrives i runde 2.** LOYPE sier ikke at runde 1 skal tas vare på. Jeg tok en kopi utenfor repoet.
11. **Referansesporingen følger bare OpenAlex-id-er.** Norske kilder fra vitenarkivet og *Arbeid og velferd* gir ingen referanser.
12. **«Nesten ingen nye kilder» etter runde 2 har ingen terskel.** Runde 2 ga 4 nye av 134 kandidater, som jeg tolket som nær metning. Det blinde utvalget fant likevel 14 til. Metningsregelen bør også gjelde det blinde utvalget.
13. **«Sentral kandidat» er definert i kontrollskriptet, ikke i LOYPE** (oversikt, persentil minst 0,9 eller minst 50 siteringer). Med referansene ble det 274 sentrale kandidater å begrunne. Jeg brukte regler på tittelord og skrev begrunnelser for hånd for de viktigste. Kontroll 6 regner også valgte kilder uten egne tall (der en annen versjon er brukt) som utelatt.
14. **Rekkefølgen tekst, blindt utvalg og versjoner er ikke praktisk.** Versjoner står i steg 3, men må komme før tekst for å spare runder. Det blinde utvalget står før tekst, men det koster en runde å vente på det. Jeg kjørte uttrekk for første utvalg mens det blinde utvalget og ny tekst ble hentet.
15. **Hva det blinde utvalget skal få se, står ikke.** Jeg ga det kriterier, kandidater, referanser (begge runder) og norske kandidater, og forbød `valgt.txt`, svar, estimater og utelatte.
16. **Hva man gjør med kategori 5-kilder som bare det blinde utvalget tar med**, står ikke. Jeg tok dem ikke inn og begrunnet dem.
17. **«Følg oversiktene» kunne ikke gjøres.** Det finnes ingen norsk kunnskapsoppsummering om sykelønn i kandidatene, og de tre oversiktene som finnes, har ikke tekst. LOYPE sier ikke hva man gjør da.
18. **Samme materiale skal merkes, men `valgt.txt` har bare kommentar.** `valgt-blind.tsv` har en egen kolonne.
19. **Lange id-er fra vitenarkivet er lette å skrive feil.** Jeg skrev feil hale første gang og oppdaget det selv. Skriptet sjekker ikke at id-ene i `valgt.txt` finnes før kjøring.

### Steg 3: tekst

20. **Hvordan en åpen versjon tas inn, står ikke.** Jeg la versjonens id i `valgt.txt` med kommentar «åpen versjon av …». Svaret lenker da til arbeidsnotatet, ikke til den publiserte artikkelen.
21. **`--versjoner` må kjøres flere ganger.** Hver runde med nye kilder gir nye versjoner, som igjen krever en tekstrunde.
22. **Tittelkontrollen slapp gjennom feil dokument.** Teksten for Nandi mfl. 2018 er en annen rapport om foreldrepermisjon fra samme senter. Tittelordene står i begge.
23. **Skannede PDF-er gir nesten tom tekst** uten at `pdf-logg.tsv` sier fra (Johansson og Palme 2002: tekst på tre av 34 sider).
24. **Statuslisten som Claude Doc ble ikke laget.** LOYPE sier «lag eller oppdater», men ikke om listen for gradert sykmelding skal utvides eller om det skal lages en ny per spørsmål. `mangler.md` er oppdatert.

### Steg 4: uttrekk

25. **Tall skrevet med ord kan ikke registreres.** Instruksen krever sifre i sitatet. Hovedfunn som «um drei Prozent» (Ziebarth 2025) og «to prosentpoeng» (King mfl. 2026) falt ut.
26. **Sekundærsitater er ikke regulert.** Det ene uttrekket tok med et tall en oversikt siterte fra en annen studie, det andre lot være.
27. **Design er kodet ulikt.** Et randomisert brev om kontroll ble kodet som rct i det ene uttrekket og ikke i det andre. Instruksen har ingen kategori for simulering eller modell.
28. **Modellvalg står ikke.** Første uttrekk kjørte på samme modell som tråden, andre på Sonnet.
29. **Uavhengigheten er sårbar.** Én underagent leste to linjer av `estimater.tsv` ved et uhell. Uttrekkene leser filer i samme mappe som svaret.

### Steg 5–6: svar og kontroller

30. **Innholdskontrollen må kjøres på nytt når svaret endres, men LOYPE sier ikke om den skal gjelde hele svaret eller bare nye kilder.** Jeg gjorde blind lesing for de 32 nye kildene og skrev et nytt kort svar på alle. Sammenligningen ligger i `innholdskontroll-2.tsv`.
31. **Kontroll 5 sjekker bare tall i `estimater.tsv`.** Et tall som bare står i andre uttrekk (2,4 dager hos Puhani og Sonderhof), måtte flyttes over.
32. **Forfatternavn fra metadata gir noen ganger feil rekkefølge** sammenlignet med vanlig sitering (Westergaard-Nielsen og Pertold). Jeg fulgte metadata, slik LOYPE sier.

## Forslag til endringer i LOYPE.md

- Eget avsnitt om å gjenoppta en mappe med eldre runde.
- Én kjøring per runde med fast rekkefølge: referanser, versjoner, tekst i samme `kjor.sh`.
- Bestillingen skrives i `kriterier.md` av den som bestiller.
- Definisjonen av sentral kandidat inn i LOYPE, og et skript som lager forslag til `utelatt.tsv`.
- Ta vare på hver referanserunde (`referanser-1.tsv`, `referanser-2.tsv`).
- Sjekk for tom tekst og for feil dokument med mer enn tittelord (forfatternavn, år).
- I `UTTREKK.md`: tillat tall med ord når tallet er skrevet ut i utfall, og si hva som gjelder for sekundærsitater.
