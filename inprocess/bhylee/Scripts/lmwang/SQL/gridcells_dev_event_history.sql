set session tmp_table_size  = 16 * 1024 * 1024 * 1024;
set session max_heap_table_size = 1 * 1024 * 1024 * 1024;

 # UrbanSim software.
 # Copyright (C) 1998-2004 University of Washington
 #
 # You can redistribute this program and/or modify it under the
 # terms of the GNU General Public License as published by the
 # Free Software Foundation (http://www.gnu.org/copyleft/gpl.html).
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # file LICENSE.htm for copyright and licensing information, and the
 # file ACKNOWLEDGMENTS.htm for funding and other acknowledgments.
 #
  
 # Author: Liming Wang
 # Program: SQL Query
 # Description:
 
--create development_event_history table for baseyear database
--input database:
--  PSRC_2000_estimation_petecaba, PSRC_parcels_all_counties, PSRC_parcels_king, PSRC_parcels_kitsap, PSRC_parcels_pierce,PSRC_parcels_snohomish
--input tables;
--  parcels, land_use_generic_reclass, parcel_fractions_in_gridcells, 
--  buildings, building_use_generic_reclass,
--  development_types

use PSRC_parcels_all_counties;

--Step 1.
--<parcels_fractions_in_gridcells>
set @step = '1';
set @work = 'parcels_fractions_in_gridcells';
select @step as STEP, @work as NOW_WORKING;

--create parcels_fractions_in_gridcells for all four counties
--drop table if exists parcel_fractions_in_gridcells;
-- create table parcel_fractions_in_gridcells
-- select * from PSRC_parcels_king.parcel_fractions_in_gridcells;

-- insert into parcel_fractions_in_gridcells
-- select PARCEL_ID,GRID_ID,PARCEL_FRACTION,COUNTY from PSRC_parcels_kitsap.parcel_fractions_in_gridcells;

-- insert into parcel_fractions_in_gridcells
-- select PARCEL_ID,GRID_ID,PARCEL_FRACTION,COUNTY from PSRC_parcels_pierce.parcel_fractions_in_gridcells;

-- insert into parcel_fractions_in_gridcells
-- select PARCEL_ID,GRID_ID,PARCEL_FRACTION,COUNTY from PSRC_parcels_snohomish.parcel_fractions_in_gridcells;

-- create index parcel_fractions_in_gridcells_parcel_id_grid_id_county_index
-- 	on parcel_fractions_in_gridcells (parcel_id,grid_id,county);
--</parcels_fractions_in_gridcells>

-- Step 2a. create parcels table with all necessary fields

--<deh_ptemp_units_impv_by_parcel>
set @step = '2a';
set @work = 'deh_ptemp_units_impv_by_parcel';
select @step as STEP, @work as NOW_WORKING;

drop table if exists deh_ptemp_units_impv_by_parcel;
create table deh_ptemp_units_impv_by_parcel (
	PARCEL_ID char(12),
	COUNTY char(3),
	GENERIC_LAND_USE_2 char(3),
	RESIDENTIAL_UNITS double,
	IMPROVEMENT_VALUE int,
	RESIDENTIAL_IMPROVEMENT_VALUE bigint,
	COMMERCIAL_IMPROVEMENT_VALUE bigint,
	INDUSTRIAL_IMPROVEMENT_VALUE bigint,
	GOVERNMENTAL_IMPROVEMENT_VALUE bigint
);

insert into deh_ptemp_units_impv_by_parcel
	(PARCEL_ID,COUNTY,GENERIC_LAND_USE_2,RESIDENTIAL_UNITS,IMPROVEMENT_VALUE)
select 
	p.PARCEL_ID,
	p.COUNTY,
	l.GENERIC_LAND_USE_2,
	p.RESIDENTIAL_UNITS_IMPUTED,
	p.IMPROVEMENT_VALUE
from
	parcels p 
	  inner join 
	land_use_generic_reclass l
	  on p.county = l.county 
	  and p.land_use = l.county_land_use_code
;

update
 	deh_ptemp_units_impv_by_parcel
set RESIDENTIAL_IMPROVEMENT_VALUE = IMPROVEMENT_VALUE
where
 	GENERIC_LAND_USE_2 = "R"
;

update
	deh_ptemp_units_impv_by_parcel
set COMMERCIAL_IMPROVEMENT_VALUE = IMPROVEMENT_VALUE
where
	GENERIC_LAND_USE_2 = "C"
;

update
	deh_ptemp_units_impv_by_parcel
set INDUSTRIAL_IMPROVEMENT_VALUE = IMPROVEMENT_VALUE
where
	GENERIC_LAND_USE_2 = "I"
;

update
	deh_ptemp_units_impv_by_parcel
set GOVERNMENTAL_IMPROVEMENT_VALUE = IMPROVEMENT_VALUE
where
	GENERIC_LAND_USE_2 = "G"
;

create index 
	deh_ptemp_units_impv_by_parcel_parcel_id_county_index
on
	deh_ptemp_units_impv_by_parcel
	(PARCEL_ID, COUNTY)
;

--</deh_ptemp_units_impv_by_parcel>

-- step 2b. extract built sqft from buildings table;
--<deh_btemp_sqft_by_parcel_year_use>
set @step = '2b';
set @work = 'deh_btemp_sqft_by_parcel_year_use';
select @step as STEP, @work as NOW_WORKING;

drop table if exists deh_btemp_sqft_by_parcel_year_use;
--## create table from merged buildings table
create table
	deh_btemp_sqft_by_parcel_year_use
select
	p.PARCEL_ID,
	p.COUNTY,
	p.YEAR_BUILT,
	u.GENERIC_BUILDING_USE_2 as BUILDING_USE,
	count(*) as NUM_BUILDINGS,
	sum(p.IMPUTED_SQFT) as BUILT_SQFT
from
	buildings p
	  inner join
	PSRC_2000_data_quality_indicators.building_use_generic_reclass u
	  on p.COUNTY = u.COUNTY
	  and p.BUILDING_USE = u.COUNTY_BUILDING_USE_CODE
