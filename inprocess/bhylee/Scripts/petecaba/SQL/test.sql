#
#UrbanSim software.
#Copyright (C) 1998-2003 University of Washington
#
#You can redistribute this program and/or modify it under the
#terms of the GNU General Public License as published by the
#Free Software Foundation (http://www.gnu.org/copyleft/gpl.html).
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
#file LICENSE.htm for copyright and licensing information, and the
#file ACKNOWLEDGMENTS.htm for funding and other acknowledgments.
#
#Author: Liming Wang, modified by Chris Peak and Peter Caballero

###This script generate gridcell fields from parcels, parcel_fractions_in_gridcells, 
##and PSRC_2000_data_quality_indicators.land_use_generic_reclass table. Refer to wiki page:
##http://www.urbansim.org/projects/dataprep/tables/input_tables_parcel_to_grid.shtml
##Input: parcels,parcel_fractions_in_gridcells,PSRC_2000_data_quality_indicators.land_use_generic_reclass
##Output: gridcells table fields - GRID_ID, COMMERCIAL_SQFT, GOVERNMENTAL_SQFT, INDUSTRIAL_SQFT,
##RESIDENTIAL_UNITS,LAND_VALUE,IMPROVEMENT_VALUE,YEAR_BUILT
##Run: in MySQL 

USE peters_playhouse;

set session big_tables = 1;

# create back-up table of gridcells table in case SQL function incorrectly
drop table if exists gridcells_bak;
create table gridcells_bak select * from gridcells;

# create table gridcells table from PSRC_parcels_all_counties.parcels table. 
create table if not exists gridcells (
GRID_ID int(11) primary key,
CITY_ID int(11),
COUNTY_ID int(11),
DEVELOPMENT_TYPE_ID int(11),
PLAN_TYPE_ID int(11),
ZONE_ID int(11),
COMMERCIAL_SQFT int(11),
GOVERNMENTAL_SQFT int(11),
INDUSTRIAL_SQFT int(11),
COMMERCIAL_IMPROVEMENT_VALUE int(11),
GOVERNMENTAL_IMPROVEMENT_VALUE int(11),
INDUSTRIAL_IMPROVEMENT_VALUE int(11),
NONRESIDENTIAL_LAND_VALUE int(11),
RESIDENTIAL_IMPROVEMENT_VALUE int(11),
RESIDENTIAL_LAND_VALUE int(11),
RESIDENTIAL_UNITS int(11),
YEAR_BUILT int(11),
DISTANCE_TO_ARTERIAL float(11),
DISTANCE_TO_HIGHWAY float(11),
RELATIVE_X int(11),
RELATIVE_Y int(11),
PERCENT_WATER int(11),
PERCENT_STREAM_BUFFER int(11),
PERCENT_FLOODPLAIN int(11),
PERCENT_WETLAND int(11),
PERCENT_SLOPE int(11),
PERCENT_OPEN_SPACE int(11),
PERCENT_PUBLIC_SPACE int(11),
PERCENT_ROADS int(11),
PERCENT_UNDEVELOPABLE DOUBLE, 
IS_OUTSIDE_URBAN_GROWTH_BOUNDARY smallint(6),
FRACTION_RESIDENTIAL_LAND double(6,3),
TOTAL_NONRES_SQFT int(11),
TOTAL_UNDEVELOPABLE_SQFT INT(11)
);

DELETE FROM gridcells;

# Add index (if it doesn't exist) to the county and land use columns on the parcel table
alter table parcels add index county_lu_indx (county(3), land_use);

# Add index (if it doesn't exist) to the parcel_id and county columns on the parcel table
alter table parcels add index pin_cnty_indx (parcel_id(10), county(3));

##insert GRID_ID from parcel_fractions_in_gridcells table.
insert into gridcells (GRID_ID)
select DISTINCT GRID_ID 
from parcel_fractions_in_gridcells;

# Run script to calculate COMMERCIAL_SQFT, GOVERNMENTAL_SQFT, INDUSTRIAL_SQFT, TOTAL_NONRES_SQFT
#and YEAR_BUILT for gridcells based on building data.
\. /projects/urbansim7/scripts/public/data_prep/gridcell_generation_from_buildings.sql


#UPDATE RESIDENTIAL_UNITS
CREATE temporary table tmp_table4
SELECT b.GRID_ID AS GRID_ID, round(sum(RESIDENTIAL_UNITS_IMPUTED * b.PARCEL_FRACTION)) as RESIDENTIAL_UNITS
FROM parcels a inner join parcel_fractions_in_gridcells b on a.PARCEL_ID = b. PARCEL_ID AND a.COUNTY = b.COUNTY
GROUP BY b.GRID_ID;

alter table tmp_table4 add index grid_indx(grid_id);

update gridcells, tmp_table4
set gridcells.RESIDENTIAL_UNITS = tmp_table4.RESIDENTIAL_UNITS
WHERE gridcells.GRID_ID = tmp_table4.GRID_ID;
###########################################################
#UPDATE RESIDENTIAL LAND VALUE
CREATE temporary table tmp_table5a
SELECT b.GRID_ID AS GRID_ID, sum(a.LAND_VALUE * b.PARCEL_FRACTION) as RESIDENTIAL_LAND_VALUE
FROM (parcels a inner join parcel_fractions_in_gridcells b on a.PARCEL_ID = b. PARCEL_ID AND a.COUNTY = b.COUNTY) 
inner join PSRC_2000_data_quality_indicators.land_use_generic_reclass c 
on a.COUNTY = c.COUNTY and a.LAND_USE = c.COUNTY_LAND_USE_CODE
WHERE c.generic_land_use_2 = 'R'
GROUP BY b.GRID_ID;

alter table tmp_table5a add index grid_indx(grid_id);

update gridcells, tmp_table5a
set gridcells.RESIDENTIAL_LAND_VALUE = tmp_table5a.RESIDENTIAL_LAND_VALUE
WHERE gridcells.GRID_ID = tmp_table5a.GRID_ID; 

#UPDATE NONRESIDENTIAL LAND VALUE
CREATE temporary table tmp_table5b
SELECT b.GRID_ID AS GRID_ID, sum(a.LAND_VALUE * b.PARCEL_FRACTION) as NONRESIDENTIAL_LAND_VALUE
FROM (parcels a inner join parcel_fractions_in_gridcells b on a.PARCEL_ID = b. PARCEL_ID AND a.COUNTY = b.COUNTY) 
inner join PSRC_2000_data_quality_indicators.land_use_generic_reclass c 
on a.COUNTY = c.COUNTY and a.LAND_USE = c.COUNTY_LAND_USE_CODE
WHERE c.generic_land_use_2 = 'C' OR c.generic_land_use_2 = 'I' 
OR c.generic_land_use_2 = 'G'OR c.generic_land_use_2 = 'NR'
GROUP BY b.GRID_ID;

alter table tmp_table5b add index grid_indx(grid_id);

update gridcells, tmp_table5b
set gridcells.NONRESIDENTIAL_LAND_VALUE = tmp_table5b.NONRESIDENTIAL_LAND_VALUE
WHERE gridcells.GRID_ID = tmp_table5b.GRID_ID; 


#UPDATE INDUSTRIAL IMPROVEMENT VALUE
CREATE temporary table tmp_table6a
SELECT b.GRID_ID AS GRID_ID, sum(a.IMPROVEMENT_VALUE * b.PARCEL_FRACTION) as INDUSTRIAL_IMPROVEMENT_VALUE
FROM (parcels a inner join parcel_fractions_in_gridcells b on a.PARCEL_ID = b. PARCEL_ID AND a.COUNTY = b.COUNTY) 
inner join PSRC_2000_data_quality_indicators.land_use_generic_reclass c 
on a.COUNTY = c.COUNTY and a.LAND_USE = c.COUNTY_LAND_USE_CODE
WHERE c.generic_land_use_2 = 'I'
GROUP BY b.GRID_ID;

alter table tmp_table6a add index grid_indx(grid_id);

update gridcells, tmp_table6a
set gridcells.INDUSTRIAL_IMPROVEMENT_VALUE = tmp_table6a.INDUSTRIAL_IMPROVEMENT_VALUE
WHERE gridcells.GRID_ID = tmp_table6a.GRID_ID; 

#UPDATE GOVERNMENTAL IMPROVEMENT VALUE
CREATE temporary table tmp_table6b
SELECT b.GRID_ID AS GRID_ID, sum(a.IMPROVEMENT_VALUE * b.PARCEL_FRACTION) as GOVERNMENTAL_IMPROVEMENT_VALUE
FROM (parcels a inner join parcel_fractions_in_gridcells b on a.PARCEL_ID = b. PARCEL_ID AND a.COUNTY = b.COUNTY) 
inner join PSRC_2000_data_quality_indicators.land_use_generic_reclass c 
on a.COUNTY = c.COUNTY and a.LAND_USE = c.COUNTY_LAND_USE_CODE
WHERE c.generic_land_use_2 = 'G'
GROUP BY b.GRID_ID;

alter table tmp_table6b add index grid_indx(grid_id);

update gridcells, tmp_table6b
set gridcells.GOVERNMENTAL_IMPROVEMENT_VALUE = tmp_table6b.GOVERNMENTAL_IMPROVEMENT_VALUE
WHERE gridcells.GRID_ID = tmp_table6b.GRID_ID; 

#UPDATE COMMERCIAL IMPROVEMENT VALUE
CREATE temporary table tmp_table6c
SELECT b.GRID_ID AS GRID_ID, sum(a.IMPROVEMENT_VALUE * b.PARCEL_FRACTION) as COMMERCIAL_IMPROVEMENT_VALUE
FROM (parcels a inner join parcel_fractions_in_gridcells b on a.PARCEL_ID = b. PARCEL_ID AND a.COUNTY = b.COUNTY) 
inner join PSRC_2000_data_quality_indicators.land_use_generic_reclass c 
on a.COUNTY = c.COUNTY and a.LAND_USE = c.COUNTY_LAND_USE_CODE
WHERE c.generic_land_use_2 = 'C'
GROUP BY b.GRID_ID;

alter table tmp_table6c add index grid_indx(grid_id);

update gridcells, tmp_table6c
set gridcells.COMMERCIAL_IMPROVEMENT_VALUE = tmp_table6c.COMMERCIAL_IMPROVEMENT_VALUE
WHERE gridcells.GRID_ID = tmp_table6c.GRID_ID; 

#UPDATE RESIDENTIAL IMPROVEMENT VALUE
CREATE temporary table tmp_table6d
SELECT b.GRID_ID AS GRID_ID, sum(a.IMPROVEMENT_VALUE * b.PARCEL_FRACTION) as RESIDENTIAL_IMPROVEMENT_VALUE
FROM (parcels a inner join parcel_fractions_in_gridcells b on a.PARCEL_ID = b. PARCEL_ID AND a.COUNTY = b.COUNTY) 
inner join PSRC_2000_data_quality_indicators.land_use_generic_reclass c 
on a.COUNTY = c.COUNTY and a.LAND_USE = c.COUNTY_LAND_USE_CODE
WHERE c.generic_land_use_2 = 'R'
GROUP BY b.GRID_ID;

alter table tmp_table6d add index grid_indx(grid_id);

update gridcells_new, tmp_table6d
set gridcells_new.RESIDENTIAL_IMPROVEMENT_VALUE = tmp_table6d.RESIDENTIAL_IMPROVEMENT_VALUE
WHERE gridcells_new.GRID_ID = tmp_table6d.GRID_ID; 

# UPDATE FRACTION_RESIDENTIAL_LAND
CREATE TEMPORARY TABLE tmp_frac_res_land_1
SELECT 
f.grid_id,
(sum(if(c.generic_land_use_2 = 'R', p.lot_sqft * f.parcel_fraction, 0))/sum(p.lot_sqft * f.parcel_fraction))*100/100 AS frac_res
FROM 
parcels p
INNER JOIN parcel_fractions_in_gridcells f
on p.PARCEL_ID = f. PARCEL_ID AND p.COUNTY = f.COUNTY
INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass c 
on p.COUNTY = c.COUNTY and p.LAND_USE = c.COUNTY_LAND_USE_CODE
GROUP BY f.GRID_ID
;

CREATE UNIQUE INDEX GRID_ID ON tmp_frac_res_land_1 (GRID_ID);

update gridcells, tmp_frac_res_land_1
set gridcells.FRACTION_RESIDENTIAL_LAND = tmp_frac_res_land_1.frac_res
WHERE gridcells.GRID_ID = tmp_frac_res_land_1.GRID_ID; 

create table gridcells_new
 select 
 A.GRID_ID,
 A.CITY_ID, 
 A.COUNTY_ID, 
 A.DEVELOPMENT_TYPE_ID,
 A.PLAN_TYPE_ID,
 A.ZONE_ID,
 A.COMMERCIAL_SQFT,
 A.GOVERNMENTAL_SQFT,
 A.INDUSTRIAL_SQFT,
 A.COMMERCIAL_IMPROVEMENT_VALUE,
 A.GOVERNMENTAL_IMPROVEMENT_VALUE,
 A.INDUSTRIAL_IMPROVEMENT_VALUE,
 A.NONRESIDENTIAL_LAND_VALUE,
 A.RESIDENTIAL_LAND_VALUE,
 A.RESIDENTIAL_UNITS,
 A.YEAR_BUILT,
 A.DISTANCE_TO_ARTERIAL,
 A.DISTANCE_TO_HIGHWAY,
 A.RELATIVE_X,
 A.RELATIVE_Y,
 A.PERCENT_WATER,
 A.PERCENT_STREAM_BUFFER,
 A.PERCENT_FLOODPLAIN,
 A.PERCENT_WETLAND,
 A.PERCENT_SLOPE,
 A.PERCENT_OPEN_SPACE,
 A.PERCENT_ROADS,
 A.PERCENT_UNDEVELOPABLE,
 A.IS_OUTSIDE_URBAN_GROWTH_BOUNDARY,
 A.TOTAL_NONRES_SQFT,
 A.TOTAL_UNDEVELOPABLE_SQFT,
 F.FRAC_RES as FRACTION_RESIDENTIAL_LAND
 FROM gridcells AS A
 INNER JOIN tmp_frac_res_land_1 AS F
 ON A.GRID_ID = F.GRID_ID 
;

#############
# Get residential units for gridcells in blocks that had no parcels 
# Get list of blocks BG for which unit imputation failed
 
DROP TABLE IF EXISTS temp_imputed_units_by_block;
create temporary table temp_imputed_units_by_block
select CENSUS_BLOCK, sum(RESIDENTIAL_UNITS_IMPUTED) AS RES_UNITS
FROM parcels
GROUP BY CENSUS_BLOCK;

CREATE UNIQUE INDEX blockindex on temp_imputed_units_by_block (CENSUS_BLOCK(15));

CREATE TEMPORARY TABLE census_block_imputed_unit_discrepancies
SELECT 
B.CENSUS_BLOCK_ID AS CENSUS_BLOCK, 
IFNULL(A.RES_UNITS,0) AS IMPUTED_UNITS, 
B.UNITS AS CENSUS_UNITS
FROM PSRC_2000_data_quality_indicators.block_residential_units AS B 
LEFT OUTER JOIN temp_imputed_units_by_block AS A 
ON A.CENSUS_BLOCK = B.CENSUS_BLOCK_ID
WHERE A.CENSUS_BLOCK IS NULL
AND B.UNITS > 0
;

CREATE UNIQUE INDEX blk_indx ON census_block_imputed_unit_discrepancies (CENSUS_BLOCK(15));
# Distribute the units from BG across gridcells

CREATE TEMPORARY TABLE unit_fractions
SELECT
g.GRID_ID,
bfg.block_fraction,
(bfg.block_fraction * ud.CENSUS_UNITS) AS UNITS
FROM PSRC_2000_data_quality_indicators.block_fractions_in_gridcells bfg 
INNER JOIN census_block_imputed_unit_discrepancies ud ON bfg.stfid = ud.census_block
INNER JOIN gridcells_new g ON g.grid_id = bfg.grid_id
;

CREATE INDEX id_indx on unit_fractions (GRID_ID);

CREATE TEMPORARY TABLE census_units_summed
SELECT 
GRID_ID,
IFNULL(round(SUM(UNITS)),0) AS UNITS
FROM unit_fractions
GROUP BY GRID_ID
;

CREATE UNIQUE INDEX id_indx on census_units_summed (grid_id);

UPDATE census_units_summed cus
INNER JOIN gridcells_new g on g.grid_id = cus.grid_id
SET g.residential_units = g.residential_units + round(cus.units)
;

DROP TABLE gridcells;
ALTER TABLE gridcells_new RENAME AS gridcells;

DROP TABLE tmp_table4;
DROP TABLE tmp_table5a;
DROP TABLE tmp_table5b;
DROP TABLE tmp_table6a;
DROP TABLE tmp_table6b;
DROP TABLE tmp_table6c;
DROP TABLE tmp_table6d;
DROP TABLE tmp_frac_res_land_1;

#############################################################################################################
# New Gridcell generation process for PSRC_2000_baseyear generated from PSRC_parcels_all_counties.gridcells table
# 

USE PSRC_2000_baseyear;

SET SESSION big_tables = 1;

# create backup copy of gridcells table in case something goes wrong during script execution. 
DROP TABLE if exists gridcells_bak;
CREATE TABLE gridcells_bak select * from gridcells;

## Set gridcell fields to 0
UPDATE gridcells SET 
COMMERCIAL_SQFT = 0,
GOVERNMENTAL_SQFT = 0,
INDUSTRIAL_SQFT = 0,
COMMERCIAL_IMPROVEMENT_VALUE = 0,
INDUSTRIAL_IMPROVEMENT_VALUE = 0,
GOVERNMENTAL_IMPROVEMENT_VALUE = 0,
NONRESIDENTIAL_LAND_VALUE = 0,
RESIDENTIAL_LAND_VALUE = 0,
RESIDENTIAL_IMPROVEMENT_VALUE = 0,
RESIDENTIAL_UNITS = 0,
YEAR_BUILT = 0,
FRACTION_RESIDENTIAL_LAND = 0,
PERCENT_UNDEVELOPABLE = 0,
TOTAL_NONRES_SQFT = 0,
TOTAL_UNDEVELOPABLE_SQFT = 0;

 CREATE TEMPORARY TABLE tmp_gridcells
 SELECT 
A.GRID_ID,
IFNULL(A.COMMERCIAL_SQFT,0) + IFNULL(B.COMMERCIAL_SQFT,0) AS COMMERCIAL_SQFT,
IFNULL(A.GOVERNMENTAL_SQFT,0) + IFNULL(B.GOVERNMENTAL_SQFT,0) AS GOVERNMENTAL_SQFT,
IFNULL(A.INDUSTRIAL_SQFT,0) + IFNULL(B.INDUSTRIAL_SQFT,0) AS INDUSTRIAL_SQFT,
IFNULL(A.COMMERCIAL_IMPROVEMENT_VALUE,0) + IFNULL(B.COMMERCIAL_IMPROVEMENT_VALUE,0) AS COMMERCIAL_IMPROVEMENT_VALUE,
IFNULL(A.INDUSTRIAL_IMPROVEMENT_VALUE,0) + IFNULL(B.INDUSTRIAL_IMPROVEMENT_VALUE,0) AS INDUSTRIAL_IMPROVEMENT_VALUE,
IFNULL(A.GOVERNMENTAL_IMPROVEMENT_VALUE,0) + IFNULL(B.GOVERNMENTAL_IMPROVEMENT_VALUE,0) AS GOVERNMENTAL_IMPROVEMENT_VALUE,
IFNULL(A.NONRESIDENTIAL_LAND_VALUE,0) + IFNULL(B.NONRESIDENTIAL_LAND_VALUE,0) AS NONRESIDENTIAL_LAND_VALUE,
IFNULL(A.RESIDENTIAL_LAND_VALUE,0) + IFNULL(B.RESIDENTIAL_LAND_VALUE,0) AS RESIDENTIAL_LAND_VALUE,
IFNULL(A.RESIDENTIAL_IMPROVEMENT_VALUE,0) + IFNULL(B.RESIDENTIAL_IMPROVEMENT_VALUE,0) AS RESIDENTIAL_IMPROVEMENT_VALUE,
IFNULL(A.RESIDENTIAL_UNITS,0) + IFNULL(B.RESIDENTIAL_UNITS,0) AS RESIDENTIAL_UNITS,
B.YEAR_BUILT,
(IFNULL(A.FRACTION_RESIDENTIAL_LAND,0) + IFNULL(B.FRACTION_RESIDENTIAL_LAND,0)) AS FRACTION_RESIDENTIAL_LAND,
0 AS PERCENT_UNDEVELOPABLE,
IFNULL(A.TOTAL_NONRES_SQFT,0) + IFNULL(B.TOTAL_NONRES_SQFT,0) AS TOTAL_NONRES_SQFT,
IFNULL(A.TOTAL_UNDEVELOPABLE_SQFT,0) + IFNULL(B.TOTAL_UNDEVELOPABLE_SQFT,0) AS TOTAL_UNDEVELOPABLE_SQFT,
0 AS DEVELOPMENT_TYPE_ID,
A.DISTANCE_TO_ARTERIAL,
A.DISTANCE_TO_HIGHWAY,
A.RELATIVE_X,
A.RELATIVE_Y,
A.PLAN_TYPE_ID,
A.PERCENT_WATER, 
A.PERCENT_WETLAND, 
A.PERCENT_STREAM_BUFFER, 
A.PERCENT_FLOODPLAIN,
A.PERCENT_SLOPE, 
A.PERCENT_OPEN_SPACE,
A.PERCENT_PUBLIC_SPACE,
A.PERCENT_ROADS, 
A.IS_OUTSIDE_URBAN_GROWTH_BOUNDARY,
A.IS_INSIDE_NATIONAL_FOREST, 
A.IS_INSIDE_TRIBAL_LAND, 
A.IS_INSIDE_MILITARY_BASE, 
A.ZONE_ID, 
A.CITY_ID, 
A.COUNTY_ID,
A.PERCENT_AGRICULTURAL_PROTECTED_LANDS,
A.ACRES
FROM 
gridcells A
LEFT JOIN PSRC_parcels_all_counties.gridcells B ON A.GRID_ID = B.GRID_ID
;

DROP TABLE gridcells;
ALTER TABLE tmp_gridcells RENAME AS gridcells;

########################################################################################################
# Test for creating new gridcells table from building records in order to work around 'table is full' error message
########################################################################################################

# get list of total built_sqft by county-pin for commercial buildings.
CREATE TEMPORARY TABLE tmp_building_summary_com
SELECT a.COUNTY, a.PARCEL_ID, SUM(a.IMPUTED_SQFT) AS BUILT_SQFT
FROM buildings a inner join PSRC_2000_data_quality_indicators.building_use_generic_reclass b
ON a.COUNTY = b.COUNTY AND a.BUILDING_USE = b.COUNTY_BUILDING_USE_CODE
WHERE b.generic_building_use_2 = 'C'
GROUP BY a.COUNTY, a.PARCEL_ID;

ALTER TABLE tmp_building_summary_com ADD INDEX prcl_cnty_indx (parcel_id(12), county(3));

# Distribute commercial sqft across gridcells
CREATE temporary table tmp_table1
SELECT b.GRID_ID AS GRID_ID, sum(a.BUILT_SQFT * b.PARCEL_FRACTION) as COMMERCIAL_SQFT
FROM (tmp_building_summary_com a right join parcel_fractions_in_gridcells b on a.PARCEL_ID = b.PARCEL_ID AND a.COUNTY = b.COUNTY) 
GROUP BY b.GRID_ID;

alter table tmp_table1 add index grid_indx(grid_id);

set session big_tables = 1;

