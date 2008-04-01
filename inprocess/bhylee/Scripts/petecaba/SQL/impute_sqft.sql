# Change database names before running 1st query
# Change employer_mean_deviation table for Imputing Sqft in Snohomish County; 
#  use average of the 3 counties' sector in ('Education', 'State and Local') and land_use in ('School', 'Government')
# Change County Id at the end of the script

#*Begin Imputation Script* 

# Input tables:
# 		employers
#		final_employers_matched_to_parcels
#		parcels
#		buildings
#		land_use_generic_reclass


###################################
# Create table employers to parcels
###################################
DROP TABLE IF EXISTS prelim_employers_to_parcels;
CREATE TABLE prelim_employers_to_parcels
 SELECT 
 	a.PARCEL_ID,
 	b.EMPLOYER_ID,
 	b.SIC,
 	b.SECTOR,
 	b.NUMBER_OF_JOBS as JOBS,
 	c.USE_CODE,
 	c.SQUARE_FOOTAGE as SQFT,
 	c.LAND_USE as GENERIC_LAND_USE_1,
 	d.GENERIC_LAND_USE_2,
 	e.TAXEXEMPT_BINARY,
 	e.YEAR_BUILT
 FROM job_allocation_snohomish.final_employers_matched_to_parcels a 
 INNER JOIN job_allocation_snohomish.employers b ON (a.employer_id = b.employer_id)
 INNER JOIN job_allocation_snohomish.parcels c on (a.parcel_id = c.parcel_id)
 INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass d on (c.county = d.county 
  and c.use_code = d.county_land_use_code)
 INNER JOIN PSRC_parcels_snohomish.parcels e on a.parcel_id = e.parcel_id
 WHERE a.decision not in ('NO_PARCEL_IN_BLOCK', 'WRONG_SIDE_OF_STREET', 'WRONG_STREET_TYPE_FOR_BLOCK')
 AND (d.generic_land_use_2 <> 'R')
; 
 
ALTER TABLE prelim_employers_to_parcels ADD COLUMN SQFT_PER_JOB DOUBLE;
ALTER TABLE prelim_employers_to_parcels ADD INDEX sqft_job_indx(sqft_per_job);
ALTER TABLE prelim_employers_to_parcels ADD INDEX sctr_lu_indx(sector(15), generic_land_use_1(15));
ALTER TABLE prelim_employers_to_parcels ADD INDEX prcl_indx(parcel_id(11));

# UPDATE prelim_employers_to_parcels SET SQFT_PER_JOB = SQFT/JOBS;

##################################
# Preliminary sqft job ratio table  
##################################
DROP TABLE IF EXISTS prelim_sqft_job_ratio;
# /*
# CREATE TABLE prelim_sqft_job_ratio
#   SELECT 
#   	PARCEL_ID, 
#   	SECTOR, 
#   	SUM(JOBS) AS JOBS,
#   	SQFT,
#   	USE_CODE,
#   	GENERIC_LAND_USE_1
#   FROM prelim_employers_to_parcels
#   GROUP BY PARCEL_ID, SECTOR, GENERIC_LAND_USE_1;
 
# ALTER TABLE prelim_sqft_job_ratio ADD COLUMN SQFT_PER_JOB DOUBLE;
# UPDATE prelim_sqft_job_ratio SET SQFT_PER_JOB = SQFT/JOBS;

CREATE TABLE prelim_sqft_job_ratio (rec_number int auto_increment primary key, parcel_id mediumtext, sector mediumtext, sqft int, jobs int, sqft_per_job double,
 use_code int, land_use mediumtext, taxexempt int)
; 

INSERT INTO prelim_sqft_job_ratio (parcel_id, sector, sqft, jobs, sqft_per_job, use_code, land_use, taxexempt) 
 SELECT parcel_id, sector, sqft, sum(jobs) AS jobs, sqft_per_job, use_code, generic_land_use_1 AS land_use, taxexempt_binary as taxexempt
 FROM prelim_employers_to_parcels 
 GROUP BY parcel_id, sector, generic_land_use_1, taxexempt 
 ORDER BY sector, land_use
; 
      
UPDATE prelim_sqft_job_ratio SET sqft_per_job = sqft/jobs;
   

# CREATE TABLE prelim_sqft_job_ratio (rec_number int auto_increment primary key, parcel_id mediumtext, sector mediumtext, 
#  sqft int, jobs int, sqft_per_job double, use_code int, land_use mediumtext)
# ; 

