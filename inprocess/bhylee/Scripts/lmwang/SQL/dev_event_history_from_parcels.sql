-- please refer to gridcells_dev_event_history for current script for 
-- generating development_event_history table

--create development_event_history table for baseyear database
--input database:
--PSRC_parcels_king, PSRC_parcels_kitsap, PSRC_parcels_pierce,PSRC_parcels_snohomish
--input tables;
--parcels, parcel_fractions_in_gridcells, development_types

--Step 1.
--create parcels_fractions_in_gridcells for all four counties
create table parcel_fractions_in_gridcells
select * from PSRC_parcels_king.parcel_fractions_in_gridcells;

insert into parcel_fractions_in_gridcells
select PARCEL_ID,GRID_ID,PARCEL_FRACTION,COUNTY from PSRC_parcels_kitsap.parcel_fractions_in_gridcells;

insert into parcel_fractions_in_gridcells
select PARCEL_ID,GRID_ID,PARCEL_FRACTION,COUNTY from PSRC_parcels_pierce.parcel_fractions_in_gridcells;

insert into parcel_fractions_in_gridcells
select PARCEL_ID,GRID_ID,PARCEL_FRACTION,COUNTY from PSRC_parcels_snohomish.parcel_fractions_in_gridcells;

create index parcel_fractions_in_gridcells_parcel_id_grid_id_county_index
	on parcel_fractions_in_gridcells (parcel_id,grid_id,county);

-- mysql> describe parcels;
-- +---------------------------+-------------+------+-----+---------+-------+
-- | Field                     | Type        | Null | Key | Default | Extra |
-- +---------------------------+-------------+------+-----+---------+-------+
-- | PARCEL_ID                 | mediumtext  | YES  |     | NULL    |       |
-- | LAND_USE                  | int(11)     | YES  | MUL | NULL    |       |
-- | BUILT_SQFT                | int(11)     | YES  |     | NULL    |       |
-- | IMPROVEMENT_VALUE         | int(11)     | YES  | MUL | NULL    |       |
-- | LAND_VALUE                | int(11)     | YES  |     | NULL    |       |
-- | LOT_SQFT                  | int(11)     | YES  |     | NULL    |       |
-- | ACRES                     | double(8,3) | YES  |     | NULL    |       |
-- | RESIDENTIAL_UNITS         | int(11)     | YES  |     | NULL    |       |
-- | RESIDENTIAL_UNITS_IMPUTED | double      | YES  |     | NULL    |       |
-- | YEAR_BUILT                | int(11)     | YES  | MUL | NULL    |       |
-- | COUNTY                    | mediumtext  | YES  | MUL | NULL    |       |
-- | CITY                      | mediumtext  | YES  | MUL | NULL    |       |
-- | LAND_USE_IMPUTED_FLAG     | int(11)     | YES  |     | NULL    |       |
-- | CENSUS_BLOCK              | varchar(18) | YES  |     | NULL    |       |
-- | TAXEXEMPT_BINARY          | tinyint(4)  | YES  |     | NULL    |       |
-- +---------------------------+-------------+------+-----+---------+-------+


-- Step 2a. create parcels table with all necessary fields

create temporary table
	temp_units_impv_by_parcel
select 
	p.PARCEL_ID,
	p.COUNTY,
	p.YEAR_BUILT,
	l.GENERIC_LAND_USE_2,
	p.IMPROVEMENT_VALUE,
	p.RESIDENTIAL_UNITS
from
	parcels p 
	  inner join 
	land_use_generic_reclass l
	  on p.county = l.county 
	  and p.land_use = l.county_land_use_code
;

alter table temp_units_impv_by_parcel
add RESIDENTIAL_IMPROVEMENT_VALUE int,
add COMMERCIAL_IMPROVEMENT_VALUE int,
add INDUSTRIAL_IMPROVEMENT_VALUE int,
add GOVERNMENTAL_IMPROVEMENT_VALUE int
;

update
 	temp_units_impv_by_parcel
set RESIDENTIAL_IMPROVEMENT_VALUE = IMPROVEMENT_VALUE
where
 	GENERIC_LAND_USE_2 = "R"
;

update
	temp_units_impv_by_parcel
set COMMERCIAL_IMPROVEMENT_VALUE = IMPROVEMENT_VALUE
where
	GENERIC_LAND_USE_2 = "C"
;

update
	temp_units_impv_by_parcel
