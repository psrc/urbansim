# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

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
config.requests = []
#for m in range(10, 130, 10):
#    i = [{'dataset':'zone',
#         'image_type':'map',
#         'attribute':'LNE%sMTW = ln_bounded(psrc.zone.employment_within_%s_minutes_travel_time_hbw_am_transit_walk)' % (m, m),
#         'arguments':{                 
#    #                              'scale':[-1000, 7000]                              
#             },     
#         'years':[2000,2006,2011,2016,2021]
#         },
#         {'dataset':'zone',
#         'image_type':'map',
#         'attribute':'LNE%sMDA = ln_bounded(psrc.zone.employment_within_%s_minutes_travel_time_hbw_am_drive_alone)' % (m, m),
#         'arguments':{                 
#    #                              'scale':[-1000, 7000]                              
#             },     
#         'years':[2000,2006,2011,2016,2021]
#         },         
#         ]
#    config.requests += i

config.requests += [
        {'dataset':'gridcell',
         'image_type':'map',
         'attribute':'urbansim.gridcell.developable_maximum_residential_units as remaining_residential_capacity_max',
         'arguments':{                 
    #                              'scale':[-1000, 7000]                              
             },     
         'years':[2000, 2025]
        },
        {'dataset':'gridcell',
         'image_type':'map',
         'attribute':'urbansim.gridcell.developable_minimum_residential_units as remaining_residential_capacity_min',
         'arguments':{                 
    #                              'scale':[-1000, 7000]                              
             },     
         'years':[2000, 2025]
        },
        {'dataset':'gridcell',
         'image_type':'map',
         'attribute':'urbansim.gridcell.developable_maximum_commercial_sqft as remaining_commercial_capacity_max',
         'arguments':{                 
    #                              'scale':[-1000, 7000]                              
             },     
         'years':[2000, 2025]
        },
        {'dataset':'gridcell',
         'image_type':'map',
         'attribute':'urbansim.gridcell.developable_minimum_commercial_sqft as remaining_commercial_capacity_min',
         'arguments':{                 
    #                              'scale':[-1000, 7000]                              
             },     
         'years':[2000, 2025]
        },        
        {'dataset':'gridcell',
         'image_type':'map',
         'attribute':'urbansim.gridcell.developable_maximum_industrial_sqft as remaining_industrial_capacity_max',
         'arguments':{                 
    #                              'scale':[-1000, 7000]                              
             },     
         'years':[2000, 2025]
        },
        {'dataset':'gridcell',
         'image_type':'map',
         'attribute':'urbansim.gridcell.developable_minimum_industrial_sqft as remaining_industrial_capacity_min',
         'arguments':{                 
    #                              'scale':[-1000, 7000]                              
             },     
         'years':[2000, 2025]
        },        


        {'dataset':'gridcell',
         'image_type':'geotiff',
         'attribute':'urbansim.gridcell.developable_maximum_residential_units as remaining_residential_capacity_max',
         'arguments':{                 
    #                              'scale':[-1000, 7000]                              
             },     
         'years':[2000, 2025]
        },
        {'dataset':'gridcell',
         'image_type':'geotiff',
         'attribute':'urbansim.gridcell.developable_minimum_residential_units as remaining_residential_capacity_min',
         'arguments':{                 
    #                              'scale':[-1000, 7000]                              
             },     
         'years':[2000, 2025]
        },
        {'dataset':'gridcell',
         'image_type':'geotiff',
         'attribute':'urbansim.gridcell.developable_maximum_commercial_sqft as remaining_commercial_capacity_max',
         'arguments':{                 
    #                              'scale':[-1000, 7000]                              
             },     
         'years':[2000, 2025]
        },
        {'dataset':'gridcell',
         'image_type':'geotiff',
         'attribute':'urbansim.gridcell.developable_minimum_commercial_sqft as remaining_commercial_capacity_min',
         'arguments':{                 
    #                              'scale':[-1000, 7000]                              
             },     
         'years':[2000, 2025]
        },        
        {'dataset':'gridcell',
         'image_type':'geotiff',
         'attribute':'urbansim.gridcell.developable_maximum_industrial_sqft as remaining_industrial_capacity_max',
         'arguments':{                 
    #                              'scale':[-1000, 7000]                              
             },     
         'years':[2000, 2025]
        },
        {'dataset':'gridcell',
         'image_type':'geotiff',
         'attribute':'urbansim.gridcell.developable_minimum_industrial_sqft as remaining_industrial_capacity_min',
         'arguments':{                 
    #                              'scale':[-1000, 7000]                              
             },     
         'years':[2000, 2025]
        },        


    
]
#
##                
##                {'dataset':'zone',
##                 'image_type':'map',
##                 'attribute':'psrc.zone.travel_time_hbw_am_drive_alone_to_cbd',
##                 'arguments':{                 
##                              'scale':[-10, 110]
##                              },
##                 'years':[2000,2006,2011,2016,2021]
##                 },
##
##                {'dataset':'zone',
##                 'image_type':'map',
##                 'attribute':'psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone',
##                 'arguments':{                 
###                              'scale':[-1000, 7000]                              
##                              },
##                 'years':[2000,2006,2011,2016,2021]
##                 },
##
##
#                {'dataset':'zone',
#                 'image_type':'map',
#                 'attribute':'LNE40MTW = ln_bounded(psrc.zone.employment_within_40_minutes_travel_time_hbw_am_transit_walk)',
#                 'arguments':{                 
##                              'scale':[-1000, 7000]                              
#                              },
#                 'years':[2000,2006,2011,2016,2021]
#                 },
#
#                               ]

# finally, run the requests
#generate_indicators(config)