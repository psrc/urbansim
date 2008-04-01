
# Creates back-up tables for existing input proprietor distributor input tables for new runs

alter table PARCELS rename as PARCELS_bak_peter_3_15_04;
alter table JOBS_PER_COUNTY rename as JOBS_PER_COUNTY_bak_peter_3_15_04;
alter table JOBS_ROUNDED rename as JOBS_ROUNDED_bak_peter_3_15_04;
alter table DISTRIBUTED_JOBS rename as DISTRIBUTED_JOBS_bak_peter_3_15_04;

# Insert indices on the following tables.

alter table PARCELS add unique index cnty_pin_indx (county(3), parcel_id(10));
alter table PARCELS add unique index pin_indx (parcel_id(11));
alter table PARCELS add index blk_indx (census_block(15));
alter table PARCELS add index lu_fg_indx (generic_land_use_1(10), faz_group(2));
alter table PARCELS add index zone_indx (zone);
alter table PARCELS add index lu_2_indx (generic_land_use_2(1));

alter table SECTOR_LAND_USE_WEIGHTS add index lu_fg_2_indx(land_use(10), faz_group(2));

alter table parcel_fractions_in_gridcells add index pin_indx (parcel_id(12));

###############################################################################
# Get the total jobs by sector from the leftovers from the job allocator
# Be sure to change the database name.

create table job_allocator_placed
select 
	a.county, 
	a.sector,
	c.sector_code,
	sum(a.number_of_jobs) as ALLOCATED_JOBS
from job_allocation_king.employers a
	inner join job_allocation_king.final_employers_matched_to_parcels b
	on (a.employer_id = b.employer_id)
	inner join job_allocation_king.division_sectors as c
	on a.sector = c.sector
where b.decision not in ('NO_PARCEL_IN_BLOCK', 'WRONG_SIDE_OF_STREET', 'WRONG_STREET_TYPE_FOR_BLOCK')
GROUP BY a.county, a.sector, c.sector_code;

# Update the JOBS_PER_COUNTY table with new wage and salary figures
# Be sure to create preliminary wage and salary table (control_totals_by_sector) from spreadsheet

update JOBS_PER_COUNTY as a inner join control_totals_by_sector as b 
 on a.sector = b.sector_code set a.wagesal_totals = b.job_sum;

#Update the JOBS_PER_COUNTY table with new proprietor figures

update JOBS_PER_COUNTY as a inner join proprietor_totals as b 
 on a.sector = b.sector_code set a.proprietors_jobs = b.proprietor_jobs;
 
# Update the JOBS_PER_COUNTY table with allocated jobs from job_allocation process

update JOBS_PER_COUNTY as a inner join tmp_job_allocator_placed as b
 on a.sector = b.sector_code set a.allocated_jobs = b.allocated_jobs;

# Update the JOBS_PER_COUNTY table's field TOTAL_COUNTY_JOBS using the expression: wagesal-allocated + proprietor.
update JOBS_PER_COUNTY set TOTAL_COUNTY_JOBS = ((wagesal_totals - allocated_jobs) + proprietors_jobs);

update JOBS_PER_COUNTY set TOTAL_COUNTY_JOBS = 0 where TOTAL_COUNTY_JOBS like "-%";

# Create PARCELS table from job_allocation_countyname database (includes 2001 parcel records, but not 2001 building records).

CREATE TABLE blocks select distinct census_block, county, taz, maz_num, taz_all, maz, zone
 from PSRC_proprietors_distributor_kitsap.blocks;

CREATE INDEX blk_indx ON blocks (census_block);

ALTER TABLE blocks add column ZONE varchar(6);
UPDATE blocks set zone = taz where county in ('033', '035', '053');
UPDATE blocks set zone = maz where county = '061';

# Create the parcels table with most of the fields
CREATE TEMPORARY TABLE PARCELS1
SELECT
	a.COUNTY,
	a.PARCEL_ID,
	a.USE_CODE as LAND_USE,
	0 AS JOB_COUNT,
	a.SQUARE_FOOTAGE AS SQFT,
	b.GENERIC_LAND_USE_1,
	b.GENERIC_LAND_USE_2,
	c.TAXEXEMPT_BINARY AS TAX_EXEMPT
