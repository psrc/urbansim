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

import os, pickle, shutil
from time import localtime, strftime

from opus_core.logger import logger
from opus_core.fork_process import ForkProcess
from opus_core.configuration import Configuration
from opus_core.store.utils.cache_flt_data import CacheFltData
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
from sqlalchemy.sql import select, and_, func
from opus_core.misc import get_host_name
from opus_core.database_management.table_type_schema import TableTypeSchema

class RunManager(object):
    """An abstraction representing a simulation manager that automatically logs
    runs (and their status) to a database (run_activity),
    creates resources for runs, and can run simulations.
    """

    def __init__(self, options):
        self.services_db = self.create_storage(options)
        self.run_id = None
        self.ready_to_run = False

    def create_baseyear_cache(self, resources):
        if resources['creating_baseyear_cache_configuration'].cache_from_mysql:
            ForkProcess().fork_new_process(
                resources['creating_baseyear_cache_configuration'].cache_scenario_database, resources)
        else:
            CacheFltData().run(resources)
    
    def setup_new_run(self, run_name):
        self.run_id = self._get_new_run_id()
        #compose unique cache directory based on the history_id
        head, tail = os.path.split(run_name)
        unique_cache_directory = os.path.join(head, 'run_%s.%s'%(self.run_id, tail))
        run_descr = self.run_id
               
        self.current_cache_directory = unique_cache_directory
        self.ready_to_run = True
        
        logger.log_status('Cache directory for run %s set to %s' % (run_descr, self.current_cache_directory))
            
    def get_current_cache_directory(self):
        if not self.ready_to_run:
            raise 'The RunManager has not been setup to run a new yet.'
        return self.current_cache_directory 
                
    def run_run(self, run_resources, run_as_multiprocess=True, run_in_background=False):
        """check run hasn't already been marked running
           log it in to run_activity
           run simulation
           mark run as done/failed
           """
        if not self.ready_to_run:
            raise 'RunManager.setup_new_run must be execute before RunManager.run_run'
        if run_resources['cache_directory'] != self.current_cache_directory:
            #TODO: do not change the configuration en route
            run_resources['cache_directory'] = self.current_cache_directory
            #raise 'The configuration and the RunManager conflict on the proper cache_directory'

        self.add_row_to_history(self.run_id, run_resources, "started")

        try:
            # Test pre-conditions
            model_system_class_path = run_resources.get('model_system', None)
            if model_system_class_path is None:
                raise TypeError, ("The configuration must specify model_system, the"
                    " full Opus path to the model system to be used.")
            
            # Create baseyear cache
            self.create_baseyear_cache(run_resources)
