
#FOR COMPARING WITH WFRC OBSERVED MEDIUM DISTRICT DATA:


# JOBS  

#create temporary table tmp_zi1 
select z.distmed, count(j.job_id) as numjobs1
	from WFRC_1997_output_2030_LRP.jobs_exported as j, WFRC_1997_baseyear.zones as z
	where 
		j.zone_id=z.zone_id AND
		j.year=1997 
	group by z.distmed;
