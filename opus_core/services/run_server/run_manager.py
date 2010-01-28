# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os, pickle, shutil, datetime
from time import localtime, strftime

from opus_core.logger import logger
from opus_core.fork_process import ForkProcess
from opus_core.configuration import Configuration
from opus_core.store.utils.cache_flt_data import CacheFltData
from opus_core.database_management.database_server import DatabaseServer
from sqlalchemy.sql import select, and_, func
from opus_core.misc import get_host_name
from opus_core.services.run_server.abstract_service import AbstractService

class RunManager(AbstractService):
    """An abstraction representing a simulation manager that automatically logs
    runs (and their status) to a database (run_activity),
    creates resources for runs, and can run simulations.
    """

    def __init__(self, options):

        AbstractService.__init__(self, options)
        self.run_id = None
        self.ready_to_run = False
        self.model_system = None

    def create_baseyear_cache(self, resources):
        if resources['creating_baseyear_cache_configuration'].cache_from_database:
            ForkProcess().fork_new_process(
                resources['creating_baseyear_cache_configuration'].cache_scenario_database, resources)
        else:
            CacheFltData().run(resources)

    def setup_new_run(self, cache_directory, configuration):
        #compose unique cache directory based on the history_id
        self.update_environment_variables(configuration)
        self.run_id = self._get_new_run_id()

        if not os.path.exists(cache_directory):
            head, tail = os.path.split(cache_directory)
            unique_cache_directory = os.path.join(head, 'run_%s.%s'%(self.run_id, tail))
        else:
            unique_cache_directory = cache_directory

        self.current_cache_directory = unique_cache_directory
        self.ready_to_run = True
        configuration['cache_directory'] = unique_cache_directory
        logger.log_status('Cache directory for run %s set to %s' % (self.run_id, self.current_cache_directory))

    def get_current_cache_directory(self):
        if not self.ready_to_run:
            raise 'The RunManager has not been setup to run a new yet.'
        return self.current_cache_directory

    def update_environment_variables(self, run_resources):
        if 'project_name' in run_resources:
            os.environ['OPUSPROJECTNAME'] = run_resources['project_name']
            self.services_db.close()
            self.services_db = self.create_storage()

    def run_run(self, run_resources, run_name = None, run_as_multiprocess=True, run_in_background=False):
        """check run hasn't already been marked running
           log it in to run_activity
           run simulation
           mark run as done/failed
           """

        if not self.ready_to_run:
            raise 'RunManager.setup_new_run must be execute before RunManager.run_run'

        if run_resources['cache_directory'] != self.current_cache_directory:
            raise 'The configuration and the RunManager conflict on the proper cache_directory'

        self.add_row_to_history(self.run_id, run_resources, "started", run_name = run_name)

        try:
            # Test pre-conditions
            model_system_class_path = run_resources.get('model_system', None)
            if model_system_class_path is None:
                raise TypeError, ("The configuration must specify model_system, the"
                    " full Opus path to the model system to be used.")

            # Create baseyear cache
            self.create_baseyear_cache(run_resources)

            # Create brand-new output database (deletes any prior contents)
            if 'estimation_database_configuration' in run_resources:
                db_server = DatabaseServer(run_resources['estimation_database_configuration'])
                if not db_server.has_database(run_resources['estimation_database_configuration'].database_name):
                    db_server.create_database(run_resources['estimation_database_configuration'].database_name)


            # Run simulation
            exec('from %s import ModelSystem' % model_system_class_path)

            model_system = ModelSystem()
            self.model_system = model_system

            if 'base_year' not in run_resources:
                run_resources['base_year'] = run_resources['years'][0] - 1