#            if run_resources['creating_baseyear_cache_configuration'].cache_from_mysql:
#                ForkProcess().fork_new_process(
#                    run_resources['creating_baseyear_cache_configuration'].cache_scenario_database, run_resources)
#            else:
#                CacheFltData().run(run_resources)
                
            # Create brand-new output database (deletes any prior contents)
            if 'output_configuration' in run_resources:
                try:
                    protocol = run_resources['output_configuration'].protocol
                except:
                    protocol = None
                    
                db_config = DatabaseServerConfiguration(
                    protocol = protocol,
                    host_name = run_resources['output_configuration'].host_name,
                    user_name = run_resources['output_configuration'].user_name,
                    password = run_resources['output_configuration'].password                                        
                )
                db_server = DatabaseServer(db_config)
                db_server.drop_database(run_resources["output_configuration"].database_name)
                db_server.create_database(run_resources["output_configuration"].database_name)                
            
            # Run simulation
            exec('from %s import ModelSystem' % model_system_class_path)
                
            model_system = ModelSystem()

            if 'base_year' not in run_resources:
                run_resources['base_year'] = run_resources['years'][0] - 1

            base_year = run_resources['base_year']

            if run_as_multiprocess:
                model_system.run_multiprocess(run_resources)
            else:
                model_system.run_in_one_process(run_resources, run_in_background=run_in_background, class_path=model_system_class_path)

        except:
            self.add_row_to_history(self.run_id, run_resources, "failed")
            self.ready_to_run = False
            raise # This re-raises the last exception
        else:
            self.add_row_to_history(self.run_id, run_resources, "done")
            
        self.ready_to_run = False
        

    def restart_run(self, run_id, restart_year,
                    skip_urbansim=False,
                    create_baseyear_cache_if_not_exists=False,
                    skip_cache_cleanup=False):
        """Restart the specified run."""

        run_resources = self.create_run_resources_from_history(
           run_id=run_id,
           restart_year=restart_year)
        try:
            if create_baseyear_cache_if_not_exists:
                cache_directory = run_resources['cache_directory']
                base_year = run_resources['base_year']
                if not os.path.exists(cache_directory) or not os.path.exists(os.path.join(cache_directory, str(base_year))):
                    self.create_baseyear_cache(run_resources)

            if os.path.isdir(run_resources['cache_directory']) and not os.path.exists(run_resources['cache_directory']):
                raise StandardError("cache directory doesn't exist: '%s'" % run_resources['cache_directory'])
    
            model_system = run_resources.get('model_system', None)
            if model_system is None:
                raise TypeError, ("The configuration must specify model_system, the"
                    " full Opus path to the model system to be used.")

            if not skip_cache_cleanup:
                # Delete 'year' folders left in the cache from a failed or stopped run (for years >= restart_year)
                year_to_purge = run_resources['years'][0]
                if skip_urbansim:
                    year_to_purge += 1
                if year_to_purge > run_resources['base_year']: # do not delete cache if it is the base year
                    while True:
                        dir_to_remove = os.path.join(run_resources['cache_directory'], str(year_to_purge))
                        if os.path.exists(dir_to_remove):
                            logger.log_status('Removing cache directory: %s' % dir_to_remove)
                            shutil.rmtree(dir_to_remove)
                            year_to_purge += 1
                        else:
                            break

            run_resources["skip_urbansim"] = skip_urbansim
            self.add_row_to_history(run_id, run_resources, "restarted in %d" % run_resources['years'][0])

            exec('from %s import ModelSystem' % model_system)

            # add years run
            model_system = ModelSystem()

            if 'base_year' not in run_resources:
                run_resources['base_year'] = run_resources['years'][0] - 1

            base_year = run_resources['base_year']
            
            model_system.run_multiprocess(run_resources)

            self.add_row_to_history(run_id, run_resources, "done")

        except:
            self.add_row_to_history(run_id, run_resources, "failed")
            raise

    def create_run_resources_from_history(self,
                                          run_id=None,
                                          restart_year=None,
                                          end_year=None
                                          ):
        """Re-creates and returns a resources dictionary given a specific entry in run_activity.
        Entirely based on the pickled "resources" field for that entry, which also
        contains a pickled version of the "run request" (a dictionary) associated with that entry."""
        if not run_id:
            raise StandardError("run_id un-specified")

        resources = self.get_resources_for_run_id_from_history(run_id=run_id)
        if 'cache_variables' not in resources:
            resources['cache_variables'] = False

        if not restart_year:
            raise StandardError("restart year un-specified")
        if restart_year < resources["years"][0]:
            raise StandardError("restart year cannot be less than %s" % resources["years"][0])

        #if no end_year is specified, it will default to the current end_year in "years" entry in resources
        if not end_year:
            end_year = resources["years"][-1]
        if 'base_year' not in resources:
            resources['base_year'] = resources['years'][0] - 1

        #set up resources for restarting the simulation
        resources["years"] = (restart_year, end_year)

        return resources
    
    ######## DATABASE OPERATIONS ###########
    
    def get_resources_for_run_id_from_history(self, run_id, filter_by_status = True):
        """Returns the resources for this run_id, as stored in the run_activity table.
        """

        run_activity = self.services_db.get_table('run_activity')
        
        if filter_by_status:
            whereclause = and_(
                        run_activity.c.status=='started',
                        run_activity.c.run_id==int(run_id))
        else:
            whereclause = run_activity.c.run_id==int(run_id)
            
        query = select(
            columns = [run_activity.c.resources],
            whereclause = whereclause)
        
        run_resources = self.services_db.engine.execute(query).fetchone()
        
        if not run_resources:
            raise StandardError("run_id %s doesn't exist on server %s" % (run_id, self.services_db.get_connection_string(scrub = True)))

        return Configuration(pickle.loads(str(run_resources[0])))
    
    def get_run_info(self, run_ids = None, resources = False, status = None):
        """ returns the name of the server where this run was processed"""

        #note: this method is never used in the codebase         
        run_activity = self.services_db.get_table('run_activity')
        
        cols = [run_activity.c.run_id,
                run_activity.c.run_name, 
                run_activity.c.processor_name]
        
        if resources:
            cols.append(run_activity.c.resources)
 
        query = select(columns = cols)
        if run_ids is not None:
            query = query.where(run_activity.c.run_id in run_ids)
            
        if status is not None:
            query = query.where(run_activity.c.status == status)
                        
        if resources:
            results = [(run_id, run_name, processor_name, Configuration(pickle.loads(str(run_resources)))) for \
                        run_id, run_name, processor_name, run_resources in \
                        self.services_db.engine.execute(query).fetchall() ]       

        else:
            results = [(run_id, run_name, processor_name) for \
                        run_id, run_name, processor_name in \
                        self.services_db.engine.execute(query).fetchall() ]       

        return results
    
    def get_runs_by_status(self, run_ids):
        """Returns a dictionary where keys are the status (e.g. 'started', 'done', 'failed').
        If run_ids is None, all runs from available runs are considered, otherwise only ids 
        given by the run_ids list.
        """
        map = {}
        run_activity_table = self.services_db.get_table('run_activity')
        s = select([run_activity_table.c.run_id, run_activity_table.c.status])
        for run_id, status in self.services_db.engine.execute(s).fetchall():
            if status in map:
                map[status].append(run_id)
            else:
                map[status] = [run_id]
        
        return map
    
    def _get_new_run_id(self):
        """Returns a unique run_id for a new run_activity trail."""
        
        run_activity = self.services_db.get_table('run_activity')
        query = select(
            columns = [func.max(run_activity.c.run_id),
                       func.count(run_activity.c.run_id)]
        )
        last_id, cnt = self.services_db.engine.execute(query).fetchone()
        
        if cnt > 0:
            run_id = last_id + 1
        else:
            run_id = 1

        return run_id

    def add_row_to_history(self, run_id, resources, status):
        """update the run history table to indicate changes to the state of this run history trail."""
        
        resources['run_id'] = run_id
        pickled_resources = pickle.dumps(resources)
        
        values = {'run_id':run_id, 
             'run_name':'%s' % resources.get('description', 'No description'),
             'status':'%s' % status,
             'processor_name':'%s' % get_host_name(), 
             'date_time':strftime('%Y-%m-%d %H:%M:%S', localtime()),
             'resources':'%s' % pickled_resources,
             }        

        run_activity_table = self.services_db.get_table('run_activity')
        if self.has_run(run_id):
            qry = run_activity_table.update(values = values,
                                            whereclause = run_activity_table.c.run_id == run_id)
        else:
            qry = run_activity_table.insert(values = values)

        self.services_db.engine.execute(qry)

    def has_run(self, run_id):
        run_activity_table = self.services_db.get_table('run_activity')
        qry = run_activity_table.select(whereclause=run_activity_table.c.run_id==run_id)
        return self.services_db.engine.execute(qry).fetchone() is not None
        
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
            raise Exception('Cannot connect to a services database')
        
        if not services_db.table_exists('run_activity'):
            tt_schema = TableTypeSchema()
            try:
                services_db.create_table(
                     'run_activity', 
                     tt_schema.get_table_schema('run_activity'))
            except:
                raise Exception('Cannot create the run_activity table in the services database')
        
        return services_db
            
    def get_cache_directory(self, run_id):
        resources = self.get_resources_for_run_id_from_history(run_id, filter_by_status = False)
        return resources['cache_directory']
        
    def get_years_run(self, cache_directory):
        years = []
        if os.path.exists(cache_directory):
            for dir in os.listdir(cache_directory):
                if len(dir) == 4 and dir.isdigit():
                    years.append(int(dir))
        return years
        
