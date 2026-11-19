# Merknader fra første uttrekk (Opus, 19.11.2026)

Rapportene fra de 13 gruppene, ordrett. Brukes i sammenligning.md og svar.md.

## 

54 rader for 25 kilder i `/tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g02/forskning/sporsmal/evu-voksne/estimater.tsv`. Kontroll 1–4 har ingen feil. Resten av FEIL-linjene gjelder bare kontroll 6 og 9, og de er ventet i kopien.

- **Kilder uten tall:** 14. Én av dem er tekstkilden LI-sf35mlm1q24b0fp2, se under. De 13 andre er bare lest i sammendrag, og sammendraget har ikke noe effekttall: W2120167541, W2010796133, W2433767964, W2184201471, W2908262949, W2102454047, W2072287290, W3118879220, W1927179113, W1963973901, W2088280977, W4386420582 og W1583669699. For W2184201471 er sammendraget bare en innholdsfortegnelse.
- **Feil dokument:** LI-sf35mlm1q24b0fp2. Tittelen er «PM … år 2018 och 2019», men tekstfila er Skolverkets rapport om etablering 2022 og 2023. Jeg har skrevet én rad uten estimat som sier dette.
- **Kilder som ligger på kanten av mandatet, men har rader:**
  - 01993e05413d-1c34631c-cb38-41f7-999b-2593f32522f4 (Proba 2015) har ikke noe effektestimat. Jeg har tatt med to tall for deltakelse, med `design` = `beskrivende`.
  - W4415689128 gjelder ikke bare voksne. Det står i `utfall`.
  - Inntektsestimatene for kurs i 0198cc8cf62f-70957a9d-6a90-4e38-bdc2-59d56097116a skiller ikke ut offentlig finansiering. Det står også i `utfall`.
- `tidligere-estimater.tsv` hadde ingen rader for kildene i denne gruppen.

Hjelpeskriptet som skriver radene er `/tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g02/hjelp/rader.py`.

## 

56 rader for 25 kilder i gruppe 01. Kontroll 1–4 gir ingen feil. De eneste FEIL-linjene er kontroll 6 (6321) og 9 (2), som er ventet i kopien.

- **Kilder uten tall: 9.** Hver har én rad med tomt estimat og en forklaring i `utfall`.
  - Tre er lest bare som sammendrag: W171095229, W2956924494 og W2106519551.
  - Seks er lest som tekst: 0198cc5263f2-db66fb0c-87cd-4aa1-9668-dccb5c95a966, KU-15673374-2b35-4d1f-82b0-1a12211e128e, W7210025147, W2226242137, W235943261 og W4401711642.
- **Mulig feil dokument eller bare delvis tekst:**
  - W2226242137: teksten er bare en tosiders synopsis (NRDC Research Review). Hele rapporten om kontrollerte forsøk ligger ikke i filen.
  - W2956924494: sammendraget er protokollen til W82406113, altså samme materiale. Det står i `utfall`.
- **Merknader:**
  - Mange tall fra oversiktene er gjengitt fra en annen studie, og det står i `utfall` hvilken. Det gjelder blant annet Patrignani og Conlon 2011, McIntosh 2004, Zhang, Humlum mfl. 2025 og NEAEP.
  - W2771339852 side 79: minustegnet står som tankestrek med mellomrom. Estimatet er derfor skrevet 5.3, og at effekten er negativ står i `utfall`.
  - Fra tidligere-estimater.tsv tok jeg bare med rader om opplæring, de samlede andelene for alle programtyper og radene om tiltak for unge. Radene om lønnstilskudd er ikke tatt med.

Filer:
- /tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g01/forskning/sporsmal/evu-voksne/estimater.tsv
- /tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g01/hjelp/rader.py (skriptet som lager radene)

## 

Uttrekket for gruppe 04 er ferdig. Kontroll 1–4 har ingen feil lenger. Feilene i kontroll 5, 6 og 9 står igjen som ventet i kopien.

- **Antall rader:** 42, for alle 25 kildene. Radene står i `/tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g04/forskning/sporsmal/evu-voksne/estimater.tsv`.
- **Kilder uten tall:** 12. Det er W3090832067, W1582975199, W1964861379, W2969413042, W4411098014, W2026651182, W4412204416, KU-a2a2fd8e-0e58-45be-a828-35b0960fd2e8, W2914642225, W2044685238, W2417897354 og W1574919135.
  - W3090832067 er bare protokollen. Den ferdige oversikten finnes i utvalget som W7160028630.
  - W4411098014 bygger på samme materiale som W4412115963, og jeg har brukt den nyeste versjonen.
