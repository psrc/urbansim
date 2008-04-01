# This script formats UrbanSim output data for use in the WFRC travel model by creating
# two tables.  These tables are:
#
#    1. SEdata, and
#    2. HHdistrib_joint_inclohi.
#
# This version is intended for processing through a perl script:
#
#    Scripts\lmwang\travel_model_urbansim_interaction\tu_automate.pl
#
# In the perl script, the following parameters are dynamically replaced with appropriate values:
#
#    $output_db - the name of the database containing the UrbanSim output tables; and
#    $year1 - the four-digit year of the end year of the simulation or some other projected year.

# select the output database

use $output_db;

# Select the endyear and combine "exported" and "constants" jobs and 
# households data for use in creating both of the output tables

# Select out the endyear ($year1) data

drop table if exists households_exported_$year1;
create table households_exported_$year1
  select * 
  from households_exported 
  where year=$year1;
create index hh 
  on households_exported_$year1(household_id);

drop table if exists jobs_exported_$year1;
create table jobs_exported_$year1
  select * 
  from jobs_exported 
  where year=$year1;
create index jobs 
  on jobs_exported_$year1(job_id);

drop table if exists gridcells_exported_$year1;
create table gridcells_exported_$year1
  select * 
  from gridcells_exported 
  where year=$year1;
create index grid 
  on gridcells_exported_$year1(grid_id);

# Create a table that merges "constants" and "exported" data on households

drop table if exists households_all_$year1;
create TABLE households_all_$year1
  select households_exported_$year1.grid_id, 
    households_exported_$year1.zone_id, 
    households_constants.*
  from households_exported_$year1, 
    households_constants
  where households_constants.household_id=households_exported_$year1.household_id;
create index households_all_$year1_household_id_zone_id 
  on households_all_$year1 (household_id, zone_id);
create index households_all_$year1_zone_id 
  on households_all_$year1 (zone_id);

######################################################################
#  THIS PART OF THE SCRIPT IS USED TO CREATE THE "SEdata" TABLE  #
######################################################################

# Create indicators for household size groups.
# For 5-person households, allocate between HH5 and HH6-plus
# by the specified portions

alter table households_all_$year1 add column(HH1 int(1)),
     add column(HH2 int(1)),
     add column(HH3 int(1)),
     add column(HH4 int(1)),
     add column(HH5 double),
     add column(HH6P double),
     add column(pop double),
     change column persons persons decimal(5,2);

update households_all_$year1 set HH1=1 where persons=1;
update households_all_$year1 set HH2=1 where persons=2;
update households_all_$year1 set HH3=1 where persons=3;
update households_all_$year1 set HH4=1 where persons=4;
update households_all_$year1 set HH5=.432 where persons=5;
update households_all_$year1 set HH6P=.568 where persons=5;

# Set the top household size category to the representative "average" size for that category

update households_all_$year1 set persons=5.8 where persons=5;

# Aggregate persons and households by zone

Create TEMPORARY TABLE tmp_hhstat1
  select zone_id, 
     count(household_id) as TOTHH, 
     sum(HH1) as HH1, 
     sum(HH2) as HH2, 
     sum(HH3) as HH3, 
     sum(HH4) as HH4, 
     Sum(HH5) as HH5, 
     sum(HH6P) as HH6P, 
     sum(persons) as TOTPOP
  from households_all_$year1 
  group by zone_id;
create index tmp_hhstat1_zone_id
  on tmp_hhstat1 (zone_id);

# Create a table that merges "constants" and "exported" data on gridcells

drop table if exists tmp_gridcell_zones;
create temporary table tmp_gridcell_zones
  select grid_id, 
    zone_id
  from WFRC_1997_baseyear.gridcells;  
create index tmp_gridcell_zones_zone_id
     on tmp_gridcell_zones (zone_id);

drop table if exists tmp_gridcells_all;
Create TEMPORARY TABLE tmp_gridcells_all
  select tmp_gridcell_zones.zone_id as zone_id, 
    gridcells_exported_$year1.residential_units as residential_units
  from gridcells_exported_$year1 inner join  
    tmp_gridcell_zones
  on gridcells_exported_$year1.grid_id=tmp_gridcell_zones.grid_id;
create index tmp_gridcells_all_zone_id
  on tmp_gridcells_all (zone_id);

drop table if exists tmp_gcstat;  
create temporary table tmp_gcstat
     select zone_id as zone_id,
          sum(residential_units) as TOTDWL
     from tmp_gridcells_all
     group by zone_id;
