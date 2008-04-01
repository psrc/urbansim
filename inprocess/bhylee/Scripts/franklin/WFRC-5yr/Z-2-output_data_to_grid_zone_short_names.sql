# Select only the bookend years

USE WFRC_1997_output_2030_const;

CREATE TEMPORARY TABLE households_exported_endyears 
SELECT * FROM households_exported 
WHERE year=1997
  OR year=2030;

     CREATE INDEX households_exported_endyears_year_household_id 
     ON households_exported_endyears 
       (year, household_id);

CREATE TEMPORARY TABLE jobs_exported_endyears 
SELECT * FROM jobs_exported 
WHERE year=1997
  OR year=2030;

     CREATE INDEX jobs_exported_endyears_year_job_id 
     ON jobs_exported_endyears 
     (year, job_id);

CREATE TEMPORARY TABLE gridcells_exported_endyears 
SELECT * FROM gridcells_exported 
WHERE year=1997
  OR year=2030;

     CREATE INDEX gridcells_exported_endyears_year_grid_id 
     ON gridcells_exported_endyears 
       (year, grid_id);

CREATE TEMPORARY TABLE accessibilities_endyears 
SELECT * FROM accessibilities 
WHERE year=1997
  OR year=2030;

     CREATE INDEX accessibilities_endyears_year_zone_id 
     ON accessibilities_endyears 
       (year, zone_id);

# Match households_constants to households_exported

DROP TABLE IF EXISTS households_endyears;

CREATE TABLE households_endyears
SELECT hh_e.year AS year, 
  hh_e.household_id AS household_id, 
  hh_e.grid_id AS grid_id, 
  hh_e.zone_id AS zone_id,
  hh_c.persons AS persons,
  hh_c.workers AS workers,
  hh_c.age_of_head AS age_of_head,
  hh_c.income AS income,
  hh_c.children AS children,
  hh_c.race_id AS race_id
FROM households_exported_endyears AS hh_e 
  INNER JOIN households_constants AS hh_c
    ON hh_e.household_id=hh_c.household_id;

     CREATE INDEX households_endyears_year_household_id_zone_id
     ON households_endyears
       (year, household_id, zone_id);

     CREATE INDEX households_endyears_year_household_id_grid_id
     ON households_endyears
       (year, household_id, grid_id);

DROP TABLE households_exported_endyears;

# Aggregate household data to TAZ level

CREATE TEMPORARY TABLE zones_hhdata
SELECT year AS year,
  zone_id AS zone_id,
  count(household_id) AS households,
  SUM(persons) AS population,
  SUM(workers) AS workers,
  SUM(income) AS total_income,
  SUM(children) AS children,
  AVG(age_of_head) AS average_age_of_head
FROM households_endyears
GROUP BY year, 
  zone_id;

     CREATE INDEX zones_hhdata_year_zone_id
     ON zones_hhdata 
       (year, zone_id);

# Match jobs_constants to jobs_exported

DROP TABLE IF EXISTS jobs_endyears;

CREATE TABLE jobs_endyears
SELECT j_e.year AS year,
  j_e.job_id AS job_id,
  j_e.grid_id AS grid_id,
  j_e.home_based AS home_based,
  j_e.zone_id AS zone_id,
  j_c.sector_id AS sector_id
FROM jobs_exported_endyears AS j_e
  INNER JOIN jobs_constants AS j_c
    ON j_e.job_id=j_c.job_id;

     CREATE INDEX jobs_endyears_year_job_id_zone_id
     ON jobs_endyears
       (year, job_id, zone_id);

     CREATE INDEX jobs_endyears_year_job_id_grid_id
     ON jobs_endyears
       (year, job_id, grid_id);

     DROP TABLE jobs_exported_endyears;

# Aggregate job data to TAZ level

CREATE TEMPORARY TABLE zones_jobdata
SELECT year AS year,
  zone_id AS zone_id,
  COUNT(job_id) AS jobs,
  AVG(home_based) AS pct_home_based
FROM jobs_endyears
GROUP BY year, zone_id;

     CREATE INDEX zones_jobdata_year_zone_id
     ON zones_jobdata 
       (year, zone_id);

# Create "wedges", which are subsections of gridcells that belong to different TAZs,
# and allocate real estate data based on gridcell_fractions_in_zones.

