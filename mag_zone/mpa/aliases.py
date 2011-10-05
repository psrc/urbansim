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
    'mpa_residential_units = mpa.aggregate(building.residential_units)',
    'mpa_jobs_5 = mpa.aggregate(job.sector_id==5)',
    'mpa_total_jobs = mpa.number_of_agents(job)',
    'mpa_county_jobs_5 = mpa.disaggregate(county.county_jobs_5)',
    'mpa_county_total_jobs = mpa.disaggregate(county.county_total_jobs)',
    'lq5 = safe_array_divide((safe_array_divide(mag_zone.mpa.mpa_jobs_5,mag_zone.mpa.mpa_total_jobs)), \
                             (safe_array_divide(mag_zone.mpa.mpa_county_jobs_5,mag_zone.mpa.mpa_county_total_jobs)))',
           ]


