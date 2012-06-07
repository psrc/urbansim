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
    'zone_id = job.disaggregate(building.disaggregate(zone.zone_id))',
    'taz2012_id = job.disaggregate(building.disaggregate(zone.taz2012_id))',
    'mpa_id = job.disaggregate(building.disaggregate(zone.mpa_id))',
    'raz_id = job.disaggregate(building.disaggregate(zone.raz_id))',
    'raz2012_id = job.disaggregate(building.disaggregate(zone.raz2012_id))',
    'county_id = job.disaggregate(building.disaggregate(zone.county_id))',
    'tazi03_id = job.disaggregate(building.disaggregate(zone.tazi03_id))',
    'pseudo_blockgroup_id = job.disaggregate(building.disaggregate(zone.pseudo_blockgroup_id))',
    'census_place_id = job.disaggregate(building.disaggregate(zone.census_place_id))',
    'is_pub_employment = (job.sector_id == 20)',
           ]