create index tmp_gcstat_zone_id
     on tmp_gcstat (zone_id);
  
# Create a table that merges "constants" and "exported" data on jobs

drop table if exists tmp_jobs_all;
Create TEMPORARY TABLE tmp_jobs_all
  select jobs_exported_$year1.zone_id, 
    jobs_constants.*
  from jobs_exported_$year1, 
    jobs_constants
  where jobs_constants.job_id=jobs_exported_$year1.job_id;
create index tmp_jobs_all_job_id_zone_id
  on tmp_jobs_all (job_id, zone_id);

# Create sector-specific dummy variables

alter table tmp_jobs_all add column(TOT int(1)),
     add column(RET int(1)),
     add column(IND int(1)),
     add column(OTH int(1));

# Populate sector-specific dummy variables

update tmp_jobs_all set TOT=1 where sector_id>2;
                                               
update tmp_jobs_all set RET=1 where sector_id=6 
                                 or sector_id=7 
                                 or sector_id=8;

update tmp_jobs_all set IND=1 where sector_id=3 
                                 or sector_id=4;
                                               
update tmp_jobs_all set OTH=1 where sector_id=5 
                                 or sector_id=9 
                                 or sector_id=10
                                 or sector_id=11
                                 or sector_id=12
                                 or sector_id=13
                                 or sector_id=14;

# Aggregate sector counts to the zone level

drop table if exists tmp_jobstat;
create TEMPORARY TABLE tmp_jobstat
  select zone_id, 
    sum(TOT) as TOTEMP, 
    sum(RET) as RETEMP, 
    sum(IND) as INDEMP,
    sum(OTH) as OTHEMP
  from tmp_jobs_all group by zone_id;
create index tmp_jobstat_zone_id
  on tmp_jobstat (zone_id);

# Aggregate for average household income and size

drop table if exists tmp_hhstat2;
Create TEMPORARY TABLE tmp_hhstat2
  select zone_id, 
    avg(income) as AVGINCOME, 
    avg(persons) as HHSIZE
  from households_all_$year1
  group by zone_id;
create index tmp_hhstat2_zone_id
  on tmp_hhstat2 (zone_id);

# get list of zones from baseyear database

drop temporary table if exists tmp_zones_list;
create temporary table tmp_zones_list
     select zone_id
     from WFRC_1997_baseyear.zones;    
create index tmp_zones_list_zone_id
     on tmp_zones_list (zone_id);

# Combine zones list, hhstat1, gcstat, jobstat, and hhstat2

drop table if exists SEdata;
Create table SEdata(Z int, TOTHH int, 
     HH1 decimal(5,1), HH2 decimal(5,1), HH3 decimal(5,1), HH4 decimal(5,1), HH5 decimal(5,1), HH6P decimal(5,1),
     TOTPOP int, TOTDWL int, TOTEMP int, RETEMP int, INDEMP int, OTHEMP int, AVGINCOME int, HHSIZE decimal(5,2));

Insert into SEdata
     select zn.zone_id as Z,
          hh1.TOTHH as TOTHH,
          hh1.HH1 as HH1,
          hh1.HH2 as HH2,
          hh1.HH3 as HH3,
          hh1.HH4 as HH4,
          hh1.HH5 as HH5,
          hh1.HH6P as HH6P,
          hh1.TOTPOP as TOTPOP,
          gc.TOTDWL as TOTDWL,
          j.TOTEMP as TOTEMP,
          j.RETEMP as RETEMP,
          j.INDEMP as INDEMP,
          j.OTHEMP as OTHEMP,
          hh2.AVGINCOME as AVGINCOME,
          hh2.HHSIZE as HHSIZE
     from tmp_zones_list as zn
          left outer join tmp_gcstat as gc
               on zn.zone_id=gc.zone_id
          left outer join tmp_hhstat1 as hh1
               on zn.zone_id=hh1.zone_id
          left outer join tmp_jobstat as j
               on zn.zone_id=j.zone_id
          left outer join tmp_hhstat2 as hh2
               on zn.zone_id=hh2.zone_id;
create index SEdata_Z
  on SEdata (Z);
  
