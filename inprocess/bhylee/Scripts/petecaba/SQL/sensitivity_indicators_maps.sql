########################################################
## Main Indicator table for 2000 Baseline Scenario run #
########################################################


# USE PSRC_2000_base_run_output;



CREATE TABLE TAZ_INDICATORS
 (ZONE_ID INT, 
  HH_2000 INT, 
  HH_2030 INT, 
  CH_HH_2000_2030 DOUBLE, 
  AVG_HH_SZ_2000 DOUBLE, 
  AVG_HH_SZ_2030 DOUBLE,
  AVG_HH_INC_2000 DOUBLE, 
  AVG_HH_INC_2030 DOUBLE,
  JOBS_2000 INT,
  JOBS_2030 INT,
  CH_JOBS_2000_2030 DOUBLE,
  HH_UNITS_2000 INT, 
  HH_UNITS_2030 INT,
  CH_HU_2000_2030 DOUBLE,
  RES_VAC_RATE_2000 DOUBLE,
  RES_VAC_RATE_2030 DOUBLE,
  NONRES_SQFT_2000 INT,
  NONRES_SQFT_2030 INT,
  CH_NONRES_FLSP_2000_2030 DOUBLE,
  NONRES_VAC_RATE_2000 DOUBLE,
  NONRES_VAC_RATE_2030 DOUBLE,
  SOV_ACCESS_2000 DOUBLE,
  SOV_ACCESS_2030 DOUBLE,
  CH_SOV_ACCESS_2000_2030 DOUBLE,
  TRNST_ACCESS_2000 DOUBLE,
  TRNST_ACCESS_2030 DOUBLE,
  CH_TRNST_ACCESS_2000_2030 DOUBLE,
  LP_2000 INT,
  LP_2030 INT,
  CH_LP_2000_2030 DOUBLE);

INSERT INTO TAZ_INDICATORS (ZONE_ID) SELECT DISTINCT ZONE_ID FROM GSPSRC_2000_baseyear_flattened.gridcells;
ALTER TABLE TAZ_INDICATORS ADD INDEX ZONE_ID_INDEX(ZONE_ID);

 #########################
 # Households Indicators #
 #########################
 
 # 2000 HH characteristics
 
 CREATE TEMPORARY TABLE tmp_hh_characteristics_2000
  SELECT b.ZONE_ID, count(*) as HOUSEHOLDS, SUM(a.persons) AS PERSONS, SUM(a.income) AS INCOME
  FROM GSPSRC_2000_baseyear_flattened.households a 
  INNER JOIN GSPSRC_2000_baseyear_flattened.gridcells b 
  ON a.grid_id = b.grid_id
 GROUP BY b.ZONE_ID;
 
 ALTER TABLE tmp_hh_characteristics_2000 ADD INDEX zone_id_index(zone_id);
 
 UPDATE TAZ_INDICATORS a 
  INNER JOIN tmp_hh_characteristics_2000 b
  ON a.ZONE_ID = b.ZONE_ID
  SET a.HH_2000 = b.households;
 
 UPDATE TAZ_INDICATORS a 
  INNER JOIN tmp_hh_characteristics_2000 b
  ON a.ZONE_ID = b.ZONE_ID
  SET a.AVG_HH_SZ_2000 = b.PERSONS / a.HH_2000;
 
 UPDATE TAZ_INDICATORS a 
  INNER JOIN tmp_hh_characteristics_2000 b
  ON a.ZONE_ID = b.ZONE_ID
 SET a.AVG_HH_INC_2000 = b.INCOME / a.HH_2000;
 

