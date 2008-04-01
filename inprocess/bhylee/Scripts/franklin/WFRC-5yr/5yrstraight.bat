REM Run UrbanSim from 1997 to 2003
cd C:\Program Files\UrbanSim
urbansim.bat C:\eclipse\workspace\scripts\franklin\WFRC-5yr\WFRC_1997_parameters_5yr_2003_straight.xml


REM Run basic set of indicators and put tables in the output database

cd C:\eclipse\workspace\scripts\franklin\WFRC-5yr\
perl ..\PERL\sql.pl Z-1-urbansim_indicators_straight.sql


REM Create short-name tables of zone and grid level aggregations for GIS use

cd C:\eclipse\workspace\scripts\franklin\WFRC-5yr\
perl ..\PERL\sql.pl Z-2-output_data_to_grid_zone_short_names_straight.sql