create temporary table tmp_gridcells_com
 select 
 A.GRID_ID,
 A.CITY_ID, 
 A.COUNTY_ID, 
 A.DEVELOPMENT_TYPE_ID,
 A.PLAN_TYPE_ID,
 A.ZONE_ID,
 B.COMMERCIAL_SQFT,
 A.GOVERNMENTAL_SQFT,
 A.INDUSTRIAL_SQFT,
 A.COMMERCIAL_IMPROVEMENT_VALUE,
 A.GOVERNMENTAL_IMPROVEMENT_VALUE,
 A.INDUSTRIAL_IMPROVEMENT_VALUE,
 A.NONRESIDENTIAL_LAND_VALUE,
 A.RESIDENTIAL_LAND_VALUE,
 A.RESIDENTIAL_IMPROVEMENT_VALUE,
 A.RESIDENTIAL_UNITS,
 A.YEAR_BUILT,
 A.DISTANCE_TO_ARTERIAL,
 A.DISTANCE_TO_HIGHWAY,
 A.RELATIVE_X,
 A.RELATIVE_Y,
 A.PERCENT_WATER,
 A.PERCENT_STREAM_BUFFER,
 A.PERCENT_FLOODPLAIN,
 A.PERCENT_WETLAND,
 A.PERCENT_SLOPE,
 A.PERCENT_OPEN_SPACE,
 A.PERCENT_ROADS,
 A.PERCENT_UNDEVELOPABLE,
 A.IS_OUTSIDE_URBAN_GROWTH_BOUNDARY,
 A.TOTAL_NONRES_SQFT,
 A.TOTAL_UNDEVELOPABLE_SQFT,
 A.FRACTION_RESIDENTIAL_LAND
 FROM gridcells AS A
 LEFT JOIN tmp_table1 AS B
 ON A.GRID_ID = B.GRID_ID 
;

# update gridcells, tmp_table1
# set gridcells.COMMERCIAL_SQFT = tmp_table1.COMMERCIAL_SQFT
# WHERE gridcells.GRID_ID = tmp_table1.GRID_ID;

drop table tmp_building_summary_com;
drop table tmp_table1;


########################################################################################################

create table STEP (STEP text, SIC int(11), SECTOR text, TRAVEL_MODEL_SECTOR INT, TRAVEL_MODEL TEXT); 

insert into STEP (SIC, SECTOR)
 select SIC, DIVISION as SECTOR from job_allocation_king.sic_sector 
 group by SIC, DIVISION;
 
create table step_to_sector_reclass (STEP text, SECTOR text);
 
INSERT INTO step_to_sector_reclass (STEP, SECTOR)
 VALUES 
 ('Const/Res', 'Agriculture'),
 ('Const/Res','Construction'),
 ('Const/Res', 'Mining'),
 ('MANUF', 'Manufacturing'),
 ('WTCU', 'Transportation, Communications, Electric, Gas, San'),
 ('WTCU', 'Wholesale Trade'),
 ('RETAIL', 'Retail Trade'),
 ('FIRES', 'FIRES'),
 ('FIRES', 'Services'),
 ('GOVED', 'FEDERAL, CIVILIAN'),
 ('GOVED', 'FEDERAL, MILITARY'),
 ('GOVED', 'PUBLIC Administration'),
 ('GOVED', 'STATE AND LOCAL'),
 ('GOVED', 'EDUCATION K-12'),
 ('GOVED', 'EDUCATION HIGHER')
 ;
 
 update STEP as a inner join step_to_sector_reclass as b on a.sector = b.sector set a.STEP = b.STEP;

#######################################
alter table emploment_sectors rename as employment_sectors_job_allocator;

create table employment_sectors (SECTOR_ID int, NAME text);

insert into employment_sectors (SECTOR_ID, NAME)
 values 
 (1, 'Agriculture'),
 (2, 'Forestry, Fishing, and Mining'),
 (3, 'Forestry, Fishing, and Mining'),
 (4, 'Food Products'),
 (5, 'Textiles and Apparel'),
 (6, 'Wood Products'),
 (7, 'Paper Products'),
 (8, 'Printing and Publishing'),
 (9, 'Chemcicals and Petroleum'),
 (10, 'Stone, Clay, and Glass Products'),
 (11, 'Primary Metals'),
 (12, 'Fabricated Metals'),
 (13, 'Nonelectric Machinery'),
 (14, 'Electrical Machinery'),
 (15, 'Aerospace'), 
 (16, 'Ship and Boatbuilding'),
 (17, 'Other Transportation Equipment'),
 (18, 'Other Manufacturing'),
 (19, 'Construction'),
 (20, 'Transportation, Communications, and Utilities'),
 (21, 'Wholesale Trade'),
 (22, 'Eating and Drinking Places'), 
 (23, 'Other Retail Trade'),
 (24, 'Finance, Insurance, and Real Estate'),
 (25, 'Producer Services'),
 (26, 'Consumer Services'),
 (27, 'Health Services'),
 (28, 'Federal Government, Civilian'),
 (29, 'Federal Government, Military'),
 (30, 'Education, K-12'),
 (31, 'Education, Higher'),
 (32, 'Public Administration'),
 (33, 'State and Local Government')
; 

###########################################

PSRC 2000 Baseyear consistence checker

# Create pseudo tables from WFRC_1997_baseyear. Remember to delete tables once consistency checker has passed.

create table developer_model_coefficients select * from WFRC_1997_baseyear.developer_model_coefficients;
create table developer_model_specification select * from WFRC_1997_baseyear.developer_model_specification;

create table employment_location_choice_model_coefficients select * from WFRC_1997_baseyear.employment_location_choice_model_coefficients;
create table employment_location_choice_model_specification select * from WFRC_1997_baseyear.employment_location_choice_model_specification;

alter table employment_location_choice_model_coefficients change column SUB_MODEL_ID SUB_MODEL_ID int;

alter table employment_location_choice_model_specification change column SUB_MODEL_ID SUB_MODEL_ID int;
alter table employment_location_choice_model_specification change column EQUATION_ID EQUATION_ID int;

create table residential_land_share_model_coefficients select * from WFRC_1997_baseyear.residential_land_share_model_coefficients;
create table residential_land_share_model_specification select * from WFRC_1997_baseyear.residential_land_share_model_specification;

create tableselect * from WFRC_1997_baseyear. ;


drop table developer_model_coefficients;
drop table developer_model_specification;
drop table employment_location_choice_model_coefficients;
drop table employment_location_choice_model_specification;
drop table residential_land_share_model_coefficients;
drop table residential_land_share_model_specification;


##############################################

# PSRC_2000_baseyear check-off list.

CREATE TABLE URBANSIM_INPUT_TABLES (TABLE_NAME text, AUTOMATED_SCRIPT tinyint, TABLE_COMPLETED tinyint, COMMENTS text);

INSERT INTO URBANSIM_INPUT_TABLES (TABLE_NAME, AUTOMATED_SCRIPT, TABLE_COMPLETED)
 VALUES
 ('annual_employment_control_totals',0, 0),
 ('annual_household_control_totals', 0, 0),
 ('annual_relocation_rates_for_households', 0, 0),
 ('annual_relocation_rates_for_jobs', 0, 0),
 ('base_year', 0, 1),
 ('cities', 0, 1),
 ('counties', 0, 1),
 ('development_constraints', 0, 0 ),
 ('development_constraint_events', 0, 0),
 ('development_events', 0, 0),
 ('development_event_history', 1, 1),
 ('developer_model_alternative_shares', 0, 0),
 ('developer_model_coefficients', 0, 0),
 ('developer_model_specifications', 0, 0),
 ('development_types', 1, 1),
 ('development_type_groups', 0, 1),
 ('development_type_group_definitions', 0, 1),
 ('employment_events', 0, 0),
 ('employment_location_choice_coefficients', 0, 0),
 ('employment_location_choice_model_specifications', 0, 0),
 ('employment_sectors', 0, 0),
 ('employment_adhoc_sector_groups', 0, 1),
 ('employment_adhoc_sector_group_definitions', 0, 0),
 #('geographies', 0, 0),
 #('geography_names', 0, 0),
 ('gridcell_fractions_in_zones', 0, 1),
 ('gridcells', 1, 1),
 #('gridcells_in_geographies', 0, 0),
 ('household_characteristics_for_hlc', 0, 1),
 ('household_characteristics_for_ht', 0, 0),
 ('household_location_choice_coefficients', 0, 0),
 ('household_location_choice_specification', 0, 0),
 ('households', 1, 1),
 ('jobs', 1, 1),
 ('land_price_coefficients', 0, 0),
 ('land_price_model_specification', 0, 0),
 ('land_use_events', 0, 0),
 ('models', 0, 1),
 ('model_variables', 0, 0),
 ('plan_types', 0, 1),
 ('primary_uses', 0, 0),
 ('race_names', 0, 1),
 ('residential_land_share_coefficients', 0, 0),
 ('residential_land_share_specification', 0, 0),
 ('residential_units_for_home_based_jobs', 0, 0),
 ('sampling_rates', 0, 0),
 ('scenario_information', 0, 0),
 ('sqft_for_non_home_based_jobs',0, 0 ),
 ('target_vacancies', 0, 0),
 ('transition_types', 0, 0),
 ('travel_data', 0, 1),
 ('urbansim_constants', 0, 0),
 ('zones', 0, 1)
 ;
 
 
##################################################

# Snohomish County updates to building use codes via Mark Simons PSRC

update Final_LRSN_Flagged set Adj_GBU1 = 'Imputed - School' where Adj_GBU1 = 'School';
update Final_LRSN_Flagged set Adj_GBU1 = 'Imputed - Commercial' where Adj_GBU1 = 'Commercial';
update Final_LRSN_Flagged set Adj_GBU1 = 'Imputed - Civic and Quasi-Public' where Adj_GBU1 = 'Civic and Quasi-Public';

select count(*) from buildings_not_imputed a inner join Final_LRSN_Flagged b on a.parcel_id = b.lrsn and a.building_use = b.building_u; 

update buildings_not_imputed a inner join Final_LRSN_Flagged b on a.parcel_id = b.lrsn and a.building_use = b.building_u 
 set a.building_use = b.adj_gbu1;


 
###############################################

#DQI maps from PSRC_2000_base_run_output_petecaba (30 year run with travel model 2010, 2020, 2030) map only year 2030

## Population 
CREATE TABLE map_population_per_acre_20041005
 SELECT a.ZONE_ID,
 SUM(b.PERSONS) as PERSONS
 FROM PSRC_2000_base_run_output_petecaba.households_exported a 
INNER JOIN PSRC_2000_base_run_output_petecaba.households_constants b 
 ON a.household_id = b.household_id 
WHERE a.YEAR = 2030 
GROUP BY a.ZONE_ID
;

## Residential Units
CREATE TABLE map_residential_units_per_acre_20041005
 SELECT b.ZONE_ID,
 SUM(a.RESIDENTIAL_UNITS) AS RESIDENTIAL_UNITS
 FROM PSRC_2000_base_run_output_petecaba.gridcells_exported a 
 INNER JOIN GSPSRC_2000_baseyear_flattened.gridcells b
ON a.grid_id = b.grid_id
 WHERE YEAR = 2030
 GROUP BY b.ZONE_ID
; 

## Employment
CREATE TABLE map_employment_per_acre_20041005
 SELECT ZONE_ID,
 COUNT(*) AS JOBS
 FROM PSRC_2000_base_run_output_petecaba.jobs_exported
 WHERE YEAR = 2030
 GROUP BY ZONE_ID
;

## Non-residential Floor Space 
CREATE TABLE map_non_residential_floor_space_per_acre_20041005
 SELECT b.ZONE_ID,
 SUM(a.commercial_sqft + a.industrial_sqft + a.governmental_sqft) as NONRES_SQFT
 FROM PSRC_2000_base_run_output_petecaba.gridcells_exported a 
 INNER JOIN GSPSRC_2000_baseyear_flattened.gridcells b 
ON a.grid_id = b.grid_id 
 WHERE a.YEAR = 2030
 GROUP BY b.ZONE_ID
;
UPDATE map_non_residential_floor_space_per_acre_20041005 SET NONRES_SQFT = NONRES_SQFT / 1000;

## Land Price
CREATE TABLE map_land_price_per_acre_20041005
 SELECT b.ZONE_ID,
 SUM(a.NONRESIDENTIAL_LAND_VALUE) AS NONRES_LAND_VALUE
 FROM PSRC_2000_base_run_output_petecaba.gridcells_exported a 
 INNER JOIN GSPSRC_2000_baseyear_flattened.gridcells b 
ON a.grid_id = b.grid_id
 WHERE a.YEAR = 2030
 GROUP BY b.ZONE_ID
; 

###############################################

## Use GSPSRC_2000_baseyear_flattened (2000)
# Population
CREATE TABLE map_baseyear_population_per_acre_20041006
 SELECT b.ZONE_ID,
 SUM(a.PERSONS) as PERSONS
 FROM GSPSRC_2000_baseyear_flattened.households a
 INNER JOIN GSPSRC_2000_baseyear_flattened.gridcells b 
ON a.grid_id = b.grid_id
 GROUP BY b.ZONE_ID
;

## Residential Units
CREATE TABLE map_baseyear_residential_units_per_acre_20041006
 SELECT ZONE_ID,
 SUM(RESIDENTIAL_UNITS) AS RESIDENTIAL_UNITS
 FROM GSPSRC_2000_baseyear_flattened.gridcells 
 GROUP BY ZONE_ID
;

## Employment
CREATE TABLE map_baseyear_employment_per_acre_20041006
 SELECT b.ZONE_ID,
 COUNT(*) AS JOBS
 FROM GSPSRC_2000_baseyear_flattened.jobs a
 INNER JOIN GSPSRC_2000_baseyear_flattened.gridcells b
ON a.grid_id = b.grid_id
 GROUP BY b.ZONE_ID
;

## Non-residential Floor Space 
CREATE TABLE map_baseyear_non_residential_floor_space_per_acre_20041006
 SELECT ZONE_ID,
 SUM(commercial_sqft + industrial_sqft + governmental_sqft) as NONRES_SQFT
 FROM GSPSRC_2000_baseyear_flattened.gridcells
 GROUP BY ZONE_ID
;
UPDATE map_baseyear_non_residential_floor_space_per_acre_20041006 SET NONRES_SQFT = NONRES_SQFT / 1000;

## Non-Residential Land Price
CREATE TABLE map_baseyear_land_price_per_acre_20041006
 SELECT ZONE_ID,
 SUM(NONRESIDENTIAL_LAND_VALUE) AS NONRES_LAND_VALUE
 FROM GSPSRC_2000_baseyear_flattened.gridcells 
 GROUP BY ZONE_ID
;

## Total Land Price
CREATE TABLE map_baseyear_total_land_price_per_acre_20041007
 SELECT ZONE_ID,
 SUM(NONRESIDENTIAL_LAND_VALUE + RESIDENTIAL_LAND_VALUE) AS TOTAL_LAND_VALUE
 FROM GSPSRC_2000_baseyear_flattened.gridcells 
 GROUP BY ZONE_ID
;

#########################################################
#DQI maps from PSRC_2000_base_run_output (30 year run with travel model 2010, 2020, 2030) map only year 2030

## Population 
CREATE TABLE map_population_per_acre_20041012
 SELECT a.ZONE_ID,
 SUM(b.PERSONS) as PERSONS
 FROM PSRC_2000_base_run_output.households_exported a 
INNER JOIN PSRC_2000_base_run_output_petecaba.households_constants b 
 ON a.household_id = b.household_id 
WHERE a.YEAR = 2030 
GROUP BY a.ZONE_ID
;

## Residential Units
CREATE TABLE map_residential_units_per_acre_20041012
 SELECT b.ZONE_ID,
 SUM(a.RESIDENTIAL_UNITS) AS RESIDENTIAL_UNITS
 FROM PSRC_2000_base_run_output.gridcells_exported a 
 INNER JOIN GSPSRC_2000_baseyear_flattened.gridcells b
ON a.grid_id = b.grid_id
 WHERE YEAR = 2030
 GROUP BY b.ZONE_ID
; 

## Employment
CREATE TABLE map_employment_per_acre_20041012
 SELECT ZONE_ID,
 COUNT(*) AS JOBS
 FROM PSRC_2000_base_run_output.jobs_exported
 WHERE YEAR = 2030
 GROUP BY ZONE_ID
;

## Non-residential Floor Space 
CREATE TABLE map_non_residential_floor_space_per_acre_20041012
 SELECT b.ZONE_ID,
 SUM(a.commercial_sqft + a.industrial_sqft + a.governmental_sqft) as NONRES_SQFT
 FROM PSRC_2000_base_run_output.gridcells_exported a 
 INNER JOIN GSPSRC_2000_baseyear_flattened.gridcells b 
ON a.grid_id = b.grid_id 
 WHERE a.YEAR = 2030
 GROUP BY b.ZONE_ID
;
UPDATE map_non_residential_floor_space_per_acre_20041012 SET NONRES_SQFT = NONRES_SQFT / 1000;

## Land Price
CREATE TABLE map_land_price_per_acre_20041012
 SELECT b.ZONE_ID,
 SUM(a.NONRESIDENTIAL_LAND_VALUE + a.RESIDENTIAL_LAND_VALUE) AS TOTAL_LAND_VALUE
 FROM PSRC_2000_base_run_output.gridcells_exported a 
 INNER JOIN GSPSRC_2000_baseyear_flattened.gridcells b 
ON a.grid_id = b.grid_id
 WHERE a.YEAR = 2030
 GROUP BY b.ZONE_ID
; 

#############################################################

# Household control totals.
create table gridcells select 
a.GRID_ID, 
b.COMMERCIAL_SQFT,
b.GOVERNMENTAL_SQFT,
b.INDUSTRIAL_SQFT,
a.COMMERCIAL_IMPROVEMENT_VALUE,
a.INDUSTRIAL_IMPROVEMENT_VALUE,
a.GOVERNMENTAL_IMPROVEMENT_VALUE,
a.NONRESIDENTIAL_LAND_VALUE,
a.RESIDENTIAL_LAND_VALUE,
a.RESIDENTIAL_IMPROVEMENT_VALUE,
a.RESIDENTIAL_UNITS,
a.YEAR_BUILT,
a.FRACTION_RESIDENTIAL_LAND,
a.PERCENT_UNDEVELOPABLE,
b.TOTAL_NONRES_SQFT,
a.TOTAL_UNDEVELOPABLE_SQFT,
a.DEVELOPMENT_TYPE_ID,
a.DISTANCE_TO_ARTERIAL,
a.DISTANCE_TO_HIGHWAY,
a.RELATIVE_X,
a.RELATIVE_Y,
a.PLAN_TYPE_ID,
a.PERCENT_WATER,
a.PERCENT_WETLAND,
a.PERCENT_STREAM_BUFFER,
a.PERCENT_FLOODPLAIN,
a.PERCENT_SLOPE,
a.PERCENT_OPEN_SPACE,
a.PERCENT_PUBLIC_SPACE,
a.PERCENT_ROADS,
a.IS_OUTSIDE_URBAN_GROWTH_BOUNDARY,
a.IS_INSIDE_NATIONAL_FOREST,
a.IS_INSIDE_TRIBAL_LAND,
a.IS_INSIDE_MILITARY_BASE,
a.ZONE_ID,
a.CITY_ID,
a.COUNTY_ID,
a.PERCENT_AGR_KING,
a.ACRES,
a.PERCENT_AGRICULTURAL_PROTECTED_LANDS,
a.PERCENT_FOREST,
a.PERCENT_MINING,
a.PERCENT_ROW
from GSPSRC_2000_baseyear_flattened.gridcells a left join PSRC_2000_raw_tables.gridcells_partial b
on a.grid_id = b.grid_id;

#############################################3

/* Update Scenario D double regional growth
 1. Compute, for each year after the base year and for each sub-set of the population, a growth rate between that year (Year i) and the previous year (Year i-1) as:
 Growth = (Year[i] - Year[i-1])/Year[i-1]
 This should result in a table of annual growth rates.
 
 2. Create a new table of growth rates by doubling all of the values.
 Growth2 = 2*Growth
 
 3. Compute new control totals by applying the growth rates to the base-year counts and to each year after that in succussion:
Year[i] = Growth2*Year[i-1]
*/

CREATE TEMPORARY TABLE tmp_1 
 SELECT year, ((total_number_of_households - total_number_of_households)/total_number_of_households) as prelim_change
 from annual_household_control_totals 
 group by year;

UPDATE tmp_1 SET prelim_change = prelim_change * 2;


create table prelim_inc_growth_rate (year int, households int);
insert into prelim_inc_growth_rate (year, households) values 
(2000, 1282979),
(2001, 1329968),
(2002, 1359489),
(2003, 1386455),
(2004, 1423663),
(2005, 1464516),
(2006, 1512574),
(2007, 1568347),
(2008, 1627124),
(2009, 1682705),
(2010, 1734405),
(2011, 1780173),
(2012, 1826285),
(2013, 1880378),
(2014, 1939616),
(2015, 1996823),
(2016, 2056104),
(2017, 2114999),
(2018, 2176505),
(2019, 2246961),
(2020, 2321437),
(2021, 2386670),
(2022, 2450071),
(2023, 2510182),
(2024, 2574087),
(2025, 2630314),
(2026, 2683723),
(2027, 2739980),
(2028, 2799727),
(2029, 2860424),
(2030, 2921460);

create table annual_household_control_totals_test
 select a.YEAR,
 b.race as RACE_ID,
 b.PERSONS,
 b.combo * a.households as TOTAL_NUMBER_OF_HOUSEHOLDS
 from prelim_inc_growth_rate a, tmp_race_person_prop b;
 




######
# New ELC home_based coefficients table

CREATE TEMPORARY TABLE employment_home_based_location_choice_model_coefficients_test 
 SELECT * FROM GSPSRC_2000_baseyear_flattened.employment_home_based_location_choice_model_coefficients;
 
CREATE TEMPORARY TABLE employment_home_based_location_choice_model_specification_test
 SELECT * FROM GSPSRC_2000_baseyear_flattened.employment_home_based_location_choice_model_specification;

CREATE TEMPORARY TABLE employment_sectors_test
 SELECT * FROM GSPSRC_2000_baseyear_flattened.employment_sectors;

CREATE TABLE employment_home_based_location_choice_model_coefficients
 SELECT a.SECTOR_ID AS SUB_MODEL_ID,
 b.COEFFICIENT_NAME,
 b.ESTIMATE,
 b.STANDARD_ERROR,
 b.T_STATISTIC,
 b.P_VALUE
 FROM employment_sectors_test a, employment_home_based_location_choice_model_coefficients_test b
 ORDER BY a.SECTOR_ID
; 

CREATE TABLE employment_home_based_location_choice_model_specification
 SELECT a.SECTOR_ID AS SUB_MODEL_ID,
 b.EQUATION_ID,
 b.VARIABLE_NAME,
 b.COEFFICIENT_NAME
 FROM employment_sectors_test a,employment_home_based_location_choice_model_specficiation_test b
 ORDER BY a.SECTOR_ID
; 

DELETE FROM employment_home_based_location_choice_model_coefficients WHERE sub_model_id IN (14, 15, 16, 17, 18);
DELETE FROM employment_home_based_location_choice_model_specification WHERE sub_model_id IN (14, 15, 16, 17, 18);

DROP TABLE employment_sectors_test;
DROP TABLE employment_home_based_location_choice_model_coefficients_test;
DROP TABLE employment_home_based_location_choice_model_specification_test;


create table too_many_households
select GRID_ID, count(*) as HOUSEHOLDS from households where grid_id in (
387599,
388381,
389161,
389938,
529979,
532429,
532431,
572637,
573480,
573481,
574326,
575165,
575166,
575940,
576009,
576852,
576854,
611522,
651521,
653922,
714952,
718371,
718373,
719514,
791752,
816236,
890204,
893248,
896387) group by grid_id;

create table tmp_hh_in_block_530610527044
 select b.CNTYNAME,
 b.POPULATION,
 b.TOTAL_HOUSEHOLDS,
 b.FAMILY_HOUSEHOLDS,
 b.NONFAMILY_HOUSEHOLDS,
 b.RESIDENTIAL_VACANCY_RATE,
 SUM(a.RESIDENTIAL_UNITS) AS UNITS
 FROM gridcells a INNER JOIN PSRC_2000_household_synthesis.gridcell_block_group_mapping c
ON a.grid_id = c.grid_id
 INNER JOIN PSRC_2000_household_synthesis.block_group_summary b
ON c.sfid = b.sfid 
 where a.GRID_ID in
 (387599,
388381,
389161,
389938,
529979,
532429,
532431,
572637,
573480,
573481,
574326,
575165,
575166,
575940,
576009,
576852,
576854,
611522,
651521,
653922,
714952,
718371,
718373,
719514,
791752,
816236,
890204,
893248,
896387)
 group by 
 b.CNTYNAME,
b.POPULATION,
b.TOTAL_HOUSEHOLDS,
b.FAMILY_HOUSEHOLDS,
b.NONFAMILY_HOUSEHOLDS,
b.RESIDENTIAL_VACANCY_RATE;


 
###
# create summary table of too many households