CREATE TEMPORARY TABLE wedges_endyears
SELECT b.year AS year, 
  a.zone_id AS zone_id, 
  a.grid_id AS grid_id,
  a.fraction*b.residential_units AS residential_units, 
  a.fraction*b.residential_improvement_value AS residential_improvement_value,
  a.fraction*b.commercial_sqft AS commercial_sqft, 
  a.fraction*b.commercial_improvement_value AS commercial_improvement_value, 
  a.fraction*b.industrial_sqft AS industrial_sqft, 
  a.fraction*b.industrial_improvement_value AS industrial_improvement_value, 
  a.fraction*b.governmental_sqft AS governmental_sqft,
  a.fraction*b.governmental_improvement_value AS governmental_improvement_value,
  a.fraction*b.residential_land_value AS residential_land_value,
  a.fraction*b.nonresidential_land_value AS nonresidential_land_value 
FROM WFRC_1997_baseyear.gridcell_fractions_in_zones AS a,
  gridcells_exported_endyears AS b
WHERE a.grid_id=b.grid_id;

     CREATE INDEX wedges_endyears_year_zone_id
     ON wedges_endyears 
       (year, zone_id);

# Aggregate "wedge" data up to the TAZ

CREATE TEMPORARY TABLE zones_gcdata
SELECT year AS year, 
  zone_id AS zone_id,
  sum(residential_units) AS residential_units,
  sum(residential_improvement_value) AS residential_improvement_value,
  sum(commercial_sqft) AS commercial_sqft,
  sum(commercial_improvement_value) AS commercial_improvement_value,
  sum(industrial_sqft) AS industrial_sqft,
  sum(industrial_improvement_value) AS industrial_improvement_value,
  sum(governmental_sqft) AS governmental_sqft,
  sum(governmental_improvement_value) AS governmental_improvement_value,
  sum(residential_land_value) AS residential_land_value,
  sum(nonresidential_land_value) AS nonresidential_land_value
FROM wedges_endyears
GROUP BY year, zone_id;

     CREATE INDEX zones_gcdata_year_zone_id
     ON zones_gcdata 
       (year, zone_id);

     DROP TABLE wedges_endyears;

# Combine all TAZ-level data

DROP TABLE IF EXISTS zones_endyears_short;

CREATE TABLE zones_endyears_short
SELECT z_gc.year AS year,
  z_gc.zone_id AS zone_id,
  z_gc.residential_units AS dur,
  z_gc.residential_improvement_value AS iv_r,
  z_gc.commercial_sqft AS sf_c,
  z_gc.commercial_improvement_value AS iv_c,
  z_gc.industrial_sqft AS sf_i,
  z_gc.industrial_improvement_value AS iv_i,
  z_gc.governmental_sqft AS sf_g,
  z_gc.governmental_improvement_value AS iv_g,
  z_gc.residential_land_value AS lv_r,
  z_gc.nonresidential_land_value AS lv_nr,
  if(z_hh.households IS NULL,0,z_hh.households) AS hhs,
  if(z_hh.population IS NULL,0,z_hh.population) AS pop,
  if(z_hh.workers IS NULL,0,z_hh.workers) AS wrkrs,
  if(z_hh.total_income IS NULL,0,z_hh.total_income) AS totinc,
  if(z_hh.children IS NULL,0,z_hh.children) AS child,
  z_hh.average_age_of_head AS ageh_avg,
  if(z_j.jobs IS NULL,0,z_j.jobs) AS jobs,
  z_j.pct_home_based AS hb_pct,
  acc.home_access_to_employment_0 AS hae0,
  acc.home_access_to_employment_1 AS hae1,
  acc.home_access_to_employment_2 AS hae2,
  acc.home_access_to_employment_3 AS hae3,
  acc.home_access_to_population_0 AS hap0,
  acc.home_access_to_population_1 AS hap1,
  acc.home_access_to_population_2 AS hap2,
  acc.home_access_to_population_3 AS hap3,
  acc.work_access_to_employment_0 AS wae0,
  acc.work_access_to_employment_1 AS wae1,
  acc.work_access_to_employment_2 AS wae2,
  acc.work_access_to_employment_3 AS wae3,
  acc.work_access_to_population_0 AS wap0,
  acc.work_access_to_population_1 AS wap1,
  acc.work_access_to_population_2 AS wap2,
  acc.work_access_to_population_3 AS wap3
