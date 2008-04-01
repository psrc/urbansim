REM	Run UrbanSim for one dummy year with no models to convert input data into output data

cd C:\Program Files\UrbanSim
urbansim.bat C:\eclipse\workspace\scripts\franklin\parameters\WFRC_1997_parameters_data_to_tm.xml

REM	Format the output data into travel model format

cd C:\eclipse\workspace\scripts\franklin\
perl PERL\sql.pl SQL\WFRC\0a-format_baseyear_data_for_travel_model.sql

REM	Export the travel model data from MySQL into the file system

cd C:\eclipse\workspace\scripts\franklin\
perl PERL\mysqlexchg.pl export WFRC_1997_output_data_to_tm HHdistrib_joint_inclohi C:\WFRC\DV31_UrbanSim_1997\5Urbansim\Ui\ 1997
perl PERL\mysqlexchg.pl export WFRC_1997_output_data_to_tm SEdata C:\WFRC\DV31_UrbanSim_1997\5Urbansim\Ui\ 1997

REM 	Run the travel model

cd C:\WFRC\DV31_UrbanSim_1997
HailMaryNoPauses.bat
