# Kaldtest: full løype på et felt med mange RCT-er (IPS og arbeid)

8.11.2026. Del av testrunden med fire spørsmål i egne tråder som deler køen i `sporsmal-sok.yml`. Mandatet ble utformet av Claude etter fullmakt fra bestilleren.

## Funn om oppskriften

Merket **høy** når det kan gi feil eller ufullstendig svar, **middels** når det koster tid eller krever skjønn oppskriften ikke gir, **lav** for små ting.

### Køen i Actions

1. **Høy.** `sporsmal-sok.yml` har `concurrency` uten `cancel-in-progress`, men GitHub beholder bare én ventende kjøring per gruppe. Når to tråder pusher mens en runde kjører, avbrytes den eldste ventende kjøringen (status «cancelled»). Workflowen kjører bare `kjor.sh` som er endret i sin egen push, så den avbrutte runden kjøres aldri. Skjedde kl. 23.03 med runde 1 for `arbeidstilsyn-effekt`, tre sekunder etter at `unge-ufore` pushet. LOYPE.md sier at «en ny push venter til den forrige er ferdig», som ikke stemmer når flere enn to venter. Forslag: la workflowen kjøre alle `kjor.sh` som er endret siden siste «Spørsmålssøk: resultat», eller skriv i LOYPE.md at tråden må sjekke kjøringen med `actions_list` og pushe på nytt ved «cancelled».

### Søk og utvalg

2. **Høy.** Feltet er stort: søket ga 1855 kandidater fra OpenAlex (1631 nevner IPS eller supported employment i tittel eller sammendrag), 391 norske, 417 svenske og 492 finske. Referanserunde 1 ga 2324 refererte kilder, 1559 av dem nye. Oppskriften sier at norske kandidater skal leses i sin helhet og at resten sorteres etter ord fra mandatet. Med så mange IPS-treff er ord fra mandatet ikke nok til å sortere. Jeg filtrerte i to trinn: IPS-ord og designord (randomi, trial, meta-analy, review, register, cost-effect) i tittel eller sammendrag, og titler med IPS-ord uten sammendrag. Det ga 434 og 144 titler, som ble lest. Forslag: skriv et slikt designfilter inn i oppskriften for felt med mange kandidater, og la det blinde utvalget fange resten.
3. **Middels.** Kilder fra vitenarkivet som finnes i OpenAlex fra før (kolonnen `finnes_fra_for` i `norske-kandidater.tsv`), kommer ikke inn i `kandidater.jsonl` med vitenarkivets id. Fire av mine første id-er i `valgt.txt` var derfor ugyldige og måtte byttes til OpenAlex-id-en. Oppskriften sier ikke dette. Forslag: én setning i steg 2 om å bruke id-en i `finnes_fra_for` når den er fylt ut.
4. **Lav.** Jeg skrev id-er fra vitenarkivet av fra en avkortet visning (46 tegn) og fikk feil id-er. Fanget av en egen sjekk mot `kandidater.jsonl` før push. Oppskriften advarer mot å skrive av, men kontrollen kommer først etter neste runde. Forslag: et lite skript som sjekker `valgt.txt` mot `kandidater.jsonl` før push.
5. **Middels.** Uttrykkene for referansesøket må velges med omhu i et stort felt. Jeg tok bort «vocational rehabilitation» og «competitive employment», som ville sluppet inn mye om tradisjonell attføring og prediktorer for arbeid, og beholdt bare IPS-uttrykkene. Da er det regelen om to pekere som fanger studier som bruker andre ord.
6. **Middels.** Det blinde utvalget (133 kilder, 95 felles med første utvalg) fant 38 kilder jeg ikke hadde, blant dem nye kilder i kategori 1–3: Hartford-forsøket, flersentersforsøket i Australia, et kanadisk forsøk ved tidlig psykose, et spansk forsøk, samlede analyser av fire RCT-er for unge voksne og for mottakere av uføreytelser, og en kostnadsanalyse fra 2002. Flere av dem sto i min filtrerte liste, men falt ut fordi jeg leste titler i et felt med hundrevis av like titler. Det blinde utvalget er igjen den viktigste kontrollen. Krav 2 i metningsregelen var dermed ikke oppfylt, og det ble kjørt en tredje referanserunde.
7. **Lav.** Min egen push av runde 5 avbrøt min ventende runde 4 (samme mekanisme som funn 1). Det gjorde ikke noe her fordi runde 5 hadde de samme kommandoene, men en tråd som pusher to ganger mens køen er opptatt, mister den første runden uten å merke det.
8. **Høy.** Runde 5 ble også avbrutt i køen, denne gangen av en annen tråds push. Tre av mine fem runder er så langt avbrutt. Med fire tråder som deler køen, er avbrudd det vanlige, ikke unntaket. Jeg la inn en kommentarlinje og pushet på nytt.
   Rettet av en annen tråd samme natt: `sporsmal-sok.yml` (main 79b80aa) tar nå igjen avbrutte runder ved å sammenligne `kjor.sh` med `kjor.sh.kjort`.