# INSERT INTO prelim_sqft_job_ratio (parcel_id, sector, sqft, jobs, sqft_per_job, use_code, land_use) 
#  SELECT parcel_id, sector, sqft, sum(jobs) AS jobs, sqft_per_job, use_code, generic_land_use_1 AS land_use 
#  FROM prelim_employers_to_parcels 
#  GROUP BY parcel_id, sector, generic_land_use_1 
#  ORDER BY sector, land_use, sqft_per_job
# ; 

# ALTER TABLE prelim_sqft_job_ratio ADD INDEX rec_indx(rec_number);
 

################################################################################################
# Get ordered employer list that will become the choice set of employment records to be imputed
################################################################################################

# /*
DROP TABLE IF EXISTS ordered_employer;
# CREATE TABLE ordered_employer
# (
#  REC_NUMBER INT AUTO_INCREMENT PRIMARY KEY, 
#  SECTOR VARCHAR(50), 
# 
#  LAND_USE VARCHAR(50),
#  SQFT_PER_JOB DOUBLE
# );

# INSERT INTO ordered_employer (sector, land_use, sqft_per_job)
#  SELECT 
#   sector,
#   generic_land_use_1,
#   sqft_per_job
#  FROM prelim_sqft_job_ratio
#  ORDER BY sector, generic_land_use_1, sqft_per_job
# ;
# */
CREATE TABLE ordered_employer (rec_number int auto_increment primary key, parcel_id mediumtext, sector mediumtext, land_use mediumtext, sqft_per_job double);

INSERT INTO ordered_employer (parcel_id, sector, land_use, sqft_per_job) 
 SELECT parcel_id, sector, land_use, sqft_per_job
 FROM prelim_sqft_job_ratio 
 ORDER BY sector, land_use, sqft_per_job
; 

# CREATE TABLE ordered_employer (rec_number int auto_increment primary key, sector mediumtext, land_use mediumtext, sqft_per_job double, id int);

# INSERT INTO ordered_employer (sector, land_use, sqft_per_job, id) 
#  SELECT sector, land_use, sqft_per_job, id
#  FROM prelim_sqft_job_ratio 
#  ORDER BY sector, land_use, sqft_per_job;

ALTER TABLE ordered_employer ADD INDEX sctr_lu_indx(sector(15), land_use(15));
ALTER TABLE ordered_employer ADD INDEX sqf_job_indx(sqft_per_job);

#######################################	
# Create percentile distribution tables  	
#######################################

DROP TABLE IF EXISTS percentiles;
CREATE TABLE percentiles (PERCENTILE DOUBLE);

INSERT INTO percentiles (PERCENTILE)
 VALUES	
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

DROP TABLE IF EXISTS percentile_rows; 	
CREATE TABLE percentile_rows 
 (SECTOR VARCHAR(30),
  LAND_USE VARCHAR(30),
  PERCENTILE DOUBLE,
  MIN_REC_NUMBER INT,
  MAX_REC_NUMBER INT,
  PERCENTILE_ROW INT)
; 

INSERT INTO percentile_rows (sector, land_use, percentile) 
 SELECT 
 	b.sector,
 	b.land_use,
 	a.percentile
 FROM percentiles a, prelim_sqft_job_ratio b
; 

ALTER TABLE percentile_rows ADD INDEX sctr_lu_indx(sector(15), land_use(15));

############################################################################################################################
# Get min_rec and max_rec values for each combination of generic land use 1and employment sectors from ordered employer list
#############################################################################################################################
DROP TABLE IF EXISTS row_limits;
CREATE TABLE row_limits
 SELECT 
 	SECTOR,
 	LAND_USE,
 	MIN(REC_NUMBER) AS MIN_REC_NUMBER,
 	MAX(REC_NUMBER) AS MAX_REC_NUMBER
 FROM ordered_employer 
 GROUP BY SECTOR, LAND_USE
;

ALTER TABLE row_limits ADD INDEX sctr_lu_indx(sector(15), land_use(15));

UPDATE percentile_rows a INNER JOIN row_limits b
 ON a.sector = b.sector and a.land_use = b.land_use
 SET a.min_rec_number = b.min_rec_number, a.max_rec_number = b.max_rec_number
; 

UPDATE percentile_rows 
 SET percentile_row = (ceiling((max_rec_number - min_rec_number) * percentile)) + min_rec_number;

#########################################################
# Create sector to land use preliminary percentile table
#########################################################