FROM job_allocation_king.parcels a 
	INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass b
	ON (a.county = b.county and a.use_code = b.county_land_use_code)
	INNER JOIN PSRC_parcels_king.parcels AS c
	ON (a.parcel_id = c.parcel_id);
	

ALTER TABLE PARCELS1 ADD INDEX prcl_indx(parcel_id(10));	
 	
# get the remaining fields for the parcels table
CREATE TEMPORARY TABLE PARCELS2
SELECT 
	a.*,
	b.CENSUS_BLOCK
FROM PARCELS1 a INNER JOIN job_allocation_king.parcels b
	ON a.parcel_id = b.parcel_id;

CREATE INDEX blk_indx ON PARCELS2 (CENSUS_BLOCK(15));

CREATE TEMPORARY TABLE PARCELS3
SELECT 	
	a.*,
	b.FAZ_GROUP
FROM PARCELS2 a INNER JOIN job_allocation_king.census_blocks b
	on a.census_block = b.census_block;


CREATE TABLE PARCELS
SELECT 
	a.*,
	b.ZONE
FROM PARCELS3 a INNER JOIN PSRC_proprietors_distributor_king.blocks b ON a.census_block = b.census_block;

#########################################################################################################
# scratch queries
#
#


select sum(a.number_of_jobs) as jobs from employers a inner join final_employers_matched_to_parcels_bak_peter_3_13_04 b 
on a.employer_id = b.employer_id where 
b.decision not in ('NO_PARCEL_IN_BLOCK', 'WRONG_SIDE_OF_STREET', 'WRONG_STREET_TYPE_FOR_BLOCK'); and
b.parcel_id in ('8590400755', '8590400750', '8590400530', '8590400535', '8590400525', '8590400785', '8590400540', '8590400545', '9821700010');

create table tmp_allocated_jobs_per_taz_3_16_04
select c.taz_int as TAZ, sum(a.number_of_jobs) as JOBS from employers a inner join final_employers_matched_to_parcels b 
on (a.employer_id = b.employer_id) inner join PSRC_2000_data_quality_indicator_maps.block_faz_and_taz c
on b.census_block = c.census_block 
where b.decision not in ('NO_PARCEL_IN_BLOCK', 'WRONG_SIDE_OF_STREET', 'WRONG_STREET_TYPE_FOR_BLOCK') and c.taz_int in (125, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149)
group by c.taz order by taz_int asc
;


select sum(a.number_of_jobs) as jobs from employers a inner join final_employers_matched_to_parcels_bak_peter_3_12_04 b
on (a.employer_id = b.employer_id) inner join PSRC_2000_data_quality_indicator_maps.block_faz_and_taz c
on b.census_block = c.census_block where c.taz_int = 125 and b.decision not in ('NO_PARCEL_IN_BLOCK', 'WRONG_SIDE_OF_STREET', 'WRONG_STREET_TYPE_FOR_BLOCK');

select a.census_block from final_employers_matched_to_parcels a 
inner join PSRC_2000_data_quality_indicator_maps.block_faz_and_taz b
on a.census_block = b.census_block where b.taz_int = 149 
group by a.census_block;

select sum(number_of_jobs) from employers where census_block in ('530330085001008', '530330085001009', '530330085001010');

create table employers_geocoded_to_parcels
select a.EMPLOYER_ID, 
       a.SECTOR, 
       a.NUMBER_OF_JOBS, 
       a.GEOCODING_RESOURCE as PSRC_GEOCODING_RESOURCE,
       a.SIC, 
       a.COUNTY, 
       b.PARCEL_ID, 
       b.CENSUS_BLOCK,
       c.TAZ_INT as TAZ,
       b.DECISION as URBANSIM_DECISION       
from employers a inner join employers_matched_to_parcels b on (a.employer_id = b.employer_id)
inner join PSRC_2000_data_quality_indicator_maps.block_faz_and_taz c on b.census_block = c.census_block
where b.decision in ('PSRC_MATCHED', 'URBANSIM_MANUAL_MATCHED', 'URBANSIM_MANUAL_MATCHED_2')
;

