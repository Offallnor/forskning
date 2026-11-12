# Kaldtest: raskt svar (aktivitetskravet og tidlig oppfølging)

8.11.2026. Testrunde med fire nye spørsmål, kjørt i hver sin tråd. Mandatet ble skrevet av Claude etter fullmakt fra bestilleren (`mandater.md`, seksjon 4), uten mandatsamtale. Målet var å prøve om prøveregelen for raskt svar slår til riktig, og hva svaret mangler sammenlignet med en full løype.

## Resultat

- Tolv kilder fra kildebiblioteket (tretten id-er, Hernæs med publisert versjon uten tekst og arbeidsnotat med tekst), 27 rader i `estimater.tsv`. Automatisk kontroll: 0 feil av 136 etter to rettinger. Innholdskontrollen er ikke kjørt (valgfri).
- Tid: under en halvtime fra start til bestått kontroll, det meste til lesing. Ingen runde i Actions.
- Alle fire kjente kilder fra mandatet lå i biblioteket med tekst.

## Prøveregelen for raskt svar

1. **Krav 1 ga et falskt ja ved bokstavelig lesing.** «aktivitetskravet» står i det norske søket i `gradert-sykmelding/kjor.sh`, så kravet ser oppfylt ut. Men det engelske søket gjaldt bare gradert sykmelding, og dialogmøter, oppfølgingsplaner og tidlig oppfølging var ikke med i noe søk. Tråden vurderte kravet som *delvis* oppfylt. Regelen har ingen slik kategori, og sier ikke hva som gjelder når spørsmålet har flere tiltak og bare ett var søkt på. Forslag: kravet gjelder hvert tiltak i det spissede spørsmålet, og både det engelske og det norske søket. Er ett tiltak ikke dekket, anbefales full løype for det, eller spørsmålet deles.
2. **Krav 2 ble oppfylt av kilder som søket ikke fant.** Aktiveringsstudiene (Hernæs, Rehwald mfl., Nav-artiklene om Hedmark) kom inn via referansesporing og det blinde utvalget i `gradert-sykmelding`. Biblioteket var bedre enn søket. Men regelen kan ikke se hva som mangler: biblioteket hadde ingen effektstudie av dialogmøter, og ingen av kravene fanger det.
3. **Krav 3 er uproblematisk** (søket fra 7.11.2026).
4. **Konklusjon:** regelen slo til nesten riktig for aktivitetskravet ved åtte uker (Hedmarksmodellen), der biblioteket hadde fire norske studier og en reformstudie. Den slo feil til for «dialogmøter og annen tidlig oppfølging», der svaret i praksis bare kan si at kildene ikke har effektevalueringer.

## Hva svaret mangler sammenlignet med full løype

Kildene viser selv til studier som ikke er i biblioteket, og som en full løype trolig ville funnet via søk eller referanser:

- et svensk randomisert forsøk med tidlige møter om arbeidsevnen (Engström mfl. 2015, omtalt i Rehwald mfl.)
- den danske studien av saksbehandlersamtaler (Høgelund og Holm 2006, omtalt i Grønstad 2024)
- en svensk studie av tidsgrenser i sykeforsikringen (Hägglund 2013, omtalt i Grønstad 2024)
- de åtte studiene av tiltak i regi av Nav i FHIs forskningskart 2021
- den publiserte versjonen av Hernæs (2018), som mangler tekst
- evalueringer av innføringen av aktivitetskravet i 2004 (Kann mfl. 2014 nevner at fraværet «sank dramatisk», uten tall) og eventuelle senere evalueringer av dialogmøtene, som forskermøtet i 2013 sa manglet
- eventuelle nyere studier av Hedmarksmodellen etter 2017

Svensk og finsk søk er ikke kjørt. Utfallene AAP og uføretrygd er bare dekket indirekte (oppbrukte sykepengerettigheter).

## Funn om oppskriften og kontrollene

5. **Valg på tittel ga én feil.** Godøy 2016 («Effects of an enforced activation policy on firm profits») så ut som en studie av Hedmarksmodellen, men handler om gradert sykmelding og bedriftenes overskudd. Den ble valgt og så tatt ut etter lesing. Regelen om å bygge kommentaren på sammendraget gjelder også raskt svar, men kandidatfila hadde ikke sammendrag for den.
6. **Kontroll 6 er tom i raskt svar.** `kandidater.jsonl` har bare de valgte kildene, så det finnes ingen utelatte sentrale kandidater å begrunne. Kontrollen består alltid. Forslag: i raskt svar bør tråden se gjennom `kilder/oversikt.tsv` etter beslektede kilder og begrunne dem som ikke tas med, eller oppskriften bør si at kontrollen ikke sier noe her.
7. **Kontroll 5 krever samme antall desimaler.** «−1,39» i svaret feilet mot `-1.390` i tabellen. Uklart om det er ønsket. Feilen ble rettet ved å skrive alle desimalene.
8. **Kontroll 5 fanger tall i parentes som ikke er funn** («før dag 15», antall artikler i en oversikt). De ble enten skrevet om eller lagt inn som egne rader. Greit, men raden «antall artikler i oversikten» er ikke et funn og havner i kildebibliotekets `funn.tsv`.
9. **Faktafeil i beskrivelsen fanges ikke av kontrollene.** Svaret sa først at sykmeldte født i *partallsår* fikk tiltaket. Riktig er oddetallsår. Feilen ble funnet ved manuell sjekk av metodeavsnittet. Det er samme type feil som innholdskontrollen er laget for. For raskt svar uten innholdskontroll bør tråden i det minste sjekke beskrivelsen av design og utvalg mot teksten for hver kilde.
10. **Kolonnen `gruppe`:** `UTTREKK.md` krever den, men eldre `estimater.tsv` (for eksempel `gradert-psykisk`) mangler den. Skriptene leser kolonnene med navn, så begge virker. Her er `gruppe` med.
11. **Antall kilder:** `sporsmal/oversikt.tsv` sier 13 (id-er i `valgt.txt`), svaret sier tolv (studier). Den publiserte versjonen uten tekst telles med i oversikten. Mindre viktig, men kan forvirre.

## Kjøremiljø

12. **Raskt svar trengte ikke Actions,** så køen i `sporsmal-sok.yml` (fire tråder samtidig, bare én ventende kjøring per gruppe) påvirket ikke denne testen.
13. **Mandat uten bestiller.** Mandatet ble skrevet av Claude etter fullmakt. Det gjorde det lett å kjøre raskt svar til tross for at krav 1 bare var delvis oppfylt. Med en bestiller ville regelen sagt at full løype skulle anbefales.
