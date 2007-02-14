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

# script to produce a number of Washtenaw indicators -- 
# this illustrates using traits-based configurations programatically


from urbansim.indicators.indicator_configuration import IndicatorConfiguration
from opus_core.configurations.dataset_description import DatasetDescription
from urbansim.indicators.indicator_configuration_handler_batch_mode import generate_indicators

config = IndicatorConfiguration()

# *** Set up database ***
# use the defaults for mysql hostname, username, and password 
# (the defaults are to get these from environment variables)
config.database_configuration.database_name = 'washtenaw_estimation'
#    config.cache_directory = r'C:\urbansim_cache\workshop\2006_08_28_16_58'
config.cache_directory = '/Users/borning/urbansim_cache/workshop/2006_08_28_16_58'
config.run_description = '(baseline run without travel model)'
config.use_cache_directory_for_output = True
#
#config.datasets_to_preload = [
#    DatasetDescription(dataset_name='gridcell', package_name='urbansim'),
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
# (the substring %(year)s will be replaced by the year)
config.single_year_years = [2000]
config.single_year_requests = [
            {'dataset':'gridcell',
             'image_type':'map',
             'attribute':{'indicator_name':'urbansim.gridcell.population', 
             'scale':[0, 800]}
             }
    ]

# multi-year requests are for indicators that can be computed for multiple years.  Here, for example,
# we'll have a single chart of psrc.county.population that includes all the years betweeen 2000 and 2009
config.multi_year_years = [2000]
config.multi_year_requests = [
             {'dataset':'alldata',
              'image_type':'table',
              'attribute':'opus_core.func.aggregate_all(urbansim.gridcell.residential_units,sum) as Residential_Units'
              }, 
             {'dataset':'alldata',
              'image_type':'table',
              'attribute':'opus_core.func.aggregate_all(urbansim.gridcell.commercial_sqft,sum) as Commercial_SQFT'
              }, 
             {'dataset':'alldata',
              'image_type':'table',
              'attribute':'opus_core.func.aggregate_all(urbansim.gridcell.industrial_sqft,sum) as Industrial_SQFT'
              }, 
             {'dataset':'alldata',
              'image_type':'table',
              'attribute':'opus_core.func.aggregate_all(urbansim.gridcell.is_developed,sum) as Developed_Cells'
              }, 
             {'dataset':'alldata',
              'image_type':'table',
              'attribute':{'indicator_name':'residential_vacancy_rate',
                           'operation':'divide',
                           'arguments':['opus_core.func.aggregate_all(urbansim.gridcell.vacant_residential_units,sum)',
                                        'opus_core.func.aggregate_all(urbansim.gridcell.residential_units,sum)']
                           }
              },             
             {'dataset':'alldata',
              'image_type':'table',
              'attribute':{'indicator_name':'commercial_vacancy_rate',
                           'operation':'divide',
                           'arguments':['opus_core.func.aggregate_all(urbansim.gridcell.vacant_commercial_sqft,sum)',
                                        'opus_core.func.aggregate_all(urbansim.gridcell.commercial_sqft,sum)']
                           }
              },             
             {'dataset':'alldata',
              'image_type':'table',
              'attribute':{'indicator_name':'industrial_vacancy_rate',
                           'operation':'divide',
                           'arguments':['opus_core.func.aggregate_all(urbansim.gridcell.vacant_industrial_sqft,sum)',
                                        'opus_core.func.aggregate_all(urbansim.gridcell.industrial_sqft,sum)']
                           }
              }        
    ]

# finally, run the requests
generate_indicators(config)