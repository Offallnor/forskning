# Metning: aktivitetskravet og tidlig oppfølging i sykefraværet

Vurdert 10.11.2026 etter tre referanserunder og tre blinde utvalg. Utvalget er vurdert mot de innsnevrede kriteriene fra 9.11.2026 (krav og oppfølging som ordning, se `kriterier.md`).

## Krav 1: under 5 prosent nye i kategori 1–4 i siste referanserunde

- **Referanser runde 1** (`referanser-1.tsv`, 2084 rader) ble kjørt med brede uttrykk og ga for mange kandidater til å vurdere metning. Den er brukt som kilde til utvalget, ikke som metningsmål.
- **Referanser runde 2** (`referanser-3.tsv`, fordi `referanser-2.tsv` er tom etter en kjøring som stoppet på OpenAlex-kvoten): 1503 rader, 813 nye kandidater. 16 av dem er i kategori 1–4, om lag 2 prosent.
- **Referanser runde 3** (`referanser-4.tsv`), fulgt fra de 17 kildene fra blindt utvalg 2: 132 rader, 66 nye. Det blinde utvalget (`valgt-blind-3.tsv`) fant én i kategori 3 og én i kategori 4, om lag 3 prosent.

Krav 1 er oppfylt i de to siste rundene.

## Krav 2: det blinde utvalget finner ikke nye kilder i kategori 1–3

- **Blindt utvalg 1** (`valgt-blind.tsv`, 167 kilder): 64 kilder ble tatt inn.
- **Blindt utvalg 2** (`valgt-blind-2.tsv`, 25 av de 813 nye fra runde 2): 13 i kategori 1–3. 17 kilder ble tatt inn, blant dem svenske forsøk med kontroll av legers sykmeldinger og saksbehandlerscreening, to oversikter fra 2025 og OECD-rapportene. Kravet var ikke oppfylt, så runde 3 ble kjørt fra disse kildene.
- **Blindt utvalg 3** (`valgt-blind-3.tsv`, 4 av de 66 nye fra runde 3): én i kategori 3, en svensk studie av utvidet kontroll av tillfällig föräldrapenning med sykefravær som sideutfall (W3185498031). Den var allerede tatt inn etter gjennomgangen av runde 3. Den finske registerstudien av koordinert retur etter ortopedisk kirurgi (kategori 4) er utelatt etter innsnevringen, og den tyske strategien i pensjonstrygden (kategori 5) er utelatt fordi den mangler kontrollgruppe.

Krav 2 er oppfylt i siste runde.

## Svakheter

- **Første utvalg var for smalt.** Gjennomgangen av sentrale kandidater (kontroll 6) fant 111 oversikter og forsøk som første utvalg hadde oversett, og blindt utvalg 2 fant 17 til. Metning ble nådd først etter tre referanserunder. Det tyder på at første utvalg på tittel undervurderer bredden når spørsmålet har mange navn på samme ordning (aktivitetskrav, tidsgrenser, kontrollpunkter, avstemmingsmøter).
- **Referansesøket følger bare OpenAlex-kilder.** Norske, svenske og danske rapporter uten OpenAlex-id kan ikke følges med skriptet. Referanselistene i de norske oversiktene er derfor lest for hånd (se `utvalg.md`), og én norsk studie ble funnet på den måten.
- **Danske og svenske forvaltningsrapporter** er funnet ved søk for hånd og i LIBRIS, men mange har ikke åpen tekst (se `mangler.md`). Metningen gjelder det som kan søkes, ikke grålitteraturen.
- **Runde 3 ble først gjennomgått av tråden** og så av det blinde utvalget. Det blinde utvalget fikk ikke se hva tråden hadde valgt, men begge valgte den samme svenske kilden.
