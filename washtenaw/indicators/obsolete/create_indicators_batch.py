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

import os

from opus_core.configurations.database_configuration import DatabaseConfiguration

from urbansim.indicators.indicator_factory import IndicatorFactory

from washtenaw.indicators.obsolete.create_single_year_indicators import get_single_year_indicators
from washtenaw.indicators.obsolete.create_single_year_indicators_for_many_years import get_single_year_indicators as get_single_year_indicators_for_many_years
from washtenaw.indicators.obsolete.create_multiple_year_indicators import get_multiple_year_indicators


config = {
    'resources':{
        'input_configuration': DatabaseConfiguration(
            host_name     = os.environ['MYSQLHOSTNAME'],
            user_name     = os.environ['MYSQLUSERNAME'],
            password      = os.environ['MYSQLPASSWORD'],
            database_name = "washtenaw_class",
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
#    {'id':329, 
#     'cache_directory': 'L:/urbansim_cache/run_329.2006_04_21_22_17', 
#     'run_description': '(run 329 - baseline 5/3)', 
#    }, 
#    {'id':330, 
#     'cache_directory': 'L:/urbansim_cache/run_330.2006_04_21_22_18', 
#     'run_description': '(run 330 - highway 5/3)', 
#    }, 
    {#'id':331,
     'cache_directory':'C:/urbansim_cache/workshop/06_07_09_14_58_14',
     'run_description':'(baseline run without travel model)',
    },
#    {'id':332, 
#     'cache_directory': 'M:/urbansim_cache/run_332.2006_04_21_22_25', 
#     'run_description': '(run 332 - no ugb + highway 5/3)', 
#    }, 
#    {'id':333, 
#     'cache_directory': 'N:/urbansim_cache/run_333.2006_04_21_22_28', 
#     'run_description': '(run 333 - constrained King 5/3)', 
#    }, 

]

multiple_year = None#[2000, 2010, 2020, 2030]
single_year = 2000
many_single_year = None#[2000, 2001, 2005, 2006, 2030]

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