where
	u.GENERIC_BUILDING_USE_2 in ('C','G','I','R')
group by
	p.PARCEL_ID,
	p.YEAR_BUILT,
	u.GENERIC_BUILDING_USE_2
;

alter table deh_btemp_sqft_by_parcel_year_use
add RESIDENTIAL_SQFT double,
add COMMERCIAL_SQFT double,
add INDUSTRIAL_SQFT double,
add GOVERNMENTAL_SQFT double
;

update deh_btemp_sqft_by_parcel_year_use
set RESIDENTIAL_SQFT = BUILT_SQFT
where BUILDING_USE = 'R';

update deh_btemp_sqft_by_parcel_year_use
set COMMERCIAL_SQFT = BUILT_SQFT
where BUILDING_USE = 'C';

update deh_btemp_sqft_by_parcel_year_use
set INDUSTRIAL_SQFT = BUILT_SQFT
where BUILDING_USE = 'I';

update deh_btemp_sqft_by_parcel_year_use
set GOVERNMENTAL_SQFT = BUILT_SQFT
where BUILDING_USE = 'G';

create index
	deh_btemp_sqft_by_parcel_year_use_parcel_id_county_index
on
	deh_btemp_sqft_by_parcel_year_use
	(PARCEL_ID, COUNTY, YEAR_BUILT)
;
--</deh_btemp_sqft_by_parcel_year_use>

-- step 2c. create  tables summarize num of buildings and total built sqft in parcel
--<btemp_table_r_i_c_g>
set @step = '2c';
set @work = 'btemp_table_r,i,c,g';
select @step as STEP, @work as NOW_WORKING;

create temporary table btemp_table_r
select
	PARCEL_ID,
	COUNTY,
	sum(NUM_BUILDINGS) as TOTAL_RES_BUILDINGS_IN_PARCEL,
	sum(RESIDENTIAL_SQFT) as TOTAL_RES_SQFT_IN_PARCEL
from deh_btemp_sqft_by_parcel_year_use
where BUILDING_USE = 'R'
group by 
	PARCEL_ID, 
	COUNTY
;

create temporary table btemp_table_c
select
	PARCEL_ID,
	COUNTY,
	sum(NUM_BUILDINGS) as TOTAL_COM_BUILDINGS_IN_PARCEL,
	sum(COMMERCIAL_SQFT) as TOTAL_COM_SQFT_IN_PARCEL
from deh_btemp_sqft_by_parcel_year_use
where BUILDING_USE = 'C'
group by 
	PARCEL_ID,
	COUNTY
;

create temporary  table btemp_table_i
select
	PARCEL_ID,
	COUNTY,
	sum(NUM_BUILDINGS) as TOTAL_IND_BUILDINGS_IN_PARCEL,
	sum(INDUSTRIAL_SQFT) as TOTAL_IND_SQFT_IN_PARCEL
from deh_btemp_sqft_by_parcel_year_use
where BUILDING_USE = 'I'
group by 
	PARCEL_ID, 
	COUNTY
;

create temporary table btemp_table_g
select
	PARCEL_ID,
	COUNTY,
	sum(NUM_BUILDINGS) as TOTAL_GOV_BUILDINGS_IN_PARCEL,
	sum(GOVERNMENTAL_SQFT) as TOTAL_GOV_SQFT_IN_PARCEL
from deh_btemp_sqft_by_parcel_year_use
where BUILDING_USE = 'G'
group by
	PARCEL_ID, 
	COUNTY
;

create index btemp_table_r_parcel_id_county_index
on btemp_table_r (PARCEL_ID, COUNTY);

create index btemp_table_c_parcel_id_county_index
on btemp_table_c (PARCEL_ID, COUNTY);

create index btemp_table_i_parcel_id_county_index
on btemp_table_i (PARCEL_ID, COUNTY);

create index btemp_table_g_parcel_id_county_index
on btemp_table_g (PARCEL_ID, COUNTY);
--</btemp_table_r_i_c_g>

-- step 2d. add parcel level summary info
--<deh_btemp_sqft_by_parcel_year_use>
set @step = '2d';
set @work = 'deh_btemp_sqft_by_parcel_year_use';
select @step as STEP, @work as NOW_WORKING;

alter table deh_btemp_sqft_by_parcel_year_use
add TOTAL_RES_BUILDINGS_IN_PARCEL int,
add TOTAL_RES_SQFT_IN_PARCEL double,
add TOTAL_COM_BUILDINGS_IN_PARCEL int,
add TOTAL_COM_SQFT_IN_PARCEL double,
add TOTAL_IND_BUILDINGS_IN_PARCEL int,
add TOTAL_IND_SQFT_IN_PARCEL double,
add TOTAL_GOV_BUILDINGS_IN_PARCEL int,
add TOTAL_GOV_SQFT_IN_PARCEL double
;

update 
	deh_btemp_sqft_by_parcel_year_use t, btemp_table_r r
set t.TOTAL_RES_BUILDINGS_IN_PARCEL = r.TOTAL_RES_BUILDINGS_IN_PARCEL,
    t.TOTAL_RES_SQFT_IN_PARCEL = r.TOTAL_RES_SQFT_IN_PARCEL
where t.parcel_id = r.parcel_id 
  and t.county = r.county
;

update 
	deh_btemp_sqft_by_parcel_year_use t, btemp_table_c c
set t.TOTAL_COM_BUILDINGS_IN_PARCEL = c.TOTAL_COM_BUILDINGS_IN_PARCEL,
    t.TOTAL_COM_SQFT_IN_PARCEL = c.TOTAL_COM_SQFT_IN_PARCEL
where t.parcel_id = c.parcel_id 
  and t.county = c.county
;

update 
	deh_btemp_sqft_by_parcel_year_use t, btemp_table_i i
set t.TOTAL_IND_BUILDINGS_IN_PARCEL = i.TOTAL_IND_BUILDINGS_IN_PARCEL,
    t.TOTAL_IND_SQFT_IN_PARCEL = i.TOTAL_IND_SQFT_IN_PARCEL