update SEdata set TOTHH=0 where TOTHH is NULL;
update SEdata set HH1=0 where HH1 is NULL;
update SEdata set HH2=0 where HH2 is NULL;
update SEdata set HH3=0 where HH3 is NULL;
update SEdata set HH4=0 where HH4 is NULL;
update SEdata set HH5=0 where HH5 is NULL;
update SEdata set HH6P=0 where HH6P is NULL;
update SEdata set TOTPOP=0 where TOTPOP is NULL;
update SEdata set TOTDWL=0 where TOTDWL is NULL;
update SEdata set TOTEMP=0 where TOTEMP is NULL;
update SEdata set RETEMP=0 where RETEMP is NULL;
update SEdata set INDEMP=0 where INDEMP is NULL;
update SEdata set OTHEMP=0 where OTHEMP is NULL;


########################################################################################
#  THE SCRIPT FROM HERE FORWARD IS USED TO CREATE THE "HHdistrib_joint_inclohi" TABLE  #
########################################################################################

# Add columns to the households data table from Part 5a

alter table households_all_$year1 
     add column(S1ILW0 int(1)),
     add column(S1ILW1 int(1)),
     add column(S1ILW2 int(1)),
     add column(S1ILW3 int(1)),
     add column(S1IHW0 int(1)),
     add column(S1IHW1 int(1)),
     add column(S1IHW2 int(1)),
     add column(S1IHW3 int(1)),

     add column(S2ILW0 int(1)),
     add column(S2ILW1 int(1)),
     add column(S2ILW2 int(1)),
     add column(S2ILW3 int(1)),
     add column(S2IHW0 int(1)),
     add column(S2IHW1 int(1)),
     add column(S2IHW2 int(1)),
     add column(S2IHW3 int(1)),

     add column(S3ILW0 int(1)),
     add column(S3ILW1 int(1)),
     add column(S3ILW2 int(1)),
     add column(S3ILW3 int(1)),
     add column(S3IHW0 int(1)),
     add column(S3IHW1 int(1)),
     add column(S3IHW2 int(1)),
     add column(S3IHW3 int(1)),

     add column(S4ILW0 int(1)),
     add column(S4ILW1 int(1)),
     add column(S4ILW2 int(1)),
     add column(S4ILW3 int(1)),
     add column(S4IHW0 int(1)),
     add column(S4IHW1 int(1)),
     add column(S4IHW2 int(1)),
     add column(S4IHW3 int(1)),

     add column(S5ILW0 decimal(5,3)),
     add column(S5ILW1 decimal(5,3)),
     add column(S5ILW2 decimal(5,3)),
     add column(S5ILW3 decimal(5,3)),
     add column(S5IHW0 decimal(5,3)),
     add column(S5IHW1 decimal(5,3)),
     add column(S5IHW2 decimal(5,3)),
     add column(S5IHW3 decimal(5,3)),

     add column(S6ILW0 decimal(5,3)),
     add column(S6ILW1 decimal(5,3)),
     add column(S6ILW2 decimal(5,3)),
     add column(S6ILW3 decimal(5,3)),
     add column(S6IHW0 decimal(5,3)),
     add column(S6IHW1 decimal(5,3)),
     add column(S6IHW2 decimal(5,3)),
     add column(S6IHW3 decimal(5,3));

# Populate the table's category dummy variables

Update households_all_$year1 set S1ILW0=1 where persons=1 and income<20001 and workers=0;
Update households_all_$year1 set S1ILW1=1 where persons=1 and income<20001 and workers=1;
Update households_all_$year1 set S1ILW2=1 where persons=1 and income<20001 and workers=2;
Update households_all_$year1 set S1ILW3=1 where persons=1 and income<20001 and workers=3;
Update households_all_$year1 set S1IHW0=1 where persons=1 and income>20000 and workers=0;
Update households_all_$year1 set S1IHW1=1 where persons=1 and income>20000 and workers=1;
Update households_all_$year1 set S1IHW2=1 where persons=1 and income>20000 and workers=2;
Update households_all_$year1 set S1IHW3=1 where persons=1 and income>20000 and workers=3;

Update households_all_$year1 set S2ILW0=1 where persons=2 and income<20001 and workers=0;
Update households_all_$year1 set S2ILW1=1 where persons=2 and income<20001 and workers=1;
Update households_all_$year1 set S2ILW2=1 where persons=2 and income<20001 and workers=2;
Update households_all_$year1 set S2ILW3=1 where persons=2 and income<20001 and workers=3;
Update households_all_$year1 set S2IHW0=1 where persons=2 and income>20000 and workers=0;
Update households_all_$year1 set S2IHW1=1 where persons=2 and income>20000 and workers=1;
Update households_all_$year1 set S2IHW2=1 where persons=2 and income>20000 and workers=2;
Update households_all_$year1 set S2IHW3=1 where persons=2 and income>20000 and workers=3;

