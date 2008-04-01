REM Step 0-4. Run MySQL scripts to format baseyear data for the travel model
cd C:\eclipse\workspace\scripts\franklin\WFRC-5yr\
perl ..\PERL\sql.pl 0a-format_baseyear_data_for_travel_model.sql


REM Step 0-5. Transfer 1997 tables from MySQL Database to Travel Model

cd C:\eclipse\workspace\scripts\franklin\WFRC-5yr\
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_data_to_tm HHdistrib_joint_inclohi C:\WFRC\const\DV31_UrbanSim_1997\5Urbansim\Ui\ 1997
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_data_to_tm SEdata C:\WFRC\const\DV31_UrbanSim_1997\5Urbansim\Ui\ 1997


REM Step 0-6. Run 1997 Travel Model
c:
cd C:\WFRC\const\DV31_UrbanSim_1997
HailMaryNoPauses.bat


REM     ####################
REM     ##     Stage A    ##
REM     ##  1997 TO 2000  ##
REM     ####################


REM Step A-1. Transfer 1997 tables from Travel Model to MySQL Database
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\mysqlexchg.pl import C:\WFRC\LRP\DV31_UrbanSim_1997\5Urbansim\Uo\ 1996 WFRC_1997_scenario_LRP AccessLogsum
perl ..\PERL\mysqlexchg.pl import C:\WFRC\LRP\DV31_UrbanSim_1997\5Urbansim\Uo\ 1996 WFRC_1997_scenario_LRP HighwayTimes


REM Step A-2. Run MySQL scripts to put data into travel_data and zones tables
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl A-2-format_data_from_travel_model.sql


REM Step A-3. Run UrbanSim from 1997 to 2000
cd C:\Program Files\UrbanSim
urbansim.bat C:\eclipse\workspace\scripts\franklin\WFRC-33yr\WFRC_1997_parameters_2000_LRP.xml


REM Step A-4. Run MySQL scripts to format output for the travel model
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl A-4a-format_data_for_travel_model.sql
perl ..\PERL\sql.pl A-4b-output_to_continuation.sql


REM Step A-5. Transfer 2000 tables from MySQL Database to Travel Model

cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_2030_LRP HHdistrib_joint_inclohi C:\WFRC\const\DV31_UrbanSim_2000\5Urbansim\Ui\ 2000
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_2030_LRP SEdata C:\WFRC\const\DV31_UrbanSim_2000\5Urbansim\Ui\ 2000


REM Step A-6. Run 2000 Travel Model
cd C:\WFRC\const\DV31_UrbanSim_2000
HailMaryNoPauses.bat


REM     ####################
REM     ##     Stage B    ##
REM     ##  2000 TO 2003  ##
REM     ####################


REM Step B-1. Transfer 2000 tables from Travel Model to MySQL Database
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\mysqlexchg.pl import C:\WFRC\const\DV31_UrbanSim_2000\5Urbansim\Uo\ 2001 WFRC_2000_scenario_LRP AccessLogsum
perl ..\PERL\mysqlexchg.pl import C:\WFRC\const\DV31_UrbanSim_2000\5Urbansim\Uo\ 2001 WFRC_2000_scenario_LRP HighwayTimes


REM Step B-2. Run MySQL scripts to put data into travel_data and zones tables
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl B-2-format_data_from_travel_model.sql


REM Step B-3. Run UrbanSim from 2001 to 2003
cd C:\Program Files\UrbanSim
urbansim.bat C:\eclipse\workspace\scripts\franklin\WFRC-33yr\WFRC_2000_parameters_2003_LRP.xml


REM Step Y-1. Run basic set of 2003 indicators and put tables in the output database

cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl Y-1-2003_urbansim_indicators.sql


REM Step Y-2. Create 2003 short-name tables of zone and grid level aggregations for GIS use

cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl Y-2-2003_output_data_to_grid_zone_short_names.sql


REM Step B-4. Run MySQL scripts to format output for the travel model
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl B-4a-format_data_for_travel_model.sql
perl ..\PERL\sql.pl B-4b-output_to_continuation.sql


REM Step B-5. Transfer 2003 tables from MySQL Database to Travel Model

cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_2030_LRP HHdistrib_joint_inclohi C:\WFRC\const\DV31_UrbanSim_2003\5Urbansim\Ui\ 2003
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_2030_LRP SEdata C:\WFRC\const\DV31_UrbanSim_2003\5Urbansim\Ui\ 2003


REM Step B-6. Run 2003 Travel Model

cd C:\WFRC\const\DV31_UrbanSim_2003
HailMaryNoPauses.bat


REM     ####################
REM     ##     Stage C    ##
REM     ##  2003 TO 2008  ##
REM     ####################


REM Step C-1. Transfer 2003 tables from Travel Model to MySQL Database
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\mysqlexchg.pl import C:\WFRC\const\DV31_UrbanSim_2003\5Urbansim\Uo\ 2001 WFRC_2003_scenario_LRP AccessLogsum
perl ..\PERL\mysqlexchg.pl import C:\WFRC\const\DV31_UrbanSim_2003\5Urbansim\Uo\ 2001 WFRC_2003_scenario_LRP HighwayTimes


