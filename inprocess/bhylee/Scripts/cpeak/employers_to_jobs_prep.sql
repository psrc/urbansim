##########################################################
### This script to be accessed through employers_to_jobs.pl

drop table if exists tmp_employers_1;
drop table if exists tmp_employers_2;
drop table if exists tmp_employers_3;
drop table if exists tmp_employers_4;
drop table if exists largest_parcel_fracs;
drop table if exists unplaced_jobs;


CREATE TABLE tmp_employers_1 
select 
	a.employer_id, 
	a.parcel_id, 
	c.SECTOR_CODE AS SECTOR
FROM (final_employers_matched_to_parcels as a 
	INNER JOIN employers as b ON a.employer_id = b.employer_id) 
	INNER JOIN division_sectors as c ON b.SECTOR = c.sector;
	

ALTER TABLE tmp_employers_1 add column home_based smallint;

ALTER TABLE tmp_employers_1 ADD INDEX (parcel_id(10));

UPDATE tmp_employers_1 as a 
	INNER JOIN parcels as b ON a.parcel_id = b.parcel_id 
	INNER JOIN PSRC_2000_reclassification_tables.land_use_generic_reclass c
	 ON b.county = c.county and b.use_code = c.county_land_use_code
SET a.home_based = 1 
WHERE c.generic_land_use_2 in ('R','GQ')
	AND a.sector not in (3,4,5,11,14)	
;


CREATE TABLE tmp_employers_2 
SELECT 
	a.parcel_id, 
	b.employer_id, 
	a.grid_id, 
	a.parcel_fraction, 
	b.sector, 
	b.home_based 
FROM parcel_fractions_in_gridcells AS a 
	INNER JOIN tmp_employers_1 AS b ON a.parcel_id = b.parcel_id;

ALTER TABLE tmp_employers_2 ADD INDEX (employer_id(10));

CREATE TABLE tmp_employers_3 
SELECT 
	a.parcel_id, 
	a.grid_id, 
	a.sector, 
	IFNULL(a.home_based,0) as home_based, 
	(b.number_of_jobs * a.parcel_fraction) AS job_count,
	b.sic
FROM tmp_employers_2 AS a 
	INNER JOIN employers AS b ON a.employer_id = b.employer_id;

ALTER TABLE tmp_employers_3 add column job_count_rounded int;

UPDATE tmp_employers_3
SET job_count_rounded = round(job_count);

alter table tmp_employers_3 add column rec_number INT AUTO_INCREMENT primary key;

DROP TABLE if exists tmp_employers_4;



################################################
# This section of the script allocates jobs that would otherwise "fall through
#  the cracks" due to rounding errors.  It finds all those round-off errors and
#  the parcels they correspond to, and allocates them to the largest 
#  fraction of that parcel.  If there are two equally large parcel fractions
#  (which is rare), it allocates the jobs to the grid cell with the highest 
#  grid_id.  

#- find the largest parcel_fraction per parcel

alter table tmp_employers_3 add index parcelid_indx (parcel_id(10));

create table largest_parcel_fracs
select 
	parcel_id, 
	rec_number,
	max(grid_id) as max_grid_id,
	max(job_count) as max_job_count
from tmp_employers_3
where job_count > 0 
group by parcel_id;

#- find the difference between allocated and total jobs per parcel_id
create table unplaced_jobs
select 
	parcel_id, 
	sum(job_count) as total_jobs,
	sum(job_count_rounded) as placed_jobs, 
	round(sum(job_count) - sum(job_count_rounded)) as difference
from tmp_employers_3
group by parcel_id
having difference > 0;

# attribute remainder jobs to polygon with largest area (or job_count)
update (unplaced_jobs a
	inner join largest_parcel_fracs b on a.parcel_id = b.parcel_id)
	inner join tmp_employers_3 c on b.rec_number = c.rec_number
set c.job_count_rounded = c.job_count_rounded + a.difference;

#########################################################################

CREATE TABLE tmp_employers_4 
SELECT 
	grid_id, 
	sector, 
	home_based, 
	sum(job_count_rounded) as jobs, 
	sic 
FROM tmp_employers_3 
GROUP BY grid_id, sector, home_based;


#drop table tmp_employers_1;
#drop table tmp_employers_2;
#drop table tmp_employers_3;