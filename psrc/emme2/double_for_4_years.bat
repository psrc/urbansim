REM Iterate over each of the four decades to 
REM double lane width in each of the 5 scenarios.
REM
REM Steps for using this batch file:
REM
REM (1) cd to the top level directory  for the travel model, 
REM e.g., D:\baseline_travel_model_psrc_highway
REM
REM (2) Make sure that the lanes are normal width in this
REM directory.
REM
REM (3) Invoke this batch file from there.
REM
cd 2000_06
call ..\double_for_one_year.bat
cd ..
cd 2010_06
call ..\double_for_one_year.bat
cd ..
cd 2020_06
call ..\double_for_one_year.bat
cd ..
cd 2030_06
call ..\double_for_one_year.bat
cd ..
