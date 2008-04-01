
# get the total jobs by sector from the leftovers from the job allocator
create table JOBS_PER_COUNTY_from_job_allocator
select 
	a.county, 
	a.sector, 
	sum(a.number_of_jobs) as TOTAL_JOBS
from job_allocation_king.employers a
	inner join job_allocation_king.final_employers_matched_to_parcels b
	on a.employer_id = b.employer_id
where b.decision in ('NO_PARCEL_IN_BLOCK', 'WRONG_SIDE_OF_STREET', 'WRONG_STREET_TYPE_FOR_BLOCK')
GROUP BY a.county, a.sector;

########---------- create the sector_land_use_weights table --------------------------

#copy sector_land_use_rates;

USE PSRC_proprietors_distributor_snohomish;

DROP table if exists SECTOR_LAND_USE_WEIGHTS;

CREATE TABLE SECTOR_LAND_USE_WEIGHTS 
SELECT 
	a.summary_area as FAZ_GROUP,
	b.sector_code AS SECTOR,
	a.land_use AS LAND_USE,
	a.PROXIMITY AS SEC_LU_WEIGHT
FROM job_allocation_snohomish.sector_land_use_rates a
	inner join division_sectors b on a.sector = b.sector
;

# Check the counts by sector again
SELECT SECTOR, COUNT(*) FROM SECTOR_LAND_USE_WEIGHTS GROUP BY SECTOR;

/*
ALTER TABLE SECTOR_LAND_USE_WEIGHTS CHANGE COLUMN summary_area FAZ_GROUP VARCHAR(4);
ALTER TABLE SECTOR_LAND_USE_WEIGHTS CHANGE COLUMN PROXIMITY SEC_LU_WEIGHT DOUBLE;

# reclassify sectors
CREATE TABLE gen_sectors_reclass SELECT * FROM  PSRC_proprietors_distributor_king.sec_lu_sector_reclass;

UPDATE SECTOR_LAND_USE_WEIGHTS a INNER JOIN gen_sectors_reclass b on a.sector = b.sector
SET a.sector = b.sector_code_2;

#CHECK THE SECTORS IN SECTOR_LAND_USE_WEIGHTS HERE!!!!!
#  Some sector/faz_group/land_use combinations will now have multiple sec_lu_weights. 
SELECT SECTOR, COUNT(*) FROM SECTOR_LAND_USE_WEIGHTS GROUP BY SECTOR;


#  These will now be collapsed.


CREATE TABLE SECTOR_LAND_USE_WEIGHTS_summed 
SELECT 
	FAZ_GROUP, 
	SECTOR, 
	LAND_USE, 
	SUM(SEC_LU_WEIGHT) AS SEC_LU_WEIGHT
FROM SECTOR_LAND_USE_WEIGHTS 
GROUP BY  
	FAZ_GROUP, 
	SECTOR, 
	LAND_USE
;

# Replace old version of SECTOR_LAND_USE_WEIGHTS with new one.

DROP TABLE SECTOR_LAND_USE_WEIGHTS;
RENAME TABLE SECTOR_LAND_USE_WEIGHTS_summed to SECTOR_LAND_USE_WEIGHTS;
ALTER TABLE SECTOR_LAND_USE_WEIGHTS CHANGE COLUMN SECTOR SECTOR int;
*/


############-------------------Create ZONE_WEIGHTS ------------------

# Add ZONE column to employers table
#	1.spatial identity employers with regional TAZ coverage -> esdtaz
#	2.change column name on Snohomish MAZ coverage to sno_maz
#	3.spatial identity esdtzmz with Snohomish MAZ coverage -> esdtzmz
#	(rename esdtzmz -> employers
#	(make sure taz  and sno_maz are all varchar)
#	4.Set employers.ZONE = taz or blocks.prc_maz/sno_maz, depending on the county.


UPDATE employers SET ZONE = TAZ WHERE COUNTY in ('033', '035', '053');
UPDATE employers SET ZONE = MAZ WHERE COUNTY = '061';


# Summarize by zone, giving each zone the proportion of county jobs in that zone.
CREATE TABLE jobs_per_zone_allzones
SELECT 
	COUNTY,
	ZONE,
	SUM(jobs00) AS JOB_SUM
FROM employers
GROUP BY COUNTY, ZONE;