create temporary table tmp_households select a.GRID_ID, count(*) as HOUSEHOLDS, b.RESIDENTIAL_UNITS 
 from PSRC_2000_household_synthesis_output.households a inner join PSRC_2000_household_synthesis_output.gridcells b on a.grid_id = b.grid_id
 group by a.grid_id;
 
alter table tmp_households add index grid_id(grid_id);


create table too_many_households
 select sum(a.households) as HOUSEHOLDS,
 sum(a.residential_units) as RESIDENTIAL_UNITS,
 c.SFID,
 c.RESIDENTIAL_VACANCY_RATE,
 c.FAMILY_HOUSEHOLDS,
 c.NONFAMILY_HOUSEHOLDS
 from PSRC_2000_household_synthesis_output.tmp_households a 
inner join PSRC_2000_household_synthesis.gridcell_block_group_mapping b on a.grid_id = b.grid_id
inner join PSRC_2000_household_synthesis.block_group_summary c on b.sfid = c.sfid 
 where a.grid_id in (387599, 388381, 389161, 389938, 529979, 532429, 532431, 572637, 573480,
573481, 574326, 575165, 575166, 575940, 576009, 576852, 576854, 611522, 651521, 653922,
714952, 718371, 718373, 719514, 791752, 816236, 890204, 893248, 896387)
group by c.sfid, c.residential_vacancy_rate, c.family_households, c.nonfamily_households;


############################################
insert into tmp_income_proportions (income, proportions) 
values
('Less than $10,000', 0.06301096),
('$10,000 to $14,999', 0.044362602),
('$15,000 to $19,999', 0.046102388),
('$20,000 to $24,999', 0.052914278),
('$25,000 to $29,999', 0.056615901),
('30000 to 34999', 0.058686816),
('$35,000 to $39,999', 0.057367757),
('$40,000 to $44,999', 0.056214652),
('$45,000 to $49,999', 0.051175271),
('$50,000 to $59,999', 0.097773962),
('$60,000 to $74,999', 0.12384037),
('$75,000 to $99,999', 0.134171568),
('$100,000 to $124,999', 0.069149686),
('$125,000 to $149,999', 0.033153329),
('$150,000 to $199,999', 0.027027069),
('$200,000 or more', 0.02843339); 

create table tmp_annual_household_control_totals_20041203
 select 
 a.YEAR,
 b.race,
 b.persons,
 b.income,
 (a.households * b.combo) as total_number_of_households
 from tmp_hh_totals a, tmp_race_person_income_prop b;
 
 
####
# Create Nonresidential sqft per year by zone
create table tmp_indicator_names
 (indicator_name text, geography_type_id int, table_name text, column_name text, dirty text);


insert into tmp_indicator_names (indicator_name, geography_type_id, table_name, column_name, dirty)
 values ('Nonresidential sqft per year', 3,'indicators_zone', 'v99', 0);

create table tmp_indicators_zone
 (year int, geography_id int, v99 double);


create table tmp_nonres_sqft_per_zone
 select 
 b.year,
 a.zone_id, 
 sum(b.commercial_sqft + b.industrial_sqft + b.governmental_sqft) as indicator_value
 from GSPSRC_2000_baseyear_flattened.gridcells a inner join PSRC_2000_base_run_output_petecaba.gridcells_exported b
on a.grid_id = b.grid_id group by b.year, a.zone_id;
 

insert into tmp_indicators_zone (year, geography_id, v99)
 select year, zone_id, indicator_value from tmp_nonres_sqft_per_zone;
 
#### 
# Create Residential Units
insert into tmp_indicator_names (indicator_name, geography_type_id, table_name, column_name, dirty)
 values ('Residential units', 3, 'indicator_zone', 'v98', 0);

alter table tmp_indicators_zone add column v98 double;
alter table tmp_indicators_zone add index geography_id_index(geography_id);
alter table tmp_indicators_zone add index year_index(year);

create table tmp_residential_units_per_zone
 select 
 b.year,
 a.zone_id,
 sum(b.residential_units) as indicator_value
 from GSPSRC_2000_baseyear_flattened.gridcells a inner join PSRC_2000_base_run_output_petecaba.gridcells_exported b 
on a.grid_id = b.grid_id group by b.year, a.zone_id;

alter table tmp_residential_units_per_zone add index zone_id_index(zone_id);
alter table tmp_residential_units_per_zone add index year_index(year);

update tmp_indicators_zone a inner join tmp_residential_units_per_zone b on a.year = b.year and a.geography_id = b.zone_id
 set a.v98 = b.indicator_value;


####
# Enlisted Military

# McChord TEST
create table Mcchord (NAME CHAR(50), TAZ INT, GRID_CODE INT, GRID_AREA FLOAT, AREA FLOAT, JOBS INT, 
 PERCENT_AREA DOUBLE, PROPORTION_JOBS DOUBLE, JOBS_ROUNDED INT);

insert into Mcchord (name, taz, grid_code, grid_area, area, jobs)
 select * from selected_military_zone_grid where name = 'McChord Air Force Base' and TAZ in (847);

alter table Mcchord add index taz_index(taz);

create temporary table tmp_mcchord_taz_area select taz, sum(area) as area from Mcchord group by taz;
alter table tmp_mcchord_taz_area add index taz_index(taz);

update Mcchord a inner join tmp_mcchord_taz_area b on a.taz = b.taz 
 set a.percent_area = a.area / b.area;
 
update Mcchord set proportion_jobs = percent_area * jobs;

update Mcchord set jobs_rounded = round(proportion_jobs);

create table Mcchord_in_grid select GRID_CODE as GRID_ID, 0 as SIC, JOBS_ROUNDED as JOBS, 0 as EMPLOYER_ID 
 from Mcchord;
 
# Run perl script

create table Mcchord_enlisted_2 (JOB_ID int null auto_increment, primary key (job_id), GRID_ID int, SECTOR int, HOME_BASED tinyint, SIC int);

insert into Mcchord_enlisted_2 (grid_id, sector, home_based, sic) select grid_id, 15, 0, 0, from Mcchord_out_grid;

########


#######

# FINAL process used for enlisted military outside of Fort Lewis. 

create table enlisted (NAME CHAR(50), TAZ INT, GRID_CODE INT, GRID_AREA FLOAT, AREA FLOAT, JOBS INT, 
 PERCENT_AREA DOUBLE, PROPORTION_JOBS DOUBLE, JOBS_ROUNDED INT);
 
insert into enlisted (name, taz, grid_code, grid_area, area, jobs)
 select * from selected_military_zone_grid where 
 (name = 'Naval Submarine Base (Bangor)' and TAZ = 899) or
 (name = 'Puget Sound Naval Shipyard' and taz = 894) or
 (name = 'Naval Station Puget Sound' and taz = 531) or
 (name = 'Naval Undersea Warefare Engineering Station' and taz = 910) or 
 (name = 'McChord Air Force Base' and taz = 847)
; 
 
alter table enlisted add index taz_index(taz);

create temporary table tmp_taz_area select taz, sum(area) as area from enlisted group by taz;
alter table tmp_taz_area add index taz_index(taz);

update enlisted a inner join tmp_taz_area b on a.taz = b.taz
 set a.percent_area = a.area / b.area;
 
update enlisted set proportion_jobs = percent_area * jobs;

update enlisted set jobs_rounded = round(proportion_jobs);

create table enlisted_in_grid select GRID_CODE as GRID_ID, 0 as SIC, JOBS_ROUNDED as JOBS, 0 as EMPLOYER_ID 
 from enlisted;
 
# Run perl script

create table enlisted_2_grid (JOB_ID int null auto_increment, primary key (job_id), GRID_ID int, SECTOR int, HOME_BASED tinyint, SIC int);

insert into enlisted_2_grid (grid_id, sector, home_based, sic) select grid_id, 15, 0, 0 from enlisted_out_grid;

###########################

## Scenario D double growth rate 

create table prep_employment_totals_2x (YEAR INT, TOTALS int);

insert into prep_employment_totals_2x values
(2000, 1773754),
(2001, 1746332),
(2002, 1675394.949),
(2003, 1720185.609),
(2004, 1805632.519),
(2005, 1901803.56),
(2006, 2012394.657),
(2007, 2093471.86),
(2008, 2168468.205),
(2009, 2227503.306),
(2010, 2283100.617),
(2011, 2333669.119),
(2012, 2385395.966),
(2013, 2442171.075),
(2014, 2498620.916),
(2015, 2556357.625),
(2016, 2630599.212),
(2017, 2700664.284),
(2018, 2778809.571),
(2019, 2861767.496),
(2020, 2937414.196),
(2021, 2992627.253),
(2022, 3059056.791),
(2023, 3118064.599),
(2024, 3190526.628),
(2025, 3245366.333),
(2026, 3315020.663),
(2027, 3390542.175),
(2028, 3467614.456),
(2029, 3547055.447),
(2030, 3629191.979);


create table annual_employment_control_totals_20041229
 select a.YEAR,
 b.SECTOR_ID,
 (a.TOTALS * b.proportions) as new_prop
 from prep_employment_totals_2x a, prelim_proportions b
 where a.year = b.year;

create table annual_employment_control_totals_20041229_new
 (YEAR INT, SECTOR_ID INT, TOTAL_HOME_BASED_EMPLOYMENT INT, TOTAL_NON_HOME_BASED_EMPLOYMENT INT)
 
INSERT INTO annual_employment_control_totals
 select a.YEAR,
 a.SECTOR_ID,
 (a.new_prop * b.home_ratio) as TOTAL_HOME_BASED_EMPLOYMENT,
 (a.new_prop * b.non_home_ratio) as TOTAL_NON_HOME_BASED_EMPLOYMENT
 from annual_employment_control_totals_20041229 a, prelim_home_and_non_based_ratio b
 where a.year = b.year and a.sector_id = b.sector_id;
 
 drop table annual_employment_control_totals_20041229;
 drop table prep_employment_totals_2x;
 
 
 ########################
 
 # Check Negative Res Vacancy Rates for Baseline Scenario
 
 ## ZONE LEVEL
 create temporary table tmp_units_2030 select zone_id, sum(residential_units) as units 
from gridcells_exported_denormalized where year = 2030 group by zone_id;

 create temporary table tmp_hh_2030 select zone_id, count(*) as households 
from households_exported_denormalized where year = 2030 group by zone_id;
 
 alter table tmp_units_2030 add index zone_id(zone_id);
 alter table tmp_hh_2030 add index zone_id(zone_id);
 
 create temporary table tmp_comp_2030 select a.*, b.households 
from tmp_units_2030 a inner join tmp_hh_2030 b on a.zone_id = b.zone_id
where a.units < b.households;

 ## GRID LEVEL
 create temporary table tmp_units_2030_grid select grid_id, residential_units as units
from gridcells_exported_denormalized where year = 2030;

 create temporary table tmp_hh_2030_grid select grid_id, count(*) as households 
from households_exported_denormalized where year = 2030 group by grid_id;

 alter table tmp_units_2030_grid add index grid_id(grid_id);
 alter table tmp_hh_2030_grid add index grid_id(grid_id);
 
 create temporary table tmp_comp_2030_grid select a.*, b.households 
from tmp_units_2030_grid a inner join tmp_hh_2030_grid b on a.grid_id = b.grid_id;
 

## Households and Units across all years at the zone level
create temporary table tmp_total_units select year, zone_id, sum(residential_units) as units 
 from gridcells_exported_denormalized group by year, zone_id;
 
create temporary table tmp_total_households select year, zone_id, count(*) as households
 from households_exported_denormalized group by year, zone_id;
 
alter table tmp_total_units add index zone_id(zone_id);
alter table tmp_total_households add index zone_id(zone_id);

create temporary table tmp_total_units_hh 
 select a.*, b.households
 from tmp_total_units a inner join tmp_total_households b on a.zone_id = b.zone_id
 and a.year = b.year;
 
## Check Residential Vacancy Rate

create temporary table tmp_units_2030b select 
 a.zone_id, sum(b.residential_units) as units from GSPSRC_2000_baseyear_flattened.gridcells a
 inner join gridcells_exported b on a.grid_id = b.grid_id 
 where b.year = 2030 group by a.zone_id;
 
create temporary table tmp_hh_2030b select
 grid_id, zone_id, count(*) as households from households_exported
 where year = 2030 group by grid_id, zone_id;
 
alter table tmp_hh_2030b add index grid_zone_id(grid_id, zone_id); 
 
create temporary table tmp_hh_2030e
 select a.grid_id, a.zone_id as old_zone, a.households, b.zone_id as new_zone 
 from tmp_hh_2030b a inner join GSPSRC_2000_baseyear_flattened.gridcells b
 on a.grid_id = b.grid_id;
 
create temporary table tmp_hh_2030e2 
 select new_zone as zone_id, sum(households) as households from 
 tmp_hh_2030e group by new_zone;
 
create temporary table tmp_compare_2030 
 select a.*, b.households from tmp_units_2030b a 
 inner join tmp_hh_2030e2 b on a.zone_id = b.zone_id
 where a.units < b.households;


## New process for calculating household characteristics
create temporary table tmp_hh_characteristics_2030 
 select a.HOUSEHOLD_ID, 
 a.GRID_ID,
b.PERSONS,
b.WORKERS,
b.AGE_OF_HEAD,
b.INCOME,
b.CHILDREN,
b.RACE_ID,
b.CARS,
c.ZONE_ID
 from households_exported a inner join households_constants b 
on a.household_id = b.household_id 
 inner join GSPSRC_2000_baseyear_change_20041206.gridcells c
on a.grid_id = c.grid_id
 where a.year = 2030 
;
 
create temporary table tmp_household_character_2030
 select zone_id, count(*) as households, sum(persons) as persons, sum(income) as income
 from tmp_hh_characteristics_2030 group by zone_id;

alter table tmp_household_character_2030 add index zone_id(zone_id);

update TAZ_INDICATORS a 
 inner join tmp_household_character_2030 b 
 on a.zone_id = b.zone_id 
 set a.hh_2030 = b.households;

update TAZ_INDICATORS a 
 inner join tmp_household_character_2030 b 
 on a.zone_id = b.zone_id 
 set a.avg_hh_sz_2030 = b.persons / a.hh_2030;
 
update TAZ_INDICATORS a 
 inner join tmp_household_character_2030 b 
 on a.zone_id = b.zone_id 
 set a.avg_hh_inc_2030 = b.income / a.hh_2030; 
 
## New process for calculating jobs characteristics
create temporary table tmp_jobs_2030
 select a.JOB_ID,
 a.GRID_ID,
 a.HOME_BASED,
 c.ZONE_ID
 from jobs_exported a inner join jobs_constants b 
on a.job_id = b.job_id
 inner join GSPSRC_2000_baseyear_start.gridcells c 
on a.grid_id = c.grid_Id
 where a.year = 2030
; 

create temporary table tmp_job_character_2030 
 select zone_id, count(*) as jobs 
 from tmp_jobs_2030 group by zone_id;
 
alter table tmp_job_character_2030 add index zone_id(zone_id);

update TAZ_INDICATORS a inner join tmp_job_character_2030 b 
 on a.zone_id = b.zone_id 
 set a.jobs_2030 = b.jobs;
 
#########################################################################
# Need parcels table at all county level and imputed year built parcels #
#########################################################################
# 
# Year Built Imputed to re-estimation databases
# To be done in PSRC_parcels_impute_year_built_pierce
#

create table sc_parcels_all_counties select * from sc_parcels_king;
insert into sc_parcels_all_counties select * from sc_parcels_kitsap;
insert into sc_parcels_all_counties select * from sc_parcels_pierce;
insert into sc_parcels_all_counties select * from sc_parcels_snohomish; 

alter table sc_parcels_all_counties add index prcl_cnty_index(parcel_id(10), county(3));

# To be done in peter database or database containing all county building recods 
/*alter table buildings add column IMPUTED_YEAR_BUILT_FLAG int;

update buildings a inner join PSRC_parcels_impute_year_built_pierce.sc_parcels_all_counties b 
 on a.parcel_id = b.parcel_id and a.county = b.county
 set a.year_built = b.year_built, a.imputed_year_built_flag = b.year_built_impute_flag
 where a.year_built is null or a.year_built = 0;
*/ As of Jan. 27, not sure if this section of the script works 
# To be done at the individual county level
## Kitsap County ##

use PSRC_parcels_kitsap

alter table buildings add column IMPUTED_YEAR_BUILT_FLAG int;
alter table buildings add column IMPUTED_YEAR_BUILT int;

update buildings a inner join PSRC_parcels_impute_year_built_pierce.sc_parcels_kitsap b 
 on a.parcel_id = b.parcel_id
 set a.imputed_year_built = b.year_built
 where a.year_built = 0;
 
update buildings set imputed_year_built_flag = 1 where imputed_year_built <> 0 or imputed_year_built is not null;
update buildings set year_built = imputed_year_built where imputed_year_built_flag = 1;

## King County ##
use PSRC_parcels_king

alter table buildings add column IMPUTED_YEAR_BUILT_FLAG int;
alter table buildings add column IMPUTED_YEAR_BUILT int;

update buildings a inner join PSRC_parcels_impute_year_built_pierce.sc_parcels_king b 
 on a.parcel_id = b.parcel_id
 set a.imputed_year_built = b.year_built
 where a.year_built = 0;
 
update buildings set imputed_year_built_flag = 1 where imputed_year_built <> 0 or imputed_year_built is not null;
update buildings set year_built = imputed_year_built where imputed_year_built_flag = 1;

## Pierce County ##
use PSRC_parcels_pierce

alter table buildings add column IMPUTED_YEAR_BUILT_FLAG int;
alter table buildings add column IMPUTED_YEAR_BUILT int;

update buildings a inner join PSRC_parcels_impute_year_built_pierce.sc_parcels_pierce b 
 on a.parcel_id = b.parcel_id
 set a.imputed_year_built = b.year_built
 where a.year_built = 0;
 
update buildings set imputed_year_built_flag = 1 where imputed_year_built <> 0 or imputed_year_built is not null;
update buildings set year_built = imputed_year_built where imputed_year_built_flag = 1;

## Snohomish County ##
use PSRC_parcels_snohomish

alter table buildings add column IMPUTED_YEAR_BUILT_FLAG int;
alter table buildings add column IMPUTED_YEAR_BUILT int;

update buildings a inner join PSRC_parcels_impute_year_built_pierce.sc_parcels_snohomish b 
 on a.parcel_id = b.parcel_id
 set a.imputed_year_built = b.year_built
 where a.year_built = 0;
 
update buildings set imputed_year_built_flag = 1 where imputed_year_built <> 0 or imputed_year_built is not null;
update buildings set year_built = imputed_year_built where imputed_year_built_flag = 1;

####
#
# Create new jobs table containing all of the updates (+12,0000 jobs, enlisted military, reclassified pierce jobs) 
#
#
#
#

use PSRC_2000_baseyear_updates_for_reestimation;

create table jobs_20050128 
 (JOB_ID int auto_increment primary key,
GRID_ID INT,
SECTOR_ID INT,
HOME_BASED TINYINT,
SIC INT);

insert into jobs_20050128 (GRID_ID, SECTOR_ID, HOME_BASED, SIC) 
 select GRID_ID, SECTOR_ID, HOME_BASED, SIC 
 from GSPSRC_2000_baseyear_flattened.jobs_tobeused_jan05;
 
insert into jobs_20050128 (GRID_ID, SECTOR_ID, HOME_BASED, SIC) 
 select GRID_ID, SECTOR_ID, HOME_BASED, SIC 
 from PSRC_2000_baseyear_updates_for_reestimation.jobs_pie_military_reclassified;

insert into jobs_20050128 (GRID_ID, SECTOR_ID, HOME_BASED, SIC) 
 select GRID_ID, SECTOR_ID, HOME_BASED, SIC
 from PSRC_2000_baseyear_updates_for_reestimation.jobs_enlisted_military;
 
############
## First draft of PLU file received Feb. 2, 2005

#Regflu with new PLU class
 
create table gridcells_urbsimplu1 
 select GRID_CODE as GRID_ID, 
 sum(area) as AREA, 
 URBSIMPLU, 
 GRID_AREA from plu_grid_05_polygon
 group by grid_code, urbsimplu;
 
delete from gridcells_urbsimplu1 where urbsimplu = ''; 
alter table gridcells_urbsimplu1 add index grid_area_index(grid_id, area);

create table gridcells_urbsimplu 
 select GRID_ID, 
max(area) as area 
 from gridcells_urbsimplu1
 group by grid_id;

alter table gridcells_urbsimplu add column URBSIMPLU varchar(50);
alter table gridcells_urbsimplu add index grid_area_index(grid_id, area);
alter table gridcells_urbsimplu add index urbsimplu_index(urbsimplu(50));
alter table gridcells_urbsimplu add column plan_type_id int;

update gridcells_urbsimplu a inner join gridcells_urbsimplu1 b on a.grid_id = b.grid_id and a.area = b.area
 set a.urbsimplu = b.urbsimplu;

# Create plan types tables
create table plan_types (PLAN_TYPE_ID INT AUTO_INCREMENT PRIMARY KEY, NAME VARCHAR(50));
insert into plan_types (name) select distinct urbsimplu from gridcells_urbsimplu order by urbsimplu asc;

alter table plan_types add index name_index(name(50));

update gridcells_urbsimplu a inner join plan_types b on a.urbsimplu = b.name 
 set a.plan_type_id = b.plan_type_id;

# Revise plan_types table to coincide with correct design scheme. 
update plan_types set name = 'agriculture' where name = 'AGR';
update plan_types set name = 'commercial' where name = 'COM';
update plan_types set name = 'commercial_low' where name = 'COM-Low';
update plan_types set name = 'forests' where name = 'FOR';
update plan_types set name = 'government' where name = 'GOV';
update plan_types set name = 'industrial' where name = 'IND';
update plan_types set name = 'industrial_mix' where name = 'IND-Mix';
update plan_types set name = 'mixed_use_including_residential_high' where name = 'MIX-High';
update plan_types set name = 'mixed_use_including_residential_low' where name = 'MIX-Low';
update plan_types set name = 'parks_and_open_space' where name = 'POS';
update plan_types set name = 'residential_high' where name = 'RES-High';
update plan_types set name = 'residential_light' where name = 'RES-Light';
update plan_types set name = 'residential_low' where name = 'RES-Low';
update plan_types set name = 'residential_medium' where name = 'RES-Med';
update plan_types set name = 'residential_rural' where name = 'RES-Rural';
update plan_types set name = 'right_of_way' where name = 'ROW';
update plan_types set name = 'resource_extraction' where name = 'RSC';
update plan_types set name = 'tribal_government_military' where name = 'TRIB';
update plan_types set name = 'water' where name = 'WTR';


## 
## Refinements to plu code cells
##

# Insert missing records that did not have plu codes and assign those plu codes to whatever plu type is had in the old Gold Standard database
create table gridcells_with_no_plu 
 select a.GRID_ID, 
 a.PLAN_TYPE_ID 
 from GSPSRC_2000_baseyear_flattened.gridcells a left join gridcells_urbsimplu b
 on a.grid_id = b.grid_id where b.grid_id is null;

alter table gridcells_with_no_plu add column NEW_PLU varchar(50);
update gridcells_with_no_plu set new_plu = 'WTR' where plan_type_id = 11;
update gridcells_with_no_plu set new_plu = 'AGR' where plan_type_id = 1;
update gridcells_with_no_plu set new_plu = 'RES-Low' where plan_type_id = 7;

create table gridcells_new_plu (GRID_ID int, URBSIMPLU varchar(50), PLAN_TYPE_ID int); 

insert into gridcells_new_plu (grid_id, urbsimplu, plan_type_id) select grid_id, urbsimplu, plan_type_id from gridcells_urbsimplu;
insert into gridcells_new_plu (grid_id, urbsimplu, plan_type_id) select grid_id, new_plu as urbsimplu, plan_type_id as plan_type_id 
 from gridcells_with_no_plu;

alter table gridcells_new_plu add index grid_id(grid_id);

# Update plu codes from COM-Centers to COM (there should be no COM-Centers plu codes
update gridcells_new_plu set urbsimplu = 'COM' where urbsimplu = 'COM-Centers';

# Change cells whose location is in the Puget Sound and classified as RES, but should be water. 
create table water_cells 
 select a.GRID_ID, 
 a.urbsimplu, 
 b.plan_type_id from gridcells_urbsimplu a 
 inner join GSPSRC_2000_baseyear_flattened.gridcells bon a.grid_Id = b.grid_id where b.plan_type_id = 11

