REM FYI: RUN PSRC0 FROM BANK 1 DIRECTORY ONLY!!!
REM  This batch file does a partial model run just to produce outputs.
REM  Do not use for any meaningful work.
REM
REM SET the number of iterations for Intermediate and Final Assignments
SET FinalIter=10
REM
REM change from Bank 1 sub-directory to Bank 3 sub-directory
cd ..
cd bank3
REM erase all old report files in Bank 3 sub-directory
erase *.rp*
ren errors errors.rpt
erase reports
REM
REM call emme2 to obtain free-flow time skims
call emme2 000 -m run3mac\lateass0.mac
REM
REM Check for NaN in recent reports
@call ..\model\nantest .rpt
if errorlevel 4 (echo Found NaN) else (echo No NaN)
if errorlevel 4 exit /b
REM
ren *.rpt *.rp0
REM
REM change from Bank 3 sub-directory to Bank 1 sub-directory
cd ..
cd bank1
REM erase all old reports files in Bank 1 sub-directory
erase *.rp*
ren errors errors.rpt
erase reports
REM
REM call emme2 to obtain free-flow time skims
call emme2 000 -m run1mac\hbw_tdm0.mac
call emme2 000 -m run1mac\vaemp.mac
REM
REM Check for NaN in recent reports
@call ..\model\nantest .rpt
if errorlevel 4 (echo Found NaN) else (echo No NaN)
if errorlevel 4 exit /b
REM
ren *.rpt *.rp0
REM
REM change from Bank 1 sub-directory to Bank 2 sub-directory
cd ..
cd bank2
REM erase all old report files in Bank 2 sub-directory
erase *.rp*
ren errors errors.rpt
erase reports
REM
REM call emme2 to obtain free-flow time skims
call emme2 000 -m run2mac\nonw_dm0.mac
REM
REM Check for NaN in recent reports
@call ..\model\nantest .rpt
if errorlevel 4 (echo Found NaN) else (echo No NaN)
if errorlevel 4 exit /b
REM
ren *.rpt *.rp0
REM
REM Change from Bank 2 to TODmodel
cd ..
cd todmodel
REM erase all old report files in TODmodel sub-directory
erase *.rp*
ren errors errors.rpt
erase reports
REM
REM call emme2 to obtain initial TOD shares
call emme2 000 -m runtod\todmodel.mac
REM
REM Check for NaN in recent reports
@call ..\model\nantest .rpt
if errorlevel 4 (echo Found NaN) else (echo No NaN)
if errorlevel 4 exit /b
REM
ren *.rpt *.rp0
REM
REM
REM ----------- FFFFFFFFFFFFFFFFFFFFFFFFFFFF -------------------
REM ------------------------------------------------------------
REM       FINAL Complete Cycle of emme2 Macro Runs
REM
REM change from TODmodel sub-directory to Bank 1 sub-directory
cd ..
cd bank1
REM
REM call emme2 Work Commute macros in run1mac\
call emme2 000 -m run1mac\hbwtdmf1.mac
REM
REM change from Bank 1 sub-directory to Bank 3 sub-directory
cd ..
cd bank3
REM call Van Pool model
call emme2 000 -m vanpool\vanpool.mac
REM
REM change from Bank 3 sub-directory to Bank 2 sub-directory
cd ..
cd bank2
REM call emme2 Non-Work macros in run2mac\
call emme2 000 -m run2mac\nonw_dmf.mac f %FinalIter%
call emme2 000 -m run2mac\tveh2.mac
REM
REM Check for NaN in recent reports
@call ..\model\nantest .rpt
if errorlevel 4 (echo Found NaN) else (echo No NaN)
if errorlevel 4 exit /b
REM
REM
REM change report file extention to *.rp1
ren *.rpt *.rpf
REM
REM change from Bank 2 sub-directory to Bank 3 sub-directory
cd ..
cd bank3
REM
REM call emme2 to obtain PM, EV, and NI skims
call emme2 000 -m run3mac\lateassn.mac f %FinalIter%
REM
REM change to Bank 1 sub-directory
cd ..
cd bank1
REM call emme2 Work Commute macros in run1mac\
call emme2 000 -m run1mac\hbwtdmf2.mac f %FinalIter%
call emme2 000 -m run1mac\tveh1.mac
REM
REM Check for NaN in recent reports
@call ..\model\nantest .rpt
if errorlevel 4 (echo Found NaN) else (echo No NaN)
if errorlevel 4 exit /b
REM
REM change report file extention to *.rp1
ren *.rpt *.rpf
REM
REM change from Bank 1 sub-directory to Bank 3 sub-directory
cd ..
cd bank3
REM
REM call emme2 to obtain daily link volumes
call emme2 000 -m run3mac\tveh3.mac
call emme2 000 -m run3mac\tvehsum.mac
REM
REM Check for NaN in recent reports
@call ..\model\nantest .rpt
if errorlevel 4 (echo Found NaN) else (echo No NaN)
if errorlevel 4 exit /b
REM
ren *.rpt *.rpf
REM
cd ..\bank1
echo This TEST run of part of the Regional Council's Travel Demand Model is finished.