# Remove any zones that have no parcels in them.
CREATE TEMPORARY TABLE parcelzones
SELECT 	COUNTY, ZONE 
FROM PARCELS
GROUP BY COUNTY, ZONE;

create unique index cnty_zone_indx ON parcelzones (COUNTY(3), ZONE(3));

CREATE TABLE jobs_per_zone
SELECT
	a.COUNTY, 
	a.ZONE,
	a.JOB_SUM
FROM jobs_per_zone_allzones a
	inner join parcelzones b on a.county = b.county and a.zone = b.zone;

# Get the total jobs per county
CREATE TABLE jobs_per_county
SELECT COUNTY, SUM(jobs00) AS JOB_SUM
FROM employers
GROUP BY COUNTY;

#Create empty ZONE_WEIGHTS table
CREATE TABLE ZONE_WEIGHTS (
	COUNTY varchar(4),
	ZONE varchar(6),
	ZONE_WEIGHT_HOMEBASED double,
	ZONE_WEIGHT_NONHOMEBASED double);

# Populate ZONE_WEIGHTS with data from jobs_per_zone and jobs_per_county.
INSERT INTO ZONE_WEIGHTS 
	(COUNTY,
	ZONE, 
	ZONE_WEIGHT_HOMEBASED)
SELECT 
	a.COUNTY, 
	a.ZONE,
	(a.JOB_SUM / b.JOB_SUM) 
FROM jobs_per_zone a inner join jobs_per_county b
	ON a.COUNTY = b.COUNTY;
	
UPDATE ZONE_WEIGHTS 
SET ZONE_WEIGHT_NONHOMEBASED = ZONE_WEIGHT_HOMEBASED;


# -------------------------Create JOB_PROPORTIONS_BY_SECTOR -----------
# (being done by Paul Trowbridge

ALTER TABLE JOB_PROPORTIONS_BY_SECTOR ADD COLUMN COUNTY VARCHAR(3);

UPDATE JOB_PROPORTIONS_BY_SECTOR SET COUNTY = '035';

#--------------------------Create JOBS_PER_COUNTY----------------------

CREATE TEMPORARY TABLE intital_JOBS_PER_COUNTY
SELECT
	b.COUNTY, 
	b.SECTOR,
	SUM(b.NUMBER_OF_JOBS) AS JOB_COUNT
FROM job_allocation_snohomish.final_employers_matched_to_parcels a 
	INNER JOIN job_allocation_snohomish.employers b
	ON a.employer_id = b.employer_id
WHERE a.decision in ('NO_PARCEL_IN_BLOCK', 'WRONG_SIDE_OF_STREET', 'WRONG_STREET_TYPE_FOR_BLOCK')
GROUP BY b.county, b.sector;

UPDATE intital_JOBS_PER_COUNTY a INNER JOIN division_sectors b
	ON a.sector = b.sector
SET a.sector = b.sector_code;


CREATE TABLE JOBS_PER_COUNTY
SELECT 
	COUNTY,
	SECTOR, 
	SUM(JOB_COUNT) AS JOB_COUNT
FROM intital_JOBS_PER_COUNTY
GROUP BY COUNTY, SECTOR;

ALTER TABLE JOBS_PER_COUNTY CHANGE COLUMN SECTOR SECTOR INT;
ALTER TABLE JOBS_PER_COUNTY CHANGE COLUMN JOB_COUNT TOTAL_COUNTY_JOBS INT;
ALTER TABLE JOBS_PER_COUNTY ADD COLUMN JOB_ALLOCATOR_LEFTOVERS INT;
ALTER TABLE JOBS_PER_COUNTY ADD COLUMN PROPRIETORS_JOBS INT;

UPDATE JOBS_PER_COUNTY SET JOB_ALLOCATOR_LEFTOVERS = TOTAL_COUNTY_JOBS;

UPDATE JOBS_PER_COUNTY SET PROPRIETORS_JOBS = 0 WHERE PROPRIETORS_JOBS IS NULL;

UPDATE JOBS_PER_COUNTY a INNER JOIN proprietors_jobs b
	ON a.county = b.county AND a.sector = b.sector
SET a.PROPRIETORS_JOBS = b.jobs;

UPDATE JOBS_PER_COUNTY SET TOTAL_COUNTY_JOBS = IFNULL(JOB_ALLOCATOR_LEFTOVERS, 0)
	+ IFNULL(PROPRIETORS_JOBS,0);