set INDUSTRIAL_IMPROVEMENT_VALUE = IMPROVEMENT_VALUE
where
	GENERIC_LAND_USE_2 = "I"
;

update
	temp_units_impv_by_parcel
set GOVERNMENTAL_IMPROVEMENT_VALUE = IMPROVEMENT_VALUE
where
	GENERIC_LAND_USE_2 = "G"
;

create index 
	temp_units_impv_by_parcel_parcel_id_county_index
on
	temp_units_impv_by_parcel
	(PARCEL_ID(16), COUNTY(4),YEAR_BUILT)
;

-- step 2b. extract built sqft from buildings table;

-- +-----------------------+-------------+------+-----+---------+-------+
-- | Field                 | Type        | Null | Key | Default | Extra |
-- +-----------------------+-------------+------+-----+---------+-------+
-- | BUILDING_USE          | varchar(50) | YES  | MUL | NULL    |       |
-- | DESCRIPTION           | text        | YES  |     | NULL    |       |
-- | MAJOR                 | text        | YES  |     | NULL    |       |
-- | MINOR                 | text        | YES  |     | NULL    |       |
-- | PARCEL_ID             | varchar(12) | YES  | MUL | NULL    |       |
-- | BUILT_SQFT            | double      | YES  |     | NULL    |       |
-- | NUMBER_OF_BUILDINGS   | double      | YES  |     | NULL    |       |
-- | YEAR_BUILT            | double      | YES  |     | NULL    |       |
-- | RESIDENTIAL_UNITS     | double      | YES  |     | NULL    |       |
-- | COUNTY                | char(3)     | YES  | MUL | NULL    |       |
-- | use_before_imputation | varchar(10) | YES  |     | NULL    |       |
-- +-----------------------+-------------+------+-----+---------+-------+

create temporary table
	temp_sqft_by_year
select
	p.PARCEL_ID,
	p.COUNTY,
	u.GENERIC_BUILDING_USE_2 as BUILDING_USE,
	sum(p.BUILT_SQFT) as BUILT_SQFT
from
	PSRC_parcels_king.buildings p
	  inner join
	PSRC_parcels_king.building_use_generic_reclass u
	  on p.COUNTY = u.COUNTY
	  and p.BUILDING_USE = u.COUNTY_BUILDING_USE_CODE
where
	u.GENERIC_BUILDING_USE_2 in ('C','G','I','R')
group by
	p.PARCEL_ID,
	u.GENERIC_BUILDING_USE_2
;

insert into
	temp_sqft_by_year
select
	p.PARCEL_ID,
	p.COUNTY,
	u.GENERIC_BUILDING_USE_2 as BUILDING_USE,
	sum(p.BUILT_SQFT) as BUILT_SQFT 
from
	PSRC_parcels_kitsap.buildings p
  	  inner join
	PSRC_parcels_kitsap.building_use_generic_reclass u
	  on p.COUNTY = u.COUNTY
	  and p.BUILDING_USE = u.COUNTY_BUILDING_USE_CODE
where
	u.GENERIC_BUILDING_USE_2 in ('C','G','I','R')
group by
	p.PARCEL_ID,
	p.YEAR_BUILT,
	u.GENERIC_BUILDING_USE_2
;

insert into 
	temp_sqft_units_impv_by_year
	(PARCEL_ID,COUNTY,YEAR_BUILT,BUILDING_USE,NUM_BUILDINGS,BUILT_SQFT)	
select
	p.PARCEL_ID,
	p.COUNTY,
	p.YEAR_BUILT,
	u.GENERIC_BUILDING_USE_2 as BUILDING_USE,
	count(*) as NUM_BUILDINGS,
	sum(p.BUILT_SQFT) as BUILT_SQFT 
from
	PSRC_parcels_pierce.buildings p
  	  inner join
	PSRC_parcels_pierce.building_use_generic_reclass u
	  on p.COUNTY = u.COUNTY
	  and p.BUILDING_USE = u.COUNTY_BUILDING_USE_CODE
where
	u.GENERIC_BUILDING_USE_2 in ('C','G','I','R')
group by
	p.PARCEL_ID,
	p.YEAR_BUILT,
	u.GENERIC_BUILDING_USE_2
;

insert into 
	temp_sqft_units_impv_by_year
	(PARCEL_ID,COUNTY,YEAR_BUILT,BUILDING_USE,NUM_BUILDINGS,BUILT_SQFT)
