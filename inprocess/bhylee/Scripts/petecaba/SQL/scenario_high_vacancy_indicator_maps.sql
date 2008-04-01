########################################################
## Main Indicator table for 2010 Scenario A No UGB run #
########################################################


# USE PSRC_2000_base_run_output;

CREATE TABLE TAZ_INDICATORS_2010
 (ZONE_ID INT, 
  HH_2010_BASE INT, 
  HH_2010 INT, 
  CH_HH_2010_BASE_2010 DOUBLE, 
  AVG_HH_SZ_2010_BASE DOUBLE, 
  AVG_HH_SZ_2010 DOUBLE,
  CH_AVG_SZ_2010_BASE_2010 DOUBLE,
  AVG_HH_INC_2010_BASE DOUBLE, 
  AVG_HH_INC_2010 DOUBLE,
  CH_AVG_HH_INC_2010_BASE_2010 DOUBLE,
  JOBS_2010_BASE INT,
  JOBS_2010 INT,
  CH_JOBS_2010_BASE_2010 DOUBLE,
  HH_UNITS_2010_BASE INT, 
  HH_UNITS_2010 INT,
  CH_HU_2010_BASE_2010 DOUBLE,
  RES_VAC_RATE_2010_BASE DOUBLE,
  RES_VAC_RATE_2010 DOUBLE,
  CH_RES_VAC_RATE_2010_BASE_2010 DOUBLE,
  NONRES_SQFT_2010_BASE INT,
  NONRES_SQFT_2010 INT,
  CH_NONRES_FLSP_2000_2010 DOUBLE,
  NONRES_VAC_RATE_2010_BASE DOUBLE,
  NONRES_VAC_RATE_2010 DOUBLE,
  CH_NONRES_VAC_RATE_2010_BASE_2010 DOUBLE,
  SOV_ACCESS_2010_BASE DOUBLE,
  SOV_ACCESS_2010 DOUBLE,
  CH_SOV_ACCESS_2010_BASE_2010 DOUBLE,
  TRNST_ACCESS_2010_BASE DOUBLE,
  TRNST_ACCESS_2010 DOUBLE,
  CH_TRNST_ACCESS_2010_BASE_2010 DOUBLE,
  LP_2010_BASE INT,
  LP_2010 INT,
  CH_LP_2010_BASE_2010 DOUBLE);

INSERT INTO TAZ_INDICATORS_2010 (ZONE_ID) SELECT DISTINCT ZONE_ID FROM GSPSRC_2000_baseyear_flattened.gridcells;
ALTER TABLE TAZ_INDICATORS_2010 ADD INDEX ZONE_ID_INDEX(ZONE_ID);

 #########################
 # Households Indicators #
 ######################### 

# 2010 HH characteristics

create temporary table tmp_hh_characteristics_2010 
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
 inner join GSPSRC_2000_baseyear_flattened.gridcells c
  on a.grid_id = c.grid_id
 where a.year = 2010
;
 
create temporary table tmp_household_character_2010
 select zone_id, count(*) as households, sum(persons) as persons, sum(income) as income
 from tmp_hh_characteristics_2010 group by zone_id;

alter table tmp_household_character_2010 add index zone_id(zone_id);

update TAZ_INDICATORS_2010 a
 inner join tmp_household_character_2010 b 
 on a.zone_id = b.zone_id 
 set a.hh_2010 = b.households;

update TAZ_INDICATORS_2010 a 
 inner join tmp_household_character_2010 b 
 on a.zone_id = b.zone_id 
 set a.avg_hh_sz_2010 = b.persons / a.hh_2010;
 
update TAZ_INDICATORS_2010 a 
 inner join tmp_household_character_2010 b 
 on a.zone_id = b.zone_id 
 set a.avg_hh_inc_2010 = b.income / a.hh_2010; 

# Change Scenario A 2010 - Baseline 2010 Households 

UPDATE TAZ_INDICATORS a 
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b 
 ON a.ZONE_ID = b.ZONE_ID
 SET a.CH_HH_2010_BASE_2010 = a.HH_2010 - b.HH_2010;

# Change Scenario A 2010 - Baseline 2010 Household Size

UPDATE TAZ_INDICATORS a
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b
 ON a.ZONE_ID = b.ZONE_ID
SET a.CH_AVG_HH_SZ_2010_BASE_2010 = a.AVG_HH_SZ_2010 - b.AVG_HH_SZ_2010;

# Change Scenario A 2010 - Baseline 2010 Household Income

UPDATE TAZ_INDICATORS_2010 a
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS_2010 b
 ON a.ZONE_ID = b.ZONE_ID
