REM RUN THIS FROM MAIN FOLDER ONLY (NOT FROM INSIDE OF ANY DATA BANK)
cd bank1
if exist LOCKI echo LOCKI found in Bank1
if exist LOCKI exit /b
cd ..\bank2
if exist LOCKI echo LOCKI found in Bank2
if exist LOCKI exit /b
cd ..\bank3
if exist LOCKI echo LOCKI found in Bank3
if exist LOCKI exit /b
cd ..\tripgen
if exist LOCKI echo LOCKI found in Tripgen
if exist LOCKI exit /b
cd ..\todmodel
if exist LOCKI echo LOCKI found in Todmodel
if exist LOCKI exit /b
cd ..\TRIPGEN
call emme2 000 -m runtg\tripgen.mac
REM Trip Generation Completed !!
REM --------------------------------------------
REM --------------------------------------------
REM Trip Generation Completed !!
cd ..\Initial
call Initial2.bat
REM Intialization Completed !!
REM --------------------------------------------
REM --------------------------------------------
REM Intialization Completed !!
cd ..\bank1
call emme2 000 -m ..\tripgen\runtg\tgtobk1.mac
REM Copying Matrices to Bank1 Completed !!
REM --------------------------------------------
REM --------------------------------------------
REM Copying Matrices to Bank1 Completed!!
call PSRC0.bat
REM --------------------------------------------
REM --------------------------------------------
REM Model Run Completed!!