select
	p.PARCEL_ID,
	p.COUNTY,
	p.YEAR_BUILT,
	u.GENERIC_BUILDING_USE_2 as BUILDING_USE,
	count(*) as NUM_BUILDINGS,
	sum(p.BUILT_SQFT) as BUILT_SQFT 
from
	PSRC_parcels_snohomish.buildings p
	  inner join
	PSRC_parcels_snohomish.building_use_generic_reclass u
	  on p.COUNTY = u.COUNTY
	  and p.BUILDING_USE = u.COUNTY_BUILDING_USE_CODE
where
	u.GENERIC_BUILDING_USE_2 in ('C','G','I','R')
group by
	p.PARCEL_ID,
	p.YEAR_BUILT,
	u.GENERIC_BUILDING_USE_2
;

create index
	temp_sqft_units_impv_by_year_parcel_id_county_index
on
	temp_sqft_units_impv_by_year
	(PARCEL_ID, COUNTY, YEAR_BUILT)
;

-- step 2c. update residential units from parcels

alter table temp_sqft_units_impv_by_year
add TOTAL_RES_BUILDINGS_IN_PARCEL int,
add TOTAL_RES_SQFT_IN_PARCEL int,
add TOTAL_RES_IMPV_IN_PARCEL int,
add TOTAL_COM_BUILDINGS_IN_PARCEL int,
add TOTAL_COM_SQFT_IN_PARCEL int,
add TOTAL_COM_IMPV_IN_PARCEL int,
add TOTAL_IND_BUILDINGS_IN_PARCEL int,
add TOTAL_IND_SQFT_IN_PARCEL int,
add TOTAL_IND_IMPV_IN_PARCEL int,
add TOTAL_GOV_BUILDINGS_IN_PARCEL int,
add TOTAL_GOV_SQFT_IN_PARCEL int,
add TOTAL_GOV_IMPV_IN_PARCEL int,
add TOTAL_RES_UNITS_IN_PARCEL int,
add TOTAL_IMPV_IN_PARCEL int
;

create index non_temp_sqft_units_impv_by_year_index
on non_temp_sqft_units_impv_by_year (PARCEL_ID,COUNTY,YEAR_BUILT);

create temporary table temp_table_r
select
	PARCEL_ID,
	COUNTY,
	sum(NUM_BUILDINGS) as TOTAL_RES_BUILDINGS_IN_PARCEL,
	sum(BUILT_SQFT) as TOTAL_RES_SQFT_IN_PARCEL
from non_temp_sqft_units_impv_by_year
where BUILDING_USE = 'R'
group by 
	PARCEL_ID, 
	COUNTY
;

create temporary table temp_table_c
select
	PARCEL_ID,
	COUNTY,
	sum(NUM_BUILDINGS) as TOTAL_COM_BUILDINGS_IN_PARCEL,
	sum(BUILT_SQFT) as TOTAL_COM_SQFT_IN_PARCEL
from non_temp_sqft_units_impv_by_year
where BUILDING_USE = 'C'
group by 
	PARCEL_ID, 
	COUNTY
;

create temporary table temp_table_i
select
	PARCEL_ID,
	COUNTY,
	sum(NUM_BUILDINGS) as TOTAL_IND_BUILDINGS_IN_PARCEL,
	sum(BUILT_SQFT) as TOTAL_IND_SQFT_IN_PARCEL
from non_temp_sqft_units_impv_by_year
where BUILDING_USE = 'I'
group by 
	PARCEL_ID, 
	COUNTY
;

create temporary table temp_table_g
select
	PARCEL_ID,
	COUNTY,
	sum(NUM_BUILDINGS) as TOTAL_GOV_BUILDINGS_IN_PARCEL,
	sum(BUILT_SQFT) as TOTAL_GOV_SQFT_IN_PARCEL
from non_temp_sqft_units_impv_by_year
where BUILDING_USE = 'G'
group by
	PARCEL_ID, 
	COUNTY
;

create index temp_table_r_parcel_id_county_index
on temp_table_r (PARCEL_ID, COUNTY);

create index temp_table_c_parcel_id_county_index
on temp_table_c (PARCEL_ID, COUNTY);

create index temp_table_i_parcel_id_county_index
on temp_table_i (PARCEL_ID, COUNTY);

create index temp_table_g_parcel_id_county_index
on temp_table_g (PARCEL_ID, COUNTY);

