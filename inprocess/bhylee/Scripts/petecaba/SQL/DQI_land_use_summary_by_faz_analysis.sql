/* Title: Built Sqft. per Assessor Residential Units by FAZ
   Input table: land_use_summary_by_faz
   Description: Creates a table containing sqft per multi-family and single family Assessor's residential units by FAZ
   Output table: built_sqft_per_assessor_residential_units_by_faz
*/   

CREATE TABLE tmp_built_sqft_per_assessor_residential_unit_by_faz
 (FAZ INT(11),
 LAND_USE TEXT,
 BUILT_SQFT DOUBLE,
 ASSESSOR_RESIDENTIAL_UNITS DOUBLE,
 SQFT_PER_ASSESSOR_SINGLE DOUBLE)
;

INSERT INTO tmp_built_sqft_per_assessor_residential_unit_by_faz
 SELECT 
 FAZ,
 LAND_USE,
 BUILT_SQFT,
 ASSESSOR_RESIDENTIAL_UNITS,
 BUILT_SQFT/ASSESSOR_RESIDENTIAL_UNITS AS SQFT_PER_ASSESSOR_SINGLE
 FROM PSRC_2000_data_quality_indicators.land_use_summary_by_faz a
 WHERE a.land_use = "Single Family Residential"
; 

ALTER TABLE tmp_built_sqft_per_assessor_residential_unit_by_faz ADD COLUMN SQFT_PER_ASSESSOR_MULTI DOUBLE;

UPDATE tmp_built_sqft_per_assessor_residential_unit_by_faz a
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_summary_by_faz b
 ON a.faz = b.faz
 SET a.SQFT_PER_ASSESSOR_MULTI = b.BUILT_SQFT/b.ASSESSOR_RESIDENTIAL_UNITS 
 WHERE b.land_use = "Multi-Family Residential"
;

UPDATE built_sqft_per_assessor_residential_unit_by_faz 
 SET SQFT_PER_ASSESSOR_SINGLE = null
 WHERE SQFT_PER_ASSESSOR_SINGLE = 0
;

UPDATE built_sqft_per_assessor_residential_unit_by_faz 
 SET SQFT_PER_ASSESSOR_MULTI = null
 WHERE SQFT_PER_ASSESSOR_MULTI = 0
;

/* Title: Built Sqft. per Imputed Residential Units by FAZ
   Input table: land_use_summary_by_faz
   Description: Creates a table containing sqft per multi-family and single family imputed residential units by FAZ
   Output table: built_sqft_per_imputed_residential_unit_by_faz
*/

CREATE TABLE built_sqft_per_imputed_residential_unit_by_faz
 (FAZ INT(11),
  LAND_USE TEXT,
  BUILT_SQFT DOUBLE,
  IMPUTED_RESIDENTIAL_UNITS DOUBLE,
  SQFT_PER_IMPUTED_SINGLE DOUBLE)
;

INSERT INTO built_sqft_per_imputed_residential_unit_by_faz
 SELECT
 FAZ,
 LAND_USE,
 BUILT_SQFT,
 IMPUTED_RESIDENTIAL_UNITS,
 BUILT_SQFT/IMPUTED_RESIDENTIAL_UNITS AS SQFT_PER_IMPUTED_SINGLE
 FROM PSRC_2000_data_quality_indicators.land_use_summary_by_faz a
 WHERE a.land_use = "Single Family Residential"
;

ALTER TABLE built_sqft_per_imputed_residential_unit_by_faz ADD COLUMN SQFT_PER_IMPUTED_MULTI DOUBLE;

UPDATE built_sqft_per_imputed_residential_unit_by_faz a
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_summary_by_faz b
 ON a.faz = b.faz
 SET a.SQFT_PER_IMPUTED_MULTI = b.BUILT_SQFT/b.IMPUTED_RESIDENTIAL_UNITS
 WHERE b.LAND_USE = "Multi-Family Residential"
; 

UPDATE built_sqft_per_imputed_residential_unit_by_faz 
 SET SQFT_PER_IMPUTED_SINGLE = null
 WHERE SQFT_PER_IMPUTED_SINGLE = 0
;

UPDATE built_sqft_per_imputed_residential_unit_by_faz 
 SET SQFT_PER_IMPUTED_MULTI = null
 WHERE SQFT_PER_IMPUTED_MULTI = 0
;

