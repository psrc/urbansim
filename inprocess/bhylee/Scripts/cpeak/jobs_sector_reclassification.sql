###########################################################
#
#	This script reclassifies a jobs table previously
#		classified under the 15-sector job allocator sector 
#		scheme.  This reclassification was necessary
#		because the sectors that suited the job allocator
#		are not necessarily ideal for the final jobs table.  
#		This is becasue the sector_land_use_rates table is 
#		optimized by a close fit between sectors and 
#		land use, and the 18-sector classification (based
#		on the STEP classification) did not always provide
#		a good match for the job allocator. 
#	
#	The present script requires all the usual fields in the 
#		jobs table plus SIC.  This field was not always
#		populated because the data for the proprietors
#		was never provided with SIC number.  
#
#	Algorithm:
#		1. Jobs with SIC's are reclassified via the
#			sic_sector_id_mapping table.
#		2. Reclassify the sectors where there is 
#			a 1-to-1 or many-to-1 correspondence 
#			between the old sector id and a new
#			sector.
#		3. Stochastically reclassify jobs in each
#			sector-FAZ_group.  For each job of sector S, 
#			select a new sector N in accordance with
#			the probability of sector S being reclassified
#			into sector N, as observed in the previously-
#			reclassified jobs.
#			






##########
# Create table of jobs, noting those that are not
# classified by the sic_sector_id_mapping table.

create index sector_id on jobs (sector_id);

##########
#
# Create copy of jobs table, reclassifying the sector_id 
#	to that specified by the job's sic in the sic_sector_id_mapping table.
#
drop table if exists sectors_with_reclassification_status_primary;
create table sectors_with_reclassification_status_primary
select 
	a.job_id, 
	a.grid_id,
	a.sector_id,
	b.new_sector_id,
	a.home_based,
	a.sic
from 
	jobs a, sic_sector_id_mapping b
where
	a.sic between b.min_sic and b.max_sic
;

create index job_id 
	on sectors_with_reclassification_status_primary (job_id);

insert into sectors_with_reclassification_status_primary
(job_id, grid_id, sector_id, new_sector_id, home_based, sic)
select job_id, grid_id, sector_id, 14, home_based, sic
from jobs where sector_id = 4;

insert into sectors_with_reclassification_status_primary
(job_id, grid_id, sector_id, new_sector_id, home_based, sic)
select job_id, grid_id, sector_id, 15, home_based, sic
from jobs where sector_id = 5;

insert into sectors_with_reclassification_status_primary
(job_id, grid_id, sector_id, new_sector_id, home_based, sic)
select job_id, grid_id, sector_id, 16, home_based, sic
from jobs where sector_id = 3;

insert into sectors_with_reclassification_status_primary
(job_id, grid_id, sector_id, new_sector_id, home_based, sic)
select job_id, grid_id, sector_id, 17, home_based, sic
from jobs where sector_id = 14;

insert into sectors_with_reclassification_status_primary
(job_id, grid_id, sector_id, new_sector_id, home_based, sic)
select job_id, grid_id, sector_id, 18, home_based, sic
from jobs where sector_id = 11;

# Compare job sums by old sector_id
#   - pre reclass vs. post reclass
drop table if exists jobs_by_old_sector_all;
create temporary table jobs_by_old_sector_all
select sector_id, count(*) as jobcount
from jobs group by sector_id;

drop table if exists jobs_by_old_sector_partial;
create temporary table jobs_by_old_sector_partial
select sector_id, count(*) as jobcount
from sectors_with_reclassification_status_primary 
group by sector_id;

drop table if exists job_by_old_sector_comparisons;
create temporary table job_by_old_sector_comparisons
select a.sector_id, 
	a.jobcount as jobs_old_table,
	b.jobcount as jobs_new_table,
	b.jobcount - a.jobcount as job_change
from jobs_by_old_sector_all a inner join 
	jobs_by_old_sector_partial b on a.sector_id = b.sector_id
;

# mark records in jobs table that were not copied
#  add random number to be used in montecarlo sector selection
drop table if exists jobs_with_copy_status;
create temporary table jobs_with_copy_status
select
	a.*,
	b.new_sector_id, 
	rand() as rand_num
from jobs a left join sectors_with_reclassification_status_primary b
on a.job_id = b.job_id
;

# make all agriculture jobs -> resource
update jobs_with_copy_status
set new_sector_id = 1 where sector_id = 1;

