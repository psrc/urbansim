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
    'age_of_the_youngest = household.aggregate(person.age, function=minimum)',
    'county_id = household.disaggregate(building.disaggregate(zone.county_id))',
    'age_of_head = household.aggregate(person.age * person.head_of_hh)',
    'workers = household.aggregate(mag_zone.person.is_employed)',
    'children = household.aggregate(mag_zone.person.is_child)',
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
           ]