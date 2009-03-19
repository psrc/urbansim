# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os
import sys

from optparse import OptionParser

from classes.rename_by_swapping_employment_and_commercial_or_industrial_or_home_based_for_elcm\
    import RenameBySwappingEmploymentAndCommercialOrIndustrialOrHomeBasedForElcm
    
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration

    
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
        
r = RenameBySwappingEmploymentAndCommercialOrIndustrialOrHomeBasedForElcm()
r.rename_by_swapping_employment_and_commercial_or_industrial_or_home_based_for_elcm(config, 
    options.database)
print 'Done.'
