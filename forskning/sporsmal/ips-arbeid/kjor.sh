# Spørsmål: effekten av individuell jobbstøtte (IPS) på ordinært arbeid for personer med psykiske lidelser eller rusproblemer
# Runde 1 (8.11): engelsk, norsk, svensk og finsk søk
# python3 -I forskning/verktoy/sporsmal_sok.py ips-arbeid --fra=2000 '"individual placement and support"' '"individual placement" employment' '"supported employment" mental' '"supported employment" "mental illness"' '"supported employment" psychiatric' '"supported employment" schizophrenia' '"supported employment" psychosis' '"supported employment" "substance use"' '"supported employment" addiction' '"supported employment" depression' '"supported employment" "randomized"' '"supported employment" "randomised"' '"supported employment" "systematic review"' '"supported employment" "meta-analysis"' '"supported employment" veterans' '"supported employment" youth' '"supported employment" "young adults"' '"vocational rehabilitation" "severe mental illness"' '"vocational rehabilitation" schizophrenia' '"vocational rehabilitation" "mental illness" randomized' '"competitive employment" "mental illness"' '"competitive employment" psychiatric' '"competitive employment" schizophrenia' '"employment" "first episode psychosis"' '"employment" "first-episode psychosis"' '"place and train"' '"place-then-train"' '"IPS" employment' '"individuell jobbstøtte"' '"individanpassat stöd"' '"work" "severe mental illness" randomized'
# python3 -I forskning/verktoy/sporsmal_sok.py ips-arbeid --norsk 'individuell jobbstøtte' 'individuell jobbstøtte (IPS)' 'IPS-metoden' 'IPS ung' 'supported employment' 'jobbspesialist' 'jobbmestrende oppfølging' 'arbeid og psykisk helse' 'psykiske lidelser og arbeid' 'alvorlige psykiske lidelser' 'rusproblemer og arbeid' 'arbeidsrettet rehabilitering' 'arbeidsrettet oppfølging' 'arbeidsinkludering psykisk' 'Jobbfast'
# python3 -I forskning/verktoy/sporsmal_sok.py ips-arbeid --svensk --fra=2000 'individanpassat stöd till arbete' 'IPS-modellen' 'supported employment' 'psykisk funktionsnedsättning och arbete' 'arbetslivsinriktad rehabilitering psykisk' 'psykiska funktionsnedsättningar arbete'
# python3 -I forskning/verktoy/sporsmal_sok.py ips-arbeid --finsk --fra=2000 'yksilöllinen työhönvalmennus' 'IPS-malli' 'tuettu työllistyminen' 'sijoita ja valmenna' 'mielenterveyskuntoutujien työllistyminen' 'individanpassat stöd till arbete'
# Runde 2 (8.11): referanser fra første utvalg
# python3 -I forskning/verktoy/sporsmal_sok.py ips-arbeid --referanser 'individual placement' 'supported employment' 'IPS' 'jobbstøtte'
# Runde 3 (8.11): referanser fra oppdatert utvalg
# python3 -I forskning/verktoy/sporsmal_sok.py ips-arbeid --referanser 'individual placement' 'supported employment' 'IPS' 'jobbstøtte'
# Runde 4 (8.11): tekst og åpne versjoner for utvalget etter referanserunde 2
# python3 -I forskning/verktoy/sporsmal_sok.py ips-arbeid --pdf
# python3 -I forskning/verktoy/sporsmal_sok.py ips-arbeid --versjoner
# Runde 5 (8.11): referanser fra utvalget etter det blinde utvalget (metning), deretter tekst og versjoner
# python3 -I forskning/verktoy/sporsmal_sok.py ips-arbeid --referanser 'individual placement' 'supported employment' 'IPS' 'jobbstøtte'
# python3 -I forskning/verktoy/sporsmal_sok.py ips-arbeid --pdf
# python3 -I forskning/verktoy/sporsmal_sok.py ips-arbeid --versjoner
# Runde 5 på nytt (9.11): forrige kjøring ble avbrutt i køen
# Runde 6 (9.11): tekst og versjoner på nytt (runde 5 nådde tidsgrensen etter referansene og deler av teksten)
# python3 -I forskning/verktoy/sporsmal_sok.py ips-arbeid --pdf
# python3 -I forskning/verktoy/sporsmal_sok.py ips-arbeid --versjoner
# Nye kataloger (9.11.2026): norsk søk på nytt med samme ord, nå også i Kudos og Navs bibliotek
# python3 -I forskning/verktoy/sporsmal_sok.py ips-arbeid --norsk 'individuell jobbstøtte' 'individuell jobbstøtte (IPS)' 'IPS-metoden' 'IPS ung' 'supported employment' 'jobbspesialist' 'jobbmestrende oppfølging' 'arbeid og psykisk helse' 'psykiske lidelser og arbeid' 'alvorlige psykiske lidelser' 'rusproblemer og arbeid' 'arbeidsrettet rehabilitering' 'arbeidsrettet oppfølging' 'arbeidsinkludering psykisk' 'Jobbfast'
# Raskt tillegg (9.11.2026): tekst for nye kilder fra Kudos og Navs bibliotek
python3 -I forskning/verktoy/sporsmal_sok.py ips-arbeid --pdf