DROP TABLE IF EXISTS prelim_sector_land_use_percentile;
CREATE TABLE prelim_sector_land_use_percentile 
  SELECT SECTOR, 
 	PERCENTILE, 
 	MIN_REC_NUMBER, 
 	MAX_REC_NUMBER,
	PERCENTILE_ROW 
  FROM percentile_rows 
  GROUP BY SECTOR, 
 	PERCENTILE, 
 	MIN_REC_NUMBER, 
 	MAX_REC_NUMBER,
 	PERCENTILE_ROW
;

UPDATE prelim_sector_land_use_percentile 
 SET PERCENTILE = PERCENTILE * 100
; 

ALTER TABLE prelim_sector_land_use_percentile ADD INDEX sctr_lu_indx(sector(15), land_use(15)); 
ALTER TABLE prelim_sector_land_use_percentile ADD INDEX prcnt_row_indx(percentile_row);

##################################
# Delete tables
# drop table percentile_rows;
# drop table percentiles;
# drop table prelim_sqft_job_ratio;
# drop table row_limits;
##################################

#################################################################################
# Create sector, land use percentile table from prelim_sector_land_use_percentile 
# 	for the row number for each sector land use percentile combination
#################################################################################

DROP TABLE IF EXISTS sector_land_use_percentile;
CREATE TABLE sector_land_use_percentile
 SELECT 
 	STEP
        sum(IF(percentile=0, percentile_row, 0)) as "0_percentile",
        sum(IF(percentile=1, percentile_row, 0)) as "1_percentile",
        sum(IF(percentile=5, percentile_row, 0)) as "5_percentile",
        sum(IF(percentile=10, percentile_row, 0)) as "10_percentile",
        sum(IF(percentile=25, percentile_row, 0)) as "25_percentile",
        sum(IF(percentile=50, percentile_row, 0)) as "50_percentile",
        sum(IF(percentile=75, percentile_row, 0)) as "75_percentile",
        sum(IF(percentile=90, percentile_row, 0)) as "90_percentile",
        sum(IF(percentile=95, percentile_row, 0)) as "95_percentile",
        sum(IF(percentile=99, percentile_row, 0)) as "99_percentile",
        sum(IF(percentile=100, percentile_row, 0)) as "100_percentile"
 FROM prelim_sector_land_use_percentile
 GROUP BY STEP
; 

ALTER TABLE sector_land_use_percentile ADD INDEX sctr_lu_indx(sector(15), land_use(15));

#########################################################################################################
# Create mean and standard deviation values for each sector to land use combination 
#	from ordered_employer table where percentile is greater than 10th and less than 90th percentiles. 
#########################################################################################################

DROP TABLE IF EXISTS employer_mean_deviation;
DROP TABLE IF EXISTS employer_mean_deviation_2;
DROP TABLE IF EXISTS employer_mean_deviation_90;

CREATE TABLE employer_mean_deviation
 SELECT a.SECTOR, a.LAND_USE, COUNT(sqft_per_job) AS n,
  SUM(a.sqft_per_job) as SUM,
  MIN(a.sqft_per_job) as MIN,
  MAX(a.sqft_per_job) as MAX,
  AVG(a.sqft_per_job) as AVG,
  STD(a.sqft_per_job) as STD 
 FROM ordered_employer a
 INNER JOIN sector_land_use_percentile b
 ON a.sector = b.sector and a.land_use = b.land_use
 WHERE (a.rec_number >= b.10_percentile) 
 	and (a.rec_number <= b.90_percentile)
 GROUP BY a.SECTOR, a.LAND_USE
;

# Use 3 county average sqft per job value for Snohomish County's sectors in ('EDUCATION K-12', 'STATE AND LOCAL') and land_use in ('School', 'Government')

 #UPDATE employer_mean_deviation SET AVG = 637.41 WHERE sector = 'EDUCATION K-12' AND land_use = 'School';
 #UPDATE employer_mean_deviation SET AVG = 567.72 WHERE sector = 'STATE AND LOCAL' AND land_use = 'Government';

ALTER TABLE employer_mean_deviation ADD INDEX sctr_lu_indx(sector(15), land_use(15));

################################################################################################
# Create table that contains selected records that are <= 10th percentile and >= 90th percentile 
# 	from ordered_employer table
################################################################################################

DROP TABLE IF EXISTS 10th_records;
DROP TABLE IF EXISTS tmp_10;
DROP TABLE IF EXISTS 99th_records;

CREATE TABLE 10th_records
 SELECT * FROM ordered_employer 
 WHERE SQFT_PER_JOB = 0
; 
 
ALTER TABLE 10th_records ADD INDEX prcl_indx(parcel_id(11));

CREATE TEMPORARY TABLE tmp_10 SELECT * FROM 10th_records;

