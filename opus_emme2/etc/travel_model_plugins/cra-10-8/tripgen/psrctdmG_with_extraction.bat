REM this custom version of PSRCTDMn,bat adjusts the number of lanes
REM on overloaded links to accomodate large increases in planned land use.
REM
REM FYI: RUN PSRCTDM FROM BANK 1 DIRECTORY ONLY!!!
REM
REM SET the number of iterations for Intermediate and Final Assignments
SET IntIter=50
SET FinalIter=80
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
ren *.rpt *.rp0
REM
REM --------- 11111111111111111111111111111111 -----------------
REM ------------------------------------------------------------
REM       FIRST Complete Cycle of emme2 Macro Runs
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
call emme2 000 -m run2mac\nonw_dmf.mac 1 10
REM
REM +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
REM Check for overloaded links
REM
REM call emme2 to adjust link volumes for overloaded TAZs
call emme2 000 -m run2mac\addlanes.mac
cd ..\bank1
call emme2 000 -m run1mac\addlnam.mac
cd ..\bank3
call emme2 000 -m run3mac\addlnlat.mac
REM
REM Re-run initial assignments with new numbers of lanes
REM
REM call emme2 to obtain free-flow time skims
call emme2 000 -m run3mac\lateass0.mac
ren *.rpt *.rp0
REM
REM change from Bank 3 sub-directory to Bank 1 sub-directory
cd ..
cd bank1
REM
REM call emme2 to obtain free-flow time skims
call emme2 000 -m run1mac\hbw_tdm0.mac
call emme2 000 -m run1mac\vaemp.mac
ren *.rpt *.rp0
REM
REM change from Bank 1 sub-directory to Bank 2 sub-directory
cd ..
cd bank2
REM
REM call emme2 to obtain free-flow time skims
call emme2 000 -m run2mac\nonw_dm0.mac
ren *.rpt *.rp0
REM
REM re-run MD assignments
cd ..\bank2
call emme2 000 -m run2mac\nonwadjf.mac 1 %IntIter%
REM change report file extention to *.rp1
ren *.rpt *.rp1
REM
REM ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
REM
REM change from Bank 2 sub-directory to Bank 3 sub-directory
cd ..
cd bank3
REM
REM call emme2 to obtain PM, EV, and NI skims
call emme2 000 -m run3mac\lateassn.mac 1 %IntIter%
ren *.rpt *.rp1
REM
cd ..\bank1
call emme2 000 -m run1mac\hbwtdmf2.mac 1 %IntIter%
call emme2 000 -m run1mac\vaemp.mac
REM change report file extention to *.rp1
ren *.rpt *.rp1
REM
REM Change from Bank 1 to TODmodel
cd ..
cd todmodel
REM
REM call emme2 to obtain TOD shares
call emme2 000 -m runtod\todmodel.mac
ren *.rpt *.rp1
REM
REM --------- 22222222222222222222222222222222 -----------------
REM ------------------------------------------------------------
REM       2. INTERMEDIATE Complete Cycle of emme2 Macro Runs
REM       Note: This Cycle may be repeated by editing this
REM       .bat file using copy and paste - then respecifying the
REM       report suffix.
REM
REM change to Bank 1
cd ..
cd bank1
REM call emme2 Work Commute macros in run1mac\
call emme2 000 -m run1mac\hbwtdmf1.mac
REM
REM change from Bank1 sub-directory to Bank 2 sub-directory
cd ..
cd bank2
REM call emme2 Non-Work macros in run2mac\
call emme2 000 -m run2mac\nonw_dmi.mac %IntIter%
REM
REM change second round of Non-Work reports file extention
ren *.rpt *.rp2
REM
REM change from Bank 2 sub-directory to Bank 3 sub-directory
cd ..
cd bank3
REM
REM call emme2 to obtain PM, EV, and NI skims
call emme2 000 -m run3mac\lateassn.mac 1 %IntIter%
ren *.rpt *.rp2
REM
REM change from Bank 3 sub-directory to Bank 1 sub-directory
cd ..
cd bank1
REM call emme2 Work Commute macros in run1mac\
call emme2 000 -m run1mac\hbwtdmi2.mac %IntIter%
call emme2 000 -m run1mac\vaemp.mac
REM
REM change second round of Work Commute reports file extention
ren *.rpt *.rp2
REM
REM Change from Bank 1 to TODmodel
cd ..
cd todmodel
REM
REM call emme2 to obtain TOD shares
call emme2 000 -m runtod\todmodel.mac
ren *.rpt *.rp2
REM
REM --------- 33333333333333333333333333333333 -----------------
REM ------------------------------------------------------------
REM       2. INTERMEDIATE Complete Cycle of emme2 Macro Runs
REM       Note: This Cycle may be repeated by editing this
REM       .bat file using copy and paste - then respecifying the
REM       report suffix.
REM
REM change to Bank 1
cd ..
cd bank1
REM call emme2 Work Commute macros in run1mac\
call emme2 000 -m run1mac\hbwtdmf1.mac
REM
REM change from Bank1 sub-directory to Bank 2 sub-directory
cd ..
cd bank2
REM call emme2 Non-Work macros in run2mac\
call emme2 000 -m run2mac\nonw_dmi.mac %IntIter%
REM
REM change second round of Non-Work reports file extention
ren *.rpt *.rp3
REM
REM change from Bank 2 sub-directory to Bank 3 sub-directory
cd ..
cd bank3
REM
REM call emme2 to obtain PM, EV, and NI skims
call emme2 000 -m run3mac\lateassn.mac 1 %IntIter%
ren *.rpt *.rp3
REM
REM change from Bank 3 sub-directory to Bank 1 sub-directory
cd ..
cd bank1
REM call emme2 Work Commute macros in run1mac\
call emme2 000 -m run1mac\hbwtdmi2.mac %IntIter%
call emme2 000 -m run1mac\vaemp.mac
REM
REM change second round of Work Commute reports file extention
ren *.rpt *.rp3
REM
REM Change from Bank 1 to TODmodel
cd ..
cd todmodel
REM
REM call emme2 to obtain TOD shares
call emme2 000 -m runtod\todmodel.mac
ren *.rpt *.rp3
REM
REM --------- 44444444444444444444444444444444 -----------------
REM ------------------------------------------------------------
REM       2. INTERMEDIATE Complete Cycle of emme2 Macro Runs
REM       Note: This Cycle may be repeated by editing this
REM       .bat file using copy and paste - then respecifying the
REM       report suffix.
REM
REM change to Bank 1
cd ..
cd bank1
REM call emme2 Work Commute macros in run1mac\
call emme2 000 -m run1mac\hbwtdmf1.mac
REM
REM change from Bank1 sub-directory to Bank 2 sub-directory
cd ..
cd bank2
REM call emme2 Non-Work macros in run2mac\
call emme2 000 -m run2mac\nonw_dmi.mac %IntIter%
REM
REM change second round of Non-Work reports file extention
ren *.rpt *.rp4
REM
REM change from Bank 2 sub-directory to Bank 3 sub-directory
cd ..
cd bank3
REM
REM call emme2 to obtain PM, EV, and NI skims
call emme2 000 -m run3mac\lateassn.mac 1 %IntIter%
ren *.rpt *.rp4
REM
REM change from Bank 3 sub-directory to Bank 1 sub-directory
cd ..
cd bank1
REM call emme2 Work Commute macros in run1mac\
call emme2 000 -m run1mac\hbwtdmi2.mac %IntIter%
call emme2 000 -m run1mac\vaemp.mac
REM
REM change second round of Work Commute reports file extention
ren *.rpt *.rp4
REM
REM Change from Bank 1 to TODmodel
cd ..
cd todmodel
REM
REM call emme2 to obtain TOD shares
call emme2 000 -m runtod\todmodel.mac
ren *.rpt *.rp4
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
ren *.rpt *.rpf
REM
cd ..\bank1
modelzpe
echo This run of the Regional Council's Travel Demand Model is finished.
echo Extracting data for urbansim...
call emme2 000 -m run1mac\extract_logsums_and_trips.mac
call emme2 000 -m run1mac\extract_travel_times.mac
call emme2 000 -m run1mac\extract_urbansim_misc.mac
call emme2 000 -m run1mac\extract_utility_values.mac\
echo Done extracting for urbansim!
