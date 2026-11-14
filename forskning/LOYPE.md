# Løypa for forskningsspørsmål (pilot)

Oppskrift for å svare på et spisset spørsmål fra forskningen, med kildeutvalg, uttrekk og kontroller. Skrevet 7.11.2026 etter test på gradert sykmelding, og rettet samme dag etter en kaldtest på egenandel ved sykefravær (`sporsmal/egenandel-sykefravaer/kaldtest.md`). I kaldtesten kjørte en ny tråd løypa bare ut fra denne filen.

Løypa gjelder alle temaer på arbeids- og velferdsfeltet og tilgrensende felt. Eksemplene er fra sykefravær fordi de tre første spørsmålene handlet om det. Søkeord, designhierarki og kilder skal velges ut fra spørsmålet.

Hvert steg er merket:

- **[skript]** kjører i GitHub Actions
- **[vurdering]** gjøres av Claude etter skrevne regler
- **[kontroll]** gjøres av en egen kjøring eller et skript og må bestås før neste steg

Hvert spørsmål ligger i `forskning/sporsmal/<mappe>/`. Kildene ligger i et felles bibliotek, `forskning/kilder/<id>/`, som alle spørsmål bruker og bygger videre på (se «Kildebiblioteket» under). Se `gradert-sykmelding/` og `egenandel-sykefravaer/` for ferdige eksempler på hver fil.

## To varianter

- **Full løype** (steg 0–7): nytt søk, kildeutvalg med referanser og blindt utvalg, uttrekk to ganger og innholdskontroll. Med et utvalg på 100–300 studier krever den en til to timer arbeid og 1–2 millioner tokens, men med venting i Actions tar det ofte en hel dag. Aktivitetskravet (november 2026, over 5 000 kandidater) tok om lag et døgn. Store felt koster mye mer: dagpengenes varighet og nivå (10.11.2026, 10 700 kandidater, om lag 880 valgte studier, kjerne på 405 kilder) tok om lag fire timer og om lag 21 millioner tokens i underagentene, av dem 7 millioner på Haiku. Se «Store utvalg» i steg 4.
- **Raskt svar** (se eget avsnitt): bare kilder som allerede ligger i kildebiblioteket. Passer når spørsmålet ligger tett på et tidligere spørsmål. Tar fra noen minutter til en halvtime, etter hvor mange kilder som må leses.

Begge starter med mandatet i steg 0. Brukerne trenger Claude Code og skrivetilgang til dette repoet og det private repoet med fulltekst (se `CLAUDE.md` i roten).

## Kildebiblioteket

Hver kilde har én mappe, `forskning/kilder/<id>/`, uansett hvor mange spørsmål som bruker den:

- `kilde.json`: tittel, forfattere, år, lenke til oppføringen (`lenke`), adressen teksten eller fila ble hentet fra (`hentet_fra`), hvordan den ble hentet, dato og varsler fra tekstkontrollen
- `tekst.txt`: teksten, med sideskift når den kommer fra en PDF
- `fil.pdf`: fila, bare når den er lastet opp for hånd

`tekst.txt` og `fil.pdf` ligger i det private repoet med samme sti, fordi de kan være vernet. Hent dem inn med `forskning/verktoy/fulltekst.sh hent` før kildene leses (se `CLAUDE.md` i roten). Jobbene i Actions gjør det selv.

Brukeren skal kunne lese kilden selv: i svaret lenkes det til oppføringen, og `hentet_fra` eller `fil.pdf` viser hvor teksten kom fra. En kilde som allerede har tekst i biblioteket, hentes ikke på nytt.

Hver kilde har også `funn.tsv` med alle funn som er hentet ut av den, fra alle spørsmål (like funn slått sammen, med spørsmålene som har brukt funnet og datoen da kontrollen sist besto), og `budskap.tsv` med forfatternes budskap. `kilder/funn.tsv` har alle funn i biblioteket i én tabell, så det kan søkes på tvers, for eksempel etter utfall eller gruppe. Funnene føres inn fra spørsmålenes `estimater.tsv` og `budskap.tsv` etter hver runde, så de skal ikke redigeres for hånd.

`kilder/oversikt.tsv` har én linje per kilde, med hvilke spørsmål som har valgt den og hvor mange tall og budskap som er hentet ut. `sporsmal/oversikt.tsv` har én linje per spørsmål. Begge lages på nytt etter hver runde og hver opplasting (`verktoy/kilder_oversikt.py`).

## Slik kjøres skriptene

Mappen `forskning/sporsmal/<mappe>/` (kort navn med bindestrek) har fila `kjor.sh` med kommandoene for neste runde.

Workflowen `sporsmal-sok.yml` kjører `kjor.sh` i de mappene der fila er endret i pushen. Den legger resultatet tilbake på `main` med commit-meldingen «Spørsmålssøk: resultat». OpenAlex, Europe PMC og vitenarkivet nås bare fra Actions, ikke fra skymiljøet (nav.no nås fra begge).

**Starte en runde:** linjer som er ferdige, kommenteres ut, og nye linjer legges inn. En ny kommentarlinje er nok for å kjøre fila på nytt. Kommenter ikke ut en runde som ennå ikke har gitt resultat-commit: den går da tapt. Legg heller de nye linjene under. Push rett til `main`: `git pull --rebase origin main && git push origin main`.

**Vente på en runde:** en runde tar 1–7 minutter, men tekst for over hundre kilder kan ta 40 minutter, og for 900 kilder over en time. Hvert spørsmål har sin egen kø, og opptil tre spørsmål kjører samtidig. Samme spørsmål kjører aldri to runder på en gang, så en ny runde i samme mappe venter til den forrige er ferdig (dagpenger 10.11.2026: én runde ventet 60 minutter på tekstrunden før). Køen beholder bare én ventende kjøring per spørsmål, så en ventende kjøring kan bli avbrutt («cancelled») av en nyere push. Det gjør ikke noe: neste kjøring tar med alle `kjor.sh` som er endret siden de sist ble kjørt ferdig (`kjor.sh.kjort`).

**Tidsgrensen** er 100 minutter per runde. Det som er hentet, går ikke tapt om tiden går ut: tekst lagres per kilde i kildebiblioteket, referanser per kilde i `referanser-hentet.jsonl`, og resultatet legges på `main` selv om steget stopper. En runde som ikke ble ferdig, får ikke ny `kjor.sh.kjort` og fortsetter der den slapp når den startes på nytt (push en ny kommentarlinje i `kjor.sh`). Legg referanser og tekst i hver sin runde når det er mer enn om lag 50 kilder, så hver runde blir kortere og resultatet av den første kommer tidligere. Regelen gjelder rundene, ikke antall kilder per runde: teksten for alle kildene kan hentes i én runde. Vent på en ny commit «Spørsmålssøk: resultat» på `main`, for eksempel med en løkke som henter `main` hvert 15. sekund. Gjør annet arbeid i mellomtiden, for eksempel uttrekk fra tekst som allerede er hentet.

**Når en runde feiler:** finn kjøringen med `actions_list` (workflow `sporsmal-sok.yml`) og jobben med `list_workflow_jobs`. Loggen hentes med `get_job_logs`, med `job_id` og `tail_lines`. Kommer det ingen resultat-commit, er det enten ingen endringer eller en feil.

**Runder i fast rekkefølge.** Hver runde krever en ny kjøring, og vurderingene skjer mellom rundene:

1. Søk: engelsk, norsk og eventuelt svensk og finsk søk i samme `kjor.sh`. Det norske søket og en referanserunde kan også gå i samme kjøring.
2. Referanser, runde 1, etter første utvalg.
3. Referanser, runde 2, etter at utvalget er oppdatert.
4. Tekst og versjoner i samme `kjor.sh`: `--pdf` først og `--versjoner` etterpå. `--versjoner` leter bare etter kilder uten tekst, og vet ikke hvilke det er før `--pdf` har kjørt. I et lite felt kan tekst for kilder som allerede er valgt, gå sammen med referanserunde 1.
5. Tekst for åpne versjoner og for kilder fra det blinde utvalget (`--pdf`).

Nye kilder i en senere runde gir nye versjoner. Gjenta da runde 4 og 5 for dem.

## Underagenter