create table gridcells_water_plu 
 select a.GRID_ID, 
 a.URBSIMPLU, 
 a.PLAN_TYPE_ID, 
 b.PLAN_TYPE_ID as OLD_WATER_PLU 
 from gridcells_urbsimplu a 
 inner join water_cells b on a.grid_id = b.grid_id

update gridcells_water_plu set urbsimplu = 'WTR' where old_water_plu = 11;
update gridcells_water_plu set urbsimplu = 'IND' where old_water_plu = 4;

alter table gridcells_water_plu add index grid_id(grid_id);

update gridcells_new_plu a inner join gridcells_water_plu b on a.grid_id = b.grid_id set a.urbsimplu = b.urbsimplu;

# Set SBW (should be under water) PLU codes to WTR (water)
update gridcells_new_plu set urbsimplu = 'WTR' where urbsimplu = 'SBW';

# create final plan_types table
insert into plan_types (name) select distinct urbsimplu from gridcells_new_plu order by urbsimplu asc;

alter table plan_types add index name_index(name(50));

update gridcells_new_plu a inner join plan_types b on a.urbsimplu = b.name 
 set a.plan_type_id = b.plan_type_id;



## 
## New revisions to the PLU file based on the latest version received from the PSRC Feb. 4 2005
##-- Will undergo procdure from above once new file is create --

## Export tables Corres_1_Desc_to_USim_PLU and Corres_2_ID_to_DESC_and_PLU from Mark Simonson's email to PSRC_2000_baseyear_updates_for_reestimation
alter table Corres_1_Desc_to_USim_PLU add index id_index(id(50));
alter table Corres_2_ID_to_DESC_and_PLU add index flu_id_index(flucicn_id);

create table plu_grid_feb0405 
 select 
 GRID_CODE as GRID_ID,
 AREA,
 GRID_AREA,
 FLUCICN_ as FLU_ID,
 FLUCICN_ID,
 GENUSE,
 DESC_ as ID,
 URBSIMPLU
 from plu_grid_05_polygon
;

alter table plu_grid_feb0405 add index id_index(id(50));
alter table plu_grid_feb0405 add index flucicn_id_index(flu_id);

update plu_grid_feb0405 a inner join Corres_1_Desc_to_USim_PLU b on a.id = b.id
 set a.urbsimplu = b.urbsimplu;
 
update plu_grid_feb0405 a inner join Corres_2_ID_to_DESC_and_PLU b on a.flucicn_id = b.flucicn_id 
 set a.id = b.id;

update plu_grid_feb0405 a inner join Corres_2_ID_to_DESC_and_PLU b on a.flucicn_id = b.flucicn_id 
 set a.urbsimplu = b.urbsimplu;


## Once this portion is complete go back up to First draft of PLU file received Feb. 2, 2005 to re-assess the other gridcells. 


# drop tables
drop table gridcells_with_no_plu;
drop table gridcells_water_plu;
drop table water_cells;



######
# Imputed sqft revisions (use PSRC breakout of sqft/employee ratios)

# Need to group parcel records containing (9 employment sectors)
/*
Distinct PSRC sectors are:
Const/Res
FIRES
GovED
Manu/WTCU
Manufacturing
Retail/FIRES
Retail/FIRES/GovED
Retail
WTCU

Distinct sectors are:
Services
Manufacturing 
Retail Trade
Construction
Wholesale Trade 
FIRES 
Transportation, Communications, Electric, Gas, San
Agriculture 
STATE AND LOCAL 
EDUCATION K-12
Public Administration 
FEDERAL, CIVILIAN 
FEDERAL, MILITARY 
EDUCATION HIGHER
Mining
*/

# create reclass table

create table step_sector_reclass (SECTOR varchar(100), STEP varchar(100), COMBO varchar(50));
insert into step_sector_reclass (sector, step, combo)
 values ('Agriculture', 'RES', 'CONST/RES'),
 ('Construction', 'RES', 'CONST/RES'),
 ('EDUCATION HIGHER', 'GOVED', 'GOVED'),
 ('EDUCATION K-12', 'GOVED', 'GOVED'),
 ('FEDERAL, CIVILIAN', 'GOVED', 'GOVED'),
 ('FEDERAL, MILITARY', 'GOVED', 'GOVED'),
 ('FIRES', 'FIRES', 'FIRES'),
 ('Manufacturing', 'MANUF', 'MANUF'),
 ('Mining', 'RES', 'RES'),
 ('Public Administration', 'GOVED', 'GOVED'),
 ('Retail Trade', 'RETAIL', 'RETAIL'),
 ('Services', 'FIRES', 'FIRES'),
 ('STATE AND LOCAL', 'GOVED', 'GOVED'),
 ('Transportation, Communications, Electric, Gas, San', 'WTCU', 'WTCU'),
 ('Wholesale Trade', 'WTCU', 'WTCU');

alter table step_sector_reclass add index sector_index(sector(10));
alter table prelim_employers_to_parcels add column STEP varchar (100);
alter table prelim_employers_to_parcels add index sector_index(sector(10));
alter table prelim_employers_to_parcels add column sqft_per_job double;

update prelim_employers_to_parcels set sqft_per_job = sqft / jobs;

update prelim_employers_to_parcels a 
 inner join step_sector_reclass b on a.sector = b.sector
 set a.STEP = b.STEP;

create table step_sector (STEP varchar(100), COUNTY varchar(3), SQFT int);
insert into step_sector values
("const,fires,goved,manuf,retail,wtcu","035",376.4815618),
("res", "035", 778.3010471),
("fires", "035", 649.8268835),
("goved", "035", 600.721874),
("manuf,wtcu", "035", 530),
("manuf","035",796.957265),
("fires,retail","035",503.2097058),
("fires,goved,retail","035",307),
("retail","035",703.9661267),
("wtcu","035",1277.286872),
("catch_all", "035", 376)
;

create table grouped_step_sector
 select parcel_id, 
 sum(jobs) as jobs,
 sqft as parcel_sqft,
 use_code,
 generic_land_use_1,
 generic_land_use_2,
 taxexempt_binary,
 year_built,
 sqft_per_job,
 group_concat(distinct step order by step separator ',') as step
 from prelim_employers_to_parcels
 group by parcel_id;

create table grouped_parcel_with_step_sqft
 select g.*,
 s.sqft as step_sqft
 from grouped_step_sector g 
 inner join step_sector s on lower(g.step) = s.step;

create temporary table missing_records 
 select g.*,
 s.sqft as step_sqft
 from grouped_step_sector g
 left outer join step_sector s on lower(g.step) = s.step
 where s.step is null;
 
 update missing_records set step = "catch_all";
 update missing_records set step_sqft = 334;
 
 insert into grouped_parcel_with_step_sqft select * from missing_records;
 
 update grouped_parcel_with_step_sqft set sqft_per_job = parcel_sqft / jobs;
 
 alter table grouped_parcel_with_step_sqft add index prcl_index(parcel_id(10));
 
 ##
 ## Percentile table 
 ##
 
 ## Prelim value 
 
 create temporary table prelim_sqft_values (
generic_land_use_1 varchar(100),
sqft_per_job double,
step varchar(100)
 );
 
 insert into prelim_sqft_values (
 generic_land_use_1,
 sqft_per_job,
step)
select 
generic_land_use_1,
sqft_per_job, 
step 
from grouped_parcel_with_step_sqft
 ;
 
 ## Get ordered list of values
 
 create temporary table ordered_values (
rec_number int auto_increment primary key,
descriptive_field varchar(8),
group_field_1 varchar(16),
group_field_2 varchar(16),
value double
 );
 
 insert into ordered_values (
 group_field_1, 
 group_field_2,
value)
select 
generic_land_use_1,
step,
 sqft_per_job
from prelim_sqft_values
order by 
generic_land_use_1,
step,
 sqft_per_job
 ;

## Construct table of percentiles

create temporary table percentiles (percentile double);

insert into percentiles (percentile)
values
(0.0),
(.01),
(.05),
(.1),
 (.25),
(.5),
(.75),
(.9),
 (.95),
(.99),
(1)
;

## Get list of max, min row values for step in ordered_values

create temporary table group_row_limits
select 
group_field_1,
group_field_2,
count(*) as num_records,
min(rec_number) as min_rec_number,
max(rec_number) as max_rec_number
from ordered_values
group by 
group_field_1,
group_field_2
;

## Construct table group_percentile_rows listing row number 
##for summary percentile combination

create temporary table group_percentile_rows (
group_field_1 varchar(16),
group_field_2 varchar(16),
num_records int,
percentile double,
percentile_row_number int
);

insert into group_percentile_rows (
 group_field_1,
 group_field_2,
 percentile )
select 
 grl.group_field_1,
 grl.group_field_2,
 prctl.percentile
from
 group_row_limits grl
 inner join percentiles prctl
;

update group_percentile_rows gpr, group_row_limits grl
set percentile_row_number =
(ceiling((grl.max_rec_number - grl.min_rec_number) * gpr.percentile)) + grl.min_rec_number,
gpr.num_records = grl.num_records
where 
gpr.group_field_1 = grl.group_field_1 and gpr.group_field_2 = grl.group_field_2
;

## Get values of interest from the ordered list of values for the row number
## for each combo

CREATE TEMPORARY TABLE result_percentile_by_rows
SELECT
gpr.group_field_1 as land_use,
gpr.group_field_2 as step,
(gpr.percentile * 100) as percentile,
round(opv.value,2) as sqft_per_job,
gpr.num_records as total_number_of_employers
FROM group_percentile_rows gpr INNER JOIN ordered_values opv
ON gpr.percentile_row_number = opv.rec_number
ORDER BY 
gpr.group_field_1,
gpr.group_field_2,
gpr.percentile
;


## Create final percentile table

CREATE TABLE sqft_per_job_percentiles_by_sector
SELECT 
 step, 
 land_use,
 total_number_of_employers, 
 sum(IF(percentile=0, sqft_per_job, 0)) as "0_percentile",
 sum(IF(percentile=1, sqft_per_job, 0)) as "1_percentile",
 sum(IF(percentile=5, sqft_per_job, 0)) as "5_percentile",
 sum(IF(percentile=10, sqft_per_job, 0)) as "10_percentile",
 sum(IF(percentile=25, sqft_per_job, 0)) as "25_percentile",
 sum(IF(percentile=50, sqft_per_job, 0)) as "50_percentile",
 sum(IF(percentile=75, sqft_per_job, 0)) as "75_percentile",
 sum(IF(percentile=90, sqft_per_job, 0)) as "90_percentile",
 sum(IF(percentile=95, sqft_per_job, 0)) as "95_percentile",
 sum(IF(percentile=99, sqft_per_job, 0)) as "99_percentile",
 sum(IF(percentile=100, sqft_per_job, 0)) as "100_percentile"
FROM 
 result_percentile_by_rows
GROUP BY 
step,
land_use
;

## Select records from percentile table that fall below the 10th percentile or 0 Sqft values

create temporary table pre_10th_percentile
 select a.*, 1 as imputed_flag from grouped_parcel_with_step_sqft a 
 inner join sqft_per_job_percentiles_by_sector b 
 on a.step = b.step and a.generic_land_use_1 = b.land_use
 where (a.sqft_per_job <= b.10_percentile) or (a.sqft_per_job = 0);
 
alter table pre_10th_percentile add index prcl_index(parcel_id(10));
 
## Select records from percentile table that are above the 99th percentile

create temporary table pre_99th_percentile
 select a.*, 1 as imputed_flag from grouped_parcel_with_step_sqft a 
 inner join sqft_per_job_percentiles_by_sector b 
 on a.step = b.step and a.generic_land_use_1 = b.land_use
 where a.sqft_per_job >= b.99_percentile and a.parcel_sqft <> 0;

alter table pre_99th_percentile add index prcl_index(parcel_id(10));

## update tails of distribution tables with new imputed sqft values

# 10th percentile

alter table pre_10th_percentile add column imputed_sqft double;
update pre_10th_percentile set imputed_sqft = step_sqft * jobs;

# 99th percentile
alter table pre_99th_percentile add column imputed_sqft double;
update pre_99th_percentile set imputed_sqft = (abs((step_sqft * jobs)-parcel_sqft));

## update original parcel records with new imputed sqft values

alter table grouped_parcel_with_step_sqft add column imputed_sqft double;
alter table grouped_parcel_with_step_sqft add column imputed_sqft_flag tinyint;

update grouped_parcel_with_step_sqft a 
 inner join pre_10th_percentile b on a.parcel_id = b.parcel_id 
 set a.imputed_sqft = b.imputed_sqft;

update grouped_parcel_with_step_sqft a
 inner join pre_99th_percentile b on a.parcel_id = b.parcel_id 
 set a.imputed_sqft = b.imputed_sqft;

update grouped_parcel_with_step_sqft set imputed_sqft_flag = 1
 where imputed_sqft is not null;
 
update grouped_parcel_with_step_sqft set imputed_sqft = parcel_sqft 
 where imputed_sqft_flag is null;


##
## compare newly imputed values agains old imputed values
##

# Old Kitsap
create temporary table kit_bld_sqft
 select parcel_id,
 sum(imputed_sqft) as sqft
 from PSRC_parcels_kitsap.buildings
 group by parcel_id;

alter table kit_bld_sqft add index prcl_index(parcel_id(11));

create table kit_impute_old 
 select sum(b.sqft) as sqft
 from PSRC_parcels_kitsap.parcels a 
 inner join kit_bld_sqft b on a.parcel_id = b.parcel_id;
 
# New Kitsap 

create temporary table prelim_kit_prcl select * from PSRC_parcels_kitsap.parcels;

alter table prelim_kit_prcl add index prcl_index(parcel_id(11));

update prelim_kit_prcl set built_sqft = 0;

update prelim_kit_prcl a inner join kit_bld_sqft b on a.parcel_id = b.parcel_id 
 set a.built_sqft = b.sqft;

update prelim_kit_prcl a inner join grouped_parcel_with_step_sqft_kitsap b on a.parcel_id = b.parcel_id
 set a.built_sqft = b.imputed_sqft;
 
 

##
## Collate buildings table
##

create table buildings (
building_use varchar(50), 
description text, 
parcel_id varchar(15), 
year_built double, 
county char(3), 
built_sqft double, 
impute_flag tinyint,
imputed_sqft double
);

insert into buildings
 select
 building_use, 
 description,
 parcel_id,
 year_built,
 county,
 built_sqft,
 imputed_sqft_flag,
 imputed_sqft
 from king_impute_sqft.buildings;
 
insert into buildings
 select
 building_use, 
 building_use,
 parcel_id,
 year_built,
 county,
 built_sqft,
 imputed_sqft_flag,
 imputed_sqft
 from kitsap_impute_sqft.buildings;
 
insert into buildings
 select
 building_use, 
 description,
 parcel_id,
 year_built,
 county,
 built_sqft,
 imputed_sqft_flag,
 imputed_sqft
 from pierce_impute_sqft.buildings;
 
insert into buildings
 select
 building_use, 
 building_use,
 parcel_id,
 year_built,
 county,
 built_sqft,
 imputed_sqft_flag,
 imputed_sqft
 from snohomish_impute_sqft.buildings;

 
##
## Updates to baseyear re-estimation database
##

update gridcells a inner join PSRC_2000_baseyear_updates_for_reestimationgridcells b on a.grid_id = b.grid_id
 set a.plan_type_id = b.plan_type_id;
 
update gridcells a inner join PSRC_2000_baseyear_updates_for_reestimationgridcells b on a.grid_id = b.grid_id
 set a.percent_stream_buffer = b.percent_stream_buffer;
 
update gridcells a inner join PSRC_2000_baseyear_updates_for_reestimationgridcells b on a.grid_id = b.grid_id
 set a.percent_stream_buffer = b.percent_stream_buffer; 
 

create table gridcells_tobeused_for_reestimation
 select 
 b.GRID_ID, 
a.COMMERCIAL_SQFT, 
a.GOVERNMENTAL_SQFT, 
a.INDUSTRIAL_SQFT, 
a.COMMERCIAL_IMPROVEMENT_VALUE,
a.INDUSTRIAL_IMPROVEMENT_VALUE,
a.GOVERNMENTAL_IMPROVEMENT_VALUE,
a.NONRESIDENTIAL_LAND_VALUE, 
a.RESIDENTIAL_LAND_VALUE,
a.RESIDENTIAL_IMPROVEMENT_VALUE, 
b.RESIDENTIAL_UNITS, 
a.YEAR_BUILT,
a.FRACTION_RESIDENTIAL_LAND, 
a.PERCENT_UNDEVELOPABLE, 
a.TOTAL_NONRES_SQFT, 
a.TOTAL_UNDEVELOPABLE_SQFT,
 b.DEVELOPMENT_TYPE_ID, 
b.DISTANCE_TO_ARTERIAL,
b.DISTANCE_TO_HIGHWAY, 
b.RELATIVE_X,
b.RELATIVE_Y,
b.PLAN_TYPE_ID,
b.PERCENT_WATER, 
b.PERCENT_WETLAND, 
b.PERCENT_STREAM_BUFFER, 
b.PERCENT_FLOODPLAIN,
b.PERCENT_SLOPE, 
b.PERCENT_OPEN_SPACE,
b.PERCENT_PUBLIC_SPACE,
b.PERCENT_ROADS, 
b.IS_OUTSIDE_URBAN_GROWTH_BOUNDARY,
b.IS_INSIDE_NATIONAL_FOREST, 
b.IS_INSIDE_TRIBAL_LAND, 
b.IS_INSIDE_MILITARY_BASE, 
b.ZONE_ID, 
b.CITY_ID, 
b.COUNTY_ID, 
b.PERCENT_AGR_KING, 
b.ACRES, 
b.PERCENT_AGRICULTURAL_PROTECTED_LANDS,
b.PERCENT_FOREST,
b.PERCENT_MINING,
b.PERCENT_ROW
from reestimation_gridcells b left join gridcells a
 on a.grid_id = b.grid_id 
; 


alter table parcels add index cnty_lu_index(county(3), land_use);
alter table parcels add index lu_cnty_index(land_use, county(3));
alter table parcels add index pin_cnty_index(parcel_id(10), county(3));
alter table parcels add index city_lu_index(city(10), land_use);

####

# Create indicators

## Percent of units inside UGB by year

create temporary table percent_units_in_ugb (year int, units_in double, total_units double, percent double);
create temporary table tmp_in_ugb_units
 select year, sum(residential_units) as units
 from gridcells_exported_denormalized
 where IS_OUTSIDE_URBAN_GROWTH_BOUNDARY = 0
 group by year
;

create temporary table tmp_total_units
 select year, sum(residential_units) as units
 from gridcells_exported
 group by year
;

insert into percent_units_in_ugb (year, units_in) 
 select year, units 
 from tmp_in_ugb_units
 group by year
; 
 
update percent_units_in_ugb a inner join tmp_total_units b on a.year = b.year
 set a.total_units = b.units;
 
update percent_units_in_ugb set percent = units_in / total_units;

####

# Create new gridcells table
create table tmp_gridcells select * from gridcells_exported where year in (2001, 2005, 2010, 2015, 2020, 2025, 2030);
drop table gridcells_exported;
alter table tmp_gridcells rename as gridcells_exported;

# Create new households table
create table tmp_households select * from households_exported where year in (2001, 2005, 2010, 2015, 2020, 2025, 2030);
drop table households_exported;
alter table tmp_households rename as households_exported;

# Create new jobs table
create table tmp_jobs select * from jobs_exported where year in (2001, 2005, 2010, 2015, 2020, 2025, 2030);
drop table jobs_exported;
alter table tmp_jobs rename as jobs_exported;

###

# Because I'm an idiot I removed every 5 years from the baseline scenario double and transit scenarios. 

# Create new gridcells table
create table tmp_gridcells select 
 YEAR,
 GRID_ID, 
 RESIDENTIAL_IMPROVEMENT_VALUE, 
 RESIDENTIAL_LAND_VALUE,
 COMMERCIAL_SQFT,
 INDUSTRIAL_SQFT,
 GOVERNMENTAL_SQFT, 
 YEAR_BUILT,
 RESIDENTIAL_UNITS, 
 DEVELOPMENT_TYPE_ID, 
 COMMERCIAL_IMPROVEMENT_VALUE,
 INDUSTRIAL_IMPROVEMENT_VALUE,
 GOVERNMENTAL_IMPROVEMENT_VALUE,
 NONRESIDENTIAL_LAND_VALUE, 
 FRACTION_RESIDENTIAL_LAND, 
 WATER_USE 
 from gridcells_exported_denormalized
; 
drop table gridcells_exported;
alter table tmp_gridcells rename as gridcells_exported;

# Create new households table
create table tmp_households select 
 YEAR,
 HOUSEHOLD_ID,
 GRID_ID,
 ZONE_ID
 from households_exported_denormalized
;
drop table households_exported;
alter table tmp_households rename as households_exported;

# Create new jobs table
create table tmp_jobs select 
 YEAR,
 JOB_ID,
 GRID_ID,
 HOME_BASED,
 ZONE_ID
 from jobs_exported_denormalized
;
drop table jobs_exported;
alter table tmp_jobs rename as jobs_exported;

###

insert into input_configurations values 
('PSRC_2000_scenario_high_vacancy',
 'jdbc:mysql://trondheim.cs.washington.edu/PSRC_2000_baseyear',
 'jdbc:mysql://trondheim.cs.washington.edu/PSRC_2000_scenario_high_vacancy',
 'simulate_from_PSRC_2000_base_run_2_output',
 '(2005, "2000_c04"), (2010, "2010_c04")',
 'accessibility-model, household-transition-model, employment-transition-model, household-relocation-choice-model, employment-relocation-choice-model, household-location-choice-model weighted-choiceset="true", employment-non-home-based-location-choice-model weighted-choiceset="true", employment-home-based-location-choice-model weighted-choiceset="true", scaling-procedure-for-jobs-model, land-price-model, developer-model-with-vacancy-adjustment use-development-caps="false"'
 );
 
 insert into run_request_queue (priority, id, description, input_configuration_name, random_seed, end_year, export_years, status) values 
 (2.2, 14, 'High Vacancy Rate', 'PSRC_2000_scenario_high_vacancy', 0, 2010, '2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010', 'new');
 
 
 #####
 
 ## Create test tables in peters_playground for running new indicators *percent units in ugb*
 
 create table geographies select * from PSRC_2000_base_run_2_output.geographies;
 create table geography_names select * from PSRC_2000_base_run_2_output.geography_names;
 
 create temporary table tmp_gridcells select * from PSRC_2000_scenario_A_no_ugb_output_Jan_06_13_22_18.gridcells_exported where
residential_units > 10 order by rand() limit 50;
 
 create index grid_id_index on tmp_gridcells (grid_id);
 
 create table gridcells_in_geography select a.* from PSRC_2000_scenario_A_no_ugb_output_Jan_06_13_22_18.gridcells_in_geography a inner join tmp_gridcells b
on a.grid_id = b.grid_id;
 
 create index grid_id_index on gridcells_in_geography (grid_id);
 
 create table gridcells_exported select a.* from PSRC_2000_scenario_A_no_ugb_output_Jan_06_13_22_18.gridcells_exported a inner join 
gridcells_in_geography b on a.grid_id = b.grid_id where year in (2001, 2010, 2020, 2030);

 
 
####
##
## Create new Developer Model Specification table for reestimation
## 
###

create table developer_model_specification (SUB_MODEL_ID INT, EQUATION_ID INT, VARIABLE_NAME TEXT, COEFFICIENT_NAME TEXT, SHORT_NAME TEXT);