update
	temp_sqft_units_impv_by_year t,
	parcels p
set
	t.TOTAL_RES_UNITS_IN_PARCEL = p.RESIDENTIAL_UNITS
where
	t.PARCEL_ID = p.PARCEL_ID
	and t.COUNTY = p.COUNTY
;

create index non_temp_sqft_units_impv_by_year_parcel_id_county_year_built_index
on non_temp_sqft_units_impv_by_year (PARCEL_ID,COUNTY,YEAR_BUILT);

create table 
	temp_sqft_units_impv_by_year_full
select
	t.PARCEL_ID,
	t.COUNTY,
	t.YEAR_BUILT,
	t.BUILDING_USE,
	t.NUM_BUILDINGS,
	t.BUILT_SQFT,
	t.RESIDENTIAL_UNITS,
	t.TOTAL_RES_UNITS_IN_PARCEL,
	r.TOTAL_RES_BUILDINGS_IN_PARCEL,
	r.TOTAL_RES_SQFT_IN_PARCEL,
	c.TOTAL_COM_BUILDINGS_IN_PARCEL,
	c.TOTAL_COM_SQFT_IN_PARCEL,
	i.TOTAL_IND_BUILDINGS_IN_PARCEL,
	i.TOTAL_IND_SQFT_IN_PARCEL,
	g.TOTAL_GOV_BUILDINGS_IN_PARCEL,
	g.TOTAL_GOV_SQFT_IN_PARCEL,
	v.IMPROVEMENT_VALUE as TOTAL_IMPV_IN_PARCEL,
	v.RESIDENTIAL_IMPROVEMENT_VALUE as TOTAL_RES_IMPV_IN_PARCEL,
	v.COMMERCIAL_IMPROVEMENT_VALUE as TOTAL_COM_IMPV_IN_PARCEL,
	v.INDUSTRIAL_IMPROVEMENT_VALUE as TOTAL_IND_IMPV_IN_PARCEL,
	v.GOVERNMENTAL_IMPROVEMENT_VALUE as TOTAL_GOV_IMPV_IN_PARCEL 	
from non_temp_sqft_units_impv_by_year t
	left outer join temp_table_r r using (PARCEL_ID, COUNTY)
	left outer join temp_table_c c using (PARCEL_ID, COUNTY)
	left outer join temp_table_i i using (PARCEL_ID, COUNTY)
	left outer join temp_table_g g using (PARCEL_ID, COUNTY)
	left outer join temp_impv_by_parcel v using (PARCEL_ID, COUNTY)
;

create index temp_sqft_units_impv_by_year_full_index
on temp_sqft_units_impv_by_year_full (PARCEL_ID,COUNTY,YEAR_BUILT);

-- step 2d. Assign units in parcels to buildings
-- scheme 1. assign units evenly by num of buildings
update 
	temp_sqft_units_impv_by_year_full
set
	residential_units = TOTAL_RES_UNITS_IN_PARCEL * NUM_BUILDINGS / TOTAL_RES_BUILDINGS_IN_PARCEL
where
	COUNTY in ('035','053','061')
	and TOTAL_RES_BUILDINGS_IN_PARCEL <> 0
	and TOTAL_RES_BUILDINGS_IN_PARCEL is not null
;

-- scheme 2. assign units evenly by built sqft
-- update 
-- 	temp_sqft_units_impv_by_year
-- set
-- 	RESIDENTIAL_UNITS = TOTAL_RES_UNITS_IN_PARCEL * BUILT_SQFT / TOTAL_RES_SQFT_IN_PARCEL
-- where
-- 	COUNTY in ('035','053','061')
-- 	and TOTAL_RES_SQFT_IN_PARCEL <> 0
-- 	and TOTAL_RES_SQFT_IN_PARCEL is not null
-- ;

-- diagnose needed here to compare rounded building residential units to parcels

-- step 2e. assign improvement value to buildings
--scheme 1. Assign improvement value evenly by built sqft
alter table temp_sqft_units_impv_by_year_full
add IMPROVEMENT_VALUE float,
add RESIDENTIAL_IMPROVEMENT_VALUE float,
add COMMERCIAL_IMPROVEMENT_VALUE float,
add INDUSTRIAL_IMPROVEMENT_VALUE float,
add GOVERNMENTAL_IMPROVEMENT_VALUE float
;