/* Title: Lot Square Feet per Residential Units by Census Block
   Input table: parcels (PSRC_parcels_all_counties) and land_use_generic_reclass
   Description: Aggregates res. imputed units (single and multi-family) by census block
   Output table: lot_sqft_per_residential_units_by_census_block
*/

CREATE TABLE lot_sqft_per_residential_units_by_census_block
 SELECT 
 p.CENSUS_BLOCK AS CENSUS_BLOCK, 
 p.COUNTY AS COUNTY,
 lu.GENERIC_LAND_USE_1 AS RESIDENTIAL_LAND_USE,
 round(avg(p.lot_sqft/p.residential_units_imputed),2) as LOT_SQFT_PER_IMPUTED_HOUSING_UNIT
 FROM PSRC_parcels_all_counties.parcels p
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass lu
 ON p.land_use = lu.county_land_use_code 
 AND p.county = lu.county
 WHERE (lu.generic_land_use_1 = "Multi-Family Residential"
 OR lu.generic_land_use_1 = "Single Family Residential")
 AND residential_units_imputed > 0
 GROUP BY 
 p.CENSUS_BLOCK,
 p.COUNTY,
 lu.GENERIC_LAND_USE_1
;

/* Title: Lot Square Feet per Multi-Family Units by Census Block
   Input table: parcels (PSRC_parcels_all_counties) and land_use_generic_reclass
   Description: Aggregates multi-family imputed units by census block
   Output table:
*/

CREATE TABLE lot_sqft_per_multi_family_units_by_census_block
 SELECT 
 p.CENSUS_BLOCK AS CENSUS_BLOCK, 
 p.COUNTY AS COUNTY,
 lu.GENERIC_LAND_USE_1 AS RESIDENTIAL_LAND_USE,
 round(avg(p.lot_sqft/p.residential_units_imputed),2) as LOT_SQFT_PER_MULTI_HOUSING_UNIT
 FROM PSRC_parcels_all_counties.parcels p
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass lu
 ON p.land_use = lu.county_land_use_code 
 AND p.county = lu.county
 WHERE (lu.generic_land_use_1 = "Multi-Family Residential")
 AND residential_units_imputed > 0
 GROUP BY 
 p.CENSUS_BLOCK,
 p.COUNTY,
 lu.GENERIC_LAND_USE_1
;

/* Title: Lot Square Feet per Single Family Units by Census Block
   Input table: parcels (PSRC_parcels_all_counties) and land_use_generic_reclass
   Description: Aggregates single family imputed units by census block
   Output table: lot_sqft_per_single_family_units_by_census_block
*/

CREATE TABLE lot_sqft_per_single_family_units_by_census_block
 SELECT 
 p.CENSUS_BLOCK AS CENSUS_BLOCK, 
 p.COUNTY AS COUNTY,
 lu.GENERIC_LAND_USE_1 AS RESIDENTIAL_LAND_USE,
 round(avg(p.lot_sqft/p.residential_units_imputed),2) as LOT_SQFT_PER_SINGLE_HOUSING_UNIT
 FROM PSRC_parcels_all_counties.parcels p
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass lu
 ON p.land_use = lu.county_land_use_code 
 AND p.county = lu.county
 WHERE (lu.generic_land_use_1 = "Single Family Residential")
 AND residential_units_imputed > 0
 GROUP BY 
 p.CENSUS_BLOCK,
 p.COUNTY,
 lu.GENERIC_LAND_USE_1
;

/* 
   TEST	
   Title: Built Square Feet by Acre per Non Residential Space by Gridcell
   Input table: parcels, parcel_fractions_in_zones
   Description: total non-residential built square feet/acre per gridcell
   Output table: built_non_residential_sqft_by_acre_per_gridcell
*/

CREATE TABLE built_non_residential_sqft_by_acre_per_gridcell
 SELECT 
 a.PARCEL_ID,
 a.COUNTY,
 a.LAND_USE AS LAND_USE_CODE,
 a.LOT_AREA,
 a.BUILT_SQFT,
 (a.BUILT_SQFT/a.LOT_AREA) AS SQFT_PER_NON_RESIDENTIAL_PARCEL,
 b.GENERIC_LAND_USE_1 AS LAND_USE
 FROM PSRC_parcels_kitsap.parcels a
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass b
 ON a.county = b.county 
 AND a.land_use = b.county_land_use_code
 WHERE b.generic_land_use_1 <> "Multi-Family Residential" 
 OR b.generic_land_use_1 <> "Single Family Residential" 
 GROUP BY 
 b.GENERIC_LAND_USE_1 
; 

