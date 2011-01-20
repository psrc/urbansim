# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
import sys

from optparse import OptionParser

from opus_core.database_management.cross_database_operations import CrossDatabaseOperations

from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core.database_management.database_server import DatabaseServer
    
parser = OptionParser()
    
parser.add_option("-o", "--host", dest="host", type="string",
    help="The mysql host (default: 'localhost').")
parser.add_option("-u", "--username", dest="username", type="string",
    help="The mysql connection password (default: nothing).")
parser.add_option("-p", "--password", dest="password", type="string",
    help="The mysql connection password (default: nothing).")
parser.add_option("-d", "--database", dest="database", 
    type="string", help="The database to convert. (REQUIRED)")
    
(options, args) = parser.parse_args()

if options.host == None: options.host = 'localhost'
if options.username == None: 
    options.username = ''
if options.password == None: 
    options.password = 
    
if options.database == None: 
        parser.print_help()
        sys.exit(1)
    
config = DatabaseServerConfiguration(
    host_name = options.host,
    protocol = 'mysql',
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