ALTER TABLE tmp_10 ADD INDEX prcl_indx(parcel_id(12));
 
INSERT INTO 10th_records (rec_number, parcel_id, sector, land_use, sqft_per_job) 
 SELECT a.rec_number, a.parcel_id, a.sector, a.land_use, a.sqft_per_job 
 FROM ordered_employer a 
 INNER JOIN sector_land_use_percentile b
  ON (a.sector = b.sector and a.land_use = b.land_use)
 LEFT JOIN tmp_10 c 
  ON (a.PARCEL_ID = c.PARCEL_ID)
 WHERE (a.rec_number between b.0_percentile and b.10_percentile)
  AND c.PARCEL_ID IS NULL
;  
 
ALTER TABLE 10th_records ADD INDEX sctr_lu_indx(sector(15), land_use(15));
ALTER TABLE 10th_records ADD INDEX rec_indx(rec_number);

CREATE TABLE 99th_records
 SELECT a.* FROM ordered_employer a 
 INNER JOIN sector_land_use_percentile b
 ON (a.sector = b.sector and a.land_use = b.land_use)
 LEFT JOIN 10th_records c 
 ON a.rec_number = c.rec_number
 WHERE (a.rec_number between b.99_percentile and b.100_percentile)
 AND c.rec_number is null
;

ALTER TABLE 99th_records ADD INDEX sctr_lu_indx(sector(15), land_use(15));
ALTER TABLE 99th_records ADD INDEX rec_indx(rec_number); 

########################################################################
# Create table with actual records to be imputed (10th and 99th records)
########################################################################

DROP TABLE IF EXISTS 10th_output;
DROP TABLE IF EXISTS 99th_output;
 
CREATE TABLE 10th_output
 SELECT a.* 
 FROM ordered_employer a 
 INNER JOIN 10th_records b on (a.rec_number = b.rec_number)
; 
 
ALTER TABLE 10th_output ADD COLUMN AVG_IMPUTED_SQFT_PER_JOB DOUBLE;
ALTER TABLE 10th_output ADD INDEX sctr_lu_indx(sector(15), land_use(15));
ALTER TABLE 10th_output ADD INDEX prcl_indx(parcel_id(12));

UPDATE 10th_output a INNER JOIN employer_mean_deviation b 
 ON a.sector = b.sector and a.land_use = b.land_use 
 SET a.AVG_IMPUTED_SQFT_PER_JOB = b.AVG
;

CREATE TABLE 99th_output
 SELECT a.*
 FROM ordered_employer a 
 INNER JOIN 99th_records b ON (a.rec_number = b.rec_number)
;

ALTER TABLE 99th_output ADD COLUMN AVG_IMPUTED_SQFT_PER_JOB DOUBLE;
ALTER TABLE 99th_output ADD INDEX sctr_lu_indx(sector(15), land_use(15));
ALTER TABLE 99th_output ADD INDEX prcl_indx(parcel_id(12));

UPDATE 99th_output a INNER JOIN employer_mean_deviation b
 ON a.sector = b.sector and a.land_use = b.land_use 
 SET a.AVG_IMPUTED_SQFT_PER_JOB = b.AVG
; 

##########################################################################################################
# Update existing parcel tables with new imputed sqft values
# Create proportionate amount of sqft per sector land use to add/subtract from existing parcel sqft values.
##########################################################################################################

DROP TABLE IF EXISTS tmp_prop_jobs;
DROP TABLE IF EXISTS tmp_prcl_jobs;

CREATE TABLE tmp_prop_jobs 
 (PARCEL_ID MEDIUMTEXT, SECTOR MEDIUMTEXT, LAND_USE MEDIUMTEXT, SQFT DOUBLE, JOBS INT, PERCENT_JOBS DOUBLE, IMPUTED_SQFT DOUBLE, TAXEXEMPT INT)
; 
 
INSERT INTO tmp_prop_jobs (PARCEL_ID, SECTOR, LAND_USE, SQFT, JOBS, TAXEXEMPT)  
 SELECT PARCEL_ID, SECTOR, LAND_USE, SQFT, JOBS, TAXEXEMPT 
 FROM prelim_sqft_job_ratio 
 GROUP BY PARCEL_ID, SECTOR, LAND_USE, TAXEXEMPT 
;

ALTER TABLE tmp_prop_jobs ADD INDEX sctr_lu_indx(sector(15), land_use(15));
ALTER TABLE tmp_prop_jobs ADD INDEX prcl_indx(parcel_id(12));

