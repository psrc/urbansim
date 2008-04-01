# This script creates two tables that are intended for use in displaying
# UrbanSim outputs using ArcGIS or other GIS software.  These tables are:
#
#    1. gridcells_2030, and
#    2. zones_2030.
#
# The first table contains data summarized at the grid cell level, the
# second at the transportation analysis zone (aka "zone" or "TAZ) leve.
# Both employ abbreviated column names as described in:
#
#    "trondheim.cs.washington.edu\projects\urbansim4\modeler-work-specs\Short Names.xls".
#
# Each table includes three sets of columns, each suffixed with an abbreviation as follows:\
#
#    1. Data for year 1997, suffixed with "_a";
#    2. Data for year 2030, suffixed with "_z"; and
#    3. Computed absolute differences between the 1997 data and the 2030 data, with
#         the exception of development type, which is computed as null where the two years
#         contain the same development type in a particular gridcell or, if they are
#         different, then the development type of the gridcell in 2030.
#
# This version is intended for processing through a perl script:
#
#    Scripts\lmwang\travel_model_urbansim_interaction\tu_zutomate.pl
#
# In the perl script, the following parameters are dynamically replaced with appropriate values:
#
#    $output_db - the name of the database containing the UrbanSim output tables;
#    1997 - the four-digit year of the base year, or the start of the simulation;
#    2030 - the four-digit year of the end year of the simulation or some other projected year;
#    WFRC_1997_baseyear - the name of the database containing the UrbanSim baseyear tables.
#
# Replace "# tp" marks (without the space) with "/ *tp* /" marks (without the spaces) to run test point data summaries.
# (Spaces are included above so that when you do the find/replace you don't change this comment)

# Select only the bookend years

# use $output_db;

#tp  select year, count(*) as households from households_exported where year=1997 or year=2030 group by year;
#tp  select year, count(*) as jobs from jobs_exported where year=1997 or year=2030 group by year;
#tp  select year, sum(residential_units) as residential_units from gridcells_exported where year=1997 or year=2030 group by year;
#tp  select year, sum(commercial_sqft+industrial_sqft+governmental_sqft) as nonresidential_sqft 
#tp       from gridcells_exported where year=1997 or year=2030 group by year;
#tp  select year, min(HOME_ACCESS_TO_EMPLOYMENT_1), max(HOME_ACCESS_TO_EMPLOYMENT_1) 
#tp       from accessibilities where year=1997 or year=2030 group by year;

DROP TABLE IF EXISTS households_exported_endyears;
CREATE TEMPORARY TABLE households_exported_endyears 
SELECT * FROM households_exported 
WHERE year=1997
  OR year=2030;

     CREATE INDEX households_exported_endyears_year_household_id 
     ON households_exported_endyears 
       (year, household_id);

#tp  select year, count(*) as households from households_exported_endyears where year=1997 or year=2030 group by year;

DROP TABLE IF EXISTS jobs_exported_endyears;
CREATE TEMPORARY TABLE jobs_exported_endyears 
SELECT * FROM jobs_exported 
WHERE year=1997
  OR year=2030;

     CREATE INDEX jobs_exported_endyears_year_job_id 
     ON jobs_exported_endyears 
     (year, job_id);
     
#tp  select year, count(*) as jobs from jobs_exported_endyears where year=1997 or year=2030 group by year;

#Produce excess capacity data that needs to be aggregated to zone level
#Note that this assumes the gridcell_capacity table has been created - by running the excess_capapcity.sql script (only needs to be run once on the baseyear).
drop table if exists gridcell_excess_capacity;
create table gridcell_excess_capacity (
     grid_id int, 
     excess_sqft_A int(11),
     excess_units_A int(11),
     excess_sqft_Z int(11),
     excess_units_Z int(11));
insert into gridcell_excess_capacity
     select 
          gc.grid_id,
          gc.max_sqft - (ge.commercial_sqft+ge.governmental_sqft+ge.industrial_sqft) as excess_sqft_A,
          gc.max_units - ge.residential_units as excess_sqft_A,
          -1,-1
     from WFRC_1997_baseyear.gridcell_capacity as gc, gridcells_exported as ge
     where gc.grid_id = ge.grid_id 
          AND ge.year=1997
     group by gc.grid_id;
create index gridcell_excess_capacity_grid_id 
     on gridcell_excess_capacity (grid_id);
update gridcell_excess_capacity as gec, WFRC_1997_baseyear.gridcell_capacity as gc, gridcells_exported as ge
     set gec.excess_sqft_Z = gc.max_sqft - (ge.commercial_sqft+ge.governmental_sqft+ge.industrial_sqft), 
         gec.excess_units_Z = gc.max_units - ge.residential_units
     where gec.grid_id=gc.grid_id AND gc.grid_id = ge.grid_id 
          AND ge.year=2030;



DROP TABLE IF EXISTS gridcells_exported_endyears;
CREATE TEMPORARY TABLE gridcells_exported_endyears 
     (year smallint(6), grid_id int(11), residential_improvement_value int(11), residential_land_value int(11),
     commercial_sqft int(11), industrial_sqft int(11), governmental_sqft int(11), year_built int(11),
     residential_units int(11), development_type_id int(11), commercial_improvement_value int(11),
     industrial_improvement_value int(11), governmental_improvement_value int(11), nonresidential_land_value int(11),
     fraction_residential_land double, water_use double, city_id int(11), county_id int(11),
     home_based_job_spaces double, non_home_based_job_spaces double, total_job_spaces double, 
     excess_sqft int(11), excess_units int(11)); 

INSERT INTO gridcells_exported_endyears
     SELECT a.*,
          NULL as city_id,
          NULL as county_id,
          round(a.residential_units*b.ratio) AS home_based_job_spaces,
          round((a.COMMERCIAL_SQFT+a.INDUSTRIAL_SQFT+a.GOVERNMENTAL_SQFT)/c.SQFT) as non_home_based_job_spaces,
          NULL AS total_job_spaces,
            NULL AS excess_sqft,
            NULL AS excess_units
     FROM gridcells_exported AS a,
          WFRC_1997_baseyear.residential_units_for_home_based_jobs AS b,
          WFRC_1997_baseyear.sqft_for_non_home_based_jobs AS c
     WHERE (a.year=1997 OR a.year=2030)
          AND a.DEVELOPMENT_TYPE_ID=b.DEVELOPMENT_TYPE_ID
          AND a.DEVELOPMENT_TYPE_ID=c.DEVELOPMENT_TYPE_ID;

     CREATE INDEX gridcells_exported_endyears_year_grid_id 
     ON gridcells_exported_endyears 
       (year, grid_id);
     CREATE INDEX gridcells_exported_endyears_grid_id_year
     ON gridcells_exported_endyears 
       (grid_id, year);

update gridcells_exported_endyears
     set total_job_spaces=home_based_job_spaces+non_home_based_job_spaces;

update gridcells_exported_endyears as a, WFRC_1997_baseyear.gridcells AS b
     set a.city_id=b.city_id,
          a.county_id=b.county_id
     where a.grid_id=b.grid_id;
     

#Add the excess capacity data as calculated in the gridcell_excess_capacity table
update gridcells_exported_endyears as a, gridcell_excess_capacity AS gec
     set a.excess_sqft=gec.excess_sqft_A,
           a.excess_units=gec.excess_units_A
     where a.grid_id=gec.grid_id AND a.year=1997;
update gridcells_exported_endyears as a, gridcell_excess_capacity AS gec
     set a.excess_sqft=gec.excess_sqft_Z,
           a.excess_units=gec.excess_units_Z
     where a.grid_id=gec.grid_id AND a.year=2030;


#tp  select year, sum(residential_units) as residential_units from gridcells_exported_endyears where year=1997 or year=2030 group by year;
#tp  select year, sum(commercial_sqft+industrial_sqft+governmental_sqft) as nonresidential_sqft 
#tp       from gridcells_exported_endyears where year=1997 or year=2030 group by year;
#tp  select year, sum(home_based_job_spaces), sum(non_home_based_job_spaces), sum(total_job_spaces)
#tp       from gridcells_exported_endyears group by year;

DROP TABLE IF EXISTS accessibilities_endyears;
CREATE TEMPORARY TABLE accessibilities_endyears 
     SELECT * FROM accessibilities 
     WHERE year=1997
          OR year=2030;

     CREATE INDEX accessibilities_endyears_year_zone_id 
     ON accessibilities_endyears 
       (year, zone_id);

#tp  select year, min(HOME_ACCESS_TO_EMPLOYMENT_1), max(HOME_ACCESS_TO_EMPLOYMENT_1) 
#tp       from accessibilities_endyears where year=1997 or year=2030 group by year;

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

#tp  select year, count(*) as households from households_endyears where year=1997 or year=2030 group by year;

# Aggregate household data to TAZ level

DROP TABLE IF EXISTS zones_hhdata;
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

#tp select year, sum(households) from zones_hhdata where year=1997 or year=2030 group by year;

# Match jobs_constants to jobs_exported

DROP TABLE IF EXISTS jobs_endyears;
CREATE TABLE jobs_endyears
SELECT j_e.year AS year,
  j_e.job_id AS job_id,
  j_e.grid_id AS grid_id,
  j_e.home_based AS home_based,
  j_e.zone_id AS zone_id,
  j_c.sector_id AS sector_id,
  if(j_c.sector_id>=3,1,0) AS sector_3plus
FROM jobs_exported_endyears AS j_e
  INNER JOIN jobs_constants AS j_c
    ON j_e.job_id=j_c.job_id;

     CREATE INDEX jobs_endyears_year_job_id_zone_id
     ON jobs_endyears
       (year, job_id, zone_id);

     CREATE INDEX jobs_endyears_year_job_id_grid_id
     ON jobs_endyears
       (year, job_id, grid_id);

#tp  select year, count(*) as jobs from jobs_endyears where year=1997 or year=2030 group by year;

# Aggregate job data to TAZ level

DROP TABLE IF EXISTS zones_jobdata;
CREATE TEMPORARY TABLE zones_jobdata
SELECT year AS year,
  zone_id AS zone_id,
  COUNT(job_id) AS jobs,
  AVG(home_based) AS pct_home_based,
  SUM(sector_3plus) AS jobs_3plus
FROM jobs_endyears
GROUP BY year, zone_id;

     CREATE INDEX zones_jobdata_year_zone_id
     ON zones_jobdata 
       (year, zone_id);

#tp  select year, sum(jobs) as jobs from zones_jobdata where year=1997 or year=2030 group by year;

# Create a local version of gridcells_fractions_in_zones that will also include
# gridcells that are wholly contained within one TAZ.

DROP TABLE IF EXISTS tmp_gridcells_fractions_in_zones;
CREATE TEMPORARY TABLE tmp_gridcell_fractions_in_zones
     SELECT * 
     FROM WFRC_1997_baseyear.gridcell_fractions_in_zones;

     CREATE INDEX tmp_gridcells_fractions_in_zones_grid_id_zone_id
     ON tmp_gridcell_fractions_in_zones (grid_id, zone_id);

DROP TABLE IF EXISTS tmp_gridcells_from_fractions_table;
CREATE TEMPORARY TABLE tmp_gridcells_from_fractions_table
     SELECT grid_id, max(zone_id) as zone_id
          FROM tmp_gridcell_fractions_in_zones
          GROUP BY grid_id;

     CREATE INDEX tmp_gridcells_from_fractions_table_grid_id
     ON tmp_gridcells_from_fractions_table (grid_id);

CREATE TEMPORARY TABLE tmp_gridcell_fractions_whole
     SELECT a.grid_id, 
          a.zone_id, 
          b.zone_id as zone_id_from_fractions
     FROM WFRC_1997_baseyear.gridcells as a
          LEFT JOIN tmp_gridcells_from_fractions_table as b
          ON a.grid_id=b.grid_id;

     CREATE INDEX tmp_gridcell_fractions_whole_grid_id
     ON tmp_gridcell_fractions_whole (grid_id);
     
DELETE FROM tmp_gridcell_fractions_whole
     WHERE zone_id_from_fractions is not null;

INSERT INTO tmp_gridcell_fractions_in_zones
     SELECT grid_id AS grid_id, 
          zone_id AS zone_id, 
          1 AS fraction
     FROM tmp_gridcell_fractions_whole;