# 2030 HH characteristics
/*
CREATE TEMPORARY TABLE tmp_hh_characteristics_2030
 SELECT ZONE_ID, count(*) as HOUSEHOLDS, SUM(PERSONS) as PERSONS, SUM(INCOME) AS INCOME
 FROM households_exported_denormalized a 
 WHERE YEAR = 2030
GROUP BY ZONE_ID;

ALTER TABLE tmp_hh_characteristics_2030 ADD INDEX zone_id_index(zone_id);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_hh_characteristics_2030 b
 ON a.ZONE_ID = b.ZONE_ID
 SET a.HH_2030 = b.households;

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_hh_characteristics_2030 b
 ON a.ZONE_ID = b.ZONE_ID
 SET a.AVG_HH_SZ_2030 = b.PERSONS / a.HH_2030;

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_hh_characteristics_2030 b
 ON a.ZONE_ID = b.ZONE_ID
 SET a.AVG_HH_INC_2030 = b.INCOME / a.HH_2030; 
*/
#
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

# Change Household characteristics

UPDATE TAZ_INDICATORS SET CH_HH_2000_2030 = HH_2030 - HH_2000;


########################
# Employment Indicators#
########################

# CREATE 2000 Jobs

CREATE TEMPORARY TABLE tmp_jobs_2000
 SELECT b.ZONE_ID, COUNT(*) AS JOBS 
 FROM GSPSRC_2000_baseyear_flattened.jobs a 
 INNER JOIN GSPSRC_2000_baseyear_flattened.gridcells b 
 ON a.grid_id = b.grid_id
GROUP BY b.ZONE_ID;

ALTER TABLE tmp_jobs_2000 ADD INDEX zone_id(zone_id);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_jobs_2000 b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.JOBS_2000 = b.JOBS;

# CREATE 2030 Jobs
/*
CREATE TEMPORARY TABLE tmp_jobs_2030
  SELECT ZONE_ID, COUNT(*) AS JOBS 
  FROM jobs_exported_denormalized
  WHERE YEAR = 2030
GROUP BY ZONE_ID;

ALTER TABLE tmp_jobs_2030 ADD INDEX zone_id(zone_id);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_jobs_2030 b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.JOBS_2030 = b.JOBS; 
*/
#

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

# Change Employment characteristics

UPDATE TAZ_INDICATORS SET CH_JOBS_2000_2030 = JOBS_2030 - JOBS_2000;

#########
# Units #
#########

# 2000 Residential Units

CREATE TEMPORARY TABLE tmp_units_2000
 SELECT ZONE_ID, SUM(RESIDENTIAL_UNITS) AS UNITS 
 FROM GSPSRC_2000_baseyear_flattened.gridcells 
GROUP BY ZONE_ID;

ALTER TABLE tmp_units_2000 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_units_2000 b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.HH_UNITS_2000 = b.UNITS;

# 2030 Residential Units

CREATE TEMPORARY TABLE tmp_units_2030
 SELECT ZONE_ID, SUM(RESIDENTIAL_UNITS) AS UNITS 
 FROM gridcells_exported_denormalized
 WHERE YEAR = 2030
GROUP BY ZONE_ID;

ALTER TABLE tmp_units_2030 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_units_2030 b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.HH_UNITS_2030 = b.UNITS;

# Change 2000 - 2030 units

UPDATE TAZ_INDICATORS SET CH_HU_2000_2030 = HH_UNITS_2030 - HH_UNITS_2000;

# 2000 Residential Vacancy Rate 

UPDATE TAZ_INDICATORS SET RES_VAC_RATE_2000 = ROUND(1-(hh_2000/hh_units_2000),4);


# 2030 Residential Vacancty Rate

UPDATE TAZ_INDICATORS SET RES_VAC_RATE_2030 = ROUND(1-(hh_2030/hh_units_2030),4);

############################
# 2000 Nonresidential sqft #
############################

# 2000 Nonresidential Sqft

CREATE TEMPORARY TABLE tmp_nonres_sqft_2000
 SELECT ZONE_ID, SUM(COMMERCIAL_SQFT + INDUSTRIAL_SQFT + GOVERNMENTAL_SQFT) AS SQFT
 FROM GSPSRC_2000_baseyear_flattened.gridcells
GROUP BY ZONE_ID;

ALTER TABLE tmp_nonres_sqft_2000 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_nonres_sqft_2000 b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.NONRES_SQFT_2000 = b.SQFT;

