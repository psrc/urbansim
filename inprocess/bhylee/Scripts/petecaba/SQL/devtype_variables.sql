USE PSRC_2000_baseyear;

# SUB TABLES FOR NEW DEVELOPMENT TYPES
create temporary table tmp_percent_lands
 (GRID_ID int, 
  PERCENT_AGR double,
  PERCENT_FOREST double,
  PERCENT_MINING double,
  PERCENT_ROW double
  );

alter table tmp_percent_lands add index grid_indx(grid_id);

insert into tmp_percent_lands (grid_id) select distinct GRID_ID 
from PSRC_2000_baseyear.gridcells;

# UPDATE PERCENT_AGRICULTURE
update tmp_percent_lands a inner join PSRC_parcels_king.percent_agriculture b
 on a.grid_id = b.grid_id set a.percent_agr = b.percent_agr;
 
update tmp_percent_lands a inner join PSRC_parcels_kitsap.percent_agriculture b
 on a.grid_id = b.grid_id set a.percent_agr = b.percent_agr;
 
update tmp_percent_lands a inner join PSRC_parcels_pierce.percent_agriculture b
 on a.grid_id = b.grid_id set a.percent_agr = b.percent_agr; 
 
update tmp_percent_lands a inner join PSRC_parcels_snohomish.percent_agriculture b
 on a.grid_id = b.grid_id set a.percent_agr = b.percent_agr; 
 
# UPDATE PERCENT_FOREST
update tmp_percent_lands a inner join PSRC_parcels_king.percent_forest b
 on a.grid_id = b.grid_id set a.percent_forest = b.percent_forest;
 
update tmp_percent_lands a inner join PSRC_parcels_kitsap.percent_forest b
 on a.grid_id = b.grid_id set a.percent_forest = b.percent_forest;
 
update tmp_percent_lands a inner join PSRC_parcels_pierce.percent_forest b
 on a.grid_id = b.grid_id set a.percent_forest = b.percent_forest; 
 
update tmp_percent_lands a inner join PSRC_parcels_snohomish.percent_forest b
 on a.grid_id = b.grid_id set a.percent_forest = b.percent_forest; 
 
# UPDATE PERCENT_MINING
update tmp_percent_lands a inner join PSRC_parcels_king.percent_mining b
 on a.grid_id = b.grid_id set a.percent_mining = b.percent_mining;
 
update tmp_percent_lands a inner join PSRC_parcels_kitsap.percent_mining b
 on a.grid_id = b.grid_id set a.percent_mining = b.percent_mining;
 
update tmp_percent_lands a inner join PSRC_parcels_pierce.percent_mining b
 on a.grid_id = b.grid_id set a.percent_mining = b.percent_mining; 
 
update tmp_percent_lands a inner join PSRC_parcels_snohomish.percent_mining b
 on a.grid_id = b.grid_id set a.percent_mining = b.percent_mining; 
 
# UPDATE PERCENT_ROW
update tmp_percent_lands a inner join PSRC_parcels_king.percent_row b
 on a.grid_id = b.grid_id set a.percent_row = b.percent_row;
 
update tmp_percent_lands a inner join PSRC_parcels_kitsap.percent_row b
 on a.grid_id = b.grid_id set a.percent_row = b.percent_row;
 
update tmp_percent_lands a inner join PSRC_parcels_pierce.percent_row b
 on a.grid_id = b.grid_id set a.percent_row = b.percent_row; 
 
update tmp_percent_lands a inner join PSRC_parcels_snohomish.percent_row b
 on a.grid_id = b.grid_id set a.percent_row = b.percent_row; 


# INSERT NEW VARIABLES INTO EXPERIMENTAL GRIDCELLS TABLE

create table gridcells_devtype 
 select a.*, b.PERCENT_AGR, b.PERCENT_FOREST, b.PERCENT_MINING, b.PERCENT_ROW 
 from PSRC_2000_baseyear.gridcells a LEFT JOIN tmp_percent_lands b
 ON a.GRID_ID = b.GRID_ID
; 

update gridcells_devtype set development_type_id = 0;

## NEW DEVELOPMENT TYPE ID ASSIGNMENT 

#ALTER TABLE gridcells ADD COLUMN TOTAL_NONRES_SQFT int;
CREATE INDEX TNS_RU_indx on gridcells_devtype (TOTAL_NONRES_SQFT, RESIDENTIAL_UNITS);

#UPDATE gridcells SET TOTAL_NONRES_SQFT = (COMMERCIAL_SQFT + INDUSTRIAL_SQFT + GOVERNMENTAL_SQFT);

UPDATE gridcells_devtype g, development_types dt
SET 	g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND dt.NAME IN ('R1','R2','R3','R4','R5','R6','R7','R8','M1','M2','M3','M4','M5','M6','M7','M8')
;

UPDATE gridcells_devtype g, development_types dt
SET 	g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND (g.COMMERCIAL_SQFT >= g.INDUSTRIAL_SQFT) 
	AND (g.COMMERCIAL_SQFT >= g.GOVERNMENTAL_SQFT)
	AND dt.NAME IN ('C1','C2','C3')
