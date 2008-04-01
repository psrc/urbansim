proc import datafile="w:\users\lmwang\eclipse\opus\urbansim\sandbox\gridcells.tab"
out=f01
dbms=tab
replace;
getnames=yes;
run;

proc import datafile="w:\users\lmwang\eclipse\opus\urbansim\sandbox\block_area.csv"
out=f02
dbms=csv
replace;
getnames=yes;
run;

proc sort data=f01;
by GRID_ID;
run;

proc sort data=f02;
by GRID_ID;
run;

data whole;
  merge f01 (IN=g)
        f02(IN=b);
  by GRID_ID;
  if g;
run;

data clu;
  set whole (keep=grid_id barea rjobs pden rden);
run;

proc cluster data=clu method=ward std pseudo ccc outtree=otree;
   var RDEN PDEN BAREA RJOBS;
   id GRID_ID;
run;

proc tree data=otree horizontal graphics;
   title 'H tree';
run;

proc standard mean=0 std=1 data=clu out=stdclu;
   var barea rjobs pden rden ldhwy ldart;
run;

proc fastclus data=stdclu out=outclu maxc=3 noprint;
   var barea;
   id grid_id;
run;

proc freq data=outclu;
    tables cluster;
run;

proc candisc data=outclu out=outcan;
   var barea rjobs pden rden;
   class cluster;
run;

proc plot data=outcan;
   plot can2*can1=cluster;
run;

proc export data=outclu
outfile="C:\temp\outclu11.dbf"
replace;
run;