where t.parcel_id = i.parcel_id 
  and t.county = i.county
;

update 
	deh_btemp_sqft_by_parcel_year_use t, btemp_table_g g
set t.TOTAL_GOV_BUILDINGS_IN_PARCEL = g.TOTAL_GOV_BUILDINGS_IN_PARCEL,
    t.TOTAL_GOV_SQFT_IN_PARCEL = g.TOTAL_GOV_SQFT_IN_PARCEL
where t.parcel_id = g.parcel_id 
  and t.county = g.county
;

--</deh_btemp_sqft_by_parcel_year_use>

--step 2f. create table including sqft, units, improve_value combining buildings and parcels table
--<deh_ctemp_sqft_units_by_parcel_year_use>
---- by inner join, we omit all records either not in parcels table or buildings table
set @step = '2f';
set @work = 'deh_ctemp_sqft_units_by_parcel_year_use';
select @step as STEP, @work as NOW_WORKING;

drop table if exists deh_ctemp_sqft_units_by_parcel_year_use;
create table
	deh_ctemp_sqft_units_by_parcel_year_use
select
	b.PARCEL_ID,
	b.COUNTY,
	b.YEAR_BUILT,
	b.BUILDING_USE,
	b.NUM_BUILDINGS,
	b.COMMERCIAL_SQFT,
	b.INDUSTRIAL_SQFT,
	b.GOVERNMENTAL_SQFT,
	b.TOTAL_RES_BUILDINGS_IN_PARCEL,
	p.RESIDENTIAL_UNITS as TOTAL_RES_UNITS_IN_PARCEL
from 	deh_btemp_sqft_by_parcel_year_use b
	  inner join deh_ptemp_units_impv_by_parcel p
	  on b.PARCEL_ID = p.PARCEL_ID
	  and b.COUNTY = p.COUNTY
;

create index deh_ctemp_sqft_units_by_parcel_year_use_index
on deh_ctemp_sqft_units_by_parcel_year_use (PARCEL_ID,COUNTY,YEAR_BUILT);

alter table deh_ctemp_sqft_units_by_parcel_year_use
add RESIDENTIAL_UNITS double
;

---###### Assign residential units to development events ######---
-- scheme 1. assign units evenly by num of buildings in a parcel
update 
	deh_ctemp_sqft_units_by_parcel_year_use
set
	RESIDENTIAL_UNITS = TOTAL_RES_UNITS_IN_PARCEL * NUM_BUILDINGS / TOTAL_RES_BUILDINGS_IN_PARCEL
where
	TOTAL_RES_BUILDINGS_IN_PARCEL > 0
	and TOTAL_RES_BUILDINGS_IN_PARCEL is not null
	and BUILDING_USE = 'R'
;

-- scheme 2. assign units evenly by (residential) built sqft
-- update 
-- 	deh_btemp_sqft_by_parcel_year_use
-- set
-- 	RESIDENTIAL_UNITS = TOTAL_RES_UNITS_IN_PARCEL * BUILT_SQFT / TOTAL_RES_SQFT_IN_PARCEL
-- where
-- 	TOTAL_RES_SQFT_IN_PARCEL <> 0
-- 	and TOTAL_RES_SQFT_IN_PARCEL is not null
-- ;

-- diagnose needed here to compare rounded building residential units to parcels

update deh_ctemp_sqft_units_by_parcel_year_use
set 
	COMMERCIAL_SQFT = 0
where COMMERCIAL_SQFT is NULL;

update deh_ctemp_sqft_units_by_parcel_year_use
set 
	INDUSTRIAL_SQFT = 0
where INDUSTRIAL_SQFT is NULL;

update deh_ctemp_sqft_units_by_parcel_year_use
set 
	GOVERNMENTAL_SQFT = 0
where GOVERNMENTAL_SQFT is NULL;

update deh_ctemp_sqft_units_by_parcel_year_use
set 
	RESIDENTIAL_UNITS = 0
where RESIDENTIAL_UNITS is NULL;

drop table if exists deh_ctemp_sqft_units_by_parcel_year;
create table deh_ctemp_sqft_units_by_parcel_year
select
	PARCEL_ID,
	COUNTY,
	YEAR_BUILT,
	sum(COMMERCIAL_SQFT) as COMMERCIAL_SQFT,
	sum(INDUSTRIAL_SQFT) as INDUSTRIAL_SQFT,
	sum(GOVERNMENTAL_SQFT) as GOVERNMENTAL_SQFT,
	sum(RESIDENTIAL_UNITS) as RESIDENTIAL_UNITS
from deh_ctemp_sqft_units_by_parcel_year_use
group by
	PARCEL_ID,
	COUNTY,
	YEAR_BUILT
;

create index index_parcel_id_county_year_built
 on deh_ctemp_sqft_units_by_parcel_year (parcel_id, county, year_built)
;
create index index_county_year_built
 on deh_ctemp_sqft_units_by_parcel_year (county, year_built)
;


---###### Assign improvement_value to development events ######---
-- step 2e. create avg impv by county to be used to assign improvement values to events
--<deh_temp_avg_impv_by_county>
set @step = '2e';
set @work = 'deh_temp_avg_impv_by_county';
select @step as STEP, @work as NOW_WORKING;

drop table if exists deh_temp_avg_impv_by_county;
create table deh_temp_avg_impv_by_county
select
	su.county,
	sum(IF(su.RESIDENTIAL_UNITS<>0, RESIDENTIAL_IMPROVEMENT_VALUE, 0)) as TOTAL_RES_IMPV,
	sum(IF(su.COMMERCIAL_SQFT<>0, COMMERCIAL_IMPROVEMENT_VALUE, 0)) as TOTAL_COM_IMPV,
	sum(IF(su.INDUSTRIAL_SQFT<>0, INDUSTRIAL_IMPROVEMENT_VALUE, 0)) as TOTAL_IND_IMPV,
	sum(IF(su.GOVERNMENTAL_SQFT<>0, GOVERNMENTAL_IMPROVEMENT_VALUE, 0)) as TOTAL_GOV_IMPV,

	sum(su.RESIDENTIAL_UNITS) as TOTAL_RES_UNITS,
	sum(su.COMMERCIAL_SQFT) as TOTAL_COM_SQFT,
	sum(su.INDUSTRIAL_SQFT) as TOTAL_IND_SQFT,
	sum(su.GOVERNMENTAL_SQFT) as TOTAL_GOV_SQFT