REM Step C-2. Run MySQL scripts to put data into travel_data and zones tables
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl C-2-format_data_from_travel_model.sql


REM Step C-3. Run UrbanSim from 2004 to 2008
cd C:\Program Files\UrbanSim
urbansim.bat C:\eclipse\workspace\scripts\franklin\WFRC-33yr\WFRC_2003_parameters_2008_LRP.xml


REM Step C-4. Run MySQL scripts to format output for the travel model
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl C-4a-format_data_for_travel_model.sql
perl ..\PERL\sql.pl C-4b-output_to_continuation.sql


REM Step C-5. Transfer 2008 tables from MySQL Database to Travel Model

cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_2030_LRP HHdistrib_joint_inclohi C:\WFRC\const\DV31_UrbanSim_2008\5Urbansim\Ui\ 2008
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_2030_LRP SEdata C:\WFRC\const\DV31_UrbanSim_2008\5Urbansim\Ui\ 2008


REM Step C-6. Run 2008 Travel Model

cd C:\WFRC\const\DV31_UrbanSim_2008
HailMaryNoPauses.bat


REM     ####################
REM     ##     Stage D    ##
REM     ##  2008 TO 2012  ##
REM     ####################


REM Step D-1. Transfer 2008 tables from Travel Model to MySQL Database
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\mysqlexchg.pl import C:\WFRC\const\DV31_UrbanSim_2008\5Urbansim\Uo\ 2008 WFRC_2008_scenario_LRP AccessLogsum
perl ..\PERL\mysqlexchg.pl import C:\WFRC\const\DV31_UrbanSim_2008\5Urbansim\Uo\ 2008 WFRC_2008_scenario_LRP HighwayTimes


REM Step D-2. Run MySQL scripts to put data into travel_data and zones tables
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl D-2-format_data_from_travel_model.sql


REM Step D-3. Run UrbanSim from 2009 to 2012
cd C:\Program Files\UrbanSim
urbansim.bat C:\eclipse\workspace\scripts\franklin\WFRC-33yr\WFRC_2008_parameters_2012_LRP.xml


REM Step D-4. Run MySQL scripts to format output for the travel model
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl D-4a-format_data_for_travel_model.sql
perl ..\PERL\sql.pl D-4b-output_to_continuation.sql


REM Step D-5. Transfer 2012 tables from MySQL Database to Travel Model

cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_2030_LRP HHdistrib_joint_inclohi C:\WFRC\const\DV31_UrbanSim_2012\5Urbansim\Ui\ 2012
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_2030_LRP SEdata C:\WFRC\const\DV31_UrbanSim_2012\5Urbansim\Ui\ 2012


REM Step D-6. Run 2012 Travel Model

cd C:\WFRC\const\DV31_UrbanSim_2012
HailMaryNoPauses.bat


REM     ####################
REM     ##     Stage E    ##
REM     ##  2012 TO 2016  ##
REM     ####################


REM Step E-1. Transfer 2012 tables from Travel Model to MySQL Database
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\mysqlexchg.pl import C:\WFRC\const\DV31_UrbanSim_2012\5Urbansim\Uo\ 2012 WFRC_2012_scenario_LRP AccessLogsum
perl ..\PERL\mysqlexchg.pl import C:\WFRC\const\DV31_UrbanSim_2012\5Urbansim\Uo\ 2012 WFRC_2012_scenario_LRP HighwayTimes


REM Step E-2. Run MySQL scripts to put data into travel_data and zones tables
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl E-2-format_data_from_travel_model.sql


REM Step E-3. Run UrbanSim from 2013 to 2016
cd C:\Program Files\UrbanSim
urbansim.bat C:\eclipse\workspace\scripts\franklin\WFRC-33yr\WFRC_2012_parameters_2016_LRP.xml


REM Step E-4. Run MySQL scripts to format output for the travel model
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl E-4a-format_data_for_travel_model.sql
perl ..\PERL\sql.pl E-4b-output_to_continuation.sql


REM Step E-5. Transfer 2016 tables from MySQL Database to Travel Model

cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_2030_LRP HHdistrib_joint_inclohi C:\WFRC\const\DV31_UrbanSim_2016\5Urbansim\Ui\ 2016
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_2030_LRP SEdata C:\WFRC\const\DV31_UrbanSim_2016\5Urbansim\Ui\ 2016


REM Step E-6. Run 2016 Travel Model

cd C:\WFRC\const\DV31_UrbanSim_2016
HailMaryNoPauses.bat


REM     ####################
REM     ##     Stage F    ##
REM     ##  2016 TO 2020  ##
REM     ####################


REM Step F-1. Transfer 2016 tables from Travel Model to MySQL Database
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\mysqlexchg.pl import C:\WFRC\const\DV31_UrbanSim_2016\5Urbansim\Uo\ 2016 WFRC_2016_scenario_LRP AccessLogsum
perl ..\PERL\mysqlexchg.pl import C:\WFRC\const\DV31_UrbanSim_2016\5Urbansim\Uo\ 2016 WFRC_2016_scenario_LRP HighwayTimes


