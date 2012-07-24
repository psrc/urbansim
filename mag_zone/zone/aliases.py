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
    'number_of_households = zone.number_of_agents(household)',
    'number_of_jobs = zone.number_of_agents(job)',    
    'total_households_and_jobs = mag_zone.zone.number_of_households + mag_zone.zone.number_of_jobs',
    'bldg_sqft_constructed_this_year = clip_to_zero(zone.aggregate(mag_zone.building.bldg_sqft_constructed_this_year))',
    'locationid = zone.zone_id - 100',
           ]
