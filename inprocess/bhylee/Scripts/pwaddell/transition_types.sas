libname dev 's:\urban-data\InputData\AppliedUtah\DevHistory';
filename in 's:\urban-data\InputData\AppliedUtah\DevHistory\devhistory.tab';
filename out1 's:\urban-data\InputData\AppliedUtah\DevHistory\template_header.csv';
filename out2 's:\urban-data\InputData\AppliedUtah\DevHistory\template.csv';

proc import datafile='s:\urban-data\InputData\AppliedUtah\DevHistory\devhistory.tab' dbms=tab out=devhist 
replace;

data one;
set devhist (rename=(enddevtype=enddev startdevtype=startdev));

if endunits > 0 then ivres=endimpvalres/endunits;
else ivres=0;
if endsqft > 0 then ivnres=endimpvalnonres/endsqft;
else ivnres=0;

proc sort;
by startdev enddev;
proc means noprint;
by startdev enddev;
var diffunits diffsqft ivres ivnres;
output out=tmp
mean=dunit dsqft ivr ivnr
std =dunit_s dsqft_s ivr_s ivnr_s
min =dunit_m dsqft_m ivr_m ivnr_m
max =dunit_x dsqft_x ivr_x ivnr_x;

data dev.template;
set tmp;
id=_n_;
years=1;
phasing=1;
include=-1;

ivr_m=round(ivr_m);
ivnr_m=round(ivnr_m);
dunit_m=round(dunit_m);
dsqft_m=round(dsqft_m);
ivr_x=round(ivr_x);
ivnr_x=round(ivnr_x);
dunit_x=round(dunit_x);
dsqft_x=round(dsqft_x);

drop _type_ _freq_;
if ivr_s=. then ivr_s=0;
if ivnr_s=. then ivnr_s=0;
if dunit_s=. then dunit_s=0;
if dsqft_s=. then dsqft_s=0;
if ivr_m=. then ivr_m=0;
if ivnr_m=. then ivnr_m=0;
if dunit_m=. then dunit_m=0;
if dsqft_m=. then dsqft_m=0;
if ivr_x=. then ivr_x=0;
if ivnr_x=. then ivnr_x=0;
if dunit_x=. then dunit_x=0;
if dsqft_x=. then dsqft_x=0;
if ivr=. then ivr=0;
if ivnr=. then ivnr=0;
if dunit=. then dunit=0;
if dsqft=. then dsqft=0;

cdsqft=0;
cdsqft_s=0;
cdsqft_m=0;
cdsqft_x=0;

civnr=0;
civnr_s=0;
civnr_m=0;
civnr_x=0;

idsqft=0;
idsqft_s=0;
idsqft_m=0;
idsqft_x=0;

iivnr=0;
iivnr_s=0;
iivnr_m=0;
iivnr_x=0;

gdsqft=0;
gdsqft_s=0;
gdsqft_m=0;
gdsqft_x=0;

givnr=0;
givnr_s=0;
givnr_m=0;
givnr_x=0;

if enddev le 19 then do;
cdsqft=dsqft;
cdsqft_s=dsqft_s;
cdsqft_m=dsqft_m;
cdsqft_x=dsqft_x;

civnr=ivnr;
civnr_s=ivnr_s;
civnr_m=ivnr_m;
civnr_x=ivnr_x;
end;

if 20 le enddev le 22 then do;
idsqft=dsqft;
idsqft_s=dsqft_s;
idsqft_m=dsqft_m;
idsqft_x=dsqft_x;

iivnr=ivnr;
iivnr_s=ivnr_s;
iivnr_m=ivnr_m;
iivnr_x=ivnr_x;
end;

if enddev = 23 then do;
gdsqft=dsqft;
gdsqft_s=dsqft_s;
gdsqft_m=dsqft_m;
gdsqft_x=dsqft_x;

givnr=ivnr;
givnr_s=ivnr_s;
givnr_m=ivnr_m;
givnr_x=ivnr_x;
end;

*keep id startdev enddev ivr ivnr dunit dsqft ivr_s ivnr_s dunit_s dsqft_s  
ivr_m ivnr_m dunit_m dsqft_m ivr_x ivnr_x dunit_x dsqft_x years ;

*proc export data=dev.template outfile='Y:\urbansim3\urban-data\InputData\AppliedUtah\DevHistory\template.csv'
dbms=csv;
file out2;
put id ',' include ',' startdev ',' enddev ',' 
dunit ',' dunit_s ',' dunit_m ',' dunit_x ','
cdsqft ',' cdsqft_s ',' cdsqft_m ',' cdsqft_x ','
idsqft ',' idsqft_s ',' idsqft_m ',' idsqft_x ','
gdsqft ',' gdsqft_s ',' gdsqft_m ',' gdsqft_x ','
ivr ',' ivr_s ',' ivr_m ',' ivr_x ','
civnr ',' civnr_s ',' civnr_m ',' civnr_x ','
iivnr ',' iivnr_s ',' iivnr_m ',' iivnr_x ','
givnr ',' givnr_s ',' givnr_m ',' givnr_x ','
years;

proc print;

run;