FROM zones_gcdata AS z_gc
  LEFT JOIN zones_hhdata AS z_hh
    ON z_gc.year=z_hh.year AND
      z_gc.zone_id=z_hh.zone_id
  LEFT JOIN zones_jobdata AS z_j
    ON z_gc.year=z_j.year AND
      z_gc.zone_id=z_j.zone_id
  LEFT JOIN accessibilities_endyears AS acc
    ON z_gc.year=acc.year AND
      z_gc.zone_id=acc.zone_id;

     CREATE INDEX zones_endyears_short_year_zone_id
     ON zones_endyears_short 
       (year, zone_id);

     DROP TABLE zones_hhdata;
     DROP TABLE zones_jobdata;
     DROP TABLE zones_gcdata;
     DROP TABLE accessibilities_endyears;

# Aggregate household data to gridcells

CREATE TEMPORARY TABLE gridcells_hhdata
SELECT year AS year,
  grid_id AS grid_id,
  count(household_id) AS households,
  SUM(persons) AS population,
  SUM(workers) AS workers,
  SUM(income) AS total_income,
  SUM(children) AS children,
  AVG(age_of_head) AS average_age_of_head
FROM households_endyears
GROUP BY year, grid_id;

     CREATE INDEX gridcells_hhdata_year_grid_id
     ON gridcells_hhdata 
       (year, grid_id);

# Aggregate job data to gridcells

CREATE TEMPORARY TABLE gridcells_jobdata
SELECT year AS year,
  grid_id AS grid_id,
  COUNT(job_id) AS jobs,
  AVG(home_based) AS pct_home_based
FROM jobs_endyears
GROUP BY year, grid_id;

     CREATE INDEX gridcells_jobdata_year_grid_id
     ON gridcells_jobdata 
       (year, grid_id);

# Combine all gridcell-level data

DROP TABLE IF EXISTS gridcells_endyears_short;

CREATE TABLE gridcells_endyears_short
SELECT gc_gc.year AS year,
  gc_gc.grid_id AS grid_id,
  gc_gc.development_type_id AS dt_id,
  gc_gc.residential_units AS dur,
  gc_gc.residential_improvement_value AS iv_r,
  gc_gc.commercial_sqft AS sf_c,
  gc_gc.commercial_improvement_value AS iv_c,
  gc_gc.industrial_sqft AS sf_i,
  gc_gc.industrial_improvement_value AS iv_i,
  gc_gc.governmental_sqft AS sf_g,
  gc_gc.governmental_improvement_value AS iv_g,
  gc_gc.residential_land_value AS lv_r,
  gc_gc.nonresidential_land_value AS lv_nr,
  if(gc_hh.households IS NULL,0,gc_hh.households) AS hhs,
  if(gc_hh.population IS NULL,0,gc_hh.population) AS pop,
  if(gc_hh.workers IS NULL,0,gc_hh.workers) AS wrkrs,
  if(gc_hh.total_income IS NULL,0,gc_hh.total_income) AS totinc,
  if(gc_hh.children IS NULL,0,gc_hh.children) AS child,
  gc_hh.average_age_of_head AS ageh_avg,
  if(gc_j.jobs IS NULL,0,gc_j.jobs) AS jobs,
  gc_j.pct_home_based AS hb_pct
FROM gridcells_exported_endyears AS gc_gc
  LEFT JOIN gridcells_hhdata AS gc_hh
    ON gc_gc.year=gc_hh.year AND
      gc_gc.grid_id=gc_hh.grid_id
  LEFT JOIN gridcells_jobdata AS gc_j
    ON gc_gc.year=gc_j.year AND
      gc_gc.grid_id=gc_j.grid_id;

CREATE INDEX gridcells_endyears_short_year_grid_id
  ON gridcells_endyears_short
    (year, grid_id);

     DROP TABLE gridcells_hhdata;
     DROP TABLE gridcells_jobdata;
     DROP TABLE gridcells_exported_endyears;

# Create transposed zone and gridcell tables - use short names for DBF compatibility

DROP TABLE IF EXISTS zones_2030;

CREATE TABLE zones_2030 
     (zone_id int, county int, distlrg int, distmed int, distsml int);