;

UPDATE gridcells_devtype g, development_types dt
SET 	g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND (g.INDUSTRIAL_SQFT > g.COMMERCIAL_SQFT) 
	AND (g.INDUSTRIAL_SQFT > g.GOVERNMENTAL_SQFT)
	AND dt.NAME IN ('I1','I2','I3')
;

UPDATE gridcells_devtype g, development_types dt
SET g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND (g.GOVERNMENTAL_SQFT > g.COMMERCIAL_SQFT) 
	AND (g.GOVERNMENTAL_SQFT >= g.INDUSTRIAL_SQFT)
	AND g.GOVERNMENTAL_SQFT > 0
	AND dt.NAME = 'GV'
;

UPDATE gridcells_devtype SET DEVELOPMENT_TYPE_ID = 24 where TOTAL_NONRES_SQFT = 0 and RESIDENTIAL_UNITS = 0;


# Reclassified Development Types

UPDATE gridcells_devtype SET DEVELOPMENT_TYPE_ID = 23
WHERE PERCENT_PUBLIC_SPACE >= 50;

UPDATE gridcells_devtype SET DEVELOPMENT_TYPE_ID = 26
WHERE IS_INSIDE_NATIONAL_FOREST = 1;

UPDATE gridcells_devtype SET DEVELOPMENT_TYPE_ID = 27
WHERE PERCENT_MINING >= 50;

UPDATE gridcells_devtype SET DEVELOPMENT_TYPE_ID = 28
WHERE PERCENT_ROW >= 50;

UPDATE gridcells_devtype SET DEVELOPMENT_TYPE_ID = 29
WHERE IS_INSIDE_MILITARY_BASE = 1;

UPDATE gridcells_devtype SET DEVELOPMENT_TYPE_ID = 30
WHERE PERCENT_OPEN_SPACE >= 50;

UPDATE gridcells_devtype SET DEVELOPMENT_TYPE_ID = 31
WHERE PERCENT_AGRICULTURAL_PROTECTED_LANDS >= 50;

UPDATE gridcells_devtype set DEVELOPMENT_TYPE_ID = 25 
WHERE (
 PERCENT_WATER >= 50
 OR PERCENT_FLOODPLAIN >= 50
 OR PERCENT_WETLAND >= 50
 OR PERCENT_UNDEVELOPABLE >= 75
 ) and (DEVELOPMENT_TYPE_ID NOT BETWEEN 1 and 23)
;

###################################################################
# CREATE TABLE JOBS PER DEVTYPE

CREATE TEMPORARY TABLE tmp_jobs_per_devtype
 SELECT b.DEVELOPMENT_TYPE_ID, count(*) as JOBS 
 FROM jobs a INNER JOIN gridcells b 
 ON a.grid_id = b.grid_id 
 GROUP BY b.DEVELOPMENT_TYPE_ID;
 
# CREATE TABLE WITH DEVELOPMENT EVENT USING NEW DEVTYPE VARIABLES  

create temporary table events_per_grid_id
 select GRID_ID, count(*) as EVENTS from development_event_history 
 where scheduled_year between 1995 and 2000
 group by GRID_ID;
 
alter table events_per_grid_id add index grid_indx(grid_id);

CREATE TEMPORARY TABLE EVENTS_PER_DEVTYPE
 SELECT b.DEVELOPMENT_TYPE_ID, sum(a.EVENTS) as EVENTS from 
 events_per_grid_id a inner join gridcells_devtype b
 on a.grid_id = b.grid_id 
 group by b.development_type_id
; 

# Create temporary table units and sqft group by devtype
  
create temporary table tmp_units_sqft
 select development_type_id, sum(residential_units) as units, sum(total_nonres_sqft) as nonres_sqft
 from gridcells_devtype group by development_type_id;
 
drop table tmp_jobs_per_devtype;
drop table events_per_grid_id;
drop table EVENTS_PER_DEVTYPE;
drop table tmp_units_sqft

#####################################################################
# Alternate table with adjusted DEVELOPMENT TYPE VARIABLES

create table gridcells_devtype_2 select * from gridcells_devtype;

update gridcells_devtype_2 set development_type_id = 0;
alter table gridcells_devtype_2 add index grid_indx(grid_id);

## NEW DEVELOPMENT TYPE ID ASSIGNMENT 

#ALTER TABLE gridcells ADD COLUMN TOTAL_NONRES_SQFT int;
CREATE INDEX TNS_RU_indx on gridcells_devtype_2 (TOTAL_NONRES_SQFT, RESIDENTIAL_UNITS);

#UPDATE gridcells SET TOTAL_NONRES_SQFT = (COMMERCIAL_SQFT + INDUSTRIAL_SQFT + GOVERNMENTAL_SQFT);

