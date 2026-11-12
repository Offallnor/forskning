# Spørsmål: effekten av tilsyn fra arbeidsmiljømyndighetene på skader og etterlevelse
# Runde 1 (8.11): engelsk, norsk, svensk og finsk søk
# python3 -I forskning/verktoy/sporsmal_sok.py arbeidstilsyn-effekt --fra=2000 '"labor inspection"' '"labour inspection"' '"labor inspections"' '"labour inspections"' '"labour inspectorate"' '"labor inspectorate"' '"workplace inspection"' '"workplace inspections"' '"OSHA inspection"' '"OSHA inspections"' '"OSHA enforcement"' '"OSHA penalties"' '"safety inspections" injuries' '"safety inspection" workplace' '"health and safety inspections"' '"health and safety inspectors"' '"health and safety inspectorate"' '"occupational safety" enforcement' '"occupational health and safety" enforcement' '"occupational safety and health" enforcement' '"regulatory enforcement" occupational' '"inspections" "workplace injuries"' '"inspections" "occupational injuries"' '"inspection" "injury rates"' '"deterrence" "occupational safety"' '"work environment authority"' '"working environment authority"' '"mine safety" inspections' '"MSHA" inspections' '"Arbetsmiljöverket"' '"Arbejdstilsynet"' '"Arbeidstilsynet"' '"arbetsmiljöinspektion"' '"workplace safety" inspections' '"safety regulation" injuries enforcement'
# python3 -I forskning/verktoy/sporsmal_sok.py arbeidstilsyn-effekt --norsk 'Arbeidstilsynet' 'Arbeidstilsynets tilsyn' 'tilsyn med arbeidsmiljø' 'tilsyn med arbeidsmiljøet' 'arbeidsmiljøtilsyn' 'effekt av tilsyn' 'effekter av tilsyn' 'tilsynsvirksomhet' 'tilsynsmetodikk' 'Petroleumstilsynet' 'arbeidsulykker' 'arbeidsskader' 'reaksjoner fra tilsynet' 'overtredelsesgebyr' 'arbeidslivskriminalitet' 'sosial dumping'
# python3 -I forskning/verktoy/sporsmal_sok.py arbeidstilsyn-effekt --svensk --fra=2000 'Arbetsmiljöverkets tillsyn' 'Arbetsmiljöverkets inspektioner' 'tillsyn av arbetsmiljön' 'tillsyn av arbetsmiljö' 'arbetsmiljöinspektion' 'effekter av tillsyn' 'arbetsplatsolyckor' 'arbetsskador tillsyn'
# python3 -I forskning/verktoy/sporsmal_sok.py arbeidstilsyn-effekt --finsk --fra=2000 'työsuojelutarkastus' 'työsuojelutarkastukset' 'työsuojeluvalvonta' 'työsuojeluviranomainen' 'arbetarskyddstillsyn' 'arbetarskyddsinspektion' 'työtapaturmat valvonta'
# Runde 1 startet på nytt (kjøring 57 ble avbrutt i køen)
# Runde 2 (8.11): referanser fra første utvalg, og tekst for det som er valgt så langt
# python3 -I forskning/verktoy/sporsmal_sok.py arbeidstilsyn-effekt --referanser 'labor inspection' 'labour inspection' 'osha' 'msha' 'safety inspection' 'workplace inspection' 'inspectorate' 'regulatory enforcement' 'safety enforcement' 'health and safety enforcement' 'enforcement of occupational' 'inspections' 'tilsyn'
# python3 -I forskning/verktoy/sporsmal_sok.py arbeidstilsyn-effekt --pdf
# Runde 3 (8.11): tekst og åpne versjoner for nye kilder, deretter referanserunde 2
# python3 -I forskning/verktoy/sporsmal_sok.py arbeidstilsyn-effekt --pdf
# python3 -I forskning/verktoy/sporsmal_sok.py arbeidstilsyn-effekt --versjoner
# python3 -I forskning/verktoy/sporsmal_sok.py arbeidstilsyn-effekt --referanser 'labor inspection' 'labour inspection' 'osha' 'msha' 'safety inspection' 'workplace inspection' 'inspectorate' 'regulatory enforcement' 'safety enforcement' 'health and safety enforcement' 'enforcement of occupational' 'inspections' 'tilsyn'
# Runde 3 startet på nytt (kjøring 66 ble avbrutt i køen); blindt utvalg lagt til i valgt.txt
# (tom endring for å starte kjøringen)
# Runde 3 på nytt etter tidsavbrudd i køen (40 minutter for tre spørsmål)
# Runde 4: tekst for nye kilder og åpne versjoner fra referanserunde 2
# python3 -I forskning/verktoy/sporsmal_sok.py arbeidstilsyn-effekt --pdf
# Nye kataloger (9.11.2026): norsk søk på nytt med samme ord, nå også i Kudos og Navs bibliotek
python3 -I forskning/verktoy/sporsmal_sok.py arbeidstilsyn-effekt --norsk 'Arbeidstilsynet' 'Arbeidstilsynets tilsyn' 'tilsyn med arbeidsmiljø' 'tilsyn med arbeidsmiljøet' 'arbeidsmiljøtilsyn' 'effekt av tilsyn' 'effekter av tilsyn' 'tilsynsvirksomhet' 'tilsynsmetodikk' 'Petroleumstilsynet' 'arbeidsulykker' 'arbeidsskader' 'reaksjoner fra tilsynet' 'overtredelsesgebyr' 'arbeidslivskriminalitet' 'sosial dumping'
