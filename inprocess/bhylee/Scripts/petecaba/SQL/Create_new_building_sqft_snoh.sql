## Create a table containing the total square feet per parcel id from the buildings table and 
   replace old square feet value in the Snohomish County parcel table with the building square
   feet values.
   
## Sum building square feet and group by parcel id from buildings table.
 USE PSRC_parcels_snohomish;
 CREATE TABLE tmp_building_sqft
 SELECT PARCEL_ID, sum(built_sqft) as BUILDING_SQFT
 FROM buildings
 GROUP BY PARCEL_ID;
 

## Create 
 USE Snohomish_new_bldlnds_peter;
 CREATE TABLE tmp_building_sqft_by_parcel
 SELECT * from PSRC_parcels_snohomish.tmp_building_sqft;
 
 ALTER TABLE tmp_building_sqft_by_parcel ADD INDEX (PARCEL_ID(15));
 
 ALTER TABLE parcels add column tmp_building_sqft double;
 
 SET SESSION BIG_TABLES = 1;

 UPDATE parcels as a inner join tmp_building_sqft_by_parcel as b
 ON a.parcel_id = b.parcel_id
 SET a.tmp_building_sqft = b.building_sqft;
 
 
################################################################# 
## Process that involves creating a new parcels table with new sq.ft. values.
USE job_allocation_snohomish_peter;

CREATE TABLE parcels
SELECT 
	a.PARCEL_ID,
	b.generic_land_use_1 as LAND_USE,
	a.tmp_building_sqft as SQUARE_FOOTAGE,
	a.STREET_NUMBER,
	a.PREFIX,
	a.STREET_NAME,
	a.STREET_TYPE,
	a.SUFFIX,
	a.CENSUS_BLOCK,
	a.STANDARDIZED_STREET_TYPE,
	a.COUNTY
FROM Snohomish_new_bldlnds_peter.parcels a
	INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass b
	ON a.county = b.county AND a.land_use = b.county_land_use_code;
 
 