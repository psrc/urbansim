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

from opus_core.configurations.database_configuration import DatabaseConfiguration

from urbansim.indicators.indicator_factory import IndicatorFactory

from psrc.indicators.obsolete.create_single_year_indicators import get_single_year_indicators
from psrc.indicators.obsolete.create_single_year_indicators_for_many_years import get_single_year_indicators as get_single_year_indicators_for_many_years
from psrc.indicators.obsolete.create_multiple_year_indicators import get_multiple_year_indicators


config = {
    'resources':{
        'input_configuration': DatabaseConfiguration(
            host_name     = os.environ['MYSQLHOSTNAME'],
            user_name     = os.environ['MYSQLUSERNAME'],
            password      = os.environ['MYSQLPASSWORD'],
            database_name = 'PSRC_2000_baseyear',
            ),
        }, 
    'datasets_to_preload':{
        'gridcell':{
            'package_name':'urbansim', 
            }, 
        'household':{
            'package_name':'urbansim', 
            }, 
        'job':{
            'package_name':'urbansim', 
            }, 
        'zone':{
            'package_name':'urbansim', 
            }, 
        'travel_data':{
            'package_name':'urbansim', 
            }, 
        }, 
    }

runs = [
    {'id':615, 
     'cache_directory': r'D:\urbansim_cache\run_615.2006_07_14_09_05', 
     'run_description': '(run 615 - baseline 7/18)', 
    }, 
    {'id':580, 
     'cache_directory': r'K:\run_580.2006_06_26_10_54', 
     'run_description': '(run 580 - no ugb with double-capacity highway 7/18)', 
    }, 
    {'id':581,
     'cache_directory': r'D:\urbansim_cache\run_581.2006_06_26_10_55',
     'run_description': '(run 581 - no ugb with full travel model 7/18)',
    },
    {'id':582, 
     'cache_directory': r'D:\urbansim_cache\run_582.2006_06_26_10_57', 
     'run_description': '(run 582 - baseline with double-capacity highway 7/18)', 
    }, 
#    {'id':333, 
#     'cache_directory': 'N:/urbansim_cache/run_333.2006_04_21_22_28', 
#     'run_description': '(run 333 - constrained King 5/3)', 
#    }, 

]

multiple_year = [2000, 2010, 2020, 2030]
single_year = None #2030
many_single_year = None #[2000, 2001, 2005, 2006, 2030]

for run in runs:
    config['cache_directory'] = run['cache_directory']
    config['run_description'] = run['run_description']
    if single_year is not None:
        config['year'] = single_year
        IndicatorFactory().create_indicators(config, get_single_year_indicators(config))

    if many_single_year is not None:
        for year in many_single_year:
            config['year'] = year
            IndicatorFactory().create_indicators(config, get_single_year_indicators_for_many_years(config))

    if multiple_year is not None:
        config['years'] = multiple_year
        IndicatorFactory().create_indicators(config, get_multiple_year_indicators(config))