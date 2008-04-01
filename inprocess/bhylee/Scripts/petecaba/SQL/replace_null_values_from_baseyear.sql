update accessibilities_input set trip_weighted_travel_time_from_zone_for_SOV = 0 where trip_weighted_travel_time_from_zone_for_SOV is null ;
update accessibilities_input set trip_weighted_travel_time_to_zone_for_SOV   = 0 where trip_weighted_travel_time_to_zone_for_SOV   is null ;
update accessibilities_input set trip_weighted_travel_time_for_transit_walk  = 0 where trip_weighted_travel_time_for_transit_walk  is null ;
update accessibilities_input set utility_for_SOV = 0 where utility_for_SOV is null ;
update accessibilities_input set utility_for_transit_walk = 0 where utility_for_transit_walk is null ;

update annual_employment_control_totals set YEAR         = 0 where YEAR         is null ;
update annual_employment_control_totals set TOTAL_HOME_BASED_EMPLOYMENT     = 0 where TOTAL_HOME_BASED_EMPLOYMENT     is null ;
update annual_employment_control_totals set TOTAL_NON_HOME_BASED_EMPLOYMENT = 0 where TOTAL_NON_HOME_BASED_EMPLOYMENT is null ;

update annual_household_control_totals set RACE_ID = 0 where RACE_ID is null ;
update annual_household_control_totals set PERSONS = 0 where PERSONS is null ;
update annual_household_control_totals set TOTAL_NUMBER_OF_HOUSEHOLDS = 0 where TOTAL_NUMBER_OF_HOUSEHOLDS is null ;

update annual_relocation_rates_for_households set AGE_MIN = 0 where AGE_MIN is null ;
update annual_relocation_rates_for_households set AGE_MAX = 0 where AGE_MAX is null ;
update annual_relocation_rates_for_households set INCOME_MIN                = 0 where INCOME_MIN                is null ;
update annual_relocation_rates_for_households set INCOME_MAX                = 0 where INCOME_MAX                is null ;
update annual_relocation_rates_for_households set PROBABILITY_OF_RELOCATING = 0 where PROBABILITY_OF_RELOCATING is null ;

update annual_relocation_rates_for_jobs set SECTOR_ID                  = 0 where SECTOR_ID                  is null ;
update annual_relocation_rates_for_jobs set JOB_RELOCATION_PROBABILITY = 0 where JOB_RELOCATION_PROBABILITY is null ;

update base_year set year = 0 where year is null ;

update cities set city_id = 0 where city_id is null ;
update cities set city_name = 0 where city_name is null ;

update constant_taz_columns set TAZ     = 0 where TAZ     is null ;
update constant_taz_columns set PCTMF   = 0 where PCTMF   is null ;
update constant_taz_columns set GQI     = 0 where GQI     is null ;
update constant_taz_columns set GQN     = 0 where GQN     is null ;
update constant_taz_columns set FTEUNIV = 0 where FTEUNIV is null ;
update constant_taz_columns set DEN     = 0 where DEN     is null ;
update constant_taz_columns set FAZ     = 0 where FAZ     is null ;
update constant_taz_columns set YEAR    = 0 where YEAR    is null ;

update counties set county_id = 0 where county_id is null ;
update counties set county_name = 0 where county_name is null ;

update developer_model_alternative_shares set SUB_MODEL_ID       = 0 where SUB_MODEL_ID       is null ;
update developer_model_alternative_shares set EQUATION_ID        = 0 where EQUATION_ID        is null ;
update developer_model_alternative_shares set OBSERVED_FREQUENCY = 0 where OBSERVED_FREQUENCY is null ;
update developer_model_alternative_shares set ADJUST             = 0 where ADJUST             is null ;
update developer_model_alternative_shares set MAXIMUM_VALUE      = 0 where MAXIMUM_VALUE      is null ;

update developer_model_calibrated_constant_coefficients set SUB_MODEL_ID      = 0 where SUB_MODEL_ID      is null ;
update developer_model_calibrated_constant_coefficients set COEFFICIENT_NAME  = 0 where COEFFICIENT_NAME  is null ;
update developer_model_calibrated_constant_coefficients set ESTIMATE          = 0 where ESTIMATE          is null ;
update developer_model_calibrated_constant_coefficients set STANDARD_ERROR    = 0 where STANDARD_ERROR    is null ;
update developer_model_calibrated_constant_coefficients set T_STATISTIC       = 0 where T_STATISTIC       is null ;
update developer_model_calibrated_constant_coefficients set P_VALUE           = 0 where P_VALUE           is null ;

update developer_model_coefficients set SUB_MODEL_ID     = 0 where SUB_MODEL_ID     is null ;
update developer_model_coefficients set COEFFICIENT_NAME = 0 where COEFFICIENT_NAME is null ;
update developer_model_coefficients set ESTIMATE         = 0 where ESTIMATE         is null ;
update developer_model_coefficients set STANDARD_ERROR   = 0 where STANDARD_ERROR   is null ;
update developer_model_coefficients set T_STATISTIC      = 0 where T_STATISTIC      is null ;
update developer_model_coefficients set P_VALUE          = 0 where P_VALUE          is null ;

update developer_model_constant_calibration set ITERATION       = 0 where ITERATION       is null ;
update developer_model_constant_calibration set SUB_MODEL_ID    = 0 where SUB_MODEL_ID    is null ;
update developer_model_constant_calibration set EQUATION_ID     = 0 where EQUATION_ID     is null ;
update developer_model_constant_calibration set FREQUENCY       = 0 where FREQUENCY       is null ;
update developer_model_constant_calibration set PREDICTED_SHARE = 0 where PREDICTED_SHARE is null ;
update developer_model_constant_calibration set PRIOR_ESTIMATE  = 0 where PRIOR_ESTIMATE  is null ;
update developer_model_constant_calibration set ADJUSTMENT      = 0 where ADJUSTMENT      is null ;
update developer_model_constant_calibration set NEW_ESTIMATE    = 0 where NEW_ESTIMATE    is null ;