Update households_all_$year1 set S3ILW0=1 where persons=3 and income<20001 and workers=0;
Update households_all_$year1 set S3ILW1=1 where persons=3 and income<20001 and workers=1;
Update households_all_$year1 set S3ILW2=1 where persons=3 and income<20001 and workers=2;
Update households_all_$year1 set S3ILW3=1 where persons=3 and income<20001 and workers=3;
Update households_all_$year1 set S3IHW0=1 where persons=3 and income>20000 and workers=0;
Update households_all_$year1 set S3IHW1=1 where persons=3 and income>20000 and workers=1;
Update households_all_$year1 set S3IHW2=1 where persons=3 and income>20000 and workers=2;
Update households_all_$year1 set S3IHW3=1 where persons=3 and income>20000 and workers=3;

Update households_all_$year1 set S4ILW0=1 where persons=4 and income<20001 and workers=0;
Update households_all_$year1 set S4ILW1=1 where persons=4 and income<20001 and workers=1;
Update households_all_$year1 set S4ILW2=1 where persons=4 and income<20001 and workers=2;
Update households_all_$year1 set S4ILW3=1 where persons=4 and income<20001 and workers=3;
Update households_all_$year1 set S4IHW0=1 where persons=4 and income>20000 and workers=0;
Update households_all_$year1 set S4IHW1=1 where persons=4 and income>20000 and workers=1;
Update households_all_$year1 set S4IHW2=1 where persons=4 and income>20000 and workers=2;
Update households_all_$year1 set S4IHW3=1 where persons=4 and income>20000 and workers=3;

Update households_all_$year1 set S5ILW0=.432 where persons=5.8 and income<20001 and workers=0;
Update households_all_$year1 set S5ILW1=.432 where persons=5.8 and income<20001 and workers=1;
Update households_all_$year1 set S5ILW2=.432 where persons=5.8 and income<20001 and workers=2;
Update households_all_$year1 set S5ILW3=.432 where persons=5.8 and income<20001 and workers=3;
Update households_all_$year1 set S5IHW0=.432 where persons=5.8 and income>20000 and workers=0;
Update households_all_$year1 set S5IHW1=.432 where persons=5.8 and income>20000 and workers=1;
Update households_all_$year1 set S5IHW2=.432 where persons=5.8 and income>20000 and workers=2;
Update households_all_$year1 set S5IHW3=.432 where persons=5.8 and income>20000 and workers=3;

Update households_all_$year1 set S6ILW0=.568 where persons=5.8 and income<20001 and workers=0;
Update households_all_$year1 set S6ILW1=.568 where persons=5.8 and income<20001 and workers=1;
Update households_all_$year1 set S6ILW2=.568 where persons=5.8 and income<20001 and workers=2;
Update households_all_$year1 set S6ILW3=.568 where persons=5.8 and income<20001 and workers=3;
Update households_all_$year1 set S6IHW0=.568 where persons=5.8 and income>20000 and workers=0;
Update households_all_$year1 set S6IHW1=.568 where persons=5.8 and income>20000 and workers=1;
Update households_all_$year1 set S6IHW2=.568 where persons=5.8 and income>20000 and workers=2;
Update households_all_$year1 set S6IHW3=.568 where persons=5.8 and income>20000 and workers=3;

# Aggregate counts of dummy variables to the zone level