update
	temp_sqft_units_impv_by_year_full
set
	IMPROVEMENT_VALUE = TOTAL_IMPV_IN_PARCEL * BUILT_SQFT/(IFNULL(TOTAL_RES_SQFT_IN_PARCEL,0)+IFNULL(TOTAL_COM_SQFT_IN_PARCEL,0)+IFNULL(TOTAL_IND_SQFT_IN_PARCEL,0)+IFNULL(TOTAL_GOV_SQFT_IN_PARCEL,0))
where 
	(IFNULL(TOTAL_RES_SQFT_IN_PARCEL,0)+IFNULL(TOTAL_COM_SQFT_IN_PARCEL,0)+IFNULL(TOTAL_IND_SQFT_IN_PARCEL,0)+IFNULL(TOTAL_GOV_SQFT_IN_PARCEL,0)) <> 0
	AND TOTAL_IMPV_IN_PARCEL is not null
	AND BUILT_SQFT is not null
;

update
	temp_sqft_units_impv_by_year_full
set
	RESIDENTIAL_IMPROVEMENT_VALUE = IMPROVEMENT_VALUE
where
	BUILDING_USE = 'R'
;

update
	temp_sqft_units_impv_by_year_full
set
	COMMERCIAL_IMPROVEMENT_VALUE = IMPROVEMENT_VALUE
where
	BUILDING_USE = 'C'
;

update
	temp_sqft_units_impv_by_year_full
set
	INDUSTRIAL_IMPROVEMENT_VALUE = IMPROVEMENT_VALUE
where
	BUILDING_USE = 'I'
;

update
	temp_sqft_units_impv_by_year_full
set
	GOVERNMENTAL_IMPROVEMENT_VALUE = IMPROVEMENT_VALUE
where
	BUILDING_USE = 'G'
;

-- step 3a. create gridcells table from temp_parcels_table
create table
	temp_gridcells_events_by_year
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
	p.RESIDENTIAL_IMPROVEMENT_VALUE * f.PARCEL_FRACTION as RESIDENTIAL_IMPROVEMENT_VALUE_ADDED
from
	temp_sqft_units_impv_by_year p
	  inner join
	parcel_fractions_in_gridcells f
	  on p.PARCEL_ID = f.PARCEL_ID
	  and p.COUNTY = f.COUNTY
;

create index 
	temp_gridcells_events_by_year_grid_id_year_built_index
on
	temp_gridcells_events_by_year
	(grid_id, year_built)
;

-- step 3b. compound yearly added built_sqft and residential_units into 
-- built_sqft and residential_units of each year

create table
	temp_gridcells_add
select
	GRID_ID,
	YEAR_BUILT,
	round(sum(COMMERCIAL_SQFT_ADDED),0) as COMMERCIAL_SQFT,
	round(sum(COMMERCIAL_IMRPOVEMENT_VALUE_ADDED),0) as COMMERCIAL_IMRPOVEMENT_VALUE,
	round(sum(INDUSTRIAL_SQFT_ADDED),0) as INDUSTRIAL_SQFT,
	round(sum(INDUSTRIAL_IMRPOVEMENT_VALUE_ADDED),0) as INDUSTRIAL_IMRPOVEMENT_VALUE,
	round(sum(GOVERNMENTAL_SQFT_ADDED),0) as GOVERNMENTAL_SQFT,
	round(sum(GOVERNMENTAL_IMRPOVEMENT_VALUE_ADDED),0) as GOVERNMENTAL_IMRPOVEMENT_VALUE,
	round(sum(RESIDENTIAL_UNITS_ADDED),0) as RESIDENTIAL_UNITS,
	round(sum(g2.RESIDENTIAL_IMRPOVEMENT_VALUE_ADDED),0) as RESIDENTIAL_IMRPOVEMENT_VALUE
from
	temp_gridcells_events_by_year g
group by
	g.GRID_ID,
	g.YEAR_BUILT
;

create index temp_gridcells_sum_grid_id_year_built_index
on temp_gridcells_sum (GRID_ID,YEAR_BUILT);

create table
	temp_gridcells_sum
