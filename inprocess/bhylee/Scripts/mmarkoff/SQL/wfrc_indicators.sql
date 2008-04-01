
# JOBS - count and density 

create temporary table tmp_zi1
select j.zone_id, count(j.job_id) as numjobs1, count(j.job_id)/z.acres as jobdensity1
	from WFRC_1997_output_2030_LRP.jobs_exported as j, WFRC_1997_baseyear.zones as z
	where 
		j.zone_id=z.zone_id AND
		j.year=1997 
	group by zone_id;

create temporary table tmp_zi2
select j.zone_id, count(j.job_id) as numjobs2, count(j.job_id)/z.acres as jobdensity2
	from WFRC_1997_output_2030_LRP.jobs_exported as j, WFRC_1997_baseyear.zones as z
	where 
		j.zone_id=z.zone_id AND
		j.year=2003
	group by zone_id;

create table zone_info_jobs
select z.zone_id, z.travel_time_to_cbd, zi1.numjobs1, zi2.numjobs2, zi1.jobdensity1, zi2.jobdensity2  
	from WFRC_1997_baseyear.zones as z 
	left join tmp_zi1 as zi1 on z.zone_id=zi1.zone_id 
	left join tmp_zi2 as zi2 on z.zone_id=zi2.zone_id 
	group by z.zone_id;

drop table tmp_zi1;
drop table tmp_zi2;


# HOUSEHOLDS - count and density 

create temporary table tmp_zi1
select a.zone_id, count(a.household_id) as numhhs1, count(a.household_id)/z.acres as hhdensity1
	from WFRC_1997_output_2030_LRP.households_exported as a, WFRC_1997_baseyear.zones as z
	where 
		a.zone_id=z.zone_id AND
		a.year=1997 
	group by zone_id;

create temporary table tmp_zi2
select a.zone_id, count(a.household_id) as numhhs2, count(a.household_id)/z.acres as hhdensity2
	from WFRC_1997_output_2030_LRP.households_exported as a, WFRC_1997_baseyear.zones as z
	where 
		a.zone_id=z.zone_id AND
		a.year=2003
	group by zone_id;

create table zone_info_hhs
select z.zone_id, z.travel_time_to_cbd, zi1.numhhs1, zi2.numhhs2, zi1.hhdensity1, zi2.hhdensity2  
	from WFRC_1997_baseyear.zones as z 
	left join tmp_zi1 as zi1 on z.zone_id=zi1.zone_id 
	left join tmp_zi2 as zi2 on z.zone_id=zi2.zone_id 
	group by z.zone_id;

drop table tmp_zi1;
drop table tmp_zi2;


# RESIDENTIAL UNITS - count and density

create temporary table tmp_zi1
select g.zone_id, sum(a.residential_units) as numru1, sum(a.residential_units)/z.acres as rudensity1
	from WFRC_1997_output_2030_LRP.gridcells_exported as a, WFRC_1997_baseyear.gridcells as g, WFRC_1997_baseyear.zones as z
	where 
		a.grid_id=g.grid_id AND
		g.zone_id=z.zone_id AND
		a.year=1997 
	group by zone_id;

create temporary table tmp_zi2
select g.zone_id, sum(a.residential_units) as numru2, sum(a.residential_units)/z.acres as rudensity2
	from WFRC_1997_output_2030_LRP.gridcells_exported as a, WFRC_1997_baseyear.gridcells as g, WFRC_1997_baseyear.zones as z
	where 
		a.grid_id=g.grid_id AND
		g.zone_id=z.zone_id AND
		a.year=2003
	group by zone_id;

create table zone_info_ru
select z.zone_id, z.travel_time_to_cbd, zi1.numru1, zi2.numru2, zi1.rudensity1, zi2.rudensity2  
	from WFRC_1997_baseyear.zones as z 
	left join tmp_zi1 as zi1 on z.zone_id=zi1.zone_id 
	left join tmp_zi2 as zi2 on z.zone_id=zi2.zone_id 
	group by z.zone_id;

drop table tmp_zi1;
drop table tmp_zi2;


# NON-RES SQFT  - note that gridcells exported doesn't have zone_id

create temporary table tmp_zi1
select g.zone_id, sum(a.commercial_sqft + a.industrial_sqft + a.governmental_sqft) as numnonrusqft1, sum(a.commercial_sqft + a.industrial_sqft + a.governmental_sqft)/z.acres as nonrudensity1
	from WFRC_1997_output_2030_LRP.gridcells_exported as a, WFRC_1997_baseyear.gridcells as g, WFRC_1997_baseyear.zones as z
	where 
		a.grid_id=g.grid_id AND
		g.zone_id=z.zone_id AND
		a.year=1997 
	group by zone_id;

create temporary table tmp_zi2
select g.zone_id, sum(a.commercial_sqft + a.industrial_sqft + a.governmental_sqft) as numnonrusqft2, sum(a.commercial_sqft + a.industrial_sqft + a.governmental_sqft)/z.acres as nonrudensity2
	from WFRC_1997_output_2030_LRP.gridcells_exported as a, WFRC_1997_baseyear.gridcells as g, WFRC_1997_baseyear.zones as z
	where 
		a.grid_id=g.grid_id AND
		g.zone_id=z.zone_id AND
		a.year=2003
	group by zone_id;

create table zone_info_nonru
select z.zone_id, z.travel_time_to_cbd, zi1.numnonrusqft1, zi2.numnonrusqft2, zi1.nonrudensity1, zi2.nonrudensity2  
	from WFRC_1997_baseyear.zones as z 
	left join tmp_zi1 as zi1 on z.zone_id=zi1.zone_id 
	left join tmp_zi2 as zi2 on z.zone_id=zi2.zone_id 
	group by z.zone_id;

drop table tmp_zi1;
drop table tmp_zi2;