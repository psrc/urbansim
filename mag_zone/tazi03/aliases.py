#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
        # aggregate sector job totals:
        "number_of_jobs = tazi03.number_of_agents(job)",
        "number_of_public_jobs = tazi03.aggregate(job.sector_id==21)+tazi03.aggregate(job.sector_id==22)",
        "number_of_industrial_jobs = tazi03.aggregate(job.sector_id==2)+tazi03.aggregate(job.sector_id==5)+tazi03.aggregate(job.sector_id==6)+tazi03.aggregate(job.sector_id==8)",
        "number_of_entertainment_jobs = tazi03.aggregate(job.sector_id==7)+tazi03.aggregate(job.sector_id==18)+tazi03.aggregate(job.sector_id==19)",
        "number_of_homebased_jobs = tazi03.aggregate(job.home_based==1)",
        'number_of_office_jobs = tazi03.aggregate(mag_zone.job.is_office_job)',
        # individual sector job totals:
        'number_of_agricultural_jobs = tazi03.aggregate(mag_zone.job.is_agricultural_job)',
        'number_of_mining_jobs = tazi03.aggregate(mag_zone.job.is_mining_job)',
        'number_of_utilities_jobs = tazi03.aggregate(mag_zone.job.is_utilities_job)',
        'number_of_construction_jobs = tazi03.aggregate(mag_zone.job.is_construction_job)',
        'number_of_manufacturing_jobs = tazi03.aggregate(mag_zone.job.is_manufacturing_job)',
        'number_of_wholesale_jobs = tazi03.aggregate(mag_zone.job.is_wholesale_job)',
        'number_of_retail_jobs = tazi03.aggregate(mag_zone.job.is_retail_job)',
        'number_of_transportation_jobs = tazi03.aggregate(mag_zone.job.is_transportation_job)',
        'number_of_information_jobs = tazi03.aggregate(mag_zone.job.is_information_job)',
        'number_of_finance_jobs = tazi03.aggregate(mag_zone.job.is_finance_job)',
        'number_of_realestate_jobs = tazi03.aggregate(mag_zone.job.is_realestate_job)',
        'number_of_professional_jobs = tazi03.aggregate(mag_zone.job.is_professional_job)',
        'number_of_healthcare_jobs = tazi03.aggregate(mag_zone.job.is_healthcare_job)',
        'number_of_accomodation_jobs = tazi03.aggregate(mag_zone.job.is_accomodation_job)',
        'number_of_foodservice_jobs = tazi03.aggregate(mag_zone.job.is_foodservice_job)',
        'number_of_pubfedstate_jobs = tazi03.aggregate(mag_zone.job.is_pubfedstate_job)',
        'number_of_publocal_jobs = tazi03.aggregate(mag_zone.job.is_publocal_job)',
        # population related:
        'number_of_pop = tazi03.number_of_agents(person)',
        'average_population_age = tazi03.aggregate(person.age, function=mean)',
        'median_population_age = tazi03.aggregate(person.age, function=median)',
        'number_of_children = tazi03.aggregate(where(person.age < 17, 1,0))',
        'population_with_less_than_high_school_diploma = tazi03.aggregate(mag_zone.person.less_than_high_school_diploma)',
        'population_with_at_least_high_school_diploma = tazi03.aggregate(mag_zone.person.at_least_high_school_diploma)',
        'population_with_at_least_associates_degree = tazi03.aggregate(mag_zone.person.at_least_associates_degree)',
        'population_with_at_least_bachelors_degree = tazi03.aggregate(mag_zone.person.at_least_bachelors_degree)',
        'population_with_at_least_masters_degree = tazi03.aggregate(mag_zone.person.at_least_masters_degree)',
        'average_adult_education = tazi03.aggregate(mag_zone.person.is_adult*person.education, function=mean)',
        # household related:
        'number_of_hh_age_of_head_over_55 = tazi03.aggregate(mag_zone.household.hh_head_over_55)',
        'average_household_income = tazi03.aggregate(household.income, function=mean)',
        'median_household_income = tazi03.aggregate(household.income, function=median)',
        'number_of_households = tazi03.number_of_agents(household)',
        'percent_hh_age_of_head_over_55 = tazi03.aggregate(safe_array_divide(mag_zone.tazi03.number_of_hh_age_of_head_over_55,mag_zone.tazi03.number_of_households))',
        # building related:
        'developable_sf_units_capacity = tazi03.aggregate(where(building.building_type_id == 1,urbansim_zone.building.developable_residential_units_capacity,0))',
        'developable_mf_units_capacity = tazi03.aggregate(where(building.building_type_id == 2,urbansim_zone.building.developable_residential_units_capacity,0))',
        'developable_non_res_capacity = tazi03.aggregate(where(building.building_type_id > 3,urbansim_zone.building.developable_non_residential_sqft_capacity,0))',
        'vacant_res_units = tazi03.aggregate(urbansim_zone.building.vacant_residential_units)',
        'vacant_job_spaces = tazi03.aggregate(urbansim_zone.building.vacant_job_spaces)',                
        ]

