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
        # special cases for super razes:
        'number_of_srazretail_jobs = super_raz.aggregate(mag_zone.job.is_srazretail_job)',
        'number_of_srazindustrial_jobs = super_raz.aggregate(mag_zone.job.is_srazindustrial_job)',
        'number_of_srazoffice_jobs = super_raz.aggregate(mag_zone.job.is_srazoffice_job)',
        'number_of_srazother_jobs = super_raz.aggregate(mag_zone.job.is_srazother_job)',
        'number_of_srazpublic_jobs = super_raz.aggregate(mag_zone.job.is_srazpublic_job)',
        # aggregate sector job totals:
        'sraz_total_unplaced_jobs = super_raz.aggregate(mag_zone.job.is_unplaced)',
        'number_of_jobs = super_raz.number_of_agents(job)',
        'number_of_public_jobs = super_raz.aggregate(mag_zone.job.is_public_job)',
        'number_of_industrial_jobs = super_raz.aggregate(mag_zone.job.is_industrial_job)',
        'number_of_entertainment_jobs = super_raz.aggregate(mag_zone.job.is_entertainment_job)',
        'number_of_homebased_jobs = super_raz.aggregate(mag_zone.job.is_homebased_job)',
        'number_of_nonhomebased_jobs = super_raz.aggregate(mag_zone.job.is_nonhomebased_job)',
        'number_of_office_jobs = super_raz.aggregate(mag_zone.job.is_office_job)',
        # individual sector job totals:
        'number_of_01agricultural_jobs = super_raz.aggregate(mag_zone.job.is_agricultural_job)',
        'number_of_02mining_jobs = super_raz.aggregate(mag_zone.job.is_mining_job)',
        'number_of_03utilities_jobs = super_raz.aggregate(mag_zone.job.is_utilities_job)',
        'number_of_04construction_jobs = super_raz.aggregate(mag_zone.job.is_construction_job)',
        'number_of_05manufacturing_jobs = super_raz.aggregate(mag_zone.job.is_manufacturing_job)',
        'number_of_06wholesale_jobs = super_raz.aggregate(mag_zone.job.is_wholesale_job)',
        'number_of_07retail_jobs = super_raz.aggregate(mag_zone.job.is_retail_job)',
        'number_of_08transportation_jobs = super_raz.aggregate(mag_zone.job.is_transportation_job)',
        'number_of_09information_jobs = super_raz.aggregate(mag_zone.job.is_information_job)',
        'number_of_10finance_jobs = super_raz.aggregate(mag_zone.job.is_finance_job)',
        'number_of_11realestate_jobs = super_raz.aggregate(mag_zone.job.is_realestate_job)',
        'number_of_12professional_jobs = super_raz.aggregate(mag_zone.job.is_professional_job)',
        'number_of_13management_jobs = super_raz.aggregate(mag_zone.job.is_management_job)',
        'number_of_14administrative_jobs = super_raz.aggregate(mag_zone.job.is_admin_support_job)',
        'number_of_15education_jobs = super_raz.aggregate(mag_zone.job.is_educ_svcs_job)',
        'number_of_16healthcare_jobs = super_raz.aggregate(mag_zone.job.is_healthcare_job)',
        'number_of_16medical_jobs = super_raz.aggregate(mag_zone.job.is_healthcare_job)',
        'number_of_17arts_jobs = super_raz.aggregate(mag_zone.job.is_arts_ent_rec_job)',
        'number_of_18accomodation_jobs = super_raz.aggregate(mag_zone.job.is_accomodation_job)',
        'number_of_19foodservice_jobs = super_raz.aggregate(mag_zone.job.is_foodservice_job)',
        'number_of_20other_services_jobs = super_raz.aggregate(mag_zone.job.is_other_svcs_job)',
        'number_of_21pubfedstate_jobs = super_raz.aggregate(mag_zone.job.is_pubfedstate_job)',
        'number_of_22publocal_jobs = super_raz.aggregate(mag_zone.job.is_publocal_job)',
        # individual nhb sector job totals:
        'sraz_number_of_nhb_01agricultural_jobs = super_raz.aggregate(mag_zone.job.is_agricultural_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_02mining_jobs = super_raz.aggregate(mag_zone.job.is_mining_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_03utilities_jobs = super_raz.aggregate(mag_zone.job.is_utilities_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_04construction_jobs = super_raz.aggregate(mag_zone.job.is_construction_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_05manufacturing_jobs = super_raz.aggregate(mag_zone.job.is_manufacturing_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_06wholesale_jobs = super_raz.aggregate(mag_zone.job.is_wholesale_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_07retail_jobs = super_raz.aggregate(mag_zone.job.is_retail_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_08transportation_jobs = super_raz.aggregate(mag_zone.job.is_transportation_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_09information_jobs = super_raz.aggregate(mag_zone.job.is_information_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_10finance_jobs = super_raz.aggregate(mag_zone.job.is_finance_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_11realestate_jobs = super_raz.aggregate(mag_zone.job.is_realestate_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_12professional_jobs = super_raz.aggregate(mag_zone.job.is_professional_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_13management_jobs = super_raz.aggregate(mag_zone.job.is_management_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_14administrative_jobs = super_raz.aggregate(mag_zone.job.is_admin_support_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_15education_jobs = super_raz.aggregate(mag_zone.job.is_educ_svcs_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_16healthcare_jobs = super_raz.aggregate(mag_zone.job.is_healthcare_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_16medical_jobs = super_raz.aggregate(mag_zone.job.is_healthcare_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_17arts_jobs = super_raz.aggregate(mag_zone.job.is_arts_ent_rec_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_18accomodation_jobs = super_raz.aggregate(mag_zone.job.is_accomodation_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_19foodservice_jobs = super_raz.aggregate(mag_zone.job.is_foodservice_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_20other_services_jobs = super_raz.aggregate(mag_zone.job.is_other_svcs_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_21pubfedstate_jobs = super_raz.aggregate(mag_zone.job.is_pubfedstate_job * mag_zone.job.is_nonhomebased_job)',
        'sraz_number_of_nhb_22publocal_jobs = super_raz.aggregate(mag_zone.job.is_publocal_job * mag_zone.job.is_nonhomebased_job)',
        # individual hb sector job totals:
        'sraz_number_of_hb_01agricultural_jobs = super_raz.aggregate(mag_zone.job.is_agricultural_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_02mining_jobs = super_raz.aggregate(mag_zone.job.is_mining_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_03utilities_jobs = super_raz.aggregate(mag_zone.job.is_utilities_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_04construction_jobs = super_raz.aggregate(mag_zone.job.is_construction_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_05manufacturing_jobs = super_raz.aggregate(mag_zone.job.is_manufacturing_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_06wholesale_jobs = super_raz.aggregate(mag_zone.job.is_wholesale_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_07retail_jobs = super_raz.aggregate(mag_zone.job.is_retail_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_08transportation_jobs = super_raz.aggregate(mag_zone.job.is_transportation_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_09information_jobs = super_raz.aggregate(mag_zone.job.is_information_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_10finance_jobs = super_raz.aggregate(mag_zone.job.is_finance_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_11realestate_jobs = super_raz.aggregate(mag_zone.job.is_realestate_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_12professional_jobs = super_raz.aggregate(mag_zone.job.is_professional_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_13management_jobs = super_raz.aggregate(mag_zone.job.is_management_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_14administrative_jobs = super_raz.aggregate(mag_zone.job.is_admin_support_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_15education_jobs = super_raz.aggregate(mag_zone.job.is_educ_svcs_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_16healthcare_jobs = super_raz.aggregate(mag_zone.job.is_healthcare_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_16medical_jobs = super_raz.aggregate(mag_zone.job.is_healthcare_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_17arts_jobs = super_raz.aggregate(mag_zone.job.is_arts_ent_rec_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_18accomodation_jobs = super_raz.aggregate(mag_zone.job.is_accomodation_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_19foodservice_jobs = super_raz.aggregate(mag_zone.job.is_foodservice_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_20other_services_jobs = super_raz.aggregate(mag_zone.job.is_other_svcs_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_21pubfedstate_jobs = super_raz.aggregate(mag_zone.job.is_pubfedstate_job * mag_zone.job.is_homebased_job)',
        'sraz_number_of_hb_22publocal_jobs = super_raz.aggregate(mag_zone.job.is_publocal_job * mag_zone.job.is_homebased_job)',
        # population related:
        'population = super_raz.number_of_agents(person)',
        'average_population_age = super_raz.aggregate(person.age, function=mean)',
        'median_population_age = super_raz.aggregate(person.age, function=median)',
        'number_of_children = super_raz.aggregate(where(person.age < 17, 1,0))',
        'population_with_less_than_high_school_diploma = super_raz.aggregate(mag_zone.person.less_than_high_school_diploma)',
        'population_with_at_least_high_school_diploma = super_raz.aggregate(mag_zone.person.at_least_high_school_diploma)',
        'population_with_at_least_associates_degree = super_raz.aggregate(mag_zone.person.at_least_associates_degree)',
        'population_with_at_least_bachelors_degree = super_raz.aggregate(mag_zone.person.at_least_bachelors_degree)',
        'population_with_at_least_masters_degree = super_raz.aggregate(mag_zone.person.at_least_masters_degree)',
        'average_adult_education = super_raz.aggregate(mag_zone.person.is_adult*person.education, function=mean)',
        'seasonal_pop = super_raz.aggregate(household.is_seasonal)',
        # household related:
        'sraz_total_unplaced_households = super_raz.aggregate(mag_zone.household.is_unplaced)',
        'number_of_hh_age_of_head_over_55 = super_raz.aggregate(mag_zone.household.hh_head_over_55)',
        'average_household_income = super_raz.aggregate(household.income, function=mean)',
        'median_household_income = super_raz.aggregate(household.income, function=median)',
        'number_of_households = super_raz.number_of_agents(household)',
        'percent_hh_age_of_head_over_55 = super_raz.aggregate(safe_array_divide(mag_zone.super_raz.number_of_hh_age_of_head_over_55, mag_zone.super_raz.number_of_households))',
        'super_raz_hh_inc_quint01 = super_raz.aggregate(mag_zone.household.income_quintiles==1)',
        'super_raz_hh_inc_quint02 = super_raz.aggregate(mag_zone.household.income_quintiles==2)',
        'super_raz_hh_inc_quint03 = super_raz.aggregate(mag_zone.household.income_quintiles==3)',
        'super_raz_hh_inc_quint04 = super_raz.aggregate(mag_zone.household.income_quintiles==4)',
        'super_raz_hh_inc_quint05 = super_raz.aggregate(mag_zone.household.income_quintiles==5)',
        'super_raz_hh_age_of_head_under_25 = super_raz.aggregate(mag_zone.household.age_of_head_under_25)',
        'super_raz_hh_age_of_head_26_35 = super_raz.aggregate(mag_zone.household.age_of_head_26_35)',
        'super_raz_hh_age_of_head_36_45 = super_raz.aggregate(mag_zone.household.age_of_head_36_45)',
        'super_raz_hh_age_of_head_46_55 = super_raz.aggregate(mag_zone.household.age_of_head_46_55)',
        'super_raz_hh_age_of_head_56_65 = super_raz.aggregate(mag_zone.household.age_of_head_56_65)',
        'super_raz_hh_age_of_head_66_up = super_raz.aggregate(mag_zone.household.age_of_head_66_up)',
        # other indicators
        'sraz_number_of_residential_units = super_raz.aggregate(building.residential_units)',
        'sraz_residential_vacancy_rate = 1-(safe_array_divide(mag_zone.super_raz.number_of_households,mag_zone.super_raz.sraz_number_of_residential_units))',
        'sraz_vacant_residential_units = super_raz.aggregate(mag_zone.building.vacant_residential_units_with_negatives)',
        'sraz_developable_residential_units_capacity = super_raz.aggregate(urbansim_zone.building.developable_residential_units_capacity)',
           ]

