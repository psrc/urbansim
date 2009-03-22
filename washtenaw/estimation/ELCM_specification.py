# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

all_variables = [
    'age = urbansim.gridcell.building_age',
    'art = urbansim.gridcell.is_near_arterial',
    'hwy = urbansim.gridcell.is_near_highway',
    'hwydist = urbansim.gridcell.ln_distance_to_highway', 
    'flood = urbansim.gridcell.is_in_floodplain', 
    'stream = urbansim.gridcell.is_in_stream_buffer', 
    'wet = urbansim.gridcell.is_in_wetland', 
    'ln_land_val = urbansim.gridcell.ln_total_land_value', 
    'lv_ac_wwd = urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 
    'ln_impval = ln_total_improvement_value', 
    'ln_nres_ival_sqft = ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)',
    'ln_tot_val = urbansim.gridcell.ln_total_value', 
    'ln_com_sqft = urbansim.gridcell.ln_commercial_sqft', 
    'ln_com_sqft_wwd = urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 
    'ln_ind_sqft = urbansim.gridcell.ln_industrial_sqft', 
    'ln_ind_sqft_wwd = urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 
    'ln_res_units = urbansim.gridcell.ln_residential_units', 
    'ln_res_units_wwd = urbansim.gridcell.ln_residential_units_within_walking_distance', 
    'ln_nres_sqft_wwd = urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 
    'pct_low_inc_wwd = urbansim.gridcell.percent_low_income_households_within_walking_distance', 
    'pct_mid_inc_wwd = urbansim.gridcell.percent_mid_income_households_within_walking_distance', 
    'pct_high_inc_wwd = urbansim.gridcell.percent_high_income_households_within_walking_distance', 
    'ln_wk_acc_emp_1 = urbansim.gridcell.ln_work_access_to_employment_1', 
    'ln_wk_acc_pop_1 = urbansim.gridcell.ln_work_access_to_population_1', 
    'ln_pop_wwd = urbansim.gridcell.ln_total_population_within_walking_distance', 
    'ln_emp_wwd = urbansim.gridcell.ln_total_employment_within_walking_distance', 
    'ln_basic_emp_wwd = urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 
    'ln_retail_emp_wwd = urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 
    'ln_service_emp_wwd = urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 
    'ln_same_sector_emp_wwd = urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 
    'ln_same_sector_emp_faz = urbansim.job_x_gridcell.same_sector_jobs_in_faz', 
    ]

specification ={}

specification['industrial'] = { #industrial
"_definition_": all_variables,
1:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

2:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

3:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

4:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

5:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

6:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

7:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

8:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

9:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

10:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

11:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

12:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

13:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

14:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

15:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

16:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

}
specification['commercial'] = {  #commercial
"_definition_": all_variables,
1:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

2:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

3:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

4:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    #'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

5:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

6:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

7:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

8:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

9:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

10:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

11:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

12:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

13:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

14:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

15:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

16:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

}
specification['home_based'] = {  #commercial
"_definition_": all_variables,
-2:
    [
    'art',
    'hwy',
    'ln_nres_sqft_wwd',
    'ln_retail_emp_wwd',
    'ln_service_emp_wwd',
    'ln_same_sector_emp_wwd',
    ],

}
