# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

##this is a copy from inprocess/psrc_parcel/hlcm_parcel_specification
#define submarket by zone x building_type
variable_aliases = [
    "lnempden= ln((submarket.disaggregate(urbansim_parcel.zone.number_of_jobs_per_acre)).astype(float32))",
    "lnpopden= ln( (submarket.disaggregate(urbansim_parcel.zone.population_per_acre)).astype(float32))",    
    "ln_avg_parcel_sf_per_unit = ln(submarket.aggregate(urbansim_parcel.building.parcel_sqft_per_unit, function=mean))",
    "is_low_income_x_is_condo_residential = urbansim.household.is_low_income * submarket.residential_building_type_id==82",
    "is_low_income_x_is_multi_family_residential = urbansim.household.is_low_income * submarket.residential_building_type_id == 83",    
    "less_than_2_persons_x_is_not_single_family_residential = (household.persons < 2) * numpy.logical_not(submarket.residential_building_type_id == 81)",
    "ln_income_x_ln_avg_value_per_unit = ln(household.income) * ln(submarket.aggregate(urbansim_parcel.building.unit_price, function=mean))",
    "ln_income_less_price_per_unit = ln_bounded(household.income - submarket.aggregate((urbansim_parcel.building.unit_price/10.)*urbansim_parcel.building.building_sqft, function=mean))",
    "workers_ln_emp_30min_hbw_drive_alone =  household.workers * submarket.disaggregate(ln_bounded(urbansim_parcel.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
    "gcdacbd_1person= (household.persons==1) * submarket.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
]

specification = {}

specification = {
        "_definition_": variable_aliases,
        -2:   #submodel_id
            [
            "lnempden",
            "lnpopden",
            "ln_avg_parcel_sf_per_unit",
#            "is_low_income_x_is_condo_residential",
            "is_low_income_x_is_multi_family_residential",
            "less_than_2_persons_x_is_not_single_family_residential",
            #"ln_income_x_ln_avg_value_per_unit",
            "ln_income_less_price_per_unit",
            "workers_ln_emp_30min_hbw_drive_alone",
            "gcdacbd_1person",

            ],
            
    }
