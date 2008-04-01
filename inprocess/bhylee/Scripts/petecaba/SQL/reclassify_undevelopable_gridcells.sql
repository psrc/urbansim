# PSRC 2000 baseyear database gridcells table PERCENT_PUBLIC_LAND

USE PSRC_2000_baseyear;

# The MPL_OWN is the owner field and the Major Public Lands file. 
# 01 - Federal Govt
# 02 - State Govt
# 03 - County Govt
# 04 - City Govt 
# 05 - Tribe
# 98 - Other
# 99 - Unknown

# The Percent Public Land can also be delineated by Land Manager and Management Type

CREATE TABLE percent_public 
 SELECT 
 GRID_CODE AS GRID_ID,
 SUM(AREA) AS PUBLIC_AREA
 FROM public_grid
 WHERE MPL_OWN <> '00' 
 OR MPL_OWN <> '99'
 GROUP BY GRID_CODE
;

ALTER TABLE percent_public ADD UNIQUE INDEX grid_indx (grid_id);
ALTER TABLE percent_public ADD COLUMN PERCENT_PUBLIC DOUBLE;

CREATE TEMPORARY TABLE tmp_grid_area
 SELECT 
 GRID_CODE AS GRID_ID,
 SUM(AREA) AS GRID_AREA
 FROM public_grid
 GROUP BY GRID_CODE
;

ALTER TABLE tmp_grid_area ADD UNIQUE INDEX grid_indx (grid_id);

UPDATE percent_public AS a 
 INNER JOIN tmp_grid_area AS b
 ON a.grid_id = b.grid_id
 SET a.PERCENT_PUBLIC = a.PUBLIC_AREA/b.GRID_AREA*100
; 

DELETE FROM percent_public WHERE GRID_ID = -9999;

DROP TABLE tmp_grid_area;

# Note - If 'table a is full' error occurs perform the following:
# create table percent_public_land select a.grid_id, a.public_area, a.public_area/b.grid_area * 100 as percent_public
# from percent_public as a inner join tmp_grid_area as b on a.grid_id = b.grid_id;
# alter table percent_public_land add unique index grid_indx (grid_id);

#########################################################################
#
# Kitsap County PERCENT_ROW table
#

USE PSRC_parcels_kitsap;

ALTER TABLE kitrow_grid ADD INDEX (pin(12));

CREATE TABLE percent_row
 SELECT 
 GRID_CODE AS GRID_ID,
 SUM(AREA) AS ROW_AREA
 FROM kitrow_grid
 WHERE SAPN like "ROW%"
 GROUP BY GRID_CODE
;

ALTER TABLE percent_row ADD UNIQUE INDEX grid_indx(grid_id);
ALTER TABLE percent_row ADD COLUMN PERCENT_ROW DOUBLE;

CREATE TEMPORARY TABLE tmp_grid_area 
 SELECT 
 GRID_CODE AS GRID_ID,
 SUM(AREA) AS GRID_AREA
 FROM kitrow_grid
 GROUP BY GRID_ID
;

ALTER TABLE tmp_grid_area ADD UNIQUE INDEX grid_indx(grid_id);

UPDATE percent_row AS a 
 INNER JOIN tmp_grid_area AS b
 ON a.GRID_ID = b.GRID_ID
 SET a.PERCENT_ROW = a.ROW_AREA/b.GRID_AREA*100
; 

# PERCENT_MINING

CREATE TABLE percent_mining
 SELECT 
 a.GRID_CODE AS GRID_ID, 
 SUM(a.AREA) AS MINING_AREA
 FROM kitrow_grid AS a
 INNER JOIN parcels AS b
 ON (a.pin = b.parcel_id)
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS c
 ON b.land_use = c.county_land_use_code and b.county = b.county
 WHERE c.generic_land_use_1 = "Mining"
 GROUP BY a.GRID_CODE
; 

ALTER TABLE percent_mining ADD UNIQUE INDEX grid_indx (grid_id);
ALTER TABLE percent_mining ADD COLUMN PERCENT_MINING DOUBLE;

UPDATE percent_mining AS a
 INNER JOIN tmp_grid_area AS b
 ON a.grid_id = b.grid_id
 SET a.percent_mining = a.mining_area/b.grid_area*100
;

# PERCENT_FOREST

CREATE TABLE percent_forest
 SELECT 
 GRID_CODE AS GRID_ID,
 SUM(a.AREA) AS FOREST_AREA
 FROM kitrow_grid AS a
 INNER JOIN parcels AS b 
 ON (a.pin = b.parcel_id)
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS c
 ON b.land_use = c.county_land_use_code and b.county = b.county
 WHERE c.generic_land_use_1 = "Forest - protected" 
 OR c.generic_land_use_1 = "Forest - harvestable"
 GROUP BY a.GRID_CODE
