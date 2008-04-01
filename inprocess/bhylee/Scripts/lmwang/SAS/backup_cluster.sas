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

data f03;
set f02;
format barea e12.3;
run;

proc export data=f02
outfile="C:\temp\blockarea.dbf"
replace;
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


/**
data clu;
  set w2 (keep=grid_id barea yr_blt bld_age rjobs ljobsw s7wd s8wd s9wd pden lpw rden pcwd prwd piwd powd lsfcw lsfiw lduw
             lwae lwap lhae lhap tt_cbd ttf_sov ttt_sov tt_tw ut_sov ut_tw);
run;

proc cluster data=clu method=ward std pseudo ccc outtree=otree;
   var RDEN PDEN BAREA RJOBS;
   id GRID_ID;
run;

proc tree data=otree horizontal graphics;
   title 'H tree';
run;

data uftb.clu;
  set w2 (keep=grid_id barea yr_blt bld_age rjobs ljobsw s7wd s8wd s9wd pden lpw rden pcwd prwd piwd powd lsfcw lsfiw lduw
             lwae lwap lhae lhap tt_cbd ttf_sov ttt_sov tt_tw ut_sov ut_tw);
run;

**/

libname uftb 'c:\workspace\hh\sas';

proc means data=w2;
    var barea yr_blt bld_age rjobs ljobsw s7wd s8wd s9wd pden lpw rden pcwd prwd piwd powd lsfcw lsfiw lduw
             lwae lwap lhae lhap tt_cbd ttf_sov ttt_sov tt_tw ut_sov ut_tw;
run;

data w3;
  set w2;
  if yr_blt < 1900 then yr_blt = .;
  if yr_blt > 2000 then yr_blt = .;
  if bld_age < 0 then bld_age = .;
  if bld_age > 100 then bld_age = .;
  lba = log(barea);
  lrew = log(rjobs);
run;

proc standard mean=0 std=1 data=w3 out=stdw3;
   var lba barea yr_blt bld_age lrew rjobs ljobsw s7wd s8wd s9wd pden lpw rden
             pcwd prwd piwd powd lsfcw lsfiw lduw
             lwae lwap lhae lhap tt_cbd ttf_sov ttt_sov tt_tw ut_sov ut_tw;
run;

proc fastclus data=stdw3 out=outclu maxc=4 noprint;
   var lhap ttf_sov tt_tw lrew lba yr_blt ;
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
outfile="C:\workspace\outclu_all.dbf"
replace;
run;

/***merge survey and gridcell data***/
proc import datafile="C:\workspace\hh\data\hh_gid.dbf"
out=_hh
dbms=dbf
replace;
run;

data hh;
set _hh;
GRID_ID=GRID_CODE;
run;

proc sort data=hh;
by GRID_ID;
run;

proc sort data=outclu;
by GRID_ID;
run;

data chosen_nb;
  merge hh (IN=h keep=hh_id grid_id)
        outclu (IN=c keep=grid_id cluster);
  by GRID_ID;
  if h;
  if c;
run;

proc sql;
   create table chosen_m as
      select h.hh_id, p.mode
      from hh as h inner join sw_hh as w on h.hh_id = w.hh_id
           inner join persons as p on w.per_id = p.per_id;
      select * from _chosen_choice;
quit;

data chosen_choice;
   merge chosen_nb
         chosen_m;
   by hh_id;
   replicate + 1;
run

/*sample housing alternatives */
proc sort data=outclu;
by cluster;
run;

proc surveyselect data=outclu
   method=srs n=(1 1 1 1)
   out=h_alt noprint rep=5630;    /*replace with number of samples wanted*/
   strata cluster;
run;

/*create mode alternatives */
proc iml;
/*
   use faz;
   read all into alt;
*/
   alt={1,2,3,4};
   nrep = 5;
   nalt = nrow(alt);
   repz = (1:nrep)`;
   reps = repeat(repz, nalt, 1);
   alts = repeat(alt, nrep, 1);
   create _reps from reps[colname={'rep'}];
          append from reps; close _reps;
   sort _reps by rep;
   use _reps; read all into reps;
   m_alt = J(nrep*nalt, 2, .);
   m_alt[,1] = reps; m_alt[,2]= alts;
   create m_alt from m_alt[colname={'replicate', 'mode'}];
          append from m_alt;
quit;

/* merge two dimensions of choice*/
data alts;
    merge h_alt
          m_alt;
    by replicate;
run;

/*assign agent(household) to alternatives*/
proc sort data=alts;
by replicate;
run;

data _hh_alts;
  merge chosen_choice (rename = (grid_id=ch_grid cluster=ch_clu mode=ch_mode))
        alts;
  by Replicate;
run;

data hh_alts;
  set _hh_alts;
  choice = 0;
  if ch_clu = cluster then
     do;
      grid_id = ch_grid;
      cluster = ch_clu;
      if ch_mode = mode then
         choice=1;
     output;
     end;
run;