/* Parcel records contain non-residential land use types */
CREATE TEMPORARY TABLE x
 SELECT 
 a.PARCEL_ID,
 a.LAND_USE
 a.BUILT_SQFT,
 a.LOT_AREA,
 a.COUNTY,
 b.GENERIC_LAND_USE_1 AS NON_RESIDENTIAL_LAND_USE
 FROM parcels a 
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass b
 ON a.land_use = b.county_land_use_code 
 AND a.county = b.county
 WHERE b.generic_land_use_1 <> "Multi-Family Residential" 
 OR b.generic_land_use <> "Single Family Residential"
 GROUP BY 
 a.PARCEL_ID,
 b.GENERIC_LAND_USE_1
;

/* Title: Housing Units per Acre within a Gridcell
   Input table: gridcells
   Description: Number of Housing Units/Acre
   Output table: gridcells
*/

ALTER TABLE gridcells ADD COLUMN ACRE DOUBLE;
ALTER TABLE gridcells ADD COLUMN UNITS_PER_ACRE DOUBLE;

UPDATE gridcells 
 SET ACRE = 5.56
;

UPDATE gridcells 
 SET UNITS_PER_ACRE = RESIDENTIAL_UNITS/ACRE
;

UPDATE gridcells 
 SET UNITS_PER_ACRE = null 
 WHERE UNITS_PER_ACRE = 0
; 

/* 
   Title: Housing Units per Acre by TAZ
   Input table: 
   Description:
   Output table:

Conversion Acres to Feet: 43560.178439801326
Conversion Feet to Acre: 5.56

*/
ALTER TABLE PSRC_parcels_all_counties.parcels ADD COLUMN ACRES DOUBLE;

UPDATE PSRC_parcels_all_counties.parcels 
 SET ACRES = lot_sqft/43560.178439801326
; 

CREATE TABLE housing_units_by_taz
 SELECT
 bft.TAZ,
 sum(p.residential_units) AS TOTAL_RES_UNITS,
 sum(p.residential_units_imputed) AS TOTAL_RES_UNITS_IMPUTE,
 FROM PSRC_parcels_all_counties.parcels AS p
 INNER JOIN PSRC_2000_data_quality_indicator_maps.block_faz_and_taz AS bft 
 ON p.census_block = bft.census_block 
 GROUP BY
 bft.TAZ
; 

CREATE TABLE res_acres_by_taz
 SELECT 
 bft.TAZ,
 sum(p.acres) AS TOTAL_RES_ACRES
 FROM PSRC_parcels_all_counties.parcels AS p
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS lu
 ON (p.land_use = lu.county_land_use_code 
 AND p.county = lu.county) 
 INNER JOIN PSRC_2000_data_quality_indicator_maps.block_faz_and_taz AS bft 
 ON p.census_block = bft.census_block 
 WHERE lu.generic_land_use_1 = "Multi-Family Residential" 
 OR lu.generic_land_use_1 = "Single Family Residential"
 GROUP BY 
 bft.TAZ
; 

ALTER TABLE housing_units_by_taz ADD COLUMN RES_UNITS_PER_ACRE double;
ALTER TABLE housing_units_by_taz ADD COLUMN RES_UNITS_IMPUTED_PER_ACRE double;
ALTER TABLE housing_units_by_taz ADD INDEX (TAZ(5));
ALTER TABLE res_acres_by_taz ADD INDEX (TAZ(5));

UPDATE housing_units_by_taz AS a
 INNER JOIN res_acres_by_taz AS b
 ON a.taz = b.taz 
 SET a.res_units_per_acre = a.total_res_units/b.total_res_acres
; 

UPDATE housing_units_by_taz AS a
 INNER JOIN res_acres_by_taz AS b
 ON a.taz = b.taz 
 SET a.res_units_imputed_per_acre = a.total_res_units_impute/b.total_res_acres
;

update housing_units_by_taz set res_units_imputed_per_acre = null;
update housing_units_by_taz set res_units_per_acre = null;

/*
   Title: Population Units per Acre by Gridcell
   Input table: households 
   Description: Population per acre displayed at the gridcell level
   Output table: population_units_per_acre
*/

CREATE TABLE population_per_acre_by_gridcell
 SELECT 
 h.GRID_ID,
 sum(h.PERSONS) as TOTAL_PERSONS,

 5.56 AS ACRES

 FROM PSRC_2000_baseyear.households AS h
 GROUP BY GRID_ID
;

ALTER TABLE population_per_acre_by_gridcell ADD COLUMN POPULATION_PER_ACRE DOUBLE;

