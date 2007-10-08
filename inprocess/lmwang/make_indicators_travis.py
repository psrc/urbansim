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


#from urbansim.indicators.indicator_configuration import IndicatorConfiguration
#from urbansim.indicators.indicator_configuration_handler_batch_mode import generate_indicators
from inprocess.travis.urbansim.indicators.indicator_configuration import IndicatorConfiguration
from inprocess.travis.urbansim.indicators.indicator_configuration_handler_batch_mode import generate_indicators


config = IndicatorConfiguration()

# *** Set up database ***
# use the defaults for mysql hostname, username, and password 
# (the defaults are to get these from environment variables)
config.database_configuration.database_name = 'PSRC_2000_baseyear'

#config.cache_directory = r'X:\urbansim_cache\run_1847.2007_01_15_15_23'
#config.run_description = '(run 1847 - no UGB 1/17/2007)'
#config.cache_directory = r'X:\urbansim_cache\run_1848.2007_01_15_15_40'
#config.run_description = '(run 1848 - no UGB+1.5xhighway 1/17/2007)'
#config.cache_directory = r'X:\urbansim_cache\run_1849.2007_01_15_16_09'
#config.run_description = '(run 1849 - baseline 1/17/2007)'
#config.cache_directory = r'V:\psrc\run_1850.2007_01_15_17_03'
#config.run_description = '(run 1850 - baseline 1/17/2007)'
#config.cache_directory = r'V:\psrc\run_1851.2007_01_15_17_07'
#config.run_description = '(run 1851 - no build 1/17/2007)'


#config.use_cache_directory_for_output = True
#
#config.datasets_to_preload = [
#    DatasetDescription(dataset_name='gridcell', package_name='urbansim', nchunks=2), 
#    DatasetDescription(dataset_name='household', package_name='urbansim'), 
#    DatasetDescription(dataset_name='job', package_name='urbansim'),
#    DatasetDescription(dataset_name='zone', package_name='urbansim'),
#    DatasetDescription(dataset_name='travel_data', package_name='urbansim')
#    ]

# single_year_requests are indicators that are computed for a particular year.
# We give a list of years in single_year_years (is there a better name??)
# The idea is that we'll get a map of psrc.large_area.population, for example,
# for 2000 and another map for 2010.
#
# Note the syntax for specifying the indicators when the indicator name includes the year
# (the substring DDDD will be replaced by the year)
config.request_years = [2025]
config.requests = [
                # absolute value
#
#               {'dataset':'gridcell',
#                'image_type':'openev_map',
#                'attribute':'urbansim.gridcell.population',
#                'arguments':{
#                             'legend_scheme':{'range':[0, 10, 50, 100], 
#                             'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
#                             
##                             'scale':[-5000, 250000]
#                             }
#                },   
#
#               {'dataset':'gridcell',
#                'image_type':'openev_map',
#                'attribute':'urbansim.gridcell.number_of_jobs as employment',
#                'arguments':{
#                              'legend_scheme':{'range':[0, 500, 5000, 25000], 
#                              'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
#
##                             'scale':[1000, 200000]
#                             }
#                }, 

                {'dataset':'faz',
                 'image_type':'map',
                 'attribute':'urbansim.faz.population',
                  'arguments':{
#                                'scale':[1, 60000]
                              }
                },
                {'dataset':'faz',
                 'image_type':'map',
                 'attribute':'psrc.faz.population_per_acre',
                 'arguments':{
#                              'scale':[1, 60000]
                              }
                },
                
               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':'psrc.faz.number_of_jobs_without_resource_construction_sectors as employment',
                 'arguments':{
#                              'scale':[1, 60000]
                              }
                },
               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':'psrc.faz.number_of_jobs_per_acre',
                 'arguments':{
#                              'scale':[1, 60000]
                              }
                },
                
#                 ##change value
#               {'dataset':'gridcell',
#                'image_type':'openev_map',
#                'attribute':'population_change(DDDD-00)',
#                'arguments':{
#                             'operation':'change',
#                             'arguments':['urbansim.gridcell.population'],
##                             'scale':[-5000, 250000]
#                             }
#                },   
#
#               {'dataset':'gridcell',
#                'image_type':'openev_map',
#                'attribute':'psrc.gridcell.absolute_number_of_jobs_change as employment_change(DDDD-00)',
#                'arguments':{
#                             'scale':[1000, 200000]
#                             }
#                }, 
#
#               {'dataset':'gridcell',
#                'image_type':'openev_map',
#                'attribute':'psrc.gridcell.percent_population_change as percent_population_change(DDDD-00)',
#                'arguments':{
##                             'scale':[1000, 200000]
#                             }
#                }, 
#
#               {'dataset':'gridcell',
#                 'image_type':'openev_map',
#                 'attribute':'psrc.gridcell.percent_number_of_jobs_change as percent_employment_change(DDDD-00)',
#                'arguments':{
##                              'scale':[-30000, 30000]
#                              }
#                },                 
                
