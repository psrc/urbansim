##FIX:


--1. fix development_event_history table
--delete non-event events(0 units and sqft, but non-zero improvement values)
delete from development_event_history where ifnull(residential_units,0) <= 0 and (ifnull(COMMERCIAL_SQFT,0) + ifnull(INDUSTRIAL_SQFT,0) + ifnull(GOVERNMENTAL_SQFT,0)) <= 0;

--delete vacant and governmental ending development type
delete deh from development_event_history deh, PSRC_2000_baseyear_reestimation.gridcells g
where deh.grid_id = g.grid_id 
	and g.development_type_id >= 23;

--delete events violate the development_constraints
delete deh from development_event_hisotry deh
	inner join PSRC_2000_baseyear_reestimation.gridcells g using (grid_id)
	inner join PSRC_2000_baseyear_reestimation.development_constraints dc on g.plan_type_id = dc.plantype_x
where 
	g.development_type_id in (dc.devtype_x);
	#or deh.ending_development_type_id in (dc.devtype_x);	


--2. ending type >= 23
 
create table tmp_unwanted_ending_23 select year, grid_id, ending_development_type_id from developer_model_estimation_data where ending_development_type_id >=23 and choice_indicator = 1;

delete d.* from developer_model_estimation_data d, tmp_unwanted_ending_23 u where d.year = u.year and d.grid_id = u.grid_id;

delete d.* from developer_model_estimation_data d where ending_development_type_id >=23;

	
--3. plant type?