from deh_ptemp_units_impv_by_parcel imp
	inner join deh_ctemp_sqft_units_by_parcel_year su
	  on imp.parcel_id = su.parcel_id
	    and imp.county = su.county
where (su.county in ('033','053','061') and su.year_built = 2000)
	or (su.county = '035' and su.year_built = 1997)
group by
	su.county
;

alter table deh_temp_avg_impv_by_county
add AVG_RES_IMPV float,
add AVG_COM_IMPV float,
add AVG_IND_IMPV float,
add AVG_GOV_IMPV float
;

update deh_temp_avg_impv_by_county
set 
	AVG_RES_IMPV = TOTAL_RES_IMPV / TOTAL_RES_UNITS,
	AVG_COM_IMPV = TOTAL_COM_IMPV / TOTAL_COM_SQFT,
	AVG_IND_IMPV = TOTAL_IND_IMPV / TOTAL_IND_SQFT,
	AVG_GOV_IMPV = TOTAL_GOV_IMPV / TOTAL_GOV_SQFT
;

create index index_county on deh_temp_avg_impv_by_county (county);
--</deh_ctemp_avg_impv_by_county>

-- step 2g. assign improvement value to buildings
--scheme 1. Assign improvement value evenly by avg improvement value by sqft

drop table if exists deh_ctemp_sqft_units_impv_by_parcel_year;
create table deh_ctemp_sqft_units_impv_by_parcel_year
select
	su.*,
	su.RESIDENTIAL_UNITS * a.AVG_RES_IMPV as RESIDENTIAL_IMPROVEMENT_VALUE,
	su.COMMERCIAL_SQFT * a.AVG_COM_IMPV as COMMERCIAL_IMPROVEMENT_VALUE,
	su.INDUSTRIAL_SQFT * a.AVG_IND_IMPV as INDUSTRIAL_IMPROVEMENT_VALUE,
	su.GOVERNMENTAL_SQFT * a.AVG_GOV_IMPV as GOVERNMENTAL_IMPROVEMENT_VALUE
from 
	deh_ctemp_sqft_units_by_parcel_year su
	  inner join deh_temp_avg_impv_by_county a
	    on su.county = a.county
;

create index index_parcel_id_county on deh_ctemp_sqft_units_impv_by_parcel_year (parcel_id, county);
create index index_year_built on deh_ctemp_sqft_units_impv_by_parcel_year (year_built);

---- table deh_ctemp_sqft_units_impv_by_parcel_year_use is the 
---- development_event_history table for parcels
--drop table if exists development_event_history_parcels;
--create table development_event_history_parcels
--select * from deh_temp_sqft_units_impv_by_parcel_year;
--</deh_ctemp_sqft_units_impv_by_parcel_year_use>

---- \begin diagnostic code;
-- select 
-- 	sum(RESIDENTIAL_IMPROVEMENT_VALUE) r, 
-- 	sum(COMMERCIAL_IMPROVEMENT_VALUE) c, 
-- 	sum(INDUSTRIAL_IMPROVEMENT_VALUE) i, 
-- 	sum(GOVERNMENTAL_IMPROVEMENT_VALUE) g 
-- from deh_ctemp_sqft_units_impv_by_parcel_year_use;

---- \end diagnostic code;

-- step 3a. create gridcells table from deh_ctemp_sqft_units_impv_by_parcel_year_use
-- keep parcel_id for diagnose and fraction assignment purpose
--<deh_temp_gridcells_added_w_pid>
set @step = '3a';
set @work = 'deh_temp_gridcells_added_w_pid';
select @step as STEP, @work as NOW_WORKING;

drop table if exists deh_temp_gridcells_added_w_pid;
create table
	deh_temp_gridcells_added_w_pid
select
	f.GRID_ID,
	p.YEAR_BUILT,
	p.COMMERCIAL_SQFT * f.PARCEL_FRACTION as COMMERCIAL_SQFT_ADDED,
	p.COMMERCIAL_IMPROVEMENT_VALUE * f.PARCEL_FRACTION as COMMERCIAL_IMPROVEMENT_VALUE_ADDED,
	p.INDUSTRIAL_SQFT * f.PARCEL_FRACTION as INDUSTRIAL_SQFT_ADDED,
	p.INDUSTRIAL_IMPROVEMENT_VALUE * f.PARCEL_FRACTION as INDUSTRIAL_IMPROVEMENT_VALUE_ADDED,
	p.GOVERNMENTAL_SQFT * f.PARCEL_FRACTION as GOVERNMENTAL_SQFT_ADDED,
	p.GOVERNMENTAL_IMPROVEMENT_VALUE * f.PARCEL_FRACTION as GOVERNMENTAL_IMPROVEMENT_VALUE_ADDED,
	p.RESIDENTIAL_UNITS * f.PARCEL_FRACTION as RESIDENTIAL_UNITS_ADDED,
	p.RESIDENTIAL_IMPROVEMENT_VALUE * f.PARCEL_FRACTION as RESIDENTIAL_IMPROVEMENT_VALUE_ADDED,
	p.PARCEL_ID,
	p.COUNTY
from
	deh_ctemp_sqft_units_impv_by_parcel_year p
	  inner join
	parcel_fractions_in_gridcells f
	  on p.PARCEL_ID = f.PARCEL_ID
	  and p.COUNTY = f.COUNTY
;

create index 
	index_grid_id_year_built_index
on
	deh_temp_gridcells_added_w_pid
	(grid_id, year_built,parcel_id,county)
;
--</deh_temp_gridcells_added_w_pid>

