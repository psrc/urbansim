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

# General information about the indicators to create.
general_info = {
    'run_id':60,
    'run_description':'(travel model skims)',
    
    'services_configuration':{
        'type':'mysql_storage',
        'host_name':os.environ['MYSQLHOSTNAME'],
        'user_name':os.environ['MYSQLUSERNAME'],
        'password':os.environ['MYSQLPASSWORD'],
        'database_name':'services',
        },
    'required_datasets':['job', 'household', 'gridcell', 'zone', 'travel_data', 
                         'faz', 'large_area', 'county', 'development_event',
                         'city'],
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
