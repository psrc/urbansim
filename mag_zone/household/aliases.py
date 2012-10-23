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
    # household attributes
    'persons = household.number_of_agents(person)',
    'age_of_the_youngest = household.aggregate(person.age, function=minimum)',
    'age_of_head = household.aggregate(person.age * mag_zone.person.head_of_hh)',
    'age_of_head_under_25 = household.age_of_head<26',
    'age_of_head_26_35 = numpy.logical_and(household.age_of_head>25, household.age_of_head<36)',
    'age_of_head_36_45 = numpy.logical_and(household.age_of_head>35, household.age_of_head<46)',
    'age_of_head_46_55 = numpy.logical_and(household.age_of_head>45, household.age_of_head<56)',
    'age_of_head_56_65 = numpy.logical_and(household.age_of_head>55, household.age_of_head<66)',
    'age_of_head_66_up = household.age_of_head>65',
    'in_income_quintile01 = mag_zone.household.income_quintiles==1',
    'in_income_quintile02 = mag_zone.household.income_quintiles==2',
    'in_income_quintile03 = mag_zone.household.income_quintiles==3',
    'in_income_quintile04 = mag_zone.household.income_quintiles==4',
    'in_income_quintile05 = mag_zone.household.income_quintiles==5',
    'children = household.aggregate(mag_zone.person.is_child)',
    'income_greater_than_100k = household.income>99999',
    'income_greater_than_200k = household.income>199999',
    'income_greater_than_500k = household.income>499999',
    'number_of_vehicles0 = household.number_of_vehicles==0',
    'number_of_vehicles1 = household.number_of_vehicles==1',
    'number_of_vehicles2 = household.number_of_vehicles==2',
    'number_of_vehicles3 = household.number_of_vehicles==3',
    'number_of_vehicles4up = household.number_of_vehicles>3',
    'is_seasonal = household.is_seasonal==1',
    'is_seasonal_and_all_pp_over_55 = numpy.logical_and(mag_zone.household.is_seasonal, mag_zone.household.age_of_the_youngest>54)',
    'is_seasonal_and_hh_head_over_55 = numpy.logical_and(mag_zone.household.is_seasonal, mag_zone.household.age_of_head>54)',
    'all_pp_over_55 = mag_zone.household.age_of_the_youngest>54',
    'hh_head_over_55 = mag_zone.household.age_of_head>54',
    # households by geographies:
    'tazi03_id = household.disaggregate(building.disaggregate(zone.tazi03_id))',
    'razi03_id = household.disaggregate(building.disaggregate(zone.razi03_id))',
    'mpa_id = household.disaggregate(building.disaggregate(zone.mpa_id))',
    'mpa_id = household.disaggregate(raz2012.mpa_id)',
    'taz2012_id = household.disaggregate(building.disaggregate(zone.taz2012_id))',
    'raz2012_id = household.disaggregate(building.disaggregate(zone.raz2012_id))',
    'super_raz_id = household.disaggregate(building.disaggregate(zone.super_raz_id))',
    'zone_id = household.disaggregate(building.disaggregate(zone.zone_id))',
    'pseudo_blockgroup_id = household.disaggregate(building.disaggregate(zone.pseudo_blockgroup_id))',
    'census_place_id = household.disaggregate(building.disaggregate(zone.census_place_id))',
    'raz_id = household.disaggregate(building.disaggregate(zone.raz2012_id))',
    'county_id = household.disaggregate(building.disaggregate(zone.county_id))',
    'synthetic_household_id = household.household_id',
    'year_built = household.disaggregate(building.year_built)',
    'yrbuilt = 0 * (household.household_id>0) + ' + \
              '1 * (1999 <= mag_zone.household.year_built) + ' + \
              '2 * ((1995 <= mag_zone.household.year_built) & (mag_zone.household.year_built <= 1998)) + ' + \
              '3 * ((1990 <= mag_zone.household.year_built) & (mag_zone.household.year_built <= 1994)) + ' + \
              '4 * ((1980 <= mag_zone.household.year_built) & (mag_zone.household.year_built <= 1989)) + ' + \
              '5 * ((1970 <= mag_zone.household.year_built) & (mag_zone.household.year_built <= 1979)) + ' + \
              '6 * ((1960 <= mag_zone.household.year_built) & (mag_zone.household.year_built <= 1969)) + ' + \
              '7 * ((1950 <= mag_zone.household.year_built) & (mag_zone.household.year_built <= 1959)) + ' + \
              '8 * ((1940 <= mag_zone.household.year_built) & (mag_zone.household.year_built <= 1949)) + ' + \
              '9 * (mag_zone.household.year_built <= 1939)',

    'sparent = ((mag_zone.household.persons - mag_zone.household.children) == 1) & (household.aggregate(numpy.in1d(person.relate, (1, 2)))==1) & (mag_zone.household.children >= 1)',
    'mpa_abbr = household.disaggregate(mpa.mpa_abbreviation, intermediates=[zone, building])',
    "rur = numpy.in1d(mag_zone.household.mpa_abbr, ('GI', 'QC')).astype('i')",
    "urb = numpy.in1d(mag_zone.household.mpa_abbr, ('CH')).astype('i')",
           ]
