# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
import sys

from optparse import OptionParser
from warnings import filterwarnings

from .classes.create_buildings_table import CreateBuildingsTable

from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration

    
parser = OptionParser()
    
parser.add_option("-o", "--host", dest="host", type="string",
    help="The database host (default: 'localhost').")
parser.add_option("-u", "--username", dest="username", type="string",
    help="The database connection password (default: environment"
        " variable, then nothing).")
parser.add_option("-p", "--password", dest="password", type="string",
    help="The database connection password (default: environment"
        " variable, then nothing).")
parser.add_option("-d", "--database", dest="database", 
    type="string", help="The database to convert. (REQUIRED)")
    
(options, args) = parser.parse_args()
    
if options.database == None: 
        parser.print_help()
        sys.exit(1)
    
config = DatabaseServerConfiguration(
    protocol = 'mysql',
    host_name = options.host,
    user_name = options.username,
    password = options.password,
    )

filterwarnings('ignore', 'Unknown table')
CreateBuildingsTable().create_buildings_table(config, options.database)

print('Done.')