## Input table buildings from county ##




#drop table if exists prelim_employers_to_parcels;
#CREATE TABLE prelim_employers_to_parcels
# SELECT 
# 	a.PARCEL_ID,
# 	b.EMPLOYER_ID,
# 	b.SIC,
# 	b.SECTOR,
# 	b.NUMBER_OF_JOBS as JOBS,
# 	c.USE_CODE,
# 	c.SQUARE_FOOTAGE as SQFT,
# 	c.LAND_USE as GENERIC_LAND_USE_1,
# 	d.GENERIC_LAND_USE_2,
# 	e.TAXEXEMPT_BINARY,
# 	e.YEAR_BUILT
# FROM job_allocation_pierce.final_employers_matched_to_parcels a 
# INNER JOIN PSRC_parcels_pierce.parcels e on a.parcel_id = e.parcel_id
# INNER JOIN job_allocation_pierce.parcels c on (a.parcel_id = c.parcel_id)
# INNER JOIN job_allocation_pierce.employers b ON (a.employer_id = b.employer_id)
# INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass d on (c.county = d.county 
#  and c.use_code = d.county_land_use_code)
# WHERE a.decision not in ('NO_PARCEL_IN_BLOCK', 'WRONG_SIDE_OF_STREET', 'WRONG_STREET_TYPE_FOR_BLOCK')
# AND (d.generic_land_use_2 <> 'R')
#; 
 

drop table if exists step_sector_reclass;
create table step_sector_reclass (SECTOR varchar(100), STEP varchar(100), COMBO varchar(50));
insert into step_sector_reclass (sector, step, combo)
 values ('Agriculture', 'RES', 'CONST/RES'),
 	('Construction', 'RES', 'CONST/RES'),
 	('EDUCATION HIGHER', 'GOVED', 'GOVED'),
 	('EDUCATION K-12', 'GOVED', 'GOVED'),
 	('FEDERAL, CIVILIAN', 'GOVED', 'GOVED'),
 	('FEDERAL, MILITARY', 'GOVED', 'GOVED'),
 	('FIRES', 'FIRES', 'FIRES'),
 	('Manufacturing', 'MANUF', 'MANUF'),
 	('Mining', 'RES', 'RES'),
 	('Public Administration', 'GOVED', 'GOVED'),
 	('Retail Trade', 'RETAIL', 'RETAIL'),
 	('Services', 'FIRES', 'FIRES'),
 	('STATE AND LOCAL', 'GOVED', 'GOVED'),
 	('Transportation, Communications, Electric, Gas, San', 'WTCU', 'WTCU'),
 	('Wholesale Trade', 'WTCU', 'WTCU');

alter table step_sector_reclass add index sector_index(sector(10));
alter table prelim_employers_to_parcels add column STEP varchar (100);
alter table prelim_employers_to_parcels add index sector_index(sector(10));
alter table prelim_employers_to_parcels add column sqft_per_job double;

update prelim_employers_to_parcels set sqft_per_job = sqft / jobs;

update prelim_employers_to_parcels a 
 inner join step_sector_reclass b on a.sector = b.sector
 set a.STEP = b.STEP;

drop table if exists step_sector;
create table step_sector (STEP varchar(100), COUNTY varchar(3), SQFT int);
insert into step_sector values
("const,fires,goved,manuf,retail,wtcu","035",376.4815618),
("res", "035", 778.3010471),
("fires", "035", 649.8268835),
("goved", "035", 600.721874),
("manuf,wtcu", "035", 530),
("manuf","035",796.957265),
("fires,retail","035",503.2097058),
("fires,goved,retail","035",307),
("retail","035",703.9661267),
("wtcu","035",1277.286872),
("catch_all", "035", 376)
;

drop table if exists grouped_step_sector;
create table grouped_step_sector
 select parcel_id, 
 	sum(jobs) as jobs,
 	sqft as parcel_sqft,
 	use_code,
 	generic_land_use_1,
 	generic_land_use_2,
 	taxexempt_binary,
 	year_built,
 	sqft_per_job,
 	group_concat(distinct step order by step separator ',') as step
 from prelim_employers_to_parcels
 group by parcel_id;

drop table if exists grouped_parcel_with_step_sqft;
create table grouped_parcel_with_step_sqft
 select g.*,
 	s.sqft as step_sqft
 from grouped_step_sector g 
 inner join step_sector s on lower(g.step) = s.step;