;

ALTER TABLE percent_forest ADD UNIQUE INDEX grid_indx(grid_id);
ALTER TABLE percent_forest ADD COLUMN PERCENT_FOREST DOUBLE;

UPDATE percent_forest AS a 
 INNER JOIN tmp_grid_area AS b
 ON a.GRID_ID = b.GRID_ID
 SET a.PERCENT_FOREST = a.FOREST_AREA/b.GRID_AREA*100
;

# PERCENT_AGRICULTURE

CREATE TABLE percent_agriculture
 SELECT 
 GRID_CODE AS GRID_ID,
 SUM(a.AREA) AS AGR_AREA
 FROM kitrow_grid AS a
 INNER JOIN parcels AS b 
 ON (a.pin = b.parcel_id)
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS c
 ON b.land_use = c.county_land_use_code and b.county = b.county
 WHERE c.generic_land_use_1 = "Agriculture" 
 GROUP BY a.GRID_CODE
;

ALTER TABLE percent_agriculture ADD UNIQUE INDEX grid_indx(grid_id);
ALTER TABLE percent_agriculture ADD COLUMN PERCENT_AGR DOUBLE;

UPDATE percent_agriculture AS a 
 INNER JOIN tmp_grid_area AS b
 ON a.GRID_ID = b.GRID_ID
 SET a.PERCENT_AGR = a.AGR_AREA/b.GRID_AREA*100
;


#DROP TABLE tmp_grid_area;

#####################################################################

# Pierce County PERCENT_ROW table

USE PSRC_parcels_pierce;

CREATE TABLE percent_row
 SELECT 
 GRID_ID,
 SUM(AREA) AS ROW_AREA
 FROM pierow_grid
 WHERE PARCEL_ID = 0
 GROUP BY GRID_ID
;

ALTER TABLE percent_row ADD UNIQUE INDEX grid_indx(grid_id);
ALTER TABLE percent_row ADD COLUMN GRID_AREA DOUBLE;

CREATE TEMPORARY TABLE tmp_grid_area 
 SELECT 
 GRID_ID,
 SUM(AREA) AS GRID_AREA
 FROM pierow_grid
 GROUP BY GRID_ID
;

ALTER TABLE tmp_grid_area ADD UNIQUE INDEX grid_indx(grid_id);
ALTER TABLE percent_row ADD COLUMN PERCENT_ROW DOUBLE;

UPDATE percent_row AS a 
 INNER JOIN tmp_grid_area AS b
 ON a.GRID_ID = b.GRID_ID
 SET a.PERCENT_ROW = a.ROW_AREA/b.GRID_AREA*100
; 

# PERCENT_MINING

CREATE TABLE percent_mining
 SELECT 
 a.GRID_ID, 
 SUM(a.AREA) AS MINING_AREA
 FROM pierow_grid AS a
 INNER JOIN parcels AS b
 ON (a.parcel_id = b.parcel_id)
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS c
 ON b.land_use = c.county_land_use_code and b.county = b.county
 WHERE c.generic_land_use_1 = "Mining"
 GROUP BY a.GRID_ID
; 

ALTER TABLE percent_mining ADD UNIQUE INDEX grid_indx (grid_id);
ALTER TABLE percent_mining ADD COLUMN PERCENT_MINING DOUBLE;

UPDATE percent_mining AS a
 INNER JOIN tmp_grid_area AS b
 ON a.grid_id = b.grid_id
 SET a.percent_mining = a.mining_area/b.grid_area*100
;

# PERCENT_FOREST

CREATE TABLE percent_forest
 SELECT 
 a.GRID_ID,
 SUM(a.AREA) AS FOREST_AREA
 FROM pierow_grid AS a
 INNER JOIN parcels AS b 
 ON (a.parcel_id = b.parcel_id)
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS c
 ON b.land_use = c.county_land_use_code and b.county = b.county
 WHERE c.generic_land_use_1 = "Forest - protected" 
 OR c.generic_land_use_1 = "Forest - harvestable"
 GROUP BY a.GRID_ID
;

ALTER TABLE percent_forest ADD UNIQUE INDEX grid_indx(grid_id);
ALTER TABLE percent_forest ADD COLUMN PERCENT_FOREST DOUBLE;

UPDATE percent_forest AS a 
 INNER JOIN tmp_grid_area AS b
 ON a.GRID_ID = b.GRID_ID
 SET a.PERCENT_FOREST = a.FOREST_AREA/b.GRID_AREA*100
;

# PERCENT_AGRICULTURE

