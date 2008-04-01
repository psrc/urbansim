


#CREATE INDEX pin_indx on parcel_fractions_in_gridcells (PARCEL_ID(10)); 
#CREATE INDEX pin_indx ON DISTRIBUTED_JOBS (PARCEL_ID(10));

CREATE temporary TABLE jobs_gridcells_1
SELECT 
	a.GRID_ID, 
	a.PARCEL_ID,
	b.SECTOR, 
	b.HOMEBASED, 
	a.PARCEL_FRACTION,
	round(a.PARCEL_FRACTION) AS JOB
FROM parcel_fractions_in_gridcells a INNER JOIN DISTRIBUTED_JOBS b
	ON a.parcel_id = b.parcel_id
;

CREATE INDEX my_indx ON jobs_gridcells_1 (GRID_ID, PARCEL_ID(10), SECTOR);

DROP TABLE IF EXISTS JOBS_ROUNDED;
CREATE TABLE JOBS_ROUNDED (
	JOB_ID INT AUTO_INCREMENT PRIMARY KEY,
	GRID_ID INT,
	SECTOR INT, 
	HOME_BASED TINYINT
);

INSERT INTO JOBS_ROUNDED (GRID_ID, SECTOR, HOME_BASED)
SELECT GRID_ID, SECTOR, HOMEBASED 
FROM jobs_gridcells_1
WHERE JOB = 1;


#Jobs rounded is now a first aproximation of a jobs table constructed from proprietors.  It will probably 
 # be missing jobs due to rounding errors from the parcel_fracitons_in_gridcells table.

#The table jobs_lost_in_translation, generated by the following set of queries, shows the number of jobs
#  that are falling through the parcel-to-gridcell mapping process.  These will have to be allocated using a 
 # Montecarlo process.
#*/

CREATE TEMPORARY TABLE total_distributed_jobs_by_parcel
SELECT PARCEL_ID, SECTOR, HOMEBASED, COUNT(*) AS JOBS
FROM DISTRIBUTED_JOBS
GROUP BY PARCEL_ID, SECTOR, HOMEBASED;

CREATE TEMPORARY TABLE jobs_on_gridcells
SELECT parcel_id, sector, homebased, sum(job) AS jobs_remaining
FROM jobs_gridcells_1
GROUP BY parcel_id, sector, homebased;

alter table total_distributed_jobs_by_parcel add column key_col varchar(30);
alter table jobs_on_gridcells add column key_col varchar(30);
update total_distributed_jobs_by_parcel set key_col = concat(parcel_id, "_", sector, "_", homebased);
update jobs_on_gridcells set key_col = concat(parcel_id, "_", sector, "_", homebased);
create unique index key_col_indx on total_distributed_jobs_by_parcel(key_col(17));
create unique index key_col_indx on jobs_on_gridcells (key_col(17));

DROP TABLE IF EXISTS jobs_lost_in_translation;

CREATE TABLE jobs_lost_in_translation
select a.*, ifnull(b.jobs_remaining,0) as jobs_remaining
from total_distributed_jobs_by_parcel a left join jobs_on_gridcells b 
on a.key_col = b.key_col;

alter table jobs_lost_in_translation add column jobs_lost int;
update jobs_lost_in_translation set jobs_lost = jobs - jobs_remaining;