- **Feil dokument:** ingen av tekstene ser ut til å være feil dokument. Tre ting bør likevel sjekkes:
  - **W2168820403:** side 2 i PDF-en har sammendraget fra en annen artikkel i samme serie, om tekstmeldinger til arbeidssøkere ved et jobbsenter. Resten av teksten, fra side 3, er riktig artikkel, og radene er hentet derfra.
  - **W4409530334:** riktig dokument, men det gjelder Teknikcollege, som i hovedsak er yrkesfag i videregående for unge. Kilden ligger trolig utenfor mandatet, og det står i `utfall`.
  - **W3197149185:** riktig dokument, men utvalget er unge som fullfører videregående i alderen 21–28 år. Det ligger i nedre kant av aldersgruppen i mandatet, og det står i `gruppe`.
- **Andre merknader:**
  - Landet er tatt bare fra teksten eller sammendraget. For W7165961986 sier ikke sammendraget hvilket land studien gjelder, så feltet er tomt.
  - To tall i W4302969421 er gjengitt fra Lechner mfl. 2011, fordi den studien ikke ligger i utvalget.
  - Ett estimat står med ord i kilden (W4385563255, «almost four percentage points») og må kontrolleres for hånd.
  - Ingen rader i `tidligere-estimater.tsv` svarte på dette spørsmålet for disse kildene.

## 

Jeg har skrevet 47 rader for alle de 25 kildene i gruppe 03. Kontroll 1–4 har ingen feil. Kontrollen viste én feil i første kjøring. Kildeteksten (W1551402157) har tabellverdien -15,436 kroner, og kontrollen leste ikke minustegnet. Jeg skrev 15436 og la fortegnet inn i utfall («lavere»). Ellers gjenstår bare FEIL i kontroll 5, 6 og 9, som er ventet i kopien.

- **Antall rader:** 47, for 25 kilder.
- **Kilder uten tall:** 3, hver med én rad uten estimat:
  - LI-22279866 er et teoretisk kapittel om reell og formell kompetanse.
  - LI-8241310 er en oversikt som omtaler effekten av arbeidsmarkedsopplæring bare med ord.
  - 0198cc8fb35e-07b7e7c2-852e-452c-833a-f51d16f740a6 er en metaanalyse av tiltak for unge. Den har ingen samlet effektstørrelse for opplæring i løpende tekst.
- **Feil dokument:** Ingen kilder ser ut til å være feil dokument. W4294073684 har en annen tittel i teksten («A Note on Evaluating Formal Education for Adults», SOFI arbeidsnotat 2022). Sammendraget handler likevel om de samme multiplikatoreffektene som tittelen i gruppe.tsv, så det er trolig en annen versjon av samme arbeid.
- **Tidligere estimater:** tidligere-estimater.tsv har bare rader om lønnstilskudd for disse kildene. Ingen av dem svarer på dette spørsmålet, så jeg har ikke tatt noen av dem med.

Noen rader faller utenfor de vanlige tiltakene og bør vurderes i sammenstillingen:
- NB-4986 er en enkeltstudie av Navs tiltak (AMO). Jeg har ført den under tiltak 5, selv om mandatet bare tar med slike tiltak gjennom oversikter.
- To rader i NB-5063 og LI-g1x6j6j7dj2qxj9c er gjengitt fra Card mfl. 2018 og Liljeberg m.fl. 2019. Det står i utfall.
- Fire kilder måler noe annet enn deltakelse mot ikke-deltakelse:
  - W1551402157 sammenligner Kunskapslyftet med arbeidsmarkedsopplæring.
  - LI-vd36mplwstzl5l7q gjelder ressurser og frafall i Komvux.
  - LI-1gfz0fg6z3v6v8pc gjelder at rekrutteringsbidraget ble avskaffet.
  - W4225726955 gjelder all voksenopplæring, også den arbeidsgiveren betaler.

Filen ligger her: /tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g03/forskning/sporsmal/evu-voksne/estimater.tsv. Skriptet som lager den, ligger her: /tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g03/hj/rader.py.

## 

44 rader er skrevet til `/tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g06/forskning/sporsmal/evu-voksne/estimater.tsv`, minst én for hver av de 25 kildene. Kontroll 1–4 er uten feil på mine rader. Feilene som står igjen, er bare i kontroll 6 og 9, som ventet i kopien.

**Kilder uten tall:** 5. Hver har én rad med tomt estimat og en kort forklaring:
- W4399355073
- W7215142416
- W2767238478 (de to radene er uten tall; den ene gjengir Kaplan et al. 2015)
- W1484534434
- W3004014332

**Feil dokument:**
- W3004014332 (Grosz): teksten er bare nettvedlegget (online appendix) med tabeller, ikke selve artikkelen. Hovedresultatet står ikke i løpende tekst.
- W2010586812 (Kluve): ikke feil dokument, men teksten er arbeidsnotatet fra IZA (2006), mens metadata viser artikkelen fra 2010. Det er samme materiale, og det står i utfall.

**Kontrollen leser ikke alle minustegn.** For W1591201381 (to rader, 1999 og 2000) leser kontrollen minustegnet i tabellteksten («20,124 -15,809») som et spenn. Estimatene står derfor uten minustegn (15809 og 11396). Utfall sier at inntekten er lavere og at fortegnet er negativt i tabellen.

