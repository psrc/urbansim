# written for UGB scenario, keeping 2016 data; getting rid of model results from 2017 and after.
# database: WFRC_1997_output_2030_UGB

#NOTE- to tailor this SQL to your situation, make sure you change:
#1) Last good year.  In the SQL below, 2016 was the last year for which we want to keep data.  So, in
#	in other words, we are trying to re-run the model picking up from 2017 and going on from there.
#2) First bad year.  2017 in the case below.  We want to delete the model output generated for year 
	2017 and after.
#3) Database name in the 'use' statement directly below.  

use WFRC_1997_output_2030_UGB;


#*************************************************
# clean out jobs and households

# create a table with those households we need to delete
create table households_todelete
	select distinct(household_id) as household_id from households_exported where year > 2016;
create index households_todelete_x on households_todelete (household_id);
delete from households_todelete using households_todelete as hd, households_exported he 
	where he.year < 2017 and hd.household_id = he.household_id;
	#note- could have just looked at the ID values, which indicate their relative age (ie, could just delete all households with ID great than X, where X is the first ID created in the bad years.
	
# and now remove the offending rows
delete from households_constants using households_constants as hc, households_todelete as hd 
	where hd.household_id = hc.household_id;
delete from households_exported where year > 2016;


# create a table with those jobs we need to delete
create table jobs_todelete
	select distinct(job_id) as job_id from jobs_exported where year > 2016;
create index jobs_todelete_x on jobs_todelete (job_id);
delete from jobs_todelete using jobs_todelete as jd, jobs_exported je 
	where je.year < 2017 and jd.job_id = je.job_id;

# and now remove the offending rows
delete from jobs_constants using jobs_constants as jc, jobs_todelete as jd 
	where jd.job_id = jc.job_id;
delete from jobs_exported where year > 2016;



#*************************************************
# clean out accessibilities, gridcells exported

create index accessibilities_year
     on accessibilities (year);
delete from accessibilities where year > 2016;
drop index accessibilities_year on accessibilities;

create index gridcells_exported_year
     on gridcells_exported (year);
delete from gridcells_exported where year > 2016;
drop index gridcells_exported_year on gridcells_exported;