# 2030 Nonresidential Sqft 

CREATE TEMPORARY TABLE tmp_nonres_sqft_2030
 SELECT ZONE_ID, SUM(COMMERCIAL_SQFT + INDUSTRIAL_SQFT + GOVERNMENTAL_SQFT) AS SQFT
 FROM gridcells_exported_denormalized 
 WHERE YEAR = 2030
GROUP BY ZONE_ID;

ALTER TABLE tmp_nonres_sqft_2030 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_nonres_sqft_2030 b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.NONRES_SQFT_2030 = b.SQFT;

# 2000 - 2030 Change SQFT 

UPDATE TAZ_INDICATORS SET CH_NONRES_FLSP_2000_2030 = NONRES_SQFT_2030 - NONRES_SQFT_2000;

# 2000 Nonresidential Vacancy Rate

CREATE TEMPORARY TABLE tmp_jobs_nhb_2000
 SELECT GRID_ID, COUNT(*) AS JOBS
 FROM GSPSRC_2000_baseyear_flattened.jobs
 WHERE HOME_BASED = 0
GROUP BY GRID_ID;

ALTER TABLE tmp_jobs_nhb_2000 ADD UNIQUE INDEX GRID_ID(GRID_ID);

CREATE TEMPORARY TABLE tmp_sqft_2000 
 SELECT a.GRID_ID, 
 	SUM(a.COMMERCIAL_SQFT + a.INDUSTRIAL_SQFT + a.GOVERNMENTAL_SQFT) AS TOTAL_SQFT,
 	b.SQFT AS SQFT_PER_JOB
 FROM GSPSRC_2000_baseyear_flattened.gridcells a 
 INNER JOIN sqft_for_non_home_based_jobs b 
 ON a.DEVELOPMENT_TYPE_ID = b.DEVELOPMENT_TYPE_ID
GROUP BY a.GRID_ID;
 
ALTER TABLE tmp_sqft_2000 ADD UNIQUE INDEX GRID_ID(GRID_ID);
 
CREATE TEMPORARY TABLE tmp_vac_rate_2000
 SELECT a.ZONE_ID, 
 	ROUND(1 - SUM(c.JOBS * b.SQFT_PER_JOB) / SUM(b.TOTAL_SQFT), 4) AS NONRES_VAC_RATE
 FROM GSPSRC_2000_baseyear_flattened.gridcells a 
 INNER JOIN tmp_sqft_2000 b
  ON a.GRID_ID = b.GRID_ID
 LEFT JOIN tmp_jobs_nhb_2000 c
  ON b.GRID_ID = c.GRID_ID
GROUP BY a.ZONE_ID;

ALTER TABLE tmp_vac_rate_2000 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_vac_rate_2000 b 
 ON a.ZONE_ID = b.zone_id
SET a.NONRES_VAC_RATE_2000 = b.NONRES_VAC_RATE;

DROP TABLE tmp_jobs_nhb_2000;
DROP TABLE tmp_sqft_2000;
DROP TABLE tmp_vac_rate_2000;