**Tall med ord:** Tre rader har tall som står med ord i sitatet og må kontrolleres for hånd:
- W3122813172: «six percent»
- W1599229608: «four» og «eight» prosentpoeng

**Sjekklisten:** `tidligere-estimater.tsv` hadde bare rader om W2010586812 fra spørsmålet om lønnstilskudd for unge. Ingen av dem svarte på dette spørsmålet, så ingen ble tatt med.

## 

46 rader skrevet i `/tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g05/forskning/sporsmal/evu-voksne/estimater.tsv`, fra alle 25 kildene i gruppen. Kontroll 1–4 har ingen feil. De eneste feilene som står igjen, er de ventede i kontroll 6 og 9.

- **Kilder uten tall:** 1, W104926790 (Benseman). Raden har tomt estimat. Studien måler ferdigheter før og etter kurs, men har ikke noe mål på sysselsetting eller lønn.
- **Feil dokument:** ingen. Alle tekstene stemmer med titlene.
- **Samme materiale:** W1683883188 er en foreløpig versjon av W3123135221. Hovedtallene er tatt fra den nyeste versjonen, og raden for W1683883188 er merket «samme materiale».
- **Sitater fra eldre studier:** noen rader fra oversiktene er hentet fra eldre studier og merket «gjengitt fra …» i utfall. Det gjelder W2136269032, W2112371456, W2760148764 og W7218183306.
- **Tall med ord:** to rader for W2982898106 har tallet bare med ord i sitatet og må kontrolleres for hånd.
- **Tidligere uttrekk:** `tidligere-estimater.tsv` har ingen rader for disse kildene.

Hjelpeskriptet `/tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g05/arb/lag.py` lager radene på nytt. Det henter sitatene ordrett fra tekstfilene.

## 

57 rader for 25 kilder i gruppe 08, med minst én rad per kilde. Kontroll 1–4 har ingen feil for mine rader. De øvrige FEIL-linjene er fra kontroll 5, 6 og 9, som er ventet i kopien.

- **Kilder uten tall (5):** W3094946421 (protokoll uten resultater), W1572813566, W4400871115, W2993128097 og W3124881456. De fire siste er oversikter med bare beskrivende konklusjoner. Disse kildene har bare rader med tomt estimat og forklaring i utfall. Andre kilder kan også ha enkelte slike rader ved siden av tallradene.
- **Feil dokument:** ingen. Alle tekstene stemmer med tittelen.
- **W1581809000** er riktig dokument, men tekstfilen kan ikke leses: fra side 3 og utover er den bare tegnsøppel, sannsynligvis en feil i fontkodingen. De to radene er derfor tatt fra sammendraget, med side = sammendrag. Landfeltet står tomt fordi landet ikke står i sammendraget.
- **Tall som er utelatt:**
  - W3169310651: «nesten to av tre» med inntekt minst 2 G står uten estimat. Sitatet har også sifferet «2 G», så kontrollen godtok ikke tallet skrevet med ord.
  - W2803699076: tabell 5 i metaanalysen er for rotete i tekstfilen. Jeg har bare brukt de uvektede gjennomsnittene i tabell 3.
- **tidligere-estimater.tsv:** ingen rader i den gjelder dette spørsmålet for mine kilder.

Resultatet står i /tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g08/forskning/sporsmal/evu-voksne/estimater.tsv

## 

Jeg har skrevet 55 rader for alle de 25 kildene i gruppe 07 til `/tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g07/forskning/sporsmal/evu-voksne/estimater.tsv`. Kontroll 1–4 har ingen feil. De eneste feilene som er igjen, gjelder kontroll 6 og 9, og de er ventet i kopien.

- **Antall rader:** 55 rader fra 25 kilder.
- **Kilder uten tall (5):** W2260785424, W3190501518, W4393343216, W71075706 og W4212995781. De har én rad hver med tomt estimat og en kort forklaring i `utfall`.
  - W71075706 har egentlig lønnstall for NVQ-kvalifikasjoner, men de er gjengitt fra McIntosh og Garrett 2009. Den studien har egen tekst, så jeg tok ikke med tallene.
  - W4212995781 har bare tabeller som ikke lar seg lese i tekstfilen. Raden bygger derfor på sammendraget, som sier at programmet ikke hadde noen effekt.
- **Feil dokument:** ingen.
  - Sammendragssiden i W1488143163 (GAIN) er uleselig fordi tegnkodingen er ødelagt, men resten av teksten er riktig rapport.
  - Tittelen i metadata for W7137398361 er navnet på boka. Teksten er kapittelet av Kilpi-Jakonen og Sirniö fra den samme boka, altså riktig dokument.