ALTER TABLE zones_2030
  ADD COLUMN dur_a int, ADD COLUMN iv_r_a double, 
  ADD COLUMN sf_c_a double, ADD COLUMN iv_c_a double, ADD COLUMN sf_i_a double, ADD COLUMN iv_i_a double, ADD COLUMN sf_g_a double, 
  ADD COLUMN iv_g_a double, ADD COLUMN lv_r_a double, ADD COLUMN lv_nr_a double, ADD COLUMN sf_tot_a double, ADD COLUMN lv_tot_a double, 
  ADD COLUMN hhs_a double, ADD COLUMN pop_a double, ADD COLUMN wrkrs_a double, ADD COLUMN totinc_a double, ADD COLUMN child_a double, 
  ADD COLUMN ageh_a_a double, ADD COLUMN jobs_a double, ADD COLUMN hb_pct_a double, 
  ADD COLUMN hae0_a double, ADD COLUMN hae1_a double, ADD COLUMN hae2_a double, ADD COLUMN hae3_a double, 
  ADD COLUMN hap0_a double, ADD COLUMN hap1_a double, ADD COLUMN hap2_a double, ADD COLUMN hap3_a double, 
  ADD COLUMN wae0_a double, ADD COLUMN wae1_a double, ADD COLUMN wae2_a double, ADD COLUMN wae3_a double, 
  ADD COLUMN wap0_a double, ADD COLUMN wap1_a double, ADD COLUMN wap2_a double, ADD COLUMN wap3_a double,
  
  ADD COLUMN dur_z int, ADD COLUMN iv_r_z double,
  ADD COLUMN sf_c_z double, ADD COLUMN iv_c_z double, ADD COLUMN sf_i_z double, ADD COLUMN iv_i_z double, ADD COLUMN sf_g_z double, 
  ADD COLUMN iv_g_z double, ADD COLUMN lv_r_z double, ADD COLUMN lv_nr_z double, ADD COLUMN sf_tot_z double, ADD COLUMN lv_tot_z double, 
  ADD COLUMN hhs_z double, ADD COLUMN pop_z double, ADD COLUMN wrkrs_z double, ADD COLUMN totinc_z double, ADD COLUMN child_z double, 
  ADD COLUMN ageh_a_z double, ADD COLUMN jobs_z double, ADD COLUMN hb_pct_z double, 
  ADD COLUMN hae0_z double, ADD COLUMN hae1_z double, ADD COLUMN hae2_z double, ADD COLUMN hae3_z double, 
  ADD COLUMN hap0_z double, ADD COLUMN hap1_z double, ADD COLUMN hap2_z double, ADD COLUMN hap3_z double, 
  ADD COLUMN wae0_z double, ADD COLUMN wae1_z double, ADD COLUMN wae2_z double, ADD COLUMN wae3_z double, 
  ADD COLUMN wap0_z double, ADD COLUMN wap1_z double, ADD COLUMN wap2_z double, ADD COLUMN wap3_z double,

  ADD COLUMN dur_D int, ADD COLUMN iv_r_D double, 
  ADD COLUMN sf_c_D double, ADD COLUMN iv_c_D double, ADD COLUMN sf_i_D double, ADD COLUMN iv_i_D double, ADD COLUMN sf_g_D double, 
  ADD COLUMN iv_g_D double, ADD COLUMN lv_r_D double, ADD COLUMN lv_nr_D double, ADD COLUMN sf_tot_D double, ADD COLUMN lv_tot_D double, 
  ADD COLUMN hhs_D double, ADD COLUMN pop_D double, ADD COLUMN wrkrs_D double, ADD COLUMN totinc_D double, ADD COLUMN child_D double, 
  ADD COLUMN ageh_a_D double, ADD COLUMN jobs_D double, ADD COLUMN hb_pct_D double,
  ADD COLUMN hae0_d double, ADD COLUMN hae1_d double, ADD COLUMN hae2_d double, ADD COLUMN hae3_d double, 
  ADD COLUMN hap0_d double, ADD COLUMN hap1_d double, ADD COLUMN hap2_d double, ADD COLUMN hap3_d double, 
  ADD COLUMN wae0_d double, ADD COLUMN wae1_d double, ADD COLUMN wae2_d double, ADD COLUMN wae3_d double, 
  ADD COLUMN wap0_d double, ADD COLUMN wap1_d double, ADD COLUMN wap2_d double, ADD COLUMN wap3_d double; 
  
CREATE INDEX zones_2030_zone_id
     ON zones_2030 (zone_id);

