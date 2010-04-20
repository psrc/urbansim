# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.database_management.database_server import DatabaseServer
from opus_core.services.services_tables import *
from opus_core.logger import logger
from elixir import setup_all, metadata, create_all


class AbstractService(object):
    """An abstraction representing a simulation manager that automatically logs
    runs (and their status) to a database (run_activity),
    creates resources for runs, and can run simulations.
    """

    def __init__(self, config):
        
        self.server_config = config

        self.services_db = self.create_storage()
        
    def create_storage(self):

        try:
            server = DatabaseServer(self.server_config)
        except:
            logger.log_error('Cannot connect to the database server that the services database is hosted on %s.' % self.server_config.database_name)
            raise
        
        if not server.has_database(self.server_config.database_name):
            server.create_database(self.server_config.database_name)

        try:
            services_db = server.get_database(self.server_config.database_name)
        except:
            logger.log_error('Cannot connect to a services database on %s.'% server.get_connection_string(scrub = True))
            raise

        metadata.bind = services_db.engine
        setup_all()
        create_all()
        
        return services_db

    def close(self):
        self.services_db.close()
    
    
from opus_core.tests import opus_unittest
from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration

class AbstractServiceTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.database_name = 'test_services_database'
        self.config = TestDatabaseConfiguration(database_name = self.database_name)
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