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

config['years'] = [2000, 2010, 2020, 2030]  #range(2000,2031), 
indicators = [
#          {'dataset':'county',
#           'image_type':'chart',
#           'attribute':'psrc.county.population'
#           },
#          {'dataset':'county',
#           'image_type':'chart',
#           'attribute':'psrc.county.number_of_jobs'
#           }, 

      {'dataset':'large_area',
       'image_type':'table',
       'attribute':'psrc.large_area.population'
       },
      {'dataset':'large_area',
       'image_type':'table',
       'attribute':'psrc.large_area.number_of_jobs_without_resource_construction_sectors'
       },
#          {'dataset':'large_area',
#           'image_type':'table',
#           'attribute':'psrc.large_area.average_land_value_for_plan_type_group_residential',
#           },
#          {'dataset':'large_area',
#           'image_type':'table',
#           'attribute':'psrc.large_area.average_land_value_for_plan_type_group_non_residential',
#           },
       
#           {'dataset':'large_area',
#            'image_type':'chart',
#            'attribute':'psrc.large_area.population'
#            },
#           {'dataset':'large_area',
#            'image_type':'chart',
#            'attribute':'psrc.large_area.number_of_jobs'
#            }, 

#           {'dataset':'faz',
#            'image_type':'table',
#            'attribute':'psrc.county.population',
#            },
#           {'dataset':'faz',
#            'image_type':'table',
#            'attribute':'psrc.county.number_of_jobs',
#            }, 
        
    ]
    
IndicatorFactory().create_indicators(config, indicators)