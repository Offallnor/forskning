# Spørsmål: effekten av arbeidsgivers og arbeidstakers egenandel ved sykefravær på sykefravær og frafall
# Steg 1: søk
# python3 -I forskning/verktoy/sporsmal_sok.py egenandel-sykefravaer '"waiting day" sick' '"waiting days" sick' '"waiting period" "sick leave"' '"waiting period" "sickness absence"' '"replacement rate" "sick leave"' '"replacement rate" "sickness absence"' '"replacement rate" "sickness"' '"sick pay" incentives' '"sick pay" "employer"' '"employer-paid sick"' '"employer co-payment"' '"co-payment" sick' '"experience rating" sickness' '"experience rating" disability' '"sickness insurance" generosity' '"sick leave" "benefit level"' '"sickness benefit" "benefit level"' '"moral hazard" "sick leave"' '"moral hazard" "sickness absence"' '"karensdag"' '"egenandel" sykefravær' '"arbeidsgiverperiode"'
# Steg 2: hent tekst for valgte kilder (eldre runde)
# python3 -I forskning/verktoy/sporsmal_sok.py egenandel-sykefravaer --pdf
# Kaldtest av LOYPE.md (7.11): norsk søk og første runde med referanser
# python3 -I forskning/verktoy/sporsmal_sok.py egenandel-sykefravaer --norsk 'karensdag' 'karensdager' 'arbeidsgiverperiode' 'arbeidsgiverperioden' 'sykelønn' 'sykelønnsordningen' 'sykepengeordningen' 'kompensasjonsgrad' 'dekningsgrad' 'medfinansiering' 'egenandel' 'egenbetaling' 'refusjon av sykepenger' 'sykelønnsfelle'
# python3 -I forskning/verktoy/sporsmal_sok.py egenandel-sykefravaer --referanser 'sick pay' 'sickness benefit' 'sickness insurance' 'sick leave insurance' 'sick leave pay' 'waiting day' 'waiting period' 'replacement rate' 'benefit level' 'experience rating' 'employer co-payment' 'co-payment' 'karensdag' 'sjuklön' 'sykelønn' 'arbeidsgiverperiode' 'moral hazard'
# Runde 2 (7.11): referanser fra nytt utvalg (metning), åpne versjoner og tekst
# python3 -I forskning/verktoy/sporsmal_sok.py egenandel-sykefravaer --referanser 'sick pay' 'sickness benefit' 'sickness insurance' 'sick leave insurance' 'sick leave pay' 'waiting day' 'waiting period' 'replacement rate' 'benefit level' 'experience rating' 'employer co-payment' 'co-payment' 'karensdag' 'sjuklön' 'sykelønn' 'arbeidsgiverperiode' 'moral hazard'
# python3 -I forskning/verktoy/sporsmal_sok.py egenandel-sykefravaer --pdf
# python3 -I forskning/verktoy/sporsmal_sok.py egenandel-sykefravaer --versjoner
# Runde 3 (7.11): tekst for kilder fra runde 2 og åpne versjoner
# python3 -I forskning/verktoy/sporsmal_sok.py egenandel-sykefravaer --pdf
# Runde 4 (7.11): tekst for kilder fra det blinde utvalget
# python3 -I forskning/verktoy/sporsmal_sok.py egenandel-sykefravaer --pdf
# python3 -I forskning/verktoy/sporsmal_sok.py egenandel-sykefravaer --versjoner
# Runde 5 (7.11): tekst for åpne versjoner fra runde 4
# python3 -I forskning/verktoy/sporsmal_sok.py egenandel-sykefravaer --pdf
# Nye kataloger (9.11.2026): norsk søk på nytt med samme ord, nå også i Kudos og Navs bibliotek
# python3 -I forskning/verktoy/sporsmal_sok.py egenandel-sykefravaer --norsk 'karensdag' 'karensdager' 'arbeidsgiverperiode' 'arbeidsgiverperioden' 'sykelønn' 'sykelønnsordningen' 'sykepengeordningen' 'kompensasjonsgrad' 'dekningsgrad' 'medfinansiering' 'egenandel' 'egenbetaling' 'refusjon av sykepenger' 'sykelønnsfelle'
# Raskt tillegg (9.11.2026): tekst for nye kilder fra Kudos og Navs bibliotek
python3 -I forskning/verktoy/sporsmal_sok.py egenandel-sykefravaer --pdf
