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

import os

from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
from opus_core.services.services_tables import ResultsComputedIndicators, RunsRunActivity
from elixir import setup_all, metadata, create_all


class AbstractService(object):
    """An abstraction representing a simulation manager that automatically logs
    runs (and their status) to a database (run_activity),
    creates resources for runs, and can run simulations.
    """

    def __init__(self, options):
        
        self.services_db = self.create_storage(options)
        self.server_config = options
        
    def create_storage(self, options):

        try:
            database_name = options.database_name
        except:
            database_name = 'services'

        config = DatabaseServerConfiguration(
                     host_name = options.host_name,
                     user_name = options.user_name,
                     protocol = options.protocol,
                     password = options.password)
        try:
            server = DatabaseServer(config)
        except:
            raise Exception('Cannot connect to the database server that the services database is hosted on')
        
        if not server.has_database(database_name):
            server.create_database(database_name)

        try:
            services_db = server.get_database(database_name)
        except:
            raise Exception('Cannot connect to a services database on %s'%server.get_connection_string(scrub = True))

        metadata.bind = services_db.engine
        setup_all()
        create_all()
        
        return services_db

    def close(self):
        self.services_db.close()
    
    
from opus_core.tests import opus_unittest
from opus_core.database_management.database_configurations.database_configuration import DatabaseConfiguration
import tempfile 

class AbstractServiceTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.database_name = 'test_services_database'
        self.config = DatabaseConfiguration(protocol = 'sqlite',
                                            test = True, 
                                            database_name = self.database_name)
        self.db_server = DatabaseServer(self.config)
    
    def tearDown(self):
        self.db_server.drop_database(self.database_name)
        self.db_server.close()
        
    def test_create_when_already_exists(self):
        """Shouldn't do anything if the database already exists."""
        self.db_server.create_database(self.database_name)
        db = self.db_server.get_database(self.database_name)
        self.assertFalse(db.table_exists('run_activity'))
        self.assertFalse(db.table_exists('computed_indicators'))

        services = AbstractService(self.config)
        services.services_db.close()
        self.assertTrue(db.table_exists('run_activity')) 
        self.assertTrue(db.table_exists('computed_indicators'))

    def test_create(self):
        """Should create services tables if the database doesn't exist."""
        services = AbstractService(self.config)
        services.services_db.close()
        
        self.assertTrue(self.db_server.has_database(self.database_name))
        db = self.db_server.get_database(self.database_name)
        self.assertTrue(db.table_exists('run_activity')) 
        self.assertTrue(db.table_exists('computed_indicators'))               
         
if __name__ == "__main__":
    opus_unittest.main()