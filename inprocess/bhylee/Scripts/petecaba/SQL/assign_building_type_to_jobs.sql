### create database PSRC_reclass_job_building_type_countyname and run query ###

create table jobs 
	(JOB_ID INT PRIMARY KEY AUTO_INCREMENT,
	 GRID_ID INT, 
	 SECTOR_ID INT, 
	 HOME_BASED TINYINT, 
	 SIC INT, 
	 JOB_ALLOCATOR INT, 
	 PROPRIETOR INT);

insert into jobs (grid_id, sector_id, home_based, sic, job_allocator) 
 select 
 	grid_id,
 	sector,
 	home_based,
 	sic, 
 	1 as job_allocator 
from job_allocation_king.jobs;
 
insert into jobs (grid_id, sector_id, home_based, proprietor)
 select 
 	grid_id,
 	sector,
 	home_based, 
 	1 as proprietor 
from PSRC_proprietors_distributor_pierce.JOBS_ROUNDED;

### Run in job_allocation_countyname database ###

#Use "employers_to_jobs_prep.sql" script as basis for gathering the parcel's land use code (commercial, governmental, industrial, etc) 

# Run queries one tmp_employers_3 table is created from script above
alter table tmp_employers_3 add column LAND_USE varchar(50);
alter table tmp_employers_3 add column USE_CODE int;
alter table tmp_employers_3 add column GENERIC_LU varchar(20);
alter table tmp_employers_3 add column COUNTY varchar(3);
alter table tmp_employers_3 add index prcl_index(parcel_id(10));

update tmp_employers_3 
 a inner join parcels b 
  on a.parcel_id = b.parcel_id 
set a.land_use = b.land_use, 
 a.use_code = b.use_code, 
 a.county = b.county;

alter table tmp_employers_3 add index cnty_lu_index(county(3), use_code);

update tmp_employers_3 a 
 inner join PSRC_2000_reclassification_tables.land_use_generic_reclass b 
  on a.county = b.county 
 and a.use_code = b.county_land_use_code 
set a.generic_lu = b.generic_land_use_2;

create table tmp_employers_lu 
 select 
 	grid_id, 
 	sector, 
 	home_based, 
 	sum(job_count_rounded) as jobs,
 	sic,
 	generic_lu 
 from tmp_employers_3 
 group by 
	grid_id, 
	sector, 
	home_based, 
	generic_lu;

alter table tmp_employers_lu change column SIC SIC int;
alter table tmp_employers_lu add index sic_index(sic);
alter table tmp_employers_lu add column new_sector_id int;
alter table tmp_employers_lu add index grid_id_sector_home_based_index(grid_id, sector, home_based);
alter table tmp_employers_lu add index grid_id_sector_index(grid_id, sector);

update tmp_employers_lu a 
 inner join PSRC_jobs_reclassification.sic_sector_id_mapping b 
  on a.sic between b.min_sic and b.max_sic 
set a.new_sector_id = b.new_sector_id;

# Run job_reclassification script
# Run in building reclass database
# prior to running script create jobs table with proprietor and job allocator field names

# For King County I created a copy of the jobs_all_sectors_reclassified table from PSRC_jobs_reclassification.jobs_all_sectors_reclassified
# Run queries once jobs_all_sectors_reclassified table has been created

alter table jobs_all_sectors_reclassified_test add column BUILDING_TYPE varchar(10);
alter table jobs_all_sectors_reclassified_test add index grid_sector_index(grid_id, sector_id);

update jobs_all_sectors_reclassified_test a 
 inner join tmp_employers_lu b 
  on a.grid_id = b.grid_id 
  and a.sector_id = b.sector
#  and a.home_based = b.home_based
set a.building_type = b.generic_lu
 where a.job_allocator = 1;

# use jobs_lost_in_translation found in PSRC_proprietor_distributor database:

create table jobs_lost_generic_lu select * from jobs_lost_in_translation;