SET a.CH_AVG_HH_INC_2010_BASE_2010 = a.AVG_HH_INC_2010 - b.AVG_HH_INC_2010;


########################
# Employment Indicators#
########################

# CREATE 2010 Jobs

create temporary table tmp_jobs_2010
 select a.JOB_ID,
 	a.GRID_ID,
 	a.HOME_BASED,
 	c.ZONE_ID
 from jobs_exported a inner join jobs_constants b 
  on a.job_id = b.job_id
 inner join GSPSRC_2000_baseyear_start.gridcells c 
  on a.grid_id = c.grid_Id
 where a.year = 2010
; 

create temporary table tmp_job_character_2010 
 select zone_id, count(*) as jobs 
 from tmp_jobs_2010 group by zone_id;
 
alter table tmp_job_character_2010 add index zone_id(zone_id);

update TAZ_INDICATORS a inner join tmp_job_character_2010 b 
 on a.zone_id = b.zone_id 
 set a.jobs_2010 = b.jobs;

# Change Scenario A 2010 - Baseline 2010 Employment characteristics

UPDATE TAZ_INDICATORS a
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b 
 ON a.ZONE_ID = b.ZONE_ID 
 SET a.CH_JOBS_2010_BASE_2010 = a.JOBS_2010 - b.JOBS_2010;

#########
# Units #
#########

# 2010 Residential Units

CREATE TEMPORARY TABLE tmp_units_2010
 SELECT b.ZONE_ID, SUM(a.RESIDENTIAL_UNITS) AS UNITS 
 FROM gridcells_exported_denormalized a 
 INNER JOIN GSPSRC_2000_baseyear_change_20041206.gridcells b 
 ON a.GRID_ID = b.GRID_ID
 WHERE a.YEAR = 2010
GROUP BY b.ZONE_ID;

ALTER TABLE tmp_units_2010 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_units_2010 b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.HH_UNITS_2010 = b.UNITS;

# Change Scenario A 2010 - Baseline 2010 units

UPDATE TAZ_INDICATORS a 
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.CH_HU_2010_BASE_2010 = a.HH_UNITS_2010 - b.HH_UNITS_2010;

# Scenario A 2010 Residential Vacancty Rate

UPDATE TAZ_INDICATORS SET RES_VAC_RATE_2010 = ROUND(1-(hh_2010/hh_units_2010),4);

# Change Scenario A 2010 - Baseline Vacancy Rate

UPDATE TAZ_INDICATORS a
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b
 ON a.ZONE_ID = b.ZONE_ID 
SET a.CH_RES_VAC_RATE_2010_BASE_2010 = a.RES_VAC_RATE_2010 - b.RES_VAC_RATE_2010;


############################
# 2010 Nonresidential sqft #
############################

# 2010 Nonresidential Sqft 

CREATE TEMPORARY TABLE tmp_nonres_sqft_2010
 SELECT b.ZONE_ID, SUM(a.COMMERCIAL_SQFT + a.INDUSTRIAL_SQFT + a.GOVERNMENTAL_SQFT) AS SQFT
 FROM gridcells_exported a 
 INNER JOIN GSPSRC_2000_baseyear_change_20041206.gridcells b 
 ON a.GRID_ID = b.GRID_ID
 WHERE b.YEAR = 2010
GROUP BY a.ZONE_ID;

ALTER TABLE tmp_nonres_sqft_2010 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_nonres_sqft_2010 b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.NONRES_SQFT_2010 = b.SQFT;

# Change Scenario A 2010 - Baseline 2010 Change SQFT 

UPDATE TAZ_INDICATORS a
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.CH_NONRES_FLSP_2010_BASE_2010 = a.NONRES_SQFT_2010 - b.NONRES_SQFT_2010;

# 2010 Nonresidential Vacancty Rate

CREATE TEMPORARY TABLE tmp_jobs_nhb_2010
 SELECT GRID_ID, COUNT(*) AS JOBS
 FROM jobs_exported_denormalized
 WHERE HOME_BASED = 0 AND YEAR = 2010
GROUP BY GRID_ID;

ALTER TABLE tmp_jobs_nhb_2010 ADD UNIQUE INDEX GRID_ID(GRID_ID);

CREATE TEMPORARY TABLE tmp_sqft_2010 
 SELECT a.GRID_ID, 
 	SUM(a.COMMERCIAL_SQFT + INDUSTRIAL_SQFT + GOVERNMENTAL_SQFT) AS TOTAL_SQFT,
 	b.SQFT AS SQFT_PER_JOB
 FROM gridcells_exported_denormalized a 
 INNER JOIN sqft_for_non_home_based_jobs b 
 ON a.DEVELOPMENT_TYPE_ID = b.DEVELOPMENT_TYPE_ID
 WHERE a.YEAR = 2010
