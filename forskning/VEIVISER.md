# Forskning fra Nasjonalt vitenarkiv – veiviser

Startet 6.11.2026 som pilot. En oversikt over norsk forskning på arbeid, velferd, arbeid og helse og integrering, hentet fra Nasjonalt vitenarkiv (NVA, nva.sikt.no), som drives av Sikt. Repoet er åpent. Fulltekst og PDF-er ligger i et eget privat repo, fordi de kan være vernet av opphavsrett.

## Hva som ligger her

| Fil | Innhold |
|---|---|
| `temaer.tsv` | De 15 temaene, søkeordene som avgrenser dem. |
| `katalog/poster.jsonl` | Én forskningspost per linje, og hver post står bare én gang. `temaer` lister temaene posten hører til. Feltene er tittel, år, type, forfattere, institusjoner, emneord, sammendrag slik det står i NVA, lisens og lenke. `oversikt: true` markerer systematiske oversikter, metaanalyser, kunnskapsoppsummeringer og forskningskart. |
| `katalog/arbeid-og-velferd.jsonl` | Alle artikler i Navs tidsskrift Arbeid og velferd fra 2007, med forfattere, ingressen fra nav.no og lenke til PDF. Tidsskriftet er verken i NVA eller OpenAlex. Lages av `verktoy/arbeid_og_velferd.py` i den samme ukentlige jobben. |
| `katalog/kudos/` | Kunnskapsdokumenter fra offentlig sektor i DFØs Kudos (kudos.dfo.no), én fil per dokumenttype: evalueringer, studier, kartlegginger, kunnskapsoppsummeringer, NOU-er, områdegjennomganger og forhåndsutredninger. Felt: tittel, år, forfattere, eiere, utførere, sammendrag og lenke til PDF. Lages av `verktoy/kudos.py` fra DFØs åpne eksport i den samme ukentlige jobben, og brukes av det norske søket i forskningsspørsmålene. |
| `katalog/navbibliotek.jsonl` | Rapporter med lenke til fulltekst i Navs bibliotek (bibliotek.nav.no), om lag 700 av 5 200 poster (resten er fagbøker): Navs rapportserie, Fafo, NOVA, Oxford Research, Proba m.fl. Mange finnes ikke i Kudos. Lages av `verktoy/navbibliotek.py` i den samme ukentlige jobben, og brukes av det norske søket. |
| `katalog/telling.tsv` | Antall poster per tema, og hvor mange som hører til flere temaer. Tell aldri sammen tallene for flere temaer, bruk linjen `alle`. |
| `estimater/oversikter.tsv` | Estimater og konklusjoner hentet ut fra de systematiske oversiktene, med sitat, side og koblinger mellom oversiktene. |
| `kilder/<id>/` | Felles kildebibliotek for forskningsspørsmålene: metadata med lenke og adressen teksten ble hentet fra (`kilde.json`), teksten (`tekst.txt`) og fila når den er lastet opp for hånd (`fil.pdf`). `kilder/oversikt.tsv` lister alle kildene og hvilke spørsmål som bruker dem. Teksten og fila ligger i det private repoet med samme sti, fordi de kan være vernet (se `CLAUDE.md` i roten). |
| `sporsmal/oversikt.tsv` | Ett spørsmål per linje, med status og antall kilder. |
| `LOYPE.md` | Oppskrift for å svare på et spisset forskningsspørsmål: kriterier, søk (også norske kilder), utvalg, tekst, uttrekk, svar og kontroller. Pilot. Har to varianter, full løype og raskt svar fra kildebiblioteket, og begge starter med et mandat som utvikles sammen med bestilleren. Spørsmålene ligger i `sporsmal/<mappe>/`. |
| `verktoy/hent.py` | Henter katalogen. Kjøres hver tirsdag kl. 05.30 UTC (`.github/workflows/forskning-hent.yml`) og når temaene endres. |

Katalogen har bare rapporter, arbeidsnotater, artikler, kapitler, bøker, oversikter og doktorgrader fra 2010. Studentoppgaver, foredrag og medieinnslag er holdt utenfor. Fulltekst lagres ikke. Flerordssøk står i anførselstegn. En post tas bare med når søkeordet eller hele uttrykket står i tittel, sammendrag eller emneord, fordi NVA-søket også gir treff på spredte ord og fulltekst.


## Regler for svar

1. **Lenk alltid** til oppføringen i NVA (`nva`-feltet). Brukeren skal kunne lese studien selv.
2. **Si hva slags kilde det er.** Dette er forskning, ikke lov eller forskrift. Oppgi forfattere, institusjon og år.
3. **Sammendraget står ordrett** slik forfatterne skrev det i NVA. Skill mellom hva studien sier og din egen oppsummering.
4. **Estimatene er ukontrollerte** til `status` sier noe annet. Si det, og oppgi sitat og side.
5. **Oversikter holdes for seg.** Slå aldri sammen estimater fra ulike oversikter, eller fra oversikter og enkeltstudier. Bruk kolonnene `samme_oversikt_som`, `oppdaterer`, `oppdatert_av` og `overlapp_med`, og bruk den nyeste oversikten når en er oppdatert.
6. **Standardiserte tall er utregninger.** Kolonnene `pp`, `cohens_d` og `se_ln` er regnet ut av Claude med formelen i `omregning`. Oppgi originalestimatet først.
7. **Tillit** er forfatternes egen vurdering (GRADE e.l.). Sett ingen samlet tillitsscore selv.
8. **Katalogen er et utvalg.** Søkeordene avgrenser temaene grovt, og NVA har ikke all forskning (mange internasjonale artikler mangler sammendrag og fil). Si «ingen funnet i katalogen», ikke «finnes ikke».

## Estimattabellen

Én linje per estimat eller konklusjon. Viktigste kolonner:

- `kildetype`: systematisk oversikt, metaanalyse, kunnskapsoppsummering, hurtigoversikt, kartleggingsoversikt, forskningskart.
- `resultattype`: estimat, konklusjon (ordrett, uten tall), ingen studier (kunnskapshull), kostnad-nytte, kartlegging, ikke hentet.
- `mal`, `estimat`, `ki_lav`, `ki_hoy`: originalestimatet. RR = relativ risiko, OR = oddsratio, HR = hasardrate-forhold, SMD = standardisert gjennomsnittsforskjell. 1 (eller 0 for SMD) betyr ingen forskjell.
- `kontrollandel`, `pp`: andel i arbeid i kontrollgruppen fra oversiktens egen tabell, og effekten i prosentpoeng.
- `sitat`, `side`: hvor tallet står. Side er sidetall i PDF-filen.

Skjemaet for enkeltstudier (design, utfallsdata, frafall, fagfellevurdering) er beskrevet i prosjektets pilotnotat og legges til når enkeltstudiene tas inn.

## Vedlikehold

- Katalogen oppdateres automatisk.
- Estimater hentes ut for hånd (av Claude i en økt) når nye oversikter kommer til.
- Svar fra Sikt om gjenbruk av metadata og sammendrag avgjør om katalogen kan flyttes til et åpent repo.
