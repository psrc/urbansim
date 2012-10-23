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
        'number_of_jobs = super_raz.number_of_agents(job)',
        'number_of_public_jobs = super_raz.aggregate(mag_zone.job.is_public_job)',
        'number_of_industrial_jobs = super_raz.aggregate(mag_zone.job.is_industrial_job)',
        'number_of_entertainment_jobs = super_raz.aggregate(mag_zone.job.is_entertainment_job)',
        'number_of_homebased_jobs = super_raz.aggregate(mag_zone.job.is_homebased_job)',
        'number_of_nonhomebased_jobs = super_raz.aggregate(mag_zone.job.is_nonhomebased_job)',
        'number_of_office_jobs = super_raz.aggregate(mag_zone.job.is_office_job)',
        # individual sector job totals:
        'number_of_agricultural_jobs = super_raz.aggregate(mag_zone.job.is_agricultural_job)',
        'number_of_mining_jobs = super_raz.aggregate(mag_zone.job.is_mining_job)',
        'number_of_utilities_jobs = super_raz.aggregate(mag_zone.job.is_utilities_job)',
        'number_of_construction_jobs = super_raz.aggregate(mag_zone.job.is_construction_job)',
        'number_of_manufacturing_jobs = super_raz.aggregate(mag_zone.job.is_manufacturing_job)',
        'number_of_wholesale_jobs = super_raz.aggregate(mag_zone.job.is_wholesale_job)',
        'number_of_retail_jobs = super_raz.aggregate(mag_zone.job.is_retail_job)',
        'number_of_transportation_jobs = super_raz.aggregate(mag_zone.job.is_transportation_job)',
        'number_of_information_jobs = super_raz.aggregate(mag_zone.job.is_information_job)',
        'number_of_finance_jobs = super_raz.aggregate(mag_zone.job.is_finance_job)',
        'number_of_realestate_jobs = super_raz.aggregate(mag_zone.job.is_realestate_job)',
        'number_of_professional_jobs = super_raz.aggregate(mag_zone.job.is_professional_job)',
        'number_of_healthcare_jobs = super_raz.aggregate(mag_zone.job.is_healthcare_job)',
        'number_of_accomodation_jobs = super_raz.aggregate(mag_zone.job.is_accomodation_job)',
        'number_of_foodservice_jobs = super_raz.aggregate(mag_zone.job.is_foodservice_job)',
        'number_of_pubfedstate_jobs = super_raz.aggregate(mag_zone.job.is_pubfedstate_job)',
        'number_of_publocal_jobs = super_raz.aggregate(mag_zone.job.is_publocal_job)',
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
           ]

