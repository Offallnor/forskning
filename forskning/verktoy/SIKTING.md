# Grov sikting før de blinde utvalgene

Brukes i steg 2 punkt 3 i `forskning/LOYPE.md` når mappen har mer enn om lag 2 000 kandidater. Hver bolk fra `sporsmal_sikting.py --del` siktes av én egen kjøring med Haiku (`claude-haiku-5-5`). Kjøringene kan gå samtidig.

Testet 10.11.2026. I aktivitetskravet (5 718 kandidater) beholdt Haiku 123 av 124 sterke kilder. Opus-utvalget etter siktingen fant 79 prosent av de sterke kildene, mot 63 prosent med alle kandidatene, fordi Opus ikke rekker å lese alle sammendragene i en lang liste. I gradert sykmelding (754 kandidater) ga siktingen ingen gevinst. Den kostet om lag 3,8 millioner Haiku-tokens for 5 718 kandidater.

## Prompt

Erstatt `<MAPPE>` med stien til bolken (for eksempel `…/sikting/b01`). Prompten er den som ble testet, med to tillegg etter testen: årstall og design er ikke grunn til å forkaste, og id-ene kopieres med skript. I testen forkastet seks av 20 kjøringer alt fra før 2000, og andelen som ble beholdt, varierte fra 30 til 53 prosent mellom bolkene.

```
Du gjør en grov sikting av kandidater til et forskningsspørsmål. Les bare de to filene i <MAPPE>/ — ikke noe annet sted på disken, ikke git, ikke nettet. Hjelpefiler skriver du bare i den samme mappen. Bygg ikke på egen kjennskap til litteraturen: vurder bare det som står i filene.

Filer:
- kriterier.md: mandat og kriterier (tiltak, utfall, designhierarki 1–5, land)
- kandidater.tsv: en bolk kandidater med id, år, type, kilde, oversikt (True = ser ut som en oversikt), land, tittel og sammendrag (avkortet; tomt når det mangler)

Oppgave: avgjør for HVER rad om kandidaten skal gå videre til det egentlige utvalget («behold») eller sorteres bort nå («forkast»). Dette er bare et grovfilter. Et senere steg velger strengt etter kriteriene, men det ser aldri det du forkaster. Derfor:
- Behold alt som kan handle om tiltaket eller ordningen i kriterier.md, også under andre navn og i andre land, og også når det bare er en del av temaet (for eksempel brede oversikter om tiltak for sykmeldte eller retur til arbeid).
- Behold ved tvil. Behold når sammendraget mangler og tittelen kan gjelde temaet.
- Forkast bare det som klart ikke handler om tiltaket, for eksempel et annet felt, en ordning kriteriene holder utenfor, ren metodelitteratur eller bare holdninger og erfaringer uten noe om effekt.
- Årstall, land og design er ikke grunn til å forkaste. Det avgjør det strenge utvalget.

Les hele sammendraget for hver rad, ikke bare tittelen eller starten. Skriv <MAPPE>/sikting.tsv med kolonnene id, beslutning, grunn (tabulator, overskriftsrad, én rad per kandidat, grunn på høyst 15 ord som gjelder den raden). Kopier id-ene fra kandidater.tsv med et skript, ikke skriv dem av. Alle rader i kandidater.tsv skal ha en rad. Avslutt med en kort melding: antall behold og forkast.
```

## Etterpå

- Kjør `sporsmal_sikting.py <mappe> --samle <arbeidsmappe>`. Les varslene: forkortede id-er rettes når de er entydige, og kandidater uten beslutning regnes som beholdt.
- Sjekk i loggen til hver kjøring at modellen var Haiku, og at den bare åpnet sin egen bolk.
- `sikting.tsv` i spørsmålets mappe er ikke en begrunnelse for `utelatt.tsv`. Grunnene er grove, og mange kjøringer skriver samme grunn for alle de forkastede.
