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

# open a traits-based GUI for editing Washtenaw indicator requests


from urbansim.indicators.indicator_configuration import IndicatorConfiguration
from urbansim.indicators.ui.indicator_configuration_handler import IndicatorConfigurationHandler
from opus_core.configurations.dataset_description import DatasetDescription

all_datasets = [DatasetDescription(dataset_name='gridcell', package_name='urbansim'), 
                DatasetDescription(dataset_name='household', package_name='urbansim'), 
                DatasetDescription(dataset_name='job', package_name='urbansim'),
                DatasetDescription(dataset_name='zone', package_name='urbansim'),
                DatasetDescription(dataset_name='travel_data', package_name='urbansim')
                ]

all_years = [2000]

all_single_year_requests = [
             {'dataset':'gridcell',
             'image_type':'map',
             'attribute':{'indicator_name':'urbansim.gridcell.population', 
             'scale':[0, 800]}
             },  
    ]

all_multi_year_requests = [
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
              },             
             #{'dataset':'alldata',
              #'image_type':'table',
              #'attribute':'psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk'
              #}, 
             #{'dataset':'alldata',
              #'image_type':'table',
              #'attribute':'psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk'
              #}, 
             #{'dataset':'zone',
              #'image_type':'table',
              #'attribute':'psrc.county.number_of_jobs'
              #},  
    ]

config = IndicatorConfiguration()
config.database_configuration.database_name = 'washtenaw_estimation'
config.cache_directory = r'C:\urbansim_cache\workshop\2006_08_28_16_58'
config.run_description = '(baseline run without travel model)'
config.use_cache_directory_for_output = True
config.datasets_to_preload = all_datasets

handler = IndicatorConfigurationHandler(all_datasets=all_datasets, 
                                        all_years=all_years, 
                                        all_single_year_requests=all_single_year_requests, 
                                        all_multi_year_requests=all_multi_year_requests)
handler.open_editor(config)