# Create "wedges", which are subsections of gridcells that belong to different TAZs,
# and allocate real estate data based on gridcell_fractions_in_zones.

DROP TABLE IF EXISTS wedges_endyears;
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
  a.fraction*b.nonresidential_land_value AS nonresidential_land_value,
  a.fraction*b.home_based_job_spaces AS home_based_job_spaces,
  a.fraction*b.non_home_based_job_spaces AS non_home_based_job_spaces,
  a.fraction*b.total_job_spaces AS total_job_spaces,
  a.fraction*b.excess_sqft AS excess_sqft,
  a.fraction*b.excess_units AS excess_units
FROM gridcells_exported_endyears AS b
     left join tmp_gridcell_fractions_in_zones AS a
ON a.grid_id=b.grid_id;

     CREATE INDEX wedges_endyears_year_zone_id
     ON wedges_endyears 
       (year, zone_id);

#tp  select year, sum(residential_units) as residential_units from wedges_endyears where year=1997 or year=2030 group by year;
#tp  select year, sum(commercial_sqft+industrial_sqft+governmental_sqft) as nonresidential_sqft 
#tp       from wedges_endyears where year=1997 or year=2030 group by year;
#tp  select year, sum(home_based_job_spaces), sum(non_home_based_job_spaces), sum(total_job_spaces)
#tp       from wedges_endyears group by year;

# Aggregate "wedge" data up to the TAZ

DROP TABLE IF EXISTS zones_gcdata;
CREATE TEMPORARY TABLE zones_gcdata
     (year smallint(6), zone_id int(11), residential_units double, residential_improvement_value double, 
     commercial_sqft double, commercial_improvement_value double, industrial_sqft double, industrial_improvement_value double,
     governmental_sqft double, governmental_improvement_value double, residential_land_value double, nonresidential_land_value double,
     home_based_job_spaces double, non_home_based_job_spaces double, total_job_spaces double, excess_sqft int(11),
     excess_units int(11));

INSERT INTO zones_gcdata
SELECT year AS year, 
  zone_id AS zone_id,
  round(sum(residential_units)) AS residential_units,
  sum(residential_improvement_value) AS residential_improvement_value,
  sum(commercial_sqft) AS commercial_sqft,
  sum(commercial_improvement_value) AS commercial_improvement_value,
  sum(industrial_sqft) AS industrial_sqft,
  sum(industrial_improvement_value) AS industrial_improvement_value,
  sum(governmental_sqft) AS governmental_sqft,
  sum(governmental_improvement_value) AS governmental_improvement_value,
  sum(residential_land_value) AS residential_land_value,
  sum(nonresidential_land_value) AS nonresidential_land_value,
  round(sum(home_based_job_spaces)) AS home_based_job_spaces,
  round(sum(non_home_based_job_spaces)) AS non_home_based_job_spaces,
  round(sum(total_job_spaces)) AS total_job_spaces,
  round(sum(excess_sqft)) AS excess_sqft,
  round(sum(excess_units)) AS excess_units
FROM wedges_endyears
GROUP BY year, zone_id;

     CREATE INDEX zones_gcdata_year_zone_id
     ON zones_gcdata 
       (year, zone_id);

#tp  select year, sum(residential_units) as residential_units from zones_gcdata where year=1997 or year=2030 group by year;
#tp  select year, sum(commercial_sqft+industrial_sqft+governmental_sqft) as nonresidential_sqft 
#tp       from zones_gcdata where year=1997 or year=2030 group by year;
#tp  select year, sum(home_based_job_spaces), sum(non_home_based_job_spaces), sum(total_job_spaces)
#tp       from zones_gcdata group by year;

# Combine all TAZ-level data

DROP TABLE IF EXISTS zones_endyears_short;
CREATE TABLE zones_endyears_short
SELECT z_gc.year AS year,
  z_gc.zone_id AS zone_id,
  z_gc.residential_units AS dur,
  z_gc.residential_improvement_value AS iv_r,
  z_gc.commercial_sqft/1000 AS sf_c,
  z_gc.commercial_improvement_value AS iv_c,
  z_gc.industrial_sqft/1000 AS sf_i,
  z_gc.industrial_improvement_value AS iv_i,
  z_gc.governmental_sqft/1000 AS sf_g,
  z_gc.governmental_improvement_value AS iv_g,
  z_gc.residential_land_value AS lv_r,
  z_gc.nonresidential_land_value AS lv_nr,
  z_gc.home_based_job_spaces AS js_hb,
  z_gc.non_home_based_job_spaces AS js_nhb,
  z_gc.total_job_spaces AS js_tot,
  z_gc.excess_sqft/1000 AS sf_exc,
  z_gc.excess_units AS dur_exc,
  if(z_hh.households IS NULL,0,z_hh.households) AS hhs,
  if(z_hh.population IS NULL,0,z_hh.population) AS pop,
  if(z_hh.workers IS NULL,0,z_hh.workers) AS wrkrs,
  if(z_hh.total_income IS NULL,0,z_hh.total_income) AS totinc,
  if(z_hh.children IS NULL,0,z_hh.children) AS child,
  z_hh.average_age_of_head AS ageh_avg,
  if(z_j.jobs IS NULL,0,z_j.jobs) AS jobs,
  z_j.pct_home_based AS hb_pct,
  z_j.jobs_3plus AS j_3p,
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

#tp  select year, sum(dur) as residential_units from zones_endyears_short where year=1997 or year=2030 group by year;
#tp  select year, sum(sf_c+sf_i+sf_g) as nonresidential_sqft 
#tp       from zones_endyears_short where year=1997 or year=2030 group by year;
#tp  select year, sum(hhs) from zones_endyears_short where year=1997 or year=2030 group by year;
#tp  select year, sum(jobs) from zones_endyears_short where year=1997 or year=2030 group by year;
#tp  select year, min(hae1), max(hae1) 
#tp       from zones_endyears_short where year=1997 or year=2030 group by year;
#tp  select year, sum(js_hb), sum(js_nhb), sum(js_tot)
#tp       from zones_endyears_short group by year;

# Aggregate household data to gridcells

DROP TABLE IF EXISTS gridcells_hhdata;
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

#tp select year, sum(households) from gridcells_hhdata where year=1997 or year=2030 group by year;

# Aggregate job data to gridcells

DROP TABLE IF EXISTS gridcells_jobdata;
CREATE TEMPORARY TABLE gridcells_jobdata
SELECT year AS year,
  grid_id AS grid_id,
  COUNT(job_id) AS jobs,
  AVG(home_based) AS pct_home_based,
  SUM(sector_3plus) AS jobs_3plus
FROM jobs_endyears
GROUP BY year, grid_id;

     CREATE INDEX gridcells_jobdata_year_grid_id
     ON gridcells_jobdata 
       (year, grid_id);

#tp select year, sum(jobs) from gridcells_jobdata where year=1997 or year=2030 group by year;

# Combine all gridcell-level data

DROP TABLE IF EXISTS gridcells_endyears_short;
CREATE TABLE gridcells_endyears_short
SELECT gc_gc.year AS year,
  gc_gc.grid_id AS grid_id,
  gc_gc.city_id AS city_id,
  gc_gc.county_id AS county_id,
  gc_gc.development_type_id AS dt_id,
  gc_gc.residential_units AS dur,
  gc_gc.residential_improvement_value AS iv_r,
  gc_gc.commercial_sqft/1000 AS sf_c,
  gc_gc.commercial_improvement_value AS iv_c,
  gc_gc.industrial_sqft/1000 AS sf_i,
  gc_gc.industrial_improvement_value AS iv_i,
  gc_gc.governmental_sqft/1000 AS sf_g,
  gc_gc.governmental_improvement_value AS iv_g,
  gc_gc.residential_land_value AS lv_r,
  gc_gc.nonresidential_land_value AS lv_nr,
  gc_gc.home_based_job_spaces AS js_hb,
  gc_gc.non_home_based_job_spaces AS js_nhb,
  gc_gc.total_job_spaces AS js_tot,
  if(gc_hh.households=NULL,0,gc_hh.households) AS hhs,
  if(gc_hh.population=NULL,0,gc_hh.population) AS pop,
  if(gc_hh.workers=NULL,0,gc_hh.workers) AS wrkrs,
  if(gc_hh.total_income=NULL,0,gc_hh.total_income) AS totinc,
  if(gc_hh.children=NULL,0,gc_hh.children) AS child,
  gc_hh.average_age_of_head AS ageh_avg,
  if(gc_j.jobs=NULL,0,gc_j.jobs) AS jobs,
  gc_j.pct_home_based AS hb_pct,
  gc_j.jobs_3plus AS j_3p
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

/* PROGRESS MARK */

#tp  select year, sum(dur) as residential_units from gridcells_endyears_short where year=1997 or year=2030 group by year;
#tp  select year, sum(sf_c+sf_i+sf_g) as nonresidential_sqft 
#tp       from gridcells_endyears_short where year=1997 or year=2030 group by year;
#tp  select year, sum(hhs) from gridcells_endyears_short where year=1997 or year=2030 group by year;
#tp  select year, sum(jobs) from gridcells_endyears_short where year=1997 or year=2030 group by year;
#tp  select year, sum(js_hb), sum(js_nhb), sum(js_tot) from gridcells_endyears_short group by year;

# Create transposed zone and gridcell tables - use short names for DBF compatibility

DROP TABLE IF EXISTS zones_2030;
CREATE TABLE zones_2030 
     (zone_id int, county int, distlrg int, distmed int, distsml int);

ALTER TABLE zones_2030
  ADD COLUMN dur_a int, ADD COLUMN iv_r_a double, 
  ADD COLUMN sf_c_a double, ADD COLUMN iv_c_a double, ADD COLUMN sf_i_a double, ADD COLUMN iv_i_a double, ADD COLUMN sf_g_a double, 
  ADD COLUMN iv_g_a double, ADD COLUMN lv_r_a double, ADD COLUMN lv_nr_a double, ADD COLUMN sf_tot_a double, ADD COLUMN lv_tot_a double, 
  ADD COLUMN js_hb_a double, ADD COLUMN js_nhb_a double, ADD COLUMN js_tot_a double,
  ADD COLUMN sf_exc_a int, ADD COLUMN dur_exc_a int,
  ADD COLUMN hhs_a double, ADD COLUMN pop_a double, ADD COLUMN wrkrs_a double, ADD COLUMN totinc_a double, ADD COLUMN child_a double, 
  ADD COLUMN ageh_a double, ADD COLUMN jobs_a double, ADD COLUMN hb_pct_a double, ADD COLUMN j_3p_a double, 
  ADD COLUMN vr_r_a double, ADD COLUMN vr_nr_a double,
  ADD COLUMN hhsz_a double, ADD COLUMN hhin_a double,
  ADD COLUMN hae0_a double, ADD COLUMN hae1_a double, ADD COLUMN hae2_a double, ADD COLUMN hae3_a double, 
  ADD COLUMN hap0_a double, ADD COLUMN hap1_a double, ADD COLUMN hap2_a double, ADD COLUMN hap3_a double, 
  ADD COLUMN wae0_a double, ADD COLUMN wae1_a double, ADD COLUMN wae2_a double, ADD COLUMN wae3_a double, 
  ADD COLUMN wap0_a double, ADD COLUMN wap1_a double, ADD COLUMN wap2_a double, ADD COLUMN wap3_a double,
  
  ADD COLUMN dur_z int, ADD COLUMN iv_r_z double,
  ADD COLUMN sf_c_z double, ADD COLUMN iv_c_z double, ADD COLUMN sf_i_z double, ADD COLUMN iv_i_z double, ADD COLUMN sf_g_z double, 
  ADD COLUMN iv_g_z double, ADD COLUMN lv_r_z double, ADD COLUMN lv_nr_z double, ADD COLUMN sf_tot_z double, ADD COLUMN lv_tot_z double, 
  ADD COLUMN js_hb_z double, ADD COLUMN js_nhb_z double, ADD COLUMN js_tot_z double,
  ADD COLUMN sf_exc_z int, ADD COLUMN dur_exc_z int,
  ADD COLUMN hhs_z double, ADD COLUMN pop_z double, ADD COLUMN wrkrs_z double, ADD COLUMN totinc_z double, ADD COLUMN child_z double, 
  ADD COLUMN ageh_z double, ADD COLUMN jobs_z double, ADD COLUMN hb_pct_z double, ADD COLUMN j_3p_z double,
  ADD COLUMN vr_r_z double, ADD COLUMN vr_nr_z double,
  ADD COLUMN hhsz_z double, ADD COLUMN hhin_z double,
  ADD COLUMN hae0_z double, ADD COLUMN hae1_z double, ADD COLUMN hae2_z double, ADD COLUMN hae3_z double, 
  ADD COLUMN hap0_z double, ADD COLUMN hap1_z double, ADD COLUMN hap2_z double, ADD COLUMN hap3_z double, 
  ADD COLUMN wae0_z double, ADD COLUMN wae1_z double, ADD COLUMN wae2_z double, ADD COLUMN wae3_z double, 
  ADD COLUMN wap0_z double, ADD COLUMN wap1_z double, ADD COLUMN wap2_z double, ADD COLUMN wap3_z double;