UPDATE gridcells_devtype_2 g, development_types dt
SET 	g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND dt.NAME IN ('R1','R2','R3','R4','R5','R6','R7','R8','M1','M2','M3','M4','M5','M6','M7','M8')
;

UPDATE gridcells_devtype_2 g, development_types dt
SET 	g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND (g.COMMERCIAL_SQFT >= g.INDUSTRIAL_SQFT) 
	AND (g.COMMERCIAL_SQFT >= g.GOVERNMENTAL_SQFT)
	AND dt.NAME IN ('C1','C2','C3')
;

UPDATE gridcells_devtype_2 g, development_types dt
SET 	g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND (g.INDUSTRIAL_SQFT > g.COMMERCIAL_SQFT) 
	AND (g.INDUSTRIAL_SQFT > g.GOVERNMENTAL_SQFT)
	AND dt.NAME IN ('I1','I2','I3')
;

UPDATE gridcells_devtype_2 g, development_types dt
SET g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND (g.GOVERNMENTAL_SQFT > g.COMMERCIAL_SQFT) 
	AND (g.GOVERNMENTAL_SQFT >= g.INDUSTRIAL_SQFT)
	AND g.GOVERNMENTAL_SQFT > 0
	AND dt.NAME = 'GV'
;

UPDATE gridcells_devtype_2 SET DEVELOPMENT_TYPE_ID = 24 where TOTAL_NONRES_SQFT = 0 and RESIDENTIAL_UNITS = 0;

# Reclassified Development Types

UPDATE gridcells_devtype_2 SET DEVELOPMENT_TYPE_ID = 23
WHERE PERCENT_PUBLIC_SPACE >= 50;

UPDATE gridcells_devtype_2 SET DEVELOPMENT_TYPE_ID = 26
WHERE IS_INSIDE_NATIONAL_FOREST = 1;

UPDATE gridcells_devtype_2 SET DEVELOPMENT_TYPE_ID = 27
WHERE PERCENT_MINING >= 50;

UPDATE gridcells_devtype_2 SET DEVELOPMENT_TYPE_ID = 29
WHERE IS_INSIDE_MILITARY_BASE = 1;

UPDATE gridcells_devtype_2 SET DEVELOPMENT_TYPE_ID = 31
WHERE PERCENT_AGR >= 50;

UPDATE gridcells_devtype_2 set DEVELOPMENT_TYPE_ID = 25 
WHERE (
 PERCENT_WATER >= 75
 OR PERCENT_UNDEVELOPABLE >= 75
 ) and (DEVELOPMENT_TYPE_ID NOT BETWEEN 1 and 23)
;

###################################################################
# CREATE TABLE JOBS PER DEVTYPE

CREATE TEMPORARY TABLE tmp_jobs_per_devtype_2
 SELECT b.DEVELOPMENT_TYPE_ID, count(*) as JOBS 
 FROM jobs a INNER JOIN gridcells_devtypes_2 b 
 ON a.grid_id = b.grid_id 
 GROUP BY b.DEVELOPMENT_TYPE_ID;
 
# CREATE TABLE WITH DEVELOPMENT EVENT USING NEW DEVTYPE VARIABLES  

create temporary table events_per_grid_id_2
 select GRID_ID, count(*) as EVENTS from development_event_history 
 where scheduled_year between 1995 and 2000
 group by GRID_ID;
 
alter table events_per_grid_id_2 add index grid_indx(grid_id);

CREATE TEMPORARY TABLE EVENTS_PER_DEVTYPE_2
 SELECT b.DEVELOPMENT_TYPE_ID, sum(a.EVENTS) as EVENTS from 
 events_per_grid_id_2 a inner join gridcells_devtype_2 b
 on a.grid_id = b.grid_id 
 group by b.development_type_id
; 

# Create temporary table units and sqft group by devtype
  
create temporary table tmp_units_sqft_2
 select development_type_id, sum(residential_units) as units, sum(total_nonres_sqft) as nonres_sqft
 from gridcells_devtype_2 group by development_type_id;
 
drop table tmp_jobs_per_devtype_2;
drop table events_per_grid_id_2;
drop table EVENTS_PER_DEVTYPE_2;
drop table tmp_units_sqft_2;


## alter development types table ##
Changes made June 23, 2003

# change development types table in baseyear, make backup of development_types table in peters_playhouse #
use PSRC_2000_baseyear;
update development_types set name = 'Undevelopable' where development_type_id = 29;
update development_types set name = 'Military' where development_type_id = 27;

# Change development_types.sql script to adjust 27 and 29 development types changes #

# Insert new Development Type Ids into sqft_for_non_home_based_jobs (i.e. 26, 27, 28, 29). Create backup table in peters_playhouse

insert into sqft_for_non_home_based_jobs (development_type_id, sqft) 
 values 
 	(26, 500),
 	(27, 500),
 	(28,1000),
 	(29,1000)
;	


insert into residential_units_for_home_based_jobs (development_type_id, ratio)
 values (26, 1),
 	(27, 1),
 	(28, 1),
 	(29, 1)
 ;	




