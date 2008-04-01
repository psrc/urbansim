########################################################
## Main Indicator table for 2000 Scenario A No UGB run #
########################################################


# USE PSRC_2000_base_run_output;

CREATE TABLE TAZ_INDICATORS
 (ZONE_ID INT, 
  HH_2000_BASE INT, 
  HH_2000 INT, 
  CH_HH_2000_BASE_2000 DOUBLE, 
  AVG_HH_SZ_2000_BASE DOUBLE, 
  AVG_HH_SZ_2000 DOUBLE,
  CH_AVG_SZ_2000_BASE_2000 DOUBLE,
  AVG_HH_INC_2000_BASE DOUBLE, 
  AVG_HH_INC_2000 DOUBLE,
  CH_AVG_HH_INC_2000_BASE_2000 DOUBLE,
  JOBS_2000_BASE INT,
  JOBS_2000 INT,
  CH_JOBS_2000_BASE_2000 DOUBLE,
  HH_UNITS_2000_BASE INT, 
  HH_UNITS_2000 INT,
  CH_HU_2000_BASE_2000 DOUBLE,
  RES_VAC_RATE_2000_BASE DOUBLE,
  RES_VAC_RATE_2000 DOUBLE,
  CH_RES_VAC_RATE_2000_BASE_2000 DOUBLE,
  NONRES_SQFT_2000_BASE INT,
  NONRES_SQFT_2000 INT,
  CH_NONRES_FLSP_2000_2000 DOUBLE,
  NONRES_VAC_RATE_2000_BASE DOUBLE,
  NONRES_VAC_RATE_2000 DOUBLE,
  CH_NONRES_VAC_RATE_2000_BASE_2000 DOUBLE,
  SOV_ACCESS_2000_BASE DOUBLE,
  SOV_ACCESS_2000 DOUBLE,
  CH_SOV_ACCESS_2000_BASE_2000 DOUBLE,
  TRNST_ACCESS_2000_BASE DOUBLE,
  TRNST_ACCESS_2000 DOUBLE,
  CH_TRNST_ACCESS_2000_BASE_2000 DOUBLE,
  LP_2000_BASE INT,
  LP_2000 INT,
  CH_LP_2000_BASE_2000 DOUBLE);

INSERT INTO TAZ_INDICATORS (ZONE_ID) SELECT DISTINCT ZONE_ID FROM GSPSRC_2000_baseyear_flattened.gridcells;
ALTER TABLE TAZ_INDICATORS ADD INDEX ZONE_ID_INDEX(ZONE_ID);

 #########################
 # Households Indicators #
 ######################### 

# 2000 HH characteristics

create temporary table tmp_hh_characteristics_2000 
 select a.HOUSEHOLD_ID, 
 	a.GRID_ID,
	a.PERSONS,
	a.WORKERS,
	a.AGE_OF_HEAD,
	a.INCOME,
	a.CHILDREN,
	a.RACE_ID,
	a.CARS,
	b.ZONE_ID
 from GSPSRC_2000_baseyear_change_20050428.households a 
  inner join GSPSRC_2000_baseyear_change_20050428.gridcells b
  on a.grid_id = b.grid_id
;
 
create temporary table tmp_household_character_2000
 select zone_id, count(*) as households, sum(persons) as persons, sum(income) as income
 from tmp_hh_characteristics_2000 group by zone_id;

alter table tmp_household_character_2000 add index zone_id(zone_id);

update TAZ_INDICATORS a
 inner join tmp_household_character_2000 b 
 on a.zone_id = b.zone_id 
 set a.hh_2000 = b.households;

update TAZ_INDICATORS a 
 inner join tmp_household_character_2000 b 
 on a.zone_id = b.zone_id 
 set a.avg_hh_sz_2000 = b.persons / a.hh_2000;
 
update TAZ_INDICATORS a 
 inner join tmp_household_character_2000 b 
 on a.zone_id = b.zone_id 
 set a.avg_hh_inc_2000 = b.income / a.hh_2000; 

# Change Scenario A 2000 - Baseline 2000 Households 

UPDATE TAZ_INDICATORS a 
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b 
 ON a.ZONE_ID = b.ZONE_ID
 SET a.CH_HH_2000_BASE_2000 = a.HH_2000 - b.HH_2000;

# Change Scenario A 2000 - Baseline 2000 Household Size