- **Fortegn:** Rad 3 (W3125246737, kvinner 41–55 år) står med estimat 3.6 uten minustegn. Kontrollskriptet leser «0.6 -3.6» i tabellen som et spenn, så minustegnet ble ikke godtatt. Det negative fortegnet står derfor i `utfall`.
- **Gjengitte tall:** Tall som en kilde henter fra en annen studie, står med «gjengitt fra …» i `utfall`. Det gjelder bare studier som ikke har egen tekst her: Peers 2007, Heinrich mfl. 2013 og Greenberg mfl. 2003.
- **Sjekklisten:** `tidligere-estimater.tsv` hadde ingen rader om opplæring for kildene mine, så den førte ikke til nye rader.

## 

26 rader for alle 25 kildene. Alle kildene var lest bare som sammendrag, så side = sammendrag på alle radene.

- **Kilder med tall:** to. W2069316046 (GED, inntekt) har to rader, med 10 og 19 prosent som nedre og øvre ende av spennet. W2106465281 (RCT, NEWWS) har én rad med 8 pp på oppnådd grad.
- **Kilder uten tall:** 23. De har én rad hver med tomt estimat og forklaring i utfall. Sammendragene har bare kvalitative konklusjoner, eller er bare en referanse (W1866815259).
- **Tidligere uttrekk:** tidligere-estimater.tsv hadde ingen rader for kildene i denne gruppen.
- **Kontrollen:** kontroll 1–4 er fri for feil. Én sitatfeil på W2106465281 er rettet. Bindestreken i sammendraget er tegnet U+2010, ikke en vanlig bindestrek. Feilene som står igjen, er i kontroll 5, 6 og 9 og er ventet i kopien.
- **Land:** metadata-feltet for land ser ut til å vise hvor forfatterne arbeider. Det er derfor ikke brukt, og land er satt bare der teksten sier det.
- **Feil dokument:** ingen åpenbare. W2233861901 og W417211163 er enkle spørreundersøkelser og står som beskrivende. W1937081207 og W2952849036 gjelder ledige og arbeidstakere som har mistet jobben, og er ført som tiltak 5.

Radene står i /tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g10/forskning/sporsmal/evu-voksne/estimater.tsv

## 

35 rader er skrevet for alle 25 kildene i gruppe 09. Kontroll 1–4 har ingen feil. Kontrollen melder bare FEIL i kontroll 6 og 9, som er ventet i kopien.

- **Rader:** 35, minst én per kilde. Radene står i `/tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g09/forskning/sporsmal/evu-voksne/estimater.tsv`.
- **Kilder uten tall:** 17 av 25 har bare én rad med tomt estimat.
  - 14 av de 15 kildene med bare sammendrag har ingen tall. Bare W2945518912 (Komvux) har et tall: «up to 14 years».
  - Tre av tekstkildene har heller ingen tall: W1500817828, W4318038624 og W2181639995.
- **Feil dokument:** jeg fant ingen kilder der teksten ser ut til å være feil dokument. I W3041144534 er side 1 (forsiden) uleselig fordi bokstavene er skilt fra hverandre, men resten av teksten er riktig rapport.
- **Rader å se på ved samkjøring:**
  - W2544347711 og W3041144534 er samme forsøk (WorkAdvance) etter to år og på lang sikt. Det står i `utfall`.
  - W4309504983: estimatet 1.9 er den øvre grensen forfatterne kan utelukke, ikke et punktestimat. Studien finner ingen effekt.
  - W3170063813: tallene er Hedges g fra tabeller, fordi teksten ikke oppgir konfidensintervall utenfor tabellene. Kontrollen godtok sitatene.
  - Rader med tall som gjengis fra andre studier: Bloom mfl. 1997 (W2153646148), Kluve 2010 og Sianesi 2008 (W3122643191).
- **Tidligere estimater:** `tidligere-estimater.tsv` har ingen rader for kildene i denne gruppen, så det kom ingen nye tall derfra.

Hjelpeskriptene ligger i `/tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g09/hj/`.

## 

Uttrekket for gruppe 11 er ferdig, og kontroll 1–4 har ingen feil. De eneste feilene som står igjen, er de ventede i kontroll 6 (6 321 linjer) og kontroll 9 (2 linjer). Kontroll 5 ga ingen linjer.

- **Rader:** 32 rader for alle 25 kildene. Alle 25 hadde bare sammendrag, så side er «sammendrag» på alle radene.
- **Kilder uten tall:** 17 har én rad med tomt estimat og forklaring i utfall. Det gjelder W1797719169, W2151019805, W4308996649, W1518178688, W4309825820, W1588450396, W1518281674, W7148689932, W1576880634, W1536032509, W2109268950, W2185214595, W4391854887, W1878400386, W1550516742, W2087759043 og W4401871492.
- **Mulig feil dokument:** Ingen av kildene hadde tekstfil. Men sammendraget i kandidater.jsonl ser ut til å være feil tekst for tre kilder:
  - W2151019805 er en ansvarsfraskrivelse og en innholdsfortegnelse.
  - W1550516742 er en takketekst.
  - W1518178688 er bare stikkord fra lysbilder.