REM Step F-2. Run MySQL scripts to put data into travel_data and zones tables
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl F-2-format_data_from_travel_model.sql


REM Step F-3. Run UrbanSim from 2017 to 2020
cd C:\Program Files\UrbanSim
urbansim.bat C:\eclipse\workspace\scripts\franklin\WFRC-33yr\WFRC_2016_parameters_2020_LRP.xml


REM Step F-4. Run MySQL scripts to format output for the travel model
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl F-4a-format_data_for_travel_model.sql
perl ..\PERL\sql.pl F-4b-output_to_continuation.sql


REM Step F-5. Transfer 2020 tables from MySQL Database to Travel Model

cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_2030_LRP HHdistrib_joint_inclohi C:\WFRC\const\DV31_UrbanSim_2020\5Urbansim\Ui\ 2020
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_2030_LRP SEdata C:\WFRC\const\DV31_UrbanSim_2020\5Urbansim\Ui\ 2020


REM Step F-6. Run 2020 Travel Model

cd C:\WFRC\const\DV31_UrbanSim_2020
HailMaryNoPauses.bat



REM     ####################
REM     ##     Stage G    ##
REM     ##  2020 TO 2025  ##
REM     ####################


REM Step G-1. Transfer 2020 tables from Travel Model to MySQL Database
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\mysqlexchg.pl import C:\WFRC\const\DV31_UrbanSim_2020\5Urbansim\Uo\ 2020 WFRC_2020_scenario_LRP AccessLogsum
perl ..\PERL\mysqlexchg.pl import C:\WFRC\const\DV31_UrbanSim_2020\5Urbansim\Uo\ 2020 WFRC_2020_scenario_LRP HighwayTimes


REM Step G-2. Run MySQL scripts to put data into travel_data and zones tables
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl G-2-format_data_from_travel_model.sql


REM Step G-3. Run UrbanSim from 2021 to 2025
cd C:\Program Files\UrbanSim
urbansim.bat C:\eclipse\workspace\scripts\franklin\WFRC-33yr\WFRC_2020_parameters_2025_LRP.xml


REM Step G-4. Run MySQL scripts to format output for the travel model
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl G-4a-format_data_for_travel_model.sql
perl ..\PERL\sql.pl G-4b-output_to_continuation.sql


REM Step G-5. Transfer 2025 tables from MySQL Database to Travel Model

cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_2030_LRP HHdistrib_joint_inclohi C:\WFRC\const\DV31_UrbanSim_2025\5Urbansim\Ui\ 2025
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_2030_LRP SEdata C:\WFRC\const\DV31_UrbanSim_2025\5Urbansim\Ui\ 2025


REM Step G-6. Run 2025 Travel Model

cd C:\WFRC\const\DV31_UrbanSim_2025
HailMaryNoPauses.bat


REM     ####################
REM     ##     Stage H    ##
REM     ##  2025 TO 2030  ##
REM     ####################


REM Step H-1. Transfer 2025 tables from Travel Model to MySQL Database
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\mysqlexchg.pl import C:\WFRC\const\DV31_UrbanSim_2025\5Urbansim\Uo\ 2025 WFRC_2025_scenario_LRP AccessLogsum
perl ..\PERL\mysqlexchg.pl import C:\WFRC\const\DV31_UrbanSim_2025\5Urbansim\Uo\ 2025 WFRC_2025_scenario_LRP HighwayTimes


REM Step H-2. Run MySQL scripts to put data into travel_data and zones tables
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl H-2-format_data_from_travel_model.sql


REM Step H-3. Run UrbanSim from 2026 to 2030
cd C:\Program Files\UrbanSim
urbansim.bat C:\eclipse\workspace\scripts\franklin\WFRC-33yr\WFRC_2025_parameters_2030_LRP.xml


REM Step Z-1. Run basic set of indicators and put tables in the output database

cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl Z-1-urbansim_indicators.sql


REM Step Z-2. Create short-name tables of zone and grid level aggregations for GIS use

cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl Z-2-output_data_to_grid_zone_short_names.sql


REM Step H-4. Run MySQL scripts to format output for the travel model
cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\sql.pl H-4a-format_data_for_travel_model.sql
perl ..\PERL\sql.pl H-4b-output_to_continuation.sql


REM Step H-5. Transfer 2030 tables from MySQL Database to Travel Model

cd C:\eclipse\workspace\scripts\franklin\WFRC-33yr\
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_2030_LRP HHdistrib_joint_inclohi C:\WFRC\const\DV31_UrbanSim_2030\5Urbansim\Ui\ 2030
perl ..\PERL\mysqlexchg.pl export WFRC_1997_output_2030_LRP SEdata C:\WFRC\const\DV31_UrbanSim_2030\5Urbansim\Ui\ 2030


REM Step H-6. Run 2030 Travel Model

cd C:\WFRC\const\DV31_UrbanSim_2030
HailMaryNoPauses.bat
