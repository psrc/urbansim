create index grid on gridcells_exported(grid_id);
create index hh on households_exported(household_id);
create index hh on households_constants(household_id);
create index job on jobs_exported(job_id);
create index job on jobs_constants(job_id);


create temporary table new_grid
   select gridcells.grid_id as GRID_ID,
          gridcells_exported.development_type_id as DEVELOPMENT_TYPE_ID,
          gridcells.city_id as CITY_ID,
          gridcells.county_id as COUNTY_ID,
          gridcells.distance_to_arterial as DISTANCE_TO_ARTERIAL,
          gridcells.distance_to_highway as DISTANCE_TO_HIGHWay,
	  gridcells_exported.commercial_sqft as COMMERCIAL_SQFT,
	  gridcells_exported.governmental_sqft as GOVERNMENTAL_SQFT,
	  gridcells_exported.industrial_sqft as INDUSTRIAL_SQFT,
	  gridcells_exported.commercial_improvement_value as COMMERCIAL_IMPROVEMENT_VALUE,
	  gridcells_exported.industrial_improvement_value as INDUSTRIAL_IMPROVEMENT_VALUE,
 	  gridcells_exported.governmental_improvement_value as GOVERNMENTAL_IMPROVEMENT_VALUE,
	  gridcells_exported.nonresidential_land_value as NONRESIDENTIAL_LAND_VALUE,
	  gridcells_exported.residential_improvement_value as RESIDENTIAL_IMPROVEMENT_VALUE,
	  gridcells_exported.residential_land_value as RESIDENTIAL_LAND_VALUE,
	  gridcells_exported.residential_units as RESIDENTIAL_UNITS,
	  gridcells.relative_x as RELATIVE_X,
	  gridcells.relative_y as RELATIVE_Y,
	  gridcells.year_built as YEAR_BUILT,
	  gridcells.plan_type_id as PLAN_TYPE_ID,
	  gridcells.percent_floodplain as PERCENT_FLOODPLAIN,
	  gridcells.percent_open_space as PERCENT_OPEN_SPACE,
	  gridcells.percent_public_space as PERCENT_PUBLIC_SPACE,
	  gridcells.percent_stream_buffer as PERCENT_STREAM_BUFFER,
	  gridcells.percent_roads as PERCENT_ROADS,
	  gridcells.percent_slope as PERCENT_SLOPE,
	  gridcells.percent_WATER as PERCENT_WATER,
	  gridcells.percent_wetland as PERCENT_WETLAND,
	  gridcells.is_outside_urban_growth_boundary as IS_OUTSIDE_URBAN_GROWTH_BOUNDARY,
	  gridcells.zone_id as ZONE_ID,
          gridcells_exported.fraction_residential_land as FRACTION_RESIDENTIAL_LAND
    from gridcells, gridcells_exported where 
    gridcells.grid_id=gridcells_exported.grid_id and gridcells_exported.year=2003;

drop table gridcells;
create table gridcells select * from new_grid;
drop table new_grid;


create table households
    select households_exported.household_id as HOUSEHOLD_ID,
           households_exported.grid_id as GRID_ID,
           households_constants.persons as PERSONS,
           households_constants.workers as WORKERS,
           households_constants.age_of_head as AGE_OF_HEAD,
           households_constants.INCOME as INCOME,
           households_constants.CHILDREN as CHILDREN,
           households_constants.RACE_ID as RACE_ID,
           households_constants.cars as CARS           
    from households_constants, households_exported where
    households_constants.household_id=households_exported.household_id and households_exported.year=2003;

create table jobs
    select jobs_exported.job_id as JOB_ID,
           jobs_exported.grid_id as GRID_ID,
	   jobs_exported.home_based as HOME_BASED,
	   jobs_constants.SECTOR_ID as SECTOR_ID
    from jobs_exported, jobs_constants where
    jobs_exported.job_id=jobs_constants.job_id and jobs_exported.year=2003;


create index hh on households(household_id);
create index grid on households(grid_id);
create index grid on jobs(grid_id);
create index job on jobs(job_id);
create index grid on gridcells(grid_id);

