# Instruks for innholdskontroll av svar (pilot)

Kontrollen er obligatorisk i full løype og i raskt svar (kontroll 9 i `sporsmal_kontroll.py` sjekker at den er gjort). Den kommer i tillegg til de automatiske kontrollene. De automatiske kontrollene sjekker at tallene står i kildene. Denne kontrollen sjekker at svaret gjengir kildene riktig og at det samlede inntrykket følger av funnene.

Kontrollen har to steg som gjøres av to ulike kjøringer. Den som gjør steg 1, skal ikke se svaret.

## Steg 1: blind lesing (leser ikke `svar.md`)

### 1a Forfatternes budskap og identifikasjon, per kilde

Gjelder hver kilde som er omtalt i svaret (i raskt svar bare dem). Les sammendraget, innledningen og konklusjonen i hver kilde (`forskning/kilder/<id>/tekst.txt`). Har kilden bare sammendrag, bruk det (`kandidater.jsonl`, feltet `sammendrag`). Bruk bare det som står i filene.

Skriv `budskap.tsv` med disse kolonnene:

| Kolonne | Innhold |
|---|---|
| id | OpenAlex-id |
| budskap | forfatternes hovedbudskap med egne ord, på norsk, én til to setninger: hva de fant, i hvilken retning og for hvem |
| hovedresultat | det tallet forfatterne selv løfter fram som hovedresultat, med enhet (tomt hvis ingen) |
| sammenligning | hvem som sammenlignes med hvem: hvem som fikk tiltaket og hvem som ikke gjorde det, utvalg, land og periode (for eksempel «sykmeldte født i oddetallsår fikk tiltaket, partallsår er kontrollgruppe, Hedmark 2012–2013») |
| identifikasjon | hvordan studien skiller effekt fra seleksjon: randomisering, reform eller naturlig eksperiment, diskontinuitet, instrument, forskjell-i-forskjell, faste effekter, søskensammenligning, matching, justering for observerbare kjennetegn, ingen (beskrivende), eller ukjent |
| id_sitat | ordrett sitat som viser identifikasjonen (tomt hvis bare sammendrag og ingenting står) |
| side | side i tekstfilen (telles med `\f`) eller `sammendrag` |
| forbehold | forbehold forfatterne selv tar, kort |
| flagg | se under, flere skilt med semikolon, tomt hvis ingen |
| antakelse | den identifiserende antakelsen: hva som må holde for at estimatet er en effekt, kort og konkret (for eksempel «legens graderingstendens påvirker retur bare gjennom om pasienten graderes») |
| belegg | hva forfatterne viser for å støtte antakelsen, se under. Tomt når de ikke viser noe |
| troverdighet | `høy`, `middels` eller `lav`, med en kort begrunnelse etter semikolon. Tomt for beskrivende studier |

**Antakelse, belegg og troverdighet**. Vurder antakelsen ut fra det kilden selv viser, ikke ut fra metodenavnet. Mange studier sier at de instrumenterer eller bruker forskjell-i-forskjell uten at antakelsen er troverdig, og mange panelstudier er gode. Se etter:

- **Randomisering:** frafall, balanse mellom gruppene ved start, etterlevelse.
- **Instrument:** styrken i første trinn (F-verdi), argumentet for at instrumentet bare virker gjennom tiltaket, og hvem estimatet gjelder for (dem som påvirkes av instrumentet).
- **Diskontinuitet:** tegn på tilpasning rundt grensen, og om resultatet tåler andre båndbredder.
- **Forskjell-i-forskjell og panel med faste effekter:** parallelle trender før tiltaket (figur eller test), om tidspunktet er uavhengig av utfallet, forventningseffekter, tidsvarierende forhold som ikke er kontrollert, og estimator ved trinnvis innføring.
- **Matching og justering:** om det er rimelig at de målte kjennetegnene fanger opp seleksjonen. Troverdigheten er sjelden mer enn `lav` eller `middels`.

`høy`: antakelsen er rimelig og testet der den kan testes. `middels`: rimelig, men lite testet, eller med kjente svakheter forfatterne drøfter. `lav`: lite troverdig eller ikke drøftet. Har kilden bare sammendrag, skriv det i begrunnelsen og sett høyst `middels`.

Flagg:
- `årsaksspråk`: forfatterne skriver om effekt eller årsak, men identifikasjonen er justering for observerbare kjennetegn, ingen eller ukjent. Ikke flagg godt identifiserte studier.
- `undergruppe`: sammendraget løfter fram en undergruppe eller sekundær utfall framfor hovedresultatet.
- `sprik`: tall i sammendraget og tall i resultatdelen ser ut til å ikke stemme. Skriv begge tallene og om de gjelder samme sammenligning. Sjekk først at du har lest riktig rad og kolonne.
- `utvalg`: lite eller spesielt utvalg som gjør resultatet vanskelig å overføre.

### 1b Eget kort svar

Når 1a er ferdig: les `estimater.tsv` og din egen `budskap.tsv`. Skriv et kort svar på spørsmålet, fem til åtte setninger, i `kort-svar-blind.md`. Vekt studiene etter troverdigheten i identifikasjonen og størrelsen, ikke etter metodenavnet eller hvor kilden er funnet. Si hva funnene peker mot, hvor de spriker og hva som mangler.

## Steg 2: sammenligning (leser `svar.md`)

Les `svar.md`, `budskap.tsv` og `kort-svar-blind.md`. Skriv `innholdskontroll.tsv` med én linje per kilde der svaret avviker fra `budskap.tsv`, og én linje for det korte svaret (kontroll 9 krever raden `kort svar`). Kilder uten avvik trenger ingen linje:

| Kolonne | Innhold |
|---|---|
| id | OpenAlex-id, eller `kort svar` |
| svar_sier | det svaret sier om kilden, kort |
| avvik | `ingen`, `retning`, `hovedresultat`, `vekt`, `sammenligning`, `beskrivelse` (svaret beskriver utvalg, tiltak, kontrollgruppe, land eller periode annerledes enn kolonnen `sammenligning` i `budskap.tsv`), `mangler forbehold`, `troverdighet` (svaret gir studien mer eller mindre vekt enn troverdigheten i `budskap.tsv` tilsier) eller `annet` |
| forklaring | hva avviket består i, og hva som bør endres |
| alvor | `høy` (leseren får feil inntrykk), `middels` (viktig nyanse mangler) eller `lav` (formulering) |

Ta også med flagg fra `budskap.tsv` som svaret ikke har tatt høyde for. For det korte svaret: sammenlign med `kort-svar-blind.md` og si hvor de skiller seg i retning, styrke eller hva som framheves.

## Etter kontrollen

Hvert avvik leses for hånd i kilden før svaret endres. Et sprik mellom tall regnes som avlesningsfeil til det motsatte er vist.