CREATE TABLE percent_agriculture
 SELECT 
 a.GRID_ID,
 SUM(a.AREA) AS AGR_AREA
 FROM pierow_grid AS a
 INNER JOIN parcels AS b 
 ON (a.parcel_id = b.parcel_id)
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS c
 ON b.land_use = c.county_land_use_code and b.county = b.county
 WHERE c.generic_land_use_1 = "Agriculture" 
 GROUP BY a.GRID_ID
;

ALTER TABLE percent_agriculture ADD UNIQUE INDEX grid_indx(grid_id);
ALTER TABLE percent_agriculture ADD COLUMN PERCENT_AGR DOUBLE;

UPDATE percent_agriculture AS a 
 INNER JOIN tmp_grid_area AS b
 ON a.GRID_ID = b.GRID_ID
 SET a.PERCENT_AGR = a.AGR_AREA/b.GRID_AREA*100
;

# DROP TABLE tmp_grid_area;


######################################################################
# King County PERCENT_ROW table

USE PSRC_parcels_king;

CREATE TABLE percent_row
 SELECT 
 GRID_CODE AS GRID_ID,
 SUM(AREA) AS ROW_AREA
 FROM tmp_parcel_fractions_in_gridcells
 WHERE pin = 0
 GROUP BY GRID_CODE
;

ALTER TABLE percent_row ADD UNIQUE INDEX grid_indx(grid_id);
ALTER TABLE percent_row ADD COLUMN PERCENT_ROW DOUBLE;

CREATE TEMPORARY TABLE tmp_grid_area 
 SELECT 
 GRID_CODE AS GRID_ID,
 SUM(AREA) AS GRID_AREA
 FROM tmp_parcel_fractions_in_gridcells
 GROUP BY GRID_ID
;

ALTER TABLE tmp_grid_area ADD UNIQUE INDEX grid_indx(grid_id);

UPDATE percent_row AS a 
 INNER JOIN tmp_grid_area AS b
 ON a.GRID_ID = b.GRID_ID
 SET a.PERCENT_ROW = a.ROW_AREA/b.GRID_AREA*100
; 

# PERCENT_MINING

CREATE TABLE percent_mining
 SELECT 
 a.GRID_CODE AS GRID_ID, 
 SUM(a.AREA) AS MINING_AREA
 FROM tmp_parcel_fractions_in_gridcells AS a
 INNER JOIN parcels AS b
 ON (a.pin = b.parcel_id)
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS c
 ON b.land_use = c.county_land_use_code and b.county = b.county
 WHERE c.generic_land_use_1 = "Mining"
 GROUP BY a.GRID_CODE
; 

ALTER TABLE percent_mining ADD UNIQUE INDEX grid_indx (grid_id);
ALTER TABLE percent_mining ADD COLUMN PERCENT_MINING DOUBLE;

UPDATE percent_mining AS a
 INNER JOIN tmp_grid_area AS b
 ON a.grid_id = b.grid_id
 SET a.percent_mining = a.mining_area/b.grid_area*100
;

# PERCENT_FOREST

CREATE TABLE percent_forest
 SELECT 
 a.GRID_CODE AS GRID_ID,
 SUM(a.AREA) AS FOREST_AREA
 FROM tmp_parcel_fractions_in_gridcells AS a
 INNER JOIN parcels AS b 
 ON (a.pin = b.parcel_id)
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS c
 ON b.land_use = c.county_land_use_code and b.county = b.county
 WHERE c.generic_land_use_1 = "Forest - protected" 
 OR c.generic_land_use_1 = "Forest - harvestable"
 GROUP BY a.GRID_CODE
;

ALTER TABLE percent_forest ADD UNIQUE INDEX grid_indx(grid_id);
ALTER TABLE percent_forest ADD COLUMN PERCENT_FOREST DOUBLE;

UPDATE percent_forest AS a 
 INNER JOIN tmp_grid_area AS b
 ON a.GRID_ID = b.GRID_ID
 SET a.PERCENT_FOREST = a.FOREST_AREA/b.GRID_AREA*100
;

# PERCENT_AGRICULTURE

CREATE TABLE percent_agriculture
 SELECT 
 a.GRID_CODE AS GRID_ID,
 SUM(a.AREA) AS AGR_AREA
 FROM tmp_parcel_fractions_in_gridcells AS a
 INNER JOIN parcels AS b 
 ON (a.pin = b.parcel_id)
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS c
 ON b.land_use = c.county_land_use_code and b.county = b.county
 WHERE c.generic_land_use_1 = "Agriculture" 
 GROUP BY a.GRID_CODE
;