CREATE INDEX zones_2030_zone_id
     ON zones_2030 (zone_id);

INSERT INTO zones_2030
SELECT zones.zone_id AS zone_id,
  zones.county AS county,
  zones.distlrg AS distlrg,
  zones.distmed AS distmed,
  zones.distsml AS distsml,
  if(yr_a.dur IS NULL,0,yr_a.dur) AS dur_a,
  if(yr_a.iv_r IS NULL,0,yr_a.iv_r) AS iv_r_a,
  if(yr_a.sf_c IS NULL,0,yr_a.sf_c) AS sf_c_a,
  if(yr_a.iv_c IS NULL,0,yr_a.iv_c) AS iv_c_a,
  if(yr_a.sf_i IS NULL,0,yr_a.sf_i) AS sf_i_a,
  if(yr_a.iv_i IS NULL,0,yr_a.iv_i) AS iv_i_a,
  if(yr_a.sf_g IS NULL,0,yr_a.sf_g) AS sf_g_a,
  if(yr_a.iv_g IS NULL,0,yr_a.iv_g) AS iv_g_a,
  if(yr_a.lv_r IS NULL,0,yr_a.lv_r) AS lv_r_a,
  if(yr_a.lv_nr IS NULL,0,yr_a.lv_nr) AS lv_nr_a,
  NULL AS sf_tot_a,
  NULL AS lv_tot_a,
  if(yr_a.js_hb IS NULL,0,yr_a.js_hb) AS js_hb_a,
  if(yr_a.js_nhb IS NULL,0,yr_a.js_nhb) AS js_nhb_a,
  NULL AS js_tot_a,
  yr_a.sf_exc as sf_exc_a,
  yr_a.dur_exc as dur_exc_a,
  if(yr_a.hhs IS NULL,0,yr_a.hhs) AS hhs_a,
  if(yr_a.pop IS NULL,0,yr_a.pop) AS pop_a,
  if(yr_a.wrkrs IS NULL,0,yr_a.wrkrs) AS wrkrs_a,
  if(yr_a.totinc IS NULL,0,yr_a.totinc) AS totinc_a,
  if(yr_a.child IS NULL,0,yr_a.child) AS child_a,
  yr_a.ageh_avg AS ageh_a,
  if(yr_a.jobs IS NULL,0,yr_a.jobs) AS jobs_a,
  yr_a.hb_pct AS hb_pct_a,
  yr_a.j_3p AS j_3p_a,
  NULL AS vr_r_a,
  NULL AS vr_nr_a,
  NULL AS hhsz_a,
  NULL AS hhin_a,
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
  if(yr_z.dur IS NULL,0,yr_z.dur) AS dur_z,
  if(yr_z.iv_r IS NULL,0,yr_z.iv_r) AS iv_r_z,
  if(yr_z.sf_c IS NULL,0,yr_z.sf_c) AS sf_c_z,
  if(yr_z.iv_c IS NULL,0,yr_z.iv_c) AS iv_c_z,
  if(yr_z.sf_i IS NULL,0,yr_z.sf_i) AS sf_i_z,
  if(yr_z.iv_i IS NULL,0,yr_z.iv_i) AS iv_i_z,
  if(yr_z.sf_g IS NULL,0,yr_z.sf_g) AS sf_g_z,
  if(yr_z.iv_g IS NULL,0,yr_z.iv_g) AS iv_g_z,
  if(yr_z.lv_r IS NULL,0,yr_z.lv_r) AS lv_r_z,
  if(yr_z.lv_nr IS NULL,0,yr_z.lv_nr) AS lv_nr_z,
  NULL AS sf_tot_z,
  NULL AS lv_tot_z,
  if(yr_z.js_hb IS NULL,0,yr_z.js_hb) AS js_hb_z,
  if(yr_z.js_nhb IS NULL,0,yr_z.js_nhb) AS js_nhb_z,
  NULL AS js_tot_z,
  yr_z.sf_exc as sf_exc_z,
  yr_z.dur_exc as dur_exc_z,
  if(yr_z.hhs IS NULL,0,yr_z.hhs) AS hhs_z,
  if(yr_z.pop IS NULL,0,yr_z.pop) AS pop_z,
  if(yr_z.wrkrs IS NULL,0,yr_z.wrkrs) AS wrkrs_z,
  if(yr_z.totinc IS NULL,0,yr_z.totinc) AS totinc_z,
  if(yr_z.child IS NULL,0,yr_z.child) AS child_z,
  yr_z.ageh_avg AS ageh_z,
  if(yr_z.jobs IS NULL,0,yr_z.jobs) AS jobs_z,
  yr_z.hb_pct AS hb_pct_z,
  yr_z.j_3p AS j_3p_z,
  NULL AS vr_r_z,
  NULL AS vr_nr_z,
  NULL AS hhsz_z,
  NULL AS hhin_z,
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
  yr_z.wap3 AS wap3_z
FROM zones_endyears_short AS yr_a,
  zones_endyears_short AS yr_z,
  WFRC_1997_baseyear.zones AS zones
WHERE yr_a.year=1997 AND
  yr_z.year=2030 AND
  yr_a.zone_id=zones.zone_id AND
  yr_z.zone_id=zones.zone_id;

#tp  select sum(dur_a), sum(dur_z) from zones_2030;
#tp  select sum(sf_c_a+sf_i_a+sf_g_a), sum(sf_c_z+sf_i_z+sf_g_z), sum(sf_tot_a), sum(sf_tot_z)
#tp       from zones_2030;
#tp  select sum(hhs_a), sum(hhs_z) from zones_2030;
#tp  select sum(jobs_a), sum(jobs_z) from zones_2030;
#tp  select min(hae1_a), max(hae1_a), min(hae1_z), max(hae1_z) 
#tp       from zones_2030;
#tp  select sum(js_hb_a), sum(js_nhb_a), sum(js_tot_a) from zones_2030;
#tp  select sum(js_hb_z), sum(js_nhb_z), sum(js_tot_z) from zones_2030;

ALTER TABLE zones_2030
  ADD COLUMN dur_d int, ADD COLUMN iv_r_d double, 
  ADD COLUMN sf_c_d double, ADD COLUMN iv_c_d double, ADD COLUMN sf_i_d double, ADD COLUMN iv_i_d double, ADD COLUMN sf_g_d double, 
  ADD COLUMN iv_g_d double, ADD COLUMN lv_r_d double, ADD COLUMN lv_nr_d double, ADD COLUMN sf_tot_d double, ADD COLUMN lv_tot_d double, 
  ADD COLUMN js_hb_d double, ADD COLUMN js_nhb_d double, ADD COLUMN js_tot_d double,
  ADD COLUMN sf_exc_d int, ADD COLUMN dur_exc_d int,
  ADD COLUMN hhs_d double, ADD COLUMN pop_d double, ADD COLUMN wrkrs_d double, ADD COLUMN totinc_d double, ADD COLUMN child_d double, 
  ADD COLUMN ageh_d double, ADD COLUMN jobs_d double, ADD COLUMN hb_pct_d double, ADD COLUMN j_3p_d double,
  ADD COLUMN vr_r_d double, ADD COLUMN vr_nr_d double,
  ADD COLUMN hhsz_d double, ADD COLUMN hhin_d double,
  ADD COLUMN hae0_d double, ADD COLUMN hae1_d double, ADD COLUMN hae2_d double, ADD COLUMN hae3_d double, 
  ADD COLUMN hap0_d double, ADD COLUMN hap1_d double, ADD COLUMN hap2_d double, ADD COLUMN hap3_d double, 
  ADD COLUMN wae0_d double, ADD COLUMN wae1_d double, ADD COLUMN wae2_d double, ADD COLUMN wae3_d double, 
  ADD COLUMN wap0_d double, ADD COLUMN wap1_d double, ADD COLUMN wap2_d double, ADD COLUMN wap3_d double;

update zones_2030
     set  sf_tot_a = sf_c_a + sf_i_a + sf_g_a,
          lv_tot_a = lv_r_a + lv_nr_a,
          js_tot_a = js_hb_a + js_nhb_a,
          sf_tot_z = sf_c_z + sf_i_z + sf_g_z,
          lv_tot_z = lv_r_z + lv_nr_z,
          js_tot_z = js_hb_z + js_nhb_z,
          dur_d = dur_z - dur_a,
          iv_r_d = iv_r_z - iv_r_a,
          sf_c_d = sf_c_z - sf_c_a,
          iv_c_d = iv_c_z - iv_c_a,
          sf_i_d = sf_i_z - sf_i_a,
          iv_i_d = iv_i_z - iv_i_a,
          sf_g_d = sf_g_z - sf_g_a,
          iv_g_d = iv_g_z - iv_g_a,
          lv_r_d = lv_r_z - lv_r_a,
          lv_nr_d = lv_nr_z - lv_nr_a,
          js_hb_d = js_hb_z - js_hb_a,
          js_nhb_d = js_nhb_z - js_nhb_a,
          js_tot_d = js_hb_z + js_nhb_z - js_hb_a - js_nhb_a,
          sf_exc_d = sf_exc_z - sf_exc_a,
          dur_exc_d = dur_exc_z - dur_exc_a,
          sf_tot_d = sf_c_z + sf_i_z + sf_g_z - sf_c_a - sf_i_a - sf_g_a,
          lv_tot_d = lv_r_z + lv_nr_z - lv_r_a - lv_nr_a,
          hhs_d = hhs_z - hhs_a,
          pop_d = pop_z - pop_a,
          wrkrs_d = wrkrs_z - wrkrs_a,
          totinc_d = totinc_z - totinc_a,
          child_d = child_z - child_a,
          ageh_d = ageh_z - ageh_a,
          jobs_d = jobs_z - jobs_a,
          hb_pct_d = hb_pct_z - hb_pct_a,
          j_3p_d = j_3p_z - j_3p_a,
          vr_r_a = 1-(hhs_a/dur_a),
          vr_nr_a = 1-(jobs_a/(js_hb_a + js_nhb_a)),
          vr_r_z = 1-(hhs_z/dur_z),
          vr_nr_z = 1-(jobs_z/(js_hb_z + js_nhb_z)),
          vr_r_d = (hhs_a/dur_a) - (hhs_z/dur_z),
          vr_nr_d = (jobs_a/(js_hb_a + js_nhb_a)) - (jobs_z/(js_hb_z + js_nhb_z)),
          hhsz_a = pop_a/hhs_a,
          hhsz_z = pop_z/hhs_z,
          hhsz_d = (pop_z/hhs_z) - (pop_a/hhs_a),
          hhin_a = totinc_a/hhs_a,
          hhin_z = totinc_z/hhs_a,
          hhin_d = (totinc_z/hhs_z) - (totinc_a/hhs_a),
          hae0_d = hae0_z - hae0_a,
          hae1_d = hae1_z - hae1_a,
          hae2_d = hae2_z - hae2_a,
          hae3_d = hae3_z - hae3_a,
          hap0_d = hap0_z - hap0_a,
          hap1_d = hap1_z - hap1_a,
          hap2_d = hap2_z - hap2_a,
          hap3_d = hap3_z - hap3_a,
          wae0_d = wae0_z - wae0_a,
          wae1_d = wae1_z - wae1_a,
          wae2_d = wae2_z - wae2_a,
          wae3_d = wae3_z - wae3_a,
          wap0_d = wap0_z - wap0_a,
          wap1_d = wap1_z - wap1_a,
          wap2_d = wap2_z - wap2_a,
          wap3_d = wap3_z - wap3_a;

