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
        'taz_total_non_home_based_jobs = taz2012.aggregate(mag_zone.job.is_homebased_job==0)',
        'taz_total_home_based_jobs = taz2012.aggregate(mag_zone.job.is_homebased_job)',
        'number_of_jobs = taz2012.number_of_agents(job)',
        'number_of_public_jobs = taz2012.aggregate(mag_zone.job.is_public_job)',
        'number_of_industrial_jobs = taz2012.aggregate(mag_zone.job.is_industrial_job)',
        'number_of_entertainment_jobs = taz2012.aggregate(mag_zone.job.is_entertainment_job)',
        'number_of_homebased_jobs = taz2012.aggregate(mag_zone.job.is_homebased_job)',
        'number_of_office_jobs = taz2012.aggregate(mag_zone.job.is_office_job)',
        # individual sector job totals:
        'number_of_agricultural_jobs = taz2012.aggregate(mag_zone.job.is_agricultural_job)',
        'number_of_mining_jobs = taz2012.aggregate(mag_zone.job.is_mining_job)',
        'number_of_utilities_jobs = taz2012.aggregate(mag_zone.job.is_utilities_job)',
        'number_of_construction_jobs = taz2012.aggregate(mag_zone.job.is_construction_job)',
        'number_of_manufacturing_jobs = taz2012.aggregate(mag_zone.job.is_manufacturing_job)',
        'number_of_wholesale_jobs = taz2012.aggregate(mag_zone.job.is_wholesale_job)',
        'number_of_retail_jobs = taz2012.aggregate(mag_zone.job.is_retail_job)',
        'number_of_transportation_jobs = taz2012.aggregate(mag_zone.job.is_transportation_job)',
        'number_of_information_jobs = taz2012.aggregate(mag_zone.job.is_information_job)',
        'number_of_finance_jobs = taz2012.aggregate(mag_zone.job.is_finance_job)',
        'number_of_realestate_jobs = taz2012.aggregate(mag_zone.job.is_realestate_job)',
        'number_of_professional_jobs = taz2012.aggregate(mag_zone.job.is_professional_job)',
        'number_of_healthcare_jobs = taz2012.aggregate(mag_zone.job.is_healthcare_job)',
        'number_of_accomodation_jobs = taz2012.aggregate(mag_zone.job.is_accomodation_job)',
        'number_of_foodservice_jobs = taz2012.aggregate(mag_zone.job.is_foodservice_job)',
        'number_of_pubfedstate_jobs = taz2012.aggregate(mag_zone.job.is_pubfedstate_job)',
        'number_of_publocal_jobs = taz2012.aggregate(mag_zone.job.is_publocal_job)',
        # individual nhb sector job totals:
        'taz_number_of_01agricultural_jobs = taz2012.aggregate(mag_zone.job.is_agricultural_job)',
        'taz_number_of_02mining_jobs = taz2012.aggregate(mag_zone.job.is_mining_job)',
        'taz_number_of_03utilities_jobs = taz2012.aggregate(mag_zone.job.is_utilities_job)',
        'taz_number_of_04construction_jobs = taz2012.aggregate(mag_zone.job.is_construction_job)',
        'taz_number_of_05manufacturing_jobs = taz2012.aggregate(mag_zone.job.is_manufacturing_job)',
        'taz_number_of_06wholesale_jobs = taz2012.aggregate(mag_zone.job.is_wholesale_job)',
        'taz_number_of_07retail_jobs = taz2012.aggregate(mag_zone.job.is_retail_job)',
        'taz_number_of_08transportation_jobs = taz2012.aggregate(mag_zone.job.is_transportation_job)',
        'taz_number_of_09information_jobs = taz2012.aggregate(mag_zone.job.is_information_job)',
        'taz_number_of_10finance_jobs = taz2012.aggregate(mag_zone.job.is_finance_job)',
        'taz_number_of_11realestate_jobs = taz2012.aggregate(mag_zone.job.is_realestate_job)',
        'taz_number_of_12professional_jobs = taz2012.aggregate(mag_zone.job.is_professional_job)',
        'taz_number_of_13management_jobs = taz2012.aggregate(mag_zone.job.is_management_job)',
        'taz_number_of_14administrative_jobs = taz2012.aggregate(mag_zone.job.is_admin_support_job)',
        'taz_number_of_15education_jobs = taz2012.aggregate(mag_zone.job.is_educ_svcs_job)',
        'taz_number_of_16healthcare_jobs = taz2012.aggregate(mag_zone.job.is_healthcare_job)',
        'taz_number_of_16medical_jobs = taz2012.aggregate(mag_zone.job.is_healthcare_job)',
        'taz_number_of_17arts_jobs = taz2012.aggregate(mag_zone.job.is_arts_ent_rec_job)',
        'taz_number_of_18accomodation_jobs = taz2012.aggregate(mag_zone.job.is_accomodation_job)',
        'taz_number_of_19foodservice_jobs = taz2012.aggregate(mag_zone.job.is_foodservice_job)',
        'taz_number_of_20other_services_jobs = taz2012.aggregate(mag_zone.job.is_other_svcs_job)',
        'taz_number_of_21pubfedstate_jobs = taz2012.aggregate(mag_zone.job.is_pubfedstate_job)',
        'taz_number_of_22publocal_jobs = taz2012.aggregate(mag_zone.job.is_publocal_job)',
        # individual nhb sector job totals:
        'taz_number_of_nhb_01agricultural_jobs = taz2012.aggregate(mag_zone.job.is_agricultural_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_02mining_jobs = taz2012.aggregate(mag_zone.job.is_mining_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_03utilities_jobs = taz2012.aggregate(mag_zone.job.is_utilities_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_04construction_jobs = taz2012.aggregate(mag_zone.job.is_construction_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_05manufacturing_jobs = taz2012.aggregate(mag_zone.job.is_manufacturing_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_06wholesale_jobs = taz2012.aggregate(mag_zone.job.is_wholesale_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_07retail_jobs = taz2012.aggregate(mag_zone.job.is_retail_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_08transportation_jobs = taz2012.aggregate(mag_zone.job.is_transportation_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_09information_jobs = taz2012.aggregate(mag_zone.job.is_information_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_10finance_jobs = taz2012.aggregate(mag_zone.job.is_finance_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_11realestate_jobs = taz2012.aggregate(mag_zone.job.is_realestate_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_12professional_jobs = taz2012.aggregate(mag_zone.job.is_professional_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_13management_jobs = taz2012.aggregate(mag_zone.job.is_management_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_14administrative_jobs = taz2012.aggregate(mag_zone.job.is_admin_support_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_15education_jobs = taz2012.aggregate(mag_zone.job.is_educ_svcs_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_16healthcare_jobs = taz2012.aggregate(mag_zone.job.is_healthcare_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_16medical_jobs = taz2012.aggregate(mag_zone.job.is_healthcare_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_17arts_jobs = taz2012.aggregate(mag_zone.job.is_arts_ent_rec_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_18accomodation_jobs = taz2012.aggregate(mag_zone.job.is_accomodation_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_19foodservice_jobs = taz2012.aggregate(mag_zone.job.is_foodservice_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_20other_services_jobs = taz2012.aggregate(mag_zone.job.is_other_svcs_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_21pubfedstate_jobs = taz2012.aggregate(mag_zone.job.is_pubfedstate_job * mag_zone.job.is_nonhomebased_job)',
        'taz_number_of_nhb_22publocal_jobs = taz2012.aggregate(mag_zone.job.is_publocal_job * mag_zone.job.is_nonhomebased_job)',
        # individual hb sector job totals:
        'taz_number_of_hb_01agricultural_jobs = taz2012.aggregate(mag_zone.job.is_agricultural_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_02mining_jobs = taz2012.aggregate(mag_zone.job.is_mining_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_03utilities_jobs = taz2012.aggregate(mag_zone.job.is_utilities_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_04construction_jobs = taz2012.aggregate(mag_zone.job.is_construction_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_05manufacturing_jobs = taz2012.aggregate(mag_zone.job.is_manufacturing_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_06wholesale_jobs = taz2012.aggregate(mag_zone.job.is_wholesale_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_07retail_jobs = taz2012.aggregate(mag_zone.job.is_retail_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_08transportation_jobs = taz2012.aggregate(mag_zone.job.is_transportation_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_09information_jobs = taz2012.aggregate(mag_zone.job.is_information_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_10finance_jobs = taz2012.aggregate(mag_zone.job.is_finance_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_11realestate_jobs = taz2012.aggregate(mag_zone.job.is_realestate_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_12professional_jobs = taz2012.aggregate(mag_zone.job.is_professional_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_13management_jobs = taz2012.aggregate(mag_zone.job.is_management_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_14administrative_jobs = taz2012.aggregate(mag_zone.job.is_admin_support_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_15education_jobs = taz2012.aggregate(mag_zone.job.is_educ_svcs_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_16healthcare_jobs = taz2012.aggregate(mag_zone.job.is_healthcare_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_16medical_jobs = taz2012.aggregate(mag_zone.job.is_healthcare_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_17arts_jobs = taz2012.aggregate(mag_zone.job.is_arts_ent_rec_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_18accomodation_jobs = taz2012.aggregate(mag_zone.job.is_accomodation_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_19foodservice_jobs = taz2012.aggregate(mag_zone.job.is_foodservice_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_20other_services_jobs = taz2012.aggregate(mag_zone.job.is_other_svcs_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_21pubfedstate_jobs = taz2012.aggregate(mag_zone.job.is_pubfedstate_job * mag_zone.job.is_homebased_job)',
        'taz_number_of_hb_22publocal_jobs = taz2012.aggregate(mag_zone.job.is_publocal_job * mag_zone.job.is_homebased_job)',
        # population related:
        'population = taz2012.number_of_agents(person)',
        'taz_total_seasonal_population = taz2012.aggregate(household.persons*mag_zone.household.is_seasonal)',
        'taz_total_resident_population = taz2012.aggregate(household.persons*mag_zone.household.is_seasonal==0)',
        'average_population_age = taz2012.aggregate(person.age, function=mean)',
        'median_population_age = taz2012.aggregate(person.age, function=median)',
        'number_of_children = taz2012.aggregate(where(person.age < 17, 1,0))',
        'population_with_less_than_high_school_diploma = taz2012.aggregate(mag_zone.person.less_than_high_school_diploma)',
        'population_with_at_least_high_school_diploma = taz2012.aggregate(mag_zone.person.at_least_high_school_diploma)',
        'population_with_at_least_associates_degree = taz2012.aggregate(mag_zone.person.at_least_associates_degree)',
        'population_with_at_least_bachelors_degree = taz2012.aggregate(mag_zone.person.at_least_bachelors_degree)',
        'population_with_at_least_masters_degree = taz2012.aggregate(mag_zone.person.at_least_masters_degree)',
        'average_adult_education = taz2012.aggregate(mag_zone.person.is_adult*person.education, function=mean)',
        # household related:
        'number_of_hh_age_of_head_over_55 = taz2012.aggregate(mag_zone.household.hh_head_over_55)',
        'average_household_income = taz2012.aggregate(household.income, function=mean)',
        'median_household_income = taz2012.aggregate(household.income, function=median)',
        'number_of_households = taz2012.number_of_agents(household)',
        'taz_total_seasonal_households = taz2012.aggregate(mag_zone.household.is_seasonal)',
        'taz_total_resident_households = taz2012.aggregate(mag_zone.household.is_seasonal==0)',
        'percent_hh_age_of_head_over_55 = taz2012.aggregate(safe_array_divide(mag_zone.taz2012.number_of_hh_age_of_head_over_55, mag_zone.taz2012.number_of_households))',
        # building related:
        'taz_dus_constructed_this_year = taz2012.aggregate(mag_zone.building.bldg_du_constructed_this_year)',
        'taz_total_dus = taz2012.aggregate(building.residential_units)',
        'taz_residential_units_percent_buildout = mag_zone.taz2012.taz_total_dus/taz2012.aggregate(zone.res_units_capacity_2100)',
           ]

