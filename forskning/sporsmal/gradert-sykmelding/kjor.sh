# Steg 2: hent tekst for valgte kilder
# python3 -I forskning/verktoy/sporsmal_sok.py gradert-sykmelding --versjoner
# Norske kilder (7.11): vitenarkivet og Arbeid og velferd, med norske ord
# python3 -I forskning/verktoy/sporsmal_sok.py gradert-sykmelding --norsk 'gradert sykmelding' 'gradert sykemelding' 'graderte sykmeldinger' 'graderte sykemeldinger' 'gradert sykmeldt' 'gradert sykemeldt' 'gradert sykefravær' 'delvis sykmelding' 'delvis sykmeldt' 'delvis sykemeldt' 'aktiv sykmelding' 'aktivitetskravet'
# python3 -I forskning/verktoy/sporsmal_sok.py gradert-sykmelding --pdf
# Runde 2: følger nettsider til PDF, alle lokasjoner og Europe PMC
# Runde 3: tekst i lesefølge (uten -layout), så sitater over spalter kan kontrolleres
# Steg 3: følg referanser bakover og forover fra valgte kilder
# python3 -I forskning/verktoy/sporsmal_sok.py gradert-sykmelding --referanser 'partial sick leave' 'graded sick leave' 'part-time sick leave' 'partial sickness' 'graded sickness' 'active sick leave' 'partial return to work' 'graded return to work' 'gradert sykmelding' 'delvis sykmelding' 'deltidssjukskrivning' 'partial disability benefit'
# Runde 2 (7.11): tekst for nye kilder og nye referanser fra dem (metning)
# Runde 3 (7.11): tekst for åpne versjoner av Hernæs og Andrén
# Runde 4 (7.11): reserve via Europe PMC og vitenarkivet
# Runde 5 (7.11): norske studier fra FHI-oversikten
# Runde 6 (7.11): tekst for norske kilder
# Nye kataloger (9.11.2026): norsk søk på nytt med samme ord, nå også i Kudos og Navs bibliotek
# python3 -I forskning/verktoy/sporsmal_sok.py gradert-sykmelding --norsk 'gradert sykmelding' 'gradert sykemelding' 'graderte sykmeldinger' 'graderte sykemeldinger' 'gradert sykmeldt' 'gradert sykemeldt' 'gradert sykefravær' 'delvis sykmelding' 'delvis sykmeldt' 'delvis sykemeldt' 'aktiv sykmelding' 'aktivitetskravet'
# Full gjennomkjøring (9.11.2026), runde 1: svensk og finsk søk, og tekst for nye norske kilder i valgt.txt
# python3 -I forskning/verktoy/sporsmal_sok.py gradert-sykmelding --svensk 'partiell sjukskrivning' 'partiellt sjukskriven' 'partiellt sjukskrivna' 'deltidssjukskrivning' 'deltidssjukskriven' 'deltidssjukskrivna' 'partiell sjukpenning' 'graderad sjukskrivning' 'partiell sjukfrånvaro' 'deltidssjukfrånvaro'
# python3 -I forskning/verktoy/sporsmal_sok.py gradert-sykmelding --finsk 'osasairauspäiväraha' 'osasairauspäivärahan' 'osasairauspäivärahaa' 'osasairausloma' 'osittainen sairausloma' 'osittainen sairauspoissaolo' 'osittainen työhön paluu' 'partiell sjukdagpenning'
# python3 -I forskning/verktoy/sporsmal_sok.py gradert-sykmelding --pdf
# Runde 2 (9.11): tekst for nye kilder (Brage 2013 lagt inn for hånd, finske kilder) og åpne versjoner
# python3 -I forskning/verktoy/sporsmal_sok.py gradert-sykmelding --pdf
# python3 -I forskning/verktoy/sporsmal_sok.py gradert-sykmelding --versjoner
# Runde 3 (9.11): tekst for tre kilder fra det blinde utvalget
# python3 -I forskning/verktoy/sporsmal_sok.py gradert-sykmelding --pdf
# Ny gjennomkjøring 10.11.2026: tekst for nye kilder fra de blinde utvalgene C og D, og åpne versjoner
python3 -I forskning/verktoy/sporsmal_sok.py gradert-sykmelding --pdf
python3 -I forskning/verktoy/sporsmal_sok.py gradert-sykmelding --versjoner