ALTER TABLE zones_2030
  ADD COLUMN dur_dl int, ADD COLUMN sf_tot_dl double, ADD COLUMN hhs_dl double, ADD COLUMN pop_dl double, 
  ADD COLUMN jobs_dl double, ADD COLUMN hae1_dl double, ADD COLUMN lv_tot_dl double,
  
  ADD COLUMN dur_Change_percent double,
  ADD COLUMN pop_Change_percent double, ADD COLUMN hhs_Change_percent double, 
  ADD COLUMN jobs_Change_percent double, ADD COLUMN sf_tot_Change_percent double,
  ADD COLUMN hae1_Change_percent double, ADD COLUMN lv_tot_Change_percent double,
  ADD COLUMN dur_Absolute_percent double,
  ADD COLUMN pop_Absolute_percent double, ADD COLUMN hhs_Absolute_percent double, 
  ADD COLUMN jobs_Absolute_percent double, ADD COLUMN sf_tot_Absolute_percent double,
  ADD COLUMN hae1_Absolute_percent double, ADD COLUMN lv_tot_Absolute_percent double;

UPDATE zones_2030 AS a
     INNER JOIN WFRC_1997_output_2030_LRP.zones_2030 AS LRP
          ON a.zone_id=LRP.zone_id
     SET  a.dur_dl    = a.dur_z    - LRP.dur_z,
          a.sf_tot_dl = a.sf_tot_z - LRP.sf_tot_z,
          a.hhs_dl    = a.hhs_z    - LRP.hhs_z,
          a.pop_dl    = a.pop_z    - LRP.pop_z,
          a.jobs_dl   = a.jobs_z   - LRP.jobs_z,
          a.hae1_dl   = a.hae1_z   - LRP.hae1_z,
          a.lv_tot_dl = a.lv_tot_z - LRP.lv_tot_z,
          a.pop_Change_percent = (a.pop_d - LRP.pop_d) / ABS(LRP.pop_d),
          a.hhs_Change_percent = (a.hhs_d - LRP.hhs_d) / ABS(LRP.hhs_d),
          a.jobs_Change_percent = (a.jobs_d - LRP.jobs_d) / ABS(LRP.jobs_d),
          a.dur_Change_percent = (a.dur_d - LRP.dur_d) / ABS(LRP.dur_d),
          a.sf_tot_Change_percent = (a.sf_tot_d - LRP.sf_tot_d) / ABS(LRP.sf_tot_d),
          a.hae1_Change_percent = (a.hae1_d - LRP.hae1_d) / ABS(LRP.hae1_d),
          a.lv_tot_Change_percent = (a.lv_tot_d - LRP.lv_tot_d) / ABS(LRP.lv_tot_d),
          a.pop_Absolute_percent = (a.pop_z - LRP.pop_z) / ABS(LRP.pop_z),
          a.hhs_Absolute_percent = (a.hhs_z - LRP.hhs_z) / ABS(LRP.hhs_z),
          a.jobs_Absolute_percent = (a.jobs_z - LRP.jobs_z) / ABS(LRP.jobs_z),
          a.dur_Absolute_percent = (a.dur_z - LRP.dur_z) / ABS(LRP.dur_z),
          a.sf_tot_Absolute_percent = (a.sf_tot_z - LRP.sf_tot_z) / ABS(LRP.sf_tot_z),
          a.hae1_Absolute_percent = (a.hae1_z - LRP.hae1_z) / ABS(LRP.hae1_z),
          a.lv_tot_Absolute_percent = (a.lv_tot_z - LRP.lv_tot_z) / ABS(LRP.lv_tot_z);

#tp  select year, sum(residential_units) as residential_units from gridcells_exported where year=1997 or year=2030 group by year;
#tp  select sum(dur_a), sum(dur_z), sum(dur_d) from zones_2030;
#tp  select year, sum(commercial_sqft+industrial_sqft+governmental_sqft) as nonresidential_sqft 
#tp       from gridcells_exported where year=1997 or year=2030 group by year;
#tp  select sum(sf_c_a+sf_i_a+sf_g_a), sum(sf_c_z+sf_i_z+sf_g_z), sum(sf_c_d+sf_i_d+sf_g_d), sum(sf_tot_a), sum(sf_tot_z), sum(sf_tot_d)
#tp       from zones_2030;
#tp  select year, count(*) as households from households_exported where year=1997 or year=2030 group by year;
#tp  select sum(hhs_a), sum(hhs_z), sum(hhs_d) from zones_2030;
#tp  select year, count(*) as jobs from jobs_exported where year=1997 or year=2030 group by year;
#tp  select sum(jobs_a), sum(jobs_z), sum(jobs_d) from zones_2030;
#tp  select year, min(HOME_ACCESS_TO_EMPLOYMENT_1), max(HOME_ACCESS_TO_EMPLOYMENT_1) 
#tp       from accessibilities where year=1997 or year=2030 group by year;
#tp  select min(hae1_a), max(hae1_a), min(hae1_z), max(hae1_z), min(hae1_d), max(hae1_d) 
#tp       from zones_2030;
#tp  select sum(js_hb_a), sum(js_nhb_a), sum(js_tot_a) from zones_2030;
#tp  select sum(js_hb_z), sum(js_nhb_z), sum(js_tot_z) from zones_2030;
#tp  select sum(js_hb_d), sum(js_nhb_d), sum(js_tot_d) from zones_2030;

DROP TABLE IF EXISTS gridcells_2030;
CREATE TABLE gridcells_2030 (grid_id int, ci_id int, co_id int, 
  
  dt_id_a int, dur_a int, iv_r_a double, 
  sf_c_a double, iv_c_a double, sf_i_a double, iv_i_a double, sf_g_a double, iv_g_a double,
  lv_r_a double, lv_nr_a double, sf_tot_a double, lv_tot_a double,
  js_hb_a double, js_nhb_a double, js_tot_a double,
  hhs_a double, pop_a double, wrkrs_a double, totinc_a double,
  child_a double, ageh_a double, jobs_a double, hb_pct_a double, j_3p_a double,
  vr_r_a double, vr_nr_a double, hhsz_a double, hhin_a double,
  
  dt_id_z int, dur_z int, iv_r_z double, 
  sf_c_z double, iv_c_z double, sf_i_z double, iv_i_z double, sf_g_z double, iv_g_z double,
  lv_r_z double, lv_nr_z double, sf_tot_z double, lv_tot_z double,
  js_hb_z double, js_nhb_z double, js_tot_z double,
  hhs_z double, pop_z double, wrkrs_z double, totinc_z double,
  child_z double, ageh_z double, jobs_z double, hb_pct_z double, j_3p_z double,
  vr_r_z double, vr_nr_z double, hhsz_z double, hhin_z double,
  
  dt_id_d int, dur_d int, iv_r_d double, 
  sf_c_d double, iv_c_d double, sf_i_d double, iv_i_d double, sf_g_d double, iv_g_d double,
  lv_r_d double, lv_nr_d double, sf_tot_d double, lv_tot_d double,
  js_hb_d double, js_nhb_d double, js_tot_d double,
  hhs_d double, pop_d double, wrkrs_d double, totinc_d double,
  child_d double, ageh_d double, jobs_d double, hb_pct_d double, j_3p_d double,
  vr_r_d double, vr_nr_d double, hhsz_d double, hhin_d double,
  
  dur_dl int, sf_tot_dl int, hhs_dl double, pop_dl double, jobs_dl double, lv_tot_dl double
  ); 
  
alter table gridcells_2030
  ADD COLUMN dur_Change_percent double, ADD COLUMN pop_Change_percent double, 
  ADD COLUMN hhs_Change_percent double, ADD COLUMN jobs_Change_percent double, 
  ADD COLUMN sf_tot_Change_percent double, ADD COLUMN lv_tot_Change_percent double,
  ADD COLUMN dur_Absolute_percent double, ADD COLUMN pop_Absolute_percent double, 
  ADD COLUMN hhs_Absolute_percent double, ADD COLUMN jobs_Absolute_percent double, 
  ADD COLUMN sf_tot_Absolute_percent double, ADD COLUMN lv_tot_Absolute_percent double;
  
CREATE INDEX gridcells_2030_grid_id
     on gridcells_2030 (grid_id);

INSERT INTO gridcells_2030
SELECT yr_a.grid_id AS grid_id,
  yr_a.city_id AS ci_id,
  yr_a.county_id AS co_id,
  yr_a.dt_id AS dt_id_a,
  if(yr_a.dur IS NULL,0,yr_a.dur) AS dur_a,
  if(yr_a.iv_r IS NULL,0,yr_a.iv_r) AS iv_r_a,
  if(yr_a.sf_c IS NULL,0,yr_a.sf_c) AS sf_c_a,
  if(yr_a.iv_c IS NULL,0,yr_a.iv_c) AS iv_c_a,
  if(yr_a.sf_i IS NULL,0,yr_a.sf_i) AS sf_i_a,
  if(yr_a.iv_i IS NULL,0,yr_a.iv_i) AS iv_i_a,
  if(yr_a.sf_g IS NULL,0,yr_a.sf_g) AS sf_g_a,
  if(yr_a.iv_g IS NULL,0,yr_a.iv_g) AS iv_g_a,
  if(yr_a.lv_r IS NULL,0,yr_a.lv_r) AS lv_r_a,
  if(yr_a.lv_nr IS NULL,0,yr_a.lv_nr) AS lv_nr_a,
  NULL AS sf_tot_a,
  NULL AS lv_tot_a,
  if(yr_a.js_hb IS NULL,0,yr_a.js_hb) AS js_hb_a,
  if(yr_a.js_nhb IS NULL,0,yr_a.js_nhb) AS js_nhb_a,
  NULL AS js_tot_a,
  if(yr_a.hhs IS NULL,0,yr_a.hhs) AS hhs_a,
  if(yr_a.pop IS NULL,0,yr_a.pop) AS pop_a,
  if(yr_a.wrkrs IS NULL,0,yr_a.wrkrs) AS wrkrs_a,
  if(yr_a.totinc IS NULL,0,yr_a.totinc) AS totinc_a,
  if(yr_a.child IS NULL,0,yr_a.child) AS child_a,
  yr_a.ageh_avg AS ageh_a,
  if(yr_a.jobs IS NULL,0,yr_a.jobs) AS jobs_a,
  yr_a.hb_pct AS hb_pct_a,
  yr_a.j_3p AS j_3p_a,
  NULL AS vr_r_a,
  NULL AS vr_nr_a,
  NULL AS hhsz_a,
  NULL AS hhin_a,
  yr_z.dt_id AS dt_id_z,
  if(yr_z.dur IS NULL,0,yr_z.dur) AS dur_z,
  if(yr_z.iv_r IS NULL,0,yr_z.iv_r) AS iv_r_z,
  if(yr_z.sf_c IS NULL,0,yr_z.sf_c) AS sf_c_z,
  if(yr_z.iv_c IS NULL,0,yr_z.iv_c) AS iv_c_z,
  if(yr_z.sf_i IS NULL,0,yr_z.sf_i) AS sf_i_z,
  if(yr_z.iv_i IS NULL,0,yr_z.iv_i) AS iv_i_z,
  if(yr_z.sf_g IS NULL,0,yr_z.sf_g) AS sf_g_z,
  if(yr_z.iv_g IS NULL,0,yr_z.iv_g) AS iv_g_z,
  if(yr_z.lv_r IS NULL,0,yr_z.lv_r) AS lv_r_z,
  if(yr_z.lv_nr IS NULL,0,yr_z.lv_nr) AS lv_nr_z,
  NULL AS sf_tot_z,
  NULL AS lv_tot_z,
  if(yr_z.js_hb IS NULL,0,yr_z.js_hb) AS js_hb_z,
  if(yr_z.js_nhb IS NULL,0,yr_z.js_nhb) AS js_nhb_z,
  NULL AS js_tot_z,
  if(yr_z.hhs IS NULL,0,yr_z.hhs) AS hhs_z,
  if(yr_z.pop IS NULL,0,yr_z.pop) AS pop_z,
  if(yr_z.wrkrs IS NULL,0,yr_z.wrkrs) AS wrkrs_z,
  if(yr_z.totinc IS NULL,0,yr_z.totinc) AS totinc_z,
  if(yr_z.child IS NULL,0,yr_z.child) AS child_z,
  yr_z.ageh_avg AS ageh_z,
  if(yr_z.jobs IS NULL,0,yr_z.jobs) AS jobs_z,
  yr_z.hb_pct AS hb_pct_z,
  yr_z.j_3p AS j_3p_z,
  NULL AS vr_r_z,
  NULL AS vr_nr_z,
  NULL AS hhsz_z,
  NULL AS hhin_z,
  if(yr_z.dt_id=yr_a.dt_id,NULL,yr_z.dt_id) AS dt_id_d,
  NULL AS dur_d,
  NULL AS iv_r_d,
  NULL AS sf_c_d,
  NULL AS iv_c_d,
  NULL AS sf_i_d,
  NULL AS iv_i_d,
  NULL AS sf_g_d,
  NULL AS iv_g_d,
  NULL AS lv_r_d,
  NULL AS lv_nr_d,
  NULL AS sf_tot_d,
  NULL AS lv_tot_d,
  NULL AS js_hb_d,
  NULL AS js_nhb_d,
  NULL AS js_tot_d,
  NULL AS hhs_d,
  NULL AS pop_d,
  NULL AS wrkrs_d,
  NULL AS totinc_d,
  NULL AS child_d,
  NULL AS ageh_d,
  NULL AS jobs_d,
  NULL AS hb_pct_d,
  NULL AS j_3p_d,
  NULL AS vr_r_d,
  NULL AS vr_nr_d,
  NULL AS hhsz_d,
  NULL AS hhin_d,
  
  NULL AS dur_dl, 
  NULL AS sf_tot_dl, 
  NULL AS hhs_dl, 
  NULL AS pop_dl, 
  NULL AS jobs_dl,
  NULL AS lv_tot_dl,
  
  NULL AS dur_Change_percent,
  NULL AS pop_Change_percent,
  NULL AS hhs_Change_percent,
  NULL AS jobs_Change_percent,
  NULL AS sf_tot_Change_percent,
  NULL AS lv_tot_Change_percent,
  NULL AS dur_Change_percent,
  NULL AS pop_Absolute_percent,
  NULL AS hhs_Absolute_percent,
  NULL AS jobs_Absolute_percent,
  NULL AS sf_tot_Absolute_percent,
  NULL AS lv_tot_Absolute_percent
