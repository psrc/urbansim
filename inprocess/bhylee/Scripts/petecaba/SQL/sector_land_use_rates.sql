# Inputs:
#	employers_parcels_preliminary_identity
#		Fields: number_of_jobs, faz, sic, county, land_use_code, resource
#	faz_groups
#		faz, faz_group
#	Sector_reclass
#		division, sic
#	land_use_generic_reclass

ALTER TABLE faz_groups add index (faz);
ALTER TABLE faz_groups add index (faz_group);

ALTER TABLE sector_reclass add index (sic);
ALTER TABLE sector_reclass add index (division (20));

ALTER TABLE land_use_generic_reclass add index (county(3));
ALTER TABLE land_use_generic_reclass add index (county_land_use_code);

CREATE TEMPORARY TABLE jobs_by_fy_division_lu_1
SELECT b.faz_group as summary_area, c.division as division,
d.generic_land_use_1 as land_use, sum(a.number_of_jobs) as jobs
from ((employers_parcels_preliminary_identity as a 
INNER JOIN faz_groups as b on a.faz = b.faz) 
INNER JOIN sector_reclass as c on a.sic = c.sic)
INNER JOIN land_use_generic_reclass as d
on a.county = d.county and a.land_use_code = d.county_land_use_code
WHERE a.resource = "PRCL"
GROUP BY b.faz_group, c.division, d.generic_land_use_1;

CREATE TEMPORARY TABLE tmp_max_jobs_by_fg
SELECT summary_area, max(jobs) as max_jobs
FROM jobs_by_fy_division_lu_1
GROUP BY summary_area;

ALTER TABLE tmp_max_jobs_by_fg add index (summary_area);
ALTER TABLE jobs_by_fy_division_lu_1  add index (summary_area);

CREATE TEMPORARY TABLE tmp_sector_lu_rates_1
(summary_area text, division text, land_use text, proximity double);

INSERT INTO tmp_sector_lu_rates_1 (summary_area, division, land_use, proximity)
SELECT a.summary_area, a. division, a.land_use, 
(a.jobs/b.max_jobs) as proximity
FROM jobs_by_fy_division_lu_1 as a
INNER JOIN tmp_max_jobs_by_fg as b 
on a.summary_area = b.summary_area;

CREATE TEMPORARY TABLE tmp_aLAND_USE
SELECT 1 as link, generic_land_use_1
FROM land_use_generic_reclass
GROUP BY generic_land_use_1;

CREATE TEMPORARY TABLE tmp_aSUMMARY_AREA
SELECT 1 as link, faz_group as summary_area
FROM faz_groups
GROUP BY faz_group;

CREATE TEMPORARY TABLE tmp_aSECTOR
SELECT 1 as link, division
FROM sector_reclass
GROUP BY division;

CREATE TEMPORARY TABLE tmp_summary_area_sector_land_use_combinations
SELECT a.summary_area, b.division, c.generic_land_use_1
as land_use, 0 as proximity
FROM (tmp_aSUMMARY_AREA as a
INNER JOIN tmp_aSECTOR as b on a.link = b.link)
INNER JOIN tmp_aLAND_USE as c on b.link = c.link;


#1. insert records from tmp_summary_area_sector_land_use_combinations
#into tmp_sector_lu_rates_1;

INSERT INTO tmp_sector_lu_rates_1 select * from tmp_summary_area_sector_land_use_combinations;

#2. then create sector_land_use_rates summarizing by summary_area, division, land_use, max(proximity) as proximity;

create table sector_land_use_rates
 SELECT summary_area, division, land_use, sum(proximity) as PROXIMITY
 FROM tmp_sector_lu_rates_1 group by summary_area, division, land_use; 
 
ALTER TABLE sector_land_use_rates change column division SECTOR text;

drop table tmp_max_jobs_by_fg;
drop table jobs_by_fy_division_lu_1;
drop table tmp_sector_lu_rates_1;
drop table tmp_aLAND_USE;
drop table tmp_aSUMMARY_AREA;
drop table tmp_aSECTOR;
drop table tmp_summary_area_sector_land_use_combinations;