----/* here begins fraction assigning processes
-- set @step = '3b';
-- set @work = 'deh_temp_gridcells_added_w_pid_nofrac';
-- select @step as STEP, @work as NOW_WORKING;

-------------------------------------------------------------------------------
--- apply perl script to assign residential,sqft and improvement value fraction
--- to grid cell, create table deh_temp_gridcells_added_w_pid_nofrac
-------------------------------------------------------------------------------
---- */end of fraction assigning processes

-- step 3c. group by grid_id,year_built
--<deh_temp_gridcells_added_by_grid_id_year>
set @step = '3c';
set @work = 'deh_temp_gridcells_added_by_grid_id_year';
select @step as STEP, @work as NOW_WORKING;

drop table if exists deh_temp_gridcells_added_by_grid_id_year;
create table deh_temp_gridcells_added_by_grid_id_year (
GRID_ID int,
YEAR_BUILT int,
COMMERCIAL_SQFT int,
COMMERCIAL_IMPROVEMENT_VALUE bigint,
INDUSTRIAL_SQFT int,
INDUSTRIAL_IMPROVEMENT_VALUE bigint,
GOVERNMENTAL_SQFT int,
GOVERNMENTAL_IMPROVEMENT_VALUE bigint,
RESIDENTIAL_UNITS int,
RESIDENTIAL_IMPROVEMENT_VALUE bigint,
STARTING_DEVELOPMENT_TYPE_ID int,
ENDING_DEVELOPMENT_TYPE_ID int,
FRACTION_RESIDENTIAL_LAND_VALUE float
);

insert into
	deh_temp_gridcells_added_by_grid_id_year
	(GRID_ID, YEAR_BUILT, COMMERCIAL_SQFT, COMMERCIAL_IMPROVEMENT_VALUE, 
	INDUSTRIAL_SQFT, INDUSTRIAL_IMPROVEMENT_VALUE, GOVERNMENTAL_SQFT, 
	GOVERNMENTAL_IMPROVEMENT_VALUE, RESIDENTIAL_UNITS, RESIDENTIAL_IMPROVEMENT_VALUE)
select
	GRID_ID,
	YEAR_BUILT,
	round(sum(COMMERCIAL_SQFT_ADDED),0) as COMMERCIAL_SQFT,
	round(sum(COMMERCIAL_IMPROVEMENT_VALUE_ADDED),0) as COMMERCIAL_IMPROVEMENT_VALUE,
	round(sum(INDUSTRIAL_SQFT_ADDED),0) as INDUSTRIAL_SQFT,
	round(sum(INDUSTRIAL_IMPROVEMENT_VALUE_ADDED),0) as INDUSTRIAL_IMPROVEMENT_VALUE,
	round(sum(GOVERNMENTAL_SQFT_ADDED),0) as GOVERNMENTAL_SQFT,
	round(sum(GOVERNMENTAL_IMPROVEMENT_VALUE_ADDED),0) as GOVERNMENTAL_IMPROVEMENT_VALUE,
	round(sum(RESIDENTIAL_UNITS_ADDED),0) as RESIDENTIAL_UNITS,
	round(sum(RESIDENTIAL_IMPROVEMENT_VALUE_ADDED),0) as RESIDENTIAL_IMPROVEMENT_VALUE
from
	deh_temp_gridcells_added_w_pid g
group by
	g.GRID_ID,
	g.YEAR_BUILT
;

-- trick for handling NULL year_built, set NULL = 0, and change it back later.
update deh_temp_gridcells_added_by_grid_id_year
set YEAR_BUILT = 0
where YEAR_BUILT is null
;

delete from deh_temp_gridcells_added_by_grid_id_year
where YEAR_BUILT > 2000
;


create index index_grid_id_year
on deh_temp_gridcells_added_by_grid_id_year (GRID_ID,YEAR_BUILT);
--</deh_temp_gridcells_added_by_grid_id_year>

----/* \begin diagnostic code;
-- select 
-- 	sum(RESIDENTIAL_UNITS) r,
-- 	sum(COMMERCIAL_SQFT) c, 
-- 	sum(INDUSTRIAL_SQFT) i, 
-- 	sum(GOVERNMENTAL_SQFT) g
-- from deh_temp_gridcells_added_by_grid_id_year;

-- select sum(residential_units) from deh_ctemp_sqft_units_impv_by_parcel_year_use;
-- select sum(built_sqft) from deh_ctemp_sqft_units_impv_by_parcel_year_use;

-- select
-- 	sum(RESIDENTIAL_IMPROVEMENT_VALUE) r_impv,
-- 	sum(COMMERCIAL_IMPROVEMENT_VALUE) c_impv,
--  	sum(INDUSTRIAL_IMPROVEMENT_VALUE) i_impv,
-- 	sum(GOVERNMENTAL_IMPROVEMENT_VALUE) g_impv
-- from deh_temp_gridcells_added_by_grid_id_year; 
----*/ \end diagnostic code;


-- step 3d.1 add up yearly added built_sqft and residential_units to get 
-- total built_sqft and residential_units added
--<deh_temp_gridcells_total_added_by_grid_id_year>
set @step = '3d.2';
set @work = 'deh_temp_gridcells_total_added_by_grid_id_year';
select @step as STEP, @work as NOW_WORKING;

drop table if exists deh_temp_gridcells_total_added_by_grid_id_year;
create table deh_temp_gridcells_total_added_by_grid_id_year (
GRID_ID int,
YEAR_BUILT int,
COMMERCIAL_SQFT int,
INDUSTRIAL_SQFT int,
GOVERNMENTAL_SQFT int,
RESIDENTIAL_UNITS int
--,TOTAL_NONRES_SQFT int
);

insert into deh_temp_gridcells_total_added_by_grid_id_year
select
	g1.GRID_ID,
	g1.YEAR_BUILT,
	sum(g2.COMMERCIAL_SQFT) as COMMERCIAL_SQFT,
	sum(g2.INDUSTRIAL_SQFT) as INDUSTRIAL_SQFT,
	sum(g2.GOVERNMENTAL_SQFT) as GOVERNMENTAL_SQFT,
	sum(g2.RESIDENTIAL_UNITS) as RESIDENTIAL_UNITS