Store spørsmål krever underagenter for første utvalg, sikting, blinde utvalg og uttrekk.

- **Egen arbeidsmappe:** hver underagent får sin egen mappe, laget med `sporsmal_kopi.py`, `sporsmal_sikting.py --del` eller en egen kopi, og skal skrive hjelpeskript, mellomfiler og resultat bare der. Si det i oppdraget. I dagpenger (10.11.2026) skrev flere i en felles mappe og overskrev hverandres filer.
- **Bare kilden:** si i oppdraget at land, fortegn, forfattere og år bare skal tas fra teksten eller metadata, aldri fra hukommelsen eller forfatternavn (se `verktoy/UTTREKK.md`).
- **Antall:** plattformen kjører om lag 20 underagenter samtidig. Start resten når de første er ferdige.
- **Samle:** kjør `--samle` og slå sammen resultatene først når alle underagentene har levert.
- **Modell:** settes per underagent (se «Modell» i steg 0).

## Gjenoppta en mappe med en eldre runde

Har mappen resultater fra en eldre runde:

1. **Kriterier:** skriv `kriterier.md` nå, og skriv øverst at kriteriene er skrevet etter en eldre runde.
2. **Søk:** det engelske søket trenger ikke gjøres på nytt hvis `kandidater.jsonl` finnes. Det norske søket kjøres alltid.
3. **Utvalg:** gjør hele steg 2, med referanser, blindt utvalg og begrunnelser. Den eldre runden mangler nesten alltid dette.
4. **Uttrekk:** behold eksisterende `estimater.tsv` og hent bare ut tall fra nye kilder. Kilder der den eldre runden bare leste sammendraget, men der det nå finnes tekst, hentes ut på nytt.
5. **Innholdskontroll:** gjøres på nytt etter reglene i steg 6.

Rader i `estimater.tsv` fra kilder som ikke står i `valgt.txt`, betyr at den eldre runden brukte kilden uten å føre den inn. Legg kilden til i `valgt.txt`. Kilder i biblioteket uten `tekst.txt` har bare metadata. De skal ligge, så de kan leses inn fra innboksen senere.

## Steg 0: mandat og kriterier [vurdering]

**Modell.** Løypa er testet med Opus i tråden og Sonnet for det andre blinde utvalget og det andre uttrekket. Vurderingene av utvalg, troverdighet og vekting krever en sterk modell. Sjekk hvilken modell tråden kjører på før mandatet skrives. Er det ikke Opus, si det til bestilleren og be om at modellen byttes før løypa starter, med kort grunn: med en svakere modell blir utvalget og vektingen dårligere. Bytt ikke modell for tråden selv. Velger bestilleren å fortsette, skriv modellen i reproduserbarhetslinjen og ta det med i forbeholdene. Underagentene som skal kjøre på Sonnet, settes med modellvalget for underagenten.

**Start med det som finnes.** Les `sporsmal/oversikt.tsv`. Finnes det et svar på samme eller et nært spørsmål, vis det til bestilleren før noe nytt startes. Et nært spørsmål kan gjenopptas og utvides (se «Gjenoppta en mappe»), eller det nye spørsmålet kan starte med kildene derfra i `valgt.txt`.

**Mandat.** Ingen løype startes før mandatet er godkjent av bestilleren. Utvikle det sammen med bestilleren, ett spørsmål om gangen, og foreslå formuleringer i stedet for å spørre åpent. Mandatet er den første delen av `kriterier.md`, under overskriften **Mandat**:

- **Spørsmålet** med bestillerens ord, og en spisset versjon som kan besvares. «Virker gradert sykmelding?» blir for eksempel «Fører gradert sykmelding til raskere retur til arbeid enn full sykmelding?».
- **Formål:** hva svaret skal brukes til. Det avgjør hvor bredt og hvor dypt løypa går. Svaret beskriver hva forskningen viser, ikke hva noen bør gjøre.
- **Type spørsmål:** effekten av et tiltak, eller nivå og utvikling (se «Beskrivende spørsmål» under).
- **Avgrensninger:** land, periode, grupper og utfall som skal med, og det som ikke skal med. Utelukker en avgrensning en stor del av litteraturen (for eksempel generelle avgiftslettelser når spørsmålet gjelder lønnstilskudd), si det til bestilleren og la bestilleren avgjøre.
- **Kjente kilder:** studier, rapporter eller oversikter bestilleren vet om og venter å se. De legges i `valgt.txt` med kommentaren «fra bestilleren».
- **Statistikk (tilvalg):** om svaret skal ha et avsnitt med beskrivende statistikk, og hvilke tall som er nyttige: hvor mange som omfattes, nivå og utvikling, fordeling på grupper eller sammenligning med andre land. Avtal også to til fire figurer. Foreslå det alltid for beskrivende spørsmål. Se «Tilvalg: statistikk».
- **Variant og frist:** raskt svar eller full løype, og når svaret trengs.
- **Ferdig når:** hva svaret må dekke for at bestilleren er fornøyd.

Sjekk mandatet før det godkjennes: er spørsmålet så bredt at det egentlig er flere spørsmål, foreslå å dele det. Finnes det en ny og god kunnskapsoppsummering som svarer direkte, si det, og foreslå å bruke den. Når bestilleren har godkjent, skriv «Godkjent av bestilleren <dato>» under mandatet. Den gamle overskriften **Bestilling** i eldre mapper betyr det samme.

Resten av fila er kriteriene:

- tiltak og sammenligning
- utfall, med primære utfall først. Skill mellom for eksempel helse eller skader og etterlevelse, og mellom arbeid og ytelser. Samme design kan gi ulike svar på ulike utfall (i det norske tilsynsforsøket bedre etterlevelse, men ingen helseeffekt), så svaret legger vekt på de primære utfallene.
- designhierarki 1–5:
  1. oversikter, vurdert etter designene de bygger på: en oversikt over randomiserte forsøk er kategori 1, en oversikt som mest bygger på observasjonsstudier rangeres som de studiene (kategori 4 eller 5). Skriv i svaret hva oversikten bygger på.
  2. randomiserte forsøk
  3. reformer og naturlige eksperimenter
  4. registerstudier med håndtering av seleksjon
  5. andre registerstudier

  **Kategorien settes av design og troverdighet sammen.** Metodenavnet er et utgangspunkt, ikke svaret. Det avgjørende er hvor troverdig den identifiserende antakelsen er, slik den blinde lesingen vurderer den (`troverdighet` i `budskap.tsv`, se `verktoy/INNHOLDSKONTROLL.md`):
  - Et instrument med svakt første trinn eller et lite troverdig argument for at instrumentet bare virker gjennom tiltaket, flyttes ned til kategori 4.
  - En forskjell-i-forskjell eller panelstudie med faste effekter der variasjonen kommer utenfra (en regelendring, et tidspunkt utfallet ikke styrer) og trendene før tiltaket er testet, er kategori 3. Panel uten slik variasjon er kategori 4.
  - Det er kontrasten som avgjør, ikke at det finnes en lovendring. Sammenligner studien dem som selv valgte ordningen etter en lovendring med dem som ikke gjorde det (matching), er den kategori 4. Eksempel: de finske studiene av lovendringen om delvis sykmelding.
  - Troverdighet «lav» flytter en studie ett trinn ned, «høy» kan løfte en kategori 4 til 3.

  **Oversikter** vurderes både etter designene de bygger på og etter egen kvalitet: systematisk søk, vurdering av risiko for skjevhet og publiseringskanal (Cochrane, Campbell og fagfellevurderte tidsskrift før upubliserte). En oversikt uten systematisk søk brukes som bakgrunn, ikke som belegg.

  **Hvor kilden er funnet, sier ingenting om kvaliteten.** Kudos, Navs bibliotek og vitenarkivet søkes fordi de finner norske studier som ikke er andre steder. I svaret vektes de som alle andre, etter kategori. En studie i kategori 4 eller 5 kan ikke alene flytte hovedkonklusjonen bort fra sterkere studier, men den kan forklare hvorfor norske tall avviker.