#
               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':'population_change(DDDD-00)',
                 'arguments':{                 
                              'operation':'change',
                              'arguments':['urbansim.faz.population'],
#                              'scale':[-2000, 40000]
                              }
                },

               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':'employment_change(DDDD-00)',
                 'arguments':{                 
                              'operation':'change',
                              'arguments':['urbansim.faz.number_of_jobs'],
#                              'scale':[-2000, 40000]
                              }
                },

               {'dataset':'faz',
                'image_type':'map',
                'attribute':'psrc.faz.percent_population_change as percent_population_change(DDDD-00)',
                 'arguments':{                
#                             'scale':[1000, 200000]
                             }
                }, 

               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':'psrc.faz.percent_number_of_jobs_change as percent_employment_change(DDDD-00)',
                 'arguments':{                 
#                              'scale':[-30000, 30000]
                              }
                },                 

                
                 ###difference (this scenario - baseline)

#               {'dataset':'gridcell',
#                 'image_type':'openev_map',
#                 'attribute':'psrc.gridcell.absolute_population_difference_from_baseline as population_difference_from_baseline',
#                 'arguments':{
#                              'scale':[-30000, 30000]
#                              }
#                },
#                
#               {'dataset':'gridcell',
#                 'image_type':'openev_map',
#                 'attribute':'psrc.gridcell.absolute_number_of_jobs_difference_from_baseline as employment_difference_from_baseline',
#                 'arguments':{
##                              'scale':[-30000, 30000]
#                              }
#                }, 
#               {'dataset':'gridcell',
#                 'image_type':'openev_map',
#                 'attribute':'psrc.gridcell.percent_population_difference_from_baseline as percent_population_difference_from_baseline',
#                 'arguments':{
#                              'scale':[-30000, 30000]
#                              }
#                },
#                
#               {'dataset':'gridcell',
#                 'image_type':'openev_map',
#                 'attribute':'psrc.gridcell.percent_number_of_jobs_difference_from_baseline as percent_employment_difference_from_baseline',
#                 'arguments':{
##                              'scale':[-30000, 30000]
#                              }
#                }, 

               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':'psrc.faz.absolute_population_difference_from_baseline',
                 'arguments':{                 
#                              'scale':[-30000, 30000]
                              }
                }, 
               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':'psrc.faz.percent_population_difference_from_baseline',
                 'arguments':{                 
#                              'scale':[-30000, 30000]
                              }
                }, 
                
               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':'psrc.faz.absolute_number_of_jobs_difference_from_baseline as absolute_employment_difference_from_baseline',
                 'arguments':{                 
#                              'scale':[-30000, 30000]
                              }
                }, 
               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':'psrc.faz.percent_number_of_jobs_difference_from_baseline as percent_employment_difference_from_baseline',
                 'arguments':{                 
#                              'scale':[-30000, 30000]
                              }
                }, 
                
                
                {'dataset':'zone',
                 'image_type':'map',
                 'attribute':'psrc.zone.travel_time_hbw_am_drive_alone_to_cbd',
                 'arguments':{                 
                              'scale':[-10, 110]
                              },
                 'years':[2000,2006,2011,2016,2021]
                 },

                {'dataset':'zone',
                 'image_type':'map',
                 'attribute':'psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone',
                 'arguments':{                 
#                              'scale':[-1000, 7000]                              
                              },
                 'years':[2000,2006,2011,2016,2021]
                 },

                 {'dataset':'large_area',
                  'image_type':'table',
                  'attribute':'psrc.large_area.population',
                 'arguments':{},
                 'years':[2000,2010,2020,2025]                                
                  },  
                 {'dataset':'large_area',
                  'image_type':'table',
                  'attribute':'psrc.large_area.number_of_jobs_without_resource_construction_sectors',
                 'arguments':{},
                 'years':[2000,2010,2020,2025]           
                  },                               
                               ]

# finally, run the requests
#generate_indicators(config)