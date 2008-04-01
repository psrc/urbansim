# See bug # 92
# prepare temp table and indices for crystal reports

# first add the base year data into the output database for convinence of comparation

insert into GridCellsChanges select 1980,GRID_ID,RESIDENTIAL_IMPROVEMENT_VALUE,RESIDENTIAL_LAND_VALUE,COMMERCIAL_SQFT,INDUSTRIAL_SQFT,GOVERNMENTAL_SQFT,YEAR_BUILT,RESIDENTIAL_UNITS,DEVELOPMENT_TYPE_ID,COMMERCIAL_IMPROVEMENT_VALUE,INDUSTRIAL_IMPROVEMENT_VALUE,GOVERNMENTAL_IMPROVEMENT_VALUE,NONRESIDENTIAL_LAND_VALUE,FRACTION_RESIDENTIAL_LAND from Eugene1980_baseyear.GridCells;

insert into JobsChanges select
1980,JOB_ID,GRID_ID,HOME_BASED from Eugene1980_baseyear.Jobs;

insert into HouseholdsChanges select
1980,HOUSEHOLD_ID,GRID_ID from Eugene1980_baseyear.Households;

#create index for output tables
CREATE INDEX HouseholdsChanges_year_household_id_grid_id_index on HouseholdsChanges (YEAR, HOUSEHOLD_ID,GRID_ID);
CREATE INDEX HouseholdsConstants_household_id_index on HouseholdsConstants (HOUSEHOLD_ID);
CREATE INDEX JobsChanges_year_job_id_grid_id_index on JobsChanges (YEAR, JOB_ID, GRID_ID);
CREATE INDEX JobsConstants_job_id_index on JobsConstants (JOB_ID);
CREATE INDEX GridCellsChanges_year_grid_id_index on GridCellsChanges (YEAR, GRID_ID);


#create temporary table and create indices 
DROP TABLE IF EXISTS temp_HouseholdsByYear;

CREATE TABLE temp_HouseholdsByYear SELECT YEAR,GRID_ID,COUNT(HouseholdsChanges.HOUSEHOLD_ID) AS HOUSEHOLDS,
SUM(HouseholdsConstants.PERSONS) AS POPULATION
FROM HouseholdsChanges
   LEFT JOIN HouseholdsConstants
   ON HouseholdsChanges.HOUSEHOLD_ID=HouseholdsConstants.HOUSEHOLD_ID
GROUP BY GRID_ID,YEAR;

DROP TABLE IF EXISTS temp_JobsByYear;
CREATE TABLE temp_JobsByYear SELECT YEAR,GRID_ID,COUNT(JobsChanges.JOB_ID) AS JOBS, HOME_BASED as HOME_BASED
FROM JobsChanges
WHERE HOME_BASED=0   
GROUP BY GRID_ID,YEAR;

##LEFT JOIN JobsConstants
##  ON JobsChanges.JOB_ID=JobsConstants.JOB_ID

DROP TABLE IF EXISTS temp_SqftForNonHomeBasedJobs;
CREATE TABLE temp_SqftForNonHomeBasedJobs SELECT *
FROM Eugene1980_baseyear.SqftForNonHomeBasedJobs;

CREATE INDEX temp_HouseholdsByYear_year_grid_id_index on temp_HouseholdsByYear (YEAR,GRID_ID);
CREATE INDEX temp_JobsByYear_year_grid_id_home_based_index on temp_JobsByYear (YEAR,GRID_ID,HOME_BASED);

Create index temp_SqftForNonHomeBasedJobs_development_type_id_index on temp_SqftForNonHomeBasedJobs (DEVELOPMENT_TYPE_ID);


# testing tables;


#SELECT GridCellsChanges.YEAR,SUM(temp_HouseholdsByYear.POPULATION) AS POPULATION,
#SUM(temp_HouseholdsByYear.HOUSEHOLDS) AS HOUSEHOLDs,
#SUM(GridCellsChanges.RESIDENTIAL_UNITS) AS RESIDENTIAL_UNITS
#FROM GridCellsChanges 
#  LEFT JOIN temp_HouseholdsByYear
#   ON temp_HouseholdsByYear.YEAR=GridCellsChanges.YEAR 
#   AND temp_HouseholdsByYear.GRID_ID=GridCellsChanges.GRID_ID 
#GROUP BY YEAR
#ORDER BY YEAR;

#SELECT GridCellsChanges.YEAR,SUM(temp_JobsByYear.JOBS) AS JOBS,
#SUM(GridCellsChanges.COMMERCIAL_SQFT+GridCellsChanges.INDUSTRIAL_SQFT+GridCellsChanges.GOVERNMENTAL_SQFT) AS SQFT
#FROM GridCellsChanges
#  LEFT JOIN temp_JobsByYear
#   ON temp_JobsByYear.YEAR=GridCellsChanges.YEAR 
#   AND temp_JobsByYear.GRID_ID=GridCellsChanges.GRID_ID 
#  LEFT JOIN temp_SqftForNonHomeBasedJobs
#   ON GridCellsChanges.DEVELOPMENT_TYPE_ID=temp_SqftForNonHomeBasedJobs.DEVELOPMENT_TYPE_ID
#WHERE HOME_BASED=0
#GROUP BY YEAR
#ORDER BY YEAR;