- evalueringer av forvaltningen (egen kategori, utenfor hierarkiet): evalueringer av en etat eller ordning som beskriver gjennomføring, organisering eller erfaringer uten effektmål. De er ofte den eneste norske kunnskapen og tas med i et eget avsnitt i svaret, med en overskrift som sier at de ikke måler effekt (for eksempel «Evalueringer av ordningen, uten effektmål»). De brukes aldri som belegg for at et tiltak virker. Bruk `design` = `forvaltning` i `estimater.tsv`.
- land (Norden først)
- regel for flere publikasjoner av samme materiale
- metningsregel (se steg 2)

Kriteriene skrives før utvalget, ikke etter. Unntaket er når en eldre runde gjenopptas.

**Beskrivende spørsmål** («hvordan har sykefraværet utviklet seg», «hvor høyt er det i Norge sammenlignet med Sverige») spør ikke etter effekten av et tiltak. Da passer ikke designhierarkiet over. Bruk i stedet et hierarki etter datadekning:

1. data for hele befolkningen (registre, offisiell statistikk)
2. harmoniserte data på tvers av land
3. lange tidsserier fra utvalg
4. kortere eller mindre utvalg
5. enkeltstudier av en bransje eller gruppe

Skriv i kriteriene hvilke forklaringer (drivere) svaret skal dekke, for eksempel alder, kjønn, bransje, regelverk og konjunktur. Effektstudier av en bestemt ordning hører til sitt eget spørsmål og tas bare med når de forklarer utviklingen.

## Raskt svar fra kildebiblioteket

For spørsmål tett på tidligere spørsmål. Svaret bygger bare på kilder som allerede har tekst i biblioteket, og det søkes ikke etter nye.

**Når raskt svar tilbys** (prøveregel). Alle tre må stemme:

1. **Søket dekket temaet:** hvert tiltak og hvert utfall i det spissede spørsmålet var med i søkeordene i et tidligere spørsmål, både i det engelske og i det norske søket. Har spørsmålet flere tiltak (for eksempel aktivitetskravet og dialogmøtene), vurderes hvert for seg. Det holder ikke at ett ord står i ett av søkene: i testrunden 8.11.2026 sto «aktivitetskravet» i det norske søket, men dialogmøter og tidlig oppfølging var ikke søkt på i noe språk. Søkeordene står i `kjor.sh`, i feltet `sok` i `kandidater.jsonl` eller i `utvalg.md` (det første søket i de eldste mappene står ikke i `kjor.sh`). Typisk en undergruppe, et nytt utfall eller et annet land innenfor samme tiltak.
2. **Nok kilder:** kildebiblioteket har minst fem kilder med fulltekst (`tekst` = «ja» i `kilder/oversikt.tsv`) som passer mandatet, og minst én er en oversikt eller en studie i kategori 1–3. Titlene nevner sjelden en undergruppe. Sorter derfor først med et søk i `tekst.txt` etter ordene for undergruppen (for eksempel «mental», «psykisk»), og les så avsnittene der ordene står.
3. **Ferskt nok:** det tidligere søket er under tolv måneder gammelt (datoen for resultat-commiten i spørsmålets mappe).

Stemmer ett av dem ikke, anbefales full løype med begrunnelse. Er bare noen av tiltakene dekket, foreslå å dele spørsmålet: raskt svar for de dekkede, full løype for resten. Det finnes ingen «delvis oppfylt». Kravene sier ikke om biblioteket mangler studier av et tiltak. Har biblioteket ingen effektstudie av et tiltak i spørsmålet, er det et tegn på at søket ikke har dekket det, og da gjelder det samme. Velger bestilleren likevel raskt svar, skrives avviket i mandatet og i forbeholdene i svaret.

1. **Mandat:** som i steg 0, med «Variant: raskt svar». Skriv også kriteriene, men uten metningsregel.
2. **Utvalg:** velg kilder fra `kilder/oversikt.tsv` og fra `valgt.txt` i de nære spørsmålene, og skriv dem i `valgt.txt`. Kopier `kandidater.jsonl`-radene for kildene fra spørsmålene de kommer fra, så kontrollskriptet finner dem. Linjer i formen `tittel: …` i det nære spørsmålet er ikke slått opp. Ta dem med bare når tittelen finnes i `kilder/oversikt.tsv`, og bruk da id-en derfra.
3. **Uttrekk:** kjør `kilder_oversikt.py <mappe>` og hent ut tall for dette spørsmålet etter `UTTREKK.md`. Gjelder spørsmålet en undergruppe eller et utfall, er det nok å lese avsnittene om den i hver kilde (finn dem med søk i teksten), i tillegg til sammendraget. De tidligere radene brukes bare som sjekkliste etterpå. Ett uttrekk er nok.
4. **Statistikk:** når mandatet ber om det, som i «Tilvalg: statistikk». Raskt svar trenger ingen runde i Actions med mindre SSB-tall skal hentes.
5. **Svar:** skriv `svar.md` som i steg 5. Innledningen skal si at dette er et raskt svar fra kilder som er lest for andre spørsmål, hvilke spørsmål det er, og at det ikke er søkt etter nye kilder. Skriv i forbeholdene hva en full løype ville lagt til, for eksempel nyere studier eller studier av andre utfall. Gjelder spørsmålet en undergruppe, skal forbeholdene alltid si at det tidligere søket ikke var rettet mot den, så studier som bare handler om undergruppen og bruker andre ord, kan mangle.
6. **Kontroller:** de automatiske kontrollene i steg 6 skal bestås. Kontroll 6 sier lite her, fordi `kandidater.jsonl` bare har de valgte kildene. Gå derfor gjennom `valgt.txt` i de nære spørsmålene og `kilder/oversikt.tsv`, og før oversikter og studier i kategori 1–3 om samme tiltak som ikke er tatt med, inn i `utelatt.tsv` med begrunnelse. Kopier `kandidater.jsonl`-radene deres også, så kontroll 6 ser dem. Innholdskontrollen er obligatorisk også her: i testrunden ga raskt svar en feil i beskrivelsen av hvem som fikk tiltaket, som tallkontrollene ikke fanget. Den blinde lesingen gjelder bare kildene som er omtalt i svaret, og kan gjøres av en billigere modell.

Et raskt svar kan senere utvides til full løype i samme mappe (se «Gjenoppta en mappe»).

## Steg 1: søk [skript]

1. **Engelsk søk i OpenAlex:** `sporsmal_sok.py <mappe> '"frase 1" ord' '"frase 2"' ...`. Alle fraser i anførselstegn må stå i tittel eller sammendrag. Bruk mange varianter, fordi studiene bruker ulike ord: gradert sykmelding er også «partial sick leave», «graded return-to-work», «activation» og «sickness certification». Nye treff flettes inn i `kandidater.jsonl`, så et nytt søk i en gjenopptatt mappe sletter ikke noe. Hvert søk lagres med dato og ord i `sok-logg.tsv`, så det kan gjentas nøyaktig. Med `--fra=ÅR` tas bare kilder fra det året og senere med.
   - **Svenske og danske uttrykk:** ta med uttrykkene på svensk og dansk i samme søk, i tillegg til det svenske søket i LIBRIS (punkt 3) (for eksempel «sjukskrivning», «partiell sjukskrivning», «sygedagpenge»). Nordiske rapporter fra universitetsarkivene ligger ofte i OpenAlex med originaltittelen. I gjenfinningstesten mot en ISF-rapport (2016) fant søket ingen av de ti svenske og danske rapportene i fasiten.
   - **Studier uten sammendrag:** om lag en femdel av kandidatene i OpenAlex mangler sammendrag, særlig i økonomitidsskriftene. De treffes bare på tittelen, så bruk også brede uttrykk som kan stå i en tittel («sick leave», «sickness absence», «disability insurance»).