/*
CREATE TEMPORARY TABLE tmp_jobs_nhb_2000
 SELECT b.ZONE_ID, COUNT(*) AS JOBS 
 FROM GSPSRC_2000_baseyear_flattened.jobs a 
 INNER JOIN GSPSRC_2000_baseyear_flattened.gridcells b
 ON a.GRID_ID = b.GRID_ID
 WHERE HOME_BASED = 0
GROUP BY b.ZONE_ID;

ALTER TABLE tmp_jobs_nhb_2000 ADD INDEX ZONE_ID(ZONE_ID);

CREATE TEMPORARY TABLE tmp_sqft_2000
 SELECT a.ZONE_ID, 
 SUM(a.COMMERCIAL_SQFT + a.INDUSTRIAL_SQFT + a.GOVERNMENTAL_SQFT) AS NONRES_SQFT,
 b.SQFT as SQFT_PER_JOB 
 FROM GSPSRC_2000_baseyear_flattened.gridcells a
 INNER JOIN sqft_for_non_home_based_jobs b
 ON a.DEVELOPMENT_TYPE_ID = b.DEVELOPMENT_TYPE_ID
GROUP BY a.ZONE_ID;

ALTER TABLE tmp_sqft_2000 ADD INDEX ZONE_ID(ZONE_ID);

CREATE TEMPORARY TABLE tmp_vac_rate_2000
 SELECT a.ZONE_ID, ROUND(1-SUM(b.JOBS * a.SQFT_PER_JOB) / SUM(a.NONRES_SQFT),4) AS NONRES_VAC_RATE
 FROM tmp_sqft_2000 a 
 LEFT JOIN tmp_jobs_nhb_2000 b 
 ON a.zone_id = b.zone_id
GROUP BY a.zone_id;

ALTER TABLE tmp_vac_rate_2000 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_vac_rate_2000 b
 ON a.ZONE_ID = b.ZONE_ID
SET NONRES_VAC_RATE_2000 = b.NONRES_VAC_RATE;
*/

# 2030 Nonresidential Vacancty Rate

CREATE TEMPORARY TABLE tmp_jobs_nhb_2030
 SELECT GRID_ID, COUNT(*) AS JOBS
 FROM jobs_exported_denormalized
 WHERE HOME_BASED = 0 AND YEAR = 2030
GROUP BY GRID_ID;

ALTER TABLE tmp_jobs_nhb_2030 ADD UNIQUE INDEX GRID_ID(GRID_ID);

CREATE TEMPORARY TABLE tmp_sqft_2030 
 SELECT a.GRID_ID, 
 	SUM(a.COMMERCIAL_SQFT + INDUSTRIAL_SQFT + GOVERNMENTAL_SQFT) AS TOTAL_SQFT,
 	b.SQFT AS SQFT_PER_JOB
 FROM gridcells_exported_denormalized a 
 INNER JOIN sqft_for_non_home_based_jobs b 
 ON a.DEVELOPMENT_TYPE_ID = b.DEVELOPMENT_TYPE_ID
 WHERE a.YEAR = 2030
GROUP BY a.GRID_ID;
 
ALTER TABLE tmp_sqft_2030 ADD UNIQUE INDEX GRID_ID(GRID_ID);
 
CREATE TEMPORARY TABLE tmp_gridcells_exp_2030 
 SELECT * FROM gridcells_exported_denormalized 
 WHERE YEAR = 2030;
 
ALTER TABLE tmp_gridcells_exp_2030 ADD INDEX GRID_ID(GRID_ID);
 
CREATE TEMPORARY TABLE tmp_vac_rate_2030
 SELECT a.ZONE_ID, 
 	ROUND(1 - SUM(c.JOBS * b.SQFT_PER_JOB) / SUM(b.TOTAL_SQFT), 4) AS NONRES_VAC_RATE
 FROM tmp_gridcells_exp_2030 a 
 INNER JOIN tmp_sqft_2030 b
  ON a.GRID_ID = b.GRID_ID
 LEFT JOIN tmp_jobs_nhb_2030 c
  ON b.GRID_ID = c.GRID_ID
GROUP BY a.ZONE_ID;

ALTER TABLE tmp_vac_rate_2030 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_vac_rate_2030 b 
 ON a.ZONE_ID = b.zone_id
SET a.NONRES_VAC_RATE_2030 = b.NONRES_VAC_RATE;

DROP TABLE tmp_jobs_nhb_2030;
DROP TABLE tmp_sqft_2030;
DROP TABLE tmp_vac_rate_2030;