ALTER TABLE percent_agriculture ADD UNIQUE INDEX grid_indx(grid_id);
ALTER TABLE percent_agriculture ADD COLUMN PERCENT_AGR DOUBLE;

UPDATE percent_agriculture AS a 
 INNER JOIN tmp_grid_area AS b
 ON a.GRID_ID = b.GRID_ID
 SET a.PERCENT_AGR = a.AGR_AREA/b.GRID_AREA*100
;

# DROP TABLE tmp_grid_area;

######################################################################
# Snohomish County PERCENT_ROW

USE PSRC_parcels_snohomish;

CREATE TABLE percent_row
 SELECT 
 GRID_CODE AS GRID_ID,
 SUM(AREA) AS ROW_AREA
 FROM tmp_parcel_fractions_in_gridcells
 WHERE LRSN = 0 
 GROUP BY GRID_CODE
;

ALTER TABLE percent_row ADD UNIQUE INDEX grid_indx(grid_id);
ALTER TABLE percent_row ADD COLUMN PERCENT_ROW DOUBLE;

CREATE TEMPORARY TABLE tmp_grid_area 
 SELECT 
 GRID_CODE AS GRID_ID,
 SUM(AREA) AS GRID_AREA
 FROM tmp_parcel_fractions_in_gridcells
 GROUP BY GRID_ID
;

ALTER TABLE tmp_grid_area ADD UNIQUE INDEX grid_indx(grid_id);

UPDATE percent_row AS a 
 INNER JOIN tmp_grid_area AS b
 ON a.GRID_ID = b.GRID_ID
 SET a.PERCENT_ROW = a.ROW_AREA/b.GRID_AREA*100
; 


# PERCENT_MINING

ALTER TABLE tmp_parcel_fractions_in_gridcells ADD INDEX lrsn_indx (lrsn);

CREATE TABLE percent_mining
 SELECT 
 a.GRID_CODE AS GRID_ID, 
 SUM(a.AREA) AS MINING_AREA
 FROM tmp_parcel_fractions AS a
 INNER JOIN parcels AS b
 ON (a.lrsn = b.parcel_id)
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS c
 ON b.land_use = c.county_land_use_code and b.county = b.county
 WHERE c.generic_land_use_1 = "Mining"
 GROUP BY a.GRID_CODE
; 

ALTER TABLE percent_mining ADD UNIQUE INDEX grid_indx (grid_id);
ALTER TABLE percent_mining ADD COLUMN PERCENT_MINING DOUBLE;

UPDATE percent_mining AS a
 INNER JOIN tmp_grid_area AS b
 ON a.grid_id = b.grid_id
 SET a.percent_mining = a.mining_area/b.grid_area*100
;

# PERCENT_FOREST

CREATE TABLE percent_forest
 SELECT 
 a.GRID_CODE AS GRID_ID,
 SUM(a.AREA) AS FOREST_AREA
 FROM tmp_parcel_fractions AS a
 INNER JOIN parcels AS b 
 ON (a.lrsn = b.parcel_id)
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS c
 ON b.land_use = c.county_land_use_code and b.county = b.county
 WHERE c.generic_land_use_1 = "Forest - protected" 
 OR c.generic_land_use_1 = "Forest - harvestable"
 GROUP BY a.GRID_CODE
;

ALTER TABLE percent_forest ADD UNIQUE INDEX grid_indx(grid_id);
ALTER TABLE percent_forest ADD COLUMN PERCENT_FOREST DOUBLE;

UPDATE percent_forest AS a 
 INNER JOIN tmp_grid_area AS b
 ON a.GRID_ID = b.GRID_ID
 SET a.PERCENT_FOREST = a.FOREST_AREA/b.GRID_AREA*100
;

# PERCENT_AGRICULTURE

CREATE TABLE percent_agriculture
 SELECT 
 a.GRID_CODE AS GRID_ID,
 SUM(a.AREA) AS AGR_AREA
 FROM tmp_parcel_fractions AS a
 INNER JOIN parcels AS b 
 ON (a.lrsn = b.parcel_id)
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS c
 ON b.land_use = c.county_land_use_code and b.county = b.county
 WHERE c.generic_land_use_1 = "Agriculture" 
 GROUP BY a.GRID_CODE
;

ALTER TABLE percent_agriculture ADD UNIQUE INDEX grid_indx(grid_id);
ALTER TABLE percent_agriculture ADD COLUMN PERCENT_AGR DOUBLE;

UPDATE percent_agriculture AS a 
 INNER JOIN tmp_grid_area AS b
 ON a.GRID_ID = b.GRID_ID
 SET a.PERCENT_AGR = a.AGR_AREA/b.GRID_AREA*100
;


# DROP TABLE tmp_row_grid_area;