2. **Norsk søk:** `sporsmal_sok.py <mappe> --norsk 'uttrykk 1' 'uttrykk 2' ...`. Søker i Nasjonalt vitenarkiv (rapporter fra FHI, ISF, Frisch, NORCE m.fl. og masteroppgaver) og i katalogen over Navs tidsskrift *Arbeid og velferd* (`katalog/arbeid-og-velferd.jsonl`), og i DFØs Kudos-katalog (`katalog/kudos/`: evalueringer, studier, kartlegginger, kunnskapsoppsummeringer, NOU-er, områdegjennomganger og forhåndsutredninger fra offentlig sektor, ofte de samme rapportene som ligger på regjeringen.no). Kudos-kilder får id `KU-<uuid>`, og teksten hentes fra PDF-en i Kudos. Søket går også i Navs bibliotek (`katalog/navbibliotek.jsonl`: rapporter med lenke, blant annet Navs rapportserie, Fafo og NOVA), med id `NB-<nr>`. Står samme tittel i Kudos, brukes Kudos-posten. Nye kilder legges til i `kandidater.jsonl`, og alle treff listes i `norske-kandidater.tsv`. Treff fra Kudos eller Navs bibliotek der bare ett enkeltord står i sammendraget (ikke i tittelen), merkes «svak» og står sist. De er oftest fra andre sektorer, men les dem likevel raskt: evalueringen av skjermingsordningen kom bare inn slik. Navs årsrapporter tas ikke med.

   Bruk uttrykk som bare kan bety temaet, gjerne med to ord: «gradert sykmelding», «arbeidsgiverperioden», «sykepenger fra første dag». Enkeltord som «egenandel», «dekningsgrad» og «sykelønn» gir mest støy. I kaldtesten ga de 242 treff, de fleste om helsetjenester, bygg og botanikk. Ta med bøyningsformer, for eksempel «gradert sykmelding», «graderte sykmeldinger» og «gradert sykmeldt». Ta også med eldre navn på ordningene når perioden går langt tilbake, for eksempel attføring, rehabiliteringspenger, tidsbegrenset uførestønad og Aetat.

   OpenAlex mangler mye norsk forskning. Gradert sykmelding manglet både FHI-oversikten og ISF-rapporten før det norske søket ble lagt til.

3. **Svensk søk:** `sporsmal_sok.py <mappe> --svensk 'uttrykk 1' 'uttrykk 2' ...`. Søker i LIBRIS (Kungliga biblioteket), som har rapportseriene til IFAU, ISF, Statskontoret og andre svenske myndigheter. Bruk det når svenske erfaringer er relevante for spørsmålet. Bruk svenske uttrykk med to ord eller mer («arbetslösa ungdomar», «partiell sjukskrivning»), fordi LIBRIS også har mye eldre og populærvitenskapelig litteratur. Med `--fra=ÅR` tas bare poster fra det året og senere med (standard 1995). Kildene får id `LI-…`, og treffene listes i `svenske-kandidater.tsv`.
   - LIBRIS har nesten aldri sammendrag. Velg på tittel, utgiver og år, og merk i kommentaren at utvalget bygger på tittelen.
   - Lenkene i LIBRIS er ofte gamle. Teksten hentes da fra IFAUs nettsted eller fra OpenAlex når tittel og år stemmer. Rapporter fra andre utgivere (Statskontoret, ISF) må ofte legges inn med `url:`.
   - I testen mot gjenfinningsfasiten fant søket fire av fem svenske rapporter som de andre søkene bommet på.

4. **Finsk søk:** `sporsmal_sok.py <mappe> --finsk 'uttrykk 1' 'uttrykk 2' ...`. Søker i Finna (det finske nasjonalbibliotekets søk), som har rapportene til Kela, Arbeidshelseinstituttet (TTL), THL, VATT og departementene, og finske doktoravhandlinger. Bruk det når finske erfaringer er relevante. Uttrykkene kan være finske eller svenske («osasairauspäiväraha», «partiell sjukdagpenning», «palkkatuki»). Avisartikler og bacheloroppgaver tas ikke med. Kildene får id `FI-…`, og treffene listes i `finske-kandidater.tsv`.
   - Finna har sjelden sammendrag, men oftest emneord. Velg på tittel, utgiver, type og emneord.
   - Finna søker også i emneordene for hele nasjonalbiblioteket, så sammensatte finske ord gir mye støy (gradert sykmelding: 317 treff, fem valgt). Treff der ingen av søkeordene står i tittelen, merkes «svak» og står sist. Filmer, spill, kart, musikk og tidsskrifter som helhet tas ikke med.
   - De finske arkivene (Julkari, Helda, urn.fi) stenger for automatisk henting, og de gamle lenkene til TTL er døde. Teksten hentes bare når OpenAlex har en åpen versjon. Ellers står kilden i `mangler.md`, og PDF-en må lastes opp for hånd.
   - I testen på delvis sykmelding fant søket Kelas evaluering fra 2009, TTLs rapporter fra 2010 og 2011 (blant dem et randomisert forsøk), en finsk doktoravhandling fra 2013 og en finsk kunnskapsoversikt for 2008–2019. Ingen av dem var funnet av de andre søkene.

5. **Kildebiblioteket:** søk i `kilder/oversikt.tsv` på tittel, så kilder som andre spørsmål allerede har lest, kommer med.

## Steg 2: utvalg [vurdering]

1. **Første utvalg:** velg kilder etter `kriterier.md` og skriv dem i `valgt.txt`, én id per linje med kommentar etter `#`. Les `kandidater.tsv` ovenfra, slik de blinde utvalgene gjør, og les sammendraget for alle med prioritet 2 eller høyere. I aktivitetskravet (november 2026) dukket 111 sterke kilder først opp da de utelatte skulle begrunnes, fordi det første utvalget ikke hadde lest hele lista.
   - Id-ene er OpenAlex (`W…`), vitenarkivet (lang identifikator), *Arbeid og velferd* (`AV-år-nr-løpenr`), Kudos (`KU-…`), Navs bibliotek (`NB-…`), LIBRIS (`LI-…`) eller Finna (`FI-…`).
   - Kopier id-ene fra `kandidater.tsv` eller `norske-kandidater.tsv`, ikke skriv dem av. En feil id står som «finnes ikke» i `pdf-logg.tsv` etter neste runde.
   - En kilde søket ikke fant, kan slås opp med `tittel: <tittel>`.
   - En rapport som ikke finnes i databasene (offentlige utredninger, områdegjennomganger og bestilte evalueringer på regjeringen.no og lignende), legges inn med `url: <adresse> | <tittel> | <forfattere> | <år>`. Adressen kan være PDF-en eller siden som lenker til den. Kilden får id-en `R-…`, som står i loggen etter neste runde. Legg id-en inn i `valgt.txt` på linjen under `url:`-linjen. Ellers kommer kilden ikke med i gruppene til uttrekket, i kopiene, i `mangler.md` eller i vedlegg A (aktivitetskrav 10.11.2026: tre danske rapporter med tekst ble ikke hentet ut). Søk etter slike rapporter på nettet når mandatet gjelder norske tiltak, fordi ingen av databasene dekker dem godt.
   - **Åpne versjoner utenfor databasene.** Hentingen finner bare åpne PDF-er som databasene har registrert. Økonomer legger ofte artiklene på egen hjemmeside eller i arbeidsnotatserier som OpenAlex ikke kjenner til (Card, Kluve og Weber 2010 lå hos Card, lønnstilskudd for unge 11.11.2026). Søk derfor på nettet etter tittelen for kildene i «Ikke lest» i `mangler.md` før lista gis til bestilleren, og skriv adressen i kommentaren på linjen for kilden: `W123  # ... pdf: <adresse>`. Neste runde prøver adressen først, også for kilder som ga «ingen pdf» før, og teksten kontrolleres mot tittelen som ellers. Bruk ikke piratsider eller kopier på ResearchGate. Tråden kan ikke hente slike sider selv, fordi nettet i kjøremiljøet er stengt, men Actions kan.
   - Kommentaren skal bygge på sammendraget, ikke bare tittelen. Titler som «New Deal» eller «praksis» kan handle om noe helt annet.
   - **Kategorien først i kommentaren**, som ett tall 1–5, så land, tiltak og en kort beskrivelse: `W2084090750  # 3, SE, nivå, svenske reformer 2001–2002`. Skriv ikke «3?» eller «4/5». Er du i tvil mellom to, skriv den høyeste og «tvil: 4» i kommentaren. Kjernen i store utvalg lages ut fra tallet (steg 4).
   - **Lange lister** (over om lag 1 500 kandidater): del `kandidater.tsv` i bolker på om lag 500 i prioritert rekkefølge og gi hver bolk til en underagent på Opus (se «Underagenter»). Reglene er de samme: sammendraget leses for prioritet 2 og høyere, tittelen for resten.
   - **Rekkefølge:** `kandidater.tsv` har alle kandidater fra alle søk og referanser, sortert etter `prioritet` (kvalitet først, ingen tak på antall). Poeng gis for oversikt (3), ord som tyder på sterkt design i tittel eller sammendrag (3), søkeord i tittelen (2), Cochrane eller Campbell (2), nordisk (1) og høyt sitert (1), og trekkes for «svak» (−3). Kolonnen `grunn` viser hvorfor. Les ovenfra. Prioriteten avgjør bare rekkefølgen, ikke hva som velges: forfatterrangering brukes ikke, og en kilde med lav prioritet velges når sammendraget oppfyller kriteriene. `--prioriter` skriver lista på nytt uten å søke.
   - **Mange kandidater** (over noen hundre): les `norske-kandidater.tsv` i sin helhet, fordi norske studier ofte har få siteringer og mangler sammendrag.
   - **Flere versjoner av samme studie:** den publiserte versjonen er hoved-id. Åpne versjoner legges til med kommentaren «åpen versjon av <id>», og tallene hentes fra den som har tekst.
   - Flere publikasjoner av samme materiale skrives som «samme materiale som <id>» i kommentaren.
   - **OECD:** OECDs landgjennomganger og rapportserien *Connecting People with Jobs* vurderes særskilt når mandatet gjelder norske ordninger eller sammenligning med andre land. Fransk og engelsk utgave, og bok og kapittel, regnes som samme kilde.
   - **Danmark:** det finnes ingen åpen katalog over danske evalueringer som løypa kan søke i. Når danske studier er viktige for spørsmålet, sjekk jobeffekter.dk (STAR) for hånd, og legg funnene inn med `url:`.