############## RUN REMOVAL ####################

    def clean_runs(self):
        for run_id, run_name, processor_name, resources in self.get_run_info(resources = True):
            if processor_name == get_host_name() and not os.path.exists(resources['cache_directory']):
                self.delete_everything_for_this_run(run_id, cache_directory = resources['cache_directory'])
        
    def delete_everything_for_this_run(self, run_id, cache_directory = None):
        """ removes the entire tree structure along with information """
        if cache_directory is None:
            cache_directory = self.get_cache_directory(run_id)
            
        try:
            shutil.rmtree(cache_directory,onerror = self._handle_deletion_errors)
            
            while os.path.exists(cache_directory):
                shutil.rmtree(cache_directory)
        except:
            pass
        
        run_activity_table = self.services_db.get_table('run_activity')
        
        query = run_activity_table.delete(run_activity_table.c.run_id==int(run_id))
        self.services_db.engine.execute(query)
           

        
    def delete_year_dirs_in_cache(self, run_id, years_to_delete=None):
        """ only removes the years cache and leaves the indicator, changes status to partial"""
        resources = self.get_resources_for_run_id_from_history(run_id, filter_by_status = False)
        cache_directory = resources['cache_directory']
        years_run = self.get_years_run(cache_directory)
        
        if years_to_delete is None:
            years_to_delete = years_run
            
        for year in years_to_delete:            
            year_dir = os.path.join(cache_directory, str(year))
            while os.path.exists(year_dir ):
                shutil.rmtree(year_dir, onerror=self._handle_deletion_errors)

        years_cached = [year for year in years_run if year not in years_to_delete]

        resources['years_run'] = years_cached
        
        values = {
                'resources':pickle.dumps(resources),
                'status':'partial'
        }

        run_activity = self.services_db.get_table('run_activity')

        query = run_activity.update(
            whereclause = run_activity.c.run_id == int(run_id),
            values = values
        )
        
        self.services_db.engine.execute(query)
                                         
    def _handle_deletion_errors(self, function, path, info):
        """try to close the file if it's a file """
        logger.log_warning('in run_manager._handle_deletion_errors: Trying  to delete %s error from function %s: \n %s' % (path,function.__name__,info[1]))
        if function.__name__ == 'remove':
            try:
                logger.disable_all_file_logging()
                file = open(path)
                file.close()
                os.remove(path)
            except:
                logger.log_warning('in run_manager._handle_deletion_errors:unable to delete %s error from function %s: \n %s' % (path,function.__name__,info[1]))
        else:
            logger.log_warning('in run_manager._handle_deletion_errors:unable to delete %s error from function %s: \n %s' % (path,function.__name__,info[1]))