INSERT INTO zones_2030
SELECT zones.zone_id AS zone_id,
  zones.county AS county,
  zones.distlrg AS distlrg,
  zones.distmed AS distmed,
  zones.distsml AS distsml,
  yr_a.dur AS dur_a,
  yr_a.iv_r AS iv_r_a,
  yr_a.sf_c AS sf_c_a,
  yr_a.iv_c AS iv_c_a,
  yr_a.sf_i AS sf_i_a,
  yr_a.iv_i AS iv_i_a,
  yr_a.sf_g AS sf_g_a,
  yr_a.iv_g AS iv_g_a,
  yr_a.lv_r AS lv_r_a,
  yr_a.lv_nr AS lv_nr_a,
  yr_a.sf_c + yr_a.sf_i + yr_a.sf_g AS sf_tot_a,
  yr_a.lv_r + yr_a.lv_nr AS lv_tot_a,
  yr_a.hhs AS hhs_a,
  yr_a.pop AS pop_a,
  yr_a.wrkrs AS wrkrs_a,
  yr_a.totinc AS totinc_a,
  yr_a.child AS child_a,
  yr_a.ageh_avg AS ageh_a_a,
  yr_a.jobs AS jobs_a,
  yr_a.hb_pct AS hb_pct_a,
  yr_a.hae0 AS hae0_a,
  yr_a.hae1 AS hae1_a,
  yr_a.hae2 AS hae2_a,
  yr_a.hae3 AS hae3_a,
  yr_a.hap0 AS hap0_a,
  yr_a.hap1 AS hap1_a,
  yr_a.hap2 AS hap2_a,
  yr_a.hap3 AS hap3_a,
  yr_a.wae0 AS wae0_a,
  yr_a.wae1 AS wae1_a,
  yr_a.wae2 AS wae2_a,
  yr_a.wae3 AS wae3_a,
  yr_a.wap0 AS wap0_a,
  yr_a.wap1 AS wap1_a,
  yr_a.wap2 AS wap2_a,
  yr_a.wap3 AS wap3_a,
  yr_z.dur AS dur_z,
  yr_z.iv_r AS iv_r_z,
  yr_z.sf_c AS sf_c_z,
  yr_z.iv_c AS iv_c_z,
  yr_z.sf_i AS sf_i_z,
  yr_z.iv_i AS iv_i_z,
  yr_z.sf_g AS sf_g_z,
  yr_z.iv_g AS iv_g_z,
  yr_z.lv_r AS lv_r_z,
  yr_z.lv_nr AS lv_nr_z,
  yr_z.sf_c + yr_z.sf_i + yr_z.sf_g AS sf_tot_z,
  yr_z.lv_r + yr_z.lv_nr AS lv_tot_z,
  yr_z.hhs AS hhs_z,
  yr_z.pop AS pop_z,
  yr_z.wrkrs AS wrkrs_z,
  yr_z.totinc AS totinc_z,
  yr_z.child AS child_z,
  yr_z.ageh_avg AS ageh_a_z,
  yr_z.jobs AS jobs_z,
  yr_z.hb_pct AS hb_pct_z,
  yr_z.hae0 AS hae0_z,
  yr_z.hae1 AS hae1_z,
  yr_z.hae2 AS hae2_z,
  yr_z.hae3 AS hae3_z,
  yr_z.hap0 AS hap0_z,
  yr_z.hap1 AS hap1_z,
  yr_z.hap2 AS hap2_z,
  yr_z.hap3 AS hap3_z,
  yr_z.wae0 AS wae0_z,
  yr_z.wae1 AS wae1_z,
  yr_z.wae2 AS wae2_z,
  yr_z.wae3 AS wae3_z,
  yr_z.wap0 AS wap0_z,
  yr_z.wap1 AS wap1_z,
  yr_z.wap2 AS wap2_z,
  yr_z.wap3 AS wap3_z,
  yr_z.dur - yr_a.dur AS dur_d,
  yr_z.iv_r - yr_a.iv_r AS iv_r_d,
  yr_z.sf_c - yr_a.sf_c AS sf_c_d,
  yr_z.iv_c - yr_a.iv_c AS iv_c_d,
  yr_z.sf_i - yr_a.sf_i AS sf_i_d,
  yr_z.iv_i - yr_a.iv_i AS iv_i_d,
  yr_z.sf_g - yr_a.sf_g AS sf_g_d,
  yr_z.iv_g - yr_a.iv_g AS iv_g_d,
  yr_z.lv_r - yr_a.lv_r AS lv_r_d,
  yr_z.lv_nr- yr_a.lv_nr AS lv_nr_d,
  (yr_z.sf_c - yr_a.sf_c) + (yr_z.sf_i - yr_a.sf_i) + (yr_z.sf_g - yr_a.sf_g) AS sf_tot_d,
  (yr_z.lv_r - yr_a.lv_r) + (yr_z.lv_nr - yr_a.lv_nr) AS lv_tot_d,
  yr_z.hhs - yr_a.hhs AS hhs_d,
  yr_z.pop - yr_a.pop AS pop_d,
  yr_z.wrkrs - yr_a.wrkrs AS wrkrs_d,
  yr_z.totinc - yr_a.totinc AS totinc_d,
  yr_z.child - yr_a.child AS child_d,
  yr_z.ageh_avg - yr_a.ageh_avg AS ageh_a_d,
  yr_z.jobs - yr_a.jobs AS jobs_d,
  yr_z.hb_pct - yr_a.hb_pct AS hb_pct_d,
  yr_z.hae0 - yr_a.hae0 AS hae0_d,
  yr_z.hae1 - yr_a.hae1 AS hae1_d,
  yr_z.hae2 - yr_a.hae2 AS hae2_d,
  yr_z.hae3 - yr_a.hae3 AS hae3_d,
  yr_z.hap0 - yr_a.hap0 AS hap0_d,
  yr_z.hap1 - yr_a.hap1 AS hap1_d,
  yr_z.hap2 - yr_a.hap2 AS hap2_d,
  yr_z.hap3 - yr_a.hap3 AS hap3_d,
  yr_z.wae0 - yr_a.wae0 AS wae0_d,
  yr_z.wae1 - yr_a.wae1 AS wae1_d,
  yr_z.wae2 - yr_a.wae2 AS wae2_d,
  yr_z.wae3 - yr_a.wae3 AS wae3_d,
  yr_z.wap0 - yr_a.wap0 AS wap0_d,
  yr_z.wap1 - yr_a.wap1 AS wap1_d,
  yr_z.wap2 - yr_a.wap2 AS wap2_d,
  yr_z.wap3 - yr_a.wap3 AS wap3_d