select
	g1.GRID_ID,
	g1.YEAR_BUILT,
	round(sum(g2.COMMERCIAL_SQFT_ADDED),0) as COMMERCIAL_SQFT,
	round(sum(g2.COMMERCIAL_IMRPOVEMENT_VALUE_ADDED),0) as COMMERCIAL_IMRPOVEMENT_VALUE,
	round(sum(g2.INDUSTRIAL_SQFT_ADDED),0) as INDUSTRIAL_SQFT,
	round(sum(g2.INDUSTRIAL_IMRPOVEMENT_VALUE_ADDED),0) as INDUSTRIAL_IMRPOVEMENT_VALUE,
	round(sum(g2.GOVERNMENTAL_SQFT_ADDED),0) as GOVERNMENTAL_SQFT,
	round(sum(g2.GOVERNMENTAL_IMRPOVEMENT_VALUE_ADDED),0) as GOVERNMENTAL_IMRPOVEMENT_VALUE,
	round(sum(g2.RESIDENTIAL_UNITS_ADDED),0) as RESIDENTIAL_UNITS,
	round(sum(g2.RESIDENTIAL_IMRPOVEMENT_VALUE_ADDED),0) as RESIDENTIAL_IMRPOVEMENT_VALUE
from
	temp_gridcells_events_by_year g1
	  inner join
	temp_gridcells_events_by_year g2
	  on g1.GRID_ID = g2.GRID_ID
	  and g1.YEAR_BUILT >= IFNULL(g2.YEAR_BUILT,0)
group by
	g1.GRID_ID,
	g1.YEAR_BUILT
;

create index temp_gridcells_sum_grid_id_index
on temp_gridcells_sum (GRID_ID,YEAR_BUILT);

-- (unnecessary) step 4a. create fraction_residential_land for gridcells
alter table temp_gridcells_add
add FRACTION_RESIDENTIAL_LAND_VALUE double;

update
	temp_gridcells_add a,
	PSRC_2000_baseyear.gridcells g
set 
	a.FRACTION_RESIDENTIAL_LAND_VALUE = g.FRACTION_RESIDENTIAL_LAND
;

-- (unnecessary) step 4b. Assign dev type to gridcells
alter table temp_gridcells_sum
add TOTAL_NON_RES_SQFT int,
add DEVELOPMENT_TYPE_ID int;

alter table temp_gridcells_add
add DEVELOPMENT_TYPE_ID int;

update temp_gridcells_sum
set TOTAL_NON_RES_SQFT = (COMMERCIAL_SQFT + INDUSTRIAL_SQFT + GOVERNMENTAL_SQFT);

UPDATE temp_gridcells_sum g, PSRC_2000_baseyear.development_types dt
SET 	g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND dt.NAME IN ('R1','R2','R3','R4','R5','R6','R7','R8','M1','M2','M3','M4','M5','M6','M7','M8')
;

UPDATE temp_gridcells_sum g, PSRC_2000_baseyear.development_types dt
SET 	g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND (g.COMMERCIAL_SQFT >= g.INDUSTRIAL_SQFT) 
	AND (g.COMMERCIAL_SQFT >= g.GOVERNMENTAL_SQFT)
	AND g.COMMERCIAL_SQFT > 0
	AND dt.NAME IN ('C1','C2','C3')
;

UPDATE temp_gridcells_sum g, PSRC_2000_baseyear.development_types dt
SET 	g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND (g.INDUSTRIAL_SQFT > g.COMMERCIAL_SQFT) 
	AND (g.INDUSTRIAL_SQFT > g.GOVERNMENTAL_SQFT)
	AND dt.NAME IN ('I1','I2','I3')
;

UPDATE temp_gridcells_sum g, PSRC_2000_baseyear.development_types dt
SET g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND (g.GOVERNMENTAL_SQFT > g.COMMERCIAL_SQFT) 
	AND (g.GOVERNMENTAL_SQFT >= g.INDUSTRIAL_SQFT)
	AND g.GOVERNMENTAL_SQFT > 0
	AND dt.NAME = 'GV'
;

UPDATE temp_gridcells_sum SET DEVELOPMENT_TYPE_ID = 24 where TOTAL_NONRES_SQFT = 0 and RESIDENTIAL_UNITS = 0;

