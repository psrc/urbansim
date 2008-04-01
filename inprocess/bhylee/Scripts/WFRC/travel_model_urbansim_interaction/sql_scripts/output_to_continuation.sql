# This script creates two tables that are intended for use in displaying
# UrbanSim outputs using ArcGIS or other GIS software.  These tables are:
#
#    1. gridcells_$year1, and
#    2. zones_$year1.
#
# The first table contains data summarized at the grid cell leve, the
# second at the transportation analysis zone (aka "zone" or "TAZ) leve.
# Both employ abbreviated column names as described in:
#
#    "trondheim.cs.washington.edu\projects\urbansim4\modeler-work-specs\Short Names.xls".
#
# Each table includes three sets of columns, each suffixed with an abbreviation as follows:\
#
#    1. Data for year $base_year, suffixed with "_a";
#    2. Data for year $year1, suffices with "_z"; and
#    3. Computed absolute differences between the $base_year data and the $year1 data, with
#         the exception of development type, which is computed as null where the two years
#         contain the same development type in a particular gridcell or, if they are
#         different, then the development type of the gridcell in $year1.
#
# This version is intended for processing through a perl script:
#
#    Scripts\lmwang\travel_model_urbansim_interaction\tu_automate.pl
#
# In the perl script, the following parameters are dynamically replaced with appropriate values:
#
#    $output_db - the name of the previous run's output database
#    $scenario_db - the name of the continuation scenario database
#    $baseyear_db - the name of the database used as the parent, from
#         the continuation scenario's perspective (NOTE: this should
#         actually be the previous run's scenario database)
#    $year1 - the endyear for the subsequent run
#    $year0 - the endyear for the previous run
#    $baseyear_db_host - the server hosting the parent database

#use previous output year database
use $output_db;

# create "scenario_information" table
drop table if exists $scenario_db.scenario_information;
create table $scenario_db.scenario_information
     select * 
     from $baseyear_db.scenario_information;
  
update $scenario_db.scenario_information
set continuation=1, 
    end_year=$year1, 
    parent_database_url="jdbc:mysql://$baseyear_db_host/$baseyear_db";

#create "base_year" table
drop table if exists $scenario_db.base_year;
create table $scenario_db.base_year
     select * 
     from $baseyear_db.base_year;

update $scenario_db.base_year 
     set year=$year0;

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
    from $baseyear_db.gridcells as gc, 
      gridcells_exported as gc_e
    where gc.grid_id=gc_e.grid_id
          and gc_e.year=$year0;

drop table if exists $scenario_db.gridcells;
create table $scenario_db.gridcells
  select * 
  from new_grid;
drop table new_grid;

drop table if exists $scenario_db.households;
create table $scenario_db.households
    select hh_e.household_id as HOUSEHOLD_ID,
           hh_e.grid_id as GRID_ID,
           hh_c.persons as PERSONS,
           hh_c.workers as WORKERS,
           hh_c.age_of_head as AGE_OF_HEAD,
           hh_c.INCOME as INCOME,
           hh_c.CHILDREN as CHILDREN,
           hh_c.RACE_ID as RACE_ID,
           hh_c.cars as CARS           
    from households_exported as hh_e
      left join households_constants as hh_c 
        on hh_e.household_id=hh_c.household_id
    where hh_e.year=$year0;

drop table if exists $scenario_db.jobs;
create table $scenario_db.jobs
    select j_e.job_id as JOB_ID,
           j_e.grid_id as GRID_ID,
        j_e.home_based as HOME_BASED,
        j_c.SECTOR_ID as SECTOR_ID
    from jobs_exported as j_e 
      left join jobs_constants as j_c 
        on j_e.job_id=j_c.job_id
    where j_e.year=$year0;
