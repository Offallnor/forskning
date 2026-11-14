# Egen analyse i microdata.no: dagpengemottakere som bruker opp perioden

**Status: utkast, ikke kjørt.** Laget 10.11.2026 som oppfølging av forskningssvaret om dagpengenes varighet og nivå (`svar.md`). Variabler og kommandoer er sjekket mot kopien av variabelkatalogen og brukerveiledningen for microdata.no, hentet 10.11.2026 (databank versjon 59). Skriptet er ikke prøvd i microdata.no.

**Før skriptet kjøres** skal opplegget avklares med bestilleren, ett spørsmål om gangen (se under). Forslaget under er et utgangspunkt for den samtalen, ikke en bestilling.

## Kunnskapshullet

Forskningssvaret finner at både lengre periode og høyere dagpenger gir noe lengre tid før ledige kommer i arbeid. Det finner også to hull i det norske kunnskapsgrunnlaget:

- Det mangler nyere norske tall for hvor mange som bruker opp perioden, og hva som skjer med dem etterpå. Tallet som finnes, at bare om lag 5 prosent av dagpengeperiodene når utløp, kommer fra en norsk registerstudie (Godøy og Røed). De norske studiene bygger på data fra 1990- og 2000-tallet.
- Det finnes ingen nyere norsk studie av nivået, og ingen norsk studie med effektmål av de midlertidige endringene under pandemien.

Hovedforslaget under fyller det første hullet med beskrivende tall. To sterkere opplegg som kan si noe om virkninger, står til slutt som tilbud.

## Spørsmål til sparringen

Spør bare om det som ikke er klart, og ett spørsmål om gangen:

1. **Bruk.** Hva skal tallene brukes til, og hvem skal lese dem? Er det nok med nivå og fordeling (hvor mange bruker opp perioden, og hvor er de etterpå), eller er spørsmålet hva perioden *gjør*?
2. **Populasjon, utfall og periode.** Forslaget er nye mottakere høsten 2022, uten permitterte, 18–64 år, fulgt til høsten 2025. Skal permitterte, eldre eller en annen årgang med? Er «i jobb» nok, eller trengs også lønn i ny jobb?
3. **Sammenligning.** Forslaget sammenligner dem som bruker opp perioden med dem som gikk av dagpenger tidligere, og ser på alder, kjønn og utdanning. Er andre grupper viktigere, for eksempel bosted eller landbakgrunn?

Oppsummer deretter opplegget med vanlige ord og be bestilleren bekrefte det.

## Hovedforslag: beskrivende oppfølging av en kohort

**Spørsmålet.** Hvor mange av dem som fikk dagpenger høsten 2022, brukte opp perioden, og hvor var de et halvt og ett år etter?

- **Populasjon.** Personer som hadde rettighetsstatus «Dagpenger» ved utgangen av september, oktober eller november 2022, men ikke måneden før. Permitterte holdes utenfor, fordi de har egne regler og ofte går tilbake til samme arbeidsgiver. Alder 18–64 år.
- **Gruppe etter maksimal periode.** Maksimal periode i uker måles i måneden personen startet. Etter folketrygdloven § 4-15 første ledd er full stønadsperiode 104 uker for den som har hatt arbeidsinntekt på minst 2 G siste tolv måneder eller i gjennomsnitt siste 36 måneder, og ellers 52 uker. Hele og graderte dagpenger bruker av perioden på samme måte (Navs rundskriv til § 4-15, R04-00).
- **Brukt opp perioden.** Rettighetsstatusen leses ved hver månedsslutt. Med 104 uker regnes perioden som brukt opp når personen har dagpenger ved minst 23 av 27 månedsslutter fra september 2022 til november 2024. Med 52 uker gjelder minst 11 av 15 månedsslutter fra september 2022 til november 2023. Kravet gir rom for én måneds avbrudd og for at perioden slutter midt i en måned.
- **Utfall et halvt og ett år etter.** Status i mai og november året etter at perioden ville gått ut ved sammenhengende bruk: mai og november 2025 for gruppen med 104 uker, mai og november 2024 for gruppen med 52 uker. Status er én av sju, i denne rekkefølgen: i jobb, dagpenger igjen eller søkt, arbeidsavklaringspenger, annen ytelse fra Nav, sosialhjelp, registrert hos Nav uten ytelse, ingen av delene.
- **Sammenligning.** De som brukte opp perioden, mot de som gikk av dagpenger tidligere, målt på de samme datoene. Og hvem som bruker opp perioden, etter alder, kjønn og utdanning.

**Hvilke sammenhenger analysen ser på.** Analysen beskriver nivå (hvor mange bruker opp perioden), fordeling (hvor de er etterpå) og forskjeller mellom grupper. Den utnytter ingen variasjon som er tilfeldig. Forskjellen mellom dem som bruker opp perioden og dem som gikk av tidligere, er en sammenligning av to grupper som skiller seg fra hverandre fra starten: de som får jobb tidlig, har ofte bedre utsikter i utgangspunktet. Tallene viser derfor ikke hva utløpet av perioden gjør med folk. Regresjonen til slutt i skriptet justerer for alder, kjønn og utdanning, men ikke for det som ikke er målt, som helse, motivasjon og nettverk.