2. **Referanser:** `sporsmal_sok.py <mappe> --referanser 'uttrykk' ...` [skript]. Skriptet følger litteraturlistene bakover og siteringene forover fra de valgte kildene. En referert kilde tas med som kandidat når minst to valgte kilder peker på den, eller når et av uttrykkene står i tittel eller sammendrag.
   - Hver runde lagres som `referanser-<n>.tsv`, og `referanser.tsv` er alltid siste runde. Gjør minst to runder, og fortsett til metningskravet under holder, høyst fire. Skriv antall runder i `metning.md`. IPS-spørsmålet trengte tre.
   - Store utvalg (over om lag 100 kilder) kan bruke opp OpenAlex-kvoten (HTTP 429 i loggen), og runden kan stoppe på tidsgrensen. Det som er hentet, går ikke tapt: hver kilde skrives til `referanser-hentet.jsonl` så snart referansene er hentet, og neste kjøring fortsetter der runden slapp (push en ny kommentarlinje i `kjor.sh` for å starte den). Fila beholdes mellom rundene, så neste runde slår bare opp kildene som er nye i utvalget og holder seg under kvoten. Pekerne fra kildene som er fulgt før, telles fortsatt med, så regelen om to pekere virker som før (10.11.2026). `referanser-fulgt.txt` trengs ikke lenger. Finnes den i en eldre mappe, hoppes kildene der over helt, også pekerne deres.
   - Bare OpenAlex-kilder gir referanser. Litteraturlistene i sentrale norske kilder må leses for hånd.
   - Regelen om to pekere slipper inn metodelitteratur (lærebøker, guider til forskjell-i-forskjell) og studier av andre ordninger (for eksempel lovpålagt sykelønn i USA). Sorter dem bort på tittel.
3. **Blindt utvalg [kontroll], to ganger:** to egne kjøringer velger kilder etter `kriterier.md` uten å se det første utvalget eller hverandre. De skriver `valgt-blind.tsv` og `valgt-blind-b.tsv` med kolonnene id, kategori, land, tiltak, samme_materiale og begrunnelse. I stegtesten i november 2026 overlappet to blinde utvalg på samme filer bare 33 av 53 og 39 kilder, og ett nytt utvalg fikk med 71 prosent av de sterke kildene. Kilder i kategori 1–3 fra én av de to tas inn etter reglene under. Det koster om lag 200 000 tokens ekstra.
   - **Modell:** det første blinde utvalget kjører på Opus (tråden, se «Modell» i steg 0), det andre på Sonnet. Mål treffraten per studie: en annen versjon av samme studie teller som funnet, fordi løypa tar én versjon per studie. Hvert utvalg fikk alene med 84–90 prosent av de sterke studiene i gradert sykmelding. To Opus-utvalg fikk sammen 90 prosent, mens Opus og Sonnet sammen fikk 94–97 prosent. Opus og Fable sammen gjorde det like godt, men Fable koster mer. Sonnet tar med flere kopier og versjoner, så de må sorteres bort mot `valgt.txt`.
   - **Grov sikting først når mappen har mer enn om lag 2 000 kandidater:** `sporsmal_sikting.py <mappe> --del <arbeidsmappe>` deler kandidatene i bolker på 300. Hver bolk siktes av en egen kjøring på Haiku etter `verktoy/SIKTING.md`, og siktingen beholder ved tvil. `--samle` kontrollerer id-ene, skriver `sikting.tsv` og lager mappen `<arbeidsmappe>/blind/` med inndataene filtrert til de beholdte. Begge blinde utvalg får den mappen. I aktivitetskravet (5 718 kandidater) beholdt siktingen 123 av 124 sterke kilder, og Opus-utvalget etter siktingen fant 79 prosent av de sterke kildene, mot 63 prosent uten. Utvalget ble også bredere (240 mot 139 kilder), så sammenligningen med første utvalg tar lengre tid. Under om lag 2 000 kandidater siktes det ikke: i gradert sykmelding (754 kandidater) ga det ingen gevinst. Grensen er et anslag mellom de to testene. Forkastede kandidater er ikke begrunnet for `utelatt.tsv`.
   - **Når siktingen gjøres (10.11.2026):** første gang når kandidatlista passerer om lag 2 000, normalt etter referanserunde 1. Det første utvalget fra søket leser hele lista uten sikting (punkt 1). Siktingen kan brukes når første utvalg leser kandidatene fra referanserundene, og i de blinde utvalgene: forkastede kandidater leses ikke. I dagpenger beholdt siktingen 618 av de 628 kildene i første utvalg, og én av de ti forkastede var en reell effektstudie. Etter hver ny referanserunde siktes bare de nye kandidatene: `--del` hopper over dem som står i `sikting.tsv`, og `--samle` legger de nye beslutningene til de gamle.
   - **Når de blinde utvalgene kjøres:** de to fulle utvalgene kjøres etter siste planlagte referanserunde (normalt runde 2), når første utvalg er oppdatert. Gir de nye sterke kilder, kjøres en referanserunde til fra dem (punkt 4), og da leser ett blindt utvalg på Sonnet bare de nye kandidatene fra den runden.
   - Kjøringen får `kriterier.md`, `kandidater.jsonl`, `kandidater.tsv`, alle `referanser-<n>.tsv` og `norske-kandidater.tsv`.
   - Den får ikke se `valgt.txt`, `utelatt.tsv`, `estimater*.tsv`, `budskap.tsv` eller `svar.md`.

   Sammenlign med første utvalg:
   - Kilder i kategori 1–4 som det blinde utvalget fant, tas inn når de svarer på spørsmålet slik bestillingen avgrenser det. En studie av en annen ordning eller et annet utfall tas ikke inn bare fordi designet er sterkt.
   - Kilder i kategori 5 som bare det blinde utvalget tok med, tas inn bare når det finnes lite i kategori 1–4 for den gruppen eller det landet. Ellers begrunnes de i `utelatt.tsv`.
4. **Metning:** utvalget er mettet når to krav er oppfylt:
   - under 5 prosent av de nye kandidatene i siste referanserunde oppfyller kategori 1–4 (nevneren er de nye kandidatene i den runden, ikke alle kandidater)
   - det blinde utvalget ikke finner nye kilder i kategori 1–3

   Finner det blinde utvalget sterke kilder som manglet, kjøres en referanserunde til fra dem. Det blinde utvalget kjøres så på nytt, men bare på de nye kandidatene fra den runden. Finner det fortsatt nye kilder i kategori 1–3, skriv det i `metning.md` som en svakhet, og ta det med i forbeholdene. Skriv vurderingen i `metning.md`.
