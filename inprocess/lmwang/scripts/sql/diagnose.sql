--17->18 (constraints of plant_type 3)
select * from PSRC_2000_estimation_petecaba.development_event_history where grid_id = 271033 \G

select * from GSPSRC_2000_baseyear_flattened.gridcells where grid_id = 271033\G

select * from PSRC_2000_estimation_petecaba_unrolled.gridcells where grid_id = 271033\G

select * from PSRC_2000_estimation_petecaba_unrolled.developer_model_estimation_data where grid_id = 271033\G


--( the count for transition 17->18 is 224
select starting_development_type_id, ending_development_type_id, count(*) from PSRC_2000_estimation_petecaba.development_event_history where starting_development_type_id between 17 and 23 group by starting_development_type_id, ending_development_type_id;
--)


--2->23, due to defintion of type 23
select * from PSRC_2000_estimation_petecaba.development_event_history where grid_id = 250072 \G

select * from GSPSRC_2000_baseyear_flattened.gridcells where grid_id = 250072\G

select * from PSRC_2000_estimation_petecaba_unrolled.developer_model_estimation_data where grid_id = 250072\G


--24->24, type 24 in baseyear, no events (1. 29; 2. non-event event, e.g. adding impv)
select * from PSRC_2000_estimation_petecaba.development_event_history where grid_id = 632540 \G

select * from GSPSRC_2000_baseyear_flattened.gridcells where grid_id = 632540\G

select * from PSRC_2000_estimation_petecaba_unrolled.gridcells where grid_id = 632540\G

select * from PSRC_2000_estimation_petecaba_unrolled.developer_model_estimation_data where grid_id = 632540\G



select starting_development_type_id, ending_development_type_id, count(*) from developer_model_estimation_data where starting_development_type_id =24 and ending_development_type_id in (23,24) group by starting_development_type_id, ending_development_type_id;

--17-23 -> ?
select plan_type_id from developer_model_estimation_data d inner join PSRC_2000_baseyear_reestimation.gridcells g using (grid_id) 
where d.starting_development_type_id between 17 and 23 
and (d.ending_development_type_id = d.starting_development_type_id 
or d.ending_development_type_id = -1);

##diagnostic script
select grid_id, starting_development_type_id, ending_development_type_id from PSRC_2000_estimation_petecaba.development_event_history where starting_development_type_id between 17 and 23 and ending_development_type_id <> starting_development_type_id order by rand() limit 5 \G

--missing 20->17
select * from PSRC_2000_estimation_petecaba_unrolled1.developer_model_estimation_data where grid_id = 660066 and choice_indicator = 1\G
select * from PSRC_2000_estimation_petecaba_unrolled1.development_event_history where grid_id = 660066\G
select * from PSRC_2000_estimation_petecaba.development_event_history where grid_id = 660066\G
select * from PSRC_2000_baseyear_reestimation.gridcells where grid_id = 660066\G

select * from PSRC_2000_estimation_petecaba_unrolled1.developer_model_estimation_data where grid_id = 454663 and choice_indicator = 1\G
select * from PSRC_2000_estimation_petecaba_unrolled1.development_event_history where grid_id = 454663\G
select * from PSRC_2000_estimation_petecaba.development_event_history where grid_id = 454663\G
select * from PSRC_2000_baseyear_reestimation.gridcells where grid_id = 454663\G


select d.grid_id, plan_type_id, starting_development_type_id, ending_development_type_id from developer_model_estimation_data d 
	inner join PSRC_2000_baseyear_reestimation.gridcells g using (grid_id)  where d.starting_development_type_id between 17 and 23
	and (d.ending_development_type_id = d.starting_development_type_id  or d.ending_development_type_id = -1) and plan_type_id = 13;

--
select * from PSRC_2000_baseyear_reestimation.gridcells where grid_id = 716351 \G
select * from PSRC_2000_estimation_petecaba.development_event_history where grid_id = 716351 \G



#problem 2,4
select distinct d.grid_id, d.year from PSRC_2000_estimation_petecaba_unrolled1.developer_model_estimation_data d inner join PSRC_2000_estimation_petecaba.development_event_history deh on d.grid_id = deh.grid_id and d.year = deh.scheduled_year where d.starting_development_type_id = 24 and d.ending_development_type_id = 24 and d.choice_indicator = 1;


#select starting_development_type_id, ending_development_type_id, count(*) from developer_model_estimation_data  group by starting_development_type_id, ending_development_type_id order by starting_development_type_id, ending_development_type_id;


###problem 3 #check all inconsistent starting/ending development type id

create table tmp_diagonse_inconsistent_transition
select g.grid_id, g.development_type_id as b_dev_type, g.plan_type_id, g.residential_units as b_units, g.commercial_sqft as b_com_sqft, g.governmental_sqft as b_gov_sqft,g.industrial_sqft as b_ind_sqft, 
d1.scheduled_year as scenario_year, d1.starting_development_type_id scenario_starting_dev_type, d1.ending_development_type_id as scenario_ending_dev_type, 
d1.residential_units as scenario_units, d1.commercial_sqft as scenario_com_sqft, d1.industrial_sqft as scenario_ind_sqft, 
d2.scheduled_year as edw_year, d2.starting_development_type_id as edw_starting_dev_type, d2.ending_development_type_id as edw_ending_dev_type, 
d2.residential_units as edw_units, d2.commercial_sqft as edw_com_sqft, d2.industrial_sqft as edw_ind_sqft 
from PSRC_2000_baseyear_reestimation.gridcells g inner join PSRC_2000_estimation_petecaba.development_event_history d1 
            on g.grid_id = d1.grid_id 
          inner join PSRC_2000_estimation_petecaba_unrolled1.development_event_history d2 
            on d1.scheduled_year = d2.scheduled_year and d1.grid_id = d2.grid_id 
where (d1.starting_development_type_id <> d2.starting_development_type_id or d1.ending_development_type_id <> d2.ending_development_type_id) 
order by grid_id, scenario_year \G 

and d2.starting_development_type_id between 17 and 23