alter table jobs_lost_generic_lu add column use_code int;
alter table jobs_lost_generic_lu add column building_type varchar(5);
alter table jobs_lost_generic_lu add column county varchar(3);
alter table jobs_lost_generic_lu add index prcl_index(parcel_id(10));

# BE sure to change county name
update jobs_lost_generic_lu a 
 inner join job_allocation_pierce.parcels b 
  on a.parcel_id = b.parcel_id 
set a.county = b.county, 
 a.use_code = b.use_code;

alter table jobs_lost_generic_lu add index cnty_lu_index(county(3), use_code);

update jobs_lost_generic_lu a 
 inner join PSRC_2000_reclassification_tables.land_use_generic_reclass b 
  on a.county = b.county 
  and a.use_code = b.county_land_use_code 
set a.building_type = b.generic_land_use_2;

# Make sure to change the PSRC_proprietor_distributor county name 
alter table DISTRIBUTED_JOBS add index prcl_index(parcel_id(15));

create table jobs_gridcells_1
 select 
	a.GRID_ID, 
	a.PARCEL_ID,
	b.SECTOR, 
	b.HOMEBASED, 
	a.PARCEL_FRACTION,
	round(a.PARCEL_FRACTION) AS JOB
 from parcel_fractions_in_gridcells a 
 inner join DISTRIBUTED_JOBS b
	ON a.parcel_id = b.parcel_id;

alter table jobs_gridcells_1 add column use_code int;
alter table jobs_gridcells_1 add column county varchar(3);
alter table jobs_gridcells_1 add column building_type varchar(5);
alter table jobs_gridcells_1 add index prcl_index(parcel_id(10));

# Make sure to change the job_allocation county name 
update jobs_gridcells_1 a 
 inner join job_allocation_pierce.parcels b 
  on a.parcel_id = b.parcel_id 
set a.county = b.county, 
 a.use_code = b.use_code;

alter table jobs_gridcells_1 add index cnty_lu_index(county, use_code);

update jobs_gridcells_1 a 
 inner join PSRC_2000_reclassification_tables.land_use_generic_reclass b 
  on a.county = b.county 
  and a.use_code = b.county_land_use_code 
set a.building_type = b.generic_land_use_2;
 
alter table jobs_gridcells_1 add index grid_id_sector_home_based_index(grid_id, sector, homebased);
# Create table jobs_all_sectors_reclassified_test from job_allocation database
alter table jobs_all_sectors_reclassified_test add index grid_id_sector_home_based_index(grid_id, sector_id, home_based);

# Be sure to change the county name
update job_allocation_pierce.jobs_all_sectors_reclassified_test a 
 inner join proprietors_distributor_pierce_test.jobs_gridcells_1 b 
  on a.grid_id = b.grid_id 
  and a.sector_id = b.sector
  and a.home_based = b.homebased
set a.building_type = b.building_type 
 where a.proprietor = 1
  and b.job = 1;
 #where a.building_type is null;

## Set building type = 'R' where home_based = 1 ## 
#update jobs_all_sectors_reclassified_test 
# set building_type = 'R'
#where home_based = 1;

## Create scaled down table of jobs_all_sectors_reclassified_test ##

create table jobs_scaled_down
 select 
 	grid_id,
 	count(*) as jobs,
 	new_new_sector_id, 
 	home_based,
 	building_type 
 from jobs_all_sectors_reclassified_test 
 group by
 	grid_id,
 	new_new_sector_id,
 	home_based;

alter table jobs_scaled_down add index grid_id_new_sector_home_based_index(grid_id, new_new_sector_id, home_based);

# Update new jobs table 

update GSPSRC_2000_baseyear_change_20050718.jobs a 
 inner join PSRC_reclass_jobs_building_type_king.jobs_scaled_down b
  on a.grid_id = b.grid_id 
  and a.sector_id = b.new_new_sector_id
  and a.home_based = b.home_based
set a.building_type = b.building_type;
 

## Update new jobs table using PSRC_2000_baseyear_updates_for_reestimation.jobs_enlisted_military_short ##

