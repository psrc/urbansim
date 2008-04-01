/* To be run after all jobs tables are constructed for each county
in both the job_allocator and proprietors_distributor databases.
*/

use PSRC_2000_baseyear;

DROP TABLE IF EXISTS jobs_bak;

RENAME TABLE jobs to jobs_bak;

CREATE TABLE jobs (
	JOB_ID INT AUTO_INCREMENT PRIMARY KEY,
	GRID_ID INT,
	SECTOR INT, 
	HOME_BASED TINYINT,
	SIC INT
);

INSERT INTO jobs (GRID_ID, SECTOR, HOME_BASED)
SELECT GRID_ID, SECTOR, HOME_BASED
FROM PSRC_proprietors_distributor_king.JOBS_ROUNDED;

INSERT INTO jobs (GRID_ID, SECTOR, HOME_BASED, SIC)
SELECT GRID_ID, SECTOR, HOME_BASED, SIC
FROM job_allocation_king.jobs;

INSERT INTO jobs (GRID_ID, SECTOR, HOME_BASED)
SELECT GRID_ID, SECTOR, HOME_BASED
FROM PSRC_proprietors_distributor_kitsap.JOBS_ROUNDED;

INSERT INTO jobs (GRID_ID, SECTOR, HOME_BASED, SIC)
SELECT GRID_ID, SECTOR, HOME_BASED, SIC
FROM job_allocation_kitsap.jobs;

INSERT INTO jobs (GRID_ID, SECTOR, HOME_BASED)
SELECT GRID_ID, SECTOR, HOME_BASED
FROM PSRC_proprietors_distributor_pierce.JOBS_ROUNDED;

INSERT INTO jobs (GRID_ID, SECTOR, HOME_BASED, SIC)
SELECT GRID_ID, SECTOR, HOME_BASED, SIC
FROM job_allocation_pierce.jobs;

INSERT INTO jobs (GRID_ID, SECTOR, HOME_BASED)
SELECT GRID_ID, SECTOR, HOME_BASED
FROM PSRC_proprietors_distributor_snohomish.JOBS_ROUNDED;

INSERT INTO jobs (GRID_ID, SECTOR, HOME_BASED, SIC)
SELECT GRID_ID, SECTOR, HOME_BASED, SIC
FROM job_allocation_snohomish.jobs;