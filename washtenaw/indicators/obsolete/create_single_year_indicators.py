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

def get_single_year_indicators(config):    
    indicators = [
            {'dataset':'gridcell',
             'image_type':'map',
             'attribute':{'indicator_name':'urbansim.gridcell.population',
                  }
             },  
        ]

    return indicators

if __name__ == '__main__': 
    import os
    from indicator_config import config
    from urbansim.indicators.indicator_factory import IndicatorFactory
    
    config['year'] = 2000        
    IndicatorFactory().create_indicators(config, get_single_year_indicators(config))