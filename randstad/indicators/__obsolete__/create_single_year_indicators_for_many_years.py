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

years = range(1996,2002)
def get_single_year_indicators(config):
    indicators = [
#            {'dataset':'zone',
#             'image_type':'map',
#             'attribute':{'indicator_name':'urbansim.zone.travel_time_to_cbd',
#                          'scale':[0, 10000]
#                          }
#             },
               
            {'dataset':'gridcell',
             'image_type':'map',
             'attribute':{'indicator_name':'urbansim.gridcell.is_in_development_type_group_residential',}   
             }, 
#        {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':{'indicator_name':'urbansim.gridcell.commercial_sqft',}   
#             }, 
#        {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':{'indicator_name':'urbansim.gridcell.industrial_sqft',}   
#             }, 
#        {'dataset':'ring',
#             'image_type':'map',
#             'attribute':"ring_comsqft = ring.aggregate(urbansim.gridcell.commercial_sqft, function=sum)"
#             }, 
#        {'dataset':'gridcell',
#             'image_type':'map',
#             'attribute':{'indicator_name': 'land use change',
#                          'operation':'subtract',
#                          'arguments':['urbansim.gridcell.is_in_development_type_group_developed', 
#                              'urbansim.gridcell.is_in_development_type_group_developed_lag1'],
#                          'scale':[-1, 1]
#                          }
#             }, 
        ]

    return indicators
        
if __name__ == '__main__':
    for year in years:
        config['year'] = year
        IndicatorFactory().create_indicators(config, get_single_year_indicators(config))