CREATE TABLE tmp_prcl_jobs 
 SELECT PARCEL_ID, SUM(JOBS) AS TOTAL_JOBS
 FROM prelim_sqft_job_ratio 
 GROUP BY PARCEL_ID
; 

ALTER TABLE tmp_prcl_jobs add index prcl_indx(parcel_id(12));

UPDATE tmp_prop_jobs AS a 
 INNER JOIN tmp_prcl_jobs b 
 ON a.parcel_id = b.parcel_id 
 SET a.PERCENT_JOBS = a.JOBS / b.TOTAL_JOBS
; 

UPDATE tmp_prop_jobs AS a 
 INNER JOIN employer_mean_deviation b 
  ON a.sector = b.sector AND a.land_use = b.land_use
 SET a.IMPUTED_SQFT = a.PERCENT_JOBS * b.AVG 
;

##############################################################
# Create tables with imputed 10th and 99th percentile records.
##############################################################

DROP TABLE IF EXISTS tmp_10th_imputed;
DROP TABLE IF EXISTS tmp_99th_imputed;
DROP TABLE IF EXISTS tmp_imputed_records;

# 2/3/05 changed from 'LEFT JOIN' to 'INNER JOIN'
CREATE TABLE tmp_10th_imputed
 SELECT a.*, b.AVG_IMPUTED_SQFT_PER_JOB 
 FROM tmp_prop_jobs a 
 INNER JOIN 10th_output b 
 ON a.parcel_id = b.parcel_id and a.sector = b.sector and a.land_use = b.land_use
 WHERE b.parcel_id is not null
; 
 
# 2/3/05 changed from 'LEFT JOIN' to 'INNER JOIN' 
CREATE TABLE tmp_99th_imputed
 SELECT a.*, b.AVG_IMPUTED_SQFT_PER_JOB 
 FROM tmp_prop_jobs a 
 INNER JOIN 99th_output b 
 ON a.parcel_id = b.parcel_id and a.sector = b.sector and a.land_use = b.land_use
 WHERE b.parcel_id is not null
;

ALTER TABLE tmp_10th_imputed ADD INDEX prcl_indx(parcel_id(11));
ALTER TABLE tmp_10th_imputed ADD COLUMN WEIGHTED_SQFT DOUBLE;
ALTER TABLE tmp_99th_imputed ADD INDEX prcl_indx(parcel_id(11));
ALTER TABLE tmp_99th_imputed ADD COLUMN WEIGHTED_SQFT DOUBLE;

UPDATE tmp_10th_imputed SET WEIGHTED_SQFT = JOBS * IMPUTED_SQFT 
 WHERE SQFT = 0 OR TAXEXEMPT = 1
;

# Added 4.27.04
#UPDATE tmp_10th_imputed SET WEIGHTED_SQFT = IMPUTED_SQFT 
#WHERE WEIGHTED_SQFT = 0 OR WEIGHTED_SQFT IS NULL;

 UPDATE tmp_10th_imputed SET WEIGHTED_SQFT = IMPUTED_SQFT 
 WHERE SQFT <> 0 OR WEIGHTED_SQFT IS NULL
; 

UPDATE tmp_99th_imputed SET WEIGHTED_SQFT = IMPUTED_SQFT;

# Sum weighted sqft and group by parcel to update 'parcels' table.
DROP TABLE IF EXISTS tmp_10th_imputed_sqft;
DROP TABLE IF EXISTS tmp_99th_imputed_sqft;

CREATE TABLE tmp_10th_imputed_sqft 
 SELECT PARCEL_ID, SUM(WEIGHTED_SQFT) AS WEIGHTED_SQFT
 FROM tmp_10th_imputed 
 GROUP BY PARCEL_ID
; 

CREATE TABLE tmp_99th_imputed_sqft
 SELECT PARCEL_ID, SUM(WEIGHTED_SQFT) AS WEIGHTED_SQFT
 FROM tmp_99th_imputed
 WHERE TAXEXEMPT <> 1
 GROUP BY PARCEL_ID
;

# Append 10th and 99th percentile tables

CREATE TABLE tmp_imputed_records 
 (PARCEL_ID MEDIUMTEXT, WEIGHTED_SQFT DOUBLE, PERCENTILE INT);
 
INSERT INTO tmp_imputed_records (PARCEL_ID, WEIGHTED_SQFT, PERCENTILE)
 SELECT PARCEL_ID, WEIGHTED_SQFT, 1 AS PERCENTILE FROM tmp_10th_imputed_sqft
; 

ALTER TABLE tmp_imputed_records ADD INDEX prcl_indx(parcel_id(11));

