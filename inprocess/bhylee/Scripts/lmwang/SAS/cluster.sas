libname ds 'c:\workspace\hh\sas';

/*read-in gridcell variables*/
proc import datafile="c:\workspace\hh\data\gridcells.tab"
out=ds.gcs
dbms=tab
replace;
getnames=yes;
run;

proc import datafile="c:\workspace\hh\data\block_area.csv"
out=ds.blks
dbms=csv
replace;
getnames=yes;
run;

/*
proc export data=f02
outfile="C:\temp\blockarea.dbf"
replace;
run;
*/

/*perpare data for neighorhood clustering*/
proc sort data=ds.gcs;
by GRID_ID;
run;

proc sort data=ds.blks;
by GRID_ID;
run;

data _gcs_blk1;  /* */
  merge ds.gcs (IN=g)
        ds.blks (IN=b);
  by GRID_ID;
  if g;
run;

proc means data=_gcs_blk1;
    var barea yr_blt bld_age rjobs ljobsw s7wd s8wd s9wd pden lpw rden pcwd prwd piwd powd lsfcw lsfiw lduw
             lwae lwap lhae lhap tt_cbd ttf_sov ttt_sov tt_tw ut_sov ut_tw;
run;

data _gcs_blk2;
  set _gcs_blk1;
  if yr_blt < 1900 then yr_blt = .;
  if yr_blt > 2000 then yr_blt = .;
  if bld_age < 0 then bld_age = .;
  if bld_age > 100 then bld_age = .;
  lba = log(barea);
  lrew = log(rjobs);
run;

data gcs_blk;
   set ds.gcs_blk;
   if ldu > 0;
   du = ROUND(exp(ldu));
run;

proc means data=gcs_blk;
    var barea yr_blt bld_age rjobs ljobsw s7wd s8wd s9wd pden lpw rden pcwd prwd piwd powd lsfcw lsfiw lduw
             lwae lwap lhae lhap tt_cbd ttf_sov ttt_sov tt_tw ut_sov ut_tw;
run;

proc standard mean=0 std=1 data=gcs_blk out=ds.std_gb;
   var lba barea bld_age lrew rjobs ljobsw s7wd s8wd s9wd pden lpw rden
             pcwd prwd piwd powd lsfcw lsfiw lduw ldu
             lwae lwap lhae lhap tt_cbd ttf_sov ttt_sov tt_tw ut_sov ut_tw;
run;

proc fastclus data=ds.std_gb out=ds.nb_clufreq42 maxc=4 summary;
   var lhap lhae ttf_sov tt_tw lrew lduw lba bld_age ;
   id grid_id;
   freq du;
run;

proc freq data=ds.nb_clufreq43;
    tables cluster;
run;

proc candisc data=ds.nb_cluster out=outcan;
   var lhap lhae ttf_sov tt_tw lrew lduw lba bld_age;
   class cluster;
run;

proc plot data=outcan;
   plot can2*can1=cluster;
run;

proc export data=ds.nb_clufreq43
outfile="C:\workspace\nb_clufreq43.dbf"
replace;
run;

data ds.nb_clufreq43;
    set ds.nb_clufreq40;
    if cluster = 4 then cluster = 2;
run;

/**********************clustering ends**********************/

/***household with grid_id***/
proc import datafile="C:\workspace\hh\data\hh_gid.dbf"
out=_hh
dbms=dbf
replace;
run;

data ds.hh;
  set _hh;
  GRID_ID=GRID_CODE;
run;

proc datasets;
   delete _hh;
run;

/***work with grid_id***/
proc import datafile="C:\workspace\hh\data\work_gid.dbf"
out=ds.work
dbms=dbf
replace;
run;

/***single worker household***/
proc import datafile="C:\workspace\hh\data\sw_hh.csv"
out=ds.sw_hh
dbms=csv
replace;
getnames=yes;
run;

/***person***/
proc import datafile="C:\workspace\hh\data\person.csv"
out=ds.person
dbms=csv
replace;
getnames=yes;
run;

/***travel time***/
proc import datafile="C:\workspace\hh\data\travel_time.csv"
out=ds.travel_time
dbms=csv
replace;
getnames=yes;
run;

/*household's chosen neighorhood */
proc sort data=ds.hh; by GRID_ID;
run;
proc sort data=ds.nb_clufreq43; by GRID_ID;
run;

data chosen_nbq;
  merge ds.hh (IN=h keep=hh_id grid_id)
        ds.nb_clufreq43 (IN=c keep=grid_id cluster);
  by GRID_ID;
  if h;
  if c;
run;

/*household's chosen mode */
data persons_m;
    set ds.person;
    if towork = 1 then mode_w = 1;
    if towork = 2 or towork = 3 then mode_w = 2;
    if towork = 5 or towork = 6 then mode_w = 3;
    if towork = 4 or towork = 7 or towork= 8 then mode_w=4;
run;

proc sql;
   create table chosen_m as
      select w.hh_id, p.per_id, p.mode_w
      from ds.sw_hh as w inner join persons_m as p
           on w.per_id = p.per_id and w.hh_id = p.hh_id;
quit;

/*merge household's chosen mode */
proc sort data=chosen_nbq;
     by hh_id;
run;
proc sort data=chosen_m;
     by hh_id;
run;