# make all construction jobs -> construction
update jobs_with_copy_status
set new_sector_id = 2 where sector_id = 2;

# make all FIRES jobs -> FIRES
update jobs_with_copy_status
set new_sector_id = 10 where sector_id = 6;

# make all manufacturing -> Manufacturing - Other
# (assuming no proprietaror jobs in Manuf. - Aviation)
update jobs_with_copy_status
set new_sector_id = 4 where sector_id = 7;

# make all public admin jobs -> State and Local
update jobs_with_copy_status
set new_sector_id = 18 where sector_id = 8;

# make all wholesale trade -> wholesale trade.
update jobs_with_copy_status
set new_sector_id = 7  where sector_id = 13;

# make all mining -> resource.
update jobs_with_copy_status
set new_sector_id = 1  where sector_id = 15;


#########
# For un-reclassified jobs (due to coarse sectors in proprietors data),
#   get the proportion of old_sector-new_sector mappings by FAZ_group (?)
#   and use this to estimate converstions for the remaining jobs.

# Create table of sector reclassification rates by faz group.
drop table if exists jobs_by_faz_group_by_both_sectors;
create temporary table jobs_by_faz_group_by_both_sectors
select 
	a.sector_id,
	b.faz_group,
	a.new_sector_id,
	count(*) as job_count
from jobs_with_copy_status a
	inner join PSRC_2000_data_quality_indicators.gridcell_to_faz_group b
	on a.grid_id = b.grid_id
where sector_id in ( 9, 10, 12 )
group by 
	b.faz_group, 
	a.sector_id, 
	a.new_sector_id
;

# sum reclassified jobs by old_sector only
drop table if exists reclassed_jobs_by_old_sector;
create temporary table reclassed_jobs_by_old_sector
select
	faz_group,
	sector_id, 
	sum(job_count) as job_count
from jobs_by_faz_group_by_both_sectors
where new_sector_id is not null
group by faz_group, sector_id
;

# get proportion of jobs reclassed per faz_group-old_sector by new_sector
drop table if exists sector_reclass_rates;
create table sector_reclass_rates (
	inc int not null auto_increment,
	faz_group int,
	sector_id int,
	new_sector_id int,
	reclass_rate double(6,4),
	primary key (inc)
)
;

insert into sector_reclass_rates 
	(faz_group, sector_id, new_sector_id, reclass_rate)
select
	a.faz_group,
	a.sector_id,
	a.new_sector_id,
	a.job_count / b.job_count
from 
	jobs_by_faz_group_by_both_sectors a
	inner join reclassed_jobs_by_old_sector b
	on a.faz_group = b.faz_group and a.sector_id = b.sector_id
where a.new_sector_id is not null
;

# create cumulative distribution of rates per faz_group and sector_id
drop table if exists sector_reclass_cum_dists_1;
create table sector_reclass_cum_dists_1
select
	a.inc,
	a.faz_group,
	a.sector_id,
	a.new_sector_id,
	a.reclass_rate,
	sum(b.reclass_rate) as cumulative_dist
from sector_reclass_rates a, sector_reclass_rates b
where 
	a.faz_group = b.faz_group 
	and a.sector_id = b.sector_id
	and a.inc >= b.inc
group by a.inc;

drop table if exists sector_reclass_cum_dists;
create table sector_reclass_cum_dists
select 
	a.inc,
	a.faz_group,
	a.sector_id, 
	a.new_sector_id, 
	a.reclass_rate, 
	b.cumulative_dist as cumulative_dist_min,
	a.cumulative_dist as cumulative_dist_max
from sector_reclass_cum_dists_1 a,
	sector_reclass_cum_dists_1 b
where a.inc = b.inc + 1
;

insert into sector_reclass_cum_dists
	(inc, faz_group, sector_id, new_sector_id, reclass_rate, 
	cumulative_dist_min, cumulative_dist_max)
select
	1, faz_group, sector_id, new_sector_id, reclass_rate, 
	0, cumulative_dist
from sector_reclass_cum_dists_1
where inc = 1
;
	
update sector_reclass_cum_dists 
set cumulative_dist_min = 0 
where cumulative_dist_min >= 1
;

# update sector_reclass_cum_dists 
#  set cumulative_dist_max = 1 
#  where cumulative_dist_max >= 0