drop table if exists missing_records;
create temporary table missing_records 
 select g.*,  	
 	s.sqft as step_sqft
 from grouped_step_sector g
 left outer join step_sector s on lower(g.step) = s.step
 where s.step is null;
 
 update missing_records set step = "catch_all";
 update missing_records set step_sqft = 334;
 
 insert into grouped_parcel_with_step_sqft select * from missing_records;
 
 update grouped_parcel_with_step_sqft set sqft_per_job = parcel_sqft / jobs;
 
 alter table grouped_parcel_with_step_sqft add index prcl_index(parcel_id(10));
 
 ##
 ## Percentile table 
 ##
 
 ## Prelim value 
 drop table if exists prelim_sqft_values;
 create temporary table prelim_sqft_values (
  generic_land_use_1 varchar(100),
  sqft_per_job double,
  step varchar(100)
 );
 
 insert into prelim_sqft_values (
   	generic_land_use_1,
   	sqft_per_job,
  	step)
  select 
  	generic_land_use_1,
  	sqft_per_job, 
  	step 
  from grouped_parcel_with_step_sqft
 ;
 
 ## Get ordered list of values
 drop table if exists ordered_values;
 create temporary table ordered_values (
  rec_number int auto_increment primary key,
  descriptive_field varchar(8),
  group_field_1 varchar(16),
  group_field_2 varchar(16),
  value double
 );
 
 insert into ordered_values (
 	group_field_1, 
 	group_field_2,
  	value)
  select 
  	generic_land_use_1,
  	step,
   	sqft_per_job
  from prelim_sqft_values
  order by 
  	generic_land_use_1,
  	step,
   	sqft_per_job
 ;	
  	
## Construct table of percentiles  	
drop table if exists percentiles;
create temporary table percentiles (percentile double);

insert into percentiles (percentile)
values
	(0.0),
	(.01),
  	(.05),
  	(.1),
 	(.25),
	(.5),
	(.75),
	(.9),
 	(.95),
	(.99),
	(1)
;

## Get list of max, min row values for step in ordered_values
drop table if exists group_row_limits;
create temporary table group_row_limits
select 
	group_field_1,
	group_field_2,
	count(*) as num_records,
	min(rec_number) as min_rec_number,
	max(rec_number) as max_rec_number
from ordered_values
group by 
	group_field_1,
	group_field_2
;

## Construct table group_percentile_rows listing row number 
##  for summary percentile combination
drop table if exists group_percentile_rows;
create temporary table group_percentile_rows (
	group_field_1 varchar(16),
	group_field_2 varchar(16),
	num_records int,
	percentile double,
	percentile_row_number int
);

insert into group_percentile_rows (
       group_field_1,
       group_field_2,
       percentile )
select 
       grl.group_field_1,
       grl.group_field_2,
       prctl.percentile
from
     group_row_limits grl
     inner join percentiles prctl
;

update group_percentile_rows gpr, group_row_limits grl
set percentile_row_number =
    (ceiling((grl.max_rec_number - grl.min_rec_number) * gpr.percentile)) + grl.min_rec_number,
    gpr.num_records = grl.num_records
where 
      gpr.group_field_1 = grl.group_field_1 and gpr.group_field_2 = grl.group_field_2
;

## Get values of interest from the ordered list of values for the row number
##   for each combo
drop table if exists result_percentile_by_rows;
CREATE TEMPORARY TABLE result_percentile_by_rows
SELECT
	gpr.group_field_1 as land_use,
	gpr.group_field_2 as step,
	(gpr.percentile * 100) as percentile,
	round(opv.value,2) as sqft_per_job,
	gpr.num_records as total_number_of_employers
FROM group_percentile_rows gpr INNER JOIN ordered_values opv
	ON gpr.percentile_row_number = opv.rec_number
ORDER BY 
	gpr.group_field_1,
	gpr.group_field_2,
	gpr.percentile
;


## Create final percentile table
drop table if exists sqft_per_job_percentiles_by_sector;
CREATE TABLE sqft_per_job_percentiles_by_sector
SELECT 
       step, 
       land_use,
       total_number_of_employers, 
       sum(IF(percentile=0, sqft_per_job, 0)) as "0_percentile",
       sum(IF(percentile=1, sqft_per_job, 0)) as "1_percentile",
       sum(IF(percentile=5, sqft_per_job, 0)) as "5_percentile",
       sum(IF(percentile=10, sqft_per_job, 0)) as "10_percentile",
       sum(IF(percentile=25, sqft_per_job, 0)) as "25_percentile",
       sum(IF(percentile=50, sqft_per_job, 0)) as "50_percentile",
       sum(IF(percentile=75, sqft_per_job, 0)) as "75_percentile",
       sum(IF(percentile=90, sqft_per_job, 0)) as "90_percentile",
       sum(IF(percentile=95, sqft_per_job, 0)) as "95_percentile",
       sum(IF(percentile=99, sqft_per_job, 0)) as "99_percentile",
       sum(IF(percentile=100, sqft_per_job, 0)) as "100_percentile"
FROM 
     result_percentile_by_rows