FROM gridcells_endyears_short AS yr_a,
  gridcells_endyears_short AS yr_z
WHERE yr_a.year=1997 AND
  yr_z.year=2030 AND
  yr_a.grid_id=yr_z.grid_id;

UPDATE gridcells_2030
     SET  sf_tot_a = sf_c_a + sf_i_a + sf_g_a,
          lv_tot_a = lv_r_a + lv_nr_a,
          js_tot_a = js_hb_a + js_nhb_a,
          sf_tot_z = sf_c_z + sf_i_z + sf_g_z,
          lv_tot_z = lv_r_z + lv_nr_z,
          js_tot_z = js_hb_z + js_nhb_z,
          dur_d = dur_z - dur_a,
          iv_r_d = iv_r_z - iv_r_a,
          sf_c_d = sf_c_z - sf_c_a,
          iv_c_d = iv_c_z - iv_c_a,
          sf_i_d = sf_i_z - sf_i_a,
          iv_i_d = iv_i_z - iv_i_a,
          sf_g_d = sf_g_z - sf_g_a,
          iv_g_d = iv_g_z - iv_g_a,
          lv_r_d = lv_r_z - lv_r_a,
          lv_nr_d = lv_nr_z - lv_nr_a,
          js_hb_d = js_hb_z - js_hb_a,
          js_nhb_d = js_nhb_z - js_nhb_a,
          js_tot_d = js_hb_z + js_nhb_z - js_hb_a - js_nhb_a,
          sf_tot_d = sf_c_z + sf_i_z + sf_g_z - sf_c_a - sf_i_a - sf_g_a,
          lv_tot_d = lv_r_z + lv_nr_z - lv_r_a - lv_nr_a,
          hhs_d = hhs_z - hhs_a,
          pop_d = pop_z - pop_a,
          wrkrs_d = wrkrs_z - wrkrs_a,
          totinc_d = totinc_z - totinc_a,
          child_d = child_z - child_a,
          ageh_d = ageh_z - ageh_a,
          jobs_d = jobs_z - jobs_a,
          hb_pct_d = hb_pct_z - hb_pct_a,
          j_3p_d = j_3p_z - j_3p_a,
          vr_r_a = 1-(hhs_a/dur_a),
          vr_nr_a = 1-(jobs_a/(js_hb_a + js_nhb_a)),
          vr_r_z = 1-(hhs_z/dur_z),
          vr_nr_z = 1-(jobs_z/(js_hb_z + js_nhb_z)),
          vr_r_d = (hhs_a/dur_a) - (hhs_z/dur_z),
          vr_nr_d = (jobs_a/(js_hb_a + js_nhb_a)) - (jobs_z/(js_hb_z + js_nhb_z)),
          hhsz_a = pop_a/hhs_a,
          hhsz_z = pop_z/hhs_z,
          hhsz_d = (pop_z/hhs_z) - (pop_a/hhs_a),
          hhin_a = totinc_a/hhs_a,
          hhin_z = totinc_z/hhs_z,
          hhin_d = (totinc_z/hhs_z) - (totinc_a/hhs_a);

UPDATE gridcells_2030 AS a
     INNER JOIN WFRC_1997_output_2030_LRP.gridcells_2030 AS LRP
          ON a.grid_id=LRP.grid_id
     SET  a.dur_dl    = a.dur_z    - LRP.dur_z,
          a.sf_tot_dl = a.sf_tot_z - LRP.sf_tot_z,
          a.hhs_dl    = a.hhs_z    - LRP.hhs_z,
          a.pop_dl    = a.pop_z    - LRP.pop_z,
          a.jobs_dl   = a.jobs_z   - LRP.jobs_z,
          a.lv_tot_dl = a.lv_tot_z - LRP.lv_tot_z;

UPDATE gridcells_2030 AS a
     INNER JOIN WFRC_1997_output_2030_LRP.gridcells_2030 AS LRP
          ON a.grid_id=LRP.grid_id
     SET  a.pop_Change_percent = (a.pop_d - LRP.pop_d) / ABS(LRP.pop_d),
          a.hhs_Change_percent = (a.hhs_d - LRP.hhs_d) / ABS(LRP.hhs_d),
          a.jobs_Change_percent = (a.jobs_d - LRP.jobs_d) / ABS(LRP.jobs_d),
          a.dur_Change_percent = (a.dur_d - LRP.dur_d) / ABS(LRP.dur_d),
          a.sf_tot_Change_percent = (a.sf_tot_d - LRP.sf_tot_d) / ABS(LRP.sf_tot_d),
          a.lv_tot_Change_percent = (a.lv_tot_d - LRP.lv_tot_d) / ABS(LRP.lv_tot_d);

UPDATE gridcells_2030 AS a
     INNER JOIN WFRC_1997_output_2030_LRP.gridcells_2030 AS LRP
          ON a.grid_id=LRP.grid_id
     SET  a.pop_Absolute_percent = (a.pop_z - LRP.pop_z) / ABS(LRP.pop_z),
          a.hhs_Absolute_percent = (a.hhs_z - LRP.hhs_z) / ABS(LRP.hhs_z),
          a.jobs_Absolute_percent = (a.jobs_z - LRP.jobs_z) / ABS(LRP.jobs_z),
          a.dur_Absolute_percent = (a.dur_z - LRP.dur_z) / ABS(LRP.dur_z),
          a.sf_tot_Absolute_percent = (a.sf_tot_z - LRP.sf_tot_z) / ABS(LRP.sf_tot_z),
          a.lv_tot_Absolute_percent = (a.lv_tot_z - LRP.lv_tot_z) / ABS(LRP.lv_tot_z);


#tp  select year, sum(residential_units) as residential_units from gridcells_exported where year=1997 or year=2030 group by year;
#tp  select sum(dur_a), sum(dur_z) from gridcells_2030;
#tp  select year, sum(commercial_sqft+industrial_sqft+governmental_sqft) as nonresidential_sqft 
#tp       from gridcells_exported where year=1997 or year=2030 group by year;
#tp  select sum(sf_c_a+sf_i_a+sf_g_a), sum(sf_c_z+sf_i_z+sf_g_z) 
#tp       from gridcells_2030;
#tp  select year, count(*) as households from households_exported where year=1997 or year=2030 group by year;
#tp  select sum(hhs_a), sum(hhs_z) from gridcells_2030;
#tp  select year, count(*) as jobs from jobs_exported where year=1997 or year=2030 group by year;
#tp  select sum(jobs_a), sum(jobs_z) from gridcells_2030;

# Aggregate gridcell data to the city level

DROP TABLE IF EXISTS city_2030;
CREATE TABLE city_2030 (ci_id int, ci_na text);
     
ALTER TABLE city_2030
  ADD COLUMN dur_a int, ADD COLUMN iv_r_a double, 
  ADD COLUMN sf_c_a double, ADD COLUMN iv_c_a double, ADD COLUMN sf_i_a double, ADD COLUMN iv_i_a double, ADD COLUMN sf_g_a double, 
  ADD COLUMN iv_g_a double, ADD COLUMN lv_r_a double, ADD COLUMN lv_nr_a double, ADD COLUMN sf_tot_a double, ADD COLUMN lv_tot_a double, 
  ADD COLUMN js_hb_a double, ADD COLUMN js_nhb_a double, ADD COLUMN js_tot_a double,
  ADD COLUMN hhs_a double, ADD COLUMN pop_a double, ADD COLUMN wrkrs_a double, ADD COLUMN totinc_a double, ADD COLUMN child_a double, 
  ADD COLUMN ageh_a double, ADD COLUMN jobs_a double, ADD COLUMN hb_pct_a double, ADD COLUMN j_3p_a double,
  ADD COLUMN vr_r_a double, ADD COLUMN vr_nr_a double, ADD COLUMN hhsz_a double, ADD COLUMN hhin_a double,
  
  ADD COLUMN dur_z int, ADD COLUMN iv_r_z double,
  ADD COLUMN sf_c_z double, ADD COLUMN iv_c_z double, ADD COLUMN sf_i_z double, ADD COLUMN iv_i_z double, ADD COLUMN sf_g_z double, 
  ADD COLUMN iv_g_z double, ADD COLUMN lv_r_z double, ADD COLUMN lv_nr_z double, ADD COLUMN sf_tot_z double, ADD COLUMN lv_tot_z double, 
  ADD COLUMN js_hb_z double, ADD COLUMN js_nhb_z double, ADD COLUMN js_tot_z double,
  ADD COLUMN hhs_z double, ADD COLUMN pop_z double, ADD COLUMN wrkrs_z double, ADD COLUMN totinc_z double, ADD COLUMN child_z double, 
  ADD COLUMN ageh_z double, ADD COLUMN jobs_z double, ADD COLUMN hb_pct_z double, ADD COLUMN j_3p_z double,
  ADD COLUMN vr_r_z double, ADD COLUMN vr_nr_z double, ADD COLUMN hhsz_z double, ADD COLUMN hhin_z double,

  ADD COLUMN dur_d int, ADD COLUMN iv_r_d double, 
  ADD COLUMN sf_c_d double, ADD COLUMN iv_c_d double, ADD COLUMN sf_i_d double, ADD COLUMN iv_i_d double, ADD COLUMN sf_g_d double, 
  ADD COLUMN iv_g_d double, ADD COLUMN lv_r_d double, ADD COLUMN lv_nr_d double, ADD COLUMN sf_tot_d double, ADD COLUMN lv_tot_d double, 
  ADD COLUMN js_hb_d double, ADD COLUMN js_nhb_d double, ADD COLUMN js_tot_d double,
  ADD COLUMN hhs_d double, ADD COLUMN pop_d double, ADD COLUMN wrkrs_d double, ADD COLUMN totinc_d double, ADD COLUMN child_d double, 
  ADD COLUMN ageh_d double, ADD COLUMN jobs_d double, ADD COLUMN hb_pct_d double, ADD COLUMN j_3p_d double,
  ADD COLUMN vr_r_d double, ADD COLUMN vr_nr_d double, ADD COLUMN hhsz_d double, ADD COLUMN hhin_d double;

