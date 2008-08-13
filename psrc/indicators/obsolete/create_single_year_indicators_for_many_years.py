#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

years = [2000, 2001, 2005, 2006, 2030]
def get_single_year_indicators(config):
    
    indicators = [
             # absolute values
            {'dataset':'zone',
             'image_type':'map',
             'attribute':{'indicator_name':'psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone',
                 'scale':[0, 10000]}
             },
            {'dataset':'zone',
             'image_type':'map',
             'attribute':{'indicator_name':'psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd',
                 'scale':[0, 150]}
             }
        ]

    return indicators

if __name__ == '__main__': 
    import os
    from indicator_config import config
    from urbansim.indicators.indicator_factory import IndicatorFactory
                
    for year in years:
        config['year'] = year
        IndicatorFactory().create_indicators(config, get_single_year_indicators(config))