# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, pickle, shutil, datetime, zlib
from time import localtime, strftime
from numpy import array
from numpy.random import seed, randint
from opus_core.logger import logger
from opus_core.fork_process import ForkProcess
from opus_core.configuration import Configuration
from opus_core.store.utils.cache_flt_data import CacheFltData
from opus_core.database_management.database_server import DatabaseServer
from sqlalchemy.sql import select, and_, func
from opus_core.misc import get_host_name
from opus_core.services.run_server.abstract_service import AbstractService
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.version_numbers import get_opus_version_number

NO_SEED = None

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
            
        assert(os.path.isdir(self.current_cache_directory))
        self.write_run_config(resources)

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
            
    def write_run_config(self, run_resources):
        statusdir = self.current_cache_directory
        
        xml_full_file_name = run_resources.get('xml_file')
        if xml_full_file_name:
            xml_config = XMLConfiguration(xml_full_file_name)
            xml_file_name = os.path.basename(xml_full_file_name)
            file_name, ext = os.path.splitext(xml_file_name)
            xml_file_name_flattened = os.path.join(statusdir, file_name + "_flattened" + ext)
            xml_config.full_tree.write(xml_file_name_flattened, pretty_print=True)
        
        # # it may be better to save it with the run in services/run_activity database table
        version_numbers = get_opus_version_number()
        version_file = os.path.join(statusdir, "opus_version_number.txt")
        with open(version_file, 'w') as f:
            f.write(version_numbers)

    def run_run(self, run_resources, run_name = None, scenario_name=None, run_as_multiprocess=True, run_in_background=False):
        """check run hasn't already been marked running
           log it in to run_activity
           run simulation
           mark run as done/failed
           """
        if not self.ready_to_run:
            raise 'RunManager.setup_new_run must be execute before RunManager.run_run'

        if run_resources['cache_directory'] != self.current_cache_directory:
            raise 'The configuration and the RunManager conflict on the proper cache_directory'

        run_resources['run_id'] = self.run_id
        if scenario_name is not None:
            run_resources['scenario_name'] = scenario_name

        self.add_row_to_history(self.run_id, run_resources, "started", 
                                run_name=run_name, scenario_name=scenario_name)

        try:
            # Test pre-conditions
            model_system_class_path = run_resources.get('model_system', None)
            if model_system_class_path is None:
                raise TypeError("The configuration must specify model_system, the"
                    " full Opus path to the model system to be used.")

            # Create baseyear cache
            self.create_baseyear_cache(run_resources)

            # Create brand-new output database (deletes any prior contents)
            if 'estimation_database_configuration' in run_resources:
                db_server = DatabaseServer(run_resources['estimation_database_configuration'])
                if not db_server.has_database(run_resources['estimation_database_configuration'].database_name):
                    db_server.create_database(run_resources['estimation_database_configuration'].database_name)


            # Run simulation
            exec('from %s import ModelSystem' % model_system_class_path, globals())

            model_system = ModelSystem()
            self.model_system = model_system

            if 'base_year' not in run_resources:
                run_resources['base_year'] = run_resources['years'][0] - 1
            
            base_year = run_resources['base_year']
            ## create a large enough seed_array so that a restarted run
            ## can still have seed when running pass the original end_year
            ## the size needed to store seed_dict of 100 seeds is about 12568 Bytes
            self._create_seed_dictionary(run_resources, 
                                         start_year=base_year,
                                         end_year=base_year+100)
            
            if 'run_in_same_process' in run_resources and run_resources['run_in_same_process']:
                model_system.run_in_same_process(run_resources)
            elif run_as_multiprocess:
                model_system.run_multiprocess(run_resources)
            else:
                model_system.run_in_one_process(run_resources, 
                                                run_in_background=run_in_background, 
                                                class_path=model_system_class_path)

            self.model_system = None

        except:
            self.add_row_to_history(self.run_id, run_resources, "failed", 
                                    run_name=run_name, scenario_name=scenario_name)
            self.ready_to_run = False
            raise # This re-raises the last exception
        else:
            self.add_row_to_history(self.run_id, run_resources, "done", 
                                    run_name=run_name, scenario_name=scenario_name)

        self.ready_to_run = False
        return self.run_id

    def cancel_run(self):
        self.delete_everything_for_this_run(run_id = self.run_id, cache_directory = self.current_cache_directory)

    def restart_run(self, run_id, restart_year, project_name,
                    end_year=None,
                    skip_urbansim=False,
                    create_baseyear_cache_if_not_exists=False,
                    skip_cache_cleanup=False, run_as_multiprocess=True, run_in_background=False):
        """Restart the specified run."""

        if project_name:
            self.update_environment_variables(run_resources = {'project_name':project_name}) 

        run_resources = self.create_run_resources_from_history(
                                                               run_id=run_id,
                                                               restart_year=restart_year,
                                                               end_year=end_year)

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
                raise Exception("cache directory doesn't exist: '%s'" % run_resources['cache_directory'])

            model_system_class_path = run_resources.get('model_system', None)
            if model_system_class_path is None:
                raise TypeError("The configuration must specify model_system, the"
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

            exec('from %s import ModelSystem' % model_system_class_path, globals())

            # add years run
            model_system = ModelSystem()

            if 'base_year' not in run_resources:
                run_resources['base_year'] = run_resources['years'][0] - 1

            base_year = run_resources['base_year']

            if 'run_in_same_process' in run_resources and run_resources['run_in_same_process']:
                model_system.run_in_same_process(run_resources)
            elif run_as_multiprocess:
                model_system.run_multiprocess(run_resources)
            else:
                model_system.run_in_one_process(run_resources, 
                                                run_in_background=run_in_background, 
                                                class_path=model_system_class_path)
        except:
            self.add_row_to_history(run_id, run_resources, "failed", run_name = run_name)
            raise
        else:
            self.add_row_to_history(run_id, run_resources, "done", run_name = run_name)

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

        #if restart_year < resources["years"][0]:
        #    raise StandardError("restart year cannot be less than %s" % resources["years"][0])

        #if no end_year is specified, it will default to the current end_year in "years" entry in resources
        if end_year is None:
            end_year = resources["years"][-1]
        
        if end_year < restart_year:
            raise ValueError("restart year (%s) cannot be less than end_year (%s)" % (restart_year, end_year)) 
        
        if 'base_year' not in resources:
            resources['base_year'] = resources['years'][0] - 1

        #set up resources for restarting the simulation
        resources["years"] = (restart_year, end_year)

        return resources

    def _create_seed_dictionary(self, resources, start_year=None, end_year=None):
        """Create a dictionary of seeds (one dict item per year) and add it to the resources under the name
        '_seed_dictionary_'. That way one can reproduce results also for simulations that are restarted.
        
        """
        root_seed = resources.get("seed", NO_SEED)
        seed(root_seed)
        start_year = start_year if start_year is not None else resources["years"][0]
        end_year = end_year if end_year is not None else resources["years"][-1]
        seed_dict = dict( list(zip(list(range(start_year, end_year+1)),
                              randint(1,2**30, end_year-start_year+1)
                              ))
                          )
        
        resources['_seed_dictionary_'] = seed_dict
        
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
            raise Exception("run_id %s doesn't exist on server %s" % (run_id, self.services_db.get_connection_string(scrub = True)))

        try:
            r = self._unpickle(run_resources[0])
            config = Configuration(r)
        except:
            logger.log_error('Could not create the configuration file for run %i'%run_id)
            raise

        return config

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

    def get_runs(self, return_columns=['run_id'], return_rs=False, **kwargs):
        run_activity = self.services_db.get_table('run_activity')
        whereclause = run_activity.c.run_id > 0
        for k, v in list(kwargs.items()):
            if k in run_activity.c:
                whereclause = and_(whereclause, run_activity.c[k]==v)
        
        if isinstance(return_columns, list):
            assert all([ c in run_activity.c for c in return_columns]), \
                   "all return_columns have to be a column in run_activity"
            
            return_columns = [run_activity.c[c] for c in return_columns]
        query = select(columns=return_columns,
                       whereclause=whereclause)
        results = self.services_db.execute(query)
        if not return_rs:
            return results.fetchall()
        else:
            return results
    
    def get_runs_by_name(self, run_name):
        return self.get_runs(run_name=run_name)

    def has_run(self, **kwargs):
        results = self.get_runs(**kwargs)
        if len(results) >= 1:
            return True
        else:
            return False
        
    #def has_run(self, run_id):
        #run_activity_table = self.services_db.get_table('run_activity')
        #qry = run_activity_table.select(whereclause=run_activity_table.c.run_id==run_id)
        #return self.services_db.execute(qry).fetchone() is not None

    def _unpickle(self, resources):
        if self.server_config.blob_compression:
            try:
                r = pickle.loads(zlib.decompress(str(resources)))
            except zlib.error:
                # There is the possibility that the user enabled blob
                # compression after some number of runs.  We still want to
                # decompress these runs correctly.
                r = pickle.loads(str(resources))
        else:
            r = pickle.loads(str(resources))
        return r

    def get_runs_rs(self, **kwargs):
        """ returns rows from run_activity table in services database
        
        run_ids - run_id to get info for
        status - only return rows with status = [status]        
        """

        run_activity = self.services_db.get_table('run_activity')
        query = select()
        if run_ids is not None:
            query = query.where(run_activity.c.run_id.in_(run_ids))

        if status is not None:
            query = query.where(run_activity.c.status == status)

        rs = self.services_db.execute(query)
        if resources:
            for row in rs:
                row_resources = self._unpickle(rs.resources)
                if isinstance(row_resources, XMLConfiguration) and 'scenario_name' in rs.c:
                    row.resources = row_resources.get_run_configuration(row.scenario_name)
                else:
                    row.resources = row_resources
        return rs

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
                    config = self._unpickle(run_resources)
                    results.append((run_id, run_name, run_description, processor_name,config))
                except:
                    if not soft_fail: raise

        else:
            results = self.services_db.execute(query).fetchall()

        return results

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

    def add_row_to_history(self, run_id, resources, status, run_name=None, scenario_name=''):
        """update the run history table to indicate changes to the state of this run history trail."""

        self.update_environment_variables(run_resources = resources)
        resources['run_id'] = run_id
        if self.server_config.blob_compression:
            pickled_resources = zlib.compress(pickle.dumps(resources), 9)
        else:
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
             'project_name': resources.get('project_name', None),
             'scenario_name': scenario_name
             }

        run_activity_table = self.services_db.get_table('run_activity')
        if (not 'project_name' in run_activity_table.c):
            del values['project_name']
        if (not 'scenario_name' in run_activity_table.c) or not scenario_name:
            del values['scenario_name']

        if self.has_run(run_id=run_id):
            qry = run_activity_table.update(values = values,
                                            whereclause = run_activity_table.c.run_id == run_id)
        else:
            qry = run_activity_table.insert(values = values)

        self.services_db.execute(qry)

    def import_run_from_cache(self, cache_directory, run_info={}):
        baseyear = run_info.get('baseyear', -1)
        years = self.get_years_run(cache_directory, baseyear=baseyear)
                
        if years == []:
            msg = 'Cannot import run from %s: it contains no data for simulation years' % cache_directory
            logger.log_warning(msg)
            return (False, msg)
        else:
            run_id = run_manager._get_new_run_id()
            run_name = run_info.get('run_name', 
                                    os.path.basename(cache_directory))

            start_year, end_year = min(years), max(years)
            project_name = os.environ.get('OPUSPROJECTNAME', 
                                                      None)
            resources = {'cache_directory': cache_directory,
                         'description': 'run imported from cache',
                         'years': (start_year, end_year),
                         'project_name': project_name
                         }
            resources.update(run_info)

            self.add_row_to_history(run_id=run_id, 
                                    run_name=run_name, 
                                    resources=resources, 
                                    status='done',)
            return (True, '')

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
        # TODO: refactor this into a call of self.get_runs() and remove get_run_info
        for run_id, _, _, processor_name, resources in self.get_run_info(resources = True):
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

        if self.server_config.blob_compression:
            pickled_resources = zlib.compress(pickle.dumps(resources), 9)
        else:
            pickled_resources = pickle.dumps(resources)

        values = {
                'resources':pickled_resources,
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
    if 'cache_directory' in config and config['cache_directory'] is not None:
        if not os.path.exists(config['cache_directory']):
            insert_auto_generated_cache_directory = False
        elif 'overwrite_cache_directory_if_exists' in config and config['overwrite_cache_directory_if_exists'] is True:
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
        self.assertEqual(os.path.dirname(resulting_cache_directory), base_directory)
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

    def test_get_runs(self):
        from numpy.random import randint
        run_manager = RunManager(self.config)
        run_ids = list(range(1, 11))
        run_names = ['run ' + str(id) for id in run_ids]
        resources = {'cache_directory':None}
        status = ['done', 'failed'] * 5
        for idx, run_id in enumerate(run_ids):
            run_manager.add_row_to_history(run_id = run_id,
                                           resources = resources,
                                           status = status[idx],
                                           run_name = run_names[idx])
        results = run_manager.get_runs(return_columns = ['run_name'], run_id=5)
        expected = [('run 5',)]
        self.assertEqual(results, expected)
        results = run_manager.get_runs(return_columns = ['run_id'], status='done')
        expected = [(1,),(3,), (5,), (7,), (9,)]
        self.assertEqual(results, expected)
        
        results = run_manager.get_runs(return_columns = ['run_name'], return_rs=True, run_id=5)
        expected = 'run 5'
        self.assertEqual(results.fetchone()['run_name'], expected)
        results = run_manager.get_runs(return_columns = ['run_id'], return_rs=True, status='done')
        results = [rs['run_id'] for rs in results]
        expected = [1,3,5,7,9]
        self.assertEqual(results, expected)
        
if __name__ == "__main__":
    opus_unittest.main()
