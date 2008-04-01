
###New Indicators###

#1.A.5 Absolute Population Per Year

select a.YEAR as YEAR, sum(b.PERSONS) as INDICATORS_VALUE 
from households_exported a inner join households_constants b 
  on a.HOUSEHOLD_ID = b.HOUSEHOLD_ID 
group by a.YEAR;


#1.A.5 Population Net Change Per Year
create table tmp_table1 (YEAR int, POPULATION int);

insert into tmp_table1 (YEAR, POPULATION)
select a.YEAR, sum(b.PERSONS)
from households_exported a inner join households_constants b 
  on a.HOUSEHOLD_ID = b.HOUSEHOLD_ID 
group by a.YEAR;

select b.YEAR as YEAR, (b.POPULATION - a.POPULATION) as INDICATORS_VALUE 
from tmp_table1 a inner join tmp_table1 b 
on a.YEAR = b.YEAR - 1;

drop table tmp_table1;

#1.A.6 Population Moving Per Year
create temporary table tmp_table1 (YEAR int, HOUSEHOLD_ID int);

insert into tmp_table1 (YEAR, HOUSEHOLD_ID)
select b.YEAR, b.HOUSEHOLD_ID
from households_exported a inner join households_exported b
  on a.YEAR+1=b.YEAR and a.HOUSEHOLD_ID=b.HOUSEHOLD_ID
where a.GRID_ID<>b.GRID_ID;

select a.YEAR, sum(b.PERSONS) as INDICATORS_VALUE
from tmp_table1 a inner join households_constants b
  on a.HOUSEHOLD_ID = b.HOUSEHOLD_ID
group by a.YEAR;

drop table tmp_table1;

#1.A.7 Placed Population Per Year
select a.YEAR as YEAR, sum(PERSONS) as INDICATORS_VALUE 
from households_exported a inner join households_constants b
  on a.HOUSEHOLD_ID = b.HOUSEHOLD_ID
where a.GRID_ID > 0
group by a.YEAR;

#1.A.8 Unplaced Population Per Year
create temporary table tmp_table1(YEAR int, POPULATION int);
create temporary table tmp_table2(YEAR int, POPULATION int);

insert into tmp_table1 (YEAR, POPULATION)
select YEAR, 0 from households_exported group by YEAR;

insert into tmp_table2 (YEAR, POPULATION)
select a.YEAR, sum(b.PERSONS) 
from households_exported a inner join households_constants b
  on a.HOUSEHOLD_ID = b.HOUSEHOLD_ID
where a.GRID_ID < 0
group by a.YEAR;

update tmp_table1 as a, tmp_table2 as b
set a.POPULATION = b.POPULATION 
where a.YEAR = b.YEAR;

select YEAR, POPULATION as INDICATORS_VALUE from tmp_table1;

drop table tmp_table1;
drop table tmp_table2;

#1.B.1 Median Household Income
create table tmp_table1(YEAR int, HHINCOME int)

insert into tmp_table1 (YEAR, HHINCOME)
select a.YEAR, b.INCOME 
from households_exported a inner join households_constants b
  on a.HOUSEHOLD_ID = b.HOUSEHOLD_ID;

create index tmp_table1_year_hhincome_index on tmp_table1(YEAR, HHINCOME);

select a.YEAR as YEAR, a.HHINCOME as INDICATORS_VALUE 
from tmp_table1 a inner join tmp_table1 b
  on a.YEAR = b.YEAR
group by a.YEAR, a.HHINCOME
having sum(sign(1-sign(b.HHINCOME-a.HHINCOME))) = floor(count(*)+1)/2);

drop table tmp_table1;

#1.B.2 % No-Car, 1-Car, 2-Car, and >2 Car Households
create temporary table tmp_table1 (YEAR, TOTAL_HOUSEHOLDS int);

insert into tmp_table1 (YEAR,TOTAL_HOUSEHOLDS)
select YEAR, count(*) 
from households_exported
group by YEAR;

select a.YEAR, b.CARS as INDICATORS_SUBTYPE, round(count(*)/c.TOTAL_HOUSEHOLDS,2) as INDICATORS_VALUE 
from households_exported a inner join households_constants b 
  on a.HOUSEHOLD_ID = b.HOUSEHOLD_ID
  inner join tmp_table1 c on a.YEAR = c.YEAR
group by YEAR, CARS;

drop table tmp_table1;


#1.B.3 Population Density
create temporary table tmp_table1 (YEAR int, RESIDENTIAL_LAND double);
create temporary table tmp_table2 (YEAR int, PERSONS int);

