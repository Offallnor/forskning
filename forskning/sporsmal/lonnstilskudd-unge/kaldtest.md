# Kaldtest: fullt svar med statistikk (lønnstilskudd for unge)

8.11.2026. En ny tråd kjørte løypa med bare `skills/felles-forskning/SKILL.md` og `forskning/LOYPE.md`, på et tema langt fra sykefravær. Prosjektlederen spilte bestilleren i mandatsamtalen.

**Resultat:** mandat godkjent etter åtte korte runder (om lag sju minutter). Fullt svar med statistikk og kunnskapshull levert som utkast i `svar.md`, med 0 feil i den automatiske kontrollen (1758 kontroller) og en innholdskontroll med fire avvik av middels alvor, som er rettet. Tid fra start til utkast om lag en og en halv time. Underagenter brukte om lag 1,5 millioner tokens (blindt utvalg 0,3, fire uttrekk 0,86, blind lesing 0,38), i tillegg til hovedtråden.

## Det som virket

- **Mandatsamtalen.** Ett spørsmål om gangen med ferdige formuleringer gjorde at bestilleren kunne svare «ok». Kravet om å foreslå statistikk fikk med et avsnitt bestilleren ellers ikke hadde bedt om.
- **Det blinde utvalget** var den viktigste kontrollen. Det fant 49 kilder innenfor mandatet som første utvalg manglet, blant dem fem norske studier av tiltak for unge.
- **Statistikken** fant tabellene i datakatalogen (Nav TILT110 og HL050, arbeidsindikatoren, Eurostat NEET, OECD LMP, SSB 13760 via Actions). SSB-hentingen virket første gang.
- **Innholdskontrollen** fant at det korte svaret ikke skilte tydelig nok mellom godt identifiserte studier og matchingstudier.

## Funn om oppskriften

Merket **høy** når det kan gi feil eller ufullstendig svar, **middels** når det koster tid eller krever skjønn oppskriften ikke gir, **lav** for små ting.

### Mandat og variant

1. **Lav.** Skillen ber om ett spørsmål om gangen, men sier ikke at Claude kan foreslå «type» og «ferdig når» selv og vise dem i helheten. Det sparte to runder her. Én gang ble det to spørsmål i én melding.
2. **Middels.** Generelle avgiftslettelser for unge (for eksempel lavere arbeidsgiveravgift i Sverige) ble foreslått holdt utenfor av Claude og godtatt uten diskusjon. Det er et grensetilfelle med mye forskning. Oppskriften bør be om at avgrensninger som utelukker en stor del av litteraturen, nevnes eksplisitt for bestilleren.

### Søk og utvalg

3. **Middels.** `--fra=ÅR` finnes i `sporsmal_sok.py`, men står ikke i LOYPE.md. Mandatet hadde «publisert fra 2000».
4. **Høy.** Søket ga 1230 OpenAlex- og 253 norske kandidater. Oppskriften sier ikke hvordan så mange skal sorteres. Jeg filtrerte på ord og leste titler sortert etter siteringer, og bommet på norske studier med få siteringer som det blinde utvalget fant. Forslag: les `norske-kandidater.tsv` i sin helhet, og sorter ikke bare etter siteringer.
5. **Høy.** Kjente kilder fra bestilleren som ligger på regjeringen.no (områdegjennomgangen av arbeidsmarkedstiltak) har ingen hentevei. `tittel:` slår bare opp i OpenAlex, `--pdf` når ikke regjeringen.no, og skymiljøet når den heller ikke. Innboksen kjenner bare igjen kilder som finnes i `kandidater.jsonl`. Et nettsøk fant også en evaluering av varig lønnstilskudd på regjeringen.no som ingen søk fant. Løypa mangler et spor for offentlige utredninger, områdegjennomganger og bestilte evalueringer.
6. **Middels.** Referanseregelen («uttrykk i tittel eller sammendrag») med uttrykk som «youth unemployment» slapp inn mye om årsaker til ungdomsledighet, kriser og arr, og metodelitteratur om metaregresjon. Oppskriften advarer bare om metodelitteratur og andre ordninger.
7. **Middels.** Metningsregelen sier at det blinde utvalget ikke skal finne nye kilder i kategori 1–3, men ikke hva som skjer når det gjør det, ut over «en referanserunde til». Skal det da kjøres et nytt blindt utvalg? Jeg gjorde det ikke.
8. **Middels.** Utvalget vokste til 120 id-er med versjoner. Oppskriften har ingen prioritering for uttrekk når utvalget blir så stort. Jeg delte uttrekket i fire grupper og tok én versjon per studie.
9. **Middels.** Tre valgte kilder handlet ikke om spørsmålet: en studie av Civilian Conservation Corps med «New Deal» i tittelen, en juridisk masteroppgave og en praksisordning for studenter. Alle var valgt på tittel og ble fanget av uttrekket. Forslag: kommentaren i `valgt.txt` skal bygge på sammendraget.
10. **Middels.** Når publiserte versjoner dukker opp i en senere runde, sier ikke oppskriften hvilken id som skal være hovedid.

