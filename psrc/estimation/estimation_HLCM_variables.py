# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

specification ={
         -2:   
            [
#            "ln(urbansim.gridcell.housing_cost)",
            ("urbansim.household_x_gridcell.cost_to_income_ratio", "RCI"),
            ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#            "urbansim.household_x_gridcell.ln_income_less_housing_cost",
#            "urbansim.gridcell.travel_time_to_CBD",
#            "urbansim.gridcell.acres_open_space_within_walking_distance",
#            ("urbansim.household_x_gridcell.income_and_ln_improvement_value_per_unit","IIMPPU"), 
#            ('ln(urbansim.gridcell.average_income_within_walking_distance)','LAIW'),
#            ('urbansim.gridcell.percent_water', 'PWATER'),
            ("urbansim.gridcell.ln_residential_units","LDU"),
#            ('urbansim.gridcell.percent_developed_within_walking_distance', 'PDEVW'),
#            ('urbansim.gridcell.percent_open_space_within_walking_distance','POPENW'), 
#            ("urbansim.gridcell.ln_residential_units_within_walking_distance","LUW"),
            ("urbansim.gridcell.ln_service_sector_employment_within_walking_distance","LNSEW"),
#            ("urbansim.gridcell.ln_basic_sector_employment_within_walking_distance","LNBEW"),
#            ("urbansim.gridcell.ln_retail_sector_employment_within_walking_distance","LNREW"),
            ("psrc.household_x_gridcell.ln_retail_sector_employment_within_walking_distance_if_has_less_cars_than_workers","LRETWCW"),
            ("urbansim.household_x_gridcell.percent_high_income_households_within_walking_distance_if_high_income","HIHIW"),
            ("urbansim.household_x_gridcell.percent_low_income_households_within_walking_distance_if_low_income","LILIW"),
            ("urbansim.household_x_gridcell.percent_mid_income_households_within_walking_distance_if_mid_income", "MIMIW"),
            ("urbansim.household_x_gridcell.percent_minority_households_within_walking_distance_if_minority","MPMW"),
            ("urbansim.household_x_gridcell.percent_minority_households_within_walking_distance_if_not_minority","NMPMW"),
            ("urbansim.household_x_gridcell.residential_units_when_household_has_children","RUCH"),
            ("urbansim.household_x_gridcell.young_household_in_high_density_residential","YHHD"),
            ("urbansim.household_x_gridcell.young_household_in_mixed_use","YHMIX"),
            ("urbansim.household_x_gridcell.same_household_age_in_faz","SAGEFAZ"),
            ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
            ('LNE40MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_40_minutes_travel_time_hbw_am_transit_walk))','LNE40MTW'),
            ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
             ]
    }
