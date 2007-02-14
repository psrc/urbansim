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


# General information about the indicators to create.
config = {
    'cache_directory': 'C:/urbansim_cache/workshop/06_07_09_14_58_14',
    'run_description': '(baseline run without travel model)',
    'resources': {
        'input_configuration': DatabaseConfiguration(
            host_name     = os.environ['MYSQLHOSTNAME'],#'trondheim.cs.washington.edu', #artemis.ce.washington.edu
            user_name     = os.environ['MYSQLUSERNAME'],
            password      = os.environ['MYSQLPASSWORD'],
            database_name = "washtenaw_class",
            ),
        },
    'datasets_to_preload': {
        'gridcell': {
            'package_name': 'urbansim',
            },
        'household': {
            'package_name': 'urbansim',
            },
        'job': {
            'package_name': 'urbansim',
            },
        'zone': {
            'package_name': 'urbansim',
            },
        'travel_data': {
            'package_name': 'urbansim',
            },
        },
    }
