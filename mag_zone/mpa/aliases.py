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
        'number_of_jobs = mpa.number_of_agents(job)',
        'number_of_public_jobs = mpa.aggregate(mag_zone.job.is_public_job)',
        'number_of_industrial_jobs = mpa.aggregate(mag_zone.job.is_industrial_job)',
        'number_of_entertainment_jobs = mpa.aggregate(mag_zone.job.is_entertainment_job)',
        'number_of_homebased_jobs = mpa.aggregate(mag_zone.job.is_homebased_job)',
        'number_of_office_jobs = mpa.aggregate(mag_zone.job.is_office_job)',
        # individual sector job totals:
        'number_of_agricultural_jobs = mpa.aggregate(mag_zone.job.is_agricultural_job)',
        'number_of_mining_jobs = mpa.aggregate(mag_zone.job.is_mining_job)',
        'number_of_utilities_jobs = mpa.aggregate(mag_zone.job.is_utilities_job)',
        'number_of_construction_jobs = mpa.aggregate(mag_zone.job.is_construction_job)',
        'number_of_manufacturing_jobs = mpa.aggregate(mag_zone.job.is_manufacturing_job)',
        'number_of_wholesale_jobs = mpa.aggregate(mag_zone.job.is_wholesale_job)',
        'number_of_retail_jobs = mpa.aggregate(mag_zone.job.is_retail_job)',
        'number_of_transportation_jobs = mpa.aggregate(mag_zone.job.is_transportation_job)',
        'number_of_information_jobs = mpa.aggregate(mag_zone.job.is_information_job)',
        'number_of_finance_jobs = mpa.aggregate(mag_zone.job.is_finance_job)',
        'number_of_realestate_jobs = mpa.aggregate(mag_zone.job.is_realestate_job)',
        'number_of_professional_jobs = mpa.aggregate(mag_zone.job.is_professional_job)',
        'number_of_healthcare_jobs = mpa.aggregate(mag_zone.job.is_healthcare_job)',
        'number_of_accomodation_jobs = mpa.aggregate(mag_zone.job.is_accomodation_job)',
        'number_of_foodservice_jobs = mpa.aggregate(mag_zone.job.is_foodservice_job)',
        'number_of_pubfedstate_jobs = mpa.aggregate(mag_zone.job.is_pubfedstate_job)',
        'number_of_publocal_jobs = mpa.aggregate(mag_zone.job.is_publocal_job)',
        # population related:
        'population = mpa.number_of_agents(person)',
        'average_population_age = mpa.aggregate(person.age, function=mean)',
        'median_population_age = mpa.aggregate(person.age, function=median)',
        'number_of_children = mpa.aggregate(where(person.age < 17, 1,0))',
        'population_with_less_than_high_school_diploma = mpa.aggregate(mag_zone.person.less_than_high_school_diploma)',
        'population_with_at_least_high_school_diploma = mpa.aggregate(mag_zone.person.at_least_high_school_diploma)',
        'population_with_at_least_associates_degree = mpa.aggregate(mag_zone.person.at_least_associates_degree)',
        'population_with_at_least_bachelors_degree = mpa.aggregate(mag_zone.person.at_least_bachelors_degree)',
        'population_with_at_least_masters_degree = mpa.aggregate(mag_zone.person.at_least_masters_degree)',
        'average_adult_education = mpa.aggregate(mag_zone.person.is_adult*person.education, function=mean)',
        # household related:
        'number_of_hh_age_of_head_over_55 = mpa.aggregate(mag_zone.household.hh_head_over_55)',
        'number_of_households = mpa.number_of_agents(household)',
        'percent_hh_age_of_head_over_55 = mpa.aggregate(safe_array_divide(mag_zone.mpa.number_of_hh_age_of_head_over_55, mag_zone.mpa.number_of_households))',
        'number_of_hh_size_1 = mpa.aggregate(household.persons==1)',
        'number_of_hh_size_2 = mpa.aggregate(household.persons==2)',
        'number_of_hh_size_3 = mpa.aggregate(household.persons==3)',
        'number_of_hh_size_4 = mpa.aggregate(household.persons==4)',
        'number_of_hh_size_5 = mpa.aggregate(household.persons==5)',
        'number_of_hh_size_6 = mpa.aggregate(household.persons==6)',
        'number_of_hh_size_7up = mpa.aggregate(household.persons>6)',
        'number_of_hh_1_child = mpa.aggregate(household.children==1)',
        'number_of_hh_2_children = mpa.aggregate(household.children==2)',
        'number_of_hh_3_children = mpa.aggregate(household.children==3)',
        'number_of_hh_4up_children = mpa.aggregate(household.children>3)',
        'persons_per_hh = mpa.aggregate(household.persons, function=mean)',
        'number_of_hh_0_workers = mpa.aggregate(household.workers==0)',
        'number_of_hh_1_workers = mpa.aggregate(household.workers==1)',
        'number_of_hh_2_workers = mpa.aggregate(household.workers==2)',
        'number_of_hh_3up_workers = mpa.aggregate(household.workers>2)',
        'number_of_hh_0_vehicles = mpa.aggregate(mag_zone.household.number_of_vehicles0)',
        'number_of_hh_1_vehicles = mpa.aggregate(mag_zone.household.number_of_vehicles1)',
        'number_of_hh_2_vehicles = mpa.aggregate(mag_zone.household.number_of_vehicles2)',
        'number_of_hh_3_vehicles = mpa.aggregate(mag_zone.household.number_of_vehicles3)',
        'number_of_hh_4up_vehicles = mpa.aggregate(mag_zone.household.number_of_vehicles4up)',
        'average_household_income = mpa.aggregate(household.income, function=mean)',
        'median_household_income = mpa.aggregate(household.income, function=median)',
        # DU related
        'total_dus = mpa.aggregate(building.residential_units)',
        'total_sfr_dus = mpa.aggregate(mag_zone.building.number_sfr_dus)',
        'total_mfr_dus = mpa.aggregate(mag_zone.building.number_mfr_dus)',
        'total_mh_dus = mpa.aggregate(mag_zone.building.number_mh_dus)',
        'percent_dus_built = safe_array_divide(mag_zone.mpa.total_dus, mpa.aggregate(building.residential_units_capacity))',
        'percent_sfr_dus = safe_array_divide(mag_zone.mpa.total_sfr_dus, mag_zone.mpa.total_dus)',
        'percent_sfr_mh_dus = safe_array_divide((mag_zone.mpa.total_sfr_dus+mag_zone.mpa.total_mh_dus), mag_zone.mpa.total_dus)',
        'percent_mfr_dus = safe_array_divide(mag_zone.mpa.total_mfr_dus, mag_zone.mpa.total_dus)',
        'percent_mh_dus = safe_array_divide(mag_zone.mpa.total_mh_dus, mag_zone.mpa.total_dus)',
        # other indicators
        'jobs_housing_ratio = safe_array_divide(mag_zone.mpa.number_of_jobs, mag_zone.mpa.total_dus)',
        'occupancy_rate = safe_array_divide(mag_zone.mpa.number_of_households, mag_zone.mpa.total_dus)',
        # older v3x expressions:
        'mpa_residential_units = mpa.aggregate(building.residential_units)',
        'mpa_jobs_5 = mpa.aggregate(job.sector_id==5)',
        'mpa_total_jobs = mpa.number_of_agents(job)',
        'mpa_county_jobs_5 = mpa.disaggregate(county.county_jobs_5)',
        'mpa_county_total_jobs = mpa.disaggregate(county.total_jobs)',
        'lq5 = safe_array_divide((safe_array_divide(mag_zone.mpa.mpa_jobs_5,mag_zone.mpa.mpa_total_jobs)), \
                                 (safe_array_divide(mag_zone.mpa.mpa_county_jobs_5,mag_zone.mpa.mpa_county_total_jobs)))',
           ]