5. **Følg oversiktene:** les referanselistene i norske kunnskapsoppsummeringer (FHI og lignende) og sjekk at de norske studiene de omtaler, er med. Mangler de, søk etter tittel i vitenarkivet og i katalogen over *Arbeid og velferd*. Finnes det ingen norsk oversikt, eller har oversikten ikke tekst, skriv det i `utvalg.md`. For beskrivende spørsmål fyller analyser fra Nav og SSB samme rolle som oversiktene.
6. **Begrunn utelatte:** en sentral kandidat er en oversikt, en kilde i øverste tidel av siteringer for faget og året (persentil minst 0,9) eller en kilde med minst 50 siteringer. Hver sentral kandidat som ikke står i `valgt.txt`, skal ha en kort begrunnelse i `utelatt.tsv` (`id`, `begrunnelse`).
   - Kontrollskriptet lister de som mangler, i `utelatt-mangler.tsv`. Fyll ut begrunnelsen der og flytt radene til `utelatt.tsv`.
   - Begrunnelser kan gis gruppevis, for eksempel «metodelitteratur, ikke en studie av tiltaket». Hver rad skal likevel ha en begrunnelse som stemmer for den kilden. Er det hundrevis, kan gruppene lages med et skript ut fra ord i tittel og sammendrag, men kandidater som handler om tiltaket i mandatet eller som det blinde utvalget tok med, begrunnes for hånd.
7. **Rapport:** skriv `utvalg.md` med:
   - antall kilder
   - hva referansene og det blinde utvalget fant
   - metningsvurderingen
   - hvilke sentrale kilder som mangler tekst

## Steg 3: tekst [skript]

1. `sporsmal_sok.py <mappe> --pdf` henter tekst for alt i `valgt.txt` som ikke har tekst i kildebiblioteket, til `kilder/<id>/tekst.txt`, og lagrer adressen den kom fra. Den prøver i rekkefølge:
   - åpne lenker fra OpenAlex, og følger nettsider til PDF
   - Europe PMC
   - Nasjonalt vitenarkiv
   - nav.no for *Arbeid og velferd*

   Tekst der under 70 prosent av tittelordene står i starten, avvises som feil dokument. Resultatet står i `pdf-logg.tsv`.

   Id-er som fikk «ingen pdf» i forrige `pdf-logg.tsv`, prøves ikke på nytt (de står som «ingen pdf (forrige runde)»), så senere runder bare henter nye kilder. Bruk `--pdf-alle` for å prøve alle på nytt. En nettside som ikke svarer (tidsavbrudd eller ingen tilkobling), prøves bare én gang per kjøring, og andre adresser på samme vert hoppes over. Tekst som lastes opp i innboksen, finnes uansett, fordi kildebiblioteket sjekkes først.
2. **Les varslene i `pdf-logg.tsv`:**
   - **«LITE TEKST»:** PDF-en er trolig skannet. Kilden regnes som ikke lest og føres i `mangler.md`.
   - **«LITE TEKST» på en nav.no-artikkel:** bare ingressen ble hentet. Hent PDF-en for hånd eller før kilden som lest bare i sammendrag.
   - **«ÅPEN VERSJON»:** teksten er en preprint eller et arbeidsnotat. Sjekk at tallene stemmer med den publiserte versjonen der det er mulig, og si i svaret at det er en åpen versjon.
   - **«SJEKK DOKUMENT»:** førsteforfatteren står ikke i starten av teksten. Les de første sidene og sjekk tittel, forfattere og år. Er det feil dokument (for eksempel en annen rapport fra samme senter, eller en avhandling med samme generiske tittel), slett `kilder/<id>/tekst.txt` og skriv id-en i `avvist.txt` i spørsmålsmappen, med grunnen etter `#`. Ellers henter neste `--pdf` samme dokument igjen (dagpenger 10.11.2026). Kilden står da i `mangler.md`, og en riktig tekst kan lastes opp i innboksen.