CREATE INDEX city_2030_ci_id
     ON city_2030 (ci_id);
   
INSERT INTO city_2030
SELECT ci_id AS ci_id,
    NULL AS ci_na,
    SUM(dur_a) AS dur_a, 
    SUM(iv_r_a) AS iv_r_a, 
    SUM(sf_c_a) AS sf_c_a, 
    SUM(iv_c_a) AS iv_c_a, 
    SUM(sf_i_a) AS sf_i_a,
    SUM(iv_i_a) AS iv_i_a, 
    SUM(sf_g_a) AS sf_g_a, 
    SUM(iv_g_a) AS iv_g_a, 
    SUM(lv_r_a) AS lv_r_a, 
    SUM(lv_nr_a) AS lv_nr_a, 
    SUM(sf_tot_a) AS sf_tot_a, 
    SUM(lv_tot_a) AS lv_tot_a, 
    SUM(js_hb_a) AS js_hb_a, 
    SUM(js_nhb_a) AS js_nhb_a, 
    SUM(js_tot_a) AS js_tot_a, 
    SUM(hhs_a) AS hhs_a, 
    SUM(pop_a) AS pop_a, 
    SUM(wrkrs_a) AS wrkrs_a, 
    SUM(totinc_a) AS totinc_a, 
    SUM(child_a) AS child_a, 
    AVG(ageh_a) AS ageh_a, 
    SUM(jobs_a) AS jobs_a, 
    AVG(hb_pct_a) AS hb_pct_a, 
    SUM(j_3p_a) AS j_3p_a,
    NULL AS vr_r_a, 
    NULL AS vr_nr_a,
    NULL AS hhsz_a,
    NULL AS hhin_a,

    SUM(dur_z) AS dur_z, 
    SUM(iv_r_z) AS iv_r_z, 
    SUM(sf_c_z) AS sf_c_z, 
    SUM(iv_c_z) AS iv_c_z, 
    SUM(sf_i_z) AS sf_i_z,
    SUM(iv_i_z) AS iv_i_z, 
    SUM(sf_g_z) AS sf_g_z, 
    SUM(iv_g_z) AS iv_g_z, 
    SUM(lv_r_z) AS lv_r_z, 
    SUM(lv_nr_z) AS lv_nr_z, 
    SUM(sf_tot_z) AS sf_tot_z, 
    SUM(lv_tot_z) AS lv_tot_z, 
    SUM(js_hb_z) AS js_hb_z, 
    SUM(js_nhb_z) AS js_nhb_z, 
    SUM(js_tot_z) AS js_tot_z, 
    SUM(hhs_z) AS hhs_z, 
    SUM(pop_z) AS pop_z, 
    SUM(wrkrs_z) AS wrkrs_z, 
    SUM(totinc_z) AS totinc_z, 
    SUM(child_z) AS child_z, 
    AVG(ageh_z) AS ageh_z, 
    SUM(jobs_z) AS jobs_z, 
    AVG(hb_pct_z) AS hb_pct_z, 
    SUM(j_3p_z) AS j_3p_z,
    NULL AS vr_r_z, 
    NULL AS vr_nr_z, 
    NULL AS hhsz_z,
    NULL AS hhin_z,
    
    SUM(dur_d) AS dur_d, 
    SUM(iv_r_d) AS iv_r_d, 
    SUM(sf_c_d) AS sf_c_d, 
    SUM(iv_c_d) AS iv_c_d, 
    SUM(sf_i_d) AS sf_i_d,
    SUM(iv_i_d) AS iv_i_d, 
    SUM(sf_g_d) AS sf_g_d, 
    SUM(iv_g_d) AS iv_g_d, 
    SUM(lv_r_d) AS lv_r_d, 
    SUM(lv_nr_d) AS lv_nr_d, 
    SUM(sf_tot_d) AS sf_tot_d, 
    SUM(lv_tot_d) AS lv_tot_d, 
    SUM(js_hb_d) AS js_hb_d, 
    SUM(js_nhb_d) AS js_nhb_d, 
    SUM(js_tot_d) AS js_tot_d, 
    SUM(hhs_d) AS hhs_d, 
    SUM(pop_d) AS pop_d, 
    SUM(wrkrs_d) AS wrkrs_d, 
    SUM(totinc_d) AS totinc_d, 
    SUM(child_d) AS child_d, 
    NULL AS ageh_d, 
    SUM(jobs_d) AS jobs_d, 
    NULL AS hb_pct_d, 
    SUM(j_3p_d) AS j_3p_d,
    NULL AS vr_r_d, 
    NULL AS vr_nr_d,
    NULL AS hhsz_d,
    NULL AS hhin_d
FROM gridcells_2030
GROUP BY ci_id;

update city_2030
     set vr_r_a = 1 - (hhs_a/dur_a),
          vr_nr_a = 1 - (jobs_a/js_tot_a),
          vr_r_z = 1 - (hhs_z/dur_z),
          vr_nr_z = 1 - (jobs_z/js_tot_z),
          vr_r_d = (hhs_a/dur_a) - (hhs_z/dur_z),
          vr_nr_d = (jobs_a/js_tot_a) - (jobs_z/js_tot_z),
          ageh_d = ageh_z - ageh_d,
          hb_pct_d = hb_pct_z - hb_pct_a,
          hhsz_a = pop_a/hhs_a,
          hhsz_z = pop_z/hhs_z,
          hhsz_d = (pop_z/hhs_z) - (pop_a/hhs_a),
          hhin_a = totinc_a/hhs_a,
          hhin_z = totinc_z/hhs_z,
          hhin_d = (totinc_z/hhs_z) - (totinc_a/hhs_a);

update city_2030 AS a, WFRC_1997_baseyear.cities AS b
     set a.ci_na = b.city_name
     where a.ci_id = b.city_id;

# Aggregate gridcell data to the county level

DROP TABLE IF EXISTS county_2030;
CREATE TABLE county_2030 (co_id int, co_na text);
     
ALTER TABLE county_2030
  ADD COLUMN dur_a int, ADD COLUMN iv_r_a double, 
  ADD COLUMN sf_c_a double, ADD COLUMN iv_c_a double, ADD COLUMN sf_i_a double, ADD COLUMN iv_i_a double, ADD COLUMN sf_g_a double, 
  ADD COLUMN iv_g_a double, ADD COLUMN lv_r_a double, ADD COLUMN lv_nr_a double, ADD COLUMN sf_tot_a double, ADD COLUMN lv_tot_a double, 
  ADD COLUMN js_hb_a double, ADD COLUMN js_nhb_a double, ADD COLUMN js_tot_a double,
  ADD COLUMN hhs_a double, ADD COLUMN pop_a double, ADD COLUMN wrkrs_a double, ADD COLUMN totinc_a double, ADD COLUMN child_a double, 
  ADD COLUMN ageh_a double, ADD COLUMN jobs_a double, ADD COLUMN hb_pct_a double, ADD COLUMN j_3p_a double,
  ADD COLUMN vr_r_a double, ADD COLUMN vr_nr_a double, ADD COLUMN hhsz_a double, ADD COLUMN hhin_a double,
  
  ADD COLUMN dur_z int, ADD COLUMN iv_r_z double,
  ADD COLUMN sf_c_z double, ADD COLUMN iv_c_z double, ADD COLUMN sf_i_z double, ADD COLUMN iv_i_z double, ADD COLUMN sf_g_z double, 
  ADD COLUMN iv_g_z double, ADD COLUMN lv_r_z double, ADD COLUMN lv_nr_z double, ADD COLUMN sf_tot_z double, ADD COLUMN lv_tot_z double, 
  ADD COLUMN js_hb_z double, ADD COLUMN js_nhb_z double, ADD COLUMN js_tot_z double,
  ADD COLUMN hhs_z double, ADD COLUMN pop_z double, ADD COLUMN wrkrs_z double, ADD COLUMN totinc_z double, ADD COLUMN child_z double, 
  ADD COLUMN ageh_z double, ADD COLUMN jobs_z double, ADD COLUMN hb_pct_z double, ADD COLUMN j_3p_z double,
  ADD COLUMN vr_r_z double, ADD COLUMN vr_nr_z double, ADD COLUMN hhsz_z double, ADD COLUMN hhin_z double,

  ADD COLUMN dur_d int, ADD COLUMN iv_r_d double, 
  ADD COLUMN sf_c_d double, ADD COLUMN iv_c_d double, ADD COLUMN sf_i_d double, ADD COLUMN iv_i_d double, ADD COLUMN sf_g_d double, 
  ADD COLUMN iv_g_d double, ADD COLUMN lv_r_d double, ADD COLUMN lv_nr_d double, ADD COLUMN sf_tot_d double, ADD COLUMN lv_tot_d double, 
  ADD COLUMN js_hb_d double, ADD COLUMN js_nhb_d double, ADD COLUMN js_tot_d double,
  ADD COLUMN hhs_d double, ADD COLUMN pop_d double, ADD COLUMN wrkrs_d double, ADD COLUMN totinc_d double, ADD COLUMN child_d double, 
  ADD COLUMN ageh_d double, ADD COLUMN jobs_d double, ADD COLUMN hb_pct_d double, ADD COLUMN j_3p_d double,
  ADD COLUMN vr_r_d double, ADD COLUMN vr_nr_d double, ADD COLUMN hhsz_d double, ADD COLUMN hhin_d double;

CREATE INDEX county_2030_co_id
     ON county_2030 (co_id);
   
INSERT INTO county_2030
SELECT co_id AS co_id,
    NULL AS co_na,
    SUM(dur_a) AS dur_a, 
    SUM(iv_r_a) AS iv_r_a, 
    SUM(sf_c_a) AS sf_c_a, 
    SUM(iv_c_a) AS iv_c_a, 
    SUM(sf_i_a) AS sf_i_a,
    SUM(iv_i_a) AS iv_i_a, 
    SUM(sf_g_a) AS sf_g_a, 
    SUM(iv_g_a) AS iv_g_a, 
    SUM(lv_r_a) AS lv_r_a, 
    SUM(lv_nr_a) AS lv_nr_a, 
    SUM(sf_tot_a) AS sf_tot_a, 
    SUM(lv_tot_a) AS lv_tot_a, 
    SUM(js_hb_a) AS js_hb_a, 
    SUM(js_nhb_a) AS js_nhb_a, 
    SUM(js_tot_a) AS js_tot_a, 
    SUM(hhs_a) AS hhs_a, 
    SUM(pop_a) AS pop_a, 
    SUM(wrkrs_a) AS wrkrs_a, 
    SUM(totinc_a) AS totinc_a, 
    SUM(child_a) AS child_a, 
    AVG(ageh_a) AS ageh_a, 
    SUM(jobs_a) AS jobs_a, 
    AVG(hb_pct_a) AS hb_pct_a, 
    SUM(j_3p_a) AS j_3p_a,
    NULL AS vr_r_a, 
    NULL AS vr_nr_a,
    NULL AS hhsz_a,
    NULL AS hhin_a,

    SUM(dur_z) AS dur_z, 
    SUM(iv_r_z) AS iv_r_z, 
    SUM(sf_c_z) AS sf_c_z, 
    SUM(iv_c_z) AS iv_c_z, 
    SUM(sf_i_z) AS sf_i_z,
    SUM(iv_i_z) AS iv_i_z, 
    SUM(sf_g_z) AS sf_g_z, 
    SUM(iv_g_z) AS iv_g_z, 
    SUM(lv_r_z) AS lv_r_z, 
    SUM(lv_nr_z) AS lv_nr_z, 
    SUM(sf_tot_z) AS sf_tot_z, 
    SUM(lv_tot_z) AS lv_tot_z, 
    SUM(js_hb_z) AS js_hb_z, 
    SUM(js_nhb_z) AS js_nhb_z, 
    SUM(js_tot_z) AS js_tot_z, 
    SUM(hhs_z) AS hhs_z, 
    SUM(pop_z) AS pop_z, 
    SUM(wrkrs_z) AS wrkrs_z, 
    SUM(totinc_z) AS totinc_z, 
    SUM(child_z) AS child_z, 
    AVG(ageh_z) AS ageh_z, 
    SUM(jobs_z) AS jobs_z, 
    AVG(hb_pct_z) AS hb_pct_z,  
    SUM(j_3p_z) AS j_3p_z,
    NULL AS vr_r_z, 
    NULL AS vr_nr_z, 
    NULL AS hhsz_z,
    NULL AS hhin_z,
    
    SUM(dur_d) AS dur_d, 
    SUM(iv_r_d) AS iv_r_d, 
    SUM(sf_c_d) AS sf_c_d, 
    SUM(iv_c_d) AS iv_c_d, 
    SUM(sf_i_d) AS sf_i_d,
    SUM(iv_i_d) AS iv_i_d, 
    SUM(sf_g_d) AS sf_g_d, 
    SUM(iv_g_d) AS iv_g_d, 
    SUM(lv_r_d) AS lv_r_d, 
    SUM(lv_nr_d) AS lv_nr_d, 
    SUM(sf_tot_d) AS sf_tot_d, 
    SUM(lv_tot_d) AS lv_tot_d, 
    SUM(js_hb_d) AS js_hb_d, 
    SUM(js_nhb_d) AS js_nhb_d, 
    SUM(js_tot_d) AS js_tot_d, 
    SUM(hhs_d) AS hhs_d, 
    SUM(pop_d) AS pop_d, 
    SUM(wrkrs_d) AS wrkrs_d, 
    SUM(totinc_d) AS totinc_d, 
    SUM(child_d) AS child_d, 
    NULL AS ageh_d, 
    SUM(jobs_d) AS jobs_d, 
    NULL AS hb_pct_d,  
    SUM(j_3p_d) AS j_3p_d,
    NULL AS vr_r_d, 
    NULL AS vr_nr_d,
    NULL AS hhsz_d,
    NULL AS hhin_d
