REM     Long Range Plan (LRP)
C:
cd C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction
PERL tu_automate.pl -f C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction\xml\batchrun-parameter_2030_LRP.xml > C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction\log\2030perl_LRP.log

REM     Constant 1997-Based Transportation Network
C:
cd C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction
PERL tu_automate.pl -f C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction\xml\batchrun-parameter_2030_const.xml > C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction\log\2030perl_const.log

REM     LRP, Omitting Bangerter Highway
C:
cd C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction
PERL tu_automate.pl -f C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction\xml\batchrun-parameter_2030_highway.xml > C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction\log\2030perl_highway.log

REM     LRP, Omitting South LRT Extension
C:
cd C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction
PERL tu_automate.pl -f C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction\xml\batchrun-parameter_2030_transit.xml > C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction\log\2030perl_transit.log

REM     LRP, Increasing Downtown Parking Fees
C:
cd C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction
PERL tu_automate.pl -f C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction\xml\batchrun-parameter_2030_parking.xml > C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction\log\2030perl_parking.log

REM     LRP, Adding an Urban Growth Boundary
C:
cd C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction
PERL tu_automate.pl -f C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction\xml\batchrun-parameter_2030_UGB.xml > C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction\log\2030perl_UGB.log

REM     LRP, Adding a Vacancy Rate variable to the Land Price model with a coefficient of -1
C:
cd C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction
PERL tu_automate.pl -f C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction\xml\batchrun-parameter_2030_lpvr1.xml > C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction\log\2030perl_lpvr1.log

REM     LRP, Adding a Vacancy Rate variable to the Land Price model with a coefficient of -0.5
C:
cd C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction
PERL tu_automate.pl -f C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction\xml\batchrun-parameter_2030_lpvr2.xml > C:\eclipse\workspace\Scripts\WFRC\travel_model_urbansim_interaction\log\2030perl_lpvr2.log

