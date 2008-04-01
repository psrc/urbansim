## Impute land_use value for buildings missing use_codes. 
   Establish which parcel the building missing a use_code 
   overlays and extract the land_use value from the parcels table.
   
## Input tables: parcels table including imputed land_use values.
	 	 	  buildings table include only buildings with missing use_codes.
	 	 	  
 
 ALTER TABLE parcels ADD INDEX (parcel_id(10));
 ALTER TABLE parcels ADD INDEX (land_use);
 
 CREATE TABLE tmp_buildings_missing_code
  SELECT * from buildings
  WHERE use_code is null;
  
 ALTER TABLE tmp_buildings_missing_code ADD INDEX (parcel_id(10));
 
 ALTER TABLE tmp_buildings_missing_code ADD COLUMN PARCEL_LAND_USE int(11);
 ALTER TABLE tmp_buildings_missing_code ADD COLUMN BUILDING_USE_IMPUTED int(11);
 
 CREATE TABLE tmp_parcel_land_use 
  SELECT 
  a.PARCEL_ID,
  a.LAND_USE,
  a.IMPUTE_FLAG
  from parcels a 
  INNER JOIN tmp_buildings_missing_code b
  ON a.parcel_id = b.parcel_id;
 
 ALTER TABLE tmp_parcel_land_use ADD INDEX (parcel_id(10));
 ALTER TABLE tmp_parcel_land_use ADD INDEX (land_use);
 
 UPDATE tmp_buildings_missing_code a 
 inner join 
 
 CREATE TABLE PARCEL_USE_2_SUMMARY 
 SELECT b.generic_land_use_2, sum(a.built_sqft) from parcels a
 INNER JOIN land_use_generic_reclass b
 ON a.land_use = b.county_land_use_code
 GROUP BY b.generic_land_use_2;
 
 CREATE TABLE BUILDING_USE_2_SUMMARY 
 SELECT b.generic_building_use_2, sum(a.built_sqft) from buildings a
 INNER JOIN building_use_generic_reclass b
 ON a.building_use = b.county_building_use_code
 GROUP BY b.generic_building_use_2;
 
 select sum(built_sqft) from buildings_nov4_peter where extension = 'c01' or
 extension = 'c02' 
 or extension = 'c03' 
 or extension = 'c04'
 or extension = 'c05' 
 or extension = 'c06' 
 or extension = 'c09'
 ;
 
 
 
 
 
 
 
 
     	
  