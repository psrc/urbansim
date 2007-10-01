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
import tempfile

from shutil import rmtree

from opus_core.logger import logger
from opus_core.tests import opus_unittest
from opus_core.table_type_schema import TableTypeSchema
from opus_core.services.run_server.run_manager import RunManager
from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed
from opus_core.services.run_server.run_activity import RunActivity
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
from opus_core.store.attribute_cache import AttributeCache
from opus_core.misc import does_database_server_exist_for_this_hostname
from opus_core.session_configuration import SessionConfiguration

### TODO: This should be re-written so that there is no psrc/urbansim 
###       dependency!
###       Once this has been done, move everything from this file and
###       delete_run_tests back into opus_core.
from psrc.configs.subset_configuration import SubsetConfiguration


def _create_services_test_database():
    """Creates the 'services_test' database on localhost.
    Returns database.
    """
    db_server = DatabaseServer(DatabaseServerConfiguration())
    db_server.drop_database('services_test')
    db_server.create_database('services_test')
    services_database = db_server.get_database('services_test')

    tt_schema = TableTypeSchema();
    services_database.create_table("run_activity",
                                   tt_schema.get_table_schema("run_activity"))
    return services_database

def _drop_services_test_database():
    """Drops the 'services_test' database on localhost.
    """
    db_server = DatabaseServer(DatabaseServerConfiguration())
    db_server.drop_database('services_test')
    
def _do_run_simple_test_run(caller, temp_dir, services_database, end_year=None):
    """Runs model system with a single model (for speed).
    Sets the .resources property of the caller before starting the run.
    """
    run_activity = RunActivity(services_database)
    runs_manager = RunManager(run_activity)

    run_configuration = SubsetConfiguration()
    run_configuration['creating_baseyear_cache_configuration'].cache_directory_root = temp_dir
    run_configuration['models'] = ['land_price_model']
    if end_year is not None:
        run_configuration['years'] = (run_configuration['years'][0], end_year)
    
    SessionConfiguration(new_instance=True,
                         package_order=run_configuration['dataset_pool_configuration'].package_order,
                         package_order_exceptions=run_configuration['dataset_pool_configuration'].package_order_exceptions,
                         in_storage=AttributeCache())
    insert_auto_generated_cache_directory_if_needed(run_configuration)
    caller.resources = run_configuration
    runs_manager.run_run(run_configuration)
    

if does_database_server_exist_for_this_hostname(
        module_name = __name__, 
        hostname = SubsetConfiguration()['input_configuration'].host_name):
    
    class RunManagerTests(opus_unittest.OpusTestCase):
        ### TODO: These unit tests can be moved back to core once 
        ###       _do_run_simple_test_run() is no longer dependent on psrc.
    
        def setUp(self):
            self.services_database = _create_services_test_database()
            self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
            _do_run_simple_test_run(self, self.temp_dir, self.services_database)
    
        def tearDown(self):
            # Turn off the logger, so we can delete the cache directory.
            logger.disable_all_file_logging()
            cache_dir = self.resources['cache_directory']
            if os.path.exists(cache_dir):
                rmtree(cache_dir)
            if os.path.exists(self.temp_dir):
                rmtree(self.temp_dir)
            _drop_services_test_database()
    
        def test_restart_simple_run(self):
            run_activity = RunActivity(self.services_database)
            runs_manager = RunManager(run_activity)
            history_id = run_activity.storage.GetResultsFromQuery("SELECT max(run_id) FROM run_activity")[1][0]
            statuses = run_activity.storage.GetResultsFromQuery("select status from run_activity where run_id=%d order by date_time"
                                                           % history_id)[1:]
                                                           
            expected = [['started'], ['done']]
            print 'expected: ',expected
            print 'output: ', statuses
            
            for i in expected:
                self.assertTrue(i in statuses)
                
            self.assertEqual(len(statuses), len(expected))
                
            db_config = DatabaseServerConfiguration()
            
            runs_manager.restart_run(history_id,
                                     restart_year=2001,
                                     services_host_name= db_config.host_name,
                                     services_database_name='services_test',
                                     skip_urbansim=False)
            
            statuses = run_activity.storage.GetResultsFromQuery("select status from run_activity where run_id=%d order by date_time"
                                                           % history_id)[1:]
                                                           
            expected = [['started'], ['done'], ['restarted in 2001'], ['done']]
            
            for i in expected:
                self.assertTrue(i in statuses)
                
            self.assertEqual(len(statuses), len(expected))
    
            # Restaring without running urbansim should not re-run that year.
            # TODO: test that no models are run this time.
            runs_manager.restart_run(history_id,
                                     restart_year=2002,
                                     services_host_name=db_config.host_name,
                                     services_database_name='services_test',
                                     skip_urbansim=True)
            statuses = run_activity.storage.GetResultsFromQuery("select status from run_activity where run_id=%d order by date_time"
                                                           % history_id)[1:]
                                                           
            expected = [['started'], ['done'], ['restarted in 2001'], ['done'], ['restarted in 2002'], ['done']]       
                                                    
            print 'expected: ',expected
            print 'output: ', statuses

            for i in expected:
                self.assertTrue(i in statuses)
                
            self.assertEqual(len(statuses), len(expected))

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    opus_unittest.main()