GROUP BY 
      step,
      land_use
;

## Select records from percentile table that fall below the 10th percentile or 0 Sqft values
drop table if exists pre_10th_percentile;
create temporary table pre_10th_percentile
 select a.*, 1 as imputed_flag from grouped_parcel_with_step_sqft a 
 inner join sqft_per_job_percentiles_by_sector b 
 on a.step = b.step and a.generic_land_use_1 = b.land_use
 where (a.sqft_per_job < b.10_percentile) or (a.sqft_per_job = 0);
 
alter table pre_10th_percentile add index prcl_index(parcel_id(10));
 
## Select records from percentile table that are above the 99th percentile
drop table if exists pre_99th_percentile;
create temporary table pre_99th_percentile
 select a.*, 1 as imputed_flag from grouped_parcel_with_step_sqft a 
 inner join sqft_per_job_percentiles_by_sector b 
 on a.step = b.step and a.generic_land_use_1 = b.land_use
 where a.sqft_per_job >= b.99_percentile and a.parcel_sqft <> 0;

alter table pre_99th_percentile add index prcl_index(parcel_id(10));

## update tails of distribution tables with new imputed sqft values

# 10th percentile

alter table pre_10th_percentile add column imputed_sqft double;
update pre_10th_percentile set imputed_sqft = step_sqft * jobs;

# 99th percentile
alter table pre_99th_percentile add column imputed_sqft double;
update pre_99th_percentile set imputed_sqft = (abs((step_sqft * jobs)-parcel_sqft));

## update original parcel records with new imputed sqft values

alter table grouped_parcel_with_step_sqft add column imputed_sqft double;
alter table grouped_parcel_with_step_sqft add column imputed_sqft_flag tinyint;

update grouped_parcel_with_step_sqft a 
 inner join pre_10th_percentile b on a.parcel_id = b.parcel_id 
 set a.imputed_sqft = b.imputed_sqft;

update grouped_parcel_with_step_sqft a
 inner join pre_99th_percentile b on a.parcel_id = b.parcel_id 
 set a.imputed_sqft = b.imputed_sqft;

update grouped_parcel_with_step_sqft set imputed_sqft_flag = 1
 where imputed_sqft is not null;
 
update grouped_parcel_with_step_sqft set imputed_sqft = parcel_sqft 
 where imputed_sqft_flag is null;

## Allocate sqft back to buildings table
drop table if exists number_of_buildings;
create temporary table number_of_buildings
 select parcel_id, 
 	count(*) as number_of_buildings
 from buildings
 group by parcel_id;
 
alter table number_of_buildings add index prcl_index(parcel_id(10));

alter table buildings add column imputed_sqft double;
alter table buildings add column imputed_sqft_flag tinyint;
alter table buildings add index prcl_index(parcel_id(10));

drop table if exists allocate_sqft;
create temporary table allocate_sqft (parcel_id varchar(15), sqft double, number_of_buildings double, proportion double);

insert into allocate_sqft (parcel_id, sqft, number_of_buildings, proportion)
 select a.parcel_id, 
	a.imputed_sqft, 
 	b.number_of_buildings,
 	(a.imputed_sqft / b.number_of_buildings) as proportion
 from grouped_parcel_with_step_sqft a inner join number_of_buildings b on a.parcel_id = b.parcel_id
; 

alter table allocate_sqft add index prcl_index(parcel_id(10));

update buildings a inner join allocate_sqft b on a.parcel_id = b.parcel_id 
 set a.imputed_sqft = b.proportion;

update buildings set imputed_sqft_flag = 1 where imputed_sqft is not null;
 
## Find records that do not have buildings 

drop table if exists missing_building_records;
create table missing_building_records  
 select a.parcel_id,
 	a.sqft,
 	a.number_of_buildings,
 	a.proportion
 from allocate_sqft a 
 left join buildings b on a.parcel_id = b.parcel_id
 where b.parcel_id is null;

alter table missing_building_records add index prcl_index(parcel_id(10));

drop table if exists inserted_building_records;
create table inserted_building_records
 select a.parcel_id, 
 	a.sqft,
 	a.number_of_buildings,
 	a.proportion,
 	b.use_code,
 	b.generic_land_use_1, 
 	b.generic_land_use_2,
 	b.taxexempt_binary,
 	b.year_built
 from missing_building_records a inner join prelim_employers_to_parcels b
 on a.parcel_id = b.parcel_id
;

insert into buildings (parcel_id, building_use, year_built, imputed_sqft, imputed_sqft_flag)
 select parcel_id, generic_land_use_1, year_built, sqft, 2 as imputed_sqft_flag
 from inserted_building_records
; 

update buildings set imputed_sqft = built_sqft where imputed_sqft_flag is null;
 
 

 
 


