# Instruks for uttrekk av funn (pilot)

Gjelder uttrekk av funn fra kildene i `forskning/sporsmal/<mappe>/`. Instruksen er den samme for første og andre (uavhengige) uttrekk.

## Hva du leser

- `forskning/kilder/<id>/tekst.txt`: fulltekst fra kildebiblioteket. Sidene er skilt med tegnet form feed (`\f`). Side 1 er første side i PDF-en, ikke sidetallet som står trykt på siden.
- `kandidater.jsonl`: metadata og sammendrag for alle kandidater. For kilder i `valgt.txt` uten tekstfil kan du bare bruke sammendraget. Kilder uten tekst og uten sammendrag er tatt ut før uttrekket (`grupper.tsv`). Skriv ikke rader av typen «ingen tekst».
- `tidligere-estimater.tsv` (hvis den finnes): rader som andre spørsmål har hentet ut fra de samme kildene. Les den først når du er ferdig med ditt eget uttrekk fra kilden. Bruk den som en sjekkliste over tall du kan ha oversett, ikke som utgangspunkt, fordi radene er valgt for et annet spørsmål. Ta bare med rader som svarer på dette spørsmålet, og kontroller sitat og side mot teksten som for nye rader.

Bruk bare det som står i disse filene. Ikke bruk egen kunnskap om studiene, forfatterne eller andre studier. Det gjelder også land og fortegn: land tas fra teksten eller metadata, aldri fra forfatternavn eller hvor forfatterne arbeider, og står landet ikke noe sted, la feltet stå tomt (dagpenger 10.11.2026: én kjøring satte land ut fra forfatternavn).

**Arbeidsmappe.** Du har fått en egen mappe. Skriv hjelpeskript, mellomfiler og resultat bare der, aldri i mappen over eller i en mappe andre kjøringer bruker. Flere kjøringer går samtidig, og i dagpenger 10.11.2026 overskrev de hverandres filer.

Når du skriver forfatternavn, ta dem fra tittelsiden i teksten. Står det andre navn i metadata (`kandidater.jsonl`), går tittelsiden foran. Vitenarkivet fører for eksempel opp veiledere som forfattere av masteroppgaver. Årstallet tas fra metadata, også når tittelsiden har et annet år (for eksempel trykt utgave året etter at artikkelen kom på nett).

## Hva du henter ut

Hent ut hovedfunnene som svarer på spørsmålet. Det betyr effektestimater eller sentrale beskrivende tall (nivå, endring over tid), med usikkerhet når den er oppgitt. Ta med det forfatterne selv presenterer som hovedresultat, normalt 1–4 linjer per kilde. Ikke ta med alle tall i tabellene.

## Format

Én linje per funn i en tsv-fil med disse kolonnene (tabulator mellom, første linje er overskriften):

| Kolonne | Innhold |
|---|---|
| id | id-en fra `kandidater.jsonl`: OpenAlex (W…), vitenarkivet (lang identifikator), Arbeid og velferd (AV-…), Kudos (KU-…), LIBRIS (LI-…), Finna (FI-…) eller rapport lagt inn med adresse (R-…) |
| design | rct (også randomiserte brev, varsler eller kontroller), kvasi (reform, naturlig eksperiment, diskontinuitet), register (observasjonsdata med kontroll), oversikt, beskrivende, simulering (modellberegning uten observert effekt), kvalitativ, forvaltning (evaluering av en etat eller ordning uten effektmål: gjennomføring, organisering, erfaringer) |
| land | land studien gjelder |
| gruppe | hvem funnet gjelder når det ikke er hele utvalget, for eksempel «psykiske lidelser», «under 30 år», «kvinner» (tomt for hele utvalget). Gjør funnet lett å finne igjen for senere spørsmål om undergrupper |
| utfall | hva som måles, kort på norsk |
| sammenligning | hva som sammenlignes, kort på norsk |
| mal | effektmål: RR, OR, HR, pp (prosentpoeng), prosent, dager, elastisitet, koeffisient, annet |
| estimat | ett tall, med sifrene slik de står i sitatet: uten prosenttegn, enhet eller tekst. Bruk punktum som desimaltegn. Ta med minustegn bare når det står i sitatet. Er resultatet et spenn (70–85) eller flere tall (70 / 68 / 71), lag én linje per tall eller skriv det nederste tallet og forklar i utfall |
| ki_lav, ki_hoy | konfidensintervall slik det står (tomt hvis ikke oppgitt) |
| n | antall personer eller observasjoner (tomt hvis ikke funnet) |
| side | sidenummer i tekstfilen (telles med `\f`), eller `sammendrag` hvis tallet er hentet fra sammendraget i kandidater.jsonl |
| sitat | ordrett utdrag fra teksten, en eller to setninger, der estimat og KI står |

Regler for sitatet:
- Kopier ordrett fra tekstfilen. Ikke rett skrivefeil, ikke sett inn eller fjern ord. Linjeskift kan erstattes med mellomrom, og orddeling over linjeskift kan slås sammen.
- Estimatet og KI-grensene må stå i sitatet med de samme sifrene som i kolonnene. Et tall uten null foran desimaltegnet («.32») skrives 0.32 i `estimat`. Skriv aldri 32 for .32.
- Ta sitatet fra én side. Et sitat som går over et sideskift, finner ikke kontrollen.
- Står retningen med ord og ikke med minustegn («reduserte ledighetstiden med 0,9 uker»), skriv tallet uten minustegn og retningen i `utfall` («nedgang», «kortere»).
- Velg et sitat fra løpende tekst eller sammendrag framfor tabeller, fordi tabeller ofte blir uleselige i tekstfilen.
- Står tallet bare med ord i kilden («um drei Prozent», «to prosentpoeng»), skriv sifrene i `estimat` og «(tallet står med ord i sitatet)» i `utfall`. Kontrollen godtar da et sitat uten sifre, og tallet kontrolleres for hånd.

Tall som en kilde gjengir fra en annen studie (sekundærsitat):
- Ta dem bare med når den opprinnelige studien ikke er lest.
- Bruk id-en til kilden du leser, og skriv «gjengitt fra <forfatter år>» i `utfall`.
- Er den opprinnelige studien lest, hentes tallet derfra.

Finner du ikke tall for en kilde, skriv én linje med tomt estimat og en kort forklaring i `utfall`, for eksempel «ingen effektestimat i teksten». La sitatet stå tomt hvis det ikke finnes tekst å sitere.

Ta bare med tall som beskriver effekter eller utvikling. Holdninger og meninger (for eksempel andelen leger som tror et tiltak virker) er ikke funn i denne sammenhengen.