FROM zones_endyears_short AS yr_a,
  zones_endyears_short AS yr_z,
  WFRC_1997_baseyear.zones AS zones
WHERE yr_a.year=1997 AND
  yr_z.year=2030 AND
  yr_a.zone_id=zones.zone_id AND
  yr_z.zone_id=zones.zone_id;

DROP TABLE IF EXISTS gridcells_2030;

CREATE TABLE gridcells_2030 (grid_id int, dt_id_a int, dur_a int, iv_r_a double, 
  sf_c_a double, iv_c_a double, sf_i_a double, iv_i_a double, sf_g_a double, iv_g_a double,
  lv_r_a double, lv_nr_a double, sf_tot_a double, lv_tot_a double, hhs_a double, pop_a double, wrkrs_a double, totinc_a double,
  child_a double, ageh_a_a double, jobs_a double, hb_pct_a double, 
  dt_id_z int, dur_z int, iv_r_z double, 
  sf_c_z double, iv_c_z double, sf_i_z double, iv_i_z double, sf_g_z double, iv_g_z double,
  lv_r_z double, lv_nr_z double, sf_tot_z double, lv_tot_z double, hhs_z double, pop_z double, wrkrs_z double, totinc_z double,
  child_z double, ageh_a_z double, jobs_z double, hb_pct_z double, 
  dt_id_D int, dur_D int, iv_r_D double, 
  sf_c_D double, iv_c_D double, sf_i_D double, iv_i_D double, sf_g_D double, iv_g_D double,
  lv_r_D double, lv_nr_D double, sf_tot_D double, lv_tot_D double, hhs_D double, pop_D double, wrkrs_D double, totinc_D double,
  child_D double, ageh_a_D double, jobs_D double, hb_pct_D double); 
  
CREATE INDEX gridcells_2030_grid_id
     on gridcells_2030 (grid_id);

