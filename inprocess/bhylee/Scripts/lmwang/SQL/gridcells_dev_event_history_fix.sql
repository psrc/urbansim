-- This script fixes development_event_history table for use in DM EDW

--1. fix development_event_history table
# delete non-event events(0 units and sqft, but non-zero improvement values)
delete from development_event_history 
where ifnull(residential_units,0) <= 0 
  and (ifnull(COMMERCIAL_SQFT,0) + ifnull(INDUSTRIAL_SQFT,0) + ifnull(GOVERNMENTAL_SQFT,0)) <= 0;

# delete vacant and governmental ending dev type
delete deh from development_event_history deh, PSRC_2000_baseyear_reestimation.gridcells g
where deh.grid_id = g.grid_id 
	and g.development_type_id >= 23;

# delete events violate the development_constraints
create index grid_id_scheduled_year_index on development_event_history (grid_id, scheduled_year);
create index devtype_index on PSRC_2000_baseyear_reestimation.development_constraints (devtype_x);

create temporary table tmp_delete_grid_ids
select distinct deh.grid_id from development_event_history deh
	inner join PSRC_2000_baseyear_reestimation.gridcells g using (grid_id)
	inner join PSRC_2000_baseyear_reestimation.development_constraints dc on g.plan_type_id = dc.plantype_x
where 
	g.development_type_id in (dc.devtype_x)
	or 
        ( deh.ending_development_type_id in (dc.devtype_x) 
	  and (g.city_id = dc.city_id or dc.city_id = -1)
	  and (g.county_id = dc.county_id or dc.county_id = -1)
	  and (IF(g.percent_wetland>50,1,0) = dc.is_in_wetland or dc.is_in_wetland = -1)
	  and (g.is_outside_urban_growth_boundary = dc.is_outside_urban_growth_boundary or dc.is_outside_urban_growth_boundary = -1)
	  and (IF(g.percent_stream_buffer>50,1,0) = dc.is_in_stream_buffer or dc.is_in_stream_buffer = -1)
          and (IF(g.percent_slope>50,1,0) = dc.is_on_steep_slope or dc.is_on_steep_slope = -1)
	  and (IF(g.percent_floodplain>50,1,0) = dc.is_in_floodplain or dc.is_in_floodplain = -1) 
        )	
	or 
        ( deh.starting_development_type_id in (dc.devtype_x) 
	  and (g.city_id = dc.city_id or dc.city_id = -1)
	  and (g.county_id = dc.county_id or dc.county_id = -1)
	  and (IF(g.percent_wetland>50,1,0) = dc.is_in_wetland or dc.is_in_wetland = -1)
	  and (g.is_outside_urban_growth_boundary = dc.is_outside_urban_growth_boundary or dc.is_outside_urban_growth_boundary = -1)
	  and (IF(g.percent_stream_buffer>50,1,0) = dc.is_in_stream_buffer or dc.is_in_stream_buffer = -1)
          and (IF(g.percent_slope>50,1,0) = dc.is_on_steep_slope or dc.is_on_steep_slope = -1)
	  and (IF(g.percent_floodplain>50,1,0) = dc.is_in_floodplain or dc.is_in_floodplain = -1) 
	)
	or
	( dc.devtype_x = -1
	  and (g.city_id = dc.city_id or dc.city_id = -1)
	  and (g.county_id = dc.county_id or dc.county_id = -1)
	  and (IF(g.percent_wetland>50,1,0) = dc.is_in_wetland or dc.is_in_wetland = -1)
	  and (g.is_outside_urban_growth_boundary = dc.is_outside_urban_growth_boundary or dc.is_outside_urban_growth_boundary = -1)
	  and (IF(g.percent_stream_buffer>50,1,0) = dc.is_in_stream_buffer or dc.is_in_stream_buffer = -1)
          and (IF(g.percent_slope>50,1,0) = dc.is_on_steep_slope or dc.is_on_steep_slope = -1)
	  and (IF(g.percent_floodplain>50,1,0) = dc.is_in_floodplain or dc.is_in_floodplain = -1) 
	)
;

create index grid_id_index on tmp_delete_grid_ids (grid_id);

delete deh from development_event_history deh
	inner join tmp_delete_grid_ids d using (grid_id)
where 
	deh.grid_id = d.grid_id
;

--2. fixing developer_model_estimation_data with ending dev type >= 23 (should not be needed)

# run diagnose first
--select year, grid_id, ending_development_type_id 
--from developer_model_estimation_data 
--where ending_development_type_id >=23 and choice_indicator = 1;

# delete rows 
--create temporary table tmp_unwanted_ending_23 
--select year, grid_id, ending_development_type_id 
--from developer_model_estimation_data 
--where ending_development_type_id >=23 and choice_indicator = 1;

--delete d.* from developer_model_estimation_data d, tmp_unwanted_ending_23 u where d.year = u.year and d.grid_id = u.grid_id;
--delete d.* from developer_model_estimation_data d where ending_development_type_id >=23;