update developer_model_estimation_data set YEAR       = 0 where YEAR       is null ;
update developer_model_estimation_data set GRID_ID    = 0 where GRID_ID    is null ;
update developer_model_estimation_data set ALTERNATIVE_ID                = 0 where ALTERNATIVE_ID                is null ;
update developer_model_estimation_data set STARTING_DEVELOPMENT_TYPE_ID  = 0 where STARTING_DEVELOPMENT_TYPE_ID  is null ;
update developer_model_estimation_data set ENDING_DEVELOPMENT_TYPE_ID    = 0 where ENDING_DEVELOPMENT_TYPE_ID    is null ;
update developer_model_estimation_data set CHOICE_INDICATOR              = 0 where CHOICE_INDICATOR              is null ;
update developer_model_estimation_data set e_bw       = 0 where e_bw       is null ;
update developer_model_estimation_data set sfcwrt     = 0 where sfcwrt     is null ;
update developer_model_estimation_data set one        = 0 where one        is null ;
update developer_model_estimation_data set flood      = 0 where flood      is null ;
update developer_model_estimation_data set strbuf     = 0 where strbuf     is null ;
update developer_model_estimation_data set wtlnd      = 0 where wtlnd      is null ;
update developer_model_estimation_data set art        = 0 where art        is null ;
update developer_model_estimation_data set hwy        = 0 where hwy        is null ;
update developer_model_estimation_data set lalvaw     = 0 where lalvaw     is null ;
update developer_model_estimation_data set ldu        = 0 where ldu        is null ;
update developer_model_estimation_data set lduw       = 0 where lduw       is null ;
update developer_model_estimation_data set le_w       = 0 where le_w       is null ;
update developer_model_estimation_data set lv         = 0 where lv         is null ;
update developer_model_estimation_data set tr03wr     = 0 where tr03wr     is null ;
update developer_model_estimation_data set trdwrt     = 0 where trdwrt     is null ;
update developer_model_estimation_data set tr05wr     = 0 where tr05wr     is null ;
update developer_model_estimation_data set p03w       = 0 where p03w       is null ;
update developer_model_estimation_data set p_dev      = 0 where p_dev      is null ;
update developer_model_estimation_data set phiw       = 0 where phiw       is null ;
update developer_model_estimation_data set p01w       = 0 where p01w       is null ;
update developer_model_estimation_data set p05w       = 0 where p05w       is null ;
update developer_model_estimation_data set pstcw      = 0 where pstcw      is null ;
update developer_model_estimation_data set pslope     = 0 where pslope     is null ;
update developer_model_estimation_data set pwater     = 0 where pwater     is null ;
update developer_model_estimation_data set prxdev     = 0 where prxdev     is null ;
update developer_model_estimation_data set e_rew      = 0 where e_rew      is null ;
update developer_model_estimation_data set e_sew      = 0 where e_sew      is null ;
update developer_model_estimation_data set tt_cbd     = 0 where tt_cbd     is null ;
update developer_model_estimation_data set tt_tw      = 0 where tt_tw      is null ;
update developer_model_estimation_data set tt_sov     = 0 where tt_sov     is null ;
update developer_model_estimation_data set ut_sov     = 0 where ut_sov     is null ;
update developer_model_estimation_data set ut_tw      = 0 where ut_tw      is null ;

update developer_model_specification set SUB_MODEL_ID     = 0 where SUB_MODEL_ID     is null ;
update developer_model_specification set EQUATION_ID      = 0 where EQUATION_ID      is null ;
update developer_model_specification set VARIABLE_NAME    = 0 where VARIABLE_NAME    is null ;
update developer_model_specification set COEFFICIENT_NAME = 0 where COEFFICIENT_NAME is null ;
update developer_model_specification set SHORT_NAME       = 0 where SHORT_NAME       is null ;

update developer_model_variable_names set SHORT_NAME       = 0 where SHORT_NAME       is null ;
update developer_model_variable_names set VARIABLE_NAME    = 0 where VARIABLE_NAME    is null ;
update developer_model_variable_names set COEFFICIENT_NAME = 0 where COEFFICIENT_NAME is null ;
update developer_model_variable_names set MODEL_ID         = 0 where MODEL_ID         is null ;
update developer_model_variable_names set SUB_MODEL_ID     = 0 where SUB_MODEL_ID     is null ;

update development_constraint_events set CONSTRAINT_ID = 0 where CONSTRAINT_ID is null ;
update development_constraint_events set CITY_ID       = 0 where CITY_ID       is null ;
update development_constraint_events set COUNTY_ID     = 0 where COUNTY_ID     is null ;
update development_constraint_events set IS_IN_WETLAND = 0 where IS_IN_WETLAND is null ;
update development_constraint_events set IS_OUTSIDE_URBAN_GROWTH_BOUNDARY = 0 where IS_OUTSIDE_URBAN_GROWTH_BOUNDARY is null ;
update development_constraint_events set IS_IN_STREAM_BUFFER              = 0 where IS_IN_STREAM_BUFFER              is null ;
update development_constraint_events set IS_ON_STEEP_SLOPE                = 0 where IS_ON_STEEP_SLOPE                is null ;
update development_constraint_events set IS_IN_FLOODPLAIN                 = 0 where IS_IN_FLOODPLAIN                 is null ;
update development_constraint_events set DEVTYPE_X     = 0 where DEVTYPE_X     is null ;
update development_constraint_events set PLANTYPE_X    = 0 where PLANTYPE_X    is null ;
update development_constraint_events set SCHEDULED_YEAR = 0 where SCHEDULED_YEAR is null ;
update development_constraint_events set CHANGE_TYPE   = 0 where CHANGE_TYPE   is null ;

update development_constraints set CONSTRAINT_ID  = 0 where CONSTRAINT_ID  is null ;
update development_constraints set CITY_ID        = 0 where CITY_ID        is null ;
update development_constraints set COUNTY_ID      = 0 where COUNTY_ID      is null ;
update development_constraints set IS_IN_WETLAND  = 0 where IS_IN_WETLAND  is null ;
update development_constraints set IS_OUTSIDE_URBAN_GROWTH_BOUNDARY  = 0 where IS_OUTSIDE_URBAN_GROWTH_BOUNDARY  is null ;
update development_constraints set IS_IN_STREAM_BUFFER               = 0 where IS_IN_STREAM_BUFFER               is null ;
update development_constraints set IS_ON_STEEP_SLOPE                 = 0 where IS_ON_STEEP_SLOPE                 is null ;
update development_constraints set IS_IN_FLOODPLAIN                  = 0 where IS_IN_FLOODPLAIN                  is null ;
update development_constraints set PLANTYPE_X     = 0 where PLANTYPE_X     is null ;
update development_constraints set DEVTYPE_X      = 0 where DEVTYPE_X      is null ;

update development_event_history set GRID_ID         = 0 where GRID_ID         is null ;
update development_event_history set SCHEDULED_YEAR  = 0 where SCHEDULED_YEAR  is null ;
update development_event_history set STARTING_DEVELOPMENT_TYPE_ID                = 0 where STARTING_DEVELOPMENT_TYPE_ID                is null ;
update development_event_history set ENDING_DEVELOPMENT_TYPE_ID                  = 0 where ENDING_DEVELOPMENT_TYPE_ID                  is null ;
update development_event_history set DEVELOPMENT_TYPE_CHANGE_TYPE                = 0 where DEVELOPMENT_TYPE_CHANGE_TYPE                is null ;
update development_event_history set RESIDENTIAL_UNITS_CHANGE_TYPE               = 0 where RESIDENTIAL_UNITS_CHANGE_TYPE               is null ;
update development_event_history set RESIDENTIAL_UNITS        = 0 where RESIDENTIAL_UNITS        is null ;
update development_event_history set COMMERCIAL_SQFT_CHANGE_TYPE                 = 0 where COMMERCIAL_SQFT_CHANGE_TYPE                 is null ;
update development_event_history set COMMERCIAL_SQFT = 0 where COMMERCIAL_SQFT is null ;
update development_event_history set INDUSTRIAL_SQFT_CHANGE_TYPE                 = 0 where INDUSTRIAL_SQFT_CHANGE_TYPE                 is null ;
update development_event_history set INDUSTRIAL_SQFT = 0 where INDUSTRIAL_SQFT is null ;
update development_event_history set GOVERNMENTAL_SQFT_CHANGE_TYPE               = 0 where GOVERNMENTAL_SQFT_CHANGE_TYPE               is null ;
update development_event_history set GOVERNMENTAL_SQFT        = 0 where GOVERNMENTAL_SQFT        is null ;
update development_event_history set RESIDENTIAL_IMPROVEMENT_VALUE_CHANGE_TYPE   = 0 where RESIDENTIAL_IMPROVEMENT_VALUE_CHANGE_TYPE   is null ;
update development_event_history set RESIDENTIAL_IMPROVEMENT_VALUE               = 0 where RESIDENTIAL_IMPROVEMENT_VALUE               is null ;
update development_event_history set COMMERCIAL_IMPROVEMENT_VALUE_CHANGE_TYPE    = 0 where COMMERCIAL_IMPROVEMENT_VALUE_CHANGE_TYPE    is null ;
update development_event_history set COMMERCIAL_IMPROVEMENT_VALUE                = 0 where COMMERCIAL_IMPROVEMENT_VALUE                is null ;
update development_event_history set INDUSTRIAL_IMPROVEMENT_VALUE_CHANGE_TYPE    = 0 where INDUSTRIAL_IMPROVEMENT_VALUE_CHANGE_TYPE    is null ;
update development_event_history set INDUSTRIAL_IMPROVEMENT_VALUE                = 0 where INDUSTRIAL_IMPROVEMENT_VALUE                is null ;
update development_event_history set GOVERNMENTAL_IMPROVEMENT_VALUE_CHANGE_TYPE  = 0 where GOVERNMENTAL_IMPROVEMENT_VALUE_CHANGE_TYPE  is null ;
update development_event_history set GOVERNMENTAL_IMPROVEMENT_VALUE              = 0 where GOVERNMENTAL_IMPROVEMENT_VALUE              is null ;
update development_event_history set FRACTION_RESIDENTIAL_LAND_VALUE_CHANGE_TYPE = 0 where FRACTION_RESIDENTIAL_LAND_VALUE_CHANGE_TYPE is null ;
update development_event_history set FRACTION_RESIDENTIAL_LAND_VALUE             = 0 where FRACTION_RESIDENTIAL_LAND_VALUE             is null ;

