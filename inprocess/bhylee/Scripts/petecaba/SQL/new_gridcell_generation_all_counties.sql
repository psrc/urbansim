#
#  UrbanSim software.
#  Copyright (C) 1998-2003 University of Washington
#  
#  You can redistribute this program and/or modify it under the
#  terms of the GNU General Public License as published by the
#  Free Software Foundation (http://www.gnu.org/copyleft/gpl.html).
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  file LICENSE.htm for copyright and licensing information, and the
#  file ACKNOWLEDGMENTS.htm for funding and other acknowledgments.
#
#  Author: Liming Wang, modified by Chris Peak and Peter Caballero

###This script generate gridcell fields from parcels, parcel_fractions_in_gridcells, 
##and PSRC_2000_data_quality_indicators.land_use_generic_reclass table. Refer to wiki page:
##http://www.urbansim.org/projects/dataprep/tables/input_tables_parcel_to_grid.shtml
##Input: parcels,parcel_fractions_in_gridcells,PSRC_2000_data_quality_indicators.land_use_generic_reclass
##Output: gridcells table fields - GRID_ID, COMMERCIAL_SQFT, GOVERNMENTAL_SQFT, INDUSTRIAL_SQFT,
##        RESIDENTIAL_UNITS,LAND_VALUE,IMPROVEMENT_VALUE,YEAR_BUILT
##Run: in MySQL 

#USE peters_playhouse;

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
alter table parcels add index pin_cnty_indx (parcel_id(12), county(3));

# Add index (if it doesn't exist) to the parcel_id and county colunn on the buildings table
alter table buildings add index prcl_cnty_indx(parcel_id(12), county(3));

##insert GRID_ID from parcel_fractions_in_gridcells table.
insert into gridcells (GRID_ID)
select DISTINCT GRID_ID 
from parcel_fractions_in_gridcells;

# Run script to calculate COMMERCIAL_SQFT, GOVERNMENTAL_SQFT, INDUSTRIAL_SQFT, TOTAL_NONRES_SQFT
#  and YEAR_BUILT for gridcells based on building data.
\. /projects/urbansim7/scripts/public/psrc/data_prep/gridcell_generation_from_buildings.sql

set session big_tables = 1;

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
	OR c.generic_land_use_2 = 'G'  OR c.generic_land_use_2 = 'NR'
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

update gridcells, tmp_table6d
set gridcells.RESIDENTIAL_IMPROVEMENT_VALUE = tmp_table6d.RESIDENTIAL_IMPROVEMENT_VALUE
WHERE gridcells.GRID_ID = tmp_table6d.GRID_ID; 

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

# update gridcells, tmp_frac_res_land_1
# set gridcells.FRACTION_RESIDENTIAL_LAND = tmp_frac_res_land_1.frac_res
# WHERE gridcells.GRID_ID = tmp_frac_res_land_1.GRID_ID; 

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
 	F.FRAC_RES as FRACTION_RESIDENTIAL_LAND
 	FROM gridcells AS A
 	LEFT JOIN tmp_frac_res_land_1 AS F
	 ON A.GRID_ID = F.GRID_ID 
;

alter table gridcells_new add primary key grid_indx(grid_id);

#############
# Get residential units for gridcells in blocks that had no parcels 
# Get list of blocks BG for which unit imputation failed
 
DROP TABLE IF EXISTS temp_imputed_units_by_block;
create temporary table temp_imputed_units_by_block
select CENSUS_BLOCK, sum(RESIDENTIAL_UNITS_IMPUTED) AS RES_UNITS
FROM parcels
GROUP BY CENSUS_BLOCK;

CREATE UNIQUE INDEX blockindex on temp_imputed_units_by_block (CENSUS_BLOCK(15));

DROP TABLE IF EXISTS census_block_imputed_unit_discrepancies;
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

DROP TABLE IF EXISTS unit_fractions;
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

DROP TABLE IF EXISTS census_units_summed;
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
DROP TABLE census_block_imputed_unit_discrepancies;
DROP TABLE unit_fractions;
DROP TABLE census_units_summed;