FROM gridcells_2030
GROUP BY co_id;

update county_2030
     set vr_r_a = 1 - (hhs_a/dur_a),
          vr_nr_a = 1 - (jobs_a/js_tot_a),
          vr_r_z = 1 - (hhs_z/dur_z),
          vr_nr_z = 1 - (jobs_z/js_tot_z),
          vr_r_d = (hhs_a/dur_a) - (hhs_z/dur_z),
          vr_nr_d = (jobs_a/js_tot_a) - (jobs_z/js_tot_z),
          ageh_d = ageh_z - ageh_d,
          hb_pct_d = hb_pct_z - hb_pct_a,
          hhsz_a = pop_a/hhs_a,
          hhsz_z = pop_z/hhs_z,
          hhsz_d = (pop_z/hhs_z) - (pop_a/hhs_a),
          hhin_a = totinc_a/hhs_a,
          hhin_z = totinc_z/hhs_z,
          hhin_d = (totinc_z/hhs_z) - (totinc_a/hhs_a);

update county_2030 AS a, WFRC_1997_baseyear.counties AS b
     set a.co_na = b.county_name
     where a.co_id = b.county_id;

# Aggregate zone data to the small district level

DROP TABLE IF EXISTS distsml_2030;
CREATE TABLE distsml_2030 (distsml int, distmed int, distlrg int, county int);
     
ALTER TABLE distsml_2030
  ADD COLUMN dur_a int, ADD COLUMN iv_r_a double, 
  ADD COLUMN sf_c_a double, ADD COLUMN iv_c_a double, ADD COLUMN sf_i_a double, ADD COLUMN iv_i_a double, ADD COLUMN sf_g_a double, 
  ADD COLUMN iv_g_a double, ADD COLUMN lv_r_a double, ADD COLUMN lv_nr_a double, ADD COLUMN sf_tot_a double, ADD COLUMN lv_tot_a double, 
  ADD COLUMN js_hb_a double, ADD COLUMN js_nhb_a double, ADD COLUMN js_tot_a double,
  ADD COLUMN sf_exc_a int, ADD COLUMN dur_exc_a int,
  ADD COLUMN hhs_a double, ADD COLUMN pop_a double, ADD COLUMN wrkrs_a double, ADD COLUMN totinc_a double, ADD COLUMN child_a double, 
  ADD COLUMN ageh_a double, ADD COLUMN jobs_a double, ADD COLUMN hb_pct_a double, ADD COLUMN j_3p_a double,
  ADD COLUMN vr_r_a double, ADD COLUMN vr_nr_a double, ADD COLUMN hhsz_a double, ADD COLUMN hhin_a double,
  ADD COLUMN hae0_a double, ADD COLUMN hae1_a double, ADD COLUMN hae2_a double, ADD COLUMN hae3_a double, 
  ADD COLUMN hap0_a double, ADD COLUMN hap1_a double, ADD COLUMN hap2_a double, ADD COLUMN hap3_a double, 
  ADD COLUMN wae0_a double, ADD COLUMN wae1_a double, ADD COLUMN wae2_a double, ADD COLUMN wae3_a double, 
  ADD COLUMN wap0_a double, ADD COLUMN wap1_a double, ADD COLUMN wap2_a double, ADD COLUMN wap3_a double,
  
  ADD COLUMN dur_z int, ADD COLUMN iv_r_z double,
  ADD COLUMN sf_c_z double, ADD COLUMN iv_c_z double, ADD COLUMN sf_i_z double, ADD COLUMN iv_i_z double, ADD COLUMN sf_g_z double, 
  ADD COLUMN iv_g_z double, ADD COLUMN lv_r_z double, ADD COLUMN lv_nr_z double, ADD COLUMN sf_tot_z double, ADD COLUMN lv_tot_z double, 
  ADD COLUMN js_hb_z double, ADD COLUMN js_nhb_z double, ADD COLUMN js_tot_z double,
  ADD COLUMN sf_exc_z int, ADD COLUMN dur_exc_z int,
  ADD COLUMN hhs_z double, ADD COLUMN pop_z double, ADD COLUMN wrkrs_z double, ADD COLUMN totinc_z double, ADD COLUMN child_z double, 
  ADD COLUMN ageh_z double, ADD COLUMN jobs_z double, ADD COLUMN hb_pct_z double, ADD COLUMN j_3p_z double,
  ADD COLUMN vr_r_z double, ADD COLUMN vr_nr_z double, ADD COLUMN hhsz_z double, ADD COLUMN hhin_z double,
  ADD COLUMN hae0_z double, ADD COLUMN hae1_z double, ADD COLUMN hae2_z double, ADD COLUMN hae3_z double, 
  ADD COLUMN hap0_z double, ADD COLUMN hap1_z double, ADD COLUMN hap2_z double, ADD COLUMN hap3_z double, 
  ADD COLUMN wae0_z double, ADD COLUMN wae1_z double, ADD COLUMN wae2_z double, ADD COLUMN wae3_z double, 
  ADD COLUMN wap0_z double, ADD COLUMN wap1_z double, ADD COLUMN wap2_z double, ADD COLUMN wap3_z double,

  ADD COLUMN dur_d int, ADD COLUMN iv_r_d double, 
  ADD COLUMN sf_c_d double, ADD COLUMN iv_c_d double, ADD COLUMN sf_i_d double, ADD COLUMN iv_i_d double, ADD COLUMN sf_g_d double, 
  ADD COLUMN iv_g_d double, ADD COLUMN lv_r_d double, ADD COLUMN lv_nr_d double, ADD COLUMN sf_tot_d double, ADD COLUMN lv_tot_d double, 
  ADD COLUMN js_hb_d double, ADD COLUMN js_nhb_d double, ADD COLUMN js_tot_d double,
  ADD COLUMN sf_exc_d int, ADD COLUMN dur_exc_d int,
  ADD COLUMN hhs_d double, ADD COLUMN pop_d double, ADD COLUMN wrkrs_d double, ADD COLUMN totinc_d double, ADD COLUMN child_d double, 
  ADD COLUMN ageh_d double, ADD COLUMN jobs_d double, ADD COLUMN hb_pct_d double, ADD COLUMN j_3p_d double,
  ADD COLUMN vr_r_d double, ADD COLUMN vr_nr_d double, ADD COLUMN hhsz_d double, ADD COLUMN hhin_d double,
  ADD COLUMN hae0_d double, ADD COLUMN hae1_d double, ADD COLUMN hae2_d double, ADD COLUMN hae3_d double, 
  ADD COLUMN hap0_d double, ADD COLUMN hap1_d double, ADD COLUMN hap2_d double, ADD COLUMN hap3_d double, 
  ADD COLUMN wae0_d double, ADD COLUMN wae1_d double, ADD COLUMN wae2_d double, ADD COLUMN wae3_d double, 
  ADD COLUMN wap0_d double, ADD COLUMN wap1_d double, ADD COLUMN wap2_d double, ADD COLUMN wap3_d double,
  
  ADD COLUMN dur_dl int, ADD COLUMN sf_tot_dl double, ADD COLUMN hhs_dl double, ADD COLUMN pop_dl double, 
  ADD COLUMN jobs_dl double, ADD COLUMN hae1_dl double, ADD COLUMN lv_tot_dl double;

ALTER TABLE distsml_2030
  ADD COLUMN dur_Change_percent double,
  ADD COLUMN pop_Change_percent double, ADD COLUMN hhs_Change_percent double, 
  ADD COLUMN jobs_Change_percent double, ADD COLUMN sf_tot_Change_percent double,
  ADD COLUMN hae1_Change_percent double, ADD COLUMN lv_tot_Change_percent double,
  ADD COLUMN dur_Absolute_percent double,
  ADD COLUMN pop_Absolute_percent double, ADD COLUMN hhs_Absolute_percent double, 
  ADD COLUMN jobs_Absolute_percent double, ADD COLUMN sf_tot_Absolute_percent double,
  ADD COLUMN hae1_Absolute_percent double, ADD COLUMN lv_tot_Absolute_percent double;
  
CREATE INDEX distsml_2030_distsml
     ON distsml_2030 (distsml);
     
