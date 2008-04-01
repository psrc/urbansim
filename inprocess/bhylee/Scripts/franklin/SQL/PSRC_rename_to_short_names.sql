# GRIDCELLS table
create table gridcells_short
select
  GRID_ID as GRIDID,
  COMMERCIAL_SQFT as SF_C,
  DEVELOPMENT_TYPE_ID as DT_ID,
  DISTANCE_TO_ARTERIAL as D_ART,         
  DISTANCE_TO_HIGHWAY as D_HWY,         
  GOVERNMENTAL_SQFT as SF_G,         
  INDUSTRIAL_SQFT as SF_I,         
  COMMERCIAL_IMPROVEMENT_VALUE as IV_C,
  INDUSTRIAL_IMPROVEMENT_VALUE as IV_I,
  GOVERNMENTAL_IMPROVEMENT_VALUE as IV_G,
  NONRESIDENTIAL_LAND_VALUE as LV_NR,
  RESIDENTIAL_IMPROVEMENT_VALUE as IV_R,    
  RESIDENTIAL_LAND_VALUE as LV_R,    
  RESIDENTIAL_UNITS as DUR,    
  RELATIVE_X as REL_X,    
  RELATIVE_Y as REL_Y,    
  YEAR_BUILT as YRBLT,    
  PLAN_TYPE_ID as PLT_ID,    
  PERCENT_WATER as PWATER,    
  PERCENT_WETLAND as PWETLA,    
  PERCENT_STREAM_BUFFER as PSTBUF,    
  PERCENT_FLOODPLAIN as PFL,    
  PERCENT_SLOPE as PSLOPE,    
  PERCENT_OPEN_SPACE as POPEN,    
  PERCENT_PUBLIC_SPACE as PPUB,    
  PERCENT_ROADS as PROAD,    
  IS_OUTSIDE_URBAN_GROWTH_BOUNDARY as O_UGB,
  IS_INSIDE_NATIONAL_FOREST as IN_NF,
  IS_INSIDE_TRIBAL_LAND as IN_TL,
  IS_INSIDE_MILITARY_BASE as IN_MB,
  ZONE_ID as TAZ_ID,
  CITY_ID as CI_ID,
  COUNTY_ID as CO_ID,
  FRACTION_RESIDENTIAL_LAND as FL_R 
from gridcells;

# GRIDCELLS_EXPORTED table
select
  YEAR as YEAR,
  GRID_ID as GRIDID,
  RESIDENTIAL_IMPROVEMENT_VALUE as IV_R,
  RESIDENTIAL_LAND_VALUE as LV_R,
  COMMERCIAL_SQFT as SF_C,
  INDUSTRIAL_SQFT as SF_I,
  GOVERNMENTAL_SQFT as SF_G, 
  YEAR_BUILT as YRBLT,
  RESIDENTIAL_UNITS as DUR,    
  DEVELOPMENT_TYPE_ID as DT_ID,
  COMMERCIAL_IMPROVEMENT_VALUE as IV_C,
  INDUSTRIAL_IMPROVEMENT_VALUE as IV_I,
  GOVERNMENTAL_IMPROVEMENT_VALUE as IV_G,
  NONRESIDENTIAL_LAND_VALUE as LV_NR,
  FRACTION_RESIDENTIAL_LAND as FL_R 
into outfile "/projects/urbansim/third-party/mysql/out/gridcells_exported_short.csv"
fields terminated by ',' optionally enclosed by '"'
lines terminated by "\n"
from GRIDCELLS_EXPORTED;

# ACCESSIBILITIES table
select
  YEAR as YEAR,
  ZONE_ID as TAZ_ID,
  HOME_ACCESS_TO_EMPLOYMENT_0 as HAE0,
  HOME_ACCESS_TO_EMPLOYMENT_1 as HAE1,
  HOME_ACCESS_TO_EMPLOYMENT_2 as HAE2,
  HOME_ACCESS_TO_EMPLOYMENT_3 as HAE3,
  HOME_ACCESS_TO_POPULATION_0 as HAP0,
  HOME_ACCESS_TO_POPULATION_1 as HAP1,
  HOME_ACCESS_TO_POPULATION_2 as HAP2,
  HOME_ACCESS_TO_POPULATION_3 as HAP3,
  WORK_ACCESS_TO_EMPLOYMENT_0 as WAE0,
  WORK_ACCESS_TO_EMPLOYMENT_1 as WAE1,
  WORK_ACCESS_TO_EMPLOYMENT_2 as WAE2,
  WORK_ACCESS_TO_EMPLOYMENT_3 as WAE3,
  WORK_ACCESS_TO_POPULATION_0 as WAP0,
  WORK_ACCESS_TO_POPULATION_1 as WAP1,
  WORK_ACCESS_TO_POPULATION_2 as WAP2,
  WORK_ACCESS_TO_POPULATION_3 as WAP3
into outfile "/projects/urbansim/third-party/mysql/out/accessibilities_short.csv"
fields terminated by ',' optionally enclosed by '"'
lines terminated by "\n"
from ACCESSIBILITIES;

# HOUSEHOLDS_CONSTANTS table
select
  HOUSEHOLD_ID as HH_ID,
  PERSONS as PERSON,
  WORKERS as WRKRS,
  AGE_OF_HEAD as AGE_HE,
  INCOME as INC,
  CHILDREN as CHILD,
  RACE_ID as RACEID,
  CARS as CARS
into outfile "/projects/urbansim/third-party/mysql/out/households_constants_short.csv"
fields terminated by ',' optionally enclosed by '"'
lines terminated by "\n"
from HOUSEHOLDS_CONSTANTS;

# HOUSEHOLDS_EXPORTED table
select
  YEAR as YEAR,
  HOUSEHOLD_ID as HH_ID,
  GRID_ID as GRIDID,
  ZONE_ID as TAZ_ID
into outfile "/projects/urbansim/third-party/mysql/out/out/households_exported_short.csv"
fields terminated by ',' optionally enclosed by '"'
lines terminated by "\n"
from HOUSEHOLDS_EXPORTED;

# JOBS_CONSTANTS table
select
  JOB_ID as JOB_ID,
  SECTOR_ID as SECTID
into outfile "/projects/urbansim/third-party/mysql/out/out/jobs_constants_short.csv"
fields terminated by ',' optionally enclosed by '"'
lines terminated by "\n"
from JOBS_CONSTANTS;

# JOBS_EXPORTED table
select
  YEAR as YEAR,
  JOB_ID as JOB_ID,
  GRID_ID as GRIDID,
  HOME_BASED as HB,
  ZONE_ID as TAZ_ID
into outfile "/projects/urbansim/third-party/mysql/out/out/jobs_exported_short.csv"
fields terminated by ',' optionally enclosed by '"'
lines terminated by "\n"
from JOBS_EXPORTED;



