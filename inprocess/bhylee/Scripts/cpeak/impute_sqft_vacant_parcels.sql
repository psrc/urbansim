# 1. Find vacant parcels with jobs
#   (these should comprise all the jobs on vacant gridcells
#	 with the exception of those that had been placed directly
#	 on military lands)
# 2. The problem in imputing only square feet for these parcels
#	 is that because they are of vacant land uses, there is no 
#	 distribution of jobs-to-sqft ratios from which to impute
# 	 sqft.  Therefore, the land use itself 
#  	 must be imputed in addition to the square footage.  This 
#	 can be accomplished in one of several ways:
#		A. Find the dominant (most common) sector among the jobs 
#			placed on the parcel.  Assign the parcel the 
#			land use most frequently associated with that sector, 
#			as well as the square footage that goes with that 
#			sector-land use combination.  Square footage must
#			be added by adding a building to the buildings table
#		B. Same as (A) except that the dominant sector is determined
#			stochastically* from the distribution of sectors
#			among the jobs on the parcel.
#		C. Same as (B) except that after the dominant sector is
#			chosen, the land use is determined stochastically
#			from the set of land uses associated with the sector. 
#
#	* by "stochastically" I mean selected from a cumulative 
#		distribution of sectors/land uses. 

USE PSRC_parcels_king

######
#
# Create the set of vacant parcels with jobs on them
#

# get jobs from job_allocator
#  (returns no parcels for King Co.)
DROP TABLE IF EXISTS vacant_parcels_with_employment;
CREATE TEMPORARY TABLE vacant_parcels_with_employment
SELECT
	a.county, 
	a.parcel_id,
	a.land_use,
	d.generic_land_use_1,
	c.sector as old_emp_sector,
	c.number_of_jobs as jobs
FROM parcels a 
	INNER JOIN job_allocation_king.final_employers_matched_to_parcels b
	on a.parcel_id = b.parcel_id
	INNER JOIN job_allocation_king.employers c
	on b.employer_id = c.employer_id
	INNER JOIN 	PSRC_2000_data_quality_indicators.land_use_generic_reclass d
	ON a.county = d.county and 
	a.land_use = d.county_land_use_code
WHERE 
	d.generic_land_use_1 in (
	'Vacant', 
	'Forest - harvestable', 
	'Forest - protected'
	)
;


# get jobs from proprietors distributor
#  (returns 6744 parcels for King Co.)
DROP TABLE IF EXISTS vacant_parcels_with_employment_pd;
CREATE TEMPORARY TABLE vacant_parcels_with_employment_pd
SELECT
	a.county, 
	a.parcel_id,
	a.land_use,
	d.generic_land_use_1,
	b.sector as old_emp_sector,
	count(*) as jobs
FROM parcels a 
	INNER JOIN PSRC_proprietors_distributor_king.DISTRIBUTED_JOBS b
	on a.parcel_id = b.parcel_id
	INNER JOIN PSRC_2000_data_quality_indicators.land_use_generic_reclass d
	ON a.county = d.county and 
	a.land_use = d.county_land_use_code
WHERE 
	d.generic_land_use_1 not in (
	'Vacant', 
	'Forest - harvestable', 
	'Forest - protected',
	'Water'
	)
GROUP BY 
	a.county,

	a.parcel_id,
	b.sector
;
select sum(jobs) from vacant_parcels_with_employment_pd;

select 
	generic_land_use_1, 
	sum(jobs) 
from vacant_parcels_with_employment_pd
group by generic_land_use_1;