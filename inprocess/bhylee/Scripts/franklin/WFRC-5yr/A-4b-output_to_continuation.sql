# Note: Be sure to type "use ..." to switch to your output database before running this.

use WFRC_1997_output_5yr_2003;

# create "scenario_information" table
drop table if exists WFRC_2000_scenario_5yr.scenario_information;
create table WFRC_2000_scenario_5yr.scenario_information
     select * 
     from WFRC_1997_baseyear.scenario_information;
  
update WFRC_2000_scenario_5yr.scenario_information
set continuation=1, 
    end_year=2003, 
    parent_database_url="jdbc:mysql://trondheim.cs.washington.edu/WFRC_1997_baseyear";

#create "base_year" table
drop table if exists WFRC_2000_scenario_5yr.base_year;
create table WFRC_2000_scenario_5yr.base_year
     select * 
     from WFRC_1997_baseyear.base_year;

update WFRC_2000_scenario_5yr.base_year 
     set year=2000;

# Copy the year=2000 rows from the output database into the continuation scenario database
create temporary table new_grid
   select gc.grid_id as GRID_ID,
          gc_e.development_type_id as DEVELOPMENT_TYPE_ID,
          gc.city_id as CITY_ID,
          gc.county_id as COUNTY_ID,
          gc.distance_to_arterial as DISTANCE_TO_ARTERIAL,
          gc.distance_to_highway as DISTANCE_TO_HIGHWAY,
          gc_e.commercial_sqft as COMMERCIAL_SQFT,
          gc_e.governmental_sqft as GOVERNMENTAL_SQFT,
          gc_e.industrial_sqft as INDUSTRIAL_SQFT,
          gc_e.commercial_improvement_value as COMMERCIAL_IMPROVEMENT_VALUE,
          gc_e.industrial_improvement_value as INDUSTRIAL_IMPROVEMENT_VALUE,
          gc_e.governmental_improvement_value as GOVERNMENTAL_IMPROVEMENT_VALUE,
          gc_e.nonresidential_land_value as NONRESIDENTIAL_LAND_VALUE,
          gc_e.residential_improvement_value as RESIDENTIAL_IMPROVEMENT_VALUE,
          gc_e.residential_land_value as RESIDENTIAL_LAND_VALUE,
          gc_e.residential_units as RESIDENTIAL_UNITS,
          gc.relative_x as RELATIVE_X,
          gc.relative_y as RELATIVE_Y,
          gc.year_built as YEAR_BUILT,
          gc.plan_type_id as PLAN_TYPE_ID,
          gc.percent_floodplain as PERCENT_FLOODPLAIN,
          gc.percent_open_space as PERCENT_OPEN_SPACE,
          gc.percent_public_space as PERCENT_PUBLIC_SPACE,
          gc.percent_stream_buffer as PERCENT_STREAM_BUFFER,
          gc.percent_roads as PERCENT_ROADS,
          gc.percent_slope as PERCENT_SLOPE,
          gc.percent_WATER as PERCENT_WATER,
          gc.percent_wetland as PERCENT_WETLAND,
          gc.is_outside_urban_growth_boundary as IS_OUTSIDE_URBAN_GROWTH_BOUNDARY,
          gc.zone_id as ZONE_ID,
          gc_e.fraction_residential_land as FRACTION_RESIDENTIAL_LAND
    from WFRC_1997_baseyear.gridcells as gc, 
      gridcells_exported as gc_e
    where gc.grid_id=gc_e.grid_id
          and gc_e.year=2000;

drop table if exists WFRC_2000_scenario_5yr.gridcells;
create table WFRC_2000_scenario_5yr.gridcells
  select * 
  from new_grid;
drop table new_grid;

drop table if exists WFRC_2000_scenario_5yr.households;
create table WFRC_2000_scenario_5yr.households
    select hh_e.household_id as HOUSEHOLD_ID,
           hh_e.grid_id as GRID_ID,
           hh_c.persons as PERSONS,
           hh_c.workers as WORKERS,
           hh_c.age_of_head as AGE_OF_HEAD,
           hh_c.INCOME as INCOME,
           hh_c.CHILDREN as CHILDREN,
           hh_c.RACE_ID as RACE_ID,
           hh_c.cars as CARS           
    from households_constants as hh_c, 
      households_exported as hh_e
    where hh_c.household_id=hh_e.household_id 
           and hh_e.year=2000;

drop table if exists WFRC_2000_scenario_5yr.jobs;
create table WFRC_2000_scenario_5yr.jobs
    select j_e.job_id as JOB_ID,
           j_e.grid_id as GRID_ID,
        j_e.home_based as HOME_BASED,
        j_c.SECTOR_ID as SECTOR_ID
    from jobs_exported as j_e, 
      jobs_constants as j_c 
    where j_e.job_id=j_c.job_id
           and j_e.year=2000;