UPDATE tmp_imputed_records AS a INNER JOIN tmp_99th_imputed_sqft AS b 
 ON a.parcel_id = b.parcel_id 
 SET a.WEIGHTED_SQFT = a.WEIGHTED_SQFT - b.WEIGHTED_SQFT
;

INSERT INTO tmp_imputed_records (PARCEL_ID, WEIGHTED_SQFT, PERCENTILE) 
 SELECT a.PARCEL_ID, a.WEIGHTED_SQFT, 9 AS PERCENTILE FROM tmp_99th_imputed_sqft AS a 
 LEFT JOIN tmp_10th_imputed_sqft as b ON a.parcel_id = b.parcel_id 
 WHERE b.parcel_id is null
; 

#ALTER TABLE tmp_10th_imputed_sqft ADD INDEX prcl_indx(parcel_id(11));
#ALTER TABLE tmp_99th_imputed_sqft ADD INDEX prcl_indx(parcel_id(11));

##############################################################
# Update parcels tables with new sqft values
##############################################################

SET SESSION big_tables = 1;

ALTER TABLE parcels ADD COLUMN IMPUTED_SQFT double;
ALTER TABLE parcels ADD INDEX prcl_indx(parcel_id(11));

UPDATE parcels SET IMPUTED_SQFT = NULL;

UPDATE parcels AS a 
 INNER JOIN tmp_imputed_records AS b 
 ON a.parcel_id = b.parcel_id 
 SET a.IMPUTED_SQFT = (a.SQUARE_FOOTAGE + b.WEIGHTED_SQFT)
 WHERE b.PERCENTILE = 1
;

UPDATE parcels AS a 
 INNER JOIN tmp_imputed_records AS b 
 ON a.parcel_id = b.parcel_id 
 SET a.IMPUTED_SQFT = (a.SQUARE_FOOTAGE - b.WEIGHTED_SQFT)
 WHERE b.PERCENTILE = 9
;

UPDATE parcels SET IMPUTED_SQFT = SQUARE_FOOTAGE
 WHERE IMPUTED_SQFT IS NULL
; 

# UPDATE parcels AS a 
#  INNER JOIN tmp_10th_imputed_sqft AS b 
#  ON a.parcel_id = b.parcel_id 
#  SET a.IMPUTED_SQFT = (a.SQUARE_FOOTAGE + b.WEIGHTED_SQFT)
# ; 

# UPDATE parcels AS a 
#  INNER JOIN tmp_99th_imputed_sqft AS b 
#  ON a.parcel_id = b.parcel_id 
#  SET a.IMPUTED_SQFT = (a.IMPUTED_SQFT - b.WEIGHTED_SQFT) 
# ;

#########################################################################
# Allocate the imputed sqft values proportionately to the buildings table
#########################################################################

DROP TABLE IF EXISTS tmp_total_building_sqft; 
DROP TABLE IF EXISTS weighted_buildings;

ALTER TABLE buildings ADD INDEX prcl_indx(parcel_id(11));

CREATE TEMPORARY TABLE tmp_total_building_sqft 
 SELECT PARCEL_ID, SUM(BUILT_SQFT) AS BUILT_SQFT 
 FROM buildings
 GROUP BY PARCEL_ID
; 

ALTER TABLE tmp_total_building_sqft ADD INDEX prcl_indx(parcel_id(11));

CREATE TABLE weighted_buildings
 (PARCEL_ID mediumtext, BUILT_SQFT INT, PERCENT_BUILDING DOUBLE, IMPUTED_SQFT DOUBLE)
; 

INSERT INTO weighted_buildings (parcel_id, built_sqft, percent_building)
 SELECT 
 	a.PARCEL_ID,
 	c.BUILT_SQFT,
 	(c.BUILT_SQFT / b.BUILT_SQFT) as PERCENT_BUILDING
 FROM tmp_imputed_records AS a 
 LEFT JOIN buildings c
  ON (a.parcel_id = c.parcel_id)
 LEFT JOIN tmp_total_building_sqft AS b
  ON a.parcel_id = b.parcel_id 
;

ALTER TABLE weighted_buildings ADD INDEX prcl_indx(parcel_id(12));

UPDATE weighted_buildings SET PERCENT_BUILDING = 1 WHERE PERCENT_BUILDING IS NULL;


# INSERT INTO weighted_buildings (parcel_id, built_sqft, percent_building)
#  SELECT 
#  	a.PARCEL_ID,
#  	a.BUILT_SQFT,
#  	(a.BUILT_SQFT / b.BUILT_SQFT) as PERCENT_BUILDING
#  FROM buildings AS a INNER JOIN tmp_total_building_sqft AS b
#  ON a.parcel_id = b.parcel_id
# ;