9. **Høy.** Runde 5 for IPS (referanser for 169 kilder, tekst og versjoner) nådde tidsgrensen på 40 minutter i Actions, og alt som var hentet gikk tapt fordi lagringen kom etter jobben. Rettet av en annen tråd (be37e45): 120 minutter og lagring også ved tidsavbrudd. Store felt bør likevel dele referanser og tekst i hver sin runde.
10. **Høy.** Runde 5 nådde også den nye tidsgrensen (to timer, kjøring 74, som tok igjen tre avbrutte runder fra tre tråder). Referansene for 169 kilder (3078 rader) og tekst for 73 av 169 kilder ble lagret, men ikke `pdf-logg.tsv` og `versjoner.tsv`. Med lagring ved tidsavbrudd gikk ikke arbeidet tapt, men det tok fire timer fra push til delresultat. Runde 6 kjører tekst og versjoner for resten.

### Uttrekk og kontroll

11. **Lav.** `sporsmal_kopi.py` skriver en tom `estimater.tsv` uten kolonnen `gruppe`, som `UTTREKK.md` krever. Rettet for hånd i kopiene.

12. **Middels: feil tekstfil for en kilde.** Tekstfilen for W3096495837 (FHI 2017 på engelsk) inneholder en annen artikkel (Witte mfl. 2022, scoping review i Work). pdf-loggen varslet ikke. Det samme gjaldt W4412642570 (Rognli 2025), der tekstfilen er analyseplanen for forsøket, ikke artikkelen. Uttrekket brukte sammendraget i begge tilfeller. Forslag: sjekk at tittelen i metadata finnes i de første sidene av teksten, og varsle SJEKK DOKUMENT ellers.
13. **Lav: KI uten innledende null.** W2892072419 skriver KI som «[.97, 1.95]». Kontrollen leser «.97» som 97, så KI-feltene måtte stå tomme. Forslag: kontroll 3 bør godta tall som begynner med punktum.
14. **Lav: land satt på tittel ved utvalget.** To kilder som ble ført som nordiske i valgt.txt, var nederlandsk (W4220994326) og engelsk (W7170865677). Uttrekket rettet landet. Feilen var min ved utvalget, men løypa har ingen landsjekk før uttrekket.
15. **Middels: svar 429 fra OpenAlex logges ikke.** `hent()` i sporsmal_sok.py prøvde fem ganger ved 429 og ga så opp uten melding, så en brukt opp kvote ville bare synes som manglende treff. Rettet: 429 skrives nå i loggen. Skymiljøet når ikke OpenAlex (403 fra proxyen), så kvoten kan bare sjekkes i Actions-loggen. Mest tid i runde 5 gikk til døde nettsider (fem forsøk à ett minutt per adresse), ikke til OpenAlex.
16. **Middels: `--versjoner` gir beslektede arbeider, ikke versjoner.** Av 61 rader i `versjoner.tsv` var ingen en åpen versjon av samme artikkel. Treffene var andre artikler fra samme forsøk, kommentarer og fagfellevurderinger (sju rader for én artikkel i Cambridge Prisms). Ingen ble lagt til.
17. **Lav: innhentingen av avbrutte runder kjørte gamle linjer på nytt.** Kjøringen som tok igjen IPS-runden, laget `referanser-4.tsv`, identisk med `referanser-3.tsv`. Fila er slettet.
18. **Middels: grupper til uttrekket ble satt for hånd, og noen kilder falt mellom.** FHI 2017 på norsk (W2738957630) hadde tekst, men kom ikke med i noen gruppe, og fire oversikter med tall i sammendraget var heller ikke med. De ble funnet først da kildene uten rader i `estimater.tsv` ble listet. Forslag: kontroll 6 eller kildeoversikt.py bør liste valgte kilder uten rad i `estimater.tsv` før svaret skrives.
19. **Middels: døde nettsider tar mye av tiden i Actions.** Hver adresse som gir URLError, prøves fem ganger med opptil ett minutt per forsøk. I runde 5 gikk minst en halv time til fire adresser. Forslag: gi opp etter ett forsøk ved URLError på samme vert, eller kortere tidsavbrudd for andre forsøk.

## Oppsummering

- **Resultat:** svar med 170 kilder (74 med tekst, 76 bare sammendrag, 20 bare registrert), 250 rader i uttrekket, kontroll 0 feil av 3 091. Innholdskontrollen fant fire mangler ved forbehold (frafall, én kommune, avtagende effekt, unge på kort sikt), ingen feil i retning. Alle er rettet.
- **Metning:** krav 1 holdt fra referanserunde 2. Krav 2 holdt ikke i første omgang (det blinde utvalget fant 38 kilder), og en tredje runde med nytt blindt utvalg fant fortsatt én oversikt. Metningsregelen fungerer som varsel i et stort felt, men det blinde utvalget er den viktigste kontrollen.
- **Tid:** fra mandat kl. 22 8.11 til svar kl. om lag 06 9.11. Om lag halvparten av tiden gikk til å vente på køen og tidsavbrudd i Actions (runde 4 og 5 avbrutt eller tidsavbrutt fire ganger).
- **Underagenter:** seks uttrekksagenter (tre på samme modell som tråden og tre på Sonnet) og én blind leser, til sammen om lag 1,5 millioner tokens.
