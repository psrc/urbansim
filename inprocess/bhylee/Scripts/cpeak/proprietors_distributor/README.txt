Running the Proprietors Distributor and Creating the Jobs table in the baseyear database.
This assumes that the job allocator utility has already been run for all counties.


I.  Proprietors Distributor 
    (must be run for each county.  At time of this writing, each county database name is in the 
     form: PSRC_proprietors_distributor_[county].

	1. Update JOBS_PER_COUNTY table with new job totals by sector.  TOTAL_COUNTY_JOBS is the 
	important field here, and should equal the fields representing proprietors and the 
	leftovers from the job allocator.
	
	2. Run proprietors_distributor.pl
	
	example command for Kitsap County:
	(echo PSRC_proprietors_distributor_kitsap | perl -w /projects/urbansim7/scripts/private/cpeak/proprietors_distributor/proprietors_distributor.pl > pd_kitsap.out) >& pd_kitsap.err &

II. Collate all the jobs tables from the job allocator databases with all the jobs_rounded
 	tables from the PSRC_proprietors_distributor databases with 
 	/projects/urbansim7/scripts/public/data_prep/collate_jobs_tables.sql
 	
 	This will append the jobs tables in the job_allocator databases with the JOBS_ROUNDED table in the proprietors_distributor databases into a jobs table in the baseyear database.  
 	
III.  The resulting jobs table in the baseyear database at this point will have sector codes that differ from 
	the employment_sector table in the baseyear.  These must be reclassified through the jobs_sector_reclassification.sql script in Scripts/cpeak.