class SimulationRunError(Exception):
    """exception to be raised if the simulation fails at runtime"""
    pass
            
def insert_auto_generated_cache_directory_if_needed(config):
    """Auto-generate a cache directory based upon current date-time."""
    cache_directory_root = config['creating_baseyear_cache_configuration'].cache_directory_root
    cache_directory = os.path.join(cache_directory_root, get_date_time_string())
    config['cache_directory'] = cache_directory
    
def get_date_time_string():
    return strftime('%Y_%m_%d_%H_%M', localtime())


from opus_core.tests import opus_unittest
from opus_core.database_management.database_configuration import DatabaseConfiguration
import tempfile 

class RunManagerTests(opus_unittest.OpusTestCase):
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
        
        run_manager = RunManager(self.config)
        
        self.assertTrue(db.table_exists('run_activity'))

    def test_create(self):
        """Should create run_activity table if the database doesn't exist."""
        run_manager = RunManager(self.config)
        
        self.assertTrue(self.db_server.has_database(self.database_name))
        db = self.db_server.get_database(self.database_name)
        self.assertTrue(db.table_exists('run_activity'))    

    def test_setup_run(self):
        base_directory = tempfile.mkdtemp(prefix='opus_tmp')
        run_name = 'test_scenario_name'
        run_manager = RunManager(self.config)
        
        run_manager.setup_new_run(run_name = os.path.join(base_directory, run_name))
        resulting_cache_directory = run_manager.get_current_cache_directory()
        self.assertTrue(resulting_cache_directory.find(run_name)>-1)
        self.assertEquals(os.path.dirname(resulting_cache_directory), base_directory)
        self.assertTrue(run_manager.ready_to_run)
        self.assertTrue(not os.path.exists(resulting_cache_directory))
        os.rmdir(base_directory)
        
    def test_add_row_to_history(self):
        run_manager = RunManager(self.config)
        cache_directory = tempfile.mkdtemp(prefix='opus_tmp')
        resources = {'cache_directory':cache_directory,
                     'description':'test_run',
                     'base_year':2000}
        
        run_manager.add_row_to_history(run_id = 1, 
                                       resources = resources, 
                                       status = 'done')
        
        db = self.db_server.get_database(self.database_name)
        run_activity_table = db.get_table('run_activity')
        
        s = select([run_activity_table.c.run_name,
                    run_activity_table.c.status],
                    whereclause = run_activity_table.c.run_id == 1)

        results = db.engine.execute(s).fetchall()
        self.assertEqual(len(results), 1)
        
        run_name, status = results[0]
        self.assertEqual(status, 'done')
        self.assertEqual(run_name, 'test_run')
        
        os.rmdir(cache_directory)
                
            
if __name__ == "__main__":
    opus_unittest.main()