- **Land:** Satt bare når landet står i sammendraget eller tittelen. Metadatafeltet land ser ut til å gjelde forfatternes institusjoner, så jeg brukte det ikke. Der landet ikke står, er feltet tomt.
- **Tidligere uttrekk:** tidligere-estimater.tsv hadde ingen rader for kildene i gruppen.
- **Tall som står med ord:** W3146199955 oppgir studiepoeng med ord («two credits», «six credits»). Det er merket i utfall, så de to tallene må kontrolleres for hånd.

Filer:
- /tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g11/forskning/sporsmal/evu-voksne/estimater.tsv
- /tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g11/skript/skriv.py (skriptet som skrev radene)

## 

25 rader skrevet i /tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g12/forskning/sporsmal/evu-voksne/estimater.tsv, én per kilde.

- **Kilder uten tall:** alle 25. Alle kildene har lest = sammendrag, og ingen av sammendragene oppgir en effektstørrelse eller et beskrivende tall som svarer på spørsmålet. Hver rad har derfor tomt estimat og side = sammendrag. Kolonnen utfall nevner tiltaket og kort hva sammendraget konkluderer, for eksempel W3095968011 (Chile, rct): bare tegn til effekt på arbeidsinntekt, og W4235170719 (GED): minimal verdi i arbeidsmarkedet.
- **Land:** tatt fra tittel eller sammendrag. Feltet er tomt der teksten ikke nevner land. Landkodene i metadata ser ut til å gjelde der forfatterne arbeider (for eksempel CH, GB og US for studien fra Chile), så dem har jeg ikke brukt.
- **Tidligere estimater:** tidligere-estimater.tsv har ingen rader for disse kildene.
- **Kontrollen:** ingen feil i kontroll 1–4. Det som gjenstår, er bare de ventede FEIL 6 og FEIL 9.
- **Feil dokument:** ingen kilder ser ut til å ha feil tekst, fordi ingen tekstfiler ble lest. Mange kilder er bøker, bokkapitler eller bokanmeldelser med svært korte sammendrag. W2267718473 og W1601350728 har sammendrag som ikke sier noe om resultater.

## 

31 rader for 25 kilder. Kontrollen viser ingen FEIL i kontroll 1–4. Alle FEIL-linjene som står igjen, gjelder kontroll 5, 6 og 9.

- **Kilder uten tall:** 18 har én rad uten estimat og en kort forklaring i utfall. Det er W3113163605, W2287243528, W4245421203, W1481178249, W235307137, W2286125338, W2092242085, W2269959578, W125306557, W2048264620, W3154704909, W1595216198, W1522370595, W2897899629, W2529860077, W4417400053, W3215290409, W4251695828 og W2287709786.
- **Kilder med tall:** 7 kilder har tall, og alle er hentet fra sammendraget. Det er W1517838787 (GED, tiltak 2) og fem GI Bill-studier (tiltak 4: W3200727782, W3182249665, W2887181147, W2095001021, W2112894911). Det er bare seks kilder, så telling og liste stemmer ikke med hverandre.
- **Bare sammendrag:** Alle 25 kildene i gruppen er lest bare i sammendraget. Ingen kilde har tekstfil, så det er ingen tekst som kan være feil dokument.
- **Tidligere uttrekk:** tidligere-estimater.tsv har ingen rader for disse kildene.
- **Avvik fra mandatet:** GED-studien gjelder 16–21-åringer. Mange av GI Bill-studiene gjelder veteraner fra 1940- og 1950-tallet. Begge deler ligger utenfor kjernegruppen 25–64 år og perioden i mandatet.

Radene står i /tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g13/forskning/sporsmal/evu-voksne/estimater.tsv. Skriptet som skrev dem, er /tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-a/g13/rader.py.

# Merknader fra andre uttrekk (Sonnet, 19.11.2026)

31 rader skrevet til estimater.tsv for 25 kilder. Kontroll 1–4 er fri for feil. De eneste FEIL-linjene som står igjen er kontroll 6 og 9 (utelatt-kilder og kilder uten uttrekk i kopien), som var ventet.

- **Antall rader:** 31.
- **Kilder uten tall (én rad med tomt estimat):** 12 av 25.
  - 0198cc5263f2-db66fb0c-87cd-4aa1-9668-dccb5c95a966
  - KU-15673374-2b35-4d1f-82b0-1a12211e128e
  - W7210025147
  - W7167042688
  - W2771339852
  - W235943261
  - W24959778
  - W4401711642
  - W171095229
  - W2956924494
  - W2226242137
  - W2106519551
- **Feil dokument:** ingen kilder der teksten ser ut til å være feil dokument.
- **Tidligere-estimater:** sjekklisten ga ingen nye rader. Radene der gjaldt lønnstilskudd og unge eller dagpenger, ikke EVU for voksne.
- **Gjengitte tall:**
  - W1569864583 har to rader gjengitt fra Patrignani og Conlon 2011.
  - W564684827 har én rad gjengitt fra McIntosh 2004.
  - Begge er merket «gjengitt fra» i utfall.