#            model_system.run_in_same_process(run_resources)
            if run_as_multiprocess:
                model_system.run_multiprocess(run_resources)
            else:
                model_system.run_in_one_process(run_resources, run_in_background=run_in_background, class_path=model_system_class_path)

            self.model_system = None

        except:
            self.add_row_to_history(self.run_id, run_resources, "failed", run_name = run_name)
            self.ready_to_run = False
            raise # This re-raises the last exception
        else:
            self.add_row_to_history(self.run_id, run_resources, "done", run_name = run_name)

        self.ready_to_run = False
        return self.run_id

    def cancel_run(self):
        self.delete_everything_for_this_run(run_id = self.run_id, cache_directory = self.current_cache_directory)

    def restart_run(self, run_id, restart_year, project_name,
                    skip_urbansim=False,
                    create_baseyear_cache_if_not_exists=False,
                    skip_cache_cleanup=False):
        """Restart the specified run."""

        if project_name:
            self.update_environment_variables(run_resources = {'project_name':project_name}) 

        run_resources = self.create_run_resources_from_history(
           run_id=run_id,
           restart_year=restart_year)

        run_tbl = self.services_db.get_table('run_activity')
        s = select([run_tbl.c.run_name], whereclause = run_tbl.c.run_id == run_id)
        run_name = self.services_db.execute(s).fetchone()[0]

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
            self.add_row_to_history(run_id, run_resources, "restarted in %d" % run_resources['years'][0], run_name = run_name)

            exec('from %s import ModelSystem' % model_system)

            # add years run
            model_system = ModelSystem()

            if 'base_year' not in run_resources:
                run_resources['base_year'] = run_resources['years'][0] - 1

            base_year = run_resources['base_year']

            model_system.run_multiprocess(run_resources)

            self.add_row_to_history(run_id, run_resources, "done", run_name = run_name)

        except:
            self.add_row_to_history(run_id, run_resources, "failed", run_name = run_name)
            raise

    def create_run_resources_from_history(self,
                                          run_id,
                                          restart_year,
                                          end_year=None
                                          ):
        """Re-creates and returns a resources dictionary given a specific entry in run_activity.
        Entirely based on the pickled "resources" field for that entry, which also
        contains a pickled version of the "run request" (a dictionary) associated with that entry."""

        resources = self.get_resources_for_run_id_from_history(run_id=run_id)
        if 'cache_variables' not in resources:
            resources['cache_variables'] = False

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

    def get_resources_for_run_id_from_history(self, run_id, filter_by_status = False):
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

        run_resources = self.services_db.execute(query).fetchone()

        if not run_resources:
            raise StandardError("run_id %s doesn't exist on server %s" % (run_id, self.services_db.get_connection_string(scrub = True)))

        try:
            config = Configuration(pickle.loads(str(run_resources[0])))
        except:
            raise Exception('Could not create the configuration file for run %i'%run_id)

        return config

    def get_run_id_from_name(self, run_name):
        run_activity = self.services_db.get_table('run_activity')

        query = select([run_activity.c.run_id],
                       whereclause = run_activity.c.run_name == run_name)
        results = self.services_db.execute(query).fetchall()
        if len(results) > 1:
            raise Exception('Error: Multiple runs with the name %s'%run_name)
        elif len(results) == 0:
            raise Exception('Error: Cannot find a run with the name %s'%run_name)
        else:
            return results[0][0]

    def get_run_info(self, run_ids = None, resources = False, status = None, soft_fail = True):
        """ returns the name of the server where this run was processed"""

        run_activity = self.services_db.get_table('run_activity')

        if 'run_description' in run_activity.c:
            run_description_col = run_activity.c.run_description
        else:
            run_description_col = run_activity.c.run_name

        cols = [run_activity.c.run_id,
                run_activity.c.run_name,
                run_description_col,
                run_activity.c.processor_name]

        if resources:
            cols.append(run_activity.c.resources)

        query = select(columns = cols)
        if run_ids is not None:
            query = query.where(run_activity.c.run_id.in_(run_ids))

        if status is not None:
            query = query.where(run_activity.c.status == status)

        if resources:
            results = []
            for run_id, run_name, run_description, processor_name, run_resources in self.services_db.execute(query).fetchall():
                try:
                    config = pickle.loads(str(run_resources))
                    results.append((run_id, run_name, run_description, processor_name,config))
                except:
                    if not soft_fail: raise

        else:
            results = self.services_db.execute(query).fetchall()

        return results

    def get_runs_by_status(self, run_ids = None):
        """Returns a dictionary where keys are the status (e.g. 'started', 'done', 'failed').
        If run_ids is None, all runs from available runs are considered, otherwise only ids
        given by the run_ids list.
        """
        map = {}
        run_activity_table = self.services_db.get_table('run_activity')
        s = select([run_activity_table.c.run_id, run_activity_table.c.status])
        for run_id, status in self.services_db.execute(s).fetchall():
            if run_ids is None or run_id in run_ids:
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

        #print self.services_db.get_connection_string()
        last_id, cnt = self.services_db.execute(query).fetchone()

        if cnt > 0:
            run_id = last_id + 1
        else:
            run_id = 1

        return run_id

    def add_row_to_history(self, run_id, resources, status, run_name = None):
        """update the run history table to indicate changes to the state of this run history trail."""

        self.update_environment_variables(run_resources = resources)
        resources['run_id'] = run_id
        pickled_resources = pickle.dumps(resources)
        description = resources.get('description', 'No description')
        if run_name is None:
            run_name = description

        values = {'run_id':run_id,
             'run_name': run_name,
             'run_description':'%s' % description,
             'status':'%s' % status,
             'processor_name':'%s' % get_host_name(),
             'date_time':datetime.datetime.now(),
             'resources':'%s' % pickled_resources,
             'cache_directory': resources['cache_directory'],
             'project_name': resources.get('project_name', None)
             }

        run_activity_table = self.services_db.get_table('run_activity')
        if not 'project_name' in run_activity_table.c:
            del values['project_name']

        if self.has_run(run_id):
            qry = run_activity_table.update(values = values,
                                            whereclause = run_activity_table.c.run_id == run_id)
        else:
            qry = run_activity_table.insert(values = values)

        self.services_db.execute(qry)

    def has_run(self, run_id):
        run_activity_table = self.services_db.get_table('run_activity')
        qry = run_activity_table.select(whereclause=run_activity_table.c.run_id==run_id)
        return self.services_db.execute(qry).fetchone() is not None

    def get_cache_directory(self, run_id):
        resources = self.get_resources_for_run_id_from_history(run_id, filter_by_status = False)
        return resources['cache_directory']

    def get_years_run(self, cache_directory, baseyear = -1):
        years = []

        if os.path.exists(cache_directory):
            for dir in os.listdir(cache_directory):
                if len(dir) == 4 and dir.isdigit() and int(dir) >= baseyear:
                    years.append(int(dir))
        return years