GROUP BY a.GRID_ID;
 
ALTER TABLE tmp_sqft_2010 ADD UNIQUE INDEX GRID_ID(GRID_ID);
 
CREATE TEMPORARY TABLE tmp_gridcells_exp_2010 
 SELECT * FROM gridcells_exported_denormalized 
 WHERE YEAR = 2010;
 
ALTER TABLE tmp_gridcells_exp_2010 ADD INDEX GRID_ID(GRID_ID);
 
CREATE TEMPORARY TABLE tmp_vac_rate_2010
 SELECT a.ZONE_ID, 
 	ROUND(1 - SUM(c.JOBS * b.SQFT_PER_JOB) / SUM(b.TOTAL_SQFT), 4) AS NONRES_VAC_RATE
 FROM tmp_gridcells_exp_2010 a 
 INNER JOIN tmp_sqft_2010 b
  ON a.GRID_ID = b.GRID_ID
 LEFT JOIN tmp_jobs_nhb_2010 c
  ON b.GRID_ID = c.GRID_ID
GROUP BY a.ZONE_ID;

ALTER TABLE tmp_vac_rate_2010 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_vac_rate_2010 b 
 ON a.ZONE_ID = b.zone_id
SET a.NONRES_VAC_RATE_2010 = b.NONRES_VAC_RATE;

DROP TABLE tmp_jobs_nhb_2010;
DROP TABLE tmp_sqft_2010;
DROP TABLE tmp_vac_rate_2010;

###################
# Accessibilities #
###################

# 2010 Logsum-weighted access to employment by SOV and logsum-weighted access to employment by transit

# Accessibilities table 'home_access_to_employment_1' as 1-car hosuehold
# Accessibilities table 'home_access_to_employment_0' as 0-car household transit 

CREATE TEMPORARY TABLE tmp_log_acc_emp_sov_and_trnst
 SELECT ZONE_ID, 
 	HOME_ACCESS_TO_EMPLOYMENT_1 AS LN_ACC_EMP_SOV,
 	HOME_ACCESS_TO_EMPLOYMENT_0 AS LN_ACC_EMP_TRNST
 FROM accessibilities 
 WHERE YEAR = 2010;

ALTER TABLE tmp_log_acc_emp_sov_and_trnst ADD INDEX ZONE_ID(ZONE_ID);
 
UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_log_acc_emp_sov_and_trnst b
 ON a.ZONE_ID = b.ZONE_ID
 SET a.SOV_ACCESS_2010 = b.LN_ACC_EMP_SOV;
 
UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_log_acc_emp_sov_and_trnst b
 ON a.ZONE_ID = b.ZONE_ID
 SET a.TRNST_ACCESS_2010 = b.LN_ACC_EMP_TRNST;

# Change Scenario A 2010 - Baseline 2010 Logsum-weighted change in SOV accesibility

UPDATE TAZ_INDICATORS a 
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.CH_SOV_ACCESS_2010_BASE_2010 = a.SOV_ACCESS_2010 - b.SOV_ACCESS_2010;

# Change Scenario A 2010 - Baseline 2010 Logsum-weighted change in TRANSIT accesibility

UPDATE TAZ_INDICATORS a 
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.CH_TRNST_ACCESS_2010_BASE_2010 = a.TRNST_ACCESS_2010 - b.TRNST_ACCESS_2010;

##############
# Land Price #
##############

# 2010 Land Price

CREATE TEMPORARY TABLE tmp_lp_2010
 SELECT ZONE_ID, SUM(RESIDENTIAL_LAND_VALUE + NONRESIDENTIAL_LAND_VALUE) AS TOTAL_LP
 FROM gridcells_exported_denormalized
 WHERE YEAR = 2010
GROUP BY ZONE_ID;

ALTER TABLE tmp_lp_2010 ADD INDEX ZONE_ID(ZONE_ID);

UPDATE TAZ_INDICATORS a 
 INNER JOIN tmp_lp_2010 b 
 ON a.ZONE_ID = b.ZONE_ID
SET a.LP_2010 = b.TOTAL_LP;

# Change Scenario A 2010 - Baseline 2010 Land Price 

UPDATE TAZ_INDICATORS a
 INNER JOIN PSRC_2000_base_run_2_output.TAZ_INDICATORS b
 ON a.ZONE_ID = b.ZONE_ID
SET a.CH_LP_2010_BASE_2010 = a.LP_2010 - b.LP_2010;

###########################################################################################################