data ds.chosen_choiceq;
   merge chosen_nbq (IN=ngb)
         chosen_m (IN=m);
   by hh_id;
   if ngb; if m;
   if mode_w; if grid_id;
   replicate + 1;
run;

proc freq data=ds.chosen_choiceq;
    tables cluster*mode_w;
run;

/*sample housing alternatives */
proc sort data=ds.nb_clufreq43;
by cluster;
run;

proc surveyselect data=ds.nb_clufreq43
   method=srs n=(1 1 1)
   out=h_alt stats noprint rep=2560;    /*replace with number of samples wanted*/
   strata cluster;
run;

/*create mode alternatives */
proc iml;
/*
   use faz;
   read all into alt;
*/
   alt={1,2,3,4};
   nrep = 2560;
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
proc sql;
   create table ds.alts as
      select h.replicate, h.cluster, h.grid_id, h.samplingweight, m.mode
      from h_alt as h inner join m_alt as m
           on h.replicate=m.replicate;
quit;

/*assign agent(household) to alternatives*/
proc sort data=ds.alts;
by replicate;
run;

data _hh_alts;
  merge ds.chosen_choiceq (rename = (grid_id=ch_grid cluster=ch_clu mode_w=ch_mode))
        ds.alts;
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
     end;
run;

data ds.hh_alts;
   set hh_alts;
   keep replicate hh_id per_id cluster grid_id mode choice samplingweight;
run;


/*populate variables for alternative set */
proc sql;
   create table hh_alts_h as
      select a.*, hh.totveh, hh.hhsize, hh.income, hh.restype, hh.hh_taz
      from ds.hh_alts as a inner join ds.hh as hh
           on a.hh_id =hh.hh_id;
quit;

proc sql;
   create table hh_alts_hp as
      select a.*, p.age, p.educate, p.ethn, p.lic
      from hh_alts_h as a inner join ds.person as p
           on a.hh_id=p.hh_id and a.per_id=p.per_id;
quit;

proc sql;
   create table hh_alts_hpw as
      select a.*, w.occup, w.industry, w.primtaz, w.grid_code as grid_id_w
      from hh_alts_hp as a left outer join ds.work as w
           on a.hh_id=w.hh_id and a.per_id=w.per_id;
quit;

proc sql;
   create table hh_alts_hpwg as
      select a.*, zone_id,
                  tt_tw, ttf_sov, ttt_sov, ut_sov, ut_tw, tt_cbd, lwae, lwap, lhae, lhap,
                  hwy, ldhwy, art, ldart, barea, lba,
                  lsfc, lsfcw, lsfi, lsfiw, sfg, nrsf, lnrsfw,
                  rjobs, lrew, ljobsw, s7jobs, s7wd, s8jobs, s8wd, s9jobs, s9wd,
                  ltv, lp, lpw, lalvaw, impv,
                  ldu, lduw, pden, rden, pmiw, pliw, phiw, prwd, piwd, pcwd, powd, pwater,
                  bld_age, yr_blt
      from hh_alts_hpw as a inner join ds.gcs_blk as g
           on a.grid_id =g.grid_id;
quit;

data hh_alts_hpwgz;
   set hh_alts_hpwg;
   from_taz = zone_id;
   to_taz = primtaz;
run;

proc sort data=hh_alts_hpwgz;
by from_taz to_taz;
run;
proc sort data=ds.travel_time;
by from_taz to_taz;
run;

data ds.hh_alts_vars;
   merge hh_alts_hpwgz (IN=a)
         ds.travel_time (IN=t);
   by from_taz to_taz;
   if a;
   if mode = 1 then ttime = t_sov;
   if mode = 2 then ttime = (walk_access_transit_total_time + auto_access_using_P_R_transit_t) / 2;
   if mode = 3 then ttime = (bike_time + walk_time) / 2;
   if mode = 4 then ttime = 0;
   t_sov = SOV_time_in_minutes;
   t_2pv = two_persons_vehicle_time;
   t_3pv = three_persons_vehicle_time;
   tt_wat = walk_access_transit_total_time;
   t_aat =  auto_access_using_P_R_transit_t;
   t_bike = bike_time;
   t_walk = walk_time;
  drop SOV_time_in_minutes two_persons_vehicle_time three_persons_vehicle_time
       walk_access_transit_total_time auto_access_using_P_R_transit_t bike_time walk_time;
run;

proc sort data=ds.hh_alts_vars;
by hh_id cluster mode;
run;

proc export data=ds.hh_alts_vars
outfile="C:\workspace\hh\data\fhh_alts43.csv"
replace;
run;

proc logistic data=hh_alts_hpwgt;
class replicate;
model choice = lp travel_time;
run;

data x;
    set hh_alts_hpwgt;
    decision = choice;
    if replicate <= 12;
run;

proc sql;
   create table _test as
   select hh_id, sum(choice) as sum_choice, count(*) as count from hh_alts_hpwgt group by hh_id;
   select * from _test where sum_choice <> 1 or count <> 16;
run;

proc catmod data=hh_alts_hpwgt;
   model choice=



proc mdc data=hh_alts_hpwgt;
   model choice = cluster / type=clogit nchoice=16
         optmethod=qn covest=hess;
   id hh_id;
run;





/**  cluster code not being used
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














































data test;
     set hh_alts_hpwgt;
     if choice = 1;
run;


proc freq data=test;
    tables cluster*mode;
run;