update development_events set GRID_ID          = 0 where GRID_ID          is null ;
update development_events set SCHEDULED_YEAR   = 0 where SCHEDULED_YEAR   is null ;
update development_events set DEVELOPMENT_TYPE_CHANGE_TYPE                 = 0 where DEVELOPMENT_TYPE_CHANGE_TYPE                 is null ;
update development_events set DEVELOPMENT_TYPE_ID       = 0 where DEVELOPMENT_TYPE_ID       is null ;
update development_events set RESIDENTIAL_UNITS_CHANGE_TYPE                = 0 where RESIDENTIAL_UNITS_CHANGE_TYPE                is null ;
update development_events set RESIDENTIAL_UNITS         = 0 where RESIDENTIAL_UNITS         is null ;
update development_events set COMMERCIAL_SQFT_CHANGE_TYPE                  = 0 where COMMERCIAL_SQFT_CHANGE_TYPE                  is null ;
update development_events set COMMERCIAL_SQFT  = 0 where COMMERCIAL_SQFT  is null ;
update development_events set INDUSTRIAL_SQFT_CHANGE_TYPE                  = 0 where INDUSTRIAL_SQFT_CHANGE_TYPE                  is null ;
update development_events set INDUSTRIAL_SQFT  = 0 where INDUSTRIAL_SQFT  is null ;
update development_events set GOVERNMENTAL_SQFT_CHANGE_TYPE                = 0 where GOVERNMENTAL_SQFT_CHANGE_TYPE                is null ;
update development_events set GOVERNMENTAL_SQFT         = 0 where GOVERNMENTAL_SQFT         is null ;
update development_events set RESIDENTIAL_IMPROVEMENT_VALUE_CHANGE_TYPE    = 0 where RESIDENTIAL_IMPROVEMENT_VALUE_CHANGE_TYPE    is null ;
update development_events set RESIDENTIAL_IMPROVEMENT_VALUE                = 0 where RESIDENTIAL_IMPROVEMENT_VALUE                is null ;
update development_events set COMMERCIAL_IMPROVEMENT_VALUE_CHANGE_TYPE     = 0 where COMMERCIAL_IMPROVEMENT_VALUE_CHANGE_TYPE     is null ;
update development_events set COMMERCIAL_IMPROVEMENT_VALUE                 = 0 where COMMERCIAL_IMPROVEMENT_VALUE                 is null ;
update development_events set INDUSTRIAL_IMPROVEMENT_VALUE_CHANGE_TYPE     = 0 where INDUSTRIAL_IMPROVEMENT_VALUE_CHANGE_TYPE     is null ;
update development_events set INDUSTRIAL_IMPROVEMENT_VALUE                 = 0 where INDUSTRIAL_IMPROVEMENT_VALUE                 is null ;
update development_events set GOVERNMENTAL_IMPROVEMENT_VALUE_CHANGE_TYPE   = 0 where GOVERNMENTAL_IMPROVEMENT_VALUE_CHANGE_TYPE   is null ;
update development_events set GOVERNMENTAL_IMPROVEMENT_VALUE               = 0 where GOVERNMENTAL_IMPROVEMENT_VALUE               is null ;
update development_events set FRACTION_RESIDENTIAL_LAND_VALUE_CHANGE_TYPE  = 0 where FRACTION_RESIDENTIAL_LAND_VALUE_CHANGE_TYPE  is null ;
update development_events set FRACTION_RESIDENTIAL_LAND_VALUE              = 0 where FRACTION_RESIDENTIAL_LAND_VALUE              is null ;
update development_events set STARTING_DEVELOPMENT_TYPE_ID                 = 0 where STARTING_DEVELOPMENT_TYPE_ID                 is null ;
update development_events set ENDING_DEVELOPMENT_TYPE_ID = 0 where ENDING_DEVELOPMENT_TYPE_ID is null ;

update employment_home_based_location_choice_model_coefficients set SUB_MODEL_ID     = 0 where SUB_MODEL_ID     is null ;
update employment_home_based_location_choice_model_coefficients set COEFFICIENT_NAME = 0 where COEFFICIENT_NAME is null ;
update employment_home_based_location_choice_model_coefficients set ESTIMATE         = 0 where ESTIMATE         is null ;
update employment_home_based_location_choice_model_coefficients set STANDARD_ERROR   = 0 where STANDARD_ERROR   is null ;
update employment_home_based_location_choice_model_coefficients set T_STATISTIC      = 0 where T_STATISTIC      is null ;
update employment_home_based_location_choice_model_coefficients set P_VALUE          = 0 where P_VALUE          is null ;

update employment_home_based_location_choice_model_estimation_data set JOB_ID  = 0 where JOB_ID  is null ;
update employment_home_based_location_choice_model_estimation_data set ALT_ID  = 0 where ALT_ID  is null ;
update employment_home_based_location_choice_model_estimation_data set GRID_ID = 0 where GRID_ID is null ;
update employment_home_based_location_choice_model_estimation_data set CHOICE  = 0 where CHOICE  is null ;
update employment_home_based_location_choice_model_estimation_data set phiw    = 0 where phiw    is null ;
update employment_home_based_location_choice_model_estimation_data set p05w    = 0 where p05w    is null ;
update employment_home_based_location_choice_model_estimation_data set tt_cbd  = 0 where tt_cbd  is null ;

update employment_non_home_based_location_choice_model_specification set SUB_MODEL_ID     = 0 where SUB_MODEL_ID     is null ;
update employment_non_home_based_location_choice_model_specification set EQUATION_ID      = 0 where EQUATION_ID      is null ;
update employment_non_home_based_location_choice_model_specification set VARIABLE_NAME    = 0 where VARIABLE_NAME    is null ;
update employment_non_home_based_location_choice_model_specification set COEFFICIENT_NAME = 0 where COEFFICIENT_NAME is null ;

