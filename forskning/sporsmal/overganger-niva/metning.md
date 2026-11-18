# Metning: overgangene mellom nivåene

Skrevet 18.11.2026 etter referanserunde 2. Foreløpig vurdering, før de blinde utvalgene.

## Rundene

| Runde | Nye kandidater | Siktet | Beholdt i siktingen | Valgt i kategori 1–5 | Av dem kategori 1–4 |
|---|---|---|---|---|---|
| Søk (engelsk, norsk, svensk, finsk) | 3 987 | 3 987 | 2 447 | 555 | – |
| Referanserunde 1 | 4 354 | 4 354 | 3 472 | 673 | – |
| Referanserunde 2 | 14 368 | 2 795 (filtrert, se under) | 1 692 | 454 | 422 |
| Utfyllende norsk søk | 107 | lest i tråden | – | 24 | – |

Innstrammingen 18.11.2026 tok ut 318 kilder fra land utenfor Norden som ikke er harmoniserte sammenligninger (se `kriterier.md` og `utelatt.tsv`). Utvalget er 1 388 kilder.

## Vurdering

- **Krav 1 (under 5 prosent av de nye kandidatene i siste runde i kategori 1–4):** 422 av 14 368 nye kandidater i referanserunde 2, eller 2,9 prosent. Kravet er formelt oppfylt. Men 11 573 av kandidatene ble filtrert bort med skript før siktingen fordi de lå utenfor Norden og ikke så ut som sammenligninger på tvers av land. Av de 2 795 som ble siktet, oppfylte 422 kategori 1–4, eller 15 prosent. Målt mot kandidatene som faktisk kunne velges, er utvalget ikke mettet.
- **Krav 2 (blindt utvalg finner ikke nye kilder i kategori 1–3):** ikke oppfylt etter blindt utvalg A (Opus, 2 250 nordiske kandidater i fem bolker). Det valgte 649 kilder, og 577 av dem var allerede valgt. Av de 72 nye var 42 i kategori 1–3. 19 er tatt inn, merket «blindt utvalg A» i `valgt.txt`: fem norske (blant dem NOU-en om videregående og kandidatundersøkelsen for fagskolen) og ellers nordiske studier om fagskole og yrkesrettet høyere utdanning, studiestøtte og konjunkturer. De andre 23 er tatt ut fordi forklaringen er helse eller barnevern, som ikke er blant driverne, eller fordi de er nye utgaver av serier som allerede er valgt. En nordisk oversikt var feilaktig tatt ut ved innstrammingen og er lagt tilbake. Blindt utvalg B (Sonnet, samme bolker) valgte 493 kilder. 424 av dem var allerede valgt, også de 19 fra utvalg A som det fant. Av de 69 nye var 37 i kategori 1–3, og sju av dem hadde utvalg A også funnet og vurdert. 14 er tatt inn, merket «blindt utvalg B»: norske registerstudier om innvandrerbakgrunn, bosted og overgangsløp, svensk påbygging fra komvux og konjunkturer, og harmoniserte sammenligninger av yrkesopplæring og arbeidsmarkedsutfall. Begge blinde utvalg er lagret i `valgt-blind.tsv`.
- **Samlet vurdering:** Etter løypas krav er utvalget ikke mettet. Funnene fra de blinde utvalgene er likevel stadig mer perifere: det meste som ikke er tatt inn, gjelder helse, barnevern og flyktninger som voksne, og de to modellene finner i stor grad de samme kildene. Greinene 1 og 3 og fagskolen får nesten ingenting fra noen runde. Som løypa sier, kjøres en referanserunde til fra de 33 nye kildene (runde 5 i `kjor.sh`), og et blindt utvalg på de nye kandidatene fra den. Utvalget er 1 421 kilder.