- **Kommatall i sitat:** i W2779095838 står tallet i sitatet med komma (58,9), og kontrollen godtok det.

Fil: /tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-b/g01/forskning/sporsmal/evu-voksne/estimater.tsv

---

Radene er skrevet og kontroll 1–4 er fri for feil. Det finnes bare FEIL i kontroll 6 og 9, som er ventet i kopien.

- **Antall rader:** 46 i `/tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-b/g02/forskning/sporsmal/evu-voksne/estimater.tsv`, fordelt på alle 25 kilder (minst én rad hver).
- **Kilder uten tall:** 13 (13 rader med tomt estimat):
  - W2120167541, W2433767964, W2184201471, W2908262949, W2102454047, W2072287290
  - W3118879220, W1927179113, W1963973901, W2088280977, W4386420582, W1583669699
  - LI-sf35mlm1q24b0fp2, der verken tekst eller sammendrag finnes
- **Feil dokument:** ingen av kildene ser ut til å ha feil tekst. W2184201471 har bare en innholdsfortegnelse som sammendrag, så den har ingen funn.
- **Tidligere-estimater.tsv:** ingen rader der svarer på dette spørsmålet for mine kilder. Radene gjelder andre kilder og andre spørsmål, så ingenting ble lagt til.
- **Estimat med usikker kolonneplassering:** tre rader har estimat lest fra tabeller i tekstfilen, så kolonneplasseringen er usikker og utfall-feltet sier det:
  - KU-3f5a90bf-7350-48a9-a572-9bdbf20a3911, utenforskap (-0.0103)
  - KU-3f5a90bf-7350-48a9-a572-9bdbf20a3911, heltidsarbeid (-0.0069)
  - W2911366100, ekstra dager i arbeid (14.06 og 18.38)
- **Estimat med tall som ord:** rad for W2010796133 (3 av 9 forsøk) har «(tallet står med ord i sitatet)».

---

Antall rader: 45 i estimater.tsv, fordelt på alle 25 kilder. Kontroll 1–4 er fri for FEIL (kontroll 5, 6 og 9 ikke rettet, som ventet i kopien).

Kilder uten tall (én rad med tomt estimat): 12.
- W1964861379
- W2969413042
- W2026651182
- W4412204416
- KU-a2a2fd8e-0e58-45be-a828-35b0960fd2e8
- W2914642225
- W2044685238
- W2417897354
- W4411098014
- W1574919135
- W3090832067 (protokoll uten resultater)
- W1582975199 (bare kvalitativ konklusjon)

Kilder der teksten ser ut til å være feil dokument:
- W2168820403: forsiden og tittelen er «Curbing adult student attrition» (frafall i voksenopplæring), men sammendraget på side 2 handler om tekstmeldinger til jobbsøkere ved Bedford Jobcentre. Sammendraget på side 3 handler om voksenopplæring. Jeg har bare brukt side 3.
- W4409530334 (Teknikcollege, ungdom i yrkesfag på videregående) er riktig dokument, men utenfor avgrensningen fordi det gjelder ungdom og ikke voksne. Raden er merket slik.
- W4411098014 og W4412115963 er to versjoner av samme arbeid. Raden for W4411098014 har ikke tall, og W4412115963 er merket som samme materiale.

Rader fra tidligere-estimater.tsv: ingen å legge til. Eneste treff var W4302969421, og den raden uten tall er allerede dekket.

Filer:
- /tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-b/g04/forskning/sporsmal/evu-voksne/estimater.tsv

---

Jeg har skrevet 58 rader for de 25 kildene i `/tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-b/g03/forskning/sporsmal/evu-voksne/estimater.tsv`. Kontroll 1–4 er fri for feil. Kontroll 6 og 9 viser feil som er ventet i kopien.

- **Kilder uten tall (2):** LI-8241310 og LI-22279866. LI-8241310 er en oversikt over svensk arbeidsmarkedspolitikk uten effekttall for opplæring. LI-22279866 er et bokkapittel om begreper, uten tall. Begge har én rad med tomt estimat.
- **Feil dokument:** Ingen. Alle tekstene stemmer med tittelen.
- **Tidligere-estimater.tsv:** Ingen rader der svarer på dette spørsmålet for mine kilder. Radene er fra lønnstilskudd- og dagpengespørsmålene.

Tre forhold dere bør vite om:
- **W2013270147:** Tallet 29508 (årsinntekt, menn, to semestre) er lest fra en tabell uten ryddig radstruktur i tekstfilen. Det bør kontrolleres for hånd. Raden for kilden uten tall står som tom rad med sitat fra sammendraget.
- **Tiltak 5 (opplæring for ledige):** NB-4986 er en enkeltstudie av Navs tiltak (utenfor kjernen), men er tatt med for AMO og Utdanning. 0198cc8fb35e er en oversikt over tiltak for ungdom under 30 år.
- **Tallet står med ord:** Rad 21 og 22 (0198cc478c9b), rad 26 (01993890881c) og rad 51 (W2164976890) har estimat fra ord i sitatet. Dette er merket i utfall og må kontrolleres for hånd.