update employment_home_based_location_choice_model_variable_names set SHORT_NAME        = 0 where SHORT_NAME        is null ;
update employment_home_based_location_choice_model_variable_names set VARIABLE_NAME     = 0 where VARIABLE_NAME     is null ;
update employment_home_based_location_choice_model_variable_names set COEFFICIENT_NAME  = 0 where COEFFICIENT_NAME  is null ;

update employment_sector_reclass set SECTOR_ID   = 0 where SECTOR_ID   is null ;
update employment_sector_reclass set NAME        = 0 where NAME        is null ;
update employment_sector_reclass set NEW_SECTOR  = 0 where NEW_SECTOR  is null ;

update fazes set FAZ_ID         = 0 where FAZ_ID         is null ;
update fazes set FAZDISTRICT_ID = 0 where FAZDISTRICT_ID is null ;

update geographies set GEOGRAPHY_TYPE_ID      = 0 where GEOGRAPHY_TYPE_ID      is null ;
update geographies set GEOGRAPHY_TYPE_TITLE   = 0 where GEOGRAPHY_TYPE_TITLE   is null ;
update geographies set SHAPEFILE_PATH         = 0 where SHAPEFILE_PATH         is null ;
update geographies set COLUMN_NAME            = 0 where COLUMN_NAME            is null ;
update geographies set POLYGON_ID_VALID_MIN   = 0 where POLYGON_ID_VALID_MIN   is null ;
update geographies set POLYGON_ID_VALID_MAX   = 0 where POLYGON_ID_VALID_MAX   is null ;
update geographies set SHAPEFILE_JOIN_COLUMN  = 0 where SHAPEFILE_JOIN_COLUMN  is null ;

update geography_names set GEOGRAPHY_TYPE_ID  = 0 where GEOGRAPHY_TYPE_ID  is null ;
update geography_names set GEOGRAPHY_ID       = 0 where GEOGRAPHY_ID       is null ;
update geography_names set NAME               = 0 where NAME               is null ;

update gridcell_fractions_in_zones set GRID_ID       = 0 where GRID_ID       is null ;
update gridcell_fractions_in_zones set ZONE_ID       = 0 where ZONE_ID       is null ;
update gridcell_fractions_in_zones set FRACTION      = 0 where FRACTION      is null ;
update gridcell_fractions_in_zones set should_be_one = 0 where should_be_one is null ;

update gridcells set GRID_ID  = 0 where GRID_ID  is null ;
update gridcells set COMMERCIAL_SQFT   = 0 where COMMERCIAL_SQFT   is null ;
update gridcells set GOVERNMENTAL_SQFT = 0 where GOVERNMENTAL_SQFT is null ;
update gridcells set INDUSTRIAL_SQFT   = 0 where INDUSTRIAL_SQFT   is null ;
update gridcells set COMMERCIAL_IMPROVEMENT_VALUE         = 0 where COMMERCIAL_IMPROVEMENT_VALUE         is null ;
update gridcells set INDUSTRIAL_IMPROVEMENT_VALUE         = 0 where INDUSTRIAL_IMPROVEMENT_VALUE         is null ;
update gridcells set GOVERNMENTAL_IMPROVEMENT_VALUE       = 0 where GOVERNMENTAL_IMPROVEMENT_VALUE       is null ;
update gridcells set NONRESIDENTIAL_LAND_VALUE            = 0 where NONRESIDENTIAL_LAND_VALUE            is null ;
update gridcells set RESIDENTIAL_LAND_VALUE               = 0 where RESIDENTIAL_LAND_VALUE               is null ;
update gridcells set RESIDENTIAL_IMPROVEMENT_VALUE        = 0 where RESIDENTIAL_IMPROVEMENT_VALUE        is null ;
update gridcells set RESIDENTIAL_UNITS = 0 where RESIDENTIAL_UNITS is null ;
update gridcells set YEAR_BUILT        = 0 where YEAR_BUILT        is null ;
update gridcells set FRACTION_RESIDENTIAL_LAND            = 0 where FRACTION_RESIDENTIAL_LAND            is null ;
update gridcells set PERCENT_UNDEVELOPABLE                = 0 where PERCENT_UNDEVELOPABLE                is null ;
update gridcells set TOTAL_NONRES_SQFT = 0 where TOTAL_NONRES_SQFT is null ;
update gridcells set TOTAL_UNDEVELOPABLE_SQFT             = 0 where TOTAL_UNDEVELOPABLE_SQFT             is null ;
update gridcells set DEVELOPMENT_TYPE_ID                  = 0 where DEVELOPMENT_TYPE_ID                  is null ;
update gridcells set DISTANCE_TO_ARTERIAL                 = 0 where DISTANCE_TO_ARTERIAL                 is null ;
update gridcells set DISTANCE_TO_HIGHWAY                  = 0 where DISTANCE_TO_HIGHWAY                  is null ;
update gridcells set RELATIVE_X        = 0 where RELATIVE_X        is null ;
update gridcells set RELATIVE_Y        = 0 where RELATIVE_Y        is null ;
update gridcells set PLAN_TYPE_ID      = 0 where PLAN_TYPE_ID      is null ;
update gridcells set PERCENT_WATER     = 0 where PERCENT_WATER     is null ;
update gridcells set PERCENT_WETLAND   = 0 where PERCENT_WETLAND   is null ;
update gridcells set PERCENT_STREAM_BUFFER                = 0 where PERCENT_STREAM_BUFFER                is null ;
update gridcells set PERCENT_FLOODPLAIN = 0 where PERCENT_FLOODPLAIN is null ;
update gridcells set PERCENT_SLOPE     = 0 where PERCENT_SLOPE     is null ;
update gridcells set PERCENT_OPEN_SPACE = 0 where PERCENT_OPEN_SPACE is null ;
update gridcells set PERCENT_PUBLIC_SPACE                 = 0 where PERCENT_PUBLIC_SPACE                 is null ;
update gridcells set PERCENT_ROADS     = 0 where PERCENT_ROADS     is null ;
update gridcells set IS_OUTSIDE_URBAN_GROWTH_BOUNDARY     = 0 where IS_OUTSIDE_URBAN_GROWTH_BOUNDARY     is null ;
update gridcells set IS_INSIDE_NATIONAL_FOREST            = 0 where IS_INSIDE_NATIONAL_FOREST            is null ;
update gridcells set IS_INSIDE_TRIBAL_LAND                = 0 where IS_INSIDE_TRIBAL_LAND                is null ;
update gridcells set IS_INSIDE_MILITARY_BASE              = 0 where IS_INSIDE_MILITARY_BASE              is null ;
update gridcells set ZONE_ID  = 0 where ZONE_ID  is null ;
update gridcells set CITY_ID  = 0 where CITY_ID  is null ;
update gridcells set COUNTY_ID         = 0 where COUNTY_ID         is null ;
update gridcells set PERCENT_AGR_KING  = 0 where PERCENT_AGR_KING  is null ;
update gridcells set ACRES    = 0 where ACRES    is null ;
update gridcells set PERCENT_AGRICULTURAL_PROTECTED_LANDS = 0 where PERCENT_AGRICULTURAL_PROTECTED_LANDS is null ;
update gridcells set PERCENT_FOREST    = 0 where PERCENT_FOREST    is null ;
update gridcells set PERCENT_MINING    = 0 where PERCENT_MINING    is null ;
update gridcells set PERCENT_ROW       = 0 where PERCENT_ROW       is null ;
update gridcells set COMMERCIAL_SQFT_PER_JOB              = 0 where COMMERCIAL_SQFT_PER_JOB              is null ;
update gridcells set INDUSTRIAL_SQFT_PER_JOB              = 0 where INDUSTRIAL_SQFT_PER_JOB              is null ;

