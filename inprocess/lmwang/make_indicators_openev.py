# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

# script to produce a number of PSRC indicators -- 
# this illustrates using traits-based configurations programatically


from urbansim.indicators.indicator_configuration import IndicatorConfiguration
from urbansim.indicators.indicator_configuration_handler_batch_mode import generate_indicators
from opus_core.configurations.dataset_description import DatasetDescription

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
config.single_year_years = [2025]
config.single_year_requests = [
                # absolute value
#
               {'dataset':'gridcell',
                'image_type':'openev_map',
                'attribute':{'indicator_name': 'urbansim.gridcell.population',
                             'legend_scheme':{'range':[0, 10, 50, 100], 
                             'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
                             
#                             'scale':[-5000, 250000]
                             }
                },   

               {'dataset':'gridcell',
                'image_type':'openev_map',
                'attribute':{'indicator_name': 'urbansim.gridcell.number_of_jobs as employment',
                              'legend_scheme':{'range':[0, 500, 5000, 25000], 
                              'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}

#                             'scale':[1000, 200000]
                             }
                }, 
#                {'dataset':'faz',
#                 'image_type':'map',
#                 'attribute':{'indicator_name':'urbansim.faz.population',
#                              'scale':[1, 60000]
#                              }
#                },
#                
#               {'dataset':'faz',
#                 'image_type':'map',
#                 'attribute':{'indicator_name':'urbansim.faz.number_of_jobs as employment',
#                              'scale':[1, 60000]
#                              }
#                },
                
#                 ##change value
               {'dataset':'gridcell',
                'image_type':'openev_map',
                'attribute':{'indicator_name': 'population_change(DDDD-00)',
                             'operation':'change',
                             'arguments':['urbansim.gridcell.population'],
#                             'scale':[-5000, 250000]
                             }
                },   

               {'dataset':'gridcell',
                'image_type':'openev_map',
                'attribute':{'indicator_name': 'psrc.gridcell.absolute_number_of_jobs_change as employment_change(DDDD-00)',
                             'scale':[1000, 200000]
                             }
                }, 

               {'dataset':'gridcell',
                'image_type':'openev_map',
                'attribute':{'indicator_name': 'psrc.gridcell.percent_population_change as percent_population_change(DDDD-00)',
#                             'scale':[1000, 200000]
                             }
                }, 

               {'dataset':'gridcell',
                 'image_type':'openev_map',
                 'attribute':{'indicator_name': 'psrc.gridcell.percent_number_of_jobs_change as percent_employment_change(DDDD-00)',
#                              'scale':[-30000, 30000]
                              }
                },                 
                
#
#               {'dataset':'faz',
#                 'image_type':'map',
#                 'attribute':{'indicator_name': 'population_change(DDDD-00)',
#                              'operation':'change',
#                              'arguments':['urbansim.faz.population'],
#                              'scale':[-2000, 40000]
#                              }
#                },
#
#               {'dataset':'faz',
#                 'image_type':'map',
#                 'attribute':{'indicator_name': 'employment_change(DDDD-00)',
#                              'operation':'change',
#                              'arguments':['urbansim.faz.number_of_jobs'],
#                              'scale':[-2000, 40000]
#                              }
#                },
#
#               {'dataset':'faz',
#                'image_type':'map',
#                'attribute':{'indicator_name': 'psrc.faz.percent_population_change as percent_population_change(DDDD-00)',
##                             'scale':[1000, 200000]
#                             }
#                }, 
#
#               {'dataset':'faz',
#                 'image_type':'map',
#                 'attribute':{'indicator_name': 'psrc.faz.percent_number_of_jobs_change as percent_employment_change(DDDD-00)',
##                              'scale':[-30000, 30000]
#                              }
#                },                 

                
                 ###difference (this scenario - baseline)

               {'dataset':'gridcell',
                 'image_type':'openev_map',
                 'attribute':{'indicator_name': 'psrc.gridcell.absolute_population_difference_from_baseline as population_difference_from_baseline',
                              'scale':[-30000, 30000]
                              }
                },
                
               {'dataset':'gridcell',
                 'image_type':'openev_map',
                 'attribute':{'indicator_name': 'psrc.gridcell.absolute_number_of_jobs_difference_from_baseline as employment_difference_from_baseline',
#                              'scale':[-30000, 30000]
                              }
                }, 
               {'dataset':'gridcell',
                 'image_type':'openev_map',
                 'attribute':{'indicator_name': 'psrc.gridcell.percent_population_difference_from_baseline as percent_population_difference_from_baseline',
                              'scale':[-30000, 30000]
                              }
                },
                
               {'dataset':'gridcell',
                 'image_type':'openev_map',
                 'attribute':{'indicator_name': 'psrc.gridcell.percent_number_of_jobs_difference_from_baseline as percent_employment_difference_from_baseline',
#                              'scale':[-30000, 30000]
                              }
                }, 

#               {'dataset':'faz',
#                 'image_type':'map',
#                 'attribute':{'indicator_name': 'psrc.faz.absolute_population_difference_from_baseline',
##                              'scale':[-30000, 30000]
#                              }
#                }, 
#               {'dataset':'faz',
#                 'image_type':'map',
#                 'attribute':{'indicator_name': 'psrc.faz.percent_population_difference_from_baseline',
##                              'scale':[-30000, 30000]
#                              }
#                }, 
#                
#               {'dataset':'faz',
#                 'image_type':'map',
#                 'attribute':{'indicator_name': 'psrc.faz.absolute_number_of_jobs_difference_from_baseline as employment_difference_from_baseline',
##                              'scale':[-30000, 30000]
#                              }
#                }, 
#               {'dataset':'faz',
#                 'image_type':'map',
#                 'attribute':{'indicator_name': 'psrc.faz.percent_number_of_jobs_difference_from_baseline as percent_employment_difference_from_baseline',
##                              'scale':[-30000, 30000]
#                              }
#                }, 
    ]

# multi-year requests are for indicators that can be computed for multiple years.  Here, for example,
# we'll have a single chart of psrc.county.population that includes all the years betweeen 2000 and 2009
config.multi_year_years = []
config.multi_year_requests = []

# finally, run the requests
#generate_indicators(config)