drop table if exists HHdistrib_joint_inclohi;
Create table HHdistrib_joint_inclohi(ZONE int(1),
     S1ILW0 decimal(5,2), S1ILW1 decimal(5,2), S1ILW2 decimal(5,2), S1ILW3 decimal(5,2),
     S1IHW0 decimal(5,2), S1IHW1 decimal(5,2), S1IHW2 decimal(5,2), S1IHW3 decimal(5,2),
     S2ILW0 decimal(5,2), S2ILW1 decimal(5,2), S2ILW2 decimal(5,2), S2ILW3 decimal(5,2),
     S2IHW0 decimal(5,2), S2IHW1 decimal(5,2), S2IHW2 decimal(5,2), S2IHW3 decimal(5,2),
     S3ILW0 decimal(5,2), S3ILW1 decimal(5,2), S3ILW2 decimal(5,2), S3ILW3 decimal(5,2),
     S3IHW0 decimal(5,2), S3IHW1 decimal(5,2), S3IHW2 decimal(5,2), S3IHW3 decimal(5,2),
     S4ILW0 decimal(5,2), S4ILW1 decimal(5,2), S4ILW2 decimal(5,2), S4ILW3 decimal(5,2),
     S4IHW0 decimal(5,2), S4IHW1 decimal(5,2), S4IHW2 decimal(5,2), S4IHW3 decimal(5,2),
     S5ILW0 decimal(5,2), S5ILW1 decimal(5,2), S5ILW2 decimal(5,2), S5ILW3 decimal(5,2),
     S5IHW0 decimal(5,2), S5IHW1 decimal(5,2), S5IHW2 decimal(5,2), S5IHW3 decimal(5,2),
     S6ILW0 decimal(5,2), S6ILW1 decimal(5,2), S6ILW2 decimal(5,2), S6ILW3 decimal(5,2),
     S6IHW0 decimal(5,2), S6IHW1 decimal(5,2), S6IHW2 decimal(5,2), S6IHW3 decimal(5,2),
     TotalHH decimal(5,2));
     
Insert into HHdistrib_joint_inclohi
  select b.zone_id as ZONE,  
    sum(S1ILW0) as S1ILW0, 
    sum(S1ILW1) as S1ILW1,
    sum(S1ILW2) as S1ILW2, 
    sum(S1ILW3) as S1ILW3,    
    sum(S1IHW0) as S1IHW0, 
    sum(S1IHW1) as S1IHW1,
    sum(S1IHW2) as S1IHW2, 
    sum(S1IHW3) as S1IHW3, 
    sum(S2ILW0) as S2ILW0, 
    sum(S2ILW1) as S2ILW1,
    sum(S2ILW2) as S2ILW2, 
    sum(S2ILW3) as S2ILW3,
    sum(S2IHW0) as S2IHW0, 
    sum(S2IHW1) as S2IHW1,
    sum(S2IHW2) as S2IHW2, 
    sum(S2IHW3) as S2IHW3, 
    sum(S3ILW0) as S3ILW0, 
    sum(S3ILW1) as S3ILW1,
    sum(S3ILW2) as S3ILW2, 
    sum(S3ILW3) as S3ILW3,    
    sum(S3IHW0) as S3IHW0, 
    sum(S3IHW1) as S3IHW1,
    sum(S3IHW2) as S3IHW2, 
    sum(S3IHW3) as S3IHW3, 
    sum(S4ILW0) as S4ILW0, 
    sum(S4ILW1) as S4ILW1,
    sum(S4ILW2) as S4ILW2, 
    sum(S4ILW3) as S4ILW3,    
    sum(S4IHW0) as S4IHW0, 
    sum(S4IHW1) as S4IHW1,
    sum(S4IHW2) as S4IHW2, 
    sum(S4IHW3) as S4IHW3, 
    sum(S5ILW0) as S5ILW0, 
    sum(S5ILW1) as S5ILW1,
    sum(S5ILW2) as S5ILW2, 
    sum(S5ILW3) as S5ILW3,    
    sum(S5IHW0) as S5IHW0, 
    sum(S5IHW1) as S5IHW1,
    sum(S5IHW2) as S5IHW2, 
    sum(S5IHW3) as S5IHW3,
    sum(S6ILW0) as S6ILW0, 
    sum(S6ILW1) as S6ILW1,
    sum(S6ILW2) as S6ILW2, 
    sum(S6ILW3) as S6ILW3,    
    sum(S6IHW0) as S6IHW0, 
    sum(S6IHW1) as S6IHW1,
    sum(S6IHW2) as S6IHW2, 
    sum(S6IHW3) as S6IHW3,
    count(grid_id) as TotalHH 
  from households_all_$year1 as h right join WFRC_1997_baseyear.zones as b
  on h.zone_id = b.zone_id
  group by b.zone_id;
create index HHdistrib_joint_inclohi_ZONE
  on HHdistrib_joint_inclohi (ZONE);

# Set NULL's to zero