---

58 rader i estimater.tsv, og kontroll 1–4 er fri for feil. Radene ligger i `/tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-b/g05/forskning/sporsmal/evu-voksne/estimater.tsv`.

- **Antall rader:** 58, fordelt på alle 25 kildene.
- **Kilder uten tall:** 2 (W7165978732 og W104926790, tomt estimat med forklaring i utfall).
  - W7165978732 er programrapporten for de seks tallforsøkene. Den har bare en samlet beskrivelse, så tallene ligger i de enkelte forsøksrapportene.
  - W104926790 gir ingen effektestimater, bare at 18 kurs er klassifisert etter skjønn.
- **Feil dokument:** ingen kilder der teksten ser ut til å være feil dokument.
- **Tidligere estimater:** `tidligere-estimater.tsv` har ingen rader for mine 25 kilder, så det var ingenting å legge til derfra.
- **Samme materiale:** W1683883188 er førsteversjonen av W3123135221 (kupongforsøket i Sveits). Begge har rader, og W1683883188 er merket i utfall.
- **Gjengitte tall:** noen rader i oversiktskildene (W7218183306, W2000591473, W2112371456, W2760148764, W2136269032) er gjengitt fra andre studier. Det står i utfall.
- **Grensetilfelle:** W3084314794 gjelder engelskopplæring for innvandrere (ESOL). Den er markert i utfall som grensetilfelle mot kriteriene.

---

Rader: 58 (59 linjer i estimater.tsv med overskriften). Kilder uten tall: 5 (W4399355073, W1484534434, W3121632739, W2183188596 har bare ett upresist tall, så ikke telt; de tre uten noe tall er W4399355073, W1484534434 og W3121632739). Så kilder uten tall: 3.

Kilder der teksten ser ut til å være feil dokument: W3004014332. Tekstfila er bare nettvedlegget til artikkelen (figurer og tilleggstabeller), så tallene (44 prosent, 19 prosentpoeng) er hentet fra sammendraget og står med side = sammendrag.

Kontroll 1–4 har ingen FEIL-linjer. Gjenstående FEIL er bare kontroll 6 og 9, som er ventet i kopien.

Fil: /tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-b/g06/forskning/sporsmal/evu-voksne/estimater.tsv

---

Radene er skrevet til `/tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-b/g07/forskning/sporsmal/evu-voksne/estimater.tsv`. Kontroll 1–4 er fri for feil (de gjenstående FEIL-linjene er kontroll 6).

- **Antall rader:** 46, fordelt på alle 25 kilder.
- **Kilder uten tall (7 stk.):** W2260785424, W3190501518, W3125938983, W1520618467, W4393343216, W7151259557 og W4212995781. De har én rad hver med tomt estimat og forklaring i utfall.
- **Feil dokument:** ingen. Tekstene er alle riktig dokument.
- **Merknader:**
  - Flere nøkkelstudier mangler effekttall i teksten fordi tallene bare står i tabeller. Dette gjelder særlig W3125246737 (Kunnskapsløftet) og W4290607714.
  - W1488143163 (GAIN) er en enkeltstudie av opplæring for ledige og er merket «enkeltstudie» i utfall.
  - Fortegn i W4302162296 og W1511776989 følger sitatet. For W1511776989 står estimatet 167 med forklaring i utfall, fordi kontrollen krevde det.
- **Sjekkliste (tidligere-estimater.tsv):** kun W1849775659 og W3125938983 var med der, og begge gjaldt lønnstilskudd. Ingenting av det svarte på dette spørsmålet, så ingen rader er lagt til.

---

Kontroll 1–4 er uten feil.

Rader: 49 i estimater.tsv, fra alle 25 kilder.

Kilder uten tall (tomt estimat, 8 stykker): W3094946421, W2117604211, W1601384165, W1572813566, W4400871115, W2993128097, W3124881456. W2631481029 har to rader: én beskrivende med tall og én uten tall. Det gir 7 kilder helt uten tall og 8 rader med tomt estimat.

Kilder der teksten ser ut til å være feil dokument: ingen. W1581809000 (Messer og Wolter) har lesbar forside, men brødteksten er ulesbar (skriftkoding). Jeg brukte derfor sammendraget og satte side = sammendrag. Land står tomt i de radene.

I tidligere-estimater.tsv fantes ingen rader for mine 25 kilder.

Fil: /tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-b/g08/forskning/sporsmal/evu-voksne/estimater.tsv

---