update gridcells_in_geography set GRID_ID           = 0 where GRID_ID           is null ;
update gridcells_in_geography set GEOGRAPHY_TYPE_ID = 0 where GEOGRAPHY_TYPE_ID is null ;
update gridcells_in_geography set GEOGRAPHY_ID      = 0 where GEOGRAPHY_ID      is null ;

update household_characteristics_for_hlc set CHARACTERISTIC = 0 where CHARACTERISTIC is null ;
update household_characteristics_for_hlc set MIN            = 0 where MIN            is null ;
update household_characteristics_for_hlc set MAX            = 0 where MAX            is null ;

update household_characteristics_for_ht set CHARACTERISTIC      = 0 where CHARACTERISTIC      is null ;
update household_characteristics_for_ht set CHARACTERISTIC_OPUS = 0 where CHARACTERISTIC_OPUS is null ;
update household_characteristics_for_ht set MIN                 = 0 where MIN                 is null ;
update household_characteristics_for_ht set MAX                 = 0 where MAX                 is null ;

update household_location_choice_model_coefficients set sub_model_id     = 0 where sub_model_id     is null ;
update household_location_choice_model_coefficients set t_statistic      = 0 where t_statistic      is null ;
update household_location_choice_model_coefficients set estimate         = 0 where estimate         is null ;
update household_location_choice_model_coefficients set coefficient_name = 0 where coefficient_name is null ;
update household_location_choice_model_coefficients set standard_error   = 0 where standard_error   is null ;

update household_location_choice_model_estimation_data set HH_ID    = 0 where HH_ID    is null ;
update household_location_choice_model_estimation_data set ALT_ID   = 0 where ALT_ID   is null ;
update household_location_choice_model_estimation_data set GRID_ID  = 0 where GRID_ID  is null ;
update household_location_choice_model_estimation_data set CHOICE   = 0 where CHOICE   is null ;
update household_location_choice_model_estimation_data set cos_in   = 0 where cos_in   is null ;
update household_location_choice_model_estimation_data set incival  = 0 where incival  is null ;
update household_location_choice_model_estimation_data set art      = 0 where art      is null ;
update household_location_choice_model_estimation_data set lduw     = 0 where lduw     is null ;
update household_location_choice_model_estimation_data set phiw_h   = 0 where phiw_h   is null ;
update household_location_choice_model_estimation_data set pliw_l   = 0 where pliw_l   is null ;
update household_location_choice_model_estimation_data set pmiw_m   = 0 where pmiw_m   is null ;
update household_location_choice_model_estimation_data set pmnwmj   = 0 where pmnwmj   is null ;
update household_location_choice_model_estimation_data set pmnwmn   = 0 where pmnwmn   is null ;
update household_location_choice_model_estimation_data set dur_c    = 0 where dur_c    is null ;
update household_location_choice_model_estimation_data set sagefaz  = 0 where sagefaz  is null ;
update household_location_choice_model_estimation_data set schdfaz  = 0 where schdfaz  is null ;
update household_location_choice_model_estimation_data set sincfaz  = 0 where sincfaz  is null ;
update household_location_choice_model_estimation_data set sracfaz  = 0 where sracfaz  is null ;
update household_location_choice_model_estimation_data set ssizfaz  = 0 where ssizfaz  is null ;
update household_location_choice_model_estimation_data set swrkfaz  = 0 where swrkfaz  is null ;
update household_location_choice_model_estimation_data set ut_sov   = 0 where ut_sov   is null ;
update household_location_choice_model_estimation_data set ut_tw    = 0 where ut_tw    is null ;
update household_location_choice_model_estimation_data set yh_hdr   = 0 where yh_hdr   is null ;
update household_location_choice_model_estimation_data set yh_m     = 0 where yh_m     is null ;

update household_location_choice_model_specification set sub_model_id     = 0 where sub_model_id     is null ;
update household_location_choice_model_specification set equation_id      = 0 where equation_id      is null ;
update household_location_choice_model_specification set coefficient_name = 0 where coefficient_name is null ;
update household_location_choice_model_specification set variable_name    = 0 where variable_name    is null ;

update household_location_choice_model_variable_names set SHORT_NAME       = 0 where SHORT_NAME       is null ;
update household_location_choice_model_variable_names set VARIABLE_NAME    = 0 where VARIABLE_NAME    is null ;
update household_location_choice_model_variable_names set COEFFICIENT_NAME = 0 where COEFFICIENT_NAME is null ;

update households set HOUSEHOLD_ID  = 0 where HOUSEHOLD_ID  is null ;
update households set GRID_ID       = 0 where GRID_ID       is null ;
update households set PERSONS       = 0 where PERSONS       is null ;
update households set WORKERS       = 0 where WORKERS       is null ;
update households set AGE_OF_HEAD   = 0 where AGE_OF_HEAD   is null ;
update households set INCOME        = 0 where INCOME        is null ;
update households set CHILDREN      = 0 where CHILDREN      is null ;
update households set RACE_ID       = 0 where RACE_ID       is null ;
update households set CARS          = 0 where CARS          is null ;

update households_for_estimation set HOUSEHOLD_ID  = 0 where HOUSEHOLD_ID  is null ;
update households_for_estimation set CARS          = 0 where CARS          is null ;
update households_for_estimation set INC_CLASS     = 0 where INC_CLASS     is null ;
update households_for_estimation set YEARS_AT_ADD  = 0 where YEARS_AT_ADD  is null ;
update households_for_estimation set PERSONS       = 0 where PERSONS       is null ;
update households_for_estimation set ETHNICITY     = 0 where ETHNICITY     is null ;
update households_for_estimation set AGE_OF_HEAD   = 0 where AGE_OF_HEAD   is null ;
update households_for_estimation set CHILDREN      = 0 where CHILDREN      is null ;
update households_for_estimation set WORKERS       = 0 where WORKERS       is null ;
update households_for_estimation set xcoord        = 0 where xcoord        is null ;
update households_for_estimation set ycoord        = 0 where ycoord        is null ;
update households_for_estimation set grid_id       = 0 where grid_id       is null ;
update households_for_estimation set INCOME        = 0 where INCOME        is null ;
update households_for_estimation set RACE_ID       = 0 where RACE_ID       is null ;

update jobs set JOB_ID        = 0 where JOB_ID        is null ;
update jobs set GRID_ID       = 0 where GRID_ID       is null ;
update jobs set SECTOR_ID     = 0 where SECTOR_ID     is null ;
update jobs set HOME_BASED    = 0 where HOME_BASED    is null ;
update jobs set SIC           = 0 where SIC           is null ;
update jobs set BUILDING_TYPE = 0 where BUILDING_TYPE is null ;
update jobs set IMPUTE_FLAG   = 0 where IMPUTE_FLAG   is null ;

update jobs_for_estimation_home_based set job_id     = 0 where job_id     is null ;
update jobs_for_estimation_home_based set grid_id    = 0 where grid_id    is null ;
update jobs_for_estimation_home_based set sector_id  = 0 where sector_id  is null ;
update jobs_for_estimation_home_based set home_based = 0 where home_based is null ;

