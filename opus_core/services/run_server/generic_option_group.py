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

from optparse import OptionParser, OptionGroup

from opus_core.services.run_server.run_manager import RunManager


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
        self.parser.add_option("--protocol", dest="protocol", default=os.environ.get('OPUS_SERVICES_DB_ENGINE', 'sqlite'), 
                               action="store", help="Name of database engine running the database management system hosting the services database.")

#    def get_services_database(self, options):
#        """Gets services database from the specified database."""
#        
#        db_server = self.get_database_server(options)
#        
#        if db_server is None:
#            return None
#        
#        if db_server.has_database(options.database_name):
#            return db_server.get_database(options.database_name)
#        else:
#            return None
    
        