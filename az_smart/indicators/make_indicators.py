#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

# script to produce a number of PSRC indicators -- 
# this illustrates using traits-based configurations programatically


from inprocess.travis.urbansim.indicators.indicator_configuration import IndicatorConfiguration
from inprocess.travis.urbansim.indicators.indicator_configuration_handler_batch_mode import generate_indicators

config = IndicatorConfiguration()
config.dataset_pool_configuration.package_order = ['az_smart', 'urbansim', 'opus_core']

# *** Set up database ***
# use the defaults for mysql hostname, username, and password 
# (the defaults are to get these from environment variables)
#config.database_configuration.database_name = 'PSRC_2000_baseyear'
#config.run_description = '(run 1090 - double highway capacity 11/28/2006)'
config.cache_directory = r'/urbansim_cache/az_smart/run_23.2007_02_05_01_48' #'/workspace/urbansim_cache/az_smart/run_23.2007_02_05_01_48'

#
# When the indicator name includes the year as "%(year)s", it will be replaced
# each year the indicator is computed for.

#request_years is the default years that all the indicators will be computed for.
#each indicator request can optionally have a 'years' key whose value is 
#used instead of request_years for that particular indicator
config.request_years = [2001,2005]
config.requests = [
#                 {'dataset':'district14',
#                  'image_type':'table',
#                  'attribute':'opus_core.func.aggregate(az_smart.zone.population) as population'
#                  },  
#                 {'dataset':'district14',
#                  'image_type':'table',
#                  'attribute':'opus_core.func.aggregate(az_smart.zone.employment) as employment'
#                  },
#                  {'dataset':'district14',
#                    'image_type':'dataset_table',
#                    'attribute': 'dataset_table', # Must be the same as...
#                    'arguments':{
#                                 'attribute': 'dataset_table', # ... this! (for image_type dataset_table)
#                                 'attributes' : [
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_0_workers) as 0_worker_households',
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_1_workers) as 1_worker_households',
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_2_workers) as 2_worker_households',
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_3_workers) as 3_worker_households',
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_4_workers) as 4_worker_households',
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_5_workers) as 5_worker_households',
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_6_workers) as 6_worker_households',
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_7_workers) as 7_worker_households',
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households) as total_households',
#                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_cie) as cie_sector_employment',
#                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_med) as med_sector_employment',
#                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_mips) as mips_sector_employment',
#                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_pdr) as pdr_sector_employment',
#                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_retail_ent) as retail_ent_sector_employment',
#                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_visitor) as visitor_sector_employment',
#                                     'opus_core.func.aggregate(az_smart.zone.employment) as total_employment'
#                                     ],
##                                 'conditional':'==0',
#                                 },
##                    'years':[2001]
#                   },

#                  {'dataset':'district24',
#                    'image_type':'dataset_table',
#                    'attribute': 'dataset_table', # Must be the same as...
#                    'arguments':{
#                                 'attribute': 'dataset_table', # ... this! (for image_type dataset_table)
#                                 'attributes' : [
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_0_workers) as 0_worker_households',
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_1_workers) as 1_worker_households',
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_2_workers) as 2_worker_households',
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_3_workers) as 3_worker_households',
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_4_workers) as 4_worker_households',
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_5_workers) as 5_worker_households',
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_6_workers) as 6_worker_households',
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_7_workers) as 7_worker_households',
#                                     'opus_core.func.aggregate(az_smart.zone.number_of_households) as total_households',
#                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_cie) as cie_sector_employment',
#                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_med) as med_sector_employment',
#                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_mips) as mips_sector_employment',
#                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_pdr) as pdr_sector_employment',
#                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_retail_ent) as retail_ent_sector_employment',
#                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_visitor) as visitor_sector_employment',
#                                     'opus_core.func.aggregate(az_smart.zone.employment) as total_employment'
#                                     ],
##                                 'conditional':'==0',
#                                 },
##                    'years':[2001]
#                   },

                  {'dataset':'tract2000',
                    'image_type':'dataset_table',
                    'attribute': 'dataset_table', # Must be the same as...
                    'arguments':{
                                 'attribute': 'dataset_table', # ... this! (for image_type dataset_table)
                                 'attributes' : [
                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_0_workers) as 0_worker_households',
                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_1_workers) as 1_worker_households',
                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_2_workers) as 2_worker_households',
                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_3_workers) as 3_worker_households',
                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_4_workers) as 4_worker_households',
                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_5_workers) as 5_worker_households',
                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_6_workers) as 6_worker_households',
                                     'opus_core.func.aggregate(az_smart.zone.number_of_households_with_7_workers) as 7_worker_households',
                                     'opus_core.func.aggregate(az_smart.zone.number_of_households) as total_households',
                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_cie) as cie_sector_employment',
                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_med) as med_sector_employment',
                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_mips) as mips_sector_employment',
                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_pdr) as pdr_sector_employment',
                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_retail_ent) as retail_ent_sector_employment',
                                     'opus_core.func.aggregate(az_smart.zone.employment_of_sector_visitor) as visitor_sector_employment',
                                     'opus_core.func.aggregate(az_smart.zone.employment) as total_employment'
                                     ],
#                                 'conditional':'==0',
                                 },
#                    'years':[2001]
                   },

#
#                {'dataset':'zone',
#                 'image_type':'table',
#                 'attribute':'psrc.zone.generalized_cost_hbw_am_drive_alone_to_129',
#                 },
#                {'dataset':'zone',
#                 'image_type':'table',
#                 'attribute':'psrc.zone.travel_time_hbw_am_drive_alone_to_cbd',
#                 },
#                {'dataset':'zone',
#                 'image_type':'table',
#                 'attribute':'psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone',
#                 },
#                {'dataset':'zone',
#                 'image_type':'table',
#                 'attribute':'psrc.zone.travel_time_weighted_access_to_employment_hbw_am_drive_alone',
#                 },
#
#               {'dataset':'zone',
#                 'image_type':'table',
#                 'attribute':'urbansim.zone.number_of_jobs',
#                },
#                
#              {'dataset':'alldata',
#                 'image_type':'tab',
#                 'attribute':'opus_core.func.aggregate_all(urbansim.zone.number_of_jobs) as number_of_jobs',
#                },
    ]

# finally, run the requests
generate_indicators(config, show_results = False, display_error_box = False)