INSERT INTO distsml_2030
SELECT distsml AS distsml,
    MAX(distmed) AS distmed,
    MAX(distlrg) AS distlrg,
    MAX(county) AS county,
    SUM(dur_a) AS dur_a, 
    SUM(iv_r_a) AS iv_r_a, 
    SUM(sf_c_a) AS sf_c_a, 
    SUM(iv_c_a) AS iv_c_a, 
    SUM(sf_i_a) AS sf_i_a,
    SUM(iv_i_a) AS iv_i_a, 
    SUM(sf_g_a) AS sf_g_a, 
    SUM(iv_g_a) AS iv_g_a, 
    SUM(lv_r_a) AS lv_r_a, 
    SUM(lv_nr_a) AS lv_nr_a, 
    SUM(sf_tot_a) AS sf_tot_a, 
    SUM(lv_tot_a) AS lv_tot_a, 
    SUM(js_hb_a) AS js_hb_a, 
    SUM(js_nhb_a) AS js_nhb_a, 
    SUM(js_tot_a) AS js_tot_a, 
    SUM(sf_exc_a) AS sf_exc_a,
    SUM(dur_exc_a) AS dur_exc_a,
    SUM(hhs_a) AS hhs_a, 
    SUM(pop_a) AS pop_a, 
    SUM(wrkrs_a) AS wrkrs_a, 
    SUM(totinc_a) AS totinc_a, 
    SUM(child_a) AS child_a, 
    AVG(ageh_a) AS ageh_a, 
    SUM(jobs_a) AS jobs_a, 
    AVG(hb_pct_a) AS hb_pct_a, 
    SUM(j_3p_a) AS j_3p_a,
    NULL AS vr_r_a, 
    NULL AS vr_nr_a, 
    NULL AS hhsz_a,
    NULL AS hhin_a,
    AVG(hae0_a) AS hae0_a, 
    AVG(hae1_a) AS hae1_a, 
    AVG(hae2_a) AS hae2_a, 
    AVG(hae3_a) AS hae3_a,
    AVG(hap0_a) AS hap0_a, 
    AVG(hap1_a) AS hap1_a, 
    AVG(hap2_a) AS hap2_a, 
    AVG(hap3_a) AS hap3_a, 
    AVG(wae0_a) AS wae0_a, 
    AVG(wae1_a) AS wae1_a, 
    AVG(wae2_a) AS wae2_a, 
    AVG(wae3_a) AS wae3_a,
    AVG(wap0_a) AS wap0_a, 
    AVG(wap1_a) AS wap1_a, 
    AVG(wap2_a) AS wap2_a, 
    AVG(wap3_a) AS wap3_a,

    SUM(dur_z) AS dur_z, 
    SUM(iv_r_z) AS iv_r_z, 
    SUM(sf_c_z) AS sf_c_z, 
    SUM(iv_c_z) AS iv_c_z, 
    SUM(sf_i_z) AS sf_i_z,
    SUM(iv_i_z) AS iv_i_z, 
    SUM(sf_g_z) AS sf_g_z, 
    SUM(iv_g_z) AS iv_g_z, 
    SUM(lv_r_z) AS lv_r_z, 
    SUM(lv_nr_z) AS lv_nr_z, 
    SUM(sf_tot_z) AS sf_tot_z, 
    SUM(lv_tot_z) AS lv_tot_z, 
    SUM(js_hb_z) AS js_hb_z, 
    SUM(js_nhb_z) AS js_nhb_z, 
    SUM(js_tot_z) AS js_tot_z, 
    SUM(sf_exc_z) AS sf_exc_z,
    SUM(dur_exc_z) AS dur_exc_z,
    SUM(hhs_z) AS hhs_z, 
    SUM(pop_z) AS pop_z, 
    SUM(wrkrs_z) AS wrkrs_z, 
    SUM(totinc_z) AS totinc_z, 
    SUM(child_z) AS child_z, 
    AVG(ageh_z) AS ageh_z, 
    SUM(jobs_z) AS jobs_z, 
    AVG(hb_pct_z) AS hb_pct_z, 
    SUM(j_3p_z) AS j_3p_z,
    NULL AS vr_r_z, 
    NULL AS vr_nr_z, 
    NULL AS hhsz_z,
    NULL AS hhin_z,
    AVG(hae0_z) AS hae0_z, 
    AVG(hae1_z) AS hae1_z, 
    AVG(hae2_z) AS hae2_z, 
    AVG(hae3_z) AS hae3_z,
    AVG(hap0_z) AS hap0_z, 
    AVG(hap1_z) AS hap1_z, 
    AVG(hap2_z) AS hap2_z, 
    AVG(hap3_z) AS hap3_z, 
    AVG(wae0_z) AS wae0_z, 
    AVG(wae1_z) AS wae1_z, 
    AVG(wae2_z) AS wae2_z, 
    AVG(wae3_z) AS wae3_z,
    AVG(wap0_z) AS wap0_z, 
    AVG(wap1_z) AS wap1_z, 
    AVG(wap2_z) AS wap2_z, 
    AVG(wap3_z) AS wap3_z,
    
    SUM(dur_d) AS dur_d, 
    SUM(iv_r_d) AS iv_r_d, 
    SUM(sf_c_d) AS sf_c_d, 
    SUM(iv_c_d) AS iv_c_d, 
    SUM(sf_i_d) AS sf_i_d,
    SUM(iv_i_d) AS iv_i_d, 
    SUM(sf_g_d) AS sf_g_d, 
    SUM(iv_g_d) AS iv_g_d, 
    SUM(lv_r_d) AS lv_r_d, 
    SUM(lv_nr_d) AS lv_nr_d, 
    SUM(sf_tot_d) AS sf_tot_d, 
    SUM(lv_tot_d) AS lv_tot_d, 
    SUM(js_hb_d) AS js_hb_d, 
    SUM(js_nhb_d) AS js_nhb_d, 
    SUM(js_tot_d) AS js_tot_d, 
    SUM(sf_exc_d) AS sf_exc_d,
    SUM(dur_exc_d) AS dur_exc_d,
    SUM(hhs_d) AS hhs_d, 
    SUM(pop_d) AS pop_d, 
    SUM(wrkrs_d) AS wrkrs_d, 
    SUM(totinc_d) AS totinc_d, 
    SUM(child_d) AS child_d, 
    NULL AS ageh_d, 
    SUM(jobs_d) AS jobs_d, 
    NULL AS hb_pct_d, 
    SUM(j_3p_d) AS j_3p_d,
    NULL AS vr_r_d, 
    NULL AS vr_nr_d, 
    NULL AS hhsz_d,
    NULL AS hhin_d,
    AVG(hae0_d) AS hae0_d, 
    AVG(hae1_d) AS hae1_d, 
    AVG(hae2_d) AS hae2_d, 
    AVG(hae3_d) AS hae3_d,
    AVG(hap0_d) AS hap0_d, 
    AVG(hap1_d) AS hap1_d, 
    AVG(hap2_d) AS hap2_d,
    AVG(hap3_d) AS hap3_d, 
    AVG(wae0_d) AS wae0_d, 
    AVG(wae1_d) AS wae1_d, 
    AVG(wae2_d) AS wae2_d, 
    AVG(wae3_d) AS wae3_d,
    AVG(wap0_d) AS wap0_d, 
    AVG(wap1_d) AS wap1_d, 
    AVG(wap2_d) AS wap2_d, 
    AVG(wap3_d) AS wap3_d,
    
  NULL AS dur_dl, 
  NULL AS sf_tot_dl, 
  NULL AS hhs_dl, 
  NULL AS pop_dl, 
  NULL AS jobs_dl,
  NULL AS hae1_dl,
  NULL AS lv_tot_dl,
  
  NULL AS dur_Change_percent,
  NULL AS pop_Change_percent,
  NULL AS hhs_Change_percent,
  NULL AS jobs_Change_percent,
  NULL AS sf_tot_Change_percent,
  NULL AS hae1_Change_percent,
  NULL AS lv_tot_Change_percent,
  NULL AS dur_Change_percent,
  NULL AS pop_Absolute_percent,
  NULL AS hhs_Absolute_percent,
  NULL AS jobs_Absolute_percent,
  NULL AS sf_tot_Absolute_percent,
  NULL AS hae1_Absolute_percent,
  NULL AS lv_tot_Absolute_percent
FROM zones_2030
GROUP BY distsml;

update distsml_2030 
     set vr_r_a = 1 - (hhs_a/dur_a),
          vr_nr_a = 1 - (jobs_a/js_tot_a),
          vr_r_z = 1 - (hhs_z/dur_z),
          vr_nr_z = 1 - (jobs_z/js_tot_z),
          vr_r_d = (hhs_a/dur_a) - (hhs_z/dur_z),
          vr_nr_d = (jobs_a/js_tot_a) - (jobs_z/js_tot_z),
          ageh_d = ageh_z - ageh_d,
          hb_pct_d = hb_pct_z - hb_pct_a,
          hhsz_a = pop_a/hhs_a,
          hhsz_z = pop_z/hhs_z,
          hhsz_d = (pop_z/hhs_z) - (pop_a/hhs_a),
          hhin_a = totinc_a/hhs_a,
          hhin_z = totinc_z/hhs_z,
          hhin_d = (totinc_z/hhs_z) - (totinc_a/hhs_a);
     
UPDATE distsml_2030 AS a
     INNER JOIN WFRC_1997_output_2030_LRP.distsml_2030 AS LRP
          ON a.distsml=LRP.distsml
     SET  a.dur_dl    = a.dur_z    - LRP.dur_z,
          a.sf_tot_dl = a.sf_tot_z - LRP.sf_tot_z,
          a.hhs_dl    = a.hhs_z    - LRP.hhs_z,
          a.pop_dl    = a.pop_z    - LRP.pop_z,
          a.jobs_dl   = a.jobs_z   - LRP.jobs_z,
          a.hae1_dl   = a.hae1_z   - LRP.hae1_z,
          a.lv_tot_dl = a.lv_tot_z - LRP.lv_tot_z,
          a.pop_Change_percent = (a.pop_d - LRP.pop_d) / ABS(LRP.pop_d),
          a.hhs_Change_percent = (a.hhs_d - LRP.hhs_d) / ABS(LRP.hhs_d),
          a.jobs_Change_percent = (a.jobs_d - LRP.jobs_d) / ABS(LRP.jobs_d),
          a.dur_Change_percent = (a.dur_d - LRP.dur_d) / ABS(LRP.dur_d),
          a.sf_tot_Change_percent = (a.sf_tot_d - LRP.sf_tot_d) / ABS(LRP.sf_tot_d),
          a.hae1_Change_percent = (a.hae1_d - LRP.hae1_d) / ABS(LRP.hae1_d),
          a.lv_tot_Change_percent = (a.lv_tot_d - LRP.lv_tot_d) / ABS(LRP.lv_tot_d),
          a.pop_Absolute_percent = (a.pop_z - LRP.pop_z) / ABS(LRP.pop_z),
          a.hhs_Absolute_percent = (a.hhs_z - LRP.hhs_z) / ABS(LRP.hhs_z),
          a.jobs_Absolute_percent = (a.jobs_z - LRP.jobs_z) / ABS(LRP.jobs_z),
          a.dur_Absolute_percent = (a.dur_z - LRP.dur_z) / ABS(LRP.dur_z),
          a.sf_tot_Absolute_percent = (a.sf_tot_z - LRP.sf_tot_z) / ABS(LRP.sf_tot_z),
          a.hae1_Absolute_percent = (a.hae1_z - LRP.hae1_z) / ABS(LRP.hae1_z),
          a.lv_tot_Absolute_percent = (a.lv_tot_z - LRP.lv_tot_z) / ABS(LRP.lv_tot_z);

# Create a table of comparisons with census and adopted-forecast data

DROP TABLE IF EXISTS distsml_comparisons;
CREATE TABLE distsml_comparisons
     SELECT a.distsml AS distsml,
        (LN(a.dur_z/a.dur_a))/(2030 - 1997) AS dur_aarc_u,
        (LN(b.census_residential_units_2000/b.census_residential_units_1990))/10 AS dur_aarc_c,
        (LN(a.hhs_z/a.hhs_a))/(2030 - 1997) AS hhs_aarc_u,
        (LN(b.census_households_2000/b.census_households_1990))/10 AS hhs_aarc_c, 
        (LN(a.j_3p_z/a.j_3p_a))/(2030 - 1997) AS jobs_aarc_u,
        (LN(b.census_employment_2001/b.census_employment_1990))/10 AS jobs_aarc_c,
        (LN(a.pop_z/a.pop_a))/(2030 - 1997) AS pop_aarc_u,
        (LN(b.census_population_2000/b.census_population_1990))/10 AS pop_aarc_c,
        (a.dur_z-b.old_method_residential_units_2030) AS dif_DWL,
        (a.hhs_z-b.old_method_households_2030) AS dif_HH,
        (a.j_3p_z-b.old_method_employment_2030) AS dif_EMP,
        (a.pop_z-b.old_method_population_2030) AS dif_POP
     FROM distsml_2030 AS a 
     INNER JOIN WFRC_1997_baseyear.small_districts AS b
          ON a.distsml = b.smalldst;

CREATE INDEX distsml_comparisons_distsml 
     on distsml_comparisons (distsml);

ALTER TABLE distsml_comparisons
     ADD COLUMN dif_dur_aarc double(25,8),
     ADD COLUMN dif_hhs_aarc double(25,8),
     ADD COLUMN dif_jobs_aarc double(25,8),
     ADD COLUMN dif_pop_aarc double(25,8);

UPDATE distsml_comparisons
     SET dif_dur_aarc=(dur_aarc_u-dur_aarc_c),
        dif_hhs_aarc=(hhs_aarc_u-hhs_aarc_c),
        dif_jobs_aarc=(jobs_aarc_u-jobs_aarc_c),
        dif_pop_aarc=(pop_aarc_u-pop_aarc_c);

# Clean up unnecessary tables

DROP TABLE IF EXISTS gridcells_endyears_short;
DROP TABLE IF EXISTS households_endyears;
DROP TABLE IF EXISTS jobs_endyears;
DROP TABLE IF EXISTS zones_endyears_short;
DROP TABLE IF EXISTS households_exported_endyears;
DROP TABLE IF EXISTS jobs_exported_endyears;
DROP TABLE IF EXISTS wedges_endyears;
DROP TABLE IF EXISTS zones_hhdata;
DROP TABLE IF EXISTS zones_jobdata;
DROP TABLE IF EXISTS zones_gcdata;
DROP TABLE IF EXISTS accessibilities_endyears;
DROP TABLE IF EXISTS gridcells_hhdata;
DROP TABLE IF EXISTS gridcells_jobdata;
DROP TABLE IF EXISTS gridcells_exported_endyears;

