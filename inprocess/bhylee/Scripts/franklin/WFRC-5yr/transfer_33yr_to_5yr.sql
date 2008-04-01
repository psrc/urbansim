use WFRC_1997_output_5yr_2003;

# Copy output tables

drop table if exists accessibilities;
create table accessibilities 
     select * 
     from WFRC_1997_output_33yr_2030.accessibilities
     where year<=2003;
create index accessibilities_zone_id
     on accessibilities
     (zone_id);

drop table if exists gridcells_exported;
create table gridcells_exported
     select *
     from WFRC_1997_output_33yr_2030.gridcells_exported
     where year<=2003;
create index gridcells_exported_year_grid_id
     on gridcells_exported
     (year, grid_id);

drop table if exists jobs_exported;
create table jobs_exported
     select *
     from WFRC_1997_output_33yr_2030.jobs_exported
     where year<=2003;
create index jobs_exported_year_job_id
     on jobs_exported
     (year, job_id);

drop table if exists jobs_constants;
create table jobs_constants
     select *
     from WFRC_1997_output_33yr_2030.jobs_constants;
create index jobs_constants_job_id
     on jobs_constants
     (job_id);

drop table if exists households_exported;
create table households_exported
     select *
     from WFRC_1997_output_33yr_2030.households_exported
     where year<=2003;
create index households_exported_year_household_id
     on households_exported
     (year, household_id);

drop table if exists households_constants;
create table households_constants
     select *
     from WFRC_1997_output_33yr_2030.households_constants;
create index households_constants_household_id
     on households_constants
     (household_id);

# Copy indicator tables

drop table if exists households_per_year;
create table households_per_year 
     select * 
     from WFRC_1997_output_33yr_2030.households_per_year;

drop table if exists population_per_year;
create table population_per_year 
     select * 
     from WFRC_1997_output_33yr_2030.population_per_year;

drop table if exists job_spaces_per_year;
create table job_spaces_per_year 
     select * 
     from WFRC_1997_output_33yr_2030.job_spaces_per_year;

drop table if exists jobs_per_year;
create table jobs_per_year 
     select * 
     from WFRC_1997_output_33yr_2030.jobs_per_year;

drop table if exists nonresidential_sqft_per_year;
create table nonresidential_sqft_per_year 
     select * 
     from WFRC_1997_output_33yr_2030.nonresidential_sqft_per_year;

drop table if exists residential_units_per_year;
create table residential_units_per_year 
     select * 
     from WFRC_1997_output_33yr_2030.residential_units_per_year;

drop table if exists residential_vacancy_rate_per_year;
create table residential_vacancy_rate_per_year 
     select * 
     from WFRC_1997_output_33yr_2030.residential_vacancy_rate_per_year;

drop table if exists nonresidential_vacancy_rate_per_year;
create table nonresidential_vacancy_rate_per_year 
     select * 
     from WFRC_1997_output_33yr_2030.nonresidential_vacancy_rate_per_year;

drop table if exists avg_land_value_per_year;
create table avg_land_value_per_year 
     select * 
     from WFRC_1997_output_33yr_2030.avg_land_value_per_year;

drop table if exists avg_improvement_value_per_year;
create table avg_improvement_value_per_year 
     select * 
     from WFRC_1997_output_33yr_2030.avg_improvement_value_per_year;

# Copy GIS data tables

drop table if exists zones_transpose;
create table zones_transpose 
     select * 
     from WFRC_1997_output_33yr_2030.zones_transpose;

drop table if exists gridcells_transpose;
create table gridcells_transpose 
     select * 
     from WFRC_1997_output_33yr_2030.gridcells_transpose;
