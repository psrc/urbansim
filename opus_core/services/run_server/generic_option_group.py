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

from optparse import OptionParser, OptionGroup

from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration

class GenericOptionGroup:
    def __init__(self, usage="python %prog [options]", description=""):
            
        self.parser = OptionParser(usage=usage, description=description)                     
                     
        self.parser.add_option("--hostname", dest="host_name", default = None,
                               action="store", help="Name of host running services database server")
        self.parser.add_option("--username", dest="user_name", default = None,
                               action="store", help="Username for host running services database server")
        self.parser.add_option("--password", dest="password", default = None, 
                               action="store", help="Name of host running services database server")
        self.parser.add_option("--database", dest="database_name", default='services', 
                               action="store", help="Name of services database")
        self.parser.add_option("--protocol", dest="protocol", default=None, 
                               action="store", help="Name of database engine running the database management system hosting the services database. Available engines are sqlite (default), mysql, postgres, and mssql (less well tested).")
        
    def get_services_database_configuration(self, options):
        return ServicesDatabaseConfiguration(
                 protocol = options.protocol,
                 user_name = options.user_name,
                 password = options.password,
                 host_name = options.host_name,
                 database_name = options.database_name                                             
            )
        
        
    def parse(self):
        (options, args) = self.parser.parse_args()
        return (options,args)
        