insert into tmp_table1 (YEAR, RESIDENTIAL_LAND)
select YEAR, sum(150*150*0.000247*FRACTION_RESIDENTIAL_LAND) from gridcells_exported
group by YEAR;

insert into tmp_table2(YEAR, PERSONS)
select a.YEAR, sum(b.PERSONS)
from households_exported a inner join households_constants b
  on a.HOUSEHOLD_ID = b.HOUSEHOLD_ID
group by YEAR;

select a.YEAR as YEAR, round(a.PERSONS/b.RESIDENTIAL_LAND, 2) as INDICATORS_VALUE 
from tmp_table2 a inner join tmp_table1 b
  on a.YEAR = b.YEAR;

drop table tmp_table1;
drop table tmp_table2;

#1.B.4 Household Density
create temporary table tmp_table1 (YEAR int, RESIDENTIAL_LAND double);
create temporary table tmp_table2 (YEAR int, HOUSEHOLDS int);

insert into tmp_table1 (YEAR, RESIDENTIAL_LAND)
select YEAR, sum(150*150*0.000247*FRACTION_RESIDENTIAL_LAND) from gridcells_exported
group by YEAR;

insert into tmp_table2(YEAR, HOUSEHOLDS)
select a.YEAR, count(*)
from households_exported
group by YEAR;

select a.YEAR as YEAR, round(a.HOUSEHOLDS/b.RESIDENTIAL_LAND, 2) as INDICATORS_VALUE 
from tmp_table2 a inner join tmp_table1 b
  on a.YEAR = b.YEAR;

drop table tmp_table1;
drop table tmp_table2;

#2.B.3 Jobs per Capita
create temporary table tmp_table1 (YEAR int, JOBS int);
create temporary table tmp_table2 (YEAR int, PERSONS int);

insert into tmp_table1 (YEAR, JOBS)
select YEAR, count(*) from jobs_exported group by YEAR;

insert into tmp_table2 (YEAR, PERSONS)
select a.YEAR, sum(b.PERSONS) 
from households_exported a inner join households_constants b
  on a.HOUSEHOLD_ID = b.HOUSEHOLD_ID
group by a.YEAR;

select a.YEAR as YEAR, round(a.JOBS/b.PERSONS, 2) as INDICATORS_VALUE 
from tmp_table1 a inner join tmp_table2 b
  on a.YEAR = b.YEAR;

drop table tmp_table1;
drop table tmp_table2;

#2.B.3 Jobs/Housing Balance
create temporary table tmp_table1 (YEAR int, JOBS int);
create temporary table tmp_table2 (YEAR int, UNITS int);

insert into tmp_table1 (YEAR, JOBS)
select YEAR, count(*) from jobs_exported group by YEAR;

insert into tmp_table2 (YEAR, UNITS)
select YEAR, sum(RESIDENTIAL_UNITS) 
from gridcells_exported
group by YEAR;

select a.YEAR as YEAR, round(a.JOBS/b.UNITS, 2) as INDICATORS_VALUE 
from tmp_table1 a inner join tmp_table2 b
  on a.YEAR = b.YEAR;

drop table tmp_table1;
drop table tmp_table2;

#2.B.3 Employment Density
create temporary table tmp_table1 (YEAR int, JOBS int);
create temporary table tmp_table2 (YEAR int, NON_RESIDENTIAL_LAND double);

insert into tmp_table1 (YEAR, JOBS)
select YEAR, count(*) from jobs_exported group by YEAR;

insert into tmp_table2 (YEAR, NON_RESIDENTIAL_LAND)
select YEAR, sum(150*150*0.000247*(1-FRACTION_RESIDENTIAL_LAND)) from gridcells_exported
group by YEAR;

select a.YEAR as YEAR, round(a.JOBS/b.NON_RESIDENTIAL_LAND, 2) as INDICATORS_VALUE 
from tmp_table1 a inner join tmp_table2 b
  on a.YEAR = b.YEAR;

drop table tmp_table1;
drop table tmp_table2;

#3.B.5 Dwelling Density
select YEAR, round(sum(RESIDENTIAL_UNITS)/sum(150*150*0.000247*FRACTION_RESIDENTIAL_LAND), 2) as INDICATORS_VALUE
from gridcells_exported
group by YEAR;

#7.B.1 Land converted from development type 24, by Development type by year
select b.YEAR, b.DEVELOPMENT_TYPE_ID as INDICATORS_SUBTYPE, count(*) as INDICATORS_VALUE
from gridcells_exported a inner join gridcells_exported b
  on a.YEAR = b.YEAR - 1  and a.GRID_ID = b.GRID_ID