create table county_employers_geocoded_to_parcels_mhs
(EMPLOYER_ID TEXT, SECTOR TEXT, NUMBER_OF_JOBS DOUBLE, PSRC_GEOCODING_RESOURCE TEXT, SIC TEXT, COUNTY VARCHAR(4), 
PARCEL_ID TEXT, CENSUS_BLOCK TEXT, TAZ INT(11), URBANSIM_DECISION TEXT);

insert into county_employers_geocoded_to_parcels_mhs (EMPLOYER_ID, SECTOR, NUMBER_OF_JOBS, PSRC_GEOCODING_RESOURCE, 
SIC, COUNTY, PARCEL_ID, CENSUS_BLOCK, TAZ, URBANSIM_DECISION) 
select EMPLOYER_ID, SECTOR, NUMBER_OF_JOBS, PSRC_GEOCODING_RESOURCE, SIC, COUNTY, PARCEL_ID, CENSUS_BLOCK, TAZ, URBANSIM_DECISION
from job_allocation_king.employers_geocoded_to_parcels;

insert into county_employers_geocoded_to_parcels_mhs (EMPLOYER_ID, SECTOR, NUMBER_OF_JOBS, PSRC_GEOCODING_RESOURCE, 
SIC, COUNTY, PARCEL_ID, CENSUS_BLOCK, TAZ, URBANSIM_DECISION) 
select EMPLOYER_ID, SECTOR, NUMBER_OF_JOBS, PSRC_GEOCODING_RESOURCE, SIC, COUNTY, PARCEL_ID, CENSUS_BLOCK, TAZ, URBANSIM_DECISION
from job_allocation_kitsap.employers_geocoded_to_parcels;

insert into county_employers_geocoded_to_parcels_mhs (EMPLOYER_ID, SECTOR, NUMBER_OF_JOBS, PSRC_GEOCODING_RESOURCE, 
SIC, COUNTY, PARCEL_ID, CENSUS_BLOCK, TAZ, URBANSIM_DECISION) 
select EMPLOYER_ID, SECTOR, NUMBER_OF_JOBS, PSRC_GEOCODING_RESOURCE, SIC, COUNTY, PARCEL_ID, CENSUS_BLOCK, TAZ, URBANSIM_DECISION
from job_allocation_pierce.employers_geocoded_to_parcels;

insert into county_employers_geocoded_to_parcels_mhs (EMPLOYER_ID, SECTOR, NUMBER_OF_JOBS, PSRC_GEOCODING_RESOURCE, 
SIC, COUNTY, PARCEL_ID, CENSUS_BLOCK, TAZ, URBANSIM_DECISION) 
select EMPLOYER_ID, SECTOR, NUMBER_OF_JOBS, PSRC_GEOCODING_RESOURCE, SIC, COUNTY, PARCEL_ID, CENSUS_BLOCK, TAZ, URBANSIM_DECISION
from job_allocation_snohomish.employers_geocoded_to_parcels;

create table county_employers_geocoded_to_prcl_at_taz 
select TAZ, sum(number_of_jobs) as JOBS from county_employers_geocoded_to_parcels_mhs
group by TAZ;

#############################################
#
#
create temporary table tmp_parcels_commercial
select a.* from parcels a 
inner join PSRC_2000_data_quality_indicators.land_use_generic_reclass b 
on a.county = b.county and a.land_use = b.county_land_use_code where b.generic_land_use_1 = 'commercial';

create temporary table tmp_parcels_residential 
select a.* from parcels a inner join PSRC_2000_data_quality_indicators.land_use_generic_reclass b 
on a.county = b.county and a.land_use = b.county_land_use_code where b.generic_land_use_2 = 'R';

alter table tmp_parcels_commerical add unique index prcl_indx(parcel_id(7));
alter table tmp_parcels_residential add unique index prcl_indx(parcel_id(7));

#############################################
#PSRC census block to taz mapping scheme:
#

#jobs table
create table tmp_jobs_in_tz00bk00
select c.TAZ, sum(a.job_count_rounded) as JOBS from tmp_employers_3 a inner join parcels b
inner join tz00bk00 c on b.census_block = c.stfid group by c.taz;

create table tmp_proprietor_jobs_in_tz00bk00
select c.TAZ, count(*) as JOBS from DISTRIBUTED_JOBS a 
inner join PARCELS b on (a.parcel_id = b.parcel_id) 
inner join job_allocation_king.tz00bk00 c on c.stfid = b.census_block
group by c.TAZ;

