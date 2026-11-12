# Sammenligning av første og andre uttrekk: effekt av arbeidstilsyn (9.11.2026)

Første uttrekk (`estimater.tsv`) og andre uttrekk (`estimater-b.tsv`, annen modell) ble gjort uavhengig, i tre grupper hver (oversikter og sterkest design, norske og nordiske kilder, register- og panelstudier). Begge dekker alle 113 kildene i utvalget. Begge besto kontroll 2–4 i sine egne arbeidsområder.

## Tall

- 69 estimater er funnet i begge uttrekkene, med samme verdi.
- 30 tall står bare i første uttrekk og 23 bare i andre. Nesten alle er ulike valg av hvilke tall som er hovedresultat (flere undergrupper, spenn, beskrivende tall), ikke uenighet om verdien.
- Ingen tall i andre uttrekk mangler i kilden. Ingen tall i de to uttrekkene motsier hverandre for samme utfall.

## Tall fra andre uttrekk som er flyttet til `estimater.tsv`

Merket «(fra andre uttrekk)» i utfall:

- Dyreborg m.fl. 2022 (Campbell): samlet effekt av håndheving på ulykker ved lang oppfølging (RR 0,77) og ved kort oppfølging (0,86). Første uttrekk hadde bare tallene oversikten gjengir fra enkeltstudier.
- Lee og Taylor 2019: nedgang i dødsfall etter programmert tilsyn (56 prosent).
- Lafuente og Martínez Daza 2019: elastisiteten mellom tilsyn per arbeidstaker og ulykkesrate (−0,1774). Første uttrekk utelot den fordi minustegnet i kilden ikke ble lest (se `kaldtest.md`).
- Haviland m.fl. 2012 og Ko, Mendeloff og Gray 2010: øvre grense i spennene i sammendraget.
- Malta 2024: årlig nedgang i dødsulykker.
- Den svenske støykampanjen 2008: antall tiltak i virksomheter uten tilsyn (sammenligningsgruppen).
- Garshol m.fl. 2023: sykedager for muskel-skjelett- og psykiske diagnoser hver for seg.

## Ikke flyttet

- Selvrapporterte vurderinger fra den svenske effektevalueringen av sanksjonsavgifter (andel som sier avgiften fikk dem til å forebygge). Meninger regnes ikke som funn etter `UTTREKK.md`.
- Tall som STAMI-oversikten og den svenske evalueringen gjengir fra Gray og Mendeloff og fra Haviland m.fl. De opprinnelige studiene er hentet ut direkte der de har tekst eller sammendrag.
- Antall studier i evidens- og hullkartet (ikke et funn).

## Fortegn

Begge uttrekkene fikk problemer med minustegn skrevet med mellomrom foran tallet («− 2.91») i Garshol m.fl. 2025, og førte tallene som positive. Kontrollskriptet er rettet (`tall()` leser nå minustegn med mellomrom), og radene er ført med riktig fortegn i begge filene.

## Tillegg 9.11: fire kilder med ny fulltekst

Li og Singleton 2017 (arbeidsnotat), Cochrane-oversikten om skader i bygg (2018), Jakobsen m.fl. 2025 og Davis 2004 fikk tekst i siste runde og ble hentet ut på nytt i begge uttrekkene. Radene erstatter radene fra sammendraget. De to uttrekkene fant de samme hovedtallene. Første uttrekk tok i tillegg med virkningen av regulering i Cochrane-oversikten og to undergrupper hos Li og Singleton, andre uttrekk et tall Li og Singleton gjengir fra Levine m.fl. 2012 (ikke flyttet, fordi studien er hentet ut direkte).
