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
        # population related:
        'population = taz2012.number_of_agents(person)',
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
        'percent_hh_age_of_head_over_55 = taz2012.aggregate(safe_array_divide(mag_zone.taz2012.number_of_hh_age_of_head_over_55, mag_zone.taz2012.number_of_households))',
           ]