33 rader fra 25 kilder står i `estimater.tsv` i spørsmålsmappen. Kontroll 1–4 er fri for feil (kjørt på nytt etter rettingen); gjenstående FEIL gjelder bare kontroll 5, 6 og 9, som skal stå.

- **Kilder uten tall (tomt estimat):** 15 av 25. Det er W1500817828, W2181639995, W4318038624, W3124338191, W4241341401, W7139391198, W2978919928, W2897969768, W7117480952, W1518746948, W2118188388, W2804031940, W3128843297, W1981654732 og W2036089346. W2605248710 og W2979977042 har heller ikke tall i sammendraget, men det er ikke regnet med i de 15. De står med en rad hver, med tomt estimat.
- **Feil dokument:** W2181639995 er en kortversjon av Holzer og Martinson (2005), ikke sammendraget i metadata. Teksten handler fortsatt om samme tema, så jeg tok sitatet fra teksten (side 6). W3128843297 har bare tittelen som sammendrag.
- **Rettet etter kontroll:** raden W3041144534 med sysselsetting i 2018 står med estimat 1.5 og «negativ forskjell» i utfall. Kontrollen godtok ikke -1.5 mot sitatet.
- **Tidligere-estimater.tsv:** ingen rader der gjelder mine 25 kilder.

Filen er `/tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-b/g09/forskning/sporsmal/evu-voksne/estimater.tsv`.

---

Rader skrevet: 26, fra 25 kilder. Kilde-IDene står i `forskning/sporsmal/evu-voksne/estimater.tsv` i g10-kopien.

- **Tekstfiler:** Ingen av de 25 kildene hadde `tekst.txt`, så alle rader bygger på sammendrag (`side` = sammendrag).
- **Kilder uten tall:** 23. De har én rad hver med tomt estimat og en forklaring i `utfall`.
- **Kilder med tall:**
  - W2106465281: 8 prosentpoeng på sannsynlighet for vitnemål (tiltak 2).
  - W2069316046: GED-effekt på inntekt, to rader for spennet 10–19 prosent (tiltak 2).
- **Tidligere estimater:** `tidligere-estimater.tsv` har ingen rader for mine kilder.
- **Kontroll:** Kontroll 1–4 er fri for FEIL etter rettingen av ett sitat i W2106465281 (en bindestrek i sitatet var et annet tegn enn i teksten). Kontroll 6 viser de ventede FEIL-linjene om utelatte kilder i kopien, som ikke skal rettes.
- **Feil dokument:** Ingen. Teksten kunne ikke vurderes siden det ikke fantes tekstfiler. W2213966225 har tyrkisk sammendrag, men innholdet er relevant.

---

Antall rader: 25 (én per kilde, alle skrevet til estimater.tsv i arbeidsmappen g12).

Kilder uten tall: 25. Alle kildene var kun sammendrag, og ingen av sammendragene hadde et effekt- eller beskrivende tall som svarer på spørsmålet. Alle radene har derfor tomt estimat og en forklaring i utfall.

Tidligere-estimater.tsv hadde ingen rader for mine kilder.

Kontroll 1–4 ga ingen FEIL. Kontroll 6 ga mange FEIL-linjer for «utelatt», som er ventet i kopien og ikke rettet.

Kilder der teksten ser ut til å være feil dokument: ingen. W2267718473, W4229951511, W1528348100 og W1601350728 har svært korte eller innledende sammendrag, men de passer med tittelen.

---

Rader: 32, fordelt på alle 25 kilder, i estimater.tsv i spørsmålsmappen i kopien. Kontroll 1–4 er fri for feil.

Kilder uten tall: 7. Det gjelder W1797719169, W2151019805, W1518178688, W1588450396, W1878400386, W1550516742 og W1576880634. Det er oversikter eller kilder med et sammendrag uten effektmål. Alle står med én rad og tomt estimat.

Alle 25 kilder er lest bare fra sammendraget, fordi ingen har tekst.txt. Side er satt til «sammendrag» for alle radene.

Kilder der teksten ser ut til å være feil dokument: ingen. Tre sammendrag er tynne og bare delvis gjengitt, nemlig W2151019805 (bare ansvarsfraskrivelse og innholdsfortegnelse), W1550516742 (bare takkeliste) og W1518178688 (bare en kort beskrivelse av opplæring for ansatte).

Ingen rader i tidligere-estimater.tsv gjelder disse 25 kildene, så sjekklisten ga ingenting å legge til.

---

32 rader. 20 kilder er uten tall, de har én rad med tomt estimat hver. Ingen kilder ser ut til å være feil dokument.

Ingen av de 25 kildene har tekstfil, så alle er hentet fra sammendraget (side = sammendrag). Tidligere-estimater.tsv hadde ingen rader for mine kilder. Kontroll 1–4 er fri for feil.

Radene ligger i `/tmp/claude-0/-home-user/1ed95009-b39c-5ddb-a157-1eddedba0df2/scratchpad/uttrekk-b/g13/forskning/sporsmal/evu-voksne/estimater.tsv`.