INSERT INTO gridcells_2030
SELECT yr_a.grid_id AS grid_id,
  yr_a.dt_id AS dt_id_a,
  yr_a.dur AS dur_a,
  yr_a.iv_r AS iv_r_a,
  yr_a.sf_c AS sf_c_a,
  yr_a.iv_c AS iv_c_a,
  yr_a.sf_i AS sf_i_a,
  yr_a.iv_i AS iv_i_a,
  yr_a.sf_g AS sf_g_a,
  yr_a.iv_g AS iv_g_a,
  yr_a.lv_r AS lv_r_a,
  yr_a.lv_nr AS lv_nr_a,
  yr_a.sf_c + yr_a.sf_i + yr_a.sf_g AS sf_tot_a,
  yr_a.lv_r + yr_a.lv_nr AS lv_tot_a,
  yr_a.hhs AS hhs_a,
  yr_a.pop AS pop_a,
  yr_a.wrkrs AS wrkrs_a,
  yr_a.totinc AS totinc_a,
  yr_a.child AS child_a,
  yr_a.ageh_avg AS ageh_a_a,
  yr_a.jobs AS jobs_a,
  yr_a.hb_pct AS hb_pct_a,
  yr_z.dt_id AS dt_id_z,
  yr_z.dur AS dur_z,
  yr_z.iv_r AS iv_r_z,
  yr_z.sf_c AS sf_c_z,
  yr_z.iv_c AS iv_c_z,
  yr_z.sf_i AS sf_i_z,
  yr_z.iv_i AS iv_i_z,
  yr_z.sf_g AS sf_g_z,
  yr_z.iv_g AS iv_g_z,
  yr_z.lv_r AS lv_r_z,
  yr_z.lv_nr AS lv_nr_z,
  yr_z.sf_c + yr_z.sf_i + yr_z.sf_g AS sf_tot_z,
  yr_z.lv_r + yr_z.lv_nr AS lv_tot_z,
  yr_z.hhs AS hhs_z,
  yr_z.pop AS pop_z,
  yr_z.wrkrs AS wrkrs_z,
  yr_z.totinc AS totinc_z,
  yr_z.child AS child_z,
  yr_z.ageh_avg AS ageh_a_z,
  yr_z.jobs AS jobs_z,
  yr_z.hb_pct AS hb_pct_z,
  if(yr_a.dt_id=yr_z.dt_id,NULL,yr_z.dt_id) AS dt_id_d,
  yr_z.dur - yr_a.dur AS dur_d,
  yr_z.iv_r - yr_a.iv_r AS iv_r_d,
  yr_z.sf_c - yr_a.sf_c AS sf_c_d,
  yr_z.iv_c - yr_a.iv_c AS iv_c_d,
  yr_z.sf_i - yr_a.sf_i AS sf_i_d,
  yr_z.iv_i - yr_a.iv_i AS iv_i_d,
  yr_z.sf_g - yr_a.sf_g AS sf_g_d,
  yr_z.iv_g - yr_a.iv_g AS iv_g_d,
  yr_z.lv_r - yr_a.lv_r AS lv_r_d,
  yr_z.lv_nr- yr_a.lv_nr AS lv_nr_d,
  (yr_z.sf_c - yr_a.sf_c) + (yr_z.sf_i - yr_a.sf_i) + (yr_z.sf_g - yr_a.sf_g) AS sf_tot_d,
  (yr_z.lv_r - yr_a.lv_r) + (yr_z.lv_nr - yr_a.lv_nr) AS lv_tot_d,
  yr_z.hhs - yr_a.hhs AS hhs_d,
  yr_z.pop - yr_a.pop AS pop_d,
  yr_z.wrkrs - yr_a.wrkrs AS wrkrs_d,
  yr_z.totinc - yr_a.totinc AS totinc_d,
  yr_z.child - yr_a.child AS child_d,
  yr_z.ageh_avg - yr_a.ageh_avg AS ageh_a_d,
  yr_z.jobs - yr_a.jobs AS jobs_d,
  yr_z.hb_pct - yr_a.hb_pct AS hb_pct_d
FROM gridcells_endyears_short AS yr_a,
  gridcells_endyears_short AS yr_z
WHERE yr_a.year=1997 AND
  yr_z.year=2030 AND
  yr_a.grid_id=yr_z.grid_id;

# Clean up unnecessary tables

DROP TABLE IF EXISTS gridcells_endyears_short;
DROP TABLE IF EXISTS households_endyears;
DROP TABLE IF EXISTS jobs_endyears;
DROP TABLE IF EXISTS zones_endyears_short;
