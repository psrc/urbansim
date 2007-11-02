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
from opus_core.services.run_server.run_activity import RunActivity
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration

class GenericOptionGroup:
    def __init__(self, usage="python %prog [options]", description=""):
            
        self.parser = OptionParser(usage=usage, description=description)
        
        self.parser.add_option("--hostname", dest="host_name", 
                               action="store", help="Name of host running services database server")
        self.parser.add_option("--database", dest="database_name", default="services", 
                               action="store", help="Name of services database")
        
    def get_run_manager(self, options):
        """Returns a RunManager object.
        
        RunManager will have access to run activity info, if its database exists."""
        db = self.get_services_database(options)
    
        if db is None:
            return RunManager()
        
        run_activity = RunActivity(db)
        return RunManager(run_activity)
        

    def get_services_database(self, options):
        """Gets services database from the specified database."""
        
        db_server = self.get_database_server(options)
        
        if db_server is None:
            return None
        
        if db_server.has_database(options.database_name):
            return db_server.get_database(options.database_name)
        else:
            return None
        
    def get_database_server(self, options):
        """Gets database server for the specified db connection."""
        if options.host_name is None:
            return None
        
        config = DatabaseServerConfiguration(
            host_name = options.host_name,
            )
        try:
            db_server = DatabaseServer(config)
            return db_server
        except:
            # Cannot connect to database server
            return None
        