update jobs_for_estimation_non_home_based set job_id     = 0 where job_id     is null ;
update jobs_for_estimation_non_home_based set grid_id    = 0 where grid_id    is null ;
update jobs_for_estimation_non_home_based set sector_id  = 0 where sector_id  is null ;
update jobs_for_estimation_non_home_based set home_based = 0 where home_based is null ;

update land_price_model_coefficients set sub_model_id     = 0 where sub_model_id     is null ;
update land_price_model_coefficients set t_statistic      = 0 where t_statistic      is null ;
update land_price_model_coefficients set estimate         = 0 where estimate         is null ;
update land_price_model_coefficients set coefficient_name = 0 where coefficient_name is null ;
update land_price_model_coefficients set standard_error   = 0 where standard_error   is null ;

update land_price_model_estimation_data set GRID_ID  = 0 where GRID_ID  is null ;
update land_price_model_estimation_data set lavurw   = 0 where lavurw   is null ;
update land_price_model_estimation_data set ld_hy    = 0 where ld_hy    is null ;
update land_price_model_estimation_data set lhae1    = 0 where lhae1    is null ;
update land_price_model_estimation_data set lhae0    = 0 where lhae0    is null ;
update land_price_model_estimation_data set lnrsfw   = 0 where lnrsfw   is null ;
update land_price_model_estimation_data set p03w     = 0 where p03w     is null ;
update land_price_model_estimation_data set p02w     = 0 where p02w     is null ;
update land_price_model_estimation_data set phiw     = 0 where phiw     is null ;
update land_price_model_estimation_data set p01w     = 0 where p01w     is null ;
update land_price_model_estimation_data set pliw     = 0 where pliw     is null ;
update land_price_model_estimation_data set pmiw     = 0 where pmiw     is null ;
update land_price_model_estimation_data set pmnw     = 0 where pmnw     is null ;
update land_price_model_estimation_data set p05w     = 0 where p05w     is null ;
update land_price_model_estimation_data set units    = 0 where units    is null ;
update land_price_model_estimation_data set durw     = 0 where durw     is null ;
update land_price_model_estimation_data set tt_cbd   = 0 where tt_cbd   is null ;

update land_price_model_specification set sub_model_id     = 0 where sub_model_id     is null ;
update land_price_model_specification set equation_id      = 0 where equation_id      is null ;
update land_price_model_specification set coefficient_name = 0 where coefficient_name is null ;
update land_price_model_specification set variable_name    = 0 where variable_name    is null ;

update land_price_model_variable_names set SHORT_NAME       = 0 where SHORT_NAME       is null ;
update land_price_model_variable_names set VARIABLE_NAME    = 0 where VARIABLE_NAME    is null ;
update land_price_model_variable_names set COEFFICIENT_NAME = 0 where COEFFICIENT_NAME is null ;

update land_use_events set GRID_ID         = 0 where GRID_ID         is null ;
update land_use_events set SCHEDULED_YEAR  = 0 where SCHEDULED_YEAR  is null ;
update land_use_events set PLAN_TYPE_CHANGE_TYPE              = 0 where PLAN_TYPE_CHANGE_TYPE              is null ;
update land_use_events set PLAN_TYPE_ID    = 0 where PLAN_TYPE_ID    is null ;
update land_use_events set IS_OUTSIDE_UGB_CHANGE_TYPE         = 0 where IS_OUTSIDE_UGB_CHANGE_TYPE         is null ;
update land_use_events set IS_OUTSIDE_UGB  = 0 where IS_OUTSIDE_UGB  is null ;
update land_use_events set PERCENT_WATER_CHANGE_TYPE          = 0 where PERCENT_WATER_CHANGE_TYPE          is null ;
update land_use_events set PERCENT_WATER   = 0 where PERCENT_WATER   is null ;
update land_use_events set PERCENT_FLOODPLAIN_CHANGE_TYPE     = 0 where PERCENT_FLOODPLAIN_CHANGE_TYPE     is null ;
update land_use_events set PERCENT_FLOODPLAIN                 = 0 where PERCENT_FLOODPLAIN                 is null ;
update land_use_events set PERCENT_WETLAND_CHANGE_TYPE        = 0 where PERCENT_WETLAND_CHANGE_TYPE        is null ;
update land_use_events set PERCENT_WETLAND = 0 where PERCENT_WETLAND is null ;
update land_use_events set PERCENT_SLOPE_CHANGE_TYPE          = 0 where PERCENT_SLOPE_CHANGE_TYPE          is null ;
update land_use_events set PERCENT_SLOPE   = 0 where PERCENT_SLOPE   is null ;
update land_use_events set PERCENT_OPEN_SPACE_CHANGE_TYPE     = 0 where PERCENT_OPEN_SPACE_CHANGE_TYPE     is null ;
update land_use_events set PERCENT_OPEN_SPACE                 = 0 where PERCENT_OPEN_SPACE                 is null ;
update land_use_events set PERCENT_PUBLIC_SPACE_CHANGE_TYPE   = 0 where PERCENT_PUBLIC_SPACE_CHANGE_TYPE   is null ;
update land_use_events set PERCENT_PUBLIC_SPACE               = 0 where PERCENT_PUBLIC_SPACE               is null ;
update land_use_events set PERCENT_ROADS_CHANGE_TYPE          = 0 where PERCENT_ROADS_CHANGE_TYPE          is null ;
update land_use_events set PERCENT_ROADS   = 0 where PERCENT_ROADS   is null ;
update land_use_events set PERCENT_STREAM_BUFFER_CHANGE_TYPE  = 0 where PERCENT_STREAM_BUFFER_CHANGE_TYPE  is null ;
update land_use_events set PERCENT_STREAM_BUFFER              = 0 where PERCENT_STREAM_BUFFER              is null ;

update model_variables set VARIABLE_NAME   = 0 where VARIABLE_NAME   is null ;
update model_variables set SHORT_NAME      = 0 where SHORT_NAME      is null ;
update model_variables set DEFINITION      = 0 where DEFINITION      is null ;
update model_variables set DESCRIPTION     = 0 where DESCRIPTION     is null ;
update model_variables set JAVA_CLASS      = 0 where JAVA_CLASS      is null ;
update model_variables set LOG_THIS_VALUE  = 0 where LOG_THIS_VALUE  is null ;