from
	deh_temp_gridcells_added_by_grid_id_year g1
	  inner join
	deh_temp_gridcells_added_by_grid_id_year g2
	  on g1.GRID_ID = g2.GRID_ID
	  and g1.YEAR_BUILT <= g2.YEAR_BUILT
group by
	g1.GRID_ID,
	g1.YEAR_BUILT
;


update deh_temp_gridcells_total_added_by_grid_id_year
set RESIDENTIAL_UNITS = 0
where RESIDENTIAL_UNITS is null;

update deh_temp_gridcells_total_added_by_grid_id_year
set  COMMERCIAL_SQFT = 0
where COMMERCIAL_SQFT is null;

update deh_temp_gridcells_total_added_by_grid_id_year
set INDUSTRIAL_SQFT = 0
where INDUSTRIAL_SQFT is null;

update deh_temp_gridcells_total_added_by_grid_id_year
set GOVERNMENTAL_SQFT = 0
where GOVERNMENTAL_SQFT is null;

create index deh_temp_gridcells_total_added_by_grid_id_year_grid_id_index
on deh_temp_gridcells_total_added_by_grid_id_year (GRID_ID,YEAR_BUILT);

--UPDATE deh_temp_gridcells_total_added_by_grid_id_year 
--	SET TOTAL_NONRES_SQFT = ifnull(COMMERCIAL_SQFT,0) + ifnull(INDUSTRIAL_SQFT,0) + ifnull(GOVERNMENTAL_SQFT,0);

--CREATE index gridcells_sum_TNS_RU_index
--on deh_temp_gridcells_total_added_by_grid_id_year (TOTAL_NONRES_SQFT, RESIDENTIAL_UNITS);
--</deh_temp_gridcells_total_added_by_grid_id_year >


-- step 3d.2 roll back from baseyear gridcells table to create historical gridcells table
-- <deh_temp_gridcells_by_grid_id_year>
set @step = '3d.2';
set @work = 'creating historical gridcells table deh_temp_gridcells_by_grid_id_year';
select @step as STEP, @work as NOW_WORKING;

drop table if exists deh_temp_gridcells_by_grid_id_year;
create table deh_temp_gridcells_by_grid_id_year (
GRID_ID int,
YEAR_BUILT int,
COMMERCIAL_SQFT int,
INDUSTRIAL_SQFT int,
GOVERNMENTAL_SQFT int,
RESIDENTIAL_UNITS int,
TOTAL_NONRES_SQFT int,
DEVELOPMENT_TYPE_ID int
);

insert into deh_temp_gridcells_by_grid_id_year
	(GRID_ID, YEAR_BUILT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT, GOVERNMENTAL_SQFT, RESIDENTIAL_UNITS)
select
	g2.GRID_ID,
	g2.YEAR_BUILT,
	(g1.COMMERCIAL_SQFT - g2.COMMERCIAL_SQFT) as COMMERCIAL_SQFT,
	(g1.INDUSTRIAL_SQFT - g2.INDUSTRIAL_SQFT) as INDUSTRIAL_SQFT,
	(g1.GOVERNMENTAL_SQFT - g2.GOVERNMENTAL_SQFT) as GOVERNMENTAL_SQFT,
	(g1.RESIDENTIAL_UNITS - g2.RESIDENTIAL_UNITS) as RESIDENTIAL_UNITS
from
	PSRC_2000_baseyear_reestimation.gridcells g1
	  inner join
	deh_temp_gridcells_total_added_by_grid_id_year g2
	  on g1.GRID_ID = g2.GRID_ID
;


-- # insert baseyear gridcells as 'historical' gridcells table of year 2001
insert into deh_temp_gridcells_by_grid_id_year
	(GRID_ID, YEAR_BUILT, COMMERCIAL_SQFT, INDUSTRIAL_SQFT, GOVERNMENTAL_SQFT,
	RESIDENTIAL_UNITS, DEVELOPMENT_TYPE_ID)
select
	distinct g1.GRID_ID,
	2001 as YEAR_BUILT,
	g1.COMMERCIAL_SQFT,
	g1.INDUSTRIAL_SQFT,
	g1.GOVERNMENTAL_SQFT,
	g1.RESIDENTIAL_UNITS,
	g1.DEVELOPMENT_TYPE_ID
from 
	PSRC_2000_baseyear_reestimation.gridcells g1
-- 	  inner join
-- 	deh_temp_gridcells_total_added_by_grid_id_year g2
-- 	  on g1.GRID_ID = g2.GRID_ID
;

-- # keep a copy of deh_temp_gridcells_by_grid_id_year for diagnose # --
drop table if exists deh_temp_gridcells_by_grid_id_year_bak;
create table deh_temp_gridcells_by_grid_id_year_bak
select * from deh_temp_gridcells_by_grid_id_year;

update deh_temp_gridcells_by_grid_id_year
set RESIDENTIAL_UNITS = 0
where RESIDENTIAL_UNITS is null or
  RESIDENTIAL_UNITS < 0;

update deh_temp_gridcells_by_grid_id_year
set  COMMERCIAL_SQFT = 0
where COMMERCIAL_SQFT is null or
  COMMERCIAL_SQFT < 0;

update deh_temp_gridcells_by_grid_id_year
set INDUSTRIAL_SQFT = 0
where INDUSTRIAL_SQFT is null or
  INDUSTRIAL_SQFT < 0;

update deh_temp_gridcells_by_grid_id_year
set GOVERNMENTAL_SQFT = 0
where GOVERNMENTAL_SQFT is null or
  GOVERNMENTAL_SQFT < 0;

create index deh_temp_gridcells_by_grid_id_year_grid_id_index
on deh_temp_gridcells_by_grid_id_year (GRID_ID,YEAR_BUILT);

