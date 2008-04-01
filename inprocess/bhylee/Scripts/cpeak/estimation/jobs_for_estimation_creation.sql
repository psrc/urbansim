#####################
#
#	This script creates the table jobs_for_estimation
#		from the jobs table.  The output table contains 
#		only jobs in sectors 1 - 13, and samples them by
#		TAZ in proportion to the number of jobs in that 
#		sector-TAZ that had been added since 1995.  
#


use PSRC_jobs_for_estimation_creation;

# get urbansim_sector per employer
drop table if exists emp00_with_sector;
create temporary table emp00_with_sector
select
	a.jobs00 as jobs,
	a.id as zone,
	a.sic,
	b.sector_code
from emp00 a inner join sic_urbansim_sectors b
	on a.sic = b.sic
;

drop table if exists emp95_with_sector;
create temporary table emp95_with_sector
select
	a.jobs95 as jobs,
	a.id as zone,
	a.sic,
	b.sector_code
from emp95 a inner join sic_urbansim_sectors b
	on a.sic = b.sic
;

# summarize jobs by zone and sector
drop table if exists jobs_per_zone_sector_95;
create temporary table jobs_per_zone_sector_95
select 
	sector_code,
	zone,
	sum(jobs) as jobs
from emp95_with_sector
group by sector_code, zone;

drop table if exists jobs_per_zone_sector_00;
create temporary table jobs_per_zone_sector_00
select 
	sector_code,
	zone,
	sum(jobs) as jobs
from emp00_with_sector
group by sector_code, zone;

create unique index sector_zone on jobs_per_zone_sector_95 (sector_code, zone);
create unique index sector_zone on jobs_per_zone_sector_00 (sector_code, zone);

# Create p values per sector-zone
drop table if exists p_values_per_zone_sector;
create table p_values_per_zone_sector
select
	a.sector_code,
	a.zone,
	a.jobs as jobs00,
	ifnull(b.jobs,0) as jobs95,
	a.jobs - ifnull(b.jobs,0) as job_dif,
	if(a.jobs<b.jobs, 0, a.jobs - ifnull(b.jobs,0)) as job_dif_no_neg,
	ifnull((if(a.jobs<b.jobs, 0, a.jobs - ifnull(b.jobs,0)))/a.jobs*1000/1000,0) as p
from
	jobs_per_zone_sector_00 a
	left join jobs_per_zone_sector_95 b
	on a.sector_code = b.sector_code and a.zone = b.zone
;

# create index sector on p_values_per_zone_sector (sector);
# create index zone on p_values_per_zone_sector (zone);
create index zone_sector on p_values_per_zone_sector (zone, sector);

#  Affix p value to jobs table
drop table if exists jobs_with_zone_and_p;
create temporary table jobs_with_zone_and_p
select 	
	a.job_id,
	a.grid_id,
	a.sector_id,
	a.home_based,
	b.zone_id,
	c.p, 
	rand() as rand_num, 
	0 as chosen
from
	PSRC_2000_baseyear.jobs a
	inner join PSRC_2000_baseyear.gridcells b 
	on a.grid_id = b.grid_id
	inner join p_values_per_zone_sector c 
	on b.zone_id = c.zone and a.sector_id = c.sector_code
;

# Choose jobs whenever the random number < the p value 
#   for that job's sector-zone.
drop table if exists jobs_for_estimation_primary;
CREATE TABLE jobs_for_estimation_primary
select 
	job_id,
	grid_id,
	sector_id,
	home_based
from jobs_with_zone_and_p 
where rand_num < p
;
	

