create index hh on households_exported(household_id);
create index hh on households_constants(household_id);
create index hh on jobs_exported(job_id);
create index hh on jobs_constants(job_id);
create index grid on gridcells_exported(grid_id);

create table households_exported03
select * from households_exported where year=2003;

create table jobs_exported03
select * from jobs_exported where year=2003;


create table gridcells_exported03
select * from gridcells_exported where year=2003;

create index hh on households_exported03(household_id);
create index jobs on jobs_exported03(job_id);
create index grid on gridcells_exported03(grid_id);


Create temporary table column1
SELECT households_exported03.zone_id as ZONE, count(households_constants.persons) as TOTHH 
FROM households_exported03, households_constants
WHERE households_constants.household_id = households_exported03.household_id group by zone;

create temporary table tmp_table1
select households_exported03.zone_id as ZONE, households_constants.persons as SIZE
from households_exported03, households_constants 
where households_constants.household_id = households_exported03.household_id;

alter table tmp_table1 add column(HH1 int(1));
alter table tmp_table1 add column(HH2 int(1));
alter table tmp_table1 add column(HH3 int(1));
alter table tmp_table1 add column(HH4 int(1));
alter table tmp_table1 add column(HH5 double);
alter table tmp_table1 add column(HH6 double);
alter table tmp_table1 add column(pop double);


update tmp_table1 set HH1=1 where size=1;
update tmp_table1 set HH2=1 where size=2;
update tmp_table1 set HH3=1 where size=3;
update tmp_table1 set HH4=1 where size=4;
update tmp_table1 set HH5=.432 where size=5;
update tmp_table1 set HH6=.568 where size=5;

update tmp_table1 set pop=5.8 where SIZE=5;
update tmp_table1 set pop=4 where SIZE=4;
update tmp_table1 set pop=3 where SIZE=3;
update tmp_table1 set pop=2 where SIZE=2;
update tmp_table1 set pop=1 where SIZE=1;

create temporary table column2
select zone as ZONE, sum(hh1) as HH1, sum(hh2) as HH2, sum(hh3) as HH3, sum(hh4) as HH4, sum(hh5) as HH5,
sum(hh6) as HH6, sum(pop) as POPULATION from tmp_table1 group by zone;

Create TEMPORARY TABLE column3
select gridcells.zone_id as ZONE, sum(gridcells_exported03.residential_units) as TOTDWL
from gridcells, gridcells_exported03 
where gridcells.grid_id=gridcells_exported03.grid_id group by zone_id;


create temporary table tmp_table2
select households_exported03.zone_id as ZONE, households_constants.income as INCOME 
from households_exported03, households_constants 
where households_exported03.household_id=households_constants.household_id;

create temporary table column4
select ZONE, avg(income) as INCOME from tmp_table2 group by zone;

create temporary table tmp_table3
select jobs_exported03.zone_id as ZONE, jobs_constants.sector_id as SECTOR 
from jobs_exported03, jobs_constants 
where jobs_exported03.job_id=jobs_constants.job_id;

alter table tmp_table3 add column(TOT int(1));
alter table tmp_table3 add column(RET int(1));
alter table tmp_table3 add column(IND int(1));
alter table tmp_table3 add column(OTH int(1));

update tmp_table3 set TOT=1 where SECTOR>2;
update tmp_table3 set RET=1 where SECTOR=6 or SECTOR=7 or SECTOR=8;
update tmp_table3 set IND=1 where ZONE<1000 and SECTOR=3;
update tmp_table3 set IND=1 where ZONE<1000 and SECTOR=4;
update tmp_table3 set OTH=1 where SECTOR=5 or sector=9 or sector=10 or sector=11
   or sector=12 or sector=13 or sector=14;
update tmp_table3 set OTH=1 where ZONE>1000 and SECTOR=3;
update tmp_table3 set OTH=1 where ZONE>1000 and SECTOR=4;

create temporary table column5
select zone, sum(TOT) as TOTEMP, sum(RET) as RETEMP, sum(IND) as INDEMP, sum(OTH) OTHEMP from tmp_table3
group by zone;

create temporary table tmp_table4
select households_exported03.zone_id as ZONE, households_constants.workers as WORKERS 
from households_exported03, households_constants where
households_exported03.household_id=households_constants.household_id;

create temporary table column6
select zone, sum(workers) as WORKERS from tmp_table4 group by zone;

create temporary table TEMP1
select zones.zone_id as ZONE,
       column1.TOTHH as TOTHH1
from zones, column1 where zones.zone_id=column1.zone;

alter table temp1 add column(TOTHH int(8));
update temp1 set tothh=tothh1;

create temporary table TEMP2
select TEMP1.zone as ZONE,
       TEMP1.TOTHH as TOTHH,
       column2.HH1 as HH1,
       column2.HH2 as HH2,
       column2.HH3 as HH3,
       column2.HH4 as HH4,
       column2.HH5 as HH5,
       column2.HH6 as HH6,
       column2.POPULATION as POPULATION
from TEMP1, column2 where TEMP1.ZONE=column2.zone;

create temporary table TEMP3
select TEMP2.*,
       column3.TOTDWL as TOTDWL
from TEMP2, column3 where TEMP2.ZONE=column3.zone;

create temporary table TEMP4
select TEMP3.*,
       column4.INCOME as INCOME
from TEMP3, column4 where TEMP3.ZONE=column4.zone;

create temporary table TEMP5
select TEMP4.*,
       column5.TOTEMP as TOTEMP,
       column5.RETEMP as RETEMP,
       column5.INDEMP as INDEMP,
       column5.OTHEMP as OTHEMP
from TEMP4, column5 where TEMP4.ZONE=column5.zone;

create table TRAVEL_MODEL_INPUT
select TEMP5.*,
       column6.WORKERS as WORKERS
from TEMP5, column6 where TEMP5.ZONE=column6.zone;


 