UPDATE deh_temp_gridcells_by_grid_id_year 
	SET TOTAL_NONRES_SQFT = ifnull(COMMERCIAL_SQFT,0) + ifnull(INDUSTRIAL_SQFT,0) + ifnull(GOVERNMENTAL_SQFT,0);

CREATE index gridcells_sum_TNS_RU_index
on deh_temp_gridcells_by_grid_id_year (TOTAL_NONRES_SQFT, RESIDENTIAL_UNITS);
--</deh_temp_gridcells_by_grid_id_year >


-- (optional fields) step 4a. create fraction_residential_land for gridcells
-- update
-- 	deh_temp_gridcells_added_by_grid_id_year a,
-- 	PSRC_2000_estimation_petecaba.gridcells g
-- set 
-- 	a.FRACTION_RESIDENTIAL_LAND_VALUE = g.FRACTION_RESIDENTIAL_LAND
-- ;

-- step 3d.3 Assign dev type to gridcells
--<deh_temp_gridcells_sum_by_grid_id_year>
set @step = '3d.3';
set @work = 'assigning dev type for deh_temp_gridcells_sum_by_grid_id_year';
select @step as STEP, @work as NOW_WORKING;

\. /projects/urbansim7/scripts/private/lmwang/SQL/gridcells_dev_event_history_devtype.sql

-- # if baseyear dev type of gridcell >= 24, set to baseyear dev type
update deh_temp_gridcells_by_grid_id_year deh, PSRC_2000_baseyear_reestimation.gridcells g
set deh.development_type_id = g.development_type_id
where deh.grid_id = g.grid_id
and g.development_type_id >= 24;

--<deh_temp_gridcells_by_grid_id_year>

-- step 3e. determine previous events year for each gridcell, thus determin its starting_development_type_id
--<deh_temp_gridcells_previous_year>
set @step = '3e';
set @work = 'deh_temp_gridcells_previous_year';
select @step as STEP, @work as NOW_WORKING;

drop table if exists deh_temp_gridcells_previous_year;
create table deh_temp_gridcells_previous_year
select
	s1.GRID_ID,
	s1.YEAR_BUILT,
	max(s2.YEAR_BUILT) as PREVIOUS_YEAR
from 
	deh_temp_gridcells_by_grid_id_year s1
	  inner join deh_temp_gridcells_by_grid_id_year s2
	  on s1.GRID_ID = s2.GRID_ID
	  and s1.YEAR_BUILT > s2.YEAR_BUILT
group by
	s1.GRID_ID,
	s1.YEAR_BUILT
;

create index deh_temp_gridcells_previous_year_index 
	on deh_temp_gridcells_previous_year 
	(GRID_ID, YEAR_BUILT, PREVIOUS_YEAR);
--</deh_temp_gridcells_previous_year>

-- step 3f. assign dev type for deh_temp_gridcells_added_by_grid_id_year
--<deh_temp_gridcells_added_by_grid_id_year>
set @step = '3f';
set @work = 'assigning dev type for deh_temp_gridcells_added_by_grid_id_year';
select @step as STEP, @work as NOW_WORKING;


update 
	deh_temp_gridcells_added_by_grid_id_year a,
	deh_temp_gridcells_by_grid_id_year s
set
	a.STARTING_DEVELOPMENT_TYPE_ID = s.DEVELOPMENT_TYPE_ID
where
	a.GRID_ID = s.GRID_ID
	and a.YEAR_BUILT = s.YEAR_BUILT
;

update 
	deh_temp_gridcells_added_by_grid_id_year deh,
	deh_temp_gridcells_by_grid_id_year dt,
	deh_temp_gridcells_previous_year pre
set deh.ENDING_DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID
where deh.grid_id = pre.grid_id and deh.year_built = pre.previous_year 
  and dt.grid_id = pre.grid_id and dt.year_built = pre.year_built
;

update deh_temp_gridcells_added_by_grid_id_year
set STARTING_DEVELOPMENT_TYPE_ID = 24
where STARTING_DEVELOPMENT_TYPE_ID is null
;

update deh_temp_gridcells_added_by_grid_id_year
set ENDING_DEVELOPMENT_TYPE_ID = 24
where ENDING_DEVELOPMENT_TYPE_ID is null
;

--</deh_temp_gridcells_added_by_grid_id_year>


-- step 4a. create development event history table
--<development_event_history>
set @step = '4a';
set @work = 'development_event_history';
select @step as STEP, @work as NOW_WORKING;

drop table if exists development_event_history;
create table development_event_history(
GRID_ID int(11),
SCHEDULED_YEAR int(11),
STARTING_DEVELOPMENT_TYPE_ID int(11),
ENDING_DEVELOPMENT_TYPE_ID int(11),
DEVELOPMENT_TYPE_CHANGE_TYPE char(1),
RESIDENTIAL_UNITS_CHANGE_TYPE char(1),
RESIDENTIAL_UNITS int(11),
COMMERCIAL_SQFT_CHANGE_TYPE char(1),
COMMERCIAL_SQFT int(11),
INDUSTRIAL_SQFT_CHANGE_TYPE char(1),
INDUSTRIAL_SQFT int(11),
GOVERNMENTAL_SQFT_CHANGE_TYPE char(1),
GOVERNMENTAL_SQFT int(11),
RESIDENTIAL_IMPROVEMENT_VALUE_CHANGE_TYPE char(1),
RESIDENTIAL_IMPROVEMENT_VALUE int(11),
COMMERCIAL_IMPROVEMENT_VALUE_CHANGE_TYPE char(1),
COMMERCIAL_IMPROVEMENT_VALUE int(11),
INDUSTRIAL_IMPROVEMENT_VALUE_CHANGE_TYPE char(1),
INDUSTRIAL_IMPROVEMENT_VALUE int(11),
GOVERNMENTAL_IMPROVEMENT_VALUE_CHANGE_TYPE char(1),
GOVERNMENTAL_IMPROVEMENT_VALUE int(11),
FRACTION_RESIDENTIAL_LAND_VALUE_CHANGE_TYPE char(1),
FRACTION_RESIDENTIAL_LAND_VALUE double)
;

insert into 
	development_event_history