**Hva som må være oppfylt for at tallene gir et riktig bilde.**

- Rettighetsstatusen i arbeidssøkerregisteret må fange opp dem som får dagpenger. Variabelen viser rett til ytelse, ikke utbetaling (se beskrivelsen av `ARBSTATUS_AKT_DAGP` i katalogen), og kodelisten har kategorien «Ingen livsoppholdsytelse i Arena». Sjekk derfor antallet med dagpenger mot Navs publiserte tall for de samme månedene før resten tolkes.
- Statusen leses bare ved månedsslutt. Korte avbrudd og overganger midt i måneden blir borte.
- Den som får dagpenger med lange avbrudd, bruker opp perioden senere enn vinduet fanger opp, og telles som at de ikke brukte den opp. Andelen som bruker opp perioden blir da for lav.
- Oppfølgingsdatoene er faste. For dem som brukte opp perioden, er mai året etter om lag seks til åtte måneder etter utløpet, og november om lag tolv til fjorten måneder etter.

## Variabler

Alle variabelnavn står i `data/microdata/variabler.tsv` i offdocs (kopi hentet 10.11.2026). Periodene er fra kolonnene `fra` og `til`. Datoene for månedlige tverrsnitt er kontrollert mot `temporalStatusDates` i JSON-filene.

| Variabel | Innhold | Enhet | Temporalitet | Periode i katalogen | Bruk |
|---|---|---|---|---|---|
| `ARBEIDSSOKER_AS_YTELSE` | Rettighetsstatus (ytelsesstatus), koder bl.a. `DP` dagpenger, `SD` søkt dagpenger, `AP` arbeidsavklaringspenger, `ID` ingen livsoppholdsytelse i Arena | Person | STATUS, månedsslutt | 2004-01-31 – 2026-09-30 | Start, forbruk og status etterpå |
| `ARBEIDSSOKER_MAXDP` | Maksimale dagpengerettigheter, antall uker | Person | STATUS, månedsslutt | 2018-09-30 – 2026-09-30 | Gruppe (52 eller 104 uker) |
| `ARBEIDSSOKER_ARBEIDSSOKERSTATUS_FIN` | Arbeidssøkerstatus, fingruppe, koder `1` helt ledige permitterte og `4` delvis ledige permitterte | Person | STATUS, månedsslutt | 2002-10-31 – 2026-09-30 | Ta ut permitterte |
| `ARBLONN_PERS_SUM_STILLINGSPST` | Samlet avtalt stillingsprosent i alle arbeidsforhold (a-ordningen) | Person | STATUS, den 16. i måneden | 2015-01-16 – 2026-08-16 | I jobb (over 0) |
| `SOSHJELP_BIDRAG` | Mottatt sosialhjelpsbidrag i statistikkmåneden | Person | ACCUMULATED, per måned | 2015-01-01 – 2025-12-31 | Sosialhjelp (over 0) |
| `BEFOLKNING_FOEDSELS_AAR_MND` | Fødselsår og måned | Person | FIXED | | Alder |
| `BEFOLKNING_KJOENN` | Kjønn | Person | FIXED | | Kjønn |
| `NUDB_BU` | Høyeste fullførte utdanning (NUS-kode, første siffer er nivå) | Person | EVENT | 1970-11-01 – 2024-08-01 | Utdanningsnivå |

Bare for tilbudet om regresjonsdiskontinuitet:

| Variabel | Innhold | Enhet | Temporalitet | Periode i katalogen |
|---|---|---|---|---|
| `ARBLONN_LONN_KONTANT_IMP` | Kontantlønn etter imputering, per arbeidsforhold og måned | Jobb | ACCUMULATED | 2015-01-01 – 2026-08-31 |
| `ARBEIDSFORHOLD_PERSON` | Personen arbeidsforholdet tilhører, brukes til å summere fra jobb til person | Jobb | FIXED | |

Kodelisten for `ARBEIDSSOKER_AS_YTELSE` har bare én periode i katalogen. Kodelisten for `ARBEIDSSOKER_ARBEIDSSOKERSTATUS_FIN` har vært uendret siden 1. januar 2018. Det gir ingen kjent brudd i perioden analysen bruker.

**Variabler som ikke er med.** Uføretrygd (`UFOERP2011FDT_MOTTAK`) og arbeidsavklaringspenger som eget forløp (`ARBAVKLARPFDT_MOTTAK`) går bare til desember 2024 i katalogen, og dekker ikke oppfølgingen i 2025. Arbeidsavklaringspenger fanges i stedet opp gjennom rettighetsstatus `AP` så lenge personen følges opp av Nav. Uføretrygdede, utvandrede og døde havner i «ingen av delene». Dagpengegrunnlaget og antall gjenstående uker finnes ikke i katalogen. Grunnbeløpet (G) finnes heller ikke og må legges inn for hånd i tilbudet om regresjonsdiskontinuitet.

## Konfidensialitet

