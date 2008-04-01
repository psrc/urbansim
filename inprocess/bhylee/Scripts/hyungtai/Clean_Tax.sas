*Read dBase files or Excel spreasheet using PROC IMPORT;
proc import datafile='C:\Documents and Settings\hyungtai\Data\King\extr_rpacct.dbf' out=tax1 replace; run;


*Keep important variables;
data tax2 replace;
set tax1 (keep = major minor pin apprlandva apprimpsva taxablelan taxableimp);
run;

*Sort by unique id;
proc sort data=tax2 out=tax3; by pin; run;

*Sum only multiple cases;
data tax4 replace;
set tax3; by pin;
if first.pin then apprlandva1 = 0;
if first.pin then apprimpsva1 = 0;
if first.pin then taxablelan1 = 0;
if first.pin then taxableimp1 = 0;
apprlandva1 + apprlandva;
apprimpsva1 + apprimpsva;
taxablelan1 + taxablelan;
taxableimp1 + taxableimp;
if last.pin; 
drop apprlandva apprimpsva taxablelan taxableimp;
run;

*Format the data;
data tax5;
	set tax4;
	format major 6.;
	format minor 4.;
	format pin 10.;
	format apprlandva1 10.;
	format apprimpsva1 10.;
	format taxablelan1 10.;
	format taxableimp1 10.;

*Export as dbf file;
proc export data=tax5 outfile='C:\Documents and Settings\hyungtai\Data\King\Clean_Tax.dbf' replace; run;

*Export as SAS file (optional);
libname a 'C:\Documents and Settings\hyungtai\Data\King';
data a.Clean_Tax;
set tax5;
run;