UPDATE population_per_acre_by_gridcell
 SET POPULATION_PER_ACRE = TOTAL_PERSONS/ACRES
; 

UPDATE population_per_acre_by_gridcell
 SET POPULATION_PER_ACRE = null 
 WHERE POPULATION_PER_ACRE = 0
; 

ALTER TABLE population_per_acre_by_gridcell ADD UNIQUE INDEX popgrd_index(GRID_ID); 

/* 
   Title: Population per Acre by TAZ
   Input table: households and parcels 
   Description: Synthesized population per acre by TAZ
   Output table: population_per_acre_by_taz
*/

CREATE TEMPORARY TABLE total_population_per_acre
 SELECT 
 bft.TAZ,
 sum(h.persons) AS TOTAL_PERSON
 FROM PSRC_2000_data_quality_indicator_maps.block_faz_and_taz AS bft 
 INNER JOIN PSRC_2000_baseyear.households AS h 
 ON 

CREATE TEMPORARY TABLE 
 

/*
   Title: Parcels (add county name) by Generic Land Use Type 1 and 2
   Input table: Parcels (county name) and land use generic reclass
   Description: 
   Output table:
*/

CREATE TABLE glu_king_parcels 
 SELECT 
 p.PARCEL_ID,
 p.CITY_COVER,
 p.CENSUS_BLOCK,
 dqi.GENERIC_LAND_USE_1,
 dqi.GENERIC_LAND_USE_2
 FROM PSRC_parcels_king.parcels AS p
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS dqi 
 ON p.land_use = dqi.county_land_use_code 
 AND p.county = dqi.county
;

alter table glu_king_parcels change column GENERIC_LAND_USE_1 GENERIC_LAND_USE_1 varchar(100);
alter table glu_king_parcels change column GENERIC_LAND_USE_2 GENERIC_LAND_USE_2 varchar(10);
alter table glu_king_parcels add unique index prcl_id(parcel_id(10))
;

CREATE TABLE glu_kitsap_parcels 
 SELECT 
 p.PARCEL_ID,
 p.CITY_COVER,
 p.CENSUS_BLOCK,
 dqi.GENERIC_LAND_USE_1,
 dqi.GENERIC_LAND_USE_2
 FROM PSRC_parcels_kitsap.parcels AS p
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS dqi 
 ON p.land_use = dqi.county_land_use_code 
 AND p.county = dqi.county
;

alter table glu_kitsap_parcels change column GENERIC_LAND_USE_1 GENERIC_LAND_USE_1 varchar(100);
alter table glu_kitsap_parcels change column GENERIC_LAND_USE_2 GENERIC_LAND_USE_2 varchar(10);
alter table glu_kitsap_parcels add unique index prcl_id(parcel_id(10))
;

CREATE TABLE glu_pierce_parcels 
 SELECT 
 p.PARCEL_ID,
 p.CITY_COVER,
 p.CENSUS_BLOCK,
 dqi.GENERIC_LAND_USE_1,
 dqi.GENERIC_LAND_USE_2
 FROM PSRC_parcels_pierce.parcels AS p
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS dqi 
 ON p.land_use = dqi.county_land_use_code 
 AND p.county = dqi.county
;

alter table glu_pierce_parcels change column GENERIC_LAND_USE_1 GENERIC_LAND_USE_1 varchar(100);
alter table glu_pierce_parcels change column GENERIC_LAND_USE_2 GENERIC_LAND_USE_2 varchar(10);
alter table glu_pierce_parcels add unique index prcl_id(parcel_id(10))
;

CREATE TABLE glu_snoh_parcels 
 SELECT 
 p.PARCEL_ID,
 p.CITY_COVER,
 p.CENSUS_BLOCK,
 dqi.GENERIC_LAND_USE_1,
 dqi.GENERIC_LAND_USE_2
 FROM PSRC_parcels_snohomish.parcels AS p
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass AS dqi 
 ON p.land_use = dqi.county_land_use_code 
 AND p.county = dqi.county
;

alter table glu_snoh_parcels change column PARCEL_ID PARCEL_ID int(11);
alter table glu_snoh_parcels change column GENERIC_LAND_USE_1 GENERIC_LAND_USE_1 varchar(100);
alter table glu_snoh_parcels change column GENERIC_LAND_USE_2 GENERIC_LAND_USE_2 varchar(10);
alter table glu_snoh_parcels add unique index prcl_id(parcel_id)
;