update opus_development_constraints set CONSTRAINT_ID  = 0 where CONSTRAINT_ID  is null ;
update opus_development_constraints set CITY_ID        = 0 where CITY_ID        is null ;
update opus_development_constraints set COUNTY_ID      = 0 where COUNTY_ID      is null ;
update opus_development_constraints set IS_IN_WETLAND  = 0 where IS_IN_WETLAND  is null ;
update opus_development_constraints set IS_OUTSIDE_URBAN_GROWTH_BOUNDARY  = 0 where IS_OUTSIDE_URBAN_GROWTH_BOUNDARY  is null ;
update opus_development_constraints set IS_IN_STREAM_BUFFER               = 0 where IS_IN_STREAM_BUFFER               is null ;
update opus_development_constraints set IS_ON_STEEP_SLOPE                 = 0 where IS_ON_STEEP_SLOPE                 is null ;
update opus_development_constraints set IS_IN_FLOODPLAIN                  = 0 where IS_IN_FLOODPLAIN                  is null ;
update opus_development_constraints set PLAN_TYPE_ID   = 0 where PLAN_TYPE_ID   is null ;
update opus_development_constraints set MIN_UNITS      = 0 where MIN_UNITS      is null ;
update opus_development_constraints set MAX_UNITS      = 0 where MAX_UNITS      is null ;
update opus_development_constraints set MIN_COMMERCIAL_SQFT               = 0 where MIN_COMMERCIAL_SQFT               is null ;
update opus_development_constraints set MAX_COMMERCIAL_SQFT               = 0 where MAX_COMMERCIAL_SQFT               is null ;
update opus_development_constraints set MIN_INDUSTRIAL_SQFT               = 0 where MIN_INDUSTRIAL_SQFT               is null ;
update opus_development_constraints set MAX_INDUSTRIAL_SQFT               = 0 where MAX_INDUSTRIAL_SQFT               is null ;
update opus_development_constraints set MIN_GOVERNMENTAL_SQFT             = 0 where MIN_GOVERNMENTAL_SQFT             is null ;
update opus_development_constraints set MAX_GOVERNMENTAL_SQFT             = 0 where MAX_GOVERNMENTAL_SQFT             is null ;

update plan_types set PLAN_TYPE_ID = 0 where PLAN_TYPE_ID is null ;
update plan_types set NAME         = 0 where NAME         is null ;

update primary_uses set PRIMARY_USE_ID = 0 where PRIMARY_USE_ID is null ;
update primary_uses set NAME           = 0 where NAME           is null ;

update proportion_sector_by_building_type set sector_id            = 0 where sector_id            is null ;
update proportion_sector_by_building_type set name                 = 0 where name                 is null ;
update proportion_sector_by_building_type set building_type        = 0 where building_type        is null ;
update proportion_sector_by_building_type set jobs                 = 0 where jobs                 is null ;
update proportion_sector_by_building_type set building_type_count  = 0 where building_type_count  is null ;
update proportion_sector_by_building_type set proportion           = 0 where proportion           is null ;

update race_names set RACE_ID  = 0 where RACE_ID  is null ;
update race_names set NAME     = 0 where NAME     is null ;
update race_names set MINORITY = 0 where MINORITY is null ;

update residential_land_share_model_coefficients set SUB_MODEL_ID     = 0 where SUB_MODEL_ID     is null ;
update residential_land_share_model_coefficients set COEFFICIENT_NAME = 0 where COEFFICIENT_NAME is null ;
update residential_land_share_model_coefficients set ESTIMATE         = 0 where ESTIMATE         is null ;
update residential_land_share_model_coefficients set STANDARD_ERROR   = 0 where STANDARD_ERROR   is null ;
update residential_land_share_model_coefficients set T_STATISTIC      = 0 where T_STATISTIC      is null ;
update residential_land_share_model_coefficients set P_VALUE          = 0 where P_VALUE          is null ;

update residential_land_share_model_specification set SUB_MODEL_ID     = 0 where SUB_MODEL_ID     is null ;
update residential_land_share_model_specification set EQUATION_ID      = 0 where EQUATION_ID      is null ;
update residential_land_share_model_specification set VARIABLE_NAME    = 0 where VARIABLE_NAME    is null ;
update residential_land_share_model_specification set COEFFICIENT_NAME = 0 where COEFFICIENT_NAME is null ;

update residential_units_for_home_based_jobs set DEVELOPMENT_TYPE_ID = 0 where DEVELOPMENT_TYPE_ID is null ;
update residential_units_for_home_based_jobs set RATIO               = 0 where RATIO               is null ;

update sampling_rates set HLC_SAMPLING_RATE = 0 where HLC_SAMPLING_RATE is null ;
update sampling_rates set ELC_SAMPLING_RATE = 0 where ELC_SAMPLING_RATE is null ;

update scenario_information set END_YEAR            = 0 where END_YEAR            is null ;
update scenario_information set DESCRIPTION         = 0 where DESCRIPTION         is null ;
update scenario_information set PARENT_DATABASE_URL = 0 where PARENT_DATABASE_URL is null ;
update scenario_information set CONTINUATION        = 0 where CONTINUATION        is null ;

update sqft_for_non_home_based_jobs set DEVELOPMENT_TYPE_ID  = 0 where DEVELOPMENT_TYPE_ID  is null ;
update sqft_for_non_home_based_jobs set SQFT                 = 0 where SQFT                 is null ;

update start_year set YEAR = 0 where YEAR is null ;

update target_vacancies set YEAR     = 0 where YEAR     is null ;
update target_vacancies set TARGET_TOTAL_RESIDENTIAL_VACANCY     = 0 where TARGET_TOTAL_RESIDENTIAL_VACANCY     is null ;
update target_vacancies set TARGET_TOTAL_NON_RESIDENTIAL_VACANCY = 0 where TARGET_TOTAL_NON_RESIDENTIAL_VACANCY is null ;