UPDATE TAZ_INDICATORS a
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b
 ON a.ZONE_ID = b.ZONE_ID
SET a.CH_AVG_HH_SZ_2000_BASE_2000 = a.AVG_HH_SZ_2000 - b.AVG_HH_SZ_2000;

# Change Scenario A 2000 - Baseline 2000 Household Income

UPDATE TAZ_INDICATORS a
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b
 ON a.ZONE_ID = b.ZONE_ID
SET a.CH_AVG_HH_INC_2000_BASE_2000 = a.AVG_HH_INC_2000 - b.AVG_HH_INC_2000;


########################
# Employment Indicators#
########################

# CREATE 2000 Jobs

create temporary table tmp_jobs_2000
 select a.JOB_ID,
 	a.GRID_ID,
 	a.HOME_BASED,
 	c.ZONE_ID
 from jobs_exported a inner join jobs_constants b 
  on a.job_id = b.job_id
 inner join GSPSRC_2000_baseyear_start.gridcells c 
  on a.grid_id = c.grid_Id
 where a.year = 2000
; 

create temporary table tmp_job_character_2000 
 select zone_id, count(*) as jobs 
 from tmp_jobs_2000 group by zone_id;
 
alter table tmp_job_character_2000 add index zone_id(zone_id);

update TAZ_INDICATORS a inner join tmp_job_character_2000 b 
 on a.zone_id = b.zone_id 
 set a.jobs_2000 = b.jobs;

# Change Scenario A 2000 - Baseline 2000 Employment characteristics

UPDATE TAZ_INDICATORS a
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b 
 ON a.ZONE_ID = b.ZONE_ID 
 SET a.CH_JOBS_2000_BASE_2000 = a.JOBS_2000 - b.JOBS_2000;

#########
# Units #
#########

# 2000 Residential Units

CREATE TEMPORARY TABLE tmp_units_2000
 SELECT b.ZONE_ID, SUM(a.RESIDENTIAL_UNITS) AS UNITS 
 FROM gridcells_exported_denormalized a 
 INNER JOIN GSPSRC_2000_baseyear_change_20041206.gridcells b 
 ON a.GRID_ID = b.GRID_ID
 WHERE a.YEAR = 2000
GROUP BY b.ZONE_ID;

ALTER TABLE tmp_units_2000 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_units_2000 b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.HH_UNITS_2000 = b.UNITS;

# Change Scenario A 2000 - Baseline 2000 units

UPDATE TAZ_INDICATORS a 
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.CH_HU_2000_BASE_2000 = a.HH_UNITS_2000 - b.HH_UNITS_2000;

# Scenario A 2000 Residential Vacancty Rate

UPDATE TAZ_INDICATORS SET RES_VAC_RATE_2000 = ROUND(1-(hh_2000/hh_units_2000),4);

# Change Scenario A 2000 - Baseline Vacancy Rate

UPDATE TAZ_INDICATORS a
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b
 ON a.ZONE_ID = b.ZONE_ID 
SET a.CH_RES_VAC_RATE_2000_BASE_2000 = a.RES_VAC_RATE_2000 - b.RES_VAC_RATE_2000;


############################
# 2000 Nonresidential sqft #
############################

# 2000 Nonresidential Sqft 

CREATE TEMPORARY TABLE tmp_nonres_sqft_2000
 SELECT b.ZONE_ID, SUM(a.COMMERCIAL_SQFT + a.INDUSTRIAL_SQFT + a.GOVERNMENTAL_SQFT) AS SQFT
 FROM gridcells_exported a 
 INNER JOIN GSPSRC_2000_baseyear_change_20041206.gridcells b 
 ON a.GRID_ID = b.GRID_ID
 WHERE b.YEAR = 2000
GROUP BY a.ZONE_ID;

ALTER TABLE tmp_nonres_sqft_2000 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_nonres_sqft_2000 b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.NONRES_SQFT_2000 = b.SQFT;

# Change Scenario A 2000 - Baseline 2000 Change SQFT 

UPDATE TAZ_INDICATORS a
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.CH_NONRES_FLSP_2000_BASE_2000 = a.NONRES_SQFT_2000 - b.NONRES_SQFT_2000;

# 2000 Nonresidential Vacancty Rate

CREATE TEMPORARY TABLE tmp_jobs_nhb_2000
 SELECT GRID_ID, COUNT(*) AS JOBS
 FROM jobs_exported_denormalized
 WHERE HOME_BASED = 0 AND YEAR = 2000
