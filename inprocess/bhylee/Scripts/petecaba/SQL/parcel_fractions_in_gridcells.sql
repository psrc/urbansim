/* Change field names accordingly by county before running script */

/* Snohomish County */

#CREATE temporary TABLE prelim_parcel_fractions_in_gridcells
# SELECT 
# LRSN AS PARCEL_ID,
# GRID_CODE AS GRID_ID,
# AREA AS FRAGMENT_AREA
# FROM tmp_parcel_fractions_in_gridcells
#;

#ALTER TABLE prelim_parcel_fractions_in_gridcells ADD INDEX (PARCEL_ID);

#CREATE TEMPORARY TABLE tmp_parcel_area 
# SELECT 
# LRSN AS PARCEL_ID,
# SUM(AREA) as ORIG_PARCEL_AREA
# FROM tmp_parcel_fractions_in_gridcells
# GROUP BY PARCEL_ID
#; 

#ALTER TABLE tmp_parcel_area ADD INDEX (PARCEL_ID);

#create temporary table tmp_fractions
# (PARCEL_ID INT(11), GRID_ID INT(11), FRAGMENT_AREA DOUBLE(7,3),
# PARCEL_FRACTION DOUBLE(7,3))
#; 

#INSERT INTO tmp_fractions (parcel_id, grid_id, fragment_area, parcel_fraction)
# SELECT 
# a.PARCEL_ID,
# a.GRID_ID,
# a.FRAGMENT_AREA,
# a.FRAGMENT_AREA/b.ORIG_PARCEL_AREA AS PARCEL_FRACTION
# FROM prelim_parcel_fractions_in_gridcells a
# INNER JOIN tmp_parcel_area b
# ON a.PARCEL_ID = b.PARCEL_ID
#; 

#ALTER TABLE tmp_fractions ADD INDEX (parcel_id, grid_id);

#CREATE TABLE parcel_fractions_in_gridcells 
# SELECT 
# PARCEL_ID,
# GRID_ID,
# SUM(PARCEL_FRACTION) AS PARCEL_FRACTION
# FROM tmp_fractions
# GROUP BY PARCEL_ID, GRID_ID
#;

#DELETE FROM parcel_fractions_in_gridcells 
# WHERE PARCEL_ID = -9999 or PARCEL_ID = 0 or PARCEL_ID is null
#; 

#ALTER TABLE parcel_fractions_in_gridcells CHANGE COLUMN PARCEL_ID PARCEL_ID varchar(15);

#ALTER TABLE parcel_fractions_in_gridcells ADD COLUMN COUNTY varchar(3);

#UPDATE parcel_fractions_in_gridcells SET COUNTY = "061";

#DROP TABLE prelim_parcel_fractions_in_gridcells;
#DROP TABLE tmp_parcel_area;
#DROP TABLE tmp_fractions;


/* King County */

CREATE TEMPORARY TABLE prelim_parcel_fractions_in_gridcells 
 SELECT 
 PIN AS PARCEL_ID,
 GRID_CODE AS GRID_ID,
 AREA AS FRAGMENT_AREA
 FROM tmp_parcel_fractions_in_gridcells
; 

ALTER TABLE prelim_parcel_fractions_in_gridcells ADD INDEX (PARCEL_ID(11));

CREATE TEMPORARY TABLE tmp_parcel_area 
 SELECT 
 PIN AS PARCEL_ID,
 SUM(AREA) as ORIG_PARCEL_AREA
 FROM tmp_parcel_fractions_in_gridcells
 GROUP BY PARCEL_ID
; 

ALTER TABLE tmp_parcel_area ADD INDEX (PARCEL_ID(10));

CREATE TEMPORARY TABLE tmp_fractions
 (PARCEL_ID varchar(15), GRID_ID INT(11), FRAGMENT_AREA DOUBLE(7,3),
 PARCEL_FRACTION DOUBLE(7,3))
; 

INSERT INTO tmp_fractions (parcel_id, grid_id, fragment_area, parcel_fraction)
 SELECT 
 a.PARCEL_ID,
 a.GRID_ID,
 a.FRAGMENT_AREA,
 a.FRAGMENT_AREA/b.ORIG_PARCEL_AREA AS PARCEL_FRACTION
 FROM prelim_parcel_fractions_in_gridcells a 
 INNER JOIN tmp_parcel_area b 
 ON a.parcel_id = b.parcel_id
; 

ALTER TABLE tmp_fractions ADD INDEX (parcel_id, grid_id);

CREATE TABLE parcel_fractions_in_gridcells 
 SELECT 
 PARCEL_ID,
 GRID_ID,
 SUM(PARCEL_FRACTION) AS PARCEL_FRACTION
 FROM tmp_fractions
 GROUP BY PARCEL_ID, GRID_ID
;

DELETE FROM parcel_fractions_in_gridcells 
 WHERE PARCEL_ID = -9999 or PARCEL_ID = 0 or PARCEL_ID is null
;

DELETE FROM parcel_fractions_in_gridcells
 WHERE GRID_ID = -9999 or GRID_ID = 0
; 

ALTER TABLE parcel_fractions_in_gridcells ADD COLUMN COUNTY varchar(3);
ALTER TABLE parcel_fractions_in_gridcells ADD INDEX prcl_indx(parcel_id(15));
ALTER TABLE parcel_fractions_in_gridcells ADD INDEX grid_indx(grid_id);

UPDATE parcel_fractions_in_gridcells SET COUNTY = "033";

DROP TABLE prelim_parcel_fractions_in_gridcells;
DROP TABLE tmp_fractions;
DROP TABLE tmp_parcel_area;
