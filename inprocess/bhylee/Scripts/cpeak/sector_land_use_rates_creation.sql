# This script is designed to create the sector_land_use_rates table that is then 
# used in the job allocator utility, proprietor_distributor scripts, and others.
# It produces a table sector_land_use_rates that is essentially the proportion
# of jobs in a given sector and FAZ group that are found on parcels of various
# land uses.

# Inputs:
#	employers_parcels_preliminary_identity
#		Fields: 
#			number_of_jobs, 
#			faz, 
#			sic, 
#			county, 
#			land_use_code, 
#			resource
#	faz_groups
#			faz, 
#			faz_group
#	Sector_reclass
#			division, 
#			sic
#	land_use_generic_reclass

CREATE TEMPORARY TABLE jobs_by_fy_division_lu_1
SELECT 
	b.faz_group as summary_area, 
	c.division as division,
	d.generic_reclass_1 as land_use, 
	sum(a.number_of_jobs) as jobs
FROM ((employers_parcels_preliminary_identity as a 
	INNER JOIN faz_groups as b on a.faz = b.faz) 
	INNER JOIN sector_reclass as c on a.sic = c.sic)
	INNER JOIN land_use_generic_reclass as D
	on a.county = d.county and a.land_use_code = d.county_land_use_code
WHERE a.resource = "PRCL"
GROUP BY 
	b.faz_group, 
	c.division, 
	d.generic_reclass_1
;

CREATE TEMPORARY TABLE tmp_max_jobs_by_fg
SELECT summary_area, max(jobs) as max_jobs
FROM jobs_by_fy_division_lu_1
GROUP BY summary_area;

CREATE TEMPORARY TABLE tmp_sector_lu_rates_1
SELECT a.summary_area, a. division, a.land_use, 
(a.jobs/b.maxjobs) as proximity
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

#2. then create sector_land_use_rates summarizing by summary_area, division, land_use, max(proximity) as proximity;

drop table tmp_sector_lu_rates_1;
drop table tmp_aLAND_USE;
drop table tmp_aSUMMARY_AREA;
drop table tmp_aSECTOR;
drop table tmp_summary_area_sector_land_use_combinations;