# Temporary fix 
 update sector_reclass_cum_dists 
 set cumulative_dist_min = 0 
 where cumulative_dist_min > cumulative_dist_max;
# update sector_reclass_cum_dists set cumulative_dist_max = 1 where cumulative_dist_max > cumulative_dist_min;

create index faz_sector_id on sector_reclass_cum_dists 
	(faz_group, sector_id);
create index grid_id on jobs_with_copy_status (grid_id);
create index sector_id on jobs_with_copy_status (sector_id);

drop table if exists jobs_all_sectors_reclassified;
create table jobs_all_sectors_reclassified
select
	a.job_id,
	a.grid_id,
	a.sic,
	a.sector_id,
	a.new_sector_id,
	a.home_based,
	a.job_allocator,
	a.proprietor,
	ifnull(a.new_sector_id, c.new_sector_id) as new_new_sector_id
from
	jobs_with_copy_status a
	left join PSRC_2000_data_quality_indicators.gridcell_to_faz_group b
	on a.grid_id = b.grid_id
	left join sector_reclass_cum_dists c
	on b.faz_group = c.faz_group 
	and a.sector_id = c.sector_id
where ((a.rand_num between c.cumulative_dist_min and c.cumulative_dist_max)
	or c.cumulative_dist_max is null)
;
	
create index job_id on jobs_all_sectors_reclassified (job_id);
# find distributions of un-reclassified jobs among previous sectors.

#####
#
#  CREATE THE NEW jobs TABLE!!
#
drop table if exists jobs;
create table jobs 
select
	job_id, 
	grid_id,
	new_new_sector_id as sector_id,
	home_based,
	sic
from jobs_all_sectors_reclassified
;

create index job_id on jobs (job_id);
create index grid_id on jobs (grid_id);
create index sector_id on jobs (sector_id);

############# temp ###################
drop table if exists c;
create temporary table jobs_lost
select 
	a.*,
	b.job_id as job_id_null_possible
from jobs_with_copy_status a
	left join jobs b
	on a.job_id = b.job_id
having job_id_null_possible is null
;

alter table jobs_lost add index grid_indx(grid_id);
### Find the correct sector_id for unplaced jobs from jobs_lost table ###

# search jobs_lost table for faz_group and sector_id (this will be different for each reclassification run)
# select * from PSRC_2000_data_quality_indicators.gridcell_to_faz_group where grid_id in
# ( 841397, 962683, 1077069, 377098, 513053);
# find faz_groups
 
# select * from sector_reclass_cum_dists where faz_group in (12, 3, 6) and sector_id in(10);
 
### insert jobs_lost back into jobs_all_sectors_reclassified ###

# insert into jobs_new (job_id, grid_id, sic, sector_id, new_sector_id, home_based, new_new_sector_id)
#  select job_id, grid_id, sic, sector_id, new_sector_id, home_based, 13
#  from jobs_lost
#  where job_id = 1172334
# ;

# insert into jobs_new (job_id, grid_id, sic, sector_id, new_sector_id, home_based, new_new_sector_id)
#  select job_id, grid_id, sic, sector_id, new_sector_id, home_based, 13
#  from jobs_lost
#  where job_id = 1351372
# ;

# insert into jobs_new (job_id, grid_id, sic, sector_id, new_sector_id, home_based, new_new_sector_id)
#  select job_id, grid_id, sic, sector_id, new_sector_id, home_based, 13
#  from jobs_lost
#  where job_id = 1351964
# ;

# insert into jobs_new (job_id, grid_id, sic, sector_id, new_sector_id, home_based, new_new_sector_id)
#  select job_id, grid_id, sic, sector_id, new_sector_id, home_based, 13
#  from jobs_lost
#  where job_id = 1661429
# ;

# insert into jobs_new (job_id, grid_id, sic, sector_id, new_sector_id, home_based, new_new_sector_id)
#  select job_id, grid_id, sic, sector_id, new_sector_id, home_based, 13
#  from jobs_lost
#  where job_id = 1784002
# ;


### Create new jobs table with reclassified sector_id ###

# create table jobs_new select * from jobs_all_sectors_reclassified;

# update jobs_new set sector_id = null;
# update jobs_new set sector_id = new_sector_id;
# update jobs_new set sector_id = new_new_sector_id where sector_id is null;

# alter table jobs_new drop column new_sector_id;
# alter table jobs_new drop column new_new_sector_id;