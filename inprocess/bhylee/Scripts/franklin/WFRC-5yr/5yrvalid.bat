

REM Step 0-4. Run MySQL scripts to format baseyear data for the travel model
cd C:\eclipse\workspace\scripts\franklin\WFRC-5yr\
perl ..\PERL\sql.pl 0a-format_baseyear_data_for_travel_model.sql


REM Step 0-5. Transfer 1997 tables from MySQL Database to Travel Model

cd C:\eclipse\workspace\scripts\franklin\WFRC-5yr\
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_data_to_tm HHdistrib_joint_inclohi C:\WFRC\DV31_UrbanSim_1997\5Urbansim\Ui\ 1997
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_data_to_tm SEdata C:\WFRC\DV31_UrbanSim_1997\5Urbansim\Ui\ 1997


REM Step 0-6. Run 1997 Travel Model
c:
cd C:\WFRC\DV31_UrbanSim_1997
HailMaryNoPauses.bat


REM     ####################
REM     ##     Stage A    ##
REM     ##  1997 TO 2000  ##
REM     ####################


REM Step A-1. Transfer 1996 tables from Travel Model to MySQL Database
cd C:\eclipse\workspace\scripts\franklin\WFRC-5yr\
perl ..\PERL\mysqlexchg.pl import C:\WFRC\DV31_UrbanSim_1997\5Urbansim\Uo\ 1996 WFRC_1997_scenario_5yr AccessLogsum
perl ..\PERL\mysqlexchg.pl import C:\WFRC\DV31_UrbanSim_1997\5Urbansim\Uo\ 1996 WFRC_1997_scenario_5yr HighwayTimes


REM Step A-2. Run MySQL scripts to put data into travel_data and zones tables
cd C:\eclipse\workspace\scripts\franklin\WFRC-5yr\
perl ..\PERL\sql.pl A-2-format_data_from_travel_model.sql


REM Step A-3. Run UrbanSim from 1997 to 2000
cd C:\Program Files\UrbanSim
urbansim.bat C:\eclipse\workspace\scripts\franklin\WFRC-5yr\WFRC_1997_parameters_5yr_2000.xml


REM Step A-4. Run MySQL scripts to format output for the travel model
cd C:\eclipse\workspace\scripts\franklin\WFRC-5yr\
perl ..\PERL\sql.pl A-4a-format_data_for_travel_model.sql
perl ..\PERL\sql.pl A-4b-output_to_continuation.sql


REM Step A-5. Transfer 2000 tables from MySQL Database to Travel Model

cd C:\eclipse\workspace\scripts\franklin\WFRC-5yr\
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_5yr_2003 HHdistrib_joint_inclohi C:\WFRC\DV31_UrbanSim_2000\5Urbansim\Ui\ 2000
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_5yr_2003 SEdata C:\WFRC\DV31_UrbanSim_2000\5Urbansim\Ui\ 2000


REM Step A-6. Run 2000 Travel Model
cd C:\WFRC\DV31_UrbanSim_2000
HailMaryNoPauses.bat


REM     ####################
REM     ##     Stage B    ##
REM     ##  2000 TO 2003  ##
REM     ####################


REM Step B-1. Transfer 2000 tables from Travel Model to MySQL Database
cd C:\eclipse\workspace\scripts\franklin\WFRC-5yr\
perl ..\PERL\mysqlexchg.pl import C:\WFRC\DV31_UrbanSim_2000\5Urbansim\Uo\ 2001 WFRC_2000_scenario_5yr AccessLogsum
perl ..\PERL\mysqlexchg.pl import C:\WFRC\DV31_UrbanSim_2000\5Urbansim\Uo\ 2001 WFRC_2000_scenario_5yr HighwayTimes


REM Step B-2. Run MySQL scripts to put data into travel_data and zones tables
cd C:\eclipse\workspace\scripts\franklin\WFRC-5yr\
perl ..\PERL\sql.pl B-2-format_data_from_travel_model.sql


REM Step B-3. Run UrbanSim from 2001 to 2003
cd C:\Program Files\UrbanSim
urbansim.bat C:\eclipse\workspace\scripts\franklin\WFRC-5yr\WFRC_2000_parameters_5yr_2003.xml


REM Step Z-1. Run basic set of indicators and put tables in the output database

cd C:\eclipse\workspace\scripts\franklin\WFRC-5yr\
perl ..\PERL\sql.pl Z-1-urbansim_indicators.sql


REM Step Z-2. Create short-name tables of zone and grid level aggregations for GIS use

cd C:\eclipse\workspace\scripts\franklin\WFRC-5yr\
perl ..\PERL\sql.pl Z-2-output_data_to_grid_zone_short_names.sql


REM Step B-4. Run MySQL scripts to format output for the travel model
cd C:\eclipse\workspace\scripts\franklin\WFRC-5yr\
perl ..\PERL\sql.pl B-4-format_data_for_travel_model.sql


REM Step B-5. Transfer 2000 tables from MySQL Database to Travel Model

cd C:\eclipse\workspace\scripts\franklin\WFRC-5yr\
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_5yr_2003 HHdistrib_joint_inclohi C:\WFRC\DV31_UrbanSim_2003\5Urbansim\Ui\ 2003
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_5yr_2003 SEdata C:\WFRC\DV31_UrbanSim_2003\5Urbansim\Ui\ 2003


REM Step B-6. Run 2003 Travel Model

cd C:\WFRC\DV31_UrbanSim_2003
HailMaryNoPauses.bat