select
	GRID_ID,
	YEAR_BUILT as SCHEDULED_YEAR,
	STARTING_DEVELOPMENT_TYPE_ID,
	ENDING_DEVELOPMENT_TYPE_ID,
	'R' as DEVELOPMENT_TYPE_CHANGE_TYPE,
	'A' as RESIDENTIAL_UNITS_CHANGE_TYPE,
	RESIDENTIAL_UNITS,
	'A' as COMMERCIAL_SQFT_CHANGE_TYPE,
	COMMERCIAL_SQFT,
	'A' as INDUSTRIAL_SQFT_CHANGE_TYPE,
	INDUSTRIAL_SQFT,
	'A' as GOVERNMENTAL_SQFT_CHANGE_TYPE,
	GOVERNMENTAL_SQFT,
	'A' as RESIDENTIAL_IMPROVEMENT_VALUE_CHANGE_TYPE,
	RESIDENTIAL_IMPROVEMENT_VALUE,
	'A' as COMMERCIAL_IMPROVEMENT_VALUE_CHANGE_TYPE,
	COMMERCIAL_IMPROVEMENT_VALUE,
	'A' as INDUSTRIAL_IMPROVEMENT_VALUE_CHANGE_TYPE,
	INDUSTRIAL_IMPROVEMENT_VALUE,
	'A' as GOVERNMENTAL_IMPROVEMENT_VALUE_CHANGE_TYPE,
	GOVERNMENTAL_IMPROVEMENT_VALUE,
	'N' as FRACTION_RESIDENTIAL_LAND_VALUE_CHANGE_TYPE,
	0 as FRACTION_RESIDENTIAL_LAND_VALUE
from 
	deh_temp_gridcells_added_by_grid_id_year
;

---- clear up development_event_history table

update development_event_history
set scheduled_year = NULL 
where scheduled_year = 0;

update development_event_history
set starting_development_type_id = ending_development_type_id
where ending_development_type_id > 24;

delete from 
	development_event_history
where 
	grid_id = -9999
	or grid_id = 0
;

delete from
	development_event_history
where
	residential_units = 0 
    and commercial_sqft = 0
    and industrial_sqft = 0
    and governmental_sqft = 0
;

delete from development_event_history
where ending_development_type_id >= 24
;

delete from development_event_history
where scheduled_year > 2000;

-- select count(*) from development_event_history deh,  PSRC_2000_estimation_petecaba.gridcells g
-- where deh.grid_id = g.grid_id and g.development_type_id = 24;

-- select count(*) from deh_temp_gridcells_added_by_grid_id_year deh, PSRC_2000_estimation_petecaba.gridcells g
-- where deh.grid_id = g.grid_id and g.development_type_id >= 24;


delete deh from development_event_history deh, PSRC_2000_baseyear_reestimation.gridcells g
where deh.grid_id = g.grid_id 
	and g.development_type_id >= 24;

-- step 5b update IMPROVEMENT_VALUE to fit the documented usage

update development_event_history
set COMMERCIAL_IMPROVEMENT_VALUE = round(COMMERCIAL_IMPROVEMENT_VALUE / COMMERCIAL_SQFT),
INDUSTRIAL_IMPROVEMENT_VALUE = round(INDUSTRIAL_IMPROVEMENT_VALUE / INDUSTRIAL_SQFT),
GOVERNMENTAL_IMPROVEMENT_VALUE = round(GOVERNMENTAL_IMPROVEMENT_VALUE / GOVERNMENTAL_SQFT),
RESIDENTIAL_IMPROVEMENT_VALUE = round(RESIDENTIAL_IMPROVEMENT_VALUE / RESIDENTIAL_UNITS)
;

-- update development_event_history to set NULL improvement_values to zero
update development_event_history
set COMMERCIAL_IMPROVEMENT_VALUE = 0
where COMMERCIAL_IMPROVEMENT_VALUE is NULL;

update development_event_history
set INDUSTRIAL_IMPROVEMENT_VALUE = 0
where INDUSTRIAL_IMPROVEMENT_VALUE is NULL;

update development_event_history
set GOVERNMENTAL_IMPROVEMENT_VALUE = 0
where GOVERNMENTAL_IMPROVEMENT_VALUE is NULL;

update development_event_history
set RESIDENTIAL_IMPROVEMENT_VALUE = 0
where RESIDENTIAL_IMPROVEMENT_VALUE is NULL;


--</development_event_history>

drop table if exists development_event_history_full;
rename table development_event_history to development_event_history_full;

-- # apply development_event_history fix (year_built and development constraints) # --
create table development_event_history
select * from development_event_history_full 
where scheduled_year between 1996 and 2000;

\. /projects/urbansim7/scripts/private/lmwang/SQL/gridcells_dev_event_history_fix.sql

-- step 6a create transition_types
--<transition_types>
set @step = '6a';
set @work = 'transition_types';
select @step as STEP, @work as NOW_WORKING;

\! perl /projects/urbansim7/scripts/private/lmwang/Perl/transition_types.pl -H trondheim -D PSRC_parcels_all_counties -U urbansim -P UrbAnsIm4Us

--</transition_types>

-- step 5c drop temporary tables

drop table btemp_table_r;
drop table btemp_table_c;
drop table btemp_table_i;
drop table btemp_table_g;

-- drop table deh_ptemp_units_impv_by_parcel;
-- drop table deh_btemp_sqft_by_parcel_year_use;
-- drop table deh_ctemp_sqft_units_impv_by_parcel_year_use;
-- drop table deh_temp_sqft_units_impv_by_parcel_year;
-- drop table deh_temp_gridcells_added_w_pid;
-- drop table deh_temp_gridcells_added_by_grid_id_year;
-- drop table deh_temp_gridcells_sum_by_grid_id_year;
-- drop table deh_temp_gridcells_by_grid_id_year;
-- #drop table deh_temp_gridcells_added_w_pid_nofrac;
-- drop table deh_temp_gridcells_previous_year;
-- drop table deh_ptemp_avg_impv_by_county;