Fra brukerveiledningen for microdata.no, siden om konfidensialitet (<https://microdata.no/manual/konfidensialitet/>):

- Populasjonen må ha minst 1 000 personer. Kohorten av nye mottakere over tre måneder bør være godt over det, men gruppen som bruker opp perioden kan bli liten. Skriptet beholder derfor hele kohorten og viser gruppen med `if` i tabellene, i stedet for å lage et eget datasett for den.
- Alle opptellinger får tilfeldig støy, og verdiene 1–4 vises aldri. En tabell stoppes når mer enn halvparten av cellene har under 5. Derfor er statusen slått sammen til sju kategorier og alder til fire grupper.
- `generate`, `replace` og `recode` stoppes hvis de endrer færre enn 10 enheter. Små kategorier i rettighetsstatus er derfor slått sammen før de brukes.
- Numeriske variabler winsoriseres med 1 prosent i hver ende i beskrivende tall, ikke i regresjoner.
- Tallene kan avvike litt fra Navs offisielle statistikk.

## Forbehold

- **Ikke effekt.** Hovedforslaget beskriver. En enkel sammenligning viser ikke effekt.
- **Rettighet, ikke utbetaling.** Rettighetsstatusen i arbeidssøkerregisteret er ikke det samme som utbetalte dagpenger. Ventetid, sanksjoner og ferie kan gi avvik.
- **Grov tidsmåling.** Forbruket telles i månedsslutter, ikke i uker. Definisjonen av «brukt opp» er en tilnærming og bør prøves med andre grenser (for eksempel minst 22 eller 24 av 27).
- **I jobb** betyr stillingsprosent over 0 i a-ordningen den 16. i måneden. Selvstendig næringsdrivende og jobber i utlandet kommer ikke med.
- **Perioden.** Kohorten starter etter de midlertidige reglene under pandemien. Lovendringen i § 4-15 som trådte i kraft 1. januar 2025 (lov 20. desember 2024 nr. 81, ifølge endringshistorikken), er ikke vurdert. Den kan berøre nye perioder i oppfølgingen, men ikke definisjonen av kohorten.
- **Ytelsesnivået** er ikke med. Katalogen har ikke dagpengegrunnlaget per måned, bare dagpenger utbetalt per kalenderår (`INNTEKT_ARBLED`, til 2024).

## Tilbud: sterkere opplegg

Hvis bestilleren vil vite hva lengre periode *gjør*, og ikke bare hvor mange som bruker den opp, kan to opplegg vurderes. Si kort hva de krever, og press ikke. Velger bestilleren det beskrivende, går vi videre med det.

### A. Regresjonsdiskontinuitet ved inntektsgrensen på 2 G

- **Variasjonen.** Etter folketrygdloven § 4-15 første ledd får den som har hatt arbeidsinntekt på minst 2 G siste tolv måneder (eller i gjennomsnitt siste 36 måneder), 104 uker, mens den som har litt mindre, får 52. Ledige like over og like under grensen ligner hverandre, men får ulik periode. Forskjellen i utfall ved grensen kan da tolkes som virkningen av lengre periode. Nivået på dagpengene har ikke noe hopp ved 2 G, så grensen skiller periode fra nivå.
- **Hvorfor «fuzzy».** Inntekten Nav legger til grunn, kan bare gjenskapes omtrent fra a-ordningen (kontantlønn per måned). Næringsinntekt og ytelser som likestilles med arbeidsinntekt (folketrygdloven § 4-4 andre ledd) mangler, og 36-månedersregelen gir 104 uker også til noen under grensen. Den faktiske perioden finnes i `ARBEIDSSOKER_MAXDP`, så analysen kan bruke den som behandling i en fuzzy RDD (`rdd ..., fuzzy()`, brukerveiledningen for microdata.no, kapittel 5.12, <https://microdata.no/manual/brukermanual/Avansert%20analyse/5.12%20Regression%20Discontinuity%20Design%20-%20RDD/>).
- **Hva som må være oppfylt.**
  - Andelen med 104 uker må hoppe tydelig ved grensen (kontrolleres med figuren i skriptskissen).
  - Folk må ikke kunne styre inntekten sin rett over grensen. Fordelingen av inntekt bør ikke ha en topp like over 2 G.
  - Ingen andre regler må endre seg ved 2 G. Minsteinntekten på 1,5 G (folketrygdloven § 4-4 første ledd bokstav a) er en annen grense, så vinduet bør holdes mellom 1,5 og 2,5 G.
  - Kjennetegn som alder, kjønn og utdanning bør ikke hoppe ved grensen.
- **For hvem.** Estimatet gjelder bare ledige med arbeidsinntekt rundt 2 G, ofte unge, deltidsansatte og folk med kort arbeidshistorie. Det kan ikke overføres til ledige med høyere inntekt.
- **Krav til data.** Vinduet rundt grensen må ha minst 1 000 personer. Det kan kreve flere startmåneder enn i hovedforslaget, for eksempel hele 2022 og første halvår 2023. Grunnbeløpet må legges inn for hånd for hver startmåned (det endres 1. mai).

### B. De midlertidige endringene under pandemien

- **Variasjonen.** Under pandemien ble dekningsgraden midlertidig hevet til 80 prosent for inntekt opp til 3 G (Heggebø og Pedersen 2023, omtalt i svaret), og det ble gitt særlige regler om dagpenger. Ledige som ville brukt opp perioden mens reglene gjaldt, kan sammenlignes med ledige som brukte den opp før eller etter (forskjeller i forskjeller, brukerveiledningen kapittel 5.11, <https://microdata.no/manual/brukermanual/Avansert%20analyse/5.11%20Diff-in-diff-analyse/>). For nivået kan ledige med inntekt under og over 3 G sammenlignes før og mens den høyere dekningsgraden gjaldt.
- **Hva som må være oppfylt.** Datoene for når hver regel trådte i kraft og opphørte, må hentes fra de midlertidige forskriftene. Navs rundskriv til folketrygdloven § 4-7 (R04-00) sier at særlige regler under covid-19 gjaldt fra 20. mars 2020 til og med 31. mars 2022, og viser til rundskriv R04-00-01 for detaljene, men det rundskrivet er ikke lest. Uten endringene måtte gruppene ha utviklet seg likt. Det er lite trolig under pandemien, fordi arbeidsmarkedet endret seg kraftig samtidig.
- **Begrensninger.** `ARBEIDSSOKER_MAXDP` starter i september 2018, så det finnes bare om lag halvannet år før pandemien. Det er ukjent om variabelen viser forlengede perioder. Sjekk det først. Opplegget er svakere enn A, og bør bare velges hvis spørsmålet er nettopp pandemiendringene.

## Skriptutkast (hovedforslaget)

Skriptet er ikke kjørt. Det bygger på kopien av variabelkatalogen hentet 10.11.2026 (databank versjon 59) og brukerveiledningen for microdata.no hentet samme dag: kommandoene står i <https://microdata.no/manual/kommandoer_og_funksjoner/kommandoer/> og funksjonene i <https://microdata.no/manual/kommandoer_og_funksjoner/funksjoner/>. Løkkene følger eksempelet «Bruke bindinger og løkker» (<https://microdata.no/manual/eksempel/Sammensatte%20operasjoner/Bruke%20bindinger%20og%20l%C3%B8kker/>).

Kjør gjerne til og med steg 2 først, og se at antallet personer er rimelig, før resten kjøres. Får du en feilmelding, lim den inn i samtalen, så retter vi skriptet.

```
textblock
# Dagpengemottakere som bruker opp perioden – hva skjer etterpå?

Utkast, ikke kjørt. Bygger på variabelkatalogen per 10.11.2026 (databank versjon 59).

Skriptet beskriver. Det viser hvor mange som bruker opp dagpengeperioden og hvor de er etterpå,
men ikke hva utløpet av perioden *gjør* med folk. De som bruker opp perioden, skiller seg fra
dem som får jobb tidligere, også på ting som ikke er målt.

Alle antall har litt tilfeldig støy (personvern), så tallene kan avvike litt fra Navs statistikk.
endblock

// Kobler til databanken. Sjekk at versjon 59 er den som tilbys i microdata.no
require no.ssb.fdb:59 as db

textblock
## Steg 1: Finn nye dagpengemottakere høsten 2022

Vi henter rettighetsstatus fra Navs arbeidssøkerregister ved utgangen av august–november 2022.
En ny mottaker har status «Dagpenger» (kode DP) ved utgangen av en måned, men ikke måneden før.

**Sjekk:** Tabellen viser hvor mange som hadde dagpenger ved utgangen av september 2022.
Sammenlign med Navs publiserte tall for samme måned. Er avviket stort, stopp og si fra.
endblock

create-dataset kohort
// Tar med alle som er i registeret i september, oktober eller november (outer_join legger til nye personer)
import db/ARBEIDSSOKER_AS_YTELSE 2022-09-30 as y_2209
import db/ARBEIDSSOKER_AS_YTELSE 2022-10-31 as y_2210, outer_join
import db/ARBEIDSSOKER_AS_YTELSE 2022-11-30 as y_2211, outer_join
// Status måneden før første startmåned (bare for dem som allerede er med)
import db/ARBEIDSSOKER_AS_YTELSE 2022-08-31 as y_2208

// Kontrolltall: antall med hver rettighetsstatus i september 2022
tabulate y_2209

// Startmåned: 1 = september, 2 = oktober, 3 = november. 0 = ikke ny mottaker
generate start = 0
replace start = 1 if y_2209 == 'DP' & y_2208 != 'DP'
replace start = 2 if y_2210 == 'DP' & y_2209 != 'DP' & start == 0
replace start = 3 if y_2211 == 'DP' & y_2210 != 'DP' & start == 0
keep if start > 0

textblock
## Steg 2: Ta ut permitterte og avgrens alder

Permitterte har egne regler og går ofte tilbake til samme arbeidsgiver. De holdes utenfor.
Vi bruker fingruppen i arbeidssøkerregisteret: kode 1 (helt ledige permitterte) og 4 (delvis ledige permitterte),
målt i startmåneden. Vi beholder 18–64-åringer.

Tabellen viser hvor mange nye mottakere som er med, etter startmåned.
endblock

import db/ARBEIDSSOKER_ARBEIDSSOKERSTATUS_FIN 2022-09-30 as fin_2209
import db/ARBEIDSSOKER_ARBEIDSSOKERSTATUS_FIN 2022-10-31 as fin_2210
import db/ARBEIDSSOKER_ARBEIDSSOKERSTATUS_FIN 2022-11-30 as fin_2211
generate permittert = 0
replace permittert = 1 if start == 1 & inlist(fin_2209, '1', '4')
replace permittert = 1 if start == 2 & inlist(fin_2210, '1', '4')
replace permittert = 1 if start == 3 & inlist(fin_2211, '1', '4')
drop if permittert == 1

// Alder i 2022 fra fødselsår og måned (formatet er ÅÅÅÅMM)
import db/BEFOLKNING_FOEDSELS_AAR_MND as fodt
generate alder = 2022 - int(fodt/100)
keep if inrange(alder, 18, 64)

define-labels startlabel 1 'September 2022' 2 'Oktober 2022' 3 'November 2022'
assign-labels start startlabel
tabulate start

textblock
## Steg 3: Maksimal periode, 52 eller 104 uker

Maksimal periode måles i startmåneden. Etter folketrygdloven § 4-15 første ledd er den 104 uker
for den som har hatt arbeidsinntekt på minst 2 G, og ellers 52 uker.

Tabellen viser hvor mange som har hver periode. Gruppen «Annen lengde» bør være liten.
Er den stor, må vi se nærmere på hvilke verdier variabelen har før vi går videre.
endblock

import db/ARBEIDSSOKER_MAXDP 2022-09-30 as maxdp_2209
import db/ARBEIDSSOKER_MAXDP 2022-10-31 as maxdp_2210
import db/ARBEIDSSOKER_MAXDP 2022-11-30 as maxdp_2211
generate maxdp = maxdp_2209 if start == 1
replace maxdp = maxdp_2210 if start == 2
replace maxdp = maxdp_2211 if start == 3
// Viser gjennomsnitt, minste og største verdi
summarize maxdp

generate periode = 0
replace periode = 1 if maxdp == 52
replace periode = 2 if maxdp == 104
define-labels periodelabel 0 'Annen lengde' 1 '52 uker' 2 '104 uker'
assign-labels periode periodelabel
tabulate periode
keep if periode > 0

textblock
## Steg 4: Tell måneder med dagpenger

Vi ser på rettighetsstatus ved hver månedsslutt fra september 2022.
- `dp15` teller månedsslutter med dagpenger fra september 2022 til november 2023 (15 måneder).
- `dp27` teller månedsslutter med dagpenger fra september 2022 til november 2024 (27 måneder).

Løkkene henter én måned om gangen, teller den og sletter den igjen.
endblock

generate dp15 = 0
generate dp27 = 0

// Første 15 månedsslutter: telles i begge tellerne
for i, dato in 1:15, '2022-09-30' '2022-10-31' '2022-11-30' '2022-12-31' '2023-01-31' '2023-02-28' '2023-03-31' '2023-04-30' '2023-05-31' '2023-06-30' '2023-07-31' '2023-08-31' '2023-09-30' '2023-10-31' '2023-11-30'
  import db/ARBEIDSSOKER_AS_YTELSE $dato as y_ ++ $i
  replace dp15 = dp15 + 1 if y_ ++ $i == 'DP'
  replace dp27 = dp27 + 1 if y_ ++ $i == 'DP'
  drop y_ ++ $i
end

// De neste 12 månedsslutter: telles bare i dp27
for i, dato in 16:27, '2023-12-31' '2024-01-31' '2024-02-29' '2024-03-31' '2024-04-30' '2024-05-31' '2024-06-30' '2024-07-31' '2024-08-31' '2024-09-30' '2024-10-31' '2024-11-30'
  import db/ARBEIDSSOKER_AS_YTELSE $dato as y_ ++ $i
  replace dp27 = dp27 + 1 if y_ ++ $i == 'DP'
  drop y_ ++ $i
end

textblock
## Steg 5: Hvor mange bruker opp perioden?

Vi regner perioden som brukt opp når personen har dagpenger ved
- minst 23 av 27 månedsslutter, for dem med 104 uker
- minst 11 av 15 månedsslutter, for dem med 52 uker

Det gir rom for én måneds avbrudd. Den som har lengre avbrudd, kan bruke opp perioden senere
enn vi ser her, så andelen blir heller for lav enn for høy.

**Slik leser du tabellen:** Raden «104 uker» viser hvor mange prosent av dem med 104 uker
som brukte opp perioden (kolonnen «Ja»). Søylene viser det samme.
endblock

generate brukt_opp = 0
replace brukt_opp = 1 if periode == 2 & dp27 >= 23
replace brukt_opp = 1 if periode == 1 & dp15 >= 11
define-labels janei 0 'Nei' 1 'Ja'
assign-labels brukt_opp janei

// Andel som brukte opp perioden, etter maksimal periode
tabulate periode brukt_opp, rowpct
// Gjennomsnittet av en 0/1-variabel er andelen med 1
barchart (mean) brukt_opp, over(periode)

textblock
## Steg 6: Hvor er de et halvt og ett år etter?

Vi henter status på faste datoer:
- for dem med 104 uker: mai og november 2025
- for dem med 52 uker: mai og november 2024

For dem som brukte opp perioden, er mai om lag seks til åtte måneder etter utløpet,
og november om lag tolv til fjorten måneder etter.

Hver person får én status. Står en person i flere, gjelder den øverste i lista:
1. I jobb (stillingsprosent over 0 i a-ordningen)
2. Dagpenger igjen eller søkt dagpenger
3. Arbeidsavklaringspenger
4. Annen ytelse fra Nav (for eksempel tiltakspenger eller sykepenger)
5. Sosialhjelp
6. Registrert hos Nav uten ytelse
7. Ingen av delene (også uføretrygdede, utvandrede og døde)
endblock

// Rettighetsstatus ved månedsslutt
import db/ARBEIDSSOKER_AS_YTELSE 2024-05-31 as y_2405
import db/ARBEIDSSOKER_AS_YTELSE 2024-11-30 as y_2411
import db/ARBEIDSSOKER_AS_YTELSE 2025-05-31 as y_2505
import db/ARBEIDSSOKER_AS_YTELSE 2025-11-30 as y_2511
// Samlet stillingsprosent fra a-ordningen (måles den 16. i måneden)
import db/ARBLONN_PERS_SUM_STILLINGSPST 2024-05-16 as st_2405
import db/ARBLONN_PERS_SUM_STILLINGSPST 2024-11-16 as st_2411
import db/ARBLONN_PERS_SUM_STILLINGSPST 2025-05-16 as st_2505
import db/ARBLONN_PERS_SUM_STILLINGSPST 2025-11-16 as st_2511
// Sosialhjelpsbidrag i måneden
import db/SOSHJELP_BIDRAG 2024-05-31 as sos_2405
import db/SOSHJELP_BIDRAG 2024-11-30 as sos_2411
import db/SOSHJELP_BIDRAG 2025-05-31 as sos_2505
import db/SOSHJELP_BIDRAG 2025-11-30 as sos_2511

// Ikke i registeret = egen kode IR. Ingen stilling eller sosialhjelp = 0
recode y_2405 y_2411 y_2505 y_2511 (missing = 'IR' 'Ikke registrert hos Nav')
replace st_2405 = 0 if sysmiss(st_2405)
replace st_2411 = 0 if sysmiss(st_2411)
replace st_2505 = 0 if sysmiss(st_2505)
replace st_2511 = 0 if sysmiss(st_2511)
replace sos_2405 = 0 if sysmiss(sos_2405)
replace sos_2411 = 0 if sysmiss(sos_2411)
replace sos_2505 = 0 if sysmiss(sos_2505)
replace sos_2511 = 0 if sysmiss(sos_2511)

// Velger riktige datoer for hver gruppe: "6" = mai, "12" = november
generate ytelse6 = y_2505 if periode == 2
replace ytelse6 = y_2405 if periode == 1
generate ytelse12 = y_2511 if periode == 2
replace ytelse12 = y_2411 if periode == 1
generate stilling6 = st_2505 if periode == 2
replace stilling6 = st_2405 if periode == 1
generate stilling12 = st_2511 if periode == 2
replace stilling12 = st_2411 if periode == 1
generate sos6 = sos_2505 if periode == 2
replace sos6 = sos_2405 if periode == 1
generate sos12 = sos_2511 if periode == 2
replace sos12 = sos_2411 if periode == 1

// Status: senere linjer overstyrer tidligere, så «i jobb» settes sist
generate status6 = 7
replace status6 = 6 if ytelse6 == 'ID'
replace status6 = 5 if sos6 > 0 | ytelse6 == 'SO'
replace status6 = 4 if inlist(ytelse6, 'IS', 'SY', 'AT', 'VS', 'SA', 'xx')
replace status6 = 3 if ytelse6 == 'AP'
replace status6 = 2 if inlist(ytelse6, 'DP', 'SD')
replace status6 = 1 if stilling6 > 0

generate status12 = 7
replace status12 = 6 if ytelse12 == 'ID'
replace status12 = 5 if sos12 > 0 | ytelse12 == 'SO'
replace status12 = 4 if inlist(ytelse12, 'IS', 'SY', 'AT', 'VS', 'SA', 'xx')
replace status12 = 3 if ytelse12 == 'AP'
replace status12 = 2 if inlist(ytelse12, 'DP', 'SD')
replace status12 = 1 if stilling12 > 0

define-labels statuslabel 1 'I jobb' 2 'Dagpenger igjen eller søkt' 3 'Arbeidsavklaringspenger' 4 'Annen ytelse fra Nav' 5 'Sosialhjelp' 6 'Registrert uten ytelse' 7 'Ingen av delene'
assign-labels status6 statuslabel
assign-labels status12 statuslabel

// I jobb ja/nei, brukes i regresjonen til slutt
generate jobb6 = stilling6 > 0
generate jobb12 = stilling12 > 0

textblock
### Resultat: status etterpå, 104 uker

**Slik leser du tabellene:** Hver rad summerer til 100 prosent. Raden «Ja» viser hvor de som
brukte opp perioden, er. Raden «Nei» viser de som gikk av dagpenger tidligere, på de samme datoene.
Forskjellen mellom radene er ikke virkningen av utløpet: gruppene var ulike fra starten.
endblock

tabulate brukt_opp status6 if periode == 2, rowpct
tabulate brukt_opp status12 if periode == 2, rowpct
// Stablede søyler: én søyle per gruppe, fordelt på status
barchart (percent) status12 if periode == 2, over(brukt_opp) stack

textblock
### Resultat: status etterpå, 52 uker

Samme tabeller for dem med 52 uker (inntekt under 2 G). Gruppen er mindre,
så tabellene kan bli stoppet hvis for mange celler har under 5 personer.
Da slår vi sammen statusene 4–7.
endblock

tabulate brukt_opp status6 if periode == 1, rowpct
tabulate brukt_opp status12 if periode == 1, rowpct
barchart (percent) status12 if periode == 1, over(brukt_opp) stack

textblock
## Steg 7: Hvem bruker opp perioden?

Vi ser på alder, kjønn og utdanning for dem med 104 uker.
Tabellene viser hvor mange prosent i hver gruppe som brukte opp perioden.
endblock

// Aldersgrupper
generate aldersgr = 1
replace aldersgr = 2 if alder >= 30
replace aldersgr = 3 if alder >= 50
replace aldersgr = 4 if alder >= 60
define-labels alderlabel 1 '18–29 år' 2 '30–49 år' 3 '50–59 år' 4 '60–64 år'
assign-labels aldersgr alderlabel

// Kjønn: kode 2 er kvinne
import db/BEFOLKNING_KJOENN as kjonn
generate kvinne = kjonn == '2'
assign-labels kvinne janei

// Utdanning: første siffer i NUS-koden er nivået
import db/NUDB_BU 2022-09-30 as nus
generate utdniva = substr(nus, 1, 1)
destring utdniva, force
recode utdniva (0/2 = 1 'Grunnskole eller lavere') (3/5 = 2 'Videregående eller fagskole') (6/8 = 3 'Høyere utdanning') (9 = 4 'Uoppgitt') (missing = 4)

tabulate aldersgr brukt_opp if periode == 2, rowpct
tabulate kvinne brukt_opp if periode == 2, rowpct
tabulate utdniva brukt_opp if periode == 2, rowpct
barchart (mean) brukt_opp if periode == 2, over(aldersgr)

textblock
## Steg 8: Regresjoner (lineær sannsynlighetsmodell)

Utfallene er ja/nei. Vi bruker vanlig lineær regresjon med robuste standardfeil.
Da kan hver koeffisient leses direkte som en forskjell i **prosentpoeng**.

**Modell 1:** Hvem bruker opp perioden (104 uker)?
- Koeffisienten for en aldersgruppe er forskjellen i sannsynlighet for å bruke opp perioden
  sammenlignet med 18–29 år, når kjønn og utdanning er like. 0,05 betyr fem prosentpoeng høyere.
- Koeffisienten for `kvinne` er forskjellen mellom kvinner og menn med samme alder og utdanning.

**Modell 2:** Er de som brukte opp perioden, sjeldnere i jobb ett år etter?
- Koeffisienten for `brukt_opp` er forskjellen i prosentpoeng i andelen i jobb i november 2025
  mellom dem som brukte opp perioden og dem som gikk av tidligere, med samme alder, kjønn og utdanning.
- Den er **ikke** virkningen av å bruke opp perioden. Forskjeller som ikke er målt, som helse,
  motivasjon og nettverk, ligger fortsatt i tallet.
endblock

regress brukt_opp i.aldersgr kvinne i.utdniva if periode == 2, robust
regress jobb12 brukt_opp i.aldersgr kvinne i.utdniva if periode == 2, robust
```

## Skisse til skript for tilbud A (bare hvis bestilleren velger det)

Skissen bygger videre på datasettet `kohort` fra hovedskriptet, til og med steg 4. Den trenger trolig flere startmåneder for å få nok personer rundt grensen. Grunnbeløpet må settes inn for hånd der det står `SETT_INN_G`, og skriptet stopper til det er gjort. Inntekten summeres fra jobb til person slik eksempelet «Koble sammen data om arbeidsforhold på persondatasett – numeriske opplysninger» i brukerveiledningen viser (<https://microdata.no/manual/eksempel/Tema%20-%20Jobb-%20og%20inntektsanalyser/Koble%20sammen%20data%20om%20arbeidsforhold%20p%C3%A5%20persondatasett%20-%20numeriske%20opplysninger/>).

```
textblock
# Tilbud A: Gir lengre periode lengre tid på dagpenger? (regresjonsdiskontinuitet ved 2 G)

Vi sammenligner nye mottakere med arbeidsinntekt like under og like over 2 G siste tolv måneder.
Over grensen får de fleste 104 uker, under grensen de fleste 52 uker.
Forskjellen i utfall ved grensen anslår virkningen av lengre periode,
men bare for ledige med inntekt rundt 2 G.
endblock

textblock
## Steg A1: Lønn siste tolv måneder fra a-ordningen

Kontantlønn per arbeidsforhold og måned, september 2021 til august 2022, summert per person.
Det er en tilnærming til inntekten Nav bruker: næringsinntekt og enkelte ytelser mangler.
endblock

create-dataset jobber
import db/ARBLONN_LONN_KONTANT_IMP 2021-09-30 as l_1
for i, dato in 2:12, '2021-10-31' '2021-11-30' '2021-12-31' '2022-01-31' '2022-02-28' '2022-03-31' '2022-04-30' '2022-05-31' '2022-06-30' '2022-07-31' '2022-08-31'
  import db/ARBLONN_LONN_KONTANT_IMP $dato as l_ ++ $i, outer_join
end
// Summerer de tolv månedene for hvert arbeidsforhold
generate lonn12 = rowtotal(l_1, l_2, l_3, l_4, l_5, l_6, l_7, l_8, l_9, l_10, l_11, l_12)
// Summerer fra arbeidsforhold til person og kobler til kohorten
import db/ARBEIDSFORHOLD_PERSON as personid
collapse (sum) lonn12, by(personid)
merge lonn12 into kohort
use kohort
replace lonn12 = 0 if sysmiss(lonn12)

textblock
## Steg A2: Avstand til grensen, målt i G

`avstand` er 0 ved 2 G, negativ under og positiv over. Vi holder oss mellom 1,5 og 2,5 G,
fordi kravet til minsteinntekt (1,5 G) er en annen grense.
endblock

// Sett inn grunnbeløpet (kroner) som gjaldt da mottakerne søkte
generate avstand = lonn12 / SETT_INN_G - 2
keep if inrange(avstand, -0.5, 0.5)
generate maks104 = periode == 2

textblock
## Steg A3: Hopper andelen med 104 uker ved grensen?

Figuren viser andelen med 104 uker i inntektsgrupper på 0,1 G. Andelen bør være lav til venstre
for 0 og høy til høyre. Er hoppet lite, er opplegget svakt, og vi stopper her.
endblock

generate gruppe = floor(avstand * 10)
barchart (mean) maks104, over(gruppe)
// Fordelingen av inntekt rundt grensen: en topp like over 0 kan bety at inntekten er tilpasset
histogram avstand

textblock
## Steg A4: Virkningen av lengre periode

Utfallet er antall månedsslutter med dagpenger fra september 2022 til november 2024 (`dp27`).
Vi bruker fuzzy RDD med faktisk maksimal periode (`maks104`) som behandling.

**Slik leser du resultatet:** Linjen «Conventional» er anslaget. Et anslag på 2 betyr at 104 uker
i stedet for 52 gir om lag to månedsslutter mer med dagpenger for ledige med inntekt rundt 2 G.
«Robust» gir et skjevhetsjustert anslag med robuste standardfeil.
endblock

hexbin dp27 avstand
rdd dp27 avstand, fuzzy(maks104)
```

Utfall som andel i jobb et og to år etter start (`ARBLONN_PERS_SUM_STILLINGSPST` den 16. november 2023 og 2024) kan legges til på samme måte. Kontroller også at alder, kjønn og utdanning ikke hopper ved grensen, ved å kjøre `rdd` med dem som utfall.

## Åpne spørsmål før kjøring

- Om `require no.ssb.fdb:59` er riktig navn og versjon. Katalogen oppgir versjon 59.0.0.0, men eksemplene i brukerveiledningen bruker eldre versjonsnummer.
- Om `ARBEIDSSOKER_MAXDP` bare har verdiene 52 og 104 for nye mottakere i 2022, og om den viser forlengelser under pandemien (viktig for tilbud B).
- Om rettighetsstatus `DP` fortsatt fanger opp alle dagpengemottakere i 2024 og 2025, se sjekken i steg 1.
- Om sammenligningen `y_2208 != 'DP'` gir sant for personer som mangler verdi (ikke var i registeret i august). Gir den ikke det, må manglende verdier omkodes først med `recode ... (missing = 'IR' ...)`, slik steg 6 gjør.
- Om bindinger med `++` virker i `drop` og i `if`-uttrykket inne i løkkene slik eksempelet om bindinger og løkker antyder.
- Om `SOSHJELP_BIDRAG` gir månedsbeløpet når den importeres med en dato i måneden. Brukerveiledningen sier at datoen ikke betyr noe for årlige akkumulerte variabler, men denne er månedlig.
- Om `barchart ..., over(gruppe)` godtar en numerisk gruppevariabel, og om `SETT_INN_G` bør erstattes med én verdi eller ulike verdier per startmåned.