GROUP BY GRID_ID;

ALTER TABLE tmp_jobs_nhb_2000 ADD UNIQUE INDEX GRID_ID(GRID_ID);

CREATE TEMPORARY TABLE tmp_sqft_2000 
 SELECT a.GRID_ID, 
 	SUM(a.COMMERCIAL_SQFT + INDUSTRIAL_SQFT + GOVERNMENTAL_SQFT) AS TOTAL_SQFT,
 	b.SQFT AS SQFT_PER_JOB
 FROM gridcells_exported_denormalized a 
 INNER JOIN sqft_for_non_home_based_jobs b 
 ON a.DEVELOPMENT_TYPE_ID = b.DEVELOPMENT_TYPE_ID
 WHERE a.YEAR = 2000
GROUP BY a.GRID_ID;
 
ALTER TABLE tmp_sqft_2000 ADD UNIQUE INDEX GRID_ID(GRID_ID);
 
CREATE TEMPORARY TABLE tmp_gridcells_exp_2000 
 SELECT * FROM gridcells_exported_denormalized 
 WHERE YEAR = 2000;
 
ALTER TABLE tmp_gridcells_exp_2000 ADD INDEX GRID_ID(GRID_ID);
 
CREATE TEMPORARY TABLE tmp_vac_rate_2000
 SELECT a.ZONE_ID, 
 	ROUND(1 - SUM(c.JOBS * b.SQFT_PER_JOB) / SUM(b.TOTAL_SQFT), 4) AS NONRES_VAC_RATE
 FROM tmp_gridcells_exp_2000 a 
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

###################
# Accessibilities #
###################

# 2000 Logsum-weighted access to employment by SOV and logsum-weighted access to employment by transit

# Accessibilities table 'home_access_to_employment_1' as 1-car hosuehold
# Accessibilities table 'home_access_to_employment_0' as 0-car household transit 

CREATE TEMPORARY TABLE tmp_log_acc_emp_sov_and_trnst
 SELECT ZONE_ID, 
 	HOME_ACCESS_TO_EMPLOYMENT_1 AS LN_ACC_EMP_SOV,
 	HOME_ACCESS_TO_EMPLOYMENT_0 AS LN_ACC_EMP_TRNST
 FROM accessibilities 
 WHERE YEAR = 2000;

ALTER TABLE tmp_log_acc_emp_sov_and_trnst ADD INDEX ZONE_ID(ZONE_ID);
 
UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_log_acc_emp_sov_and_trnst b
 ON a.ZONE_ID = b.ZONE_ID
 SET a.SOV_ACCESS_2000 = b.LN_ACC_EMP_SOV;
 
UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_log_acc_emp_sov_and_trnst b
 ON a.ZONE_ID = b.ZONE_ID
 SET a.TRNST_ACCESS_2000 = b.LN_ACC_EMP_TRNST;

# Change Scenario A 2000 - Baseline 2000 Logsum-weighted change in SOV accesibility

UPDATE TAZ_INDICATORS a 
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.CH_SOV_ACCESS_2000_BASE_2000 = a.SOV_ACCESS_2000 - b.SOV_ACCESS_2000;

# Change Scenario A 2000 - Baseline 2000 Logsum-weighted change in TRANSIT accesibility

UPDATE TAZ_INDICATORS a 
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.CH_TRNST_ACCESS_2000_BASE_2000 = a.TRNST_ACCESS_2000 - b.TRNST_ACCESS_2000;

##############
# Land Price #
##############

# 2000 Land Price

CREATE TEMPORARY TABLE tmp_lp_2000
 SELECT ZONE_ID, SUM(RESIDENTIAL_LAND_VALUE + NONRESIDENTIAL_LAND_VALUE) AS TOTAL_LP
 FROM gridcells_exported_denormalized
 WHERE YEAR = 2000
GROUP BY ZONE_ID;

ALTER TABLE tmp_lp_2000 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_lp_2000 b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.LP_2000 = b.TOTAL_LP;

# Change Scenario A 2000 - Baseline 2000 Land Price 

UPDATE TAZ_INDICATORS a
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b
 ON a.ZONE_ID = b.ZONE_ID
SET a.CH_LP_2000_BASE_2000 = a.LP_2000 - b.LP_2000;

###########################################################################################################



