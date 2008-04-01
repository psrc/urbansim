# To minimize computation time, select only the bookend years

CREATE TABLE households_exported_97_98_30 
SELECT * FROM households_exported 
WHERE year=1997
OR year=1998
OR year=2030;

CREATE TABLE jobs_exported_97_98_30 
SELECT * FROM jobs_exported 
WHERE year=1997
OR year=1998
OR year=2030;

CREATE TABLE gridcells_exported_97_98_30 
SELECT * FROM gridcells_exported 
WHERE year=1997
OR year=1998
OR year=2030;

# Match households_constants to households_exported

CREATE TABLE households_97_98_30
SELECT hh_e.year AS year, 
hh_e.household_id AS household_id, 
hh_e.grid_id AS grid_id, 
hh_e.zone_id AS zone_id,
hh_c.persons AS persons,
hh_c.workers AS workers,
hh_c.age_of_head AS age_of_head,
hh_c.income AS income,
hh_c.children AS children,
hh_c.race_id AS race_id
FROM households_exported AS hh_e INNER JOIN households_constants AS hh_c
ON hh_e.household_id=hh_c.household_id

# Match jobs_constants to jobs_exported

CREATE TABLE jobs_97_98_30
SELECT j_e.year AS year,
j_e.job_id AS job_id,
j_e.grid_id AS grid_id,
j_e.home_based AS home_based,
j_e.zone_id AS zone_id