/*
CREATE TEMPORARY TABLE tmp_jobs_nhb_2030
 SELECT ZONE_ID, COUNT(*) AS JOBS
 FROM jobs_exported_denormalized
 WHERE HOME_BASED = 0 AND YEAR = 2030
GROUP BY ZONE_ID;

ALTER TABLE tmp_jobs_nhb_2030 ADD INDEX ZONE_ID(ZONE_ID);

CREATE TEMPORARY TABLE tmp_sqft_2030
 SELECT a.ZONE_ID, 
 SUM(a.COMMERCIAL_SQFT + a.INDUSTRIAL_SQFT + a.GOVERNMENTAL_SQFT) AS NONRES_SQFT,
 b.SQFT AS SQFT_PER_JOB 
 FROM gridcells_exported_denormalized a
 INNER JOIN sqft_for_non_home_based_jobs b
 ON a.DEVELOPMENT_TYPE_ID = b.DEVELOPMENT_TYPE_ID
 WHERE a.YEAR = 2030
GROUP BY a.ZONE_ID;

ALTER TABLE tmp_sqft_2030 ADD INDEX ZONE_ID(ZONE_ID);

CREATE TEMPORARY TABLE tmp_vac_rate_2030
 SELECT a.ZONE_ID, 
 ROUND(1-SUM(b.JOBS * a.SQFT_PER_JOB) / SUM(a.NONRES_SQFT),4) AS NONRES_VAC_RATE
 FROM tmp_sqft_2030 a 
 LEFT JOIN tmp_jobs_nhb_2030 b 
 ON a.zone_id = b.zone_id
GROUP BY a.zone_id;

ALTER TABLE tmp_vac_rate_2030 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_vac_rate_2030 b
 ON a.ZONE_ID = b.ZONE_ID
SET NONRES_VAC_RATE_2030 = b.NONRES_VAC_RATE;
*/

###################
# Accessibilities #
###################

# 2030 Logsum-weighted access to employment by SOV and 
# logsum-weighted access to employment by transit

CREATE TEMPORARY TABLE tmp_log_acc_emp_sov_and_trnst
 SELECT ZONE_ID, 
 	HOME_ACCESS_TO_EMPLOYMENT_1 AS LN_ACC_EMP_SOV,
 	HOME_ACCESS_TO_EMPLOYMENT_0 AS LN_ACC_EMP_TRNST
 FROM accessibilities 
 WHERE YEAR = 2030;

ALTER TABLE tmp_log_acc_emp_sov_and_trnst ADD INDEX ZONE_ID(ZONE_ID);
 
UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_log_acc_emp_sov_and_trnst b
 ON a.ZONE_ID = b.ZONE_ID
 SET a.SOV_ACCESS_2030 = b.LN_ACC_EMP_SOV;
 
UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_log_acc_emp_sov_and_trnst b
 ON a.ZONE_ID = b.ZONE_ID
 SET a.TRNST_ACCESS_2030 = b.LN_ACC_EMP_TRNST;

# 2030 - 2000 Logsum-weighted change in SOV accesibility

?

##############
# Land Price #
##############

# 2000 Land Price 

CREATE TEMPORARY TABLE tmp_lp_2000
 SELECT ZONE_ID, SUM(RESIDENTIAL_LAND_VALUE + NONRESIDENTIAL_LAND_VALUE) AS TOTAL_LP
 FROM GSPSRC_2000_baseyear_flattened.gridcells 
GROUP BY ZONE_ID;

ALTER TABLE tmp_lp_2000 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_lp_2000 b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.LP_2000 = b.TOTAL_LP;

# 2030 Land Price

CREATE TEMPORARY TABLE tmp_lp_2030
 SELECT ZONE_ID, SUM(RESIDENTIAL_LAND_VALUE + NONRESIDENTIAL_LAND_VALUE) AS TOTAL_LP
 FROM gridcells_exported_denormalized
 WHERE YEAR = 2030
GROUP BY ZONE_ID;

ALTER TABLE tmp_lp_2030 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_lp_2030 b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.LP_2030 = b.TOTAL_LP;

# 2000 - 2030 Change Map 

UPDATE TAZ_INDICATORS SET CH_LP_2000_2030 = LP_2030 - LP_2000;

###########################################################################################################

