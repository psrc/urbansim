# This sql script creates a basic set of UrbanSim indicators 
# as tables in the output database.
#
# This version is intended for processing through a perl script:
#
#    Scripts\lmwang\travel_model_urbansim_interaction\tu_automate.pl
#
# In the perl script, the following parameters are dynamically replaced with appropriate values:
#
#    $output_db - the name of the database containing the UrbanSim output tables;
#    $baseyear_db - the name of the database containing the UrbanSim baseyear tables.


# This sql script creates basic UrbanSim indicators 
# as tables in the output database

#use WFRC_1997_output_5yr_2003;
use $output_db;

# Households per year

drop table if exists households_per_year;
create table households_per_year
     select YEAR, count(*) as HOUSEHOLDS
     from households_exported
     group by YEAR;
     
# Population per year

drop table if exists population_per_year;
create table population_per_year
     select a.YEAR as YEAR, 
          sum(b.PERSONS) as POPULATION
     from households_exported a 
          inner join households_constants b 
               on a.HOUSEHOLD_ID = b.HOUSEHOLD_ID 
     group by a.YEAR;

# Job spaces per year

create temporary table tmp_table1(YEAR int, JOB_SPACES int);
create temporary table tmp_table2(YEAR int, JOB_SPACES int);

insert into tmp_table1(YEAR, JOB_SPACES)
     select a.YEAR as YEAR, 
          round(sum(RESIDENTIAL_UNITS * b.RATIO)) as JOB_SPACES
     from gridcells_exported a, $baseyear_db.residential_units_for_home_based_jobs b
     where a.DEVELOPMENT_TYPE_ID=b.DEVELOPMENT_TYPE_ID
     group by a.YEAR;

insert into tmp_table2(YEAR, JOB_SPACES)
     select a.YEAR as YEAR, 
          round(sum((a.COMMERCIAL_SQFT+a.INDUSTRIAL_SQFT+a.GOVERNMENTAL_SQFT)/b.SQFT)) as JOB_SPACES
     from gridcells_exported a, 
          $baseyear_db.sqft_for_non_home_based_jobs b
     where a.DEVELOPMENT_TYPE_ID=b.DEVELOPMENT_TYPE_ID
     group by a.YEAR;

drop table if exists job_spaces_per_year;
create table job_spaces_per_year
     select a.YEAR as YEAR, 
          (a.JOB_SPACES+b.JOB_SPACES) as JOB_SPACES
     from tmp_table1 as a, 
          tmp_table2 as b
     where a.YEAR=b.YEAR;

drop table tmp_table1;
drop table tmp_table2;

# Jobs per year

drop table if exists jobs_per_year;
create table jobs_per_year
     select YEAR, 
          count(*) as JOBS
     from jobs_exported
     group by YEAR;

# Jobs of Sector 3+ per year

create table jobs_3plus_per_year 
     select year, 
          sum(total_employment) 
     from $baseyear_db.annual_employment_control_totals 
     where sector_id>=3 
     group by year;

# Non-residential square feet per year

drop table if exists nonresidential_sqft_per_year;
create table nonresidential_sqft_per_year
     select YEAR, 
          sum(COMMERCIAL_SQFT+INDUSTRIAL_SQFT+GOVERNMENTAL_SQFT) as NONRESIDENTIAL_SQFT
     from gridcells_exported
     group by YEAR;

# Residential units per year

drop table if exists residential_units_per_year;
create table residential_units_per_year
     select YEAR, 
          sum(RESIDENTIAL_UNITS) as RESIDENTIAL_UNITS
     from gridcells_exported
     group by YEAR;

# Residential vacancy rate per year

create temporary table tmp_table1(YEAR int, GRID_ID int, HOUSEHOLDS int);

insert into tmp_table1(YEAR, GRID_ID, HOUSEHOLDS)
     select YEAR,
          GRID_ID,
          count(HOUSEHOLD_ID) as HOUSEHOLDS
     from households_exported
     group by GRID_ID,
          YEAR;

create index tmp_table1_year_grid_id_index on tmp_table1 (YEAR,GRID_ID);