### Tekst

11. **Middels.** Om lag halvparten av de valgte kildene fikk ikke tekst, blant dem de mest sentrale metaanalysene i publisert form. Åpne versjoner reddet flere av dem. `mangler.md` har 60 kilder, som er mer enn en bestiller kan hente for hånd. Oppskriften bør si hvilke som skal prioriteres.
12. **Lav.** En runde med `--pdf` for vel 100 kilder tok 37 minutter i Actions, og en ny push startet ikke før den forrige var ferdig. Oppskriften sier 1–7 minutter.

### Uttrekk og kontroll

13. **Middels.** Kontrollskriptet leser norske tall med tre desimaler («0,075») som tusenskille og godtar dem aldri i kontroll 3. Det rammet fire tall i norske Frisch-rapporter.
14. **Lav.** Kontrollskriptet leser ikke tankestrek som minus rett etter hakeparentes («[–2.4»).
15. **Middels.** Kontroll 6 listet 1189 sentrale kandidater uten begrunnelse. Jeg begrunnet dem gruppevis med et skript ut fra ord i tittel og sammendrag, og så for hånd på de om lag 80 som handlet om lønnstilskudd eller var valgt i det blinde utvalget. Gruppevise begrunnelser er tillatt, men med så mange blir kontrollen mest et formkrav.
16. **Lav.** Kontroll 5 godtok tallet 16,7 fra statistikken før det var ført i `statistikk.tsv`, fordi det samme tallet sto i en estimatrad. Kontroll 7 sjekker at verdien står et sted i fila, ikke i riktig rad og kolonne.
17. **Lav.** Lenketekster i svaret («[Europa](…)») tolkes som forfatternavn i kontroll 1. Bruk alltid forfatter og år som lenketekst.

### Kunnskapshull og microdata.no

18. **Høy.** Steg 5 krever at variablene sjekkes i variabelkatalogen på microdata.no før de nevnes. microdata.no (både www og metadata) nås ikke fra skymiljøet eller WebFetch. Oppskriften har ingen reservevei. Svaret nevner derfor registre, ikke variabelnavn, og sier det. Forslag: en Actions-jobb som henter variabelkatalogen til offdocs `data/`, eller at microdata.no legges til i nettverksreglene.

### Levering

19. **Lav.** Statuslista for kilder som må hentes for hånd (Claude Doc) er ikke oppdatert med et avsnitt for dette spørsmålet. Det må gjøres av den som har tilgang.

## Forslag til retting, i prioritert rekkefølge

1. Spor for offentlige rapporter på regjeringen.no (funn 5).
2. Reservevei for microdata.no (funn 18).
3. Regel for å lese norske kandidater i sin helhet og ikke sortere bare på siteringer (funn 4).
4. Retting i kontrollskriptet for «0,075» og «[–» (funn 13 og 14).
5. Prioritering av uttrekk og manuell henting når utvalget er stort (funn 8 og 11).