############## RUN REMOVAL ####################

    def clean_runs(self):
        for run_id, run_name, run_description, processor_name, resources in self.get_run_info(resources = True):
            if processor_name == get_host_name() and not os.path.exists(resources['cache_directory']):
                self.delete_everything_for_this_run(run_id, cache_directory = resources['cache_directory'])

    def delete_everything_for_this_run(self, run_id, cache_directory = None):
        """ removes the entire tree structure along with information """
        if cache_directory is None:
            cache_directory = self.get_cache_directory(run_id)

        try:
            ##TODO: why this line is needed when the line below does the same thing and better
            #shutil.rmtree(cache_directory,onerror = self._handle_deletion_errors)

            while os.path.exists(cache_directory):
                shutil.rmtree(cache_directory, onerror = self._handle_deletion_errors)
        except:
            pass

        run_activity_table = self.services_db.get_table('run_activity')

        query = run_activity_table.delete(run_activity_table.c.run_id==int(run_id))
        self.services_db.execute(query)



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

        self.services_db.execute(query)

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
    """
    Insert an auto generated cache directory with current date-time in cache_directory_root to config.
    Do nothing if
    1. 'cache_directory' is in config's keys with non-None value, and
    2. a) the specified cache_directory doesn't exists, or
       b) the specified cache_directory exists, but 'overwrite_cache_directory_if_exists' is set to True

    """
    insert_auto_generated_cache_directory = True
    if config.has_key('cache_directory') and config['cache_directory'] is not None:
        if not os.path.exists(config['cache_directory']):
            insert_auto_generated_cache_directory = False
        elif config.has_key('overwrite_cache_directory_if_exists') and config['overwrite_cache_directory_if_exists'] is True:
            insert_auto_generated_cache_directory = False

    if insert_auto_generated_cache_directory:
        cache_directory_root = config['creating_baseyear_cache_configuration'].cache_directory_root
        date_time_string = strftime('%Y_%m_%d_%H_%M', localtime())
        cache_directory = os.path.join(cache_directory_root, date_time_string)
        config['cache_directory'] = cache_directory

from opus_core.tests import opus_unittest
from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration
import tempfile

class RunManagerTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.database_name = 'test_services_database'
        self.config = TestDatabaseConfiguration(database_name = self.database_name)
        self.db_server = DatabaseServer(self.config)

    def tearDown(self):
        self.db_server.drop_database(self.database_name)
        self.db_server.close()

    def test_setup_run(self):
        base_directory = tempfile.mkdtemp(prefix='opus_tmp')
        run_name = 'test_scenario_name'
        run_manager = RunManager(self.config)

        run_manager.setup_new_run(cache_directory = os.path.join(base_directory, run_name),
                                  configuration = {})
        resulting_cache_directory = run_manager.get_current_cache_directory()
        self.assertTrue(resulting_cache_directory.find(run_name)>-1)
        self.assertEquals(os.path.dirname(resulting_cache_directory), base_directory)
        self.assertTrue(run_manager.ready_to_run)
        self.assertTrue(not os.path.exists(resulting_cache_directory))
        run_manager.services_db.close()
        os.rmdir(base_directory)

    def test_add_row_to_history(self):
        run_manager = RunManager(self.config)
        cache_directory = tempfile.mkdtemp(prefix='opus_tmp')
        resources = {'cache_directory':cache_directory,
                     'description':'test_run',
                     'base_year':2000,
                     'project_name': 'test'}

        run_manager.add_row_to_history(run_id = 1,
                                       resources = resources,
                                       status = 'done')

        db = self.db_server.get_database(self.database_name)
        run_activity_table = db.get_table('run_activity')

        s = select([run_activity_table.c.run_description,
                    run_activity_table.c.status],
                    whereclause = run_activity_table.c.run_id == 1)

        results = db.execute(s).fetchall()
        self.assertEqual(len(results), 1)

        run_name, status = results[0]
        self.assertEqual(status, 'done')
        self.assertEqual(run_name, 'test_run')

        run_manager.services_db.close()
        os.rmdir(cache_directory)


if __name__ == "__main__":
    opus_unittest.main()