insert into developer_model_specification (variable_name, coefficient_name,
 select VARIABLE_NAME, SHORT_NAME, 
 


create temporary table prelim_dm_spec
 select 
 a.E_BW, 
 a.AGE_BL, 
 a.SFCWRT, 
 a.ONE , 
 a.G_IS_I, 
 a.DVLPD , 
 a.FLOOD , 
 a.STRBUF, 
 a.WTLND , 
 a.ART , 
 a.HWY , 
 a.O_UGB , 
 a.LALVAW, 
 a.LAVURW, 
 a.LSFCWR, 
 a.LD_HY , 
 a.LHAE1 , 
 a.LSFIW , 
 a.LLV , 
 a.LP_W03, 
 a.LP_W02, 
 a.LP_W01, 
 a.LP_W04, 
 a.LP_W05, 
 a.LIVU, 
 a.LDU , 
 a.LDUW, 
 a.LSFREW, 
 a.LE_W, 
 a.LIV , 
 a.LLVA_W, 
 a.LNRSFW, 
 a.LVU_RW, 
 a.LV, 
 a.TR03WR, 
 a.TRDWRT, 
 a.TR01WR, 
 a.TR05WR, 
 a.TRSWRT, 
 a.DURWRT, 
 a.P03W, 
 a.P_DEV , 
 a.PFL , 
 a.PHIW, 
 a.P01W, 
 a.PLIW, 
 a.PMIW, 
 a.PMNW, 
 a.POPEN , 
 a.PPUB, 
 a.P05W, 
 a.PROAD , 
 a.PSTCW , 
 a.PSLOPE, 
 a.PSTBUF, 
 a.PWATER, 
 a.PWETLA, 
 a.PT0001, 
 a.PT0010, 
 a.PT0011, 
 a.PT0002, 
 a.PT0003, 
 a.PT0004, 
 a.PT0005, 
 a.PT0006, 
 a.PT0007, 
 a.PT0008, 
 a.PT0009, 
 a.PRXDEV, 
 a.DURW, 
 a.E_REW , 
 a.E_SEW , 
 a.TT_CBD 
from GSPSRC_2000_baseyear_flattened.developer_model_estimation_data a;
 
 
# Regional Level

 create temporary table tmp_jobs 
  select grid_id, count(*) as jobs 
  from jobs where home_based = 0 
  group by grid_id;

 create index grid_id_index on tmp_jobs (grid_id);

 create temporary table tmp_jobs_devtype 
  select b.development_type_id, sum(jobs) as jobs 
  from tmp_jobs a inner join gridcells b on a.grid_id = b.grid_id 
  group by b.development_type_id;
  
 create temporary table tmp_sqft_devtypes
  select development_type_id, sum(total_nonres_sqft) as sqft 
  from gridcells 
  group by development_type_id; 

 create temporary table tmp_devtype_ratios
   select a.development_type_id, (b.sqft / a.jobs) as ratio 
   from tmp_jobs_devtype a inner join tmp_sqft_devtypes b on a.development_type_id = b.development_type_id;

# IN_UGB

create temporary table prelim_jobs_devtype_ugb
 select a.grid_id, count(*) as jobs
 from jobs a inner join gridcells b on a.grid_id = b.grid_id
 where home_based = 0 and b.is_outside_urban_growth_boundary = 0
 group by a.grid_id;

create index grid_id_index on prelim_jobs_devtype_ugb (grid_id);

create temporary table tmp_jobs_devtype_ugb
 select b.development_type_id, sum(jobs) as jobs
 from prelim_jobs_devtype_ugb a inner join gridcells b on a.grid_id = b.grid_id
 group by b.development_type_id;

create temporary table tmp_sqft_devtype_ugb
 select development_type_id, sum(total_nonres_sqft) as sqft
 from gridcells 
 where is_outside_urban_growth_boundary = 0
 group by development_type_id;
 
create temporary table tmp_devtype_ratios_ugb
 select a.development_type_id, (b.sqft / a.jobs) as ratio
 from tmp_jobs_devtype_ugb a inner join tmp_sqft_devtype_ugb b on a.development_type_id = b.development_type_id;
 

# OUT_UGB 
 
 create temporary table prelim_jobs_devtype_ugb_out
  select a.grid_id, count(*) as jobs
  from jobs a inner join gridcells b on a.grid_id = b.grid_id
  where home_based = 0 and b.is_outside_urban_growth_boundary = 1
  group by a.grid_id;
 
 create index grid_id_index on prelim_jobs_devtype_ugb_out (grid_id);
 
 create temporary table tmp_jobs_devtype_ugb_out
  select b.development_type_id, sum(jobs) as jobs
  from prelim_jobs_devtype_ugb_out a inner join gridcells b on a.grid_id = b.grid_id
  group by b.development_type_id;
 
 create temporary table tmp_sqft_devtype_ugb_out
  select development_type_id, sum(total_nonres_sqft) as sqft
  from gridcells 
  where is_outside_urban_growth_boundary = 1
  group by development_type_id;
  
 create temporary table tmp_devtype_ratios_ugb_out
  select a.development_type_id, (b.sqft / a.jobs) as ratio
  from tmp_jobs_devtype_ugb_out a inner join tmp_sqft_devtype_ugb_out b on a.development_type_id = b.development_type_id;
  
 ####
 ### Running DM EDW using line command interface
 ####
 
 cd c:\eclipse\workspace\UrbanSim3: java -Xmx1500m -cp
 
 
 
 ######
 create temporary table tmp_summary_transitions
 select 
  starting_development_type_id, 
  ending_development_type_id, 
  HOUSING_UNITS_MEAN,
  COMMERCIAL_SQFT_MEAN,
  INDUSTRIAL_SQFT_MEAN,
  GOVERNMENTAL_SQFT_MEAN,
  HOUSING_IMPROVEMENT_VALUE_MEAN,
  COMMERCIAL_IMPROVEMENT_VALUE_MEAN,
  INDUSTRIAL_IMPROVEMENT_VALUE_MEAN,
  GOVERNMENTAL_IMPROVEMENT_VALUE_MEAN
  from transition_types
 group by starting_development_type_id, ending_development_type_id;
 
 create temporary table tmp_summary_devhistory
 select 
  starting_development_type_id, 
  ending_development_type_id, 
  avg(residential_units),
  COMMERCIAL_SQFT_MEAN,
  INDUSTRIAL_SQFT_MEAN,
  GOVERNMENTAL_SQFT_MEAN,
  HOUSING_IMPROVEMENT_VALUE_MEAN,
  COMMERCIAL_IMPROVEMENT_VALUE_MEAN,
  INDUSTRIAL_IMPROVEMENT_VALUE_MEAN,
  GOVERNMENTAL_IMPROVEMENT_VALUE_MEAN
  from development_event_history
 group by starting_development_type_id, ending_development_type_id;
 
 create temporary table tmp_avg_impvalue_dt
 select 
  development_type_id,
  avg(commercial_sqft) as com_sqft,
  avg(industrial_sqft) as ind_sqft,
  avg(governmental_sqft) as gov_sqft,
  avg(commercial_improvement_value) as com_imp,
  avg(industrial_improvement_value) as ind_imp,
  avg(governmental_improvement_value) as gov_imp,
  avg(RESIDENTIAL_IMPROVEMENT_VALUE) as res_imp
  from gridcells
 group by development_type_id;
 
 create temporary table tmp_summary_dt
 select  
 development_type_id,
 count(*),
 avg(COMMERCIAL_IMPROVEMENT_VALUE),  
 avg(INDUSTRIAL_IMPROVEMENT_VALUE),  
 avg(GOVERNMENTAL_IMPROVEMENT_VALUE),
 avg(RESIDENTIAL_IMPROVEMENT_VALUE)
 from GSPSRC_2000_baseyear_flattened.gridcells 
 group by development_type_id;
 
 select 
 max(COMMERCIAL_SQFT),
 max(GOVERNMENTAL_SQFT),             
 max(INDUSTRIAL_SQFT),              
 max(COMMERCIAL_IMPROVEMENT_VALUE),  
 max(INDUSTRIAL_IMPROVEMENT_VALUE),  
 max(GOVERNMENTAL_IMPROVEMENT_VALUE),
 max(NONRESIDENTIAL_LAND_VALUE),     
 max(RESIDENTIAL_LAND_VALUE),       
 max(RESIDENTIAL_IMPROVEMENT_VALUE),
 max(residential_units)
 from gridcells;
 
 #####
 create temporary table tmp_parcel_frac_with_grid_656302
  select * from parcel_fractions_in_gridcells where grid_Id = 656302;
 
 create temporary table tmp_grid_656302
 select
  parcel_id,
  improvement_value,
  land_use,
  county, 
 from parcels where parcel_id in 
 ('1697508888',
 '1974700010',
 '1974700170',
 '1974700190',
 '1976200030',
 '1976200031',
 '1976200035',
 '1976200060',
 '1976200070',
 '1976200075',
 '1976200076',
 '7666202450',
 '7666202461',
 '7666202465',
 '7666202475',
 '7666202480');
 
 update tmp_grid_656302 a inner join PSRC_2000_reclassification_tables.land_use_generic_reclass b on 
  a.county = b.county and a.land_use = b.county_land_use_code 
  set a.generic_lu = b.generic_land_use_2;
 
 create temporary table tmp_frac_656302
 select * from parcel_fractions_in_gridcells where grid_id = 656302;
 
 
 select improvement_value * parcel_fraction from tmp_grid_656302 a 
  inner join tmp_frac_656302 b on a.parcel_id = b.parcel_id 
  where a.generic_lu = 'R';
  
 #### 
 create temporary table tmp_grid_231371
  select * from parcel_fractions_in_gridcells where grid_id = 231371;
  
 create temporary table tmp_parcel_with_grid_231371
 select * from parcels where parcel_id in (
 '1052963',
 '1052976',
 '1052978',
 '1052982');
 
 alter table tmp_parcel_with_grid_231371 add column generic_lu text;
 
 update tmp_parcel_with_grid_231371 a inner join PSRC_2000_reclassification_tables.land_use_generic_reclass b on 
  a.county = b.county and a.land_use = b.county_land_use_code 
  set a.generic_lu = b.generic_land_use_2;
 
 select parcel_fraction * improvement_value from tmp_grid_231371 a inner join tmp_parcel_with_grid_231371 b on a.parcel_id = b.parcel_id
  where b.generic_lu = 'R';
 
  
 
 select * from development_event_history where grid_id in (
 669484,
 669485,
 670685,
 670686,
 671885,
 673085)
 
 create temporary table tmp_res_imp_unit
  select 
  starting_development_type_id, 
  ending_development_type_id,
  sum(RESIDENTIAL_IMPROVEMENT_VALUE) as res_imp_value,
  count(*) as count
  from development_event_history
 group by starting_development_type_id, ending_development_type_id;
 
 create temporary table tmp_res_imp_unit_3
  select 
  starting_development_type_id, 
  ending_development_type_id,
  sum(RESIDENTIAL_IMPROVEMENT_VALUE) as res_imp_value,
  sum(residential_units) as units,
  count(*) as count
  from development_event_history
 group by starting_development_type_id, ending_development_type_id;
 
 alter table tmp_res_imp_unit_3 add column res_imp_valu_adj double;
 alter table tmp_res_imp_unit_3 add column res_imp_valu_adj_count double;
 
 update tmp_res_imp_unit_3 set res_imp_valu_adj = res_imp_value / units;
 update tmp_res_imp_unit_3 set res_imp_valu_adj_count = res_imp_value / count;
 
 create temporary table prelim_transition_types
  select 
  starting_development_type_id,
  ending_development_type_id,
  count(*) as counts,
  sum(residential_improvement_value) as res_imp_value,
  sum(residential_units) as units,
  sum(commercial_improvement_value) as com_imp_value,
  sum(commercial_sqft) as com_sqft,
  sum(industrial_improvement_value) as ind_imp_value,
  sum(industrial_sqft) as ind_sqft,
  sum(governmental_improvement_value) as gov_imp_value,
  sum(governmental_sqft) as gov_sqft
 from development_event_history 
 group by starting_development_type_id, ending_development_type_id;
 
 alter table prelim_transition_types add column res_imp_value_adj double;
 alter table prelim_transition_types add column com_imp_value_adj double;
 alter table prelim_transition_types add column ind_imp_value_adj double;
 alter table prelim_transition_types add column gov_imp_value_adj double;
 
 update prelim_transition_types set res_imp_value_adj = res_imp_value / units;
 update prelim_transition_types set com_imp_value_adj = com_imp_value / com_sqft;
 update prelim_transition_types set ind_imp_value_adj = ind_imp_value / ind_sqft;
 update prelim_transition_types set gov_imp_value_adj = gov_imp_value / gov_sqft;
 
 #####
 create temporary table tmp_summary_tt
 select 
  starting_development_type_id, 
  ending_development_type_id,
  housing_improvement_value_mean,
  commercial_improvement_value_mean,
  industrial_improvement_value_mean,
  governmental_improvement_value_mean
 from transition_types group by  starting_development_type_id, ending_development_type_id;
 
 
 ####
 
 select * from model_variables where variable_name in (
  'constant',                                                 
  'ln_average_land_value_per_acre_within_walking_distance',   
  'ln_total_value',   
  'n_recent_transitions_to_developed_within_walking_distance',
  'percent_developed_within_walking_distance',
  'percent_same_type_cells_within_walking_distance',
  'percent_commercial_within_walking_distance',
  'percent_residential_within_walking_distance',
  'percent_industrial_within_walking_distance',
  'is_near_arterial',
  'is_near_highway')\G
  
  ###
 create temporary table tmp_units
 select grid_id, sum(residential_units) as units from households group by grid_id;
  
 alter table tmp_units add index grid_id_index(grid_id);
 
 create temporary table tmp_home_jobs
 select grid_id, count(*) as jobs from jobs where home_based = 1 group by grid_id;
  
 alter table tmp_home_jobs add index grid_id_index(grid_id);
 
 create temporary table tmp_households 
  select grid_id, count(*) as households from households group by grid_id;
  
 alter table tmp_households add index grid_id_index(grid_id);
  
 create temporary table tmp_summary_unplaced
  select a.grid_id, a.jobs, b.units, c.households from tmp_home_jobs a left join tmp_units b on a.grid_id = b.grid_id left join tmp_households c
  on a.grid_id = c.grid_id;
 
 ####
 create temporary table tmp_jobs select grid_id, count(*) as jobs from jobs_exported_denormalized where home_based = 1 and year = 2001 group by grid_id;
 alter table tmp_jobs add index grid_id_index(grid_id);
 
 create temporary table tmp_gridcells select * from gridcells_exported_denormalized where year = 2001;
 alter table tmp_gridcells add index grid_id_index(grid_id);
 
 select development_type_id, count(*) from tmp_jobs a left join tmp_gridcells b on a.grid_Id = b.grid_id group by development_type_id;
 
 ### Added jobs
 
 create temporary table tmp_jobs_new select a.* from jobs_constants a left join GSPSRC_2000_baseyear_flattened_old_estimated_data_20050524.jobs b 
  on a.job_id = b.job_id where b.job_id is null;
 
 alter table tmp_jobs_new add index job_id_index(job_id);
 
 create temporary table tmp_jobs_home 
  select 
  b.YEAR,
  a.JOB_ID,
  a.SECTOR_ID,
  b.GRID_ID, 
  b.HOME_BASED,
  b.ZONE_ID
 from tmp_jobs_new a left join jobs_exported b on a.job_id = b.job_id 
 where b.home_based = 1;
 
 #### remove sub_model_id and equation_id from development_event_history and transition_types table that are not in DM spec table
 
 create temporary table tmp_dm_spec 
  select sub_model_id, equation_id 
  from GSPSRC_2000_baseyear_flattened.developer_model_specification
 group by sub_model_id, equation_id;
 
 create temporary table tmp_devhistory
  select starting_development_type_id, ending_development_type_id 
  from development_event_history
 group by starting_development_type_id, ending_development_type_id;
 
 create temporary table tmp_not_used select a.* from tmp_devhistory a 
  left join tmp_dm_spec b on a.starting_development_type_id = b.sub_model_id 
  and a.ending_development_type_id = b.equation_id 
 where b.sub_model_id is null and b.equation_id is null;
 
 delete deh.* from development_event_history as deh, tmp_not_used not_used
  where deh.starting_development_type_id = not_used.starting_development_type_id 
  and deh.ending_development_type_id = not_used.ending_development_type_id;
  
 delete tt.* from transition_types tt, tmp_not_used not_used
   where tt.starting_development_type_id = not_used.starting_development_type_id 
   and tt.ending_development_type_id = not_used.ending_development_type_id;
 
 
 ###### Check real estate inventory from new transition types table
 
 /* scenario_test_transition_types_output_petecaba_050602 */
 
 create temporary table tmp_transition_summary
  (year int, unit double, res_impvl double, res_avg double, 
  com_sqft double, com_impvl double, com_avg double, 
  ind_sqft double, ind_impvl double, ind_avg double, 
  gov_sqft double, gov_impvl double, gov_avg double);
 
 insert into tmp_transition_summary (year, unit, res_impvl, com_sqft, com_impvl, ind_sqft, ind_impvl, gov_sqft, gov_impvl)
 select 
  year,
  sum(residential_units) as units,
  sum(residential_improvement_value) as res_impvl,
  sum(commercial_sqft) as com_sqft,
  sum(commercial_improvement_value) as com_impvl,
  sum(industrial_sqft) as ind_sqft,
  sum(industrial_improvement_value) as ind_impvl,
  sum(governmental_sqft) as gov_sqft,
  sum(governmental_improvement_value) as gov_impvl
 from gridcells_exported where year <= 2001 group by year;
 
 update tmp_transition_summary set
  res_avg = res_impvl / unit,
  com_avg = com_impvl / com_sqft,
  ind_avg = ind_impvl / ind_sqft,
  gov_avg = gov_impvl / gov_sqft;
 
 ##
 create temporary table tmp_transition_summary
  (year int, unit double, res_impvl double, res_avg double, 
  com_sqft double, com_impvl double, com_avg double, 
  ind_sqft double, ind_impvl double, ind_avg double, 
  gov_sqft double, gov_impvl double, gov_avg double);
 
 
 insert into tmp_transition_summary (unit, res_impvl, com_sqft, com_impvl, ind_sqft, ind_impvl, gov_sqft, gov_impvl)
 select 
  sum(residential_units) as units,
  sum(residential_improvement_value) as res_impvl,
  sum(commercial_sqft) as com_sqft,
  sum(commercial_improvement_value) as com_impvl,
  sum(industrial_sqft) as ind_sqft,
  sum(industrial_improvement_value) as ind_impvl,
  sum(governmental_sqft) as gov_sqft,
  sum(governmental_improvement_value) as gov_impvl
 from gridcells
 
 
 ## Check transition types
 
 create table tmp_gridcells_2001 select * from gridcells_exported where year = 2001;
 alter table tmp_gridcells_2001 add index grid_id_index(grid_id);
 
 create temporary table tmp_transition_summary
 
 create temporary table tmp_summary
 select 
  a.DEVELOPMENT_TYPE_ID as STARTING_ID,
  b.DEVELOPMENT_TYPE_ID as ENDING_ID,
  sum(b.residential_units) as UNITS_SUM,
  min(b.residential_units) as UNITS_MIN,
  max(b.residential_units) as UNITS_MAX,
  avg(b.residential_units) as UNITS_AVG,
  sum(b.residential_improvement_value) as RES_SUM_IMPVL,
  min(b.residential_improvement_value) as RES_MIN_IMPVL,
  max(b.residential_improvement_value) as RES_MAX_IMPVL,
  avg(b.residential_improvement_value) as RES_AVG_IMPVL,
  sum(b.commercial_sqft) as COM_SUM_SQFT,
  min(b.commercial_sqft) as COM_MIN_SQFT,
  max(b.commercial_sqft) as COM_MAX_SQFT, 
  avg(b.commercial_sqft) as COM_AVG_SQFT,
  sum(b.commercial_improvement_value) as COM_SUM_IMPVL,
  min(b.commercial_improvement_value) as COM_MIN_IMPVL,
  max(b.commercial_improvement_value) as COM_MAX_IMPVL,
  avg(b.commercial_improvement_value) as COM_AVG_IMPVL,
  sum(b.industrial_sqft) as IND_SUM_SQFT,
  min(b.industrial_sqft) as IND_MIN_SQFT,
  max(b.industrial_sqft) as IND_MAX_SQFT, 
  avg(b.industrial_sqft) as IND_AVG_SQFT,
  sum(b.industrial_improvement_value) as IND_SUM_IMPVL,
  min(b.industrial_improvement_value) as IND_MIN_IMPVL,
  max(b.industrial_improvement_value) as IND_MAX_IMPVL,
  avg(b.industrial_improvement_value) as IND_AVG_IMPVL,
  sum(b.governmental_sqft) as GOV_SUM_SQFT,
  min(b.governmental_sqft) as GOV_MIN_SQFT,
  max(b.governmental_sqft) as GOV_MAX_SQFT, 
  avg(b.governmental_sqft) as GOV_AVG_SQFT,
  sum(b.governmental_improvement_value) as GOV_SUM_IMPVL,
  min(b.governmental_improvement_value) as GOV_MIN_IMPVL,
  max(b.governmental_improvement_value) as GOV_MAX_IMPVL,
  avg(b.governmental_improvement_value) as GOV_AVG_IMPVL
 from GSPSRC_2000_baseyear_flattened.gridcells a
  inner join tmp_gridcells_2001 b on 
  a.grid_id = b.grid_id
 group by a.development_type_id, b.development_type_id;
 
update transition_summary set 
 res_avg_impvl = res_sum_impvl / units_sum,
 com_avg_impvl = com_sum_impvl / com_sum_sqft,
 ind_avg_impvl = ind_sum_impvl / ind_sum_sqft,
 gov_avg_impvl = gov_sum_impvl / gov_sum_sqft;


#### Examine LV for DM coefficients

select 
 coefficient_name, 
 count(*), 
 sum(estimate) as estimate, 
 min(estimate) as min_estimate, 
 max(estimate) as max_estimate,
 avg(estimate) as avg_estimate
from GSPSRC_2000_baseyear_flattened_old_estimated_data_20050524.developer_model_coefficients 
 where coefficient_name like '%lv%'
group by coefficient_name;


##### Get records not used in Development Event History table 

create table test_deh_temp_avg_impv_by_county_peter
select
	su.county,
	sum(IF(su.RESIDENTIAL_UNITS>0, RESIDENTIAL_IMPROVEMENT_VALUE, 0)) as TOTAL_RES_IMPV,
	sum(IF(su.COMMERCIAL_SQFT>0, COMMERCIAL_IMPROVEMENT_VALUE, 0)) as TOTAL_COM_IMPV,
	sum(IF(su.INDUSTRIAL_SQFT>0, INDUSTRIAL_IMPROVEMENT_VALUE, 0)) as TOTAL_IND_IMPV,
	sum(IF(su.GOVERNMENTAL_SQFT>0, GOVERNMENTAL_IMPROVEMENT_VALUE, 0)) as TOTAL_GOV_IMPV,

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

create table p
select imp.*
 from deh_ptemp_units_impv_by_parcel imp inner join deh_ctemp_sqft_units_by_parcel_year su
 on imp.parcel_id = su.parcel_id and imp.county = su.county where ((su.county = '033') and su.year_built = 2000)
 and su.residential_units = 0 and residential_improvement_value > 0;

### Check starting to ending development types from baseyear to re-estimated simulation data

select b.development_type_Id as starting, a.development_type_id as ending_id, count(*) 
 from gridcells_exported a 
 left join GSPSRC_2000_baseyear_flattened.gridcells b  
 on a.grid_id = b.grid_id 
 where a.year = 2001 and a.development_type_id <> b.development_type_Id 
group by b.development_type_Id, a.development_type_id;

### Insert development type ids into the development_type_groups table 

insert into development_type_group_definitions (development_type_id, group_id) values 
(26, 11), 
(27, 11), 
(28, 11), 
(29, 11);


### Send output to mysql localhost ###

<mysql url="jdbc:mysql://localhost/PSRC_2000_test_dm_all_models_50yrs"

### 6/17 Create proportion_jobs_to_buildings ###

Need reclassification table for jobs. SECTOR_ID --> NEW_SECTOR

create table employment_sector_reclass 
 (SECTOR_ID int, NAME varchar(50), NEW_SECTOR VARCHAR(50));
 
insert into employment_sector_reclass values
 (1, 'Resource', 'Industrial'),
 (2, 'Construction', 'Industrial'),
 (3, 'Manufacturing - Aviation', 'Industrial'),
 (4, 'Manufacturing - Other', 'Industrial'),
 (5, 'Transportation', 'Industrial'),
 (6, 'Communications and Utilities', 'Industrial'),
 (7, 'Wholesale Trade', 'Commercial'),
 (8, 'Eating and Drinking Places', 'Commercial'),
 (9, 'Other Retail Trade', 'Commercial'),
 (10, 'Finance, Insurance, and Real Estate', 'Commercial'),
 (11, 'Producer Services', 'Commercial'),
 (12, 'Consumer Services', 'Commercial'),
 (13, 'Health Services', 'Government'),
 (14, 'Federal Government Civilian', 'Government'),
 (15, 'Federal Government, Military', 'Government'),
 (16, 'Education, K-12', 'Government'),
 (17, 'Education, Higher', 'Government'),
 (18, 'State, Local Government', 'Government');

alter table employment_sector_reclass add index sector_index(sector_id);
create table jobs_new select * from jobs;
alter table jobs_new add column NEW_SECTOR text;
alter table jobs_new add index sector_index(sector_id);

update jobs_new a inner join employment_sector_reclass b on a.sector_id = b.sector_id
 set a.new_sector = b.new_sector;

update jobs_new set new_sector = 'Residential' where home_based = 1;   


### 6/17 Insert records for ELHB specification and coefficients table for sectors 14-18 ###

insert into employment_home_based_location_choice_model_coefficients values 
 (14, 'BTT_CBD', -0.01563432947, 0.00076766984, -20.366, 0),
 (14, 'BPHIW', 0.008973033931, 0.0011086245, 8.094, 0),
 (14, 'BP05W', -0.02615249096, 0.00066931544, -39.073, 0),
 (15, 'BTT_CBD', -0.01563432947, 0.00076766984, -20.366, 0),
 (15, 'BPHIW', 0.008973033931, 0.0011086245, 8.094, 0),
 (15, 'BP05W', -0.02615249096, 0.00066931544, -39.073, 0),
 (16, 'BTT_CBD', -0.01563432947, 0.00076766984, -20.366, 0),
 (16, 'BPHIW', 0.008973033931, 0.0011086245, 8.094, 0),
 (16, 'BP05W', -0.02615249096, 0.00066931544, -39.073, 0),
 (17, 'BTT_CBD', -0.01563432947, 0.00076766984, -20.366, 0),
 (17, 'BPHIW', 0.008973033931, 0.0011086245, 8.094, 0),
 (17, 'BP05W', -0.02615249096, 0.00066931544, -39.073, 0),
 (18, 'BTT_CBD', -0.01563432947, 0.00076766984, -20.366, 0),
 (18, 'BPHIW', 0.008973033931, 0.0011086245, 8.094, 0),
 (18, 'BP05W', -0.02615249096, 0.00066931544, -39.073, 0);
 
insert into employment_home_based_location_choice_model_specification values 
 (14, -2, 'percent_high_income_households_within_walking_distance', 'BPHIW'),
 (14, -2, 'percent_residential_within_walking_distance', 'BP05W'),
 (14, -2, 'travel_time_to_CBD', 'BTT_CBD'),
 (15, -2, 'percent_high_income_households_within_walking_distance', 'BPHIW'),
 (15, -2, 'percent_residential_within_walking_distance', 'BP05W'),
 (15, -2, 'travel_time_to_CBD', 'BTT_CBD'),
 (16, -2, 'percent_high_income_households_within_walking_distance', 'BPHIW'),
 (16, -2, 'percent_residential_within_walking_distance', 'BP05W'),
 (16, -2, 'travel_time_to_CBD', 'BTT_CBD'),
 (17, -2, 'percent_high_income_households_within_walking_distance', 'BPHIW'),
 (17, -2, 'percent_residential_within_walking_distance', 'BP05W'),
 (17, -2, 'travel_time_to_CBD', 'BTT_CBD'),
 (18, -2, 'percent_high_income_households_within_walking_distance', 'BPHIW'),
 (18, -2, 'percent_residential_within_walking_distance', 'BP05W'),
 (18, -2, 'travel_time_to_CBD', 'BTT_CBD');
 
 ### Assign building type to jobs table ###
 
 use employers_to_jobs_prep.sql script
 
 alter table tmp_employers_3 add column LAND_USE varchar(50);
 alter table tmp_employers_3 add column USE_CODE int;
 alter table tmp_employers_3 add column GENERIC_LU varchar(20);
 alter table tmp_employers_3 add column COUNTY varchar(3);
 
 update tmp_employers_3 a inner join parcels b on a.parcel_id = b.parcel_id 
  set a.land_use = b.land_use, a.use_code = b.use_code, a.county = b.county;
  
 alter table tmp_employers_3 add index cnty_lu_index(county(3), use_code);
 
 update tmp_employers_3 a inner join PSRC_2000_reclassification_tables.land_use_generic_reclass b 
  on a.county = b.county and a.use_code = b.county_land_use_code
  set a.generic_lu = b.generic_land_use_2;
 
 create table tmp_employers_lu 
  select 
  	grid_id,
  	sector,
  	home_based,
  	sum(job_count_rounded) as jobs,
  	sic,
  	generic_lu
  from tmp_employers_3
  group by grid_id, sector, home_based, generic_lu;
  
 alter table tmp_employers_lu add index grid_id_index(grid_id);
 
 
  
 #### Check non-home-based jobs on residential building types ####
 
 create temporary table tmp_jobs 
  select a.*, b.county_id from jobs a inner join gridcells b
  on a.grid_id = b.grid_id;
  
 alter table tmp_jobs add index grid_id_index(grid_id); 
 
 create temporary table tmp_jobs_kitsap_nhb_r
  select * from tmp_jobs where home_based = 0 and county_id = 35 and building_type = 'R';
  
 alter table tmp_jobs_kitsap_nhb_r add index grid_id_index(grid_id);
 
 #### Check assignment of home-based id after job allocation process ####
 
 create temporary table tmp_employers_lu
  select 
  	a.*, 
  	b.use_code, 
  	b.land_use,
  	c.number_of_jobs
  from tmp_employers_1 a inner join parcels b 
   on a.parcel_id = b.parcel_id
  left join employers c
   on a.employer_id = c.employer_id;
   
   
#### Review Job Allocation records that were placed and not placed ####

## Placed Jobs ##
 select sum(b.number_of_jobs)
 from final_employers_matched_to_parcels a
  inner join employers b on a.employer_id = b.employer_id 
  where a.decision not in 
  ('WRONG_SIDE_OF_STREET', 
   'NO_PARCEL_IN_BLOCK',
   'WRONG_STREET_TYPE_FOR_BLOCK');

## Unplaced Jobs ##   
select sum(b.number_of_jobs)
  from final_employers_matched_to_parcels a
   inner join employers b on a.employer_id = b.employer_id 
   where a.decision in 
   ('WRONG_SIDE_OF_STREET', 
    'NO_PARCEL_IN_BLOCK',
   'WRONG_STREET_TYPE_FOR_BLOCK');

####################################################################   
#### Consumption Rates using on C, G, I, and Mix-used gridcells ####


#### Four county consumption rate totals ####

create table consumption_rates_county 
 (county_id int, 
  com_sqft double, 
  gov_sqft double, 
  ind_sqft double,
  com_jobs double,
  ind_jobs double,
  gov_jobs double,
  com_sqft_per_job double,
  gov_sqft_per_job double,
  ind_sqft_per_job double,
  median_com_sqft_per_job double,
  median_ind_sqft_per_job double,
  median_gov_sqft_per_job double
  );
  
insert into consumption_rates_county (county_id) 
select distinct county_id 
from gridcells;
 
create temporary table tmp_com_sqft 
 select	
 	county_id, 
 	sum(commercial_sqft) as sqft
 from gridcells
 where commercial_sqft > 0 
  and governmental_sqft = 0
  and industrial_sqft = 0
 group by county_id;

create temporary table tmp_ind_sqft
 select county_id, sum(industrial_sqft) as sqft from gridcells
  where industrial_sqft > 0 and
  commercial_sqft = 0
 and governmental_sqft = 0
 group by county_id;

create temporary table tmp_gov_sqft
 select county_id, sum(governmental_sqft) as sqft from gridcells
  where governmental_sqft > 0 and
  commercial_sqft = 0
 and industrial_sqft = 0
 group by county_id;

update consumption_rates_county a 
 inner join tmp_com_sqft b on a.county_id = b.county_id
  set a.com_sqft = b.sqft;

update consumption_rates_county a 
 inner join tmp_ind_sqft b on a.county_id = b.county_id
  set a.ind_sqft = b.sqft;
 
update consumption_rates_county a 
 inner join tmp_gov_sqft b on a.county_id = b.county_id
  set a.gov_sqft = b.sqft; 


#Create commercial jobs
create temporary table tmp_com_cells1
 select 
	county_id,
	grid_id,
	commercial_sqft
 from gridcells 
 where commercial_sqft > 0 and
 governmental_sqft = 0
 and industrial_sqft = 0;
 
alter table tmp_com_cells1 add index grid_id_index(grid_id);

create temporary table tmp_com_cells2
select 
	county_id, 
	count(*) as jobs 
from jobs a 
inner join tmp_com_cells1 b on 
 a.grid_id = b.grid_id 
where a.building_type = 'C'
group by county_id;
 
update consumption_rates_county a inner join tmp_com_cells2 b on a.county_id = b.county_id
 set a.com_jobs = b.jobs;

#Create industrial jobs
create temporary table tmp_ind_cells1
 select 
	county_id,
	grid_id,
	industrial_sqft
 from gridcells 
 where industrial_sqft > 0 and
 governmental_sqft = 0
 and commercial_sqft = 0;
 
alter table tmp_ind_cells1 add index grid_id_index(grid_id);

create temporary table tmp_ind_cells2
select 
	county_id,
	count(*) as jobs 
from jobs a inner join tmp_ind_cells1 b 
 on a.grid_id = b.grid_id
where a.building_type = 'I'
group by county_id;

update consumption_rates_county a inner join tmp_ind_cells2 b on a.county_id = b.county_id
 set a.ind_jobs = b.jobs;
 
#Create government jobs
create temporary table tmp_gov_cells1
 select 
	county_id,
	grid_id,
	governmental_sqft
 from gridcells 
 where governmental_sqft > 0 and
 industrial_sqft = 0
 and commercial_sqft = 0;
 
alter table tmp_gov_cells1 add index grid_id_index(grid_id);

create temporary table tmp_gov_cells2
select 
	county_id,
	count(*) as jobs 
from jobs a inner join tmp_gov_cells1 b 
 on a.grid_id = b.grid_id
where a.building_type = 'G'
group by county_id;

update consumption_rates_county a inner join tmp_gov_cells2 b on a.county_id = b.county_id
 set a.gov_jobs = b.jobs;

# calculate the sqft per employee ratios #
update consumption_rates_county set com_sqft_per_job = com_sqft / com_jobs;
update consumption_rates_county set gov_sqft_per_job = gov_sqft / gov_jobs;
update consumption_rates_county set ind_sqft_per_job = ind_sqft / ind_jobs;

# Delete temporary tables
delete from consumption_rates_county where county_id = 0
drop table tmp_com_sqft;
drop table tmp_ind_sqft;
drop table tmp_gov_sqft;
drop table tmp_com_cells1;
drop table tmp_ind_cells1;
drop table tmp_gov_cells1;
drop table tmp_com_cells2;
drop table tmp_ind_cells2;
drop table tmp_gov_cells2;

#############################################################################
## Get Median commercial and industrial sqft per job values from gridcells ##

# If needed add auto_increment field to table
# alter table x add ID int not null auto_increment, primary key(ID);

drop table if exists tmp_com_sqft_ordered;
create temporary table tmp_com_sqft_ordered_county
select
	grid_id,
	commercial_sqft_per_job,
	county_id
from gridcells 
where commercial_sqft_per_job > 0
order by commercial_sqft_per_job asc;

## Determine if odd or even number of records ##
select count(*) from tmp_com_sqft_ordered;
## If count is even than the median value is the middle value
# Example query: 

select commercial_sqft_per_job 
from tmp_com_sqft_ordered 
order by 1 limit 8907, 2;

## If count is odd than the median value is the teh average of the two middle values

select commercial_sqft_per_job
from tmp_com_sqft_ordered
order by 1 limit 8907,1;

 
#### Get Industrial Median sqft per job from gridcells ####

drop table if exists tmp_ind_sqft_ordered;
create temporary table tmp_ind_sqft_ordered_county
select
	grid_id,
	industrial_sqft_per_job,
	county_id
from gridcells 
where industrial_sqft_per_job > 0
order by industrial_sqft_per_job asc;

alter table tmp_ind_sqft_ordered_county add id int not null auto_increment, add primary key (ID);

## Determine if odd or even number of records ##
select * from tmp_ind_sqft_ordered
order by 1 limit 3864,1;


########################################################################################################
#### create cross tabulation of jobs allocated to parcels from job_allocation_county_name databases ####

use job_allocation_king;

create table tmp_placed_employers1 
 select a.decision, sum(b.number_of_jobs) as jobs
 from final_employers_matched_to_parcels a 
  inner join employers b on a.employer_id = b.employer_id
  inner join parcels c on a.parcel_id = c.parcel_id
 where c.land_use like '%Residential%'
 group by a.decision;
  
use job_allocation_kitsap;

create table summary_table
 select 
 	a.decision, 
 	sum(b.number_of_jobs) as jobs,
 	c.land_use,
	d.generic_land_use_2
 from final_employers_matched_to_parcels a 
  inner join employers b 
   on a.employer_id = b.employer_id
  inner join parcels c 
   on a.parcel_id = c.parcel_id
  inner join PSRC_2000_reclassification_tables.land_use_generic_reclass d
   on c.county = d.county and c.use_code = d.county_land_use_code
 group by 
 	a.decision,
 	c.land_use,
 	d.generic_land_use_2;

create temporary table test 	
select 
	a.employer_id,
	a.parcel_id,
	c.use_code,
	c.land_use,
	b.number_of_jobs,
	b.sector
from final_employers_matched_to_parcels a 
 inner join employers b 
  on a.employer_id = b.employer_id
 left join parcels c 
  on a.parcel_id = c.parcel_id
 where c.land_use = 'Multi-Family Residential' 
  and a.decision = 'PSRC_MATCHED';
  
use job_allocation_pierce;

create table tmp_placed_employers 
 select a.decision, sum(b.number_of_jobs) as jobs
 from final_employers_matched_to_parcels a 
  inner join employers b on a.employer_id = b.employer_id
  group by a.decision;

use job_allocation_snohomish;

create temporary table tmp_placed_employers 
 select a.decision, sum(b.number_of_jobs) as jobs
 from final_employers_matched_to_parcels a 
  inner join employers b on a.employer_id = b.employer_id
  group by a.decision;

################################################################################################  
#### Select records that are NOT home_based, but are on RESIDENTIAL parcels (job allocator) ####
############### 	
#Kitsap County#
create temporary table nhb_res_jobs
 select
 	a.GRID_ID,
 	a.BUILDING_TYPE,
 	a.SECTOR_ID as USIM_SECTOR,
 	a.HOME_BASED,
 	b.PARCEL_ID,
 	c.EMPLOYER_ID,
 	d.DECISION,
 	e.NUMBER_OF_JOBS as ESD_JOBS,
 	e.SECTOR as ESD_SECTOR
 from jobs_all_sectors_reclassified_test a
  inner join jobs_gridcells_1 b
   on a.grid_id = b.grid_id 
   and a.sector_id = b.sector 
   and a.home_based = b.homebased
  inner join job_allocation_kitsap.tmp_employers_2 c
   on b.parcel_id = c.parcel_id
  inner join job_allocation_kitsap.final_employers_matched_to_parcels d
   on c.employer_id = d.employer_id
  inner join job_allocation_kitsap.employers e
   on d.employer_id = e.employer_id
 where 
 	a.job_allocator = 1
 	and a.building_type = 'R'
 	and a.home_based = 0;

############# 
#King County#

create temporary table nhb_res_jobs
 select
 	a.GRID_ID,
 	a.BUILDING_TYPE,
 	a.SECTOR_ID as USIM_SECTOR,
 	a.HOME_BASED,
 	b.PARCEL_ID,
 	c.EMPLOYER_ID,
 	d.DECISION,
 	e.NUMBER_OF_JOBS as ESD_JOBS,
 	e.SECTOR as ESD_SECTOR
 from jobs_all_sectors_reclassified_test a
  inner join jobs_gridcells_1 b
   on a.grid_id = b.grid_id 
   and a.sector_id = b.sector 
   and a.home_based = b.homebased
  inner join job_allocation_king.tmp_employers_2 c
   on b.parcel_id = c.parcel_id
  inner join job_allocation_king.final_employers_matched_to_parcels d
   on c.employer_id = d.employer_id
  inner join job_allocation_king.employers e
   on d.employer_id = e.employer_id
 where 
 	a.job_allocator = 1
 	and a.building_type = 'R'
 	and a.home_based = 0;

############### 	
#Pierce County#
create table nhb_res_jobs
 select
 	a.GRID_ID,
 	a.BUILDING_TYPE,
 	a.SECTOR_ID as USIM_SECTOR,
 	a.HOME_BASED,
 	b.PARCEL_ID,
 	c.EMPLOYER_ID,
 	d.DECISION,
 	e.NUMBER_OF_JOBS as ESD_JOBS,
 	e.SECTOR as ESD_SECTOR
 from jobs_all_sectors_reclassified_test a
  inner join jobs_gridcells_1 b
   on a.grid_id = b.grid_id 
   and a.sector_id = b.sector 
   and a.home_based = b.homebased
  inner join job_allocation_pierce.tmp_employers_2 c
   on b.parcel_id = c.parcel_id
  inner join job_allocation_pierce.final_employers_matched_to_parcels d
   on c.employer_id = d.employer_id
  inner join job_allocation_pierce.employers e
   on d.employer_id = e.employer_id
 where 
 	a.job_allocator = 1
 	and a.building_type = 'R'
 	and a.home_based = 0;
 	
##################
#Snohomish County#

create temporary table nhb_res_jobs1
 select
 	a.GRID_ID,
 	a.BUILDING_TYPE,
 	a.SECTOR_ID as USIM_SECTOR,
 	a.HOME_BASED,
 	b.PARCEL_ID,
 	c.EMPLOYER_ID,
 	d.DECISION,
 	count(*) as USIM_JOBS,
 	e.NUMBER_OF_JOBS as ESD_JOBS,
 	e.SECTOR as ESD_SECTOR
 from jobs_all_sectors_reclassified_test a
  inner join job_allocation_snohomish.tmp_employers_3 b
   on a.grid_id = b.grid_id
   and a.sector_id = b.sector
   and a.home_based = b.home_based
  inner join job_allocation_snohomish.tmp_employers_2 c
   on b.parcel_id = c.parcel_id
   and b.grid_id = c.grid_id
   and b.sector = c.sector
  left join job_allocation_snohomish.final_employers_matched_to_parcels d
   on c.employer_id = d.employer_id
  inner join job_allocation_snohomish.employers e
   on c.employer_id = e.employer_id
 where 
 	a.job_allocator = 1
 	and a.building_type = 'R'
 	and a.home_based = 0
 group by 
 	a.GRID_ID,
 	a.BUILDING_TYPE,
	a.SECTOR_ID,
	a.HOME_BASED,
	b.PARCEL_ID,
	c.EMPLOYER_ID,
	d.DECISION,
	e.NUMBER_OF_JOBS,
	e.SECTOR;
	
	
	
##################################################
create table nhb_res_jobs
 select
 	a.GRID_ID,
 	a.BUILDING_TYPE,
 	a.SECTOR_ID as USIM_SECTOR,
 	a.HOME_BASED,
 	b.PARCEL_ID,
 	c.EMPLOYER_ID,
 	d.DECISION,
 	e.NUMBER_OF_JOBS as ESD_JOBS,
 	e.SECTOR as ESD_SECTOR
 from jobs_all_sectors_reclassified_test a
  inner join job_allocation_snohomish.tmp_employers_3 b
   on a.grid_id = b.grid_id
   and a.sector_id = b.sector
   and a.home_based = b.home_based
  inner join job_allocation_snohomish.tmp_employers_2 c
   on b.parcel_id = c.parcel_id
   and b.grid_id = c.grid_id
   and b.sector = c.sector
  left join job_allocation_snohomish.final_employers_matched_to_parcels d
   on c.employer_id = d.employer_id
  inner join job_allocation_snohomish.employers e
   on c.employer_id = e.employer_id
 where 
 	a.job_allocator = 1
 	and a.building_type = 'R'
 	and a.home_based = 0
 	
#############################################################################################
## Search how many nhb and hb jobs were placed in job allocator and proprietor distributor ##

## Proprietor Distributor ##

create table nhb_hb_prop_jobs (COUNTY_ID int, HOME_BASED tinyint, JOBS int);

insert into nhb_hb_prop_jobs (county_id, home_based, JOBS)
select 33, home_based, count(*) as jobs 
 from PSRC_proprietors_distributor_king.JOBS_ROUNDED
 group by home_based;

insert into nhb_hb_prop_jobs (county_id, home_based, JOBS)
select 35, home_based, count(*) as jobs 
 from PSRC_proprietors_distributor_kitsap.JOBS_ROUNDED
 group by home_based;

insert into nhb_hb_prop_jobs (county_id, home_based, JOBS)
select 53, home_based, count(*) as jobs 
 from PSRC_proprietors_distributor_pierce.JOBS_ROUNDED
 group by home_based;

insert into nhb_hb_prop_jobs (county_id, home_based, JOBS)
select 61, home_based, count(*) as jobs 
 from PSRC_proprietors_distributor_snohomish.JOBS_ROUNDED
 group by home_based;
 
## Job Allocator ##

create table nhb_hb_allocator_jobs (COUNTY_ID int, HOME_BASED tinyint, JOBS int);

insert into nhb_hb_allocator_jobs (county_id, home_based, JOBS)
select 33, home_based, count(*) as jobs 
 from job_allocation_king.jobs
 group by home_based;

insert into nhb_hb_allocator_jobs (county_id, home_based, JOBS)
select 35, home_based, count(*) as jobs 
 from job_allocation_kitsap.jobs
 group by home_based;

insert into nhb_hb_allocator_jobs (county_id, home_based, JOBS)
select 53, home_based, count(*) as jobs 
 from job_allocation_pierce.jobs
 group by home_based;

insert into nhb_hb_allocator_jobs (county_id, home_based, JOBS)
select 61, home_based, count(*) as jobs 
 from job_allocation_snohomish.jobs
 group by home_based;
 
 
## Determine why there are more jobs to be placed in the proprietor distributor than leftover from the job allocator ##
## Reason: Wage and Salary jobs factored in
create table p (total_county_jobs int, job_allocator_leftovers int, proprietors_jobs int, allocated_jobs int, wagesal_totals int);

 insert into p
 select 
	sum(total_county_jobs),
	sum(JOB_ALLOCATOR_LEFTOVERS),
	sum(PROPRIETORS_JOBS), 
	sum(ALLOCATED_JOBS), 
	sum(WAGESAL_TOTALS)  
 from PSRC_proprietors_distributor_king.JOBS_PER_COUNTY;
 
 insert into p
  select 
 	sum(total_county_jobs),
 	sum(JOB_ALLOCATOR_LEFTOVERS),
 	sum(PROPRIETORS_JOBS), 
 	sum(ALLOCATED_JOBS), 
 	sum(WAGESAL_TOTALS)  
 from PSRC_proprietors_distributor_kitsap.JOBS_PER_COUNTY;
 
 insert into p
  select 
 	sum(total_county_jobs),
 	sum(JOB_ALLOCATOR_LEFTOVERS),
 	sum(PROPRIETORS_JOBS), 
 	sum(ALLOCATED_JOBS), 
 	sum(WAGESAL_TOTALS)  
 from PSRC_proprietors_distributor_pierce.JOBS_PER_COUNTY;
 
 insert into p
  select 
 	sum(total_county_jobs),
 	sum(JOB_ALLOCATOR_LEFTOVERS),
 	sum(PROPRIETORS_JOBS), 
 	sum(ALLOCATED_JOBS), 
 	sum(WAGESAL_TOTALS)  
 from PSRC_proprietors_distributor_snohomish.JOBS_PER_COUNTY;
 
 alter table p add column difference int;
 alter table p add column difference_2 int;
 update p set difference_2 = (total_county_jobs-(job_allocator_leftovers + proprietors_jobs));
 update p set difference = (proprietors_jobs +(wagesal_totals - allocated_jobs));

 
###########################################################################
## Find sqft per job ratio found in urban centers and Industrial centers ##

# table can be found in peters_playground 

# create summary table for centers
create table centers_summary 
 (county_id int, 
  com_sqft int,
  ind_sqft int, 
  gov_sqft int,
  com_jobs int,
  ind_jobs int,
  gov_jobs int,
  com_emp_sqft_ratio double,
  ind_emp_sqft_ratio double,
  gov_emp_sqft_ratio double);

insert into centers_summary (county_id) select distinct county_id from gridcells;

# Select records where centers are located #
create temporary table center_cells
 select
  	b.county_id,
 	a.grid_id, 
 	b.commercial_sqft,
 	b.governmental_sqft,
 	b.industrial_sqft
 from urbcen_short a 
 inner join gridcells b 
  on a.grid_id = b.grid_id;
 	
alter table center_cells add index grid_id_index(grid_id);

create temporary table tmp_com_sqft 
 select	
 	county_id, 
 	sum(commercial_sqft) as com_sqft
 from center_cells
 where commercial_sqft > 0 
  and governmental_sqft = 0
  and industrial_sqft = 0
 group by county_id;

create temporary table tmp_ind_sqft
 select 
 	county_id,
 	sum(industrial_sqft) as sqft 
 from center_cells
 where industrial_sqft > 0 
  and commercial_sqft = 0
  and governmental_sqft = 0
 group by county_id;

create temporary table tmp_gov_sqft
 select 
 	county_id,
 	sum(governmental_sqft) as sqft 
 from center_cells
 where governmental_sqft > 0 
  and commercial_sqft = 0
  and industrial_sqft = 0
 group by county_id;


#Create commercial jobs
create temporary table tmp_com_cells
 select 
	county_id,
	grid_id,
	commercial_sqft
 from center_cells
 where commercial_sqft > 0 and
 governmental_sqft = 0
 and industrial_sqft = 0;
 
alter table tmp_com_cells add index grid_id_index(grid_id);

create temporary table com_jobs
 select 
	county_id,
	count(*) 
 from jobs a 
 inner join tmp_com_cells b 
  on a.grid_id = b.grid_id
 group by county_id;

#Create industrial jobs
create temporary table tmp_ind_cells
 select 
	county_id,
	grid_id,
	industrial_sqft
 from center_cells 
 where industrial_sqft > 0 and
 governmental_sqft = 0
 and commercial_sqft = 0;
 
alter table tmp_ind_cells add index grid_id_index(grid_id);

create temporary table ind_jobs
 select 
 	county_id,
 	count(*) as jobs 
 from jobs a 
 inner join tmp_ind_cells b 
  on a.grid_id = b.grid_id
 group by county_id;
 
#Create government jobs
create temporary table tmp_gov_cells
 select 
 	county_id,
	grid_id,
	governmental_sqft
 from center_cells
 where governmental_sqft > 0 and
 industrial_sqft = 0
 and commercial_sqft = 0;
 
alter table tmp_gov_cells add index grid_id_index(grid_id);

create temporary table gov_jobs
 select 
 	county_id,
 	count(*) as jobs
 from jobs a 
 inner join tmp_gov_cells b 
  on a.grid_id = b.grid_id
 group by county_id;
 
## Update centers_summary table with results from temporary queries ##
# update sqft values
update centers_summary a 
 inner join tmp_com_sqft b
  on a.county_id = b.county_id
 set a.com_sqft = b.sqft;

update centers_summary a 
 inner join tmp_ind_sqft b
  on a.county_id = b.county_id
 set a.ind_sqft = b.sqft;

update centers_summary a 
 inner join tmp_gov_sqft b
  on a.county_id = b.county_id
 set a.gov_sqft = b.sqft;

# update jobs values
update centers_summary a 
 inner join com_jobs b 
  on a.county_id = b.county_id
 set a.com_jobs = b.jobs;
 
update centers_summary a 
 inner join ind_jobs b 
  on a.county_id = b.county_id
 set a.ind_jobs = b.jobs;
 
update centers_summary a 
 inner join gov_jobs b 
  on a.county_id = b.county_id
 set a.gov_jobs = b.jobs;
 
# update employee sqft ratios #
update centers_summary 
 set com_emp_sqft_ratio = com_sqft / com_jobs, 
     ind_emp_sqft_ratio = ind_sqft / ind_jobs,
     gov_emp_sqft_ratio = gov_sqft / gov_jobs;
     
### Create table that contains cells outside of urban centers ###
create table centers_out_summary 
 (county_id int, 
  com_sqft int,
  ind_sqft int, 
  gov_sqft int,
  com_jobs int,
  ind_jobs int,
  gov_jobs int,
  com_emp_sqft_ratio double,
  ind_emp_sqft_ratio double,
  gov_emp_sqft_ratio double);

insert into centers_out_summary (county_id) select distinct county_id from gridcells;

create temporary table centers_out
 select 
 	county_id,
 	grid_id,
 	commercial_sqft, 
 	governmental_sqft,
 	industrial_sqft
 from gridcells;
  
delete centers from centers_out centers, urbcen_short g
 where centers.grid_id = g.grid_id;
 
alter table prelim_centers_out add index grid_id_index(grid_id);	

create temporary table tmp_com_sqft_out
 select	
 	county_id, 
 	sum(commercial_sqft) as com_sqft
 from centers_out
 where commercial_sqft > 0 
  and governmental_sqft = 0
  and industrial_sqft = 0
 group by county_id;

create temporary table tmp_ind_sqft_out
 select 
 	county_id,
 	sum(industrial_sqft) as sqft 
 from centers_out
 where industrial_sqft > 0 
  and commercial_sqft = 0
  and governmental_sqft = 0
 group by county_id;

create temporary table tmp_gov_sqft_out
 select 
 	county_id,
 	sum(governmental_sqft) as sqft 
 from centers_out
 where governmental_sqft > 0 
  and commercial_sqft = 0
  and industrial_sqft = 0
 group by county_id;

#Create commercial jobs
create temporary table tmp_com_cells_out
 select 
	county_id,
	grid_id,
	commercial_sqft
 from centers_out
 where commercial_sqft > 0 and
 governmental_sqft = 0
 and industrial_sqft = 0;
 
alter table tmp_com_cells_out add index grid_id_index(grid_id);

create temporary table com_jobs_out
 select 
	county_id,
	count(*) as jobs
 from jobs a 
 inner join tmp_com_cells_out b 
  on a.grid_id = b.grid_id
 group by county_id;

#Create industrial jobs 
create temporary table tmp_ind_cells_out
 select
 	county_id,
 	grid_id,
 	industrial_sqft
 from centers_out
 where industrial_sqft > 0 
  and governmental_sqft = 0
  and commercial_sqft = 0;

alter table tmp_ind_cells_out add index grid_id_index(grid_id);

create temporary table ind_jobs_out
 select 
 	county_id,
 	count(*) as jobs
 from jobs a 
 inner join tmp_ind_cells_out b 
  on a.grid_id = b.grid_id 
 group by county_id;
 
# Create government jobs
create temporary table tmp_gov_cells_out
 select 
 	county_id,
 	grid_id,
 	governmental_sqft
 from centers_out
 where governmental_sqft > 0 
  and commercial_sqft = 0
  and industrial_sqft = 0;
 
alter table tmp_gov_cells_out add index grid_id_index(grid_id);

create temporary table gov_jobs_out
 select
 	county_id,
 	count(*) as jobs
 from jobs a 
 inner join tmp_gov_cells_out b
  on a.grid_id = b.grid_id
 group by county_id;
 
## Update centers_out_summary ##
# update sqft fields
update centers_out_summary a
 inner join tmp_com_sqft_out b 
  on a.county_id = b.county_id
 set a.com_sqft = b.sqft;

update centers_out_summary a 
 inner join tmp_ind_sqft_out b 
  on a.county_id = b.county_id
 set a.ind_sqft = b.sqft;
 
update centers_out_summary a 
 inner join tmp_gov_sqft_out b 
  on a.county_id = b.county_id
 set a.gov_sqft = b.sqft;

# update job fields
update centers_out_summary a
 inner join com_jobs_out b 
  on a.county_id = b.county_id
 set a.com_jobs = b.jobs;

update centers_out_summary a
 inner join ind_jobs_out b 
  on a.county_id = b.county_id
 set a.ind_jobs = b.jobs;

update centers_out_summary a
 inner join gov_jobs_out b 
  on a.county_id = b.county_id
 set a.gov_jobs = b.jobs;
 
## Update sqft per employee fields ##
update centers_out_summary 
 set com_emp_sqft_ratio = com_sqft / com_jobs, 
     ind_emp_sqft_ratio = ind_sqft / ind_jobs,
     gov_emp_sqft_ratio = gov_sqft / gov_jobs;

##########################################################
## Create summary table for cells in Industrial Centers ##

# Create table industrial_summary
create table industrial_summary
(county_id int, 
  com_sqft int,
  ind_sqft int, 
  gov_sqft int,
  com_jobs int,
  ind_jobs int,
  gov_jobs int,
  com_emp_sqft_ratio double,
  ind_emp_sqft_ratio double,
  gov_emp_sqft_ratio double);
  
insert into industrial_summary (county_id) select distinct county_id from gridcells;

create temporary table industrial_centers
 select 
 	b.county_id,
 	a.grid_id,
 	b.commercial_sqft,
 	b.governmental_sqft,
 	b.industrial_sqft
 from micen_short a 
 inner join gridcells b
  on a.grid_id = b.grid_id;

alter table industrial_centers add index grid_id_index(grid_id); 	

create temporary table micen_com_sqft
 select	
 	county_id, 
 	sum(commercial_sqft) as com_sqft
 from industrial_centers
 where commercial_sqft > 0 
  and governmental_sqft = 0
  and industrial_sqft = 0
 group by county_id;

create temporary table micen_ind_sqft
 select 
 	county_id,
 	sum(industrial_sqft) as sqft 
 from industrial_centers
 where industrial_sqft > 0 
  and commercial_sqft = 0
  and governmental_sqft = 0
 group by county_id;

create temporary table micen_gov_sqft
 select 
 	county_id,
 	sum(governmental_sqft) as sqft 
 from industrial_centers
 where governmental_sqft > 0 
  and commercial_sqft = 0
  and industrial_sqft = 0
 group by county_id;

# Jobs in industrial centers
# Commercial jobs
create temporary table micen_com_cells
 select 
	county_id,
	grid_id,
	commercial_sqft
 from industrial_centers
 where commercial_sqft > 0 and
 governmental_sqft = 0
 and industrial_sqft = 0;
 
alter table micen_com_cells_out add index grid_id_index(grid_id);

create temporary table micen_com_jobs
 select 
	county_id,
	count(*) as jobs
 from jobs a 
 inner join micen_com_cells b 
  on a.grid_id = b.grid_id
 group by county_id;

# Industrial jobs
create temporary table micen_ind_cells
 select 
	county_id,
	grid_id,
	industrial_sqft
 from industrial_centers
 where industrial_sqft > 0 and
 governmental_sqft = 0
 and commercial_sqft = 0;
 
alter table micen_ind_cells add index grid_id_index(grid_id);

create temporary table micen_ind_jobs
 select 
	county_id,
	count(*) as jobs
 from jobs a 
 inner join micen_ind_cells b 
  on a.grid_id = b.grid_id
 group by county_id;
 
# Government Jobs
create temporary table micen_gov_cells
 select 
	county_id,
	grid_id,
	governmental_sqft
 from industrial_centers
 where governmental_sqft > 0 and
 industrial_sqft = 0
 and commercial_sqft = 0;
 
alter table micen_gov_cells add index grid_id_index(grid_id);

create temporary table micen_gov_jobs
 select 
	county_id,
	count(*) as jobs
 from jobs a 
 inner join micen_gov_cells b 
  on a.grid_id = b.grid_id
 group by county_id;
 
#### Update industrial summary table ####

# Sqft 
update industrial_summary a 
 inner join micen_com_sqft b
  on a.county_id = b.county_id
 set a.com_sqft = b.sqft;

update industrial_summary a 
 inner join micen_ind_sqft b
  on a.county_id = b.county_id
 set a.ind_sqft = b.sqft;

update industrial_summary a 
 inner join micen_gov_sqft b
  on a.county_id = b.county_id
 set a.gov_sqft = b.sqft;

# Update jobs 
update industrial_summary a 
 inner join micen_com_jobs b 
  on a.county_id = b.county_id
 set a.com_jobs = b.jobs;

update industrial_summary a 
 inner join micen_ind_jobs b 
  on a.county_id = b.county_id
 set a.ind_jobs = b.jobs;
 
update industrial_summary a 
 inner join micen_gov_jobs b 
  on a.county_id = b.county_id
 set a.gov_jobs = b.jobs;
 
## Update employee per sqft ratios ##
update industrial_summary 
 set com_emp_sqft_ratio = com_sqft / com_jobs,
     ind_emp_sqft_ratio = ind_sqft / ind_jobs,
     gov_emp_sqft_ratio = gov_sqft / gov_jobs;

###############################################################
## Create industrial sqft figures outside industrial centers ##
create table industrial_summary_out
(county_id int, 
  com_sqft int,
  ind_sqft int, 
  gov_sqft int,
  com_jobs int,
  ind_jobs int,
  gov_jobs int,
  com_emp_sqft_ratio double,
  ind_emp_sqft_ratio double,
  gov_emp_sqft_ratio double);
  
insert into industrial_summary_out (county_id) select distinct county_id from gridcells;

create temporary table industrial_out
 select 
 	county_id,
 	grid_id,
 	commercial_sqft, 
 	governmental_sqft,
 	industrial_sqft
 from gridcells;

delete industrial from industrial_out industrial, micen_short m
 where industrial.grid_id = m.grid_id;
 
alter table industrial_out add index grid_id_index(grid_id);	

create temporary table micen_com_sqft_out
 select	
 	county_id, 
 	sum(commercial_sqft) as sqft
 from industrial_out
 where commercial_sqft > 0 
  and governmental_sqft = 0
  and industrial_sqft = 0
 group by county_id;

create temporary table micen_ind_sqft_out
 select	
 	county_id, 
 	sum(industrial_sqft) as sqft
 from industrial_out
 where industrial_sqft > 0 
  and governmental_sqft = 0
  and commercial_sqft = 0
 group by county_id;
 
create temporary table micen_gov_sqft_out
 select	
 	county_id, 
 	sum(governmental_sqft) as sqft
 from industrial_out
 where governmental_sqft > 0 
  and industrial_sqft = 0
  and commercial_sqft = 0
 group by county_id;
 
# Jobs in industrial centers
# Commercial jobs
create temporary table micen_com_cells_out
 select 
	county_id,
	grid_id,
	commercial_sqft
 from industrial_out
 where commercial_sqft > 0 and
 governmental_sqft = 0
 and industrial_sqft = 0;
 
alter table micen_com_cells_out add index grid_id_index(grid_id);

create temporary table micen_com_jobs_out
 select 
	county_id,
	count(*) as jobs
 from jobs a 
 inner join micen_com_cells_out b 
  on a.grid_id = b.grid_id
 group by county_id;

# Industrial jobs
create temporary table micen_ind_cells_out
 select 
	county_id,
	grid_id,
	industrial_sqft
 from industrial_out
 where industrial_sqft > 0 and
 governmental_sqft = 0
 and commercial_sqft = 0;
 
alter table micen_ind_cells_out add index grid_id_index(grid_id);

create temporary table micen_ind_jobs_out
 select 
	county_id,
	count(*) as jobs
 from jobs a 
 inner join micen_ind_cells_out b 
  on a.grid_id = b.grid_id
 group by county_id;
 
# Governmental jobs 
create temporary table micen_gov_cells_out
 select 
	county_id,
	grid_id,
	governmental_sqft
 from industrial_out
 where governmental_sqft > 0 and
 industrial_sqft = 0
 and commercial_sqft = 0;
 
alter table micen_gov_cells_out add index grid_id_index(grid_id);

create temporary table micen_gov_jobs_out
 select 
	county_id,
	count(*) as jobs
 from jobs a 
 inner join micen_gov_cells_out b 
  on a.grid_id = b.grid_id
 group by county_id;

## update sqft industrial_summary_out 
# Sqft values
update industrial_summary_out a 
 inner join micen_com_sqft_out b
  on a.county_id = b.county_id
 set a.com_sqft = b.sqft;

update industrial_summary_out a 
 inner join micen_ind_sqft_out b
  on a.county_id = b.county_id
 set a.ind_sqft = b.sqft;

update industrial_summary_out a 
 inner join micen_gov_sqft_out b
  on a.county_id = b.county_id
 set a.gov_sqft = b.sqft; 
 
# Job values
update industrial_summary_out a 
 inner join micen_com_jobs_out b
  on a.county_id = b.county_id
 set a.com_jobs = b.jobs;

update industrial_summary_out a 
 inner join micen_ind_jobs_out b
  on a.county_id = b.county_id
 set a.ind_jobs = b.jobs;

update industrial_summary_out a 
 inner join micen_gov_jobs_out b
  on a.county_id = b.county_id
 set a.gov_jobs = b.jobs;

## Update employee per sqft fields ##
update industrial_summary_out 
 set com_emp_sqft_ratio = com_sqft / com_jobs,
     ind_emp_sqft_ratio = ind_sqft / ind_jobs,
     gov_emp_sqft_ratio = gov_sqft / gov_jobs;

drop table micen_com_jobs_out;
drop table micen_ind_jobs_out;
drop table micen_gov_jobs_out;
 
##############################################################
## Select records where PSRC_MATCHED and spot check records ##

create table psrc_matched_on_residential
 select 
 	a.employer_id,
 	a.decision,
 	a.parcel_id,
 	c.number_of_jobs,
 	c.prefix,
 	c.street_number,
 	c.street_name,
 	c.street_type,
 	c.suffix,
 	c.sector,
 	c.sic
 from final_employers_matched_to_parcels a 
 inner join parcels b
  on a.parcel_id = b.parcel_id
 inner join employers c 
  on a.employer_id = c.employer_id
 where decision = 'PSRC_MATCHED' 
  and land_use like '%Residential%';
 
#################################################
## Update GSPSRC_2000_baseyear_change_20050719 ##

# update gridcells_in_geography table with non zero values #

# Get FAZ and FAZ District id values
create table cells_with_zone_faz_fazdist_id
 select 
 	a.GRID_ID,
 	a.ZONE_ID, 
 	b.FAZ_ID,
 	c.FAZDISTRICT_ID
 from GSPSRC_2000_baseyear_flattened.gridcells a
 inner join GSPSRC_2000_baseyear_flattened.zones_in_faz b
  on a.zone_id = b.zone_id
 inner join GSPSRC_2000_baseyear_change_20050719.fazes c
  on b.faz_id = c.faz_id;
  
alter table cells_with_zone_faz_fazdist_id add index grid_id_index(grid_id);

update gridcells_in_geography a
 inner join cells_with_zone_faz_fazdist_id b
 on a.grid_id = b.grid_id 
set a.geography_id = b.faz_id 
 where a.geography_id = 0 and a.geography_type_id = 4;
  
update gridcells_in_geography a
 inner join cells_with_zone_faz_fazdist_id b
 on a.grid_id = b.grid_id 
set a.geography_id = b.fazdistrict_id 
 where a.geography_id = 0 and a.geography_type_id= 7;
 
# Get county id values 

create table grid_id_faz_id_county_id
 select
 	a.GRID_ID,
 	b.ZONE_ID,
 	c.COUNTY_INT
 from GSPSRC_2000_baseyear_flattened.gridcells a
 inner join GSPSRC_2000_baseyear_flattened.zones_in_faz b
  on a.zone_id = b.zone_id 
 inner join PSRC_2000_reclassification_tables.county_faz c
  on b.faz_id = c.faz;

alter table grid_id_faz_id_county_id add index grid_id_index(grid_id);

update gridcells_in_geography a 
 inner join grid_id_faz_id_county_id b 
  on a.grid_id = b.grid_id
set a.geography_id = b.county_int 
 where a.geography_type_id= 5 and geography_id = 0;

######################################################################
## Update travel_data table in GSPSRC_2000_baseyear_change_20050804 ## 

# Because there are positive logsum values, will need to subtract the maximum
#  logsum value from all the logsums in the travel_data table

# Check for max logsum value 
select max(logsum0), max(logsum1), max(logsum2) from travel_data;

+--------------+--------------+--------------+
| max(logsum0) | max(logsum1) | max(logsum2) |
+--------------+--------------+--------------+
|       0.6893 |     -0.62855 |       0.5813 |
+--------------+--------------+--------------+

update travel_data set 
	logsum0 = logsum0 - 0.6893, 
	logsum1 = logsum - 0.6893, 
	logsum2 = logsum2 - 0.6893;

# The result of this query should shift all logsum values <= 0

create table y 
select a.* from p a 
 inner join r b 
  on a.from_zone_id = b.from_zone_id 
 where a.logsum0 <> b.logsum0 
  or a.logsum1 <> b.logsum1 
  or a.logsum2 <> b.logsum2;
 

#################################################################
## create test database for Proprietor Distributor Perl script ##
##  Subset records from king county 

# Use proprietor_distributor_king_test (derived from PSRC_proprietor_distributor_king
create table PARCELS_NEW select * from PARCELS
 where job_count between 10 and 50;

update PARCELS_NEW set job_count = 0;

alter table PARCELS_NEW add index cnty_prcl_id_index(county(3), parcel_id(10));
alter table PARCELS_NEW add index lu_fg_index(generic_land_use_1(10), faz_group);
alter table PARCELS_NEW add index blk_index(census_block);
alter table PARCELS_NEW add index zone_index(zone);
alter table PARCELS_NEW add index lu_2_index(generic_land_use_2(3));
alter table PARCELS_NEW add index prcl_index(parcel_id);

create table parcel_fractions_in_gridcells_new
select b.* from PARCELS_NEW a left join parcel_fractions_in_gridcells1 b 
 on a.parcel_id = b.parcel_id;
 
alter table parcel_fractions_in_gridcells_new add index prcl_index(parcel_id(10));
alter table parcel_fractions_in_gridcells_new add index prcl_cnty_index(parcel_id(10), county(3));

create table BUILDINGS_NEW 
select b.* from PARCELS_NEW a left join BUILDINGS b
 on a.parcel_id = b.parcel_id;

alter table BUILDINGS_NEW add index prcl_index(parcel_id(10));
alter table BUILDINGS_NEW add index cnty_prcl_index(county(3), parcel_id(10));

update JOBS_PER_COUNTY set total_county_jobs = (total_county_jobs * .25);

drop table PARCELS;
drop table parcel_fractions_in_gridcells;
drop table BUILDINGS;


alter table PARCELS_NEW rename as PARCELS;
alter table parcel_fractions_in_gridcells_new rename as parcel_fractions_in_gridcells;
alter table BUILDINGS_NEW rename as BUILDINGS;


/* Run Perl Script
(echo proprietor_distributor_king_test | perl -w /projects/urbansim7/scripts/private/cpeak/proprietors_distributor/proprietors_distributor.pl > /projects/null/urbansim4/users/petecaba/pd_king1.out) >& /projects/null/urbansim4/users/petecaba/pd_king1.err &
*/

#############################################################################################
## Update JOB_PROPORTIONS_BY_SECTOR table to reclassify non-home-based and home-based jobs ##

# created temporary database proprietor_distributor_kitsap_test 
#  select * from PSRC_proprietor_distributor_kitsap
# create on urbansim8 and symbolic link onto urbansim6

use proprietor_distributor_kitsap_test;

alter table JOBS_PER_COUNTY add column WS_JA int;

update JOBS_PER_COUNTY set WS_JA = WAGESAL_TOTALS - ALLOCATED_JOBS;

update JOBS_PER_COUNTY set WS_JA = 0 where WS_JA < 0;

#King County only: update JOBS_PER_COUNTY set total_county_jobs = (WS_JA + PROPRIETORS_JOBS);

update JOB_PROPORTIONS_BY_SECTOR 
 set PROPORTION_OF_JOBS_NONHOMEBASED = 0, PROPORTION_OF_JOBS_HOMEBASED = 0;

# Non-home-based Proportions
update JOB_PROPORTIONS_BY_SECTOR a 
 inner join JOBS_PER_COUNTY b
  on a.county = b.county and a.sector = b.sector
set a.PROPORTION_OF_JOBS_NONHOMEBASED = (b.WS_JA/b.TOTAL_COUNTY_JOBS);

# Home-based Proportions
update JOB_PROPORTIONS_BY_SECTOR a 
 inner join JOBS_PER_COUNTY b 
  on a.county = b.county and a.sector = b.sector 
set PROPORTION_OF_JOBS_HOMEBASED = (1-PROPORTION_OF_JOBS_NONHOMEBASED);
 
update JOB_PROPORTIONS_BY_SECTOR a 
 inner join JOBS_PER_COUNTY b 
  on a.county = b.county and a.sector = b.sector
 set a.PROPORTION_OF_JOBS_HOMEBASED = 0, a.PROPORTION_OF_JOBS_NONHOMEBASED = 0
where b.PROPRIETORS_JOBS = 0 and b.WS_JA = 0;

\. /projects/urbansim7/scripts/private/cpeak/proprietors_distributor/get_jobs_per_zone.sql
 
/*
update JOB_PROPORTIONS_BY_SECTOR a 
 inner join JOBS_PER_COUNTY b 
  on a.county = b.county and a.sector = b.sector
 set PROPORTION_OF_JOBS_HOMEBASED = 0 
where b.PROPRIETORS_JOBS = 0 and PROPORTION_OF_JOBS_HOMEBASED = 0;


update JOB_PROPORTIONS_BY_SECTOR a
 inner join JOBS_PER_COUNTY b 
  on a.county = b.county and a.sector = b.sector
 set PROPORTION_OF_JOBS_NONHOMEBASED = 1
where b.JOB_ALLOCATOR_LEFTOVERS > b.TOTAL_COUNTY_JOBS 
 and PROPRIETORS_JOBS = 0;
*/

# Kitsap County
#update JOB_PROPORTIONS_BY_SECTOR set PROPORTION_OF_JOBS_HOMEBASED = 1 where sector in (4, 5, 8, 11);
# King County
#update JOB_PROPORTIONS_BY_SECTOR set PROPORTION_OF_JOBS_HOMEBASED = 1 where sector in (4, 5, 8, 11);

create table jobs_test
 (JOB_ID INT AUTO_INCREMENT PRIMARY KEY,
  GRID_ID INT,
  SECTOR_ID INT,
  HOME_BASED TINYINT(4),
  SIC INT,
  BUILDING_TYPE VARCHAR(5),
  IMPUTE_FLAG TINYINT(4));

  
insert into jobs_test (GRID_ID, SECTOR_ID, HOME_BASED, SIC, BUILDING_TYPE, IMPUTE_FLAG)
 select grid_id, sector_id, home_based, sic, building_type, impute_flag 
 from job_allocation_king.jobs_final;
 
insert into jobs (GRID_ID, SECTOR_ID, HOME_BASED)
 select grid_id, sector, home_based
 from proprietor_distributor_king_test.JOBS_ROUNDED;
 
insert into jobs_test (GRID_ID, SECTOR_ID, HOME_BASED, SIC, BUILDING_TYPE, IMPUTE_FLAG)
 select grid_id, sector_id, home_based, sic, building_type, impute_flag 
 from job_allocation_kitsap.jobs_final;
 
insert into jobs (GRID_ID, SECTOR_ID, HOME_BASED)
 select grid_id, sector, home_based
 from proprietors_distributor_kitsap_test.JOBS_ROUNDED;
 
insert into jobs_test (GRID_ID, SECTOR_ID, HOME_BASED, SIC, BUILDING_TYPE, IMPUTE_FLAG)
 select grid_id, sector_id, home_based, sic, building_type, impute_flag 
 from job_allocation_pierce.jobs_final;
 
insert into jobs (GRID_ID, SECTOR_ID, HOME_BASED)
 select grid_id, sector, home_based
 from proprietors_distributor_pierce_test.JOBS_ROUNDED;
 
insert into jobs_test (GRID_ID, SECTOR_ID, HOME_BASED, SIC, BUILDING_TYPE, IMPUTE_FLAG)
 select grid_id, sector_id, home_based, sic, building_type, impute_flag 
 from job_allocation_snohomish.jobs_final;
 
insert into jobs (GRID_ID, SECTOR_ID, HOME_BASED)
 select grid_id, sector, home_based
 from proprietors_distributor_snohomish_test.JOBS_ROUNDED; 
 
INSERT INTO jobs_test (GRID_ID, SECTOR_ID, HOME_BASED, SIC, BUILDING_TYPE, IMPUTE_FLAG)
SELECT GRID_ID, SECTOR_ID, HOME_BASED, SIC, BUILDING_TYPE, IMPUTE_FLAG
FROM PSRC_2000_baseyear_updates_for_reestimation.jobs_pie_military_reclassified;
 
INSERT INTO jobs_test (GRID_ID, SECTOR_ID, HOME_BASED, SIC, BUILDING_TYPE, IMPUTE_FLAG)
SELECT GRID_ID, SECTOR_ID, HOME_BASED, SIC, BUILDING_TYPE, IMPUTE_FLAG
FROM PSRC_2000_baseyear_updates_for_reestimation.jobs_enlisted_military;


############################################################
## Select employment records that were matched to parcels ##

drop table if exists tmp_emp_matched_to_prcl;
create temporary table tmp_emp_matched_to_prcl
select 
	a.employer_id,
	b.parcel_id,
	b.land_use,
	b.use_code,
	b.square_footage as prcl_sqft,
	d.generic_land_use_1, 
	d.generic_land_use_2,
	a.county,
	c.number_of_jobs,
	c.sector
from final_employers_matched_to_parcels a 
inner join parcels b 
 on a.parcel_id = b.parcel_id
inner join employers c 
 on a.employer_id = c.employer_id
inner join PSRC_2000_reclassification_tables.land_use_generic_reclass d
 on b.county = d.county and b.use_code = d.county_land_use_code
where a.decision = 'PSRC_MATCHED';

alter table tmp_emp_matched_to_prcl add index prcl_id_index(parcel_id(10));
alter table tmp_emp_matched_to_prcl add column built_sqft double;

## Change county name ##
drop table if exists tmp_buildings
create temporary table tmp_buildings
select 
	parcel_id,
	sum(imputed_sqft) as built_sqft
from PSRC_parcels_king.buildings
group by parcel_id;

alter table tmp_buildings add index prcl_id_index(parcel_id(10));

update tmp_emp_matched_to_prcl a 
inner join tmp_buildings b 
 on a.parcel_id= b.parcel_id
set a.built_sqft = b.built_sqft;

## Create mean sqft per job ratios ##
alter table tmp_emp_matched_to_prcl add column mean_sqft_per_job double;

update tmp_emp_matched_to_prcl 
set mean_sqft_per_job = built_sqft/number_of_jobs;


## Group records into C, G, and I land use types ##
# Create table containng C, G, and I use types
drop table if exists tmp_summary_lu;
create temporary table tmp_summary_lu
(generic_land_use_2 varchar(50),
 prcl_sqft double,
 built_sqft double,
 jobs double);

# Commercial
drop table if exists tmp_commercial_parcels;
insert into tmp_summary_lu 
	(generic_land_use_2, 
	 prcl_sqft,
	 built_sqft,
	 jobs)
select 
	generic_land_use_2 as generic_land_use_2,
	sum(prcl_sqft) as prcl_sqft,
	sum(built_sqft) as built_sqft,
	sum(number_of_jobs) as jobs
from tmp_emp_matched_to_prcl
where generic_land_use_2 = 'C'
group by generic_land_use_2;

# Industrial
insert into tmp_summary_lu 
	(generic_land_use_2, 
	 prcl_sqft,
	 built_sqft,
	 jobs)
select 
	generic_land_use_2,
	sum(prcl_sqft) as prcl_sqft,
	sum(built_sqft) as built_sqft,
	sum(number_of_jobs) as jobs
from tmp_emp_matched_to_prcl
where generic_land_use_2 = 'I'
group by generic_land_use_2;

# Governmental
insert into tmp_summary_lu 
	(generic_land_use_2, 
	 prcl_sqft,
	 built_sqft,
	 jobs)
select 
	generic_land_use_2,
	sum(prcl_sqft) as prcl_sqft,
	sum(built_sqft) as built_sqft,
	sum(number_of_jobs) as jobs
from tmp_emp_matched_to_prcl
where generic_land_use_2 = 'G'
group by generic_land_use_2;

###############################################################################################
## Get records that UrbanSim (Kapena manually geocoded to parcel in job allocation databases ##

create table usim_matched_employers
select a.* 
from employers a
inner join final_employers_matched_to_parcels b 
on a.employer_id = b.employer_id 
where b.decision in ('URBANSIM_MANUAL_MATCHED');

####################################################################################################
## Find records where disconnect of building use and land use records are found in gridcells table ##

## Commercial improvement value, but no commercial sqft values ##
drop table if exists com_impvl_no_sqft;
create table com_impvl_no_sqft
select 
	grid_id,
	commercial_sqft as com_sqft,
	industrial_sqft as ind_sqft,
	governmental_sqft as gov_sqft,
	commercial_improvement_value as com_impvl,
	industrial_improvement_value as ind_impvl,
	governmental_improvement_value as gov_impvl
from gridcells
where commercial_sqft = 0 
 and governmental_sqft = 0 
 and industrial_sqft = 0
 and commercial_improvement_value > 0;
 
## Commerical sqft values, but no commercial improvement values ##
drop table if exists com_sqft_no_impvl;
create table com_sqft_no_impvl
select
	grid_id,
	commercial_sqft as com_sqft,
	industrial_sqft as ind_sqft,
	governmental_sqft as gov_sqft,
	commercial_improvement_value as com_impvl,
	industrial_improvement_value as ind_impvl,
	governmental_improvement_value as gov_impvl
from gridcells
where commercial_sqft > 0
 and governmental_sqft = 0
 and industrial_sqft = 0
 and commercial_improvement_value = 0;
	
## Industrial improvement value, but no industrial sqft values ##
drop table if exists ind_impvl_no_sqft;
create table ind_impvl_no_sqft
select
	grid_id,
	commercial_sqft as com_sqft,
	industrial_sqft as ind_sqft,
	governmental_sqft as gov_sqft,
	industrial_improvement_value as ind_impvl,
	commercial_improvement_value as com_impvl,
	governmental_improvement_value as gov_impvl
from gridcells
where industrial_sqft = 0
 and governmental_sqft = 0
 and commercial_sqft = 0
 and industrial_improvement_value > 0;

## Industrial sqft value, but no industrial improvement values ##
drop table if exists ind_sqft_no_impvl;
create table ind_sqft_no_impvl
select 
	grid_id,
	commercial_sqft as com_sqft,
	industrial_sqft as ind_sqft,
	governmental_sqft as gov_sqft,
	industrial_improvement_value as ind_implv,
	commercial_improvement_value as com_impvl,
	governmental_improvement_value as gov_impvl
from gridcells 
where industrial_sqft > 0
 and commercial_sqft = 0
 and governmental_sqft = 0
 and industrial_improvement_value = 0;


############################################################################
## Determine how many jobs that are prefer building type c, but no c sqft ##

## find commercial building type jobs where com_sqft is null and impute to largest sqft value in gridcells ##
drop table if exists tmp_com_no_sqft;
create temporary table tmp_com_no_sqft
select a.* from jobs a
left join gridcells b on a.grid_id = b.grid_id
where a.building_type = 'C' and b.commercial_sqft = 0;

alter table tmp_com_no_sqft add index job_id_index(job_id);
alter table tmp_com_no_sqft add index grid_id_index(grid_id);

## Determine largest/existing land use with sqft in cell ##
drop table if exists tmp_max_use_1;
create temporary table tmp_max_use_1
 select 
  	a.grid_id,
  	a.job_id,
  	b.commercial_sqft, 
  	b.governmental_sqft,
  	b.industrial_sqft
 from tmp_com_no_sqft a
  left join gridcells b
   on a.grid_id = b.grid_id;

alter table tmp_max_use_1 add column max_use text;

drop table if exists tmp_max_use;
create temporary table tmp_max_use
 select 
 	grid_id, 
 	job_id,
 	commercial_sqft,
 	governmental_sqft,
 	industrial_sqft,
 	if(industrial_sqft > 
 	if(commercial_sqft > governmental_sqft, commercial_sqft, governmental_sqft), industrial_sqft, 
 	if(commercial_sqft > governmental_sqft, commercial_sqft, governmental_sqft)) as max_sqft
 from tmp_max_use_1 
 group by 
 	grid_id,
 	job_id;

alter table tmp_max_use add column building_type varchar(5);

update tmp_max_use set building_type = 'I' where max_sqft = industrial_sqft and industrial_sqft > 0;
update tmp_max_use set building_type = 'C' where max_sqft = commercial_sqft and commercial_sqft > 0;
update tmp_max_use set building_type = 'G' where max_sqft = governmental_sqft and governmental_sqft > 0;

alter table jobs add index job_id_index(job_id);
alter table tmp_max_use add index job_id_index(job_id);

update jobs a
inner join tmp_max_use b on a.job_id = b.job_id
set a.building_type = b.building_type 
where b.building_type is not null
and a.home_based = 0;


## Repeat process above for industrial building type jobs ##

drop table if exists tmp_ind_no_sqft;
create temporary table tmp_ind_no_sqft
select a.* from jobs a
left join gridcells b on a.grid_id = b.grid_id
where a.building_type = 'I' and b.industrial_sqft = 0;

alter table tmp_ind_no_sqft add index job_id_index(job_id);
alter table tmp_ind_no_sqft add index grid_id_index(grid_id);

## Determine largest/existing land use with sqft in cell ##
drop table if exists tmp_max_use_2;
create temporary table tmp_max_use_2
 select 
  	a.grid_id,
  	a.job_id,
  	b.commercial_sqft, 
  	b.governmental_sqft,
  	b.industrial_sqft
 from tmp_ind_no_sqft a
  left join gridcells b
   on a.grid_id = b.grid_id;

alter table tmp_max_use_2 add column max_use text;

drop table if exists tmp_max_use2;
create temporary table tmp_max_use2
 select 
 	grid_id, 
 	job_id,
 	commercial_sqft,
 	governmental_sqft,
 	industrial_sqft,
 	if(industrial_sqft > 
 	if(commercial_sqft > governmental_sqft, commercial_sqft, governmental_sqft), industrial_sqft, 
 	if(commercial_sqft > governmental_sqft, commercial_sqft, governmental_sqft)) as max_sqft
 from tmp_max_use_2
 group by 
 	grid_id,
 	job_id;

alter table tmp_max_use2 add column building_type varchar(5);

#update tmp_max_use2 set building_type = 'I' where max_sqft = industrial_sqft and industrial_sqft > 0;
update tmp_max_use2 set building_type = 'C' where max_sqft = commercial_sqft and commercial_sqft > 0;
update tmp_max_use2 set building_type = 'G' where max_sqft = governmental_sqft and governmental_sqft > 0;
#update tmp_max_use2 set building_type = 'C' where max_sqft = 0;

alter table jobs add index job_id_index(job_id);
alter table tmp_max_use2 add index job_id_index(job_id);

update jobs a
inner join tmp_max_use2 b on a.job_id = b.job_id
set a.building_type = b.building_type 
where b.building_type is not null
and a.home_based = 0;

## at this point update commerical and industrial sqft per job columns ##
# Run parce of script from assign_building_type_to_jobs.sql 
# that calculates ratios



## Determine what gridcells need to have their ratios imputed using 500 sqft ##
# Commercial cells
drop table if exists tmp_cells_com_500sqft;
create temporary table tmp_cells_com_500sqft (grid_id int, com_sqft_per_job double);

insert into tmp_cells_com_500sqft (grid_id)
select 
	a.grid_id
from jobs a left join gridcells b 
on a.grid_id= b.grid_id
where a.building_type = 'C' and b.commercial_sqft = 0
group by a.grid_id;

update tmp_cells_com_500sqft set com_sqft_per_job = 500;

alter table tmp_cells_com_500sqft add index grid_id_index(grid_id);

update gridcells a 
inner join tmp_cells_com_500sqft b 
 on a.grid_id = b.grid_id 
set a.commercial_sqft_per_job = b.com_sqft_per_job
where a.commercial_sqft_per_job = 0;

# Industrial cells
drop table if exists tmp_cells_ind_1000sqft;
create temporary table tmp_cells_ind_1000sqft (grid_id int, ind_sqft_per_job double);

insert into tmp_cells_ind_1000sqft (grid_id)
select 
	a.grid_id
from jobs a left join gridcells b 
on a.grid_id= b.grid_id
where a.building_type = 'I' and b.industrial_sqft = 0
group by a.grid_id;

update tmp_cells_ind_1000sqft set ind_sqft_per_job = 1000;

alter table tmp_cells_ind_1000sqft add index grid_id_index(grid_id);

update gridcells a 
inner join tmp_cells_ind_1000sqft b 
 on a.grid_id = b.grid_id 
set a.industrial_sqft_per_job = b.ind_sqft_per_job
where a.industrial_sqft_per_job = 0; 


####
drop table if exists prelim_job_space;
create temporary table prelim_job_space
select
	a.grid_id, 
	a.building_type,
	count(*) as jobs
from jobs a
group by 
	a.grid_id,
	a.building_type;

alter table prelim_job_space add index grid_id_index(grid_id);

create temporary table jobs_com_no_sqft	
select sum(jobs)
from prelim_job_space a 
inner join gridcells b on a.grid_id = b.grid_id
where b.commercial_sqft = 0 and a.building_type = 'C';

/*Get results for commercial
Commercial
25,089 commercial building type jobs
1,322,615 total jobs
*/

/*Get results for industrial
Industrial
1743  industrial building type jobs
202,232
*/

################################################ 
## select jobs in lowest employment quartile  ##

## Be sure to switch table names when creating 1995 tables ##

create table prelim_kit_low_quartile
select  
	ACCTSER,
	PRIMNAME,
	DESC_,
	MONTH3,
	NAICS,
	X_COORD,
	Y_COORD
from kitsap03 
where left(naics,3) 
in (211,482,814,722,111,447,451,713,512,491,448,721,624,115,453,812,485,623,452,112,315);

SELECT king03.PSRCID, king03.PRIMNAME, kings03.TOTWAGES, king03.month3, king03.NAICS, king03.X_COORD, king03.Y_COORD INTO total_employment_lower_quartile_2003_revised
FROM king03
WHERE (((Left([naics],3)) In (211,482,814,722,111,447,451,713,512,491,448,721,624,115,453,812,485,623,452,112,315,445)));

## 1995 Emp data from ESD ##
# 1. Append 1995_1st_naics and 1995_2nd_naics tables together 
# 2. Calculate average employment wage
# 3. Select records from appended table containing the above mentioned naics codes

select  
	PRIMNAME,
	JOB95,
	NAICS,
	TOTWAGES,
	X_COORD,
	Y_COORD
from kit95;


#############

create temporary table tmp_jobs_stats (grid_id int, ratio double, cell_count int);

insert into tmp_jobs_stats (grid_id, ratio, cell_count)
select 
	a.grid_id,
	(a.total_nonres_sqft / b.jobs) as ratio,
	count(*) as cell_count
from gridcells a, tmp_jobs b 
where a.grid_id= b.grid_id
group by
	a.grid_id
order by ratio asc;

drop table if exists jobs_stats;
create temporary table jobs_stats 
(grouping int not null auto_increment, primary key (grouping), ratio text, cell_count int);

insert into jobs_stats (cell_count)
select count(*) as cell_count
from tmp_jobs_stats 
where ratio between 1 and 401;
	
## Recalculate sqft/emp ratios at the block group level 
##  using urbansim data

create table bg_ratio_summary 
(BLOCK_GROUP VARCHAR(20),COM_SQFT INT, IND_SQFT INT, COM_JOBS INT, IND_JOBS int, COM_RATIO DOUBLE, IND_RATIO DOUBLE);

# Gridcells info
insert into bg_ratio_summary (block_group, com_sqft, ind_sqft)
select
	c.BLOCK_GROUP as BLOCK_GROUP,
	SUM(a.COMMERCIAL_SQFT) AS COM_SQFT,
	SUM(a.INDUSTRIAL_SQFT) AS IND_SQFT
from gridcells a
inner join PSRC_2000_reclassification_tables.gridcell_block_mapping b
 on a.grid_id = b.grid_id
inner join PSRC_2000_reclassification_tables.census_block_mappings c
 on b.stfid = c.census_block
group by
	c.BLOCK_GROUP;

alter table bg_ratio_summary add index blk_grp (block_group(15));

# Jobs info	
create temporary table tmp_bg_job_summary
select
	c.BLOCK_GROUP as BLOCK_GROUP,
	count(*) as JOBS,
	a.BUILDING_TYPE
from jobs a 
inner join PSRC_2000_reclassification_tables.gridcell_block_mapping b
 on a.grid_id = b.grid_id
inner join PSRC_2000_reclassification_tables.census_block_mappings c 
 on b.stfid = c.census_block
group by
	c.BLOCK_GROUP,
	a.BUILDING_TYPE;

alter table tmp_bg_job_summary add index blck_grp(block_group(12));

# Update ratios in bg_summary table

update bg_ratio_summary a 
inner join tmp_bg_job_summary b 
on a.block_group = b.block_group
set a.COM_JOBS = JOBS
where b.BUILDING_TYPE = 'C';

update bg_ratio_summary a 
inner join tmp_bg_job_summary b 
on a.block_group = b.block_group
set a.IND_JOBS = JOBS
where b.BUILDING_TYPE = 'I';	

update bg_ratio_summary set com_ratio = com_sqft/com_jobs, ind_ratio = ind_sqft/ind_jobs;
	
 
/*
select
	count(*) as JOBS
from jobs a 
inner join PSRC_2000_reclassification_tables.gridcell_block_mapping b
 on a.grid_id = b.grid_id
inner join PSRC_2000_reclassification_tables.census_block_mappings c 
 on b.stfid = c.census_block
where c.block_group = '530330081002'
*/


####
drop table if exists zone_indicators;
Create table zone_indicators 
(ZONE_ID INT, 
 RESIDENTIAL_UNITS INT, 
 HOUSEHOLDS INT, 
 JOBS INT, 
 POPULATION INT, 
 COMMERCIAL_SQFT INT,
 INDUSTRIAL_SQFT INT,
 RESIDENTIAL_LAND_VALUE INT, 
 NONRESIDENTIAL_LAND_VALUE INT);
 
# Gridcell data
insert into zone_indicators
(zone_id, residential_units, commercial_sqft, industrial_sqft, residential_land_value, nonresidential_land_value)
select
a.zone_id,
sum(a.residential_units),
sum(a.commercial_sqft),
sum(a.industrial_sqft),
sum(a.residential_land_value),
sum(a.nonresidential_land_value)
from gridcells_exported a
group by a.zone_id;

# Job data
drop table if exists tmp_jobs_zones;
create temporary table tmp_jobs_zones
select 
b.zone_id,
count(*) as jobs
from jobs_exported a inner join gridcells_exported b on a.grid_id = b.grid_id
group by b.zone_id;

update zone_indicators a inner join tmp_jobs_zones b on a.zone_id = b.zone_id
set a.jobs = b.jobs;

drop table tmp_jobs_zones;

# Household data
drop table if exists tmp_households_zones;
create temporary table tmp_households_zones
select
b.zone_id,
count(*) as households,
sum(a.persons) as population
from households_exported a inner join gridcells_exported b on a.grid_id = b.grid_id
group by b.zone_id;

update zone_indicators a inner join tmp_households_zones b on a.zone_id = b.zone_id
set a.households = b.households, a.population = b.population;

drop table tmp_households_zones;

# TAZ to FAZ
drop table if exists faz_indicators;
create table faz_indicators
select
a.FAZ,
sum(b.residential_units) as RESIDENITAL_UNITS,
sum(b.households) as HOUSEHOLDS,
sum(b.jobs) as JOBS,
sum(b.POPULATION) as POPULATION,
sum(b.COMMERCIAL_SQFT) as COM_SQFT,
sum(b.industrial_sqft) as IND_SQFT,
sum(b.residential_land_value) as RES_LV,
sum(b.nonresidential_land_value) as NONRES_LV
from zone_indicators b inner join PSRC_2000_reclassification_tables.taz_to_faz a on a.taz_int = b.zone_id
group by a.FAZ;


#### January 18, 2006 ####
## Check if commercial or industrial jobs has enough allowable sqft in gridcell ##
drop table tmp_jobs;
create temporary table tmp_jobs
select grid_id, building_type, count(*) as jobs from jobs
group by grid_id, building_type;

alter table tmp_jobs add index grid_id_index(grid_id);
alter table tmp_jobs add column com_sqft double;
alter table tmp_jobs add column ind_sqft double;

update tmp_jobs 
set com_sqft = (jobs * 550)
where building_type = 'C';

update tmp_jobs
set ind_sqft = (jobs * 1100)
where building_type = 'I';