where a. DEVELOPMENT_TYPE_ID = 24 and b.DEVELOPMENT_TYPE_ID between 1 and 23
group by b.YEAR, b.DEVELOPMENT_TYPE_ID;


#############################################################################


##indicators ver 2, using households_exported and households_constants joined table.

create temporary table tmp_table0 (YEAR int, HOUSEHOLD_ID int, GRID_ID int, PERSONS int, CARS int, INCOME int);

insert into tmp_table0 (YEAR, HOUSEHOLD_ID, GRID_ID, PERSONS, CARS, INCOME)
select a.YEAR, a.HOUSEHOLD_ID,a.GRID_ID,b.PERSONS,b.CARS,b.INCOME
from households_exported a inner join households_constants b
  on a.HOUSEHOLD_ID = b.HOUSEHOLD_ID;

create index tmp_table0_year_household_id_grid_id_index on tmp_table0 (year,household_id,grid_id);

create table tmp_table00 (YEAR int, POPULATION int);

insert into tmp_table00 (YEAR, POPULATION)
select YEAR, sum(PERSONS) as INDICATORS_VALUE 
from tmp_table0
group by YEAR;


#1.A.5 Absolute Population Per Year
select YEAR, POPULATION as INDICATORS_VALUE 
from tmp_table00;

#1.A.5 Population Net Change Per Year
select b.YEAR as YEAR, (b.POPULATION - a.POPULATION) as INDICATORS_VALUE 
from tmp_table00 a inner join tmp_table00 b 
on a.YEAR = b.YEAR - 1;

#1.A.6 Population Moving Per Year
create temporary table tmp_table1 (YEAR int, HOUSEHOLD_ID int);

insert into tmp_table1 (YEAR, HOUSEHOLD_ID)
select b.YEAR, b.HOUSEHOLD_ID
from households_exported a inner join households_exported b
  on a.YEAR+1=b.YEAR and a.HOUSEHOLD_ID=b.HOUSEHOLD_ID
where a.GRID_ID<>b.GRID_ID;

select a.YEAR, sum(b.PERSONS) as INDICATORS_VALUE
from tmp_table1 a inner join households_constants b
  on a.HOUSEHOLD_ID = b.HOUSEHOLD_ID
group by a.YEAR;

drop table tmp_table1;

#1.A.7 Placed Population Per Year
select YEAR, sum(PERSONS) as INDICATORS_VALUE 
from tmp_table0
where GRID_ID > 0
group by YEAR;

#1.A.8 Unplaced Population Per Year
create temporary table tmp_table1(YEAR int, POPULATION int);
create temporary table tmp_table2(YEAR int, POPULATION int);

insert into tmp_table1 (YEAR, POPULATION)
select YEAR, 0 from households_exported group by YEAR;

insert into tmp_table2 (YEAR, POPULATION)
select YEAR, sum(PERSONS) 
from tmp_table0
where GRID_ID < 0
group by YEAR;

update tmp_table1 as a, tmp_table2 as b
set a.POPULATION = b.POPULATION 
where a.YEAR = b.YEAR;

select YEAR, POPULATION as INDICATORS_VALUE from tmp_table1;

drop table tmp_table1;
drop table tmp_table2;

#1.B.1 Median Household Income
create table tmp_table1(YEAR int, HHINCOME int);

insert into tmp_table1 (YEAR, HHINCOME)
select YEAR, INCOME 
from tmp_table0;

create index tmp_table1_year_hhincome_index on tmp_table1(YEAR, HHINCOME);

select a.YEAR as YEAR, a.HHINCOME as INDICATORS_VALUE 
from tmp_table1 a inner join tmp_table1 b
  on a.YEAR = b.YEAR
group by a.YEAR, a.HHINCOME
having sum(sign(1-sign(b.HHINCOME-a.HHINCOME))) = floor((count(*)+1)/2);

drop table tmp_table1;

#1.B.2 % No-Car, 1-Car, 2-Car, and >2 Car Households
create temporary table tmp_table1 (YEAR, TOTAL_HOUSEHOLDS int);

insert into tmp_table1 (YEAR,TOTAL_HOUSEHOLDS)
select YEAR, count(*) 
from households_exported
group by YEAR;

select a.YEAR, a.CARS as INDICATORS_SUBTYPE, round(count(a.*)/c.TOTAL_HOUSEHOLDS,2) as INDICATORS_VALUE 
from tmp_table0 a
  inner join tmp_table1 c on a.YEAR = c.YEAR
