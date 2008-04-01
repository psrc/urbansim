##Residential vacancy rates

  # 1.create indices for output tables 
CREATE INDEX households_exported_year_household_id_grid_id_index on households_exported (YEAR, HOUSEHOLD_ID,GRID_ID);
CREATE INDEX households_constants_household_id_index on households_constants (HOUSEHOLD_ID);

  # 2.create temporary needed table and create indices for these tables  
DROP TABLE IF EXISTS tmp_households_by_year;
CREATE TEMPORARY TABLE tmp_households_by_year SELECT YEAR,GRID_ID,COUNT(households_exported.HOUSEHOLD_ID) AS HOUSEHOLDS,
SUM(households_constants.PERSONS) AS POPULATION
FROM households_exported
   LEFT JOIN households_constants
   ON households_exported.HOUSEHOLD_ID=households_constants.HOUSEHOLD_ID
GROUP BY GRID_ID,YEAR;

CREATE INDEX tmp_households_by_year_year_grid_id_index on tmp_households_by_year (YEAR,GRID_ID);

  # 3.creat tmp_residential_vacancy_rates_by_devtype
drop table if exists tmp_residential_vacancy_rates_by_devtype;
create table tmp_residential_vacancy_rates_by_devtype 
select grid.YEAR,grid.DEVELOPMENT_TYPE_ID,sum(grid.RESIDENTIAL_UNITS),sum(HOUSEHOLDS) as HOUSEHOLDS,100*(1-sum(HOUSEHOLDS)/sum(RESIDENTIAL_UNITS)) as VACANCY_RATE
from gridcells_exported grid inner join tmp_households_by_year households on grid.YEAR = households.YEAR and grid.GRID_ID = households.GRID_ID
group by grid.YEAR,grid.DEVELOPMENT_TYPE_ID;

##Non residential vacancy rates (by job space)

  # 1.create indices for output tables 
CREATE INDEX jobs_exported_year_job_id_grid_id_index on jobs_exported (YEAR, JOB_ID, GRID_ID);
CREATE INDEX jobs_constants_job_id_index on jobs_constants (JOB_ID);
CREATE INDEX gridcells_exported_year_grid_id_index on gridcells_exported (YEAR, GRID_ID);

  # 2.create temporary needed table and create indices for these tables

DROP TABLE IF EXISTS tmp_jobs_by_year;
CREATE TEMPORARY TABLE tmp_jobs_by_year SELECT YEAR,GRID_ID,COUNT(jobs_exported.JOB_ID) AS JOBS, HOME_BASED as HOME_BASED
FROM jobs_exported
WHERE HOME_BASED=0   
GROUP BY GRID_ID,YEAR;

DROP TABLE IF EXISTS tmp_sqft_for_non_home_based_jobs;
CREATE TEMPORARY TABLE tmp_sqft_for_non_home_based_jobs SELECT *
FROM Eugene_1980_baseyear.sqft_for_non_home_based_jobs;

CREATE INDEX tmp_jobs_by_year_year_grid_id_home_based_index on tmp_jobs_by_year (YEAR,GRID_ID,HOME_BASED);
Create index tmp_sqft_for_non_home_based_jobs_development_type_id_index on tmp_sqft_for_non_home_based_jobs (DEVELOPMENT_TYPE_ID);

  # 3.creat tmp_non_residential_vacancy_rates_by_devtype by job space
drop table if exists tmp_non_residential_vacancy_rates_by_devtype_by_job_space;
create table tmp_non_residential_vacancy_rates_by_devtype_by_job_space select grid.YEAR,grid.DEVELOPMENT_TYPE_ID, round(sum(COMMERCIAL_SQFT+INDUSTRIAL_SQFT+GOVERNMENTAL_SQFT)/SQFT) as TOTAL_JOB_SPACE,sum(JOBS) as JOBS, SQFT, 100*(1-sum(JOBS)/(sum(COMMERCIAL_SQFT+INDUSTRIAL_SQFT+GOVERNMENTAL_SQFT)/SQFT)) as VACANCY_RATE 
from gridcells_exported grid inner join tmp_jobs_by_year job on grid.YEAR = job.YEAR and grid.GRID_ID = job.GRID_ID 
inner join tmp_sqft_for_non_home_based_jobs sqft on grid.DEVELOPMENT_TYPE_ID = sqft.DEVELOPMENT_TYPE_ID
group by grid.YEAR, grid.DEVELOPMENT_TYPE_ID
order by grid.YEAR, grid.DEVELOPMENT_TYPE_ID;
