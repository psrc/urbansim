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

from opus_core.database_management.database_configuration import DatabaseConfiguration

class GenericOptionGroup:
    def __init__(self, usage="python %prog [options]", description=""):
            
        self.parser = OptionParser(usage=usage, description=description)                     
                     
        self.parser.add_option("--hostname", dest="host_name", default = os.environ.get('OPUS_SERVICES_HOSTNAME', None),
                               action="store", help="Name of host running services database server")
        self.parser.add_option("--username", dest="user_name", default = os.environ.get('OPUS_SERVICES_USERNAME', None),
                               action="store", help="Username for host running services database server")
        self.parser.add_option("--password", dest="password", default = os.environ.get('OPUS_SERVICES_PASSWORD', None), 
                               action="store", help="Name of host running services database server")
        self.parser.add_option("--database", dest="database_name", default="services", 
                               action="store", help="Name of services database")
        self.parser.add_option("--protocol", dest="protocol", default=self._get_default_run_manager_database_engine(), 
                               action="store", help="Name of database engine running the database management system hosting the services database. Available engines are sqlite (default), mysql, postgres, and mssql (less well tested).")
        
    def _get_default_run_manager_database_engine(self):
        from opus_core.database_management.database_server_configuration import _get_installed_database_engines
        engines = _get_installed_database_engines()
        if 'sqlite' in engines:
            default = 'sqlite'
        else:
            default = DatabaseConfiguration()._get_default_database_engine()
            
        return os.environ.get('OPUS_SERVICES_DB_ENGINE', default)
        
    def parse(self):
        (options, args) = self.parser.parse_args()
        config = DatabaseConfiguration(host_name = options.host_name,
                                             user_name = options.user_name,
                                             protocol = options.protocol,
                                             password = options.password,
                                             database = options.database)
        return (options,args)
        