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
from urbansim.indicators.indicator_factory import IndicatorFactory


# The indicators to chart or map
from general_info import general_info
general_info['years'] = [2005]#2000,2005,2010,2015,2020,2025,2030]
general_info['run_id'] = 331

indicators = [
        #absolute value
        {'dataset':'alldata',
         'image_type':'table',
         
         'attribute':{'indicator_name':'vehicle_miles_traveled_per_capita = alldata.aggregate_all(psrc.zone.vehicle_miles_traveled_per_capita, function=mean)',
                      }
         },
        #absolute value
        {'dataset':'alldata',
         'image_type':'table',
         
         'attribute':{'indicator_name':'vehicle_miles_traveled = alldata.aggregate_all(psrc.zone.vehicle_miles_traveled, function=sum)',
                      }
         },
        #absolute value
        {'dataset':'alldata',
         'image_type':'table',
         
         'attribute':{'indicator_name':'greenhouse_gas_emissions_from_vehicle_travel = alldata.aggregate_all(psrc.zone.greenhouse_gas_emissions_from_vehicle_travel, function=sum)',
                      }
         }
#            {'dataset':'alldata',
#             'image_type':'table',
#             
#             'attribute':{'indicator_name':'mode_split_human_powered_over_all = alldata.aggregate_all(psrc.zone.mode_split_human_powered_over_all, function=mean)',
#                          }
#             }
    ]

IndicatorFactory().create_indicators(general_info, indicators)