drop table if exists residential_vacancy_rate_per_year;
create table residential_vacancy_rate_per_year
     select a.YEAR as YEAR,
          round(100*(1-SUM(HOUSEHOLDS)/sum(RESIDENTIAL_UNITS)),2) as RESIDENTIAL_VACANCY_RATE
     from gridcells_exported a 
          left outer join tmp_table1 b 
          on a.YEAR=b.YEAR 
               and a.GRID_ID=b.GRID_ID
     group by a.YEAR
     order by a.YEAR;

drop table tmp_table1;

# Non-residential vacancy rate per year

create temporary table tmp_table1(YEAR int, GRID_ID int, JOBS int);
create temporary table tmp_table2(YEAR int, GRID_ID int, TOTAL_SQFT int, DEVELOPMENT_TYPE_ID int, SQFT int);

insert into tmp_table1(YEAR, GRID_ID, JOBS)
     select YEAR,
          GRID_ID,
          count(JOB_ID) as JOBS
     from jobs_exported
     where HOME_BASED=0   
     group by GRID_ID,
          YEAR;

insert into tmp_table2(YEAR, GRID_ID, TOTAL_SQFT, DEVELOPMENT_TYPE_ID, SQFT)
     select a.YEAR, 
          a.GRID_ID, 
          (a.COMMERCIAL_SQFT+a.INDUSTRIAL_SQFT+a.GOVERNMENTAL_SQFT) as TOTAL_SQFT,
          a.DEVELOPMENT_TYPE_ID, 
          b.SQFT
     from gridcells_exported a, 
          $baseyear_db.sqft_for_non_home_based_jobs b 
     where a.DEVELOPMENT_TYPE_ID=b.DEVELOPMENT_TYPE_ID;

create index tmp_table1_year_grid_id_index 
     on tmp_table1 (YEAR,GRID_ID);
create index tmp_table2_year_grid_id_dev_type_index 
     on tmp_table2 (YEAR,GRID_ID,DEVELOPMENT_TYPE_ID);

drop table if exists nonresidential_vacancy_rate_per_year;
create table nonresidential_vacancy_rate_per_year
     select a.YEAR as YEAR,
          round(100*(1-sum(b.JOBS*a.SQFT)/sum(a.TOTAL_SQFT)),2) as NONRESIDENTIAL_VACANCY_RATE 
     from tmp_table2 a 
          left outer join tmp_table1 b 
               on a.YEAR=b.YEAR 
                    and a.GRID_ID=b.GRID_ID 
     group by a.YEAR
     order by a.YEAR;

drop table tmp_table1;
drop table tmp_table2;

# Land value per year

drop table if exists avg_land_value_per_year;
create table avg_land_value_per_year
     select YEAR, 
          avg(RESIDENTIAL_LAND_VALUE) as RESIDENTIAL_LAND_VALUE,
          avg(NONRESIDENTIAL_LAND_VALUE) as NONRESIDENTIAL_LAND_VALUE,
          avg(RESIDENTIAL_LAND_VALUE) + avg(NONRESIDENTIAL_LAND_VALUE) as TOTAL_LAND_VALUE
     from gridcells_exported
     group by YEAR;

# Improvement value per year

drop table if exists avg_improvement_value_per_year;
create table avg_improvement_value_per_year
     select YEAR, 
          avg(RESIDENTIAL_IMPROVEMENT_VALUE) as RESIDENTIAL_IMPROVEMENT_VALUE,
          avg(COMMERCIAL_IMPROVEMENT_VALUE) as COMMERCIAL_IMPROVEMENT_VALUE,
          avg(INDUSTRIAL_IMPROVEMENT_VALUE) as INDUSTRIAL_IMPROVEMENT_VALUE,
          avg(GOVERNMENTAL_IMPROVEMENT_VALUE) as GOVERNMENTAL_IMPROVEMENT_VALUE,
          avg(COMMERCIAL_IMPROVEMENT_VALUE) 
               + avg(INDUSTRIAL_IMPROVEMENT_VALUE) 
               + avg(GOVERNMENTAL_IMPROVEMENT_VALUE) as NONRESIDENTIAL_IMPROVEMENT_VALUE,
          avg(RESIDENTIAL_IMPROVEMENT_VALUE) 
               + avg(COMMERCIAL_IMPROVEMENT_VALUE) 
               + avg(INDUSTRIAL_IMPROVEMENT_VALUE) 
               + avg(GOVERNMENTAL_IMPROVEMENT_VALUE) as TOTAL_IMPROVEMENT_VALUE
     from gridcells_exported
     group by YEAR;