#-------------------------- Create PARCELS ------------------------------
# Add ZONE column to census blocks
#	1.spatial identity block centroids with regional TAZ coverage -> blktaz
#	2.change column name on Snohomish MAZ coverage to sno_maz
#	3.spatial identity blktzmz1 with Snohomish MAZ coverage -> blktzmz
#	(rename blktzmz -> blocks
#	(make sure taz, prc_maz and sno_maz are all varchar)

CREATE TABLE blocks select distinct census_block, county, taz, maz_num, taz_all, maz, zone
 from PSRC_proprietors_distributor_kitsap.blocks;

CREATE INDEX blk_indx ON blocks (census_block);

ALTER TABLE blocks add column ZONE varchar(6);
UPDATE blocks set zone = taz where county in ('033', '035', '053');
UPDATE blocks set zone = maz where county = '061';

# Create the parcels table with most of the fields
CREATE TEMPORARY TABLE PARCELS1
SELECT
	a.COUNTY,
	a.PARCEL_ID,
	a.USE_CODE as LAND_USE,
	0 AS JOB_COUNT,
	a.SQUARE_FOOTAGE AS SQFT,
	b.GENERIC_LAND_USE_1,
	b.GENERIC_LAND_USE_2,
	c.TAXEXEMPT_BINARY AS TAX_EXEMPT
FROM job_allocation_kitsap.parcels a 
	INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass b
	ON (a.county = b.county and a.use_code = b.county_land_use_code)
	INNER JOIN PSRC_parcels_kitsap.parcels AS c
	ON (a.parcel_id = c.parcel_id);
	

ALTER TABLE PARCELS1 ADD INDEX prcl_indx(parcel_id(10));	
 	
# get the remaining fields for the parcels table
CREATE TEMPORARY TABLE PARCELS2
SELECT 
	a.*,
	b.CENSUS_BLOCK
FROM PARCELS1 a INNER JOIN job_allocation_kitsap.parcels b
	ON a.parcel_id = b.parcel_id;

CREATE INDEX blk_indx ON PARCELS2 (CENSUS_BLOCK(15));

CREATE TEMPORARY TABLE PARCELS3
SELECT 	
	a.*,
	b.FAZ_GROUP
FROM PARCELS2 a INNER JOIN job_allocation_kitsap.census_blocks b
	on a.census_block = b.census_block;


CREATE TABLE PARCELS
SELECT 
	a.*,
	b.ZONE
FROM PARCELS3 a INNER JOIN blocks b ON a.census_block = b.census_block;



CREATE INDEX blk_indx ON PARCELS (CENSUS_BLOCK(15));
CREATE INDEX lu_fg_indx on PARCELS (generic_land_use_1(10), faz_group(2));
CREATE INDEX zone_indx ON PARCELS (ZONE);

### NOTE:
# Snohomish county was unlike others in that they wanted their zones to be their microanalysis zones.
# In Snohomish's case, the parcels coverage was intersected with their MAZ coverage and the PARCELS
#  table was updated accordingly. 



#### -----------------Add proprietors to JOBS_PER_COUNTY --------------------

#INPUT TABLES: 
#	JOBS_PER_COUNTY
#	proprietors_jobs

ALTER TABLE JOBS_PER_COUNTY CHANGE COLUMN JOB_COUNT TOTAL_COUNTY_JOBS INT;
ALTER TABLE JOBS_PER_COUNTY ADD COLUMN JOB_ALLOCATOR_LEFTOVERS INT;
ALTER TABLE JOBS_PER_COUNTY ADD COLUMN PROPRIETORS_JOBS INT;

UPDATE JOBS_PER_COUNTY SET JOB_ALLOCATOR_LEFTOVERS = TOTAL_COUNTY_JOBS;

UPDATE JOBS_PER_COUNTY SET PROPRIETORS_JOBS = 0 WHERE PROPRIETORS_JOBS IS NULL;

UPDATE JOBS_PER_COUNTY a INNER JOIN proprietors_jobs b
	ON a.county = b.county AND a.sector = b.sector
SET a.PROPRIETORS_JOBS = b.jobs;

UPDATE JOBS_PER_COUNTY SET TOTAL_COUNTY_JOBS = IFNULL(JOB_ALLOCATOR_LEFTOVERS, 0)
	+ IFNULL(PROPRIETORS_JOBS,0);