update transition_types set TRANSITION_ID          = 0 where TRANSITION_ID          is null ;
update transition_types set INCLUDE_IN_DEVELOPER_MODEL      = 0 where INCLUDE_IN_DEVELOPER_MODEL      is null ;
update transition_types set STARTING_DEVELOPMENT_TYPE_ID    = 0 where STARTING_DEVELOPMENT_TYPE_ID    is null ;
update transition_types set ENDING_DEVELOPMENT_TYPE_ID      = 0 where ENDING_DEVELOPMENT_TYPE_ID      is null ;
update transition_types set HOUSING_UNITS_MEAN     = 0 where HOUSING_UNITS_MEAN     is null ;
update transition_types set HOUSING_UNITS_STANDARD_DEVIATION = 0 where HOUSING_UNITS_STANDARD_DEVIATION is null ;
update transition_types set HOUSING_UNITS_MIN      = 0 where HOUSING_UNITS_MIN      is null ;
update transition_types set HOUSING_UNITS_MAX      = 0 where HOUSING_UNITS_MAX      is null ;
update transition_types set COMMERCIAL_SQFT_MEAN   = 0 where COMMERCIAL_SQFT_MEAN   is null ;
update transition_types set COMMERCIAL_SQFT_STANDARD_DEVIATION                 = 0 where COMMERCIAL_SQFT_STANDARD_DEVIATION                 is null ;
update transition_types set COMMERCIAL_SQFT_MIN    = 0 where COMMERCIAL_SQFT_MIN    is null ;
update transition_types set COMMERCIAL_SQFT_MAX    = 0 where COMMERCIAL_SQFT_MAX    is null ;
update transition_types set INDUSTRIAL_SQFT_MEAN   = 0 where INDUSTRIAL_SQFT_MEAN   is null ;
update transition_types set INDUSTRIAL_SQFT_STANDARD_DEVIATION                 = 0 where INDUSTRIAL_SQFT_STANDARD_DEVIATION                 is null ;
update transition_types set INDUSTRIAL_SQFT_MIN    = 0 where INDUSTRIAL_SQFT_MIN    is null ;
update transition_types set INDUSTRIAL_SQFT_MAX    = 0 where INDUSTRIAL_SQFT_MAX    is null ;
update transition_types set GOVERNMENTAL_SQFT_MEAN = 0 where GOVERNMENTAL_SQFT_MEAN is null ;
update transition_types set GOVERNMENTAL_SQFT_STANDARD_DEVIATION               = 0 where GOVERNMENTAL_SQFT_STANDARD_DEVIATION               is null ;
update transition_types set GOVERNMENTAL_SQFT_MIN  = 0 where GOVERNMENTAL_SQFT_MIN  is null ;
update transition_types set GOVERNMENTAL_SQFT_MAX  = 0 where GOVERNMENTAL_SQFT_MAX  is null ;
update transition_types set HOUSING_IMPROVEMENT_VALUE_MEAN  = 0 where HOUSING_IMPROVEMENT_VALUE_MEAN  is null ;
update transition_types set HOUSING_IMPROVEMENT_VALUE_STANDARD_DEVIATION       = 0 where HOUSING_IMPROVEMENT_VALUE_STANDARD_DEVIATION       is null ;
update transition_types set HOUSING_IMPROVEMENT_VALUE_MIN   = 0 where HOUSING_IMPROVEMENT_VALUE_MIN   is null ;
update transition_types set HOUSING_IMPROVEMENT_VALUE_MAX   = 0 where HOUSING_IMPROVEMENT_VALUE_MAX   is null ;
update transition_types set COMMERCIAL_IMPROVEMENT_VALUE_MEAN                  = 0 where COMMERCIAL_IMPROVEMENT_VALUE_MEAN                  is null ;
update transition_types set COMMERCIAL_IMPROVEMENT_VALUE_STANDARD_DEVIATION    = 0 where COMMERCIAL_IMPROVEMENT_VALUE_STANDARD_DEVIATION    is null ;
update transition_types set COMMERCIAL_IMPROVEMENT_VALUE_MIN = 0 where COMMERCIAL_IMPROVEMENT_VALUE_MIN is null ;
update transition_types set COMMERCIAL_IMPROVEMENT_VALUE_MAX = 0 where COMMERCIAL_IMPROVEMENT_VALUE_MAX is null ;
update transition_types set INDUSTRIAL_IMPROVEMENT_VALUE_MEAN                  = 0 where INDUSTRIAL_IMPROVEMENT_VALUE_MEAN                  is null ;
update transition_types set INDUSTRIAL_IMPROVEMENT_VALUE_STANDARD_DEVIATION    = 0 where INDUSTRIAL_IMPROVEMENT_VALUE_STANDARD_DEVIATION    is null ;
update transition_types set INDUSTRIAL_IMPROVEMENT_VALUE_MIN = 0 where INDUSTRIAL_IMPROVEMENT_VALUE_MIN is null ;
update transition_types set INDUSTRIAL_IMPROVEMENT_VALUE_MAX = 0 where INDUSTRIAL_IMPROVEMENT_VALUE_MAX is null ;
update transition_types set GOVERNMENTAL_IMPROVEMENT_VALUE_MEAN                = 0 where GOVERNMENTAL_IMPROVEMENT_VALUE_MEAN                is null ;
update transition_types set GOVERNMENTAL_IMPROVEMENT_VALUE_STANDARD_DEVIATION  = 0 where GOVERNMENTAL_IMPROVEMENT_VALUE_STANDARD_DEVIATION  is null ;
update transition_types set GOVERNMENTAL_IMPROVEMENT_VALUE_MIN                 = 0 where GOVERNMENTAL_IMPROVEMENT_VALUE_MIN                 is null ;
update transition_types set GOVERNMENTAL_IMPROVEMENT_VALUE_MAX                 = 0 where GOVERNMENTAL_IMPROVEMENT_VALUE_MAX                 is null ;
update transition_types set YEARS_TO_BUILD         = 0 where YEARS_TO_BUILD         is null ;

update travel_data set FROM_ZONE_ID = 0 where FROM_ZONE_ID is null ;
update travel_data set TO_ZONE_ID   = 0 where TO_ZONE_ID   is null ;
update travel_data set logsum0      = 0 where logsum0      is null ;
update travel_data set logsum1      = 0 where logsum1      is null ;
update travel_data set logsum2      = 0 where logsum2      is null ;

update travel_data_logsum_offsets set logsum0 = 0 where logsum0 is null ;
update travel_data_logsum_offsets set logsum1 = 0 where logsum1 is null ;
update travel_data_logsum_offsets set logsum2 = 0 where logsum2 is null ;

update urbansim_constants set AIRPORT_ZONE_ID   = 0 where AIRPORT_ZONE_ID   is null ;
update urbansim_constants set CBD_ZONE_ID       = 0 where CBD_ZONE_ID       is null ;
update urbansim_constants set WALKING_DISTANCE_CIRCLE_RADIUS                = 0 where WALKING_DISTANCE_CIRCLE_RADIUS                is null ;
update urbansim_constants set YOUNG_AGE         = 0 where YOUNG_AGE         is null ;
update urbansim_constants set PROPERTY_VALUE_TO_ANNUAL_COST_RATIO           = 0 where PROPERTY_VALUE_TO_ANNUAL_COST_RATIO           is null ;
update urbansim_constants set LOW_INCOME_FRACTION        = 0 where LOW_INCOME_FRACTION        is null ;
update urbansim_constants set MID_INCOME_FRACTION        = 0 where MID_INCOME_FRACTION        is null ;
update urbansim_constants set NEAR_ARTERIAL_THRESHOLD    = 0 where NEAR_ARTERIAL_THRESHOLD    is null ;
update urbansim_constants set NEAR_HIGHWAY_THRESHOLD     = 0 where NEAR_HIGHWAY_THRESHOLD     is null ;
update urbansim_constants set PERCENT_COVERAGE_THRESHOLD = 0 where PERCENT_COVERAGE_THRESHOLD is null ;
update urbansim_constants set RECENT_YEARS      = 0 where RECENT_YEARS      is null ;
update urbansim_constants set MAX_PERSONS_PER_HOUSEHOLD_FOR_CONTROL_TOTALS  = 0 where MAX_PERSONS_PER_HOUSEHOLD_FOR_CONTROL_TOTALS  is null ;
update urbansim_constants set CELL_SIZE         = 0 where CELL_SIZE         is null ;
update urbansim_constants set UNITS             = 0 where UNITS             is null ;
update urbansim_constants set LOGIT_CHOICE_SET_SIZE_FOR_ESTIMATION          = 0 where LOGIT_CHOICE_SET_SIZE_FOR_ESTIMATION          is null ;
update urbansim_constants set DEVELOPER_MODEL_ESTIMATION_THRESHOLD_COUNT    = 0 where DEVELOPER_MODEL_ESTIMATION_THRESHOLD_COUNT    is null ;
update urbansim_constants set HLC_ESTIMATION_SAMPLE_FRACTION                = 0 where HLC_ESTIMATION_SAMPLE_FRACTION                is null ;
update urbansim_constants set NUMBER_OF_DEVELOPER_MODEL_HISTORY_YEARS       = 0 where NUMBER_OF_DEVELOPER_MODEL_HISTORY_YEARS       is null ;

update zones set ZONE_ID                = 0 where ZONE_ID                is null ;
update zones set TRAVEL_TIME_TO_CBD     = 0 where TRAVEL_TIME_TO_CBD     is null ;
update zones set TRAVEL_TIME_TO_AIRPORT = 0 where TRAVEL_TIME_TO_AIRPORT is null ;
update zones set FAZ_ID                 = 0 where FAZ_ID                 is null ;

update zones_in_faz set FAZ_ID  = 0 where FAZ_ID  is null ;
update zones_in_faz set ZONE_ID = 0 where ZONE_ID is null ;
