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
import sys

from optparse import OptionParser

from opus_core.database_management.cross_database_operations import CrossDatabaseOperations

from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
from opus_core.database_management.database_server import DatabaseServer
    
parser = OptionParser()
    
parser.add_option("-o", "--host", dest="host", type="string",
    help="The mysql host (default: 'localhost').")
parser.add_option("-u", "--username", dest="username", type="string",
    help="The mysql connection password (default: MYSQLUSERNAME environment"
        " variable, then nothing).")
parser.add_option("-p", "--password", dest="password", type="string",
    help="The mysql connection password (default: MYSQLPASSWORD environment"
        " variable, then nothing).")
parser.add_option("-d", "--database", dest="database", 
    type="string", help="The database to convert. (REQUIRED)")
    
(options, args) = parser.parse_args()
    
if options.database == None: 
        parser.print_help()
        sys.exit(1)
    
config = DatabaseServerConfiguration(
    host_name = options.host,
    user_name = options.username,
    password = options.password,
    )
db_server = DatabaseServer(config)
db = db_server.get_database(options.database)
cdo = CrossDatabaseOperations()

cdo.copy_table('employment_home_based_location_choice_model_specification', 
               db, db, 
               'single_family_home_elcm_specification')

cdo.copy_table('employment_home_based_location_choice_model_specification', 
               db, db, 
               'multiple_family_home_elcm_specification')

cdo.copy_table('employment_home_based_location_choice_model_coefficients', 
               db, db, 
               'single_family_home_elcm_coefficients')

cdo.copy_table('employment_home_based_location_choice_model_coefficients', 
               db, db, 
               'multiple_family_home_elcm_coefficients')