# ALTER TABLE weighted_buildings ADD INDEX prcl_indx(parcel_id(11));
# 

UPDATE weighted_buildings AS a 
 INNER JOIN parcels b ON a.parcel_id = b.parcel_id 
 SET a.IMPUTED_SQFT = a.PERCENT_BUILDING * b.IMPUTED_SQFT
;

ALTER TABLE weighted_buildings ADD INDEX blt_sqft_indx(built_sqft);
 
########################################################################################
# Create new building records to buildings table where records did not exist.
########################################################################################

DROP TABLE IF EXISTS prelim_new_building_records;
DROP TABLE IF EXISTS new_building_records;

CREATE TABLE prelim_new_building_records 
 SELECT a.PARCEL_ID, 
 	a.USE_CODE,
 	a.YEAR_BUILT,
 	c.WEIGHTED_SQFT AS IMPUTED_SQFT
 FROM prelim_employers_to_parcels AS a 
 INNER JOIN tmp_imputed_records c ON (a.parcel_id = c.parcel_id)
 LEFT JOIN buildings AS b ON a.parcel_id = b.parcel_id
  WHERE b.parcel_id is null
; 

CREATE TABLE new_building_records SELECT PARCEL_ID, USE_CODE, YEAR_BUILT, IMPUTED_SQFT 
 FROM prelim_new_building_records GROUP BY PARCEL_ID, USE_CODE, YEAR_BUILT, IMPUTED_SQFT
; 

#######################################################################################
# Update buildings table with new imputed sqft values from weighted_buildings
# Append new building records to existing buildings table
#######################################################################################

# Update buildings table with imputed sqft

ALTER TABLE buildings ADD COLUMN IMPUTE_FLAG TINYINT;
ALTER TABLE buildings ADD COLUMN IMPUTED_SQFT DOUBLE;
ALTER TABLE buildings ADD INDEX blt_sqft_indx(built_sqft);

UPDATE buildings AS a INNER JOIN weighted_buildings AS b 
 ON a.parcel_id = b.parcel_id and a.built_sqft = b.built_sqft
 SET a.IMPUTED_SQFT = b.IMPUTED_SQFT
; 

UPDATE buildings SET IMPUTE_FLAG = 1 WHERE IMPUTED_SQFT is not null;
UPDATE buildings SET IMPUTED_SQFT = BUILT_SQFT WHERE IMPUTED_SQFT is null or IMPUTED_SQFT = 0;

# Append new building records

INSERT INTO buildings (YEAR_BUILT, BUILDING_USE, PARCEL_ID, IMPUTED_SQFT, COUNTY, IMPUTE_FLAG)
 SELECT YEAR_BUILT, NULL AS BUILDING_USE, PARCEL_ID, IMPUTED_SQFT, '035' AS COUNTY, 2 AS IMPUTE_FLAG 
 FROM new_building_records
; 

ALTER TABLE parcels ADD INDEX cnty_lu_indx(county(3), use_code);

UPDATE ((buildings a 
	INNER JOIN parcels b
	ON a.parcel_id = b.parcel_id)
	INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass c
	ON b.county = c.county and b.use_code = c.county_land_use_code)
	LEFT JOIN PSRC_2000_data_quality_indicators.building_use_generic_reclass bu
	ON a.county = bu.county and a.building_use = bu.county_building_use_code
 SET a.building_use = concat('Imputed - ', c.generic_land_use_1)
 WHERE a.building_use is null or a.building_use = '0' or bu.generic_building_use_1 = 'Basement'
;

# Delete tables
DROP TABLE percentile_rows;
DROP TABLE percentiles;
DROP TABLE row_limits;
DROP TABLE prelim_sector_land_use_percentile;
DROP TABLE 10th_records;
DROP TABLE 99th_records;
DROP TABLE 10th_output;
DROP TABLE 99th_output;
DROP TABLE tmp_prop_jobs;
DROP TABLE tmp_prcl_jobs;
DROP TABLE tmp_10th_imputed;
DROP TABLE tmp_99th_imputed;
DROP TABLE tmp_10th_imputed_sqft;
DROP TABLE tmp_99th_imputed_sqft;
DROP TABLE tmp_imputed_records;
# DROP TABLE tmp_total_building_sqft;
# DROP TABLE weighted_buildings;
DROP TABLE prelim_new_building_records;

