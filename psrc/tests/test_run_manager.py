# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
import tempfile

from shutil import rmtree

from opus_core.logger import logger
from opus_core.tests import opus_unittest
from opus_core.services.run_server.run_manager import RunManager
from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration

from sqlalchemy.sql import select, func

### TODO: This should be re-written so that there is no psrc/urbansim 
###       dependency!
###       Once this has been done, move everything from this file and
###       delete_run_tests back into opus_core.
from psrc.configs.subset_configuration import SubsetConfiguration

def _do_run_simple_test_run(caller, temp_dir, config, end_year=None):
    """Runs model system with a single model (for speed).
    Sets the .resources property of the caller before starting the run.
    """
    runs_manager = RunManager(config)

    run_configuration = SubsetConfiguration()
    run_configuration['creating_baseyear_cache_configuration'].cache_directory_root = temp_dir
    run_configuration['models'] = ['land_price_model']
    if end_year is not None:
        run_configuration['years'] = (run_configuration['years'][0], end_year)
    
    SessionConfiguration(new_instance=True,
                         package_order=run_configuration['dataset_pool_configuration'].package_order,
                         in_storage=AttributeCache())
    insert_auto_generated_cache_directory_if_needed(run_configuration)
    caller.resources = run_configuration
    runs_manager.setup_new_run(cache_directory = run_configuration['cache_directory'],
                               configuration = run_configuration)
    runs_manager.run_run(run_configuration)
    

class RunManagerTests(opus_unittest.OpusIntegrationTestCase):
    ### TODO: These unit tests can be moved back to core once 
    ###       _do_run_simple_test_run() is no longer dependent on psrc.

    def setUp(self):
        self.config = TestDatabaseConfiguration(database_name = 'services_test')
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')

    def tearDown(self):
        # Turn off the logger, so we can delete the cache directory.
        logger.disable_all_file_logging()
        db_server = DatabaseServer(self.config)
        db_server.drop_database('services_test')
        db_server.close()

    def cleanup_test_run(self):
        cache_dir = self.resources['cache_directory']
        if os.path.exists(cache_dir):
            rmtree(cache_dir)
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        
    def test_restart_simple_run(self):
        _do_run_simple_test_run(self, self.temp_dir, self.config)
        runs_manager = RunManager(self.config)
        runs_manager.update_environment_variables(run_resources = SubsetConfiguration())
        
        run_activity = runs_manager.services_db.get_table('run_activity')
        s = select([func.max(run_activity.c.run_id)])
        run_id = runs_manager.services_db.execute(s).fetchone()[0]
        
        s = select([run_activity.c.status],
                   whereclause = run_activity.c.run_id == run_id)
        status = runs_manager.services_db.execute(s).fetchone()[0]
                                                                   
        expected = 'done'
        self.assertEqual(status, expected)
                        
        runs_manager.restart_run(run_id,
                                 restart_year=2001,
                                 project_name = SubsetConfiguration()['project_name'],
                                 skip_urbansim=False)
        
        s = select([run_activity.c.status],
                   whereclause = run_activity.c.run_id == run_id)
        status = runs_manager.services_db.execute(s).fetchone()[0]
                                                       
        expected = 'done'
        self.assertEqual(status, expected)
           
        # Restaring without running urbansim should not re-run that year.
        # TODO: test that no models are run this time.
        runs_manager.restart_run(run_id,
                                 restart_year=2002,
                                 project_name = SubsetConfiguration()['project_name'],
                                 skip_urbansim=True)
        s = select([run_activity.c.status],
                   whereclause = run_activity.c.run_id == run_id)
        status = runs_manager.services_db.execute(s).fetchone()[0]
                                                                   
        expected = 'done'
        self.assertEqual(status, expected)
                    
        self.cleanup_test_run()

if __name__ == "__main__":
    opus_unittest.main()