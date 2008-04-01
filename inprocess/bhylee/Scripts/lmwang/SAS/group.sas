/* 
sas program to generate group assignment per Jack's request
*/

data inputdata;
  input id_field @@;
  datalines;
1 2 
3 4 
9 16
;
run;

data mydata;
set inputdata;
center = id_field;
keep center;
run;

proc sql;
  create table xx as
  select a.center as A, b.center as B from mydata a, mydata b
  where a.center < b.center;
quit;

data yy;
set xx;
retain step 1;
groupid + step;
keep groupid A B;
run;

data groupdata;
set yy(keep=groupid A rename=(A=centerid)) yy(keep=groupid B rename=(B=centerid));
run;

proc sort data=groupdata;
by groupid;
run;

proc print data=groupdata;
run;
