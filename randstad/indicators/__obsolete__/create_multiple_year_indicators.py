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

import os 
from indicator_config import config
from urbansim.indicators.indicator_factory import IndicatorFactory

config['years'] = range(1995, 2002)  #default values, 
def get_multiple_year_indicators(config):
    
    indicators = [
             #include here multiple_year indicators, i.e. table and chart
            {'dataset':'alldata',
             'image_type':'table',
             'attribute':"num_cells_of_devtype101 = alldata.aggregate_all(urbansim.gridcell.devtype_101)"
             },
            {'dataset':'alldata',
             'image_type':'table',
             'attribute':"num_cells_of_devtype102 = alldata.aggregate_all(urbansim.gridcell.devtype_102)"
             },
            {'dataset':'alldata',
             'image_type':'table',
             'attribute':"num_cells_of_devtype103 = alldata.aggregate_all(urbansim.gridcell.devtype_103)"
             },
            {'dataset':'alldata',
             'image_type':'table',
             'attribute':"num_cells_of_devtype104 = alldata.aggregate_all(urbansim.gridcell.devtype_104)"
             },
            {'dataset':'alldata',
             'image_type':'table',
             'attribute':"num_cells_of_devtype105 = alldata.aggregate_all(urbansim.gridcell.devtype_105)"
             },

#            {'dataset':'alldata',
#             'image_type':'table',
#             'attribute':"region_households = alldata.aggregate_all(urbansim.gridcell.number_of_households)"
#             },
#            {'dataset':'alldata',
#             'image_type':'table',
#             'attribute':"region_jobs = alldata.aggregate_all(urbansim.gridcell.number_of_jobs)"
#             },
#            {'dataset':'alldata',
#             'image_type':'table',
#             'attribute':"region_comsqft = alldata.aggregate_all(urbansim.gridcell.commercial_sqft)"
#             },
#            {'dataset':'alldata',
#             'image_type':'table',
#             'attribute':"region_indsqft = alldata.aggregate_all(urbansim.gridcell.industrial_sqft)"
#             },
#            {'dataset':'ring',
#             'image_type':'table',
#             'attribute':"ring_comsqft = ring.aggregate(urbansim.gridcell.commercial_sqft, function=sum)"
#             }, 
#             {'dataset':'ring',
#             'image_type':'table',
#             'attribute':"ring_indsqft = ring.aggregate(urbansim.gridcell.industrial_sqft, function=sum)"
#             },  
#           {'dataset':'ring',
#             'image_type':'table',
#             'attribute':"ring_resunit = ring.aggregate(urbansim.gridcell.residential_units, function=sum)"
#             }, 
#            {'dataset':'alldata',
#             'image_type':'table',
#             'attribute':{'indicator_name': 'residential_vacancy_rates',
#                          'operation':'divide',
#                          'arguments':['alldata.aggregate_all(urbansim.gridcell.vacant_residential_units)', 
#                              'alldata.aggregate_all(urbansim.gridcell.residential_units)'],
#                          'scale':[0, 1]
#                          }
#             },
#            {'dataset':'alldata',
#             'image_type':'table',
#             'attribute':{'indicator_name': 'commercial_vacancy_rates',
#                          'operation':'divide',
#                          'arguments':['alldata.aggregate_all(urbansim.gridcell.vacant_commercial_sqft)', 
#                              'alldata.aggregate_all(urbansim.gridcell.commercial_sqft)'],
#                          'scale':[0, 1]
#                          }
#             },
            
#            {'dataset':'alldata',
#             'image_type':'table',
#             'attribute':{'indicator_name': 'industrial_vacancy_rates',
#                          'operation':'divide',
#                          'arguments':['alldata.aggregate_all(urbansim.gridcell.vacant_industrial_sqft)', 
#                                       'alldata.aggregate_all(urbansim.gridcell.industrial_sqft)'],
#                          'scale':[0, 1]
#                          }
#             }
#            {'dataset':'alldata',
#             'image_type':'chart',
#             'attribute':'region_residential_units = alldata.aggregate_all(urbansim.gridcell.residential_units, function=sum)'
#             },
#            {'dataset':'alldata',
#             'image_type':'chart',
#             'attribute':'region_vacant_industrial_sqft = alldata.aggregate_all(urbansim.gridcell.vacant_industrial_sqft, function=sum)'
#             },
#            {'dataset':'alldata',
#             'image_type':'chart',
#             'attribute':'region_vacant_commercial_sqft = alldata.aggregate_all(urbansim.gridcell.vacant_commercial_sqft, function=sum)'
#             },
#            {'dataset':'alldata',
#             'image_type':'chart',
#             'attribute':'region_population = alldata.aggregate_all(urbansim.household.persons, function=sum)'
#             },
#            {'dataset':'alldata',
#             'image_type':'chart',
#             'attribute':'region_average_income = alldata.aggregate_all(urbansim.household.income, function=mean)'
#             },   
            
#            {'dataset':'ring',
#             'image_type':'chart',
#             'attribute':"total_employment_in_ring = ring.aggregate(urbansim.gridcell.number_of_jobs)"
#             },   
             
#            {'dataset':'ring',
#             'image_type':'table',
#             'attribute':"total_employment_in_ring = ring.aggregate(urbansim.gridcell.number_of_jobs)"
#             },   

#             {'dataset':'gridcell',
#              'image_type':'table',
#              'attribute':'urbansim.gridcell.total_employment_within_walking_distance'
#              }
        ]
        
    return indicators

if __name__ == '__main__':
    IndicatorFactory().create_indicators(config, get_multiple_year_indicators(config))