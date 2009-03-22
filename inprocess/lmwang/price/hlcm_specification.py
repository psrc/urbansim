# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

##this is a copy from inprocess/psrc_parcel/hlcm_parcel_specification
#define submarket by zone x building_type
variable_aliases = [    
    "lnempden=(ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_per_acre))).astype(float32)",
    "lnpopden=(ln(building.disaggregate(urbansim_parcel.zone.population_per_acre))).astype(float32)",
    "ln_parcel_sf_per_unit = ln(urbansim_parcel.building.parcel_sqft_per_unit)",
    "is_low_income_x_is_condo_residential = urbansim.household.is_low_income * urbansim.building.is_condo_residential",
    "is_low_income_x_is_multi_family_residential = urbansim.household.is_low_income * urbansim.building.is_multi_family_residential",
    "less_than_2_persons_x_is_not_single_family_residential = (household.persons < 2) * numpy.logical_not(urbansim.building.is_single_family_residential)",
    "ln_income_x_ln_avg_value_per_unit = ln(household.income) * ln(urbansim_parcel.building.unit_price)",
    "ln_income_less_price_per_unit = ln_bounded(household.income - (urbansim_parcel.building.unit_price/10.)*urbansim_parcel.building.building_sqft)",
    "workers_ln_emp_30min_hbw_drive_alone =  household.workers * building.disaggregate(ln_bounded(urbansim_parcel.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
    "gcdacbd_1person= (household.persons==1) * building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
    "ln_supply = ln_bounded(building.disaggregate(submarket.supply))"
]

specification = {}

specification = {
        "_definition_": variable_aliases,
        -2:   #submodel_id
            [
            #("urbansim_parcel.household_x_building.ln_sampling_probability_for_bias_correction_mnl_vacant_supply", "bias", 1),
            "ln_supply",    
            "lnempden",
            "lnpopden",
            "ln_parcel_sf_per_unit",
#            "is_low_income_x_is_condo_residential",
            "is_low_income_x_is_multi_family_residential",
            "less_than_2_persons_x_is_not_single_family_residential",
            #"ln_income_x_ln_avg_value_per_unit",
            "ln_income_less_price_per_unit",
            "workers_ln_emp_30min_hbw_drive_alone",
            "gcdacbd_1person",

            ],
            
    }