--
## Summary Table of buildings sqft at Generic Building Use 1

 alter table buildings add index cnty_bu_indx(county(3), building_use(15));

 create temporary table tmp_total_bldgsqft_bu1
  select a.generic_building_use_1, sum(b.built_sqft) as built_sqft, sum(b.imputed_sqft) as imputed_sqft
  from PSRC_2000_data_quality_indicators.building_use_generic_reclass a inner join buildings b 
  on a.county = b.county and a.county_building_use_code = b.building_use
  group by a.generic_building_use_1
 ; 

# create temporary table tmp_parcel_bldgsqft_bu1
#  select a.generic_building_use_1, sum(b.built_sqft) as built_sqft, sum(b.imputed_sqft) as imputed_sqft
#  from PSRC_2000_data_quality_indicators.building_use_generic_reclass a inner join buildings b 
#  on a.county = b.county and a.county_building_use_code = b.building_use
#  inner join parcels c on b.parcel_id = c.parcel_id
#  where c.parcel_id is not null
#  group by a.generic_building_use_1
# ; 

--
## Summary Table of buildings sqft at Generic Building Use 2 

 create temporary table tmp_total_bldgsqft_bu2
  select a.generic_building_use_2, sum(b.built_sqft) as built_sqft, sum(b.imputed_sqft) as imputed_sqft
  from PSRC_2000_data_quality_indicators.building_use_generic_reclass a inner join buildings b 
  on a.county = b.county and a.county_building_use_code = b.building_use
  group by a.generic_building_use_2
 ;

# create temporary table tmp_parcel_bldgsqft_bu2
#  select a.generic_building_use_2, sum(b.built_sqft) as built_sqft, sum(b.imputed_sqft) as imputed_sqft
#  from PSRC_2000_data_quality_indicators.building_use_generic_reclass a inner join buildings b 
#  on a.county = b.county and a.county_building_use_code = b.building_use
#  inner join parcels c on b.parcel_id = c.parcel_id
#  where c.parcel_id is not null
#  group by a.generic_building_use_2
# ;

--
## Create temporary table schools

# create temporary table tmp_school_bldgsqft select a.parcel_id, a.imputed_sqft from buildings a 
# inner join PSRC_2000_data_quality_indicators.building_use_generic_reclass b on a.county = b.county and a.building_use = b.county_building_use_code
# where b.generic_building_use_1 = 'School';

# create temporary table tmp_schools (parcel_id text, built_sqft double, old_imputed_sqft double, new_imputed_sqft double);
# insert into tmp_schools (parcel_id, built_sqft, old_imputed_sqft) select parcel_id, built_sqft, imputed_sqft from kitsap_schools; 
# insert into tmp_schools (parcel_id, new_imputed_sqft) select a.parcel_id, a.imputed_sqft from tmp_school_bldgsqft a left join kitsap_schools b
# on a.parcel_id = b.parcel_id where b.parcel_id is null;

--
## Test query for total jobs per non_res_sqft

# CREATE TABLE city_sqft (CITY_NAME TEXT, NONRES_SQFT DOUBLE, JOBS INT, JOBS_PER_1000_SQFT DOUBLE, COUNTY varchar(3));
# 
# ALTER TABLE gridcells ADD INDEX city_indx(city_id);
# ALTER TABLE jobs ADD INDEX grid_indx(grid_id);
# 
# INSERT INTO city_sqft (city_name, nonres_sqft, county)
#  SELECT b.CITY_NAME, sum(a.total_nonres_sqft) as NONRES_SQFT, a.county_id as COUNTY 
#  FROM gridcells AS a
#  INNER JOIN cities AS b ON (a.city_id = b.city_id)
#  GROUP BY b.CITY_NAME
# ; 

# CREATE TEMPORARY TABLE tmp_jobs
# SELECT c.CITY_NAME, COUNT(*) AS JOBS 
#  FROM jobs AS a
#  INNER JOIN gridcells AS b ON (a.GRID_ID = b.GRID_ID)
#  INNER JOIN cities AS c ON b.CITY_ID = c.CITY_ID
#  GROUP BY c.CITY_NAME
# ; 

# ALTER TABLE tmp_jobs ADD INDEX city_indx(city_name(30));
# ALTER TABLE city_sqft ADD INDEX city_indx(city_name(30));

# UPDATE city_sqft AS a 
#  INNER JOIN tmp_jobs AS b ON a.city_name = b.city_name
#  SET a.JOBS = b.JOBS;

# UPDATE city_sqft as a 
#  INNER JOIN tmp_jobs as b ON a.city_name = b.city_name
#  SET a.JOBS_PER_1000_SQFT = ((b.JOBS / a.NONRES_SQFT)*1000);
# 