create table jobs_enlisted_military_short 
 select 
 	GRID_ID, 
 	SECTOR_ID,
 	count(*) as JOBS
 from jobs_enlisted_military 
 group by 
	grid_id,
	sector_id;

alter table jobs_enlisted_military_short add column BUILDING_TYPE varchar(5);

update jobs_enlisted_military_short set building_type = 'G';

alter table jobs_enlisted_military_short add index grid_id_sector_index(grid_id, sector_id);

update GSPSRC_2000_baseyear_change_20050718.jobs a 
 inner join PSRC_2000_baseyear_updates_for_reestimation.jobs_enlisted_military_short b
  on a.grid_id = b.grid_id 
  and a.sector_id = b.sector_id 
set a.building_type = b.building_type
 where a.building_type is null;
 
## Update jobs_new table using PSRC_2000_baseyear_updates_for_reestimation.jobs_pie_military_reclassified_short ##

create table jobs_pie_military_reclassified_short
 select 
 	GRID_ID, 
 	SECTOR_ID, 
 	SIC, 
 	count(*) as JOBS
 from jobs_pie_military_reclassified
 group by 
 	grid_id, 
 	sector_id,
 	sic;
 
alter table jobs_pie_military_reclassified_short add column BUILDING_TYPE varchar(5);

update jobs_pie_military_reclassified_short set building_type = 'G';

alter table jobs_pie_military_reclassified_short add index grid_id_sector_index(grid_id, sector_id);

update GSPSRC_2000_baseyear_change_20050718.jobs a 
 inner join PSRC_2000_baseyear_updates_for_reestimation.jobs_pie_military_reclassified_short b
  on a.grid_id = b.grid_id 
  and a.sector_id = b.sector_id 
set a.building_type = b.building_type
 where a.building_type is null;


# Update jobs_new table setting all home_based jobs' building_type = 'R' 

update jobs_new set building_type = 'R' where home_based = 1;
update jobs_new set building_type = 'R' where building_type = 'GQ';

#########################################################################################################################
#### Assign majority type (commercial, governmental, industrial sqft) to jobs where building type = "NR" and is null ####

/*
create table jobs_final 
 select JOB_ID,
 	GRID_ID,
 	NEW_NEW_SECTOR_ID AS SECTOR_ID, 
 	HOME_BASED,
 	SIC,
 	BUILDING_TYPE
 from jobs_all_sectors_reclassified_test
 where new_new_sector_id is not null;
*/
update jobs_final set building_type = 'R' where building_type = 'GQ';
update jobs_final set building_type = 'R' where home_based = 1;

create temporary table tmp_no_building_type 
 select 
 	grid_id,
 	sector_id,
 	home_based,
 	sic
 from jobs_final
 where building_type is null or building_type = 'NR' or
 (building_type = 'R' and home_based = 0);

alter table tmp_no_building_type add index grid_id_index(grid_id);

create temporary table tmp_max_use_1
 select 
  	a.grid_id,
  	b.commercial_sqft, 
  	b.governmental_sqft,
  	b.industrial_sqft
 from tmp_no_building_type a
  left join GSPSRC_2000_baseyear_flattened.gridcells b
   on a.grid_id = b.grid_id;

alter table tmp_max_use_1 add column max_use text;

create temporary table tmp_max_use
 select 
 	grid_id, 
 	commercial_sqft,
 	governmental_sqft,
 	industrial_sqft,
 	if(industrial_sqft > 
 	if(commercial_sqft > governmental_sqft, commercial_sqft, governmental_sqft), industrial_sqft, 
 	if(commercial_sqft > governmental_sqft, commercial_sqft, governmental_sqft)) as max_sqft
 from tmp_max_use_1 
 group by 
 	grid_id;

alter table tmp_max_use add column building_type varchar(5);

update tmp_max_use set building_type = 'I' where max_sqft = industrial_sqft;
update tmp_max_use set building_type = 'C' where max_sqft = commercial_sqft;
update tmp_max_use set building_type = 'G' where max_sqft = governmental_sqft;
update tmp_max_use set building_type = 'C' where max_sqft = 0;

