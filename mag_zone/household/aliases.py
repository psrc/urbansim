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
    'taz2012_id = household.disaggregate(building.disaggregate(zone.taz2012_id))',
    'raz2012_id = household.disaggregate(building.disaggregate(zone.raz2012_id))',
    'zone_id = household.disaggregate(building.disaggregate(zone.zone_id))',
    'pseudo_blockgroup_id = household.disaggregate(building.disaggregate(zone.pseudo_blockgroup_id))',
    'census_place_id = household.disaggregate(building.disaggregate(zone.census_place_id))',
    'raz_id = household.disaggregate(building.disaggregate(zone.raz2012_id))',
    'county_id = household.disaggregate(building.disaggregate(zone.county_id))',
    'synthetic_household_id = household.household_id',
           ]