3. **Åpne versjoner:** `--versjoner` finner åpne versjoner (arbeidsnotater, preprint) av kilder uten tekst og skriver `versjoner.tsv`. Ta inn en versjon bare når tittelen stemmer. Legg versjonens id i `valgt.txt` med kommentaren «åpen versjon av <id>», og la den publiserte id-en stå. Tallene hentes fra versjonen. I svaret lenkes det til versjonen, og det står at det er et arbeidsnotat.
4. **Det som ikke kan hentes:** `sporsmal_mangler.py <mappe>` skriver `mangler.md`. Er listen lang, marker de 10–15 bestilleren bør hente først: oversikter og studier i kategori 1–3 uten åpen versjon, norske før utenlandske. Resten kan stå som sammendrag. Skriptet med lenker til forlag og Google Scholar. Statuslista oppdateres av den som har tilgang til Claude Docs. En kjøring uten tilgang skriver endringene i rapporten sin i stedet. Statuslista er én Claude Doc for alle spørsmål, «Kilder som må hentes for hånd» (https://claude.ai/artifact/XXh6fFjz7nD8TZXhc9FYd9). Den har ett avsnitt per spørsmål og statusvalgene Lastet opp, Ikke tilgjengelig, Ikke relevant og Lest inn. Legg til avsnitt for nye spørsmål, og sett «Lest inn» når teksten er hentet ut.

   **Si fra til bestilleren med en gang, uten å stoppe.** En liste i en fil blir sjelden lest: i dagpenger sto tolv viktige PDF-er bare i `mangler.md` og i sluttrapporten. Så snart `mangler.md` er skrevet, send bestilleren en egen melding med:
   - de 10–15 kildene som bør hentes først, hver med lenke og en halv linje om hvorfor den betyr noe (kategori, land, norsk eller utenlandsk)
   - lenken til opplastingssiden: https://github.com/Offallnor/forskning-tekst/upload/main/forskning/innboks
   - en kort forklaring: prøv lenken til forlaget først (den virker ofte gjennom abonnementet til arbeidsplassen eller biblioteket), så Google Scholar (ofte en åpen versjon hos forfatteren, merket «[PDF]»). Last ned PDF-en og dra den inn på opplastingssiden. Filnavnet spiller ingen rolle. Finnes kilden ikke, eller er den bak betalingsmur, si fra, så føres den som ikke tilgjengelig.

   Fortsett med uttrekket mens bestilleren henter. Før svaret skrives (steg 5), gi en ny påminnelse med det som fortsatt mangler, og tilby å lese inn det som er lastet opp før svaret låses. Vent ikke hvis bestilleren ikke svarer. Det som er lastet opp, hentes ut og kontrolleres som i steg 4.
5. **Innboksen:** bestilleren laster ned PDF-er og drar dem inn på opplastingssiden for `forskning/innboks/`. Workflowen `forskning-innboks.yml` kjenner igjen kilden på DOI eller tittel, legger fila og teksten i kildebiblioteket og logger i `innboks/logg.md`. Fila lagres alltid. Teksten erstattes bare når den gamle var for kort, fordi uttrekkene viser til sidene i den teksten som ligger der. Filnavnet spiller ingen rolle. Ukjente filer havner i `innboks/ukjent/`.

## Steg 4: uttrekk [vurdering]

**Store utvalg (over om lag 300 studier når versjoner er slått sammen).** Spør bestilleren om uttrekket skal avgrenses til en kjerne. Spør etter at første utvalg, kategorisering og prioritering er gjort, så avgrensningen bygger på dem. Foreslå denne kjernen: oversikter, kategori 1–3 og nordiske studier, med dobbelt uttrekk. Resten står i `valgt.txt` og i vedlegg A uten tall, og forbeholdene sier hva som er holdt utenfor. Uten avgrensning blir kostnaden mange ganger anslaget.
- **Før kjernen låses:** les metodedelen for studier i kategori 4 med et design som kan holde til kategori 3 (matching, panel, forskjell-i-forskjell, instrument), og for studier merket «tvil». Flytt dem opp der identifikasjonen holder etter reglene i steg 0. Kategorien er satt ut fra sammendraget i første utvalg, så en sterk studie kan ellers falle utenfor kjernen.
- **Kjør** `sporsmal_grupper.py <mappe> --kjerne`. Den leser kategorien først i kommentaren i `valgt.txt`. Kilder uten kategori tas med, og skriptet sier hvor mange det er, så sett kategori på dem og kjør på nytt. Kilder utenfor kjernen får «ikke uttrekk (utenfor kjernen)», og `--sjekk` teller dem ikke.

**Grupper:** `python3 -I forskning/verktoy/sporsmal_grupper.py <mappe>` skriver `grupper.tsv`. Kilder med tekst eller sammendrag fordeles i grupper på høyst 25 (oversikter først, så nordiske, så resten), og hver gruppe gis til én uttrekkskjøring. Kilder uten tekst og uten sammendrag får «ikke uttrekk»: de gir ingen tall og skal ikke ha rader i `estimater.tsv`. `kildeoversikt.py` lister dem i vedlegg A under «Kilder som ikke kunne leses». Ta én versjon per studie. Etter uttrekket viser `sporsmal_grupper.py <mappe> --sjekk` kilder med tekst eller sammendrag som ikke fikk noen rad. De hentes ut før svaret skrives.

Kjør først `kilder_oversikt.py <mappe>`. Den skriver `tidligere-estimater.tsv` og `tidligere-budskap.tsv` med det andre spørsmål har hentet ut fra de samme kildene. Hver kilde leses likevel på nytt for dette spørsmålet. De tidligere radene brukes først etterpå, som en sjekkliste over tall som kan være oversett, fordi de er valgt for et annet spørsmål og kan styre lesingen. Budskapsrader gjelder forfatternes hovedbudskap og kan brukes i steg 1a, men flaggene vurderes på nytt mot dette spørsmålet.

En egen kjøring henter ut tall etter `verktoy/UTTREKK.md` til `estimater.tsv`. Hvert tall skal ha ordrett sitat og side. Tall som bare står med ord, og tall som en kilde gjengir fra en annen studie, behandles etter reglene i `UTTREKK.md`. Forfatternavn tas fra tittelsiden når den finnes, ellers fra metadata, aldri fra hukommelsen, også når rekkefølgen er en annen enn den som vanligvis brukes. Tittelsiden går foran når de to er ulike. Vitenarkivet fører for eksempel opp veiledere som forfattere av masteroppgaver.

**Uavhengighet:** kjøringen får en kopi i et eget arbeidsområde, laget med `sporsmal_kopi.py <mappe> <målmappe>`. Kopien har bare kildene i `valgt.txt`, `kandidater.jsonl`, `valgt.txt`, `kriterier.md`, skriptene og instruksene, og tomme `svar.md` og `estimater.tsv`. Kontroll 6 feiler i kopien, fordi `utelatt.tsv` mangler, og skal ikke rettes der. Den skal ikke kunne lese `svar.md`, `estimater.tsv` eller `budskap.tsv`. Den skriver nye rader til `estimater-nye.tsv`, kjører kontrollene på en kopi der radene er lagt til, og retter egne feil før den leverer.

**Andre uttrekk:** når svaret skal brukes videre, gjøres et andre, uavhengig uttrekk (`estimater-b.tsv`) med en annen modell. Første uttrekk kjører på Opus (tråden), det andre på Sonnet. Med flere enn to–tre grupper kjøres uttrekket av underagenter, én per gruppe, hver i sin egen kopi: Opus for første uttrekk og Sonnet for det andre. De to sammenlignes i `sammenligning.md`. Det andre uttrekket har funnet tall det første hadde oversett, men ingen oppdiktede tall. Tall som skal brukes i svaret, må flyttes til `estimater.tsv`, fordi kontroll 5 bare leser den fila.

## Tilvalg: statistikk [skript og vurdering]

Når mandatet ber om statistikk. Løypa brukes på mange temaer, så kildene finnes ut fra spørsmålet, ikke fra en fast liste.

1. **Finn tabellene i datakatalogen** i Offallnor/offdocs: start i `data/VEIVISER.md` og `data/sporsmal.md` (https://raw.githubusercontent.com/Offallnor/offdocs/main/data/VEIVISER.md). Den dekker SSB, Nav, Eurostat og OECD. Velg aldri tabell eller tall fra hukommelsen. Mangler katalogen tall for temaet, si det i svaret («ikke dekket i datakatalogen»), og foreslå hvor de kan finnes.
2. **Lagre uttrekket** i `statistikk/` i spørsmålets mappe, så tallene kan kontrolleres:
   - Nav, Eurostat og OECD: kopier TSV-fila fra `data/` i offdocs.
   - SSB: legg `sporsmal_sok.py <mappe> --ssb <tabell> '<valueCodes>'` i `kjor.sh` (SSB nås bare fra Actions). Finn tabell og koder med SSB-tilkoblingen eller `data/ssb.md`, og filtrer smalt (se `data/ssb-bruk.md`).
3. **Før tallene i `statistikk.tsv`**, ett tall per linje, med kolonnene `kilde`, `tabell`, `beskrivelse`, `periode`, `verdi`, `enhet`, `definisjon`, `fil`, `adresse`, `hentet` og `utregning`. `definisjon` sier hva tallet måler hos kilden. Er tallet regnet ut (andel, endring), skriv formelen og kildetallene i `utregning`, og før kildetallene på egne linjer.
4. **Kontroll 7** sjekker at hvert tall står i fila det er hentet fra, og kontroll 5 godtar tall i svaret som står i `statistikk.tsv` (også tabellkoden). Et tall som er avrundet i svaret (37,4 der fila har 37.412118), føres som egen rad med avrundingen i `utregning`.
5. **Figurer:** avtal to til fire figurer med bestilleren i mandatet, for eksempel utvikling over tid, land, undergrupper eller diagnoser. Før tallpunktene i `figurer.tsv`, ett punkt per linje, med kolonnene `figur`, `type` (linje eller soyle), `tittel`, `enhet`, `serie`, `x`, `verdi`, `fil` og `kilde`. `python3 -I forskning/verktoy/figur.py <mappe>` sjekker at hvert tall står i fila det er hentet fra, og lager PNG i `figurer/`. Mangler et tall, lages ingen figurer. Lim figurene inn i `svar.md` med `![tittel](figurer/<figur>.png)`. Skriptet krever matplotlib (`pip install matplotlib`) og kjører lokalt, ikke i Actions. Kontroll 8 sjekker tallene på nytt, og at hver figur er laget og lenket i svaret.

Regler for svaret:
- Statistikken står i et eget avsnitt, atskilt fra forskningen, og beskriver nivå, utvikling og fordeling. Den brukes aldri som bevis for effekt.
- Si hvilken kilde og definisjon hvert tall har. Samme begrep måles ofte ulikt hos ulike kilder og i studiene. Sammenlign ikke tall med ulik definisjon uten å si det.
- Oppgi periode og hentedato. Statistikk revideres.

## Steg 5: svar [vurdering]

**Tall i teksten.** Tall til og med tolv skrives med bokstaver i løpende tekst, tall over tolv med siffer (*tre forsøk*, *14 studier*, *etter 18 måneder*). Estimater, prosent, beløp, konfidensintervaller og tall med målenhet skrives alltid med siffer, også når de er små (*4 prosentpoeng*, *RR 1,22*). Veksle ikke mellom bokstaver og siffer i samme setning når tallene hører sammen (*mellom 6 og 14 år*, ikke *mellom seks og 14 år*). Begynn ikke en setning med siffer, skriv den om (*Av dem er 134 lest i fulltekst*). Regelen følger Språkrådet («Siffer eller tallord?») og de felles skrivereglene. Kontroll 5 sjekker ikke tallene i innledningen eller antall og tidsrom som beskriver studiene (*15 forsøk*, *96 kommuner*, *etter 18 måneder*).

Skriv `svar.md` med disse delene, i denne rekkefølgen:

- en innledning om kildegrunnlaget, med antall kilder i fulltekst og bare sammendrag
- kort svar
- statistikk med figurer, når mandatet ber om det (se «Tilvalg: statistikk»)
- funn gruppert etter design, i lesbar tekst med få tall per avsnitt (alle tallene står i vedlegg A). Evalueringer av forvaltningen står til slutt i et eget avsnitt med forbeholdet i overskriften.
- oversikter
- beslektede tiltak
- forbehold
- kunnskapshull og mulige egne analyser

Forbeholdene skal si hvor mange av de sentrale kildene som ikke er lest i fulltekst, og nevne de viktigste med navn. Antallet står i vedlegg B, og kontrollskriptet minner om det (kontroll 10, en påminnelse som ikke teller som feil). Er en oversikt eller en studie i kategori 1–3 blant dem, står det også i det korte svaret.

Forbeholdene skal alltid si at danske rapporter på eget språk og de nyeste arbeidsnotatene kan mangle, fordi søket ikke dekker dem godt. Er det svenske eller finske søket ikke kjørt, gjelder det også svenske eller finske rapporter.

Deretter vedleggene:

- **Vedlegg A, kildeoversikt:** `python3 -I forskning/verktoy/kildeoversikt.py <mappe>` skriver `vedlegg-kilder.md` med alle kildene i `estimater.tsv`, gruppert etter design (Norden først, nyeste først). Tallene tas ordrett fra uttrekket med side, og forbeholdene fra `budskap.tsv`. Alle kildene skal med, ikke bare de viktigste. Kjør skriptet på nytt etter hver endring i uttrekket.
- **Vedlegg B, sentrale kilder som ikke er lest eller er utelatt:** `python3 -I forskning/verktoy/vedlegg_bc.py <mappe>` skriver `vedlegg-b.md` med oversikter og studier i kategori 1–3 uten fulltekst (en annen versjon med tekst regnes som lest), kilder utenfor kjernen og de utelatte etter begrunnelse fra `utelatt.tsv`.
- **Vedlegg C, kort metode:** samme skript skriver `vedlegg-metode.md` med tall for søk, kandidater, referanserunder, sikting, blinde utvalg, uttrekk og kontroller, hentet fra filene i mappen. Vurderingene står i `utvalg.md` og `metning.md`. Kjør skriptet på nytt etter hver endring.

**Kunnskapshull og mulige egne analyser.** Skriv først når kartleggingen av forskning og statistikk er ferdig. Si hva svaret ikke dekker: mangler norske studier, en gruppe, et utfall eller en nyere periode, eller finnes det bare tall som ikke kan brytes ned slik spørsmålet krever? Når registerdata kan fylle hullet, pek på microdata.no (SSB og Sikt) som mulighet for egne analyser eller bedre tall. Skriv kort hvilke registre og variabler som trolig trengs, hvilken sammenligning som kan gjøres, og hvilke begrensninger det har (for eksempel at en enkel sammenligning ikke viser effekt). Følg `data/microdata.md` i offdocs (https://raw.githubusercontent.com/Offallnor/offdocs/main/data/microdata.md): variabelnavn bare fra kopien av variabelkatalogen (`data/microdata/variabler.tsv`), med periode og enhet sjekket, og kommandoer bare fra brukerveiledningen (`data/microdata/manual/`). Merk forslaget som et utkast og oppgi datoen katalogen ble hentet. Står en variabel ikke i katalogen, nevn registeret (for eksempel Navs tiltaksregister og a-ordningen), ikke et gjettet navn. Selve analysen gjøres av brukeren i microdata.no, fordi tilgangen krever innlogging via egen institusjon. Hold avsnittet i svaret kort (om lag 120 ord): kunnskapshullet, hva analysen kan vise og ikke vise, de viktigste registrene og eventuelt ett sterkere opplegg i én setning. Opplegg, forbehold og skriptutkast står i `microdata.md` i spørsmålsmappen, og svaret lenker dit.

Et beskrivende svar grupperes i stedet etter land og etter forklaringene som er nevnt i kriteriene, med nivå og utvikling først.

Hver påstand har lenke til kilden, med forfatter og år som lenketekst (kontroll 1 sjekker navnet): openalex.org/W…, nva.sikt.no/registration/… eller artikkelsiden på nav.no. Skriv hva studien sammenligner og hvilke forbehold forfatterne selv tar. Små antall skrives med bokstaver, fordi hvert tall i svaret må finnes i `estimater.tsv`.

## Steg 6: kontroller [kontroll]

1. **Automatisk:** `python3 -I forskning/verktoy/sporsmal_kontroll.py <mappe>` skriver `kontroll.md`. Svaret går ikke videre med feil. Kontrollene:
   1. kilden finnes, og etternavnet i lenketeksten står blant forfatterne i metadata eller på tittelsiden
   2. sitatet står på oppgitt side (±1)
   3. tallet står i sitatet
   4. estimatet ligger i konfidensintervallet
   5. hvert tall i svaret står i estimat- eller statistikktabellen
   6. utelatte sentrale kilder er begrunnet
   7. hvert tall i statistikktabellen står i den lagrede fila (bare når statistikk er valgt)
   8. hvert tall i figurtabellen står i den lagrede fila, og hver figur er laget og lenket i svaret (bare når det er figurer)
   9. innholdskontrollen er gjort: `kort-svar-blind.md` finnes, hver kilde som er lenket i svaret har en rad i `budskap.tsv` (blind lesing), og `innholdskontroll.tsv` har raden `kort svar`

   Innholdskontrollen (punkt 2–4) er obligatorisk i begge varianter, og svaret leveres ikke før kontroll 9 består. I testrunden i november 2026 fant den feil i vekt eller forbehold i alle tre fulle kjøringer, og i det raske svaret ble en feil i beskrivelsen av utvalget bare funnet ved en manuell sjekk. Kontroll 1–8 fant ingen av dem.
2. **Innhold, steg 1a, blind:** en egen kjøring som ikke ser svaret, skriver forfatternes budskap, identifikasjon og flagg per kilde (`budskap.tsv`) og et eget kort svar (`kort-svar-blind.md`) etter `verktoy/INNHOLDSKONTROLL.md`.
3. **Innhold, steg 2:** kan gjøres av tråden som skrev svaret, men først etter at `kort-svar-blind.md` er lest. Sammenlign svaret med `budskap.tsv` og `kort-svar-blind.md` og skriv `innholdskontroll.tsv`.
4. **Retting:** hvert avvik leses for hånd i kilden før svaret endres. Et sprik mellom tall regnes som avlesningsfeil til det motsatte er vist. På gradert sykmelding fant innholdskontrollen tall som gikk mot hovedtendensen og var utelatt. På egenandel fant den at svaret ga feil inntrykk av hva en norsk studie konkluderte med.
5. **Når svaret endres etter nye kilder:** gjør steg 1a for de nye kildene og legg radene til i `budskap.tsv`. Skriv et nytt blindt kort svar for alle kildene. Gjør steg 2 for hele svaret og lagre det som `innholdskontroll-<n>.tsv`.

## Steg 7: levering

Svaret leveres som Claude Doc eller som tekst til bestilleren, merket «utkast, ukontrollert» til en fagperson har sett det. Si hvilke sentrale kilder som mangler.

**Reproduserbarhet.** Øverst i `svar.md`, under innledningen, står en linje med dato for søket, commit for katalogene (`git log -1 --format=%h -- forskning/katalog`), modell for uttrekk og blind lesing, og hvor mange kilder som bare er lest i sammendrag. En stegtest i november 2026 viste at søket gir samme kandidater ved ny kjøring, at to nye synteser lander på samme retning, men at et nytt blindt utvalg bare fikk med 71 prosent av de sterke kildene (84–90 prosent per studie med prioritert rekkefølge, 94–97 prosent med to utvalg på ulike modeller). Den endelige vektingen i det korte svaret er derfor en vurdering, og det korte svaret skal leses av en fagperson før det brukes.

**Når en ny omgang endrer konklusjonen.** Endrer en ny gjennomkjøring det korte svaret i retning, skrives det øverst i svaret med dato og grunn.

## Kostnad

**Grov sikting med Haiku (aktivitetskravet, 5 718 kandidater):** om lag 3,8 millioner Haiku-tokens i 20 kjøringer på fire til seks minutter. Kjøringene går samtidig.

**Gradert sykmelding, fra start:**
- uttrekk: om lag 150 000–270 000 tokens per runde
- blind lesing: om lag 190 000 tokens for sju kilder
- innholdskontroll for tre spørsmål: om lag 780 000 tokens

**Egenandel, gjenopptatt med 43 nye kilder:**
- underagenter: om lag 1,4 millioner tokens, i tillegg til hovedtråden
- tid: om lag en time, med fem runder i Actions
