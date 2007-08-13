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

config['year'] = 1995
def get_single_year_indicators(config):
    indicators = [
            #{'dataset':'zone',
            # 'image_type':'map',
            # 'attribute':'urbansim.zone.population'
            # },
            #{'dataset':'zone',
            # 'image_type':'map',
            # 'attribute':'urbansim.zone.number_of_jobs'
            # },
#            {'dataset':'zone',
#             'image_type':'map',
#             'attribute':'urbansim.zone.residential_units'
#             },
#            {'dataset':'zone',
#             'image_type':'map',
#             'attribute':'urbansim.zone.average_land_value'
#             },
             
#            {'dataset':'zone',
#             'image_type':'map',
#             'attribute':{'indicator_name':'urbansim.zone.population', 'scale':[1, 20000]}
#             },
#            {'dataset':'zone',
#             'image_type':'map',
#             'attribute':{'indicator_name':'psrc.zone.number_of_jobs_without_resource_construction_sectors',
#                          'scale':[1, 35000]
#                          }
#             }, 
#            {'dataset':'zone',
#             'image_type':'map',
#             'attribute':{'indicator_name': 'urbansim_population_change',
#                          'operation':'change',
#                          'arguments':['urbansim.zone.population']
#                          }
#             },
#            {'dataset':'zone',
#             'image_type':'map',
#             'attribute':{'indicator_name': 'urbansim_employment_change',
#                          'operation':'change',
#                          'arguments':['psrc.zone.number_of_jobs_without_resource_construction_sectors']
#                          }
#             },
             
            #{'dataset':'gridcell',
            # 'image_type':'map',
            # 'attribute':'urbansim.gridcell.population'
            # },    
            {'dataset':'gridcell',
             'image_type':'map',
             'attribute':'urbansim.gridcell.number_of_commercial_jobs'
             }, 
            {'dataset':'gridcell',
             'image_type':'map',
             'attribute':'urbansim.gridcell.number_of_industrial_jobs'
             }, 
            {'dataset':'gridcell',
             'image_type':'map',
             'attribute':'urbansim.gridcell.commercial_sqft'
             }, 
            {'dataset':'gridcell',
             'image_type':'map',
             'attribute':'urbansim.gridcell.industrial_sqft'
             }, 
             {'dataset':'gridcell',
             'image_type':'map',
             'attribute':'urbansim.gridcell.number_of_jobs'
             }, 
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':{'indicator_name': 'urbansim_population_change',
#                          'operation':'change',
#                          'arguments':['urbansim.gridcell.population']
#                          }
#             },      
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':{'indicator_name': 'urbansim_employment_change',
#                          'operation':'change',
#                          'arguments':['psrc.gridcell.number_of_jobs_without_resource_construction_sectors']
#                          }
#             }, 
             
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':'urbansim.gridcell.average_income'
#             }, 
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':'urbansim.gridcell.total_land_value'
#             }, 
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':'urbansim.gridcell.total_improvement_value'
#             }, 
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':'urbansim.gridcell.average_residential_value_per_housing_unit'
#             }, 
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':'urbansim.gridcell.total_nonresidential_value'
#             },       
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':'urbansim.gridcell.residential_units'
#             }, 
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':'urbansim.gridcell.industrial_sqft'
#             }, 
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':'urbansim.gridcell.commercial_sqft'
#             }, 
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':'urbansim.gridcell.non_residential_sqft'
#             }, 
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':'urbansim.gridcell.number_of_households'
#             }, 
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':'urbansim.gridcell.number_of_industrial_jobs'
#             }, 
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':'urbansim.gridcell.number_of_commercial_jobs'
#             }, 
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':'urbansim.gridcell.number_of_non_home_based_jobs'
#             }, 
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':'urbansim.gridcell.number_of_home_based_jobs'
#             }, 
#             
#            {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':'psrc.gridcell.travel_time_hbw_am_drive_alone_to_cbd'
#             },   
        ]

    return indicators
        
if __name__ == '__main__':
    IndicatorFactory().create_indicators(config, get_single_year_indicators(config))