-- there should not have any dev type 25 here
-- UPDATE gridcells set DEVELOPMENT_TYPE_ID = 25 
-- WHERE	
-- 	PERCENT_WATER >= 50
-- 	OR PERCENT_OPEN_SPACE >= 50
-- 	OR PERCENT_FLOODPLAIN >= 50
-- 	OR PERCENT_WETLAND >= 50
-- 	OR PERCENT_PUBLIC_SPACE >= 50
-- 	OR IS_INSIDE_MILITARY_BASE = 1
-- 	OR IS_INSIDE_NATIONAL_FOREST = 1
-- 	OR PERCENT_UNDEVELOPABLE >= 75
-- 	OR PERCENT_AGRICULTURAL_PROTECTED_LANDS >= 50
-- 
update 
	temp_gridcells_add a,
	temp_gridcells_sum s
set
	a.DEVELOPMENT_TYPE_ID = s.DEVELOPMENT_TYPE_ID
where
	a.GRID_ID = s.GRID_ID
	and a.YEAR_BUILT = s.YEAR_BUILT
;

-- step 5. create development event history table
-- mysql> describe development_event_history;
-- +----------------------------------------------+-----------+------+-----+---------+-------+
-- | Field                                        | Type      | Null | Key | Default | Extra |
-- +----------------------------------------------+-----------+------+-----+---------+-------+
-- | GRID_ID                                      | int(11)   | YES  |     | NULL    |       |
-- | SCHEDULED_YEAR                               | int(11)   | YES  |     | NULL    |       |
---------------------------------------------------------------------------------------------
-- | STARTING_NON_RESIDENTIAL_SQFT                | int(11)   | YES  |     | NULL    |       |
-- | STARTING_RESIDENTIAL_UNITS                   | int(11)   | YES  |     | NULL    |       |
-- | STARTING_RESIDENTIAL_IMPROVEMENT_VALUE       | int(11)   | YES  |     | NULL    |       |
-- | STARTING_NON_RESIDENTIAL_IMPROVEMENT_VALUE   | int(11)   | YES  |     | NULL    |       |

-- | ENDING_NON_RESIDENTIAL_SQFT                  | int(11)   | YES  |     | NULL    |       |
-- | ENDING_RESIDENTIAL_UNITS                     | int(11)   | YES  |     | NULL    |       |
-- | ENDING_RESIDENTIAL_IMPROVEMENT_VALUE         | int(11)   | YES  |     | NULL    |       |
-- | ENDING_NON_RESIDENTIAL_IMPROVEMENT_VALUE     | int(11)   | YES  |     | NULL    |       |

-- | DIFFERENCE_NON_RESIDENTIAL_SQFT              | int(11)   | YES  |     | NULL    |       |
-- | DIFFERENCE_RESIDENTIAL_UNITS                 | int(11)   | YES  |     | NULL    |       |
-- | DIFFERENCE_RESIDENTIAL_IMPROVEMENT_VALUE     | int(11)   | YES  |     | NULL    |       |
-- | DIFFERENCE_NON_RESIDENTIAL_IMPROVEMENT_VALUE | int(11)   | YES  |     | NULL    |       |
---------------------------------------------------------------------------------------------

-- | STARTING_DEVELOPMENT_TYPE_ID                 | int(11)   | YES  |     | NULL    |       |
-- | ENDING_DEVELOPMENT_TYPE_ID                   | int(11)   | YES  |     | NULL    |       |
-- | DEVELOPMENT_TYPE_CHANGE_TYPE                 | char(255) | YES  |     | NULL    |       |

-- | RESIDENTIAL_UNITS_CHANGE_TYPE                | char(255) | YES  |     | NULL    |       |
-- | RESIDENTIAL_UNITS                            | int(11)   | YES  |     | NULL    |       |
-- | COMMERCIAL_SQFT_CHANGE_TYPE                  | char(255) | YES  |     | NULL    |       |
-- | COMMERCIAL_SQFT                              | int(11)   | YES  |     | NULL    |       |
-- | INDUSTRIAL_SQFT_CHANGE_TYPE                  | char(255) | YES  |     | NULL    |       |
-- | INDUSTRIAL_SQFT                              | int(11)   | YES  |     | NULL    |       |
-- | GOVERNMENTAL_SQFT_CHANGE_TYPE                | char(255) | YES  |     | NULL    |       |
-- | GOVERNMENTAL_SQFT                            | int(11)   | YES  |     | NULL    |       |