update HHdistrib_joint_inclohi set S1ILW0=0 where S1ILW0 is NULL;
update HHdistrib_joint_inclohi set S1ILW1=0 where S1ILW1 is NULL;
update HHdistrib_joint_inclohi set S1ILW2=0 where S1ILW2 is NULL;
update HHdistrib_joint_inclohi set S1ILW3=0 where S1ILW3 is NULL;
update HHdistrib_joint_inclohi set S2ILW0=0 where S2ILW0 is NULL;
update HHdistrib_joint_inclohi set S2ILW1=0 where S2ILW1 is NULL;
update HHdistrib_joint_inclohi set S2ILW2=0 where S2ILW2 is NULL;
update HHdistrib_joint_inclohi set S2ILW3=0 where S2ILW3 is NULL;
update HHdistrib_joint_inclohi set S3ILW0=0 where S3ILW0 is NULL;
update HHdistrib_joint_inclohi set S3ILW1=0 where S3ILW1 is NULL;
update HHdistrib_joint_inclohi set S3ILW2=0 where S3ILW2 is NULL;
update HHdistrib_joint_inclohi set S3ILW3=0 where S3ILW3 is NULL;
update HHdistrib_joint_inclohi set S4ILW0=0 where S4ILW0 is NULL;
update HHdistrib_joint_inclohi set S4ILW1=0 where S4ILW1 is NULL;
update HHdistrib_joint_inclohi set S4ILW2=0 where S4ILW2 is NULL;
update HHdistrib_joint_inclohi set S4ILW3=0 where S4ILW3 is NULL;
update HHdistrib_joint_inclohi set S5ILW0=0 where S5ILW0 is NULL;
update HHdistrib_joint_inclohi set S5ILW1=0 where S5ILW1 is NULL;
update HHdistrib_joint_inclohi set S5ILW2=0 where S5ILW2 is NULL;
update HHdistrib_joint_inclohi set S5ILW3=0 where S5ILW3 is NULL;
update HHdistrib_joint_inclohi set S6ILW0=0 where S6ILW0 is NULL;
update HHdistrib_joint_inclohi set S6ILW1=0 where S6ILW1 is NULL;
update HHdistrib_joint_inclohi set S6ILW2=0 where S6ILW2 is NULL;
update HHdistrib_joint_inclohi set S6ILW3=0 where S6ILW3 is NULL;
update HHdistrib_joint_inclohi set S1IHW0=0 where S1IHW0 is NULL;
update HHdistrib_joint_inclohi set S1IHW1=0 where S1IHW1 is NULL;
update HHdistrib_joint_inclohi set S1IHW2=0 where S1IHW2 is NULL;
update HHdistrib_joint_inclohi set S1IHW3=0 where S1IHW3 is NULL;
update HHdistrib_joint_inclohi set S2IHW0=0 where S2IHW0 is NULL;
update HHdistrib_joint_inclohi set S2IHW1=0 where S2IHW1 is NULL;
update HHdistrib_joint_inclohi set S2IHW2=0 where S2IHW2 is NULL;
update HHdistrib_joint_inclohi set S2IHW3=0 where S2IHW3 is NULL;
update HHdistrib_joint_inclohi set S3IHW0=0 where S3IHW0 is NULL;
update HHdistrib_joint_inclohi set S3IHW1=0 where S3IHW1 is NULL;
update HHdistrib_joint_inclohi set S3IHW2=0 where S3IHW2 is NULL;
update HHdistrib_joint_inclohi set S3IHW3=0 where S3IHW3 is NULL;
update HHdistrib_joint_inclohi set S4IHW0=0 where S4IHW0 is NULL;
update HHdistrib_joint_inclohi set S4IHW1=0 where S4IHW1 is NULL;
update HHdistrib_joint_inclohi set S4IHW2=0 where S4IHW2 is NULL;
update HHdistrib_joint_inclohi set S4IHW3=0 where S4IHW3 is NULL;
update HHdistrib_joint_inclohi set S5IHW0=0 where S5IHW0 is NULL;
update HHdistrib_joint_inclohi set S5IHW1=0 where S5IHW1 is NULL;
update HHdistrib_joint_inclohi set S5IHW2=0 where S5IHW2 is NULL;
update HHdistrib_joint_inclohi set S5IHW3=0 where S5IHW3 is NULL;
update HHdistrib_joint_inclohi set S6IHW0=0 where S6IHW0 is NULL;
update HHdistrib_joint_inclohi set S6IHW1=0 where S6IHW1 is NULL;
update HHdistrib_joint_inclohi set S6IHW2=0 where S6IHW2 is NULL;
update HHdistrib_joint_inclohi set S6IHW3=0 where S6IHW3 is NULL;

# clean up

drop table if exists gridcells_exported_$year1;
drop table if exists households_all_$year1;
drop table if exists households_exported_$year1;
drop table if exists jobs_exported_$year1;