alter table tmp_max_use add index grid_id_index(grid_id);

# Update missing jobs with null or 'NR' building types

alter table jobs_final add column IMPUTE_FLAG tinyint;

update jobs_final set impute_flag = 1 
 where building_type is null or building_type = 'NR'
 or (building_type = 'R' and home_based = 0);

update jobs_final a 
 inner join tmp_max_use b
  on a.grid_id = b.grid_id
set a.building_type = b.building_type 
 where a.building_type is null or a.building_type = 'NR' or
 (a.building_type = 'R' and home_based = 0);

#########################################################
#### create proportion_sector_by_building_type table ####

create table proportion_sector_by_building_type
 (sector_id int,
  name text,
  building_type varchar(5),
  jobs int,
  #building_type_count int,
  sector_id_count int,
  proportion double);

insert into proportion_sector_by_building_type (sector_id, name, building_type, jobs)
 select 
 	a.sector_id as sector_id,
 	b.name as name,
 	a.building_type as building_type,
 	count(*) as jobs
 from jobs a 
 inner join GSPSRC_2000_baseyear_flattened.employment_sectors b
  on a.sector_id = b.sector_id
 where a.home_based <> 1 and a.building_type <> 'R'
 group by 
 	a.sector_id, 
 	b.name, 
 	a.building_type;

/*
create temporary table tmp_building_type_count
 select
 	building_type,
 	count(*) as count
 from jobs
 group by 
 	building_type;
*/

create temporary table tmp_sector_id_count
select
	sector_id,
	count(*) as count
from jobs
group by 
	sector_id;


update proportion_sector_by_building_type a 
 inner join tmp_sector_id_count b 
  on a.sector_id = b.sector_id
set a.sector_id_count = b.count;

update proportion_sector_by_building_type 
 set proportion = jobs / sector_id_count;
 
##############################################################################################################
#### create commercial and industrial sqft per job columns in gridcells table (ex. commercial_sqft / job) ####

/* work in progress

create table gridcells_new select * from GSPSRC_2000_baseyear_flattened.gridcells

alter table gridcells add column commercial_sqft_per_job double;
alter table gridcells add column industrial_sqft_per_job double;
alter table gridcells add column vacant_sqft double;

create temporary table tmp_jobs_summarized
 select 
	 grid_id, 
	 building_type, 
	 count(*) as jobs
 from jobs 
 where building_type in ('C', 'I') 
 group by 
 	grid_id, 
 	building_type;
  
alter table tmp_jobs_summarized add index grid_id_index(grid_id); 

update gridcells a 
 inner join tmp_jobs_summarized b 
 on a.grid_id = b.grid_id
set a.commercial_sqft_per_job = (a.commercial_sqft/ b.jobs)
 where b.building_type = 'C';
 
update gridcells a 
 inner join tmp_jobs_summarized b 
 on a.grid_id = b.grid_id
set a.industrial_sqft_per_job = (a.industrial_sqft/ b.jobs)
 where b.building_type = 'I'; 
 
update gridcells a
 inner join tmp_jobs_summarized b 
 on a.grid_id = b.grid_id
set a.vacant_commercial_sqft = (a.commercial_sqft - (b.jobs * a.commercial_sqft_per_job))
 where b.building_type = 'C';
 
update gridcells a
 inner join tmp_jobs_summarized b 
 on a.grid_id = b.grid_id
set a.vacant_industrial_sqft = (a.industrial_sqft - (b.jobs * a.industrial_sqft_per_job))
 where b.building_type = 'I'; 

# Delete tables
drop table tmp_jobs_summarized;


*check* 
create temporary table c 
 select 
 	 grid_id, 
 	 building_type, 
 	 count(*) a 
 from jobs_new 
 where building_type not in ('G', 'R') 
 group by 
 	grid_id,
 	building_type; 
 
 
 
 