group by YEAR, CARS;

drop table tmp_table1;


#1.B.3 Population Density
create temporary table tmp_table1 (YEAR int, RESIDENTIAL_LAND double);

insert into tmp_table1 (YEAR, RESIDENTIAL_LAND)
select YEAR, sum(150*150*0.000247*FRACTION_RESIDENTIAL_LAND) from gridcells_exported
group by YEAR;

select a.YEAR as YEAR, round(a.POPULATION/b.RESIDENTIAL_LAND, 2) as INDICATORS_VALUE 
from tmp_table00 a inner join tmp_table1 b
  on a.YEAR = b.YEAR;

drop table tmp_table1;

#1.B.4 Household Density
create temporary table tmp_table1 (YEAR int, RESIDENTIAL_LAND double);
create temporary table tmp_table2 (YEAR int, HOUSEHOLDS int);

insert into tmp_table1 (YEAR, RESIDENTIAL_LAND)
select YEAR, sum(150*150*0.000247*FRACTION_RESIDENTIAL_LAND) from gridcells_exported
group by YEAR;

insert into tmp_table2(YEAR, HOUSEHOLDS)
select a.YEAR, count(*)
from households_exported
group by YEAR;

select a.YEAR as YEAR, round(a.HOUSEHOLDS/b.RESIDENTIAL_LAND, 2) as INDICATORS_VALUE 
from tmp_table2 a inner join tmp_table1 b
  on a.YEAR = b.YEAR;

drop table tmp_table1;
drop table tmp_table2;

#2.B.3 Jobs per Capita
create temporary table tmp_table1 (YEAR int, JOBS int);
create temporary table tmp_table2 (YEAR int, PERSONS int);

insert into tmp_table1 (YEAR, JOBS)
select YEAR, count(*) from jobs_exported group by YEAR;

select a.YEAR as YEAR, round(a.JOBS/b.POPULATION, 2) as INDICATORS_VALUE 
from tmp_table1 a inner join tmp_table00 b
  on a.YEAR = b.YEAR;

drop table tmp_table1;

#2.B.3 Jobs/Housing Balance
create temporary table tmp_table1 (YEAR int, JOBS int);
create temporary table tmp_table2 (YEAR int, UNITS int);

insert into tmp_table1 (YEAR, JOBS)
select YEAR, count(*) from jobs_exported group by YEAR;

insert into tmp_table2 (YEAR, UNITS)
select YEAR, sum(RESIDENTIAL_UNITS) 
from gridcells_exported
group by YEAR;

select a.YEAR as YEAR, round(a.JOBS/b.UNITS, 2) as INDICATORS_VALUE 
from tmp_table1 a inner join tmp_table2 b
  on a.YEAR = b.YEAR;

drop table tmp_table1;
drop table tmp_table2;

#2.B.3 Employment Density
create temporary table tmp_table1 (YEAR int, JOBS int);
create temporary table tmp_table2 (YEAR int, NON_RESIDENTIAL_LAND double);

insert into tmp_table1 (YEAR, JOBS)
select YEAR, count(*) from jobs_exported group by YEAR;

insert into tmp_table2 (YEAR, NON_RESIDENTIAL_LAND)
select YEAR, sum(150*150*0.000247*(1-FRACTION_RESIDENTIAL_LAND)) from gridcells_exported
group by YEAR;

select a.YEAR as YEAR, round(a.JOBS/b.NON_RESIDENTIAL_LAND, 2) as INDICATORS_VALUE 
from tmp_table1 a inner join tmp_table2 b
  on a.YEAR = b.YEAR;

drop table tmp_table1;
drop table tmp_table2;

#3.B.5 Dwelling Density
select YEAR, round(sum(RESIDENTIAL_UNITS)/sum(150*150*0.000247*FRACTION_RESIDENTIAL_LAND), 2) as INDICATORS_VALUE
from gridcells_exported
group by YEAR;

#7.B.1 Land converted from development type 24, by Development type by year
select b.YEAR, b.DEVELOPMENT_TYPE_ID as INDICATORS_SUBTYPE, count(*) as INDICATORS_VALUE
from gridcells_exported a inner join gridcells_exported b
  on a.YEAR = b.YEAR - 1  and a.GRID_ID = b.GRID_ID
where a. DEVELOPMENT_TYPE_ID = 24 and b.DEVELOPMENT_TYPE_ID between 1 and 23
group by b.YEAR, b.DEVELOPMENT_TYPE_ID;