-- | RESIDENTIAL_IMPROVEMENT_VALUE_CHANGE_TYPE    | char(255) | YES  |     | NULL    |       |
-- | RESIDENTIAL_IMPROVEMENT_VALUE                | int(11)   | YES  |     | NULL    |       |
-- | COMMERCIAL_IMPROVEMENT_VALUE_CHANGE_TYPE     | char(255) | YES  |     | NULL    |       |
-- | COMMERCIAL_IMPROVEMENT_VALUE                 | int(11)   | YES  |     | NULL    |       |
-- | INDUSTRIAL_IMPROVEMENT_VALUE_CHANGE_TYPE     | char(255) | YES  |     | NULL    |       |
-- | INDUSTRIAL_IMPROVEMENT_VALUE                 | int(11)   | YES  |     | NULL    |       |
-- | GOVERNMENTAL_IMPROVEMENT_VALUE_CHANGE_TYPE   | char(255) | YES  |     | NULL    |       |
-- | GOVERNMENTAL_IMPROVEMENT_VALUE               | int(11)   | YES  |     | NULL    |       |

-- | FRACTION_RESIDENTIAL_LAND_VALUE_CHANGE_TYPE  | char(255) | YES  |     | NULL    |       |
-- | FRACTION_RESIDENTIAL_LAND_VALUE              | double    | YES  |     | NULL    |       |
-- +----------------------------------------------+-----------+------+-----+---------+-------+

create table development_event_history
GRID_ID int(11),
SCHEDULED_YEAR int(11),
STARTING_DEVELOPMENT_TYPE_ID int(11),
ENDING_DEVELOPMENT_TYPE_ID int(11),
DEVELOPMENT_TYPE_CHANGE_TYPE char(255),
RESIDENTIAL_UNITS_CHANGE_TYPE char(255),
RESIDENTIAL_UNITS int(11),
COMMERCIAL_SQFT_CHANGE_TYPE char(255),
COMMERCIAL_SQFT int(11),
INDUSTRIAL_SQFT_CHANGE_TYPE char(255),
INDUSTRIAL_SQFT int(11),
GOVERNMENTAL_SQFT_CHANGE_TYPE char(255),
GOVERNMENTAL_SQFT int(11),
RESIDENTIAL_IMPROVEMENT_VALUE_CHANGE_TYPE char(255),
RESIDENTIAL_IMPROVEMENT_VALUE int(11),
COMMERCIAL_IMPROVEMENT_VALUE_CHANGE_TYPE char(255),
COMMERCIAL_IMPROVEMENT_VALUE int(11),
INDUSTRIAL_IMPROVEMENT_VALUE_CHANGE_TYPE char(255),
INDUSTRIAL_IMPROVEMENT_VALUE int(11),
GOVERNMENTAL_IMPROVEMENT_VALUE_CHANGE_TYPE char(255),
GOVERNMENTAL_IMPROVEMENT_VALUE int(11),
FRACTION_RESIDENTIAL_LAND_VALUE_CHANGE_TYPE char(255),
FRACTION_RESIDENTIAL_LAND_VALUE double
;


insert into 
	development_event_history
select
	GRID_ID,
	YEAR_BUILT as SCHEDULED_YEAR,
	0 as STARTING_DEVELOPMENT_TYPE_ID,
	DEVELOPMENT_TYPE_ID as ENDING_DEVELOPMENT_TYPE_ID,
	'N' as DEVELOPMENT_TYPE_CHANGE_TYPE,
	RESIDENTIAL_UNITS,
	'A' as RESIDENTIAL_UNITS_CHANGE_TYPE,
	COMMERCIAL_SQFT,
	'A' as COMMERCIAL_SQFT_CHANGE_TYPE,
	INDUSTRIAL_SQFT,
	'A' as INDUSTRIAL_SQFT_CHANGE_TYPE,
	GOVERNMENTAL_SQFT,
	'A' as GOVERNMENTAL_SQFT_CHANGE_TYPE,
	RESIDENTIAL_IMPROVEMENT_VALUE,
	'A' as RESIDENTIAL_IMPROVEMENT_VALUE_CHANGE_TYPE,
	COMMERCIAL_IMPROVEMENT_VALUE,
	'A' as COMMERCIAL_IMPROVEMENT_VALUE_CHANGE_TYPE,
	GOVERNMENTAL_IMPROVEMENTAL_VALUE,
	'A' as GOVERNMENTAL_IMPROVEMENTAL_VALUE_CHANGE_TYPE,
	0 as FRACTION_RESIDENTIAL_LAND_VALUE,
	'N' as FRACTION_RESIDENTIAL_LAND_VALUE_CHANGE_TYPE
from 
	temp_gridcells_add
;