#final_employers_matched_to_parcels table
create table tmp_prcl_jobs_in_tz00bk00
select c.TAZ, sum(a.number_of_jobs) as JOBS from employers a inner join final_employers_matched_to_parcels b
on (a.employer_id = b.employer_id)
inner join tz00bk00 c on b.census_block = c.stfid where b.decision not in ('NO_PARCEL_IN_BLOCK', 'WRONG_SIDE_OF_STREET', 'WRONG_STREET_TYPE_FOR_BLOCK') 
group by c.TAZ;

drop table tmp_jobs_in_tz00bk00;
drop table tmp_proprietor_jobs_in_tz00bk00;

UW census block to taz mapping scheme:

create table tmp_jobs_in_uw_taz
select c.TAZ, sum(a.job_count_rounded) as JOBS from tmp_employers_3 a inner join parcels b
on (a.parcel_id = b.parcel_id)
inner join PSRC_2000_data_quality_indicator_maps.block_faz_and_taz c 
on b.census_block = c.census_block group by c.taz;


###########################################
# Create table containing jobs counts pre-job allocator, post job allocator, and post proprietor distributor by TAZ
# Requested by Mark Simonson 3.24.04

# Job from parcel to taz
create table jobs_placed_pre_job_allocator_parcel_to_taz
select c.TAZ, sum(a.number_of_jobs) as JOBS from employers a 
inner join employers_matched_to_parcels b 
on (a.employer_id = b.employer_id)
inner join PSRC_2000_data_quality_indicator_maps.block_faz_and_taz c
on b.census_block = c.census_block
where b.decision in ('PSRC_MATCHED', 'URBANSIM_MANUAL_MATCHED', 'URBANSIM_MANUAL_MATCHED_2')
group by c.TAZ;

create table jobs_placed_post_job_allocator_parcel_to_taz
select c.TAZ, sum(a.number_of_jobs) as JOBS from employers a 
inner join final_employers_matched_to_parcels b
on (a.employer_id = b.employer_id)
inner join PSRC_2000_data_quality_indicator_maps.block_faz_and_taz c
on b.census_block = c.census_block
where b.decision not in ('NO_PARCEL_IN_BLOCK', 'WRONG_SIDE_OF_STREET', 'WRONG_STREET_TYPE_FOR_BLOCK')
group by c.TAZ;

# Jobs from gridcell to taz
create table jobs_placed_post_job_allocator_gridcell_to_taz
select b.ZONE_ID as TAZ, count(*) as JOBS from jobs a 
inner join PSRC_2000_baseyear.gridcells b 
on a.grid_id = b.grid_id group by b.zone_id;

# Get Proprietor Jobs to taz
# Jobs at parcel to taz
create table jobs_placed_post_proprietor_parcel_to_taz
select c.TAZ, count(*) as JOBS from DISTRIBUTED_JOBS a 
inner join PARCELS b on (a.parcel_id = b.parcel_id)
inner join PSRC_2000_data_quality_indicator_maps.block_faz_and_taz c on b.census_block = c.census_block
group by c.taz;

# Jobs at gridcell to taz
create table jobs_placed_post_proprietor_gridcell_to_taz
select b.ZONE_ID as TAZ, count(*) as JOBS from JOBS_ROUNDED a 
inner join PSRC_2000_baseyear.gridcells b 
on (a.grid_id = b.grid_id)
group by b.ZONE_ID;

#drop table jobs_placed_pre_job_allocator_parcel_to_taz;
#drop table jobs_placed_post_job_allocator_parcel_to_taz;
#drop table jobs_placed_post_job_allocator_gridcell_to_taz;
#drop table jobs_placed_post_proprietor_parcel_to_taz;
#drop table jobs_placed_post_proprietor_gridcell_to_taz;

# Pathname for running DQIUpdated.pl perl script must be in Liming Wang's directory in order to run query. 
(perl DQIUpdate.pl -w /projects/urbansim7/users/cpeak/DataQuality/exported_indicators/ -U urbansim -P UrbAnsIm4Us -u -t -v > ~/pd_DQI.out) >& ~/pd_DQI.err &

