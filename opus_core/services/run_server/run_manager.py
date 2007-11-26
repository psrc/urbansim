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
from sqlalchemy.sql import select, and_

class RunManager(object):
    """An abstraction representing a simulation manager that automatically logs
    runs (and their status) to a database (run_activity),
    creates resources for runs, and can run simulations.
    """
    #TODO: some preconditions should be checked!
    def __init__(self, run_activity=None):
        self.run_activity = run_activity

    def set_run_activity(self, run_activity):
        self.run_activity = run_activity

    def get_resources_for_run_id_from_history(self, run_id,
                                          services_host_name='localhost',
                                          services_database_name='services',
                                          services_user_name=None,
                                          services_password=None):
        """Returns the resources for this run_id, as stored in the run_activity table.
        """
#        import pdb; pdb.set_trace()
        db_config = DatabaseServerConfiguration(
            host_name=services_host_name, 
            user_name=services_user_name, 
            password=services_password                                   
        )
        db_server = DatabaseServer(db_config)
        db = db_server.get_database(services_database_name)
                
        run_activity = db.get_table('run_activity')
        query = select(
            columns = [run_activity.c.resources],
            whereclause = and_(
                            run_activity.c.status=='started',
                            run_activity.c.run_id==int(run_id)))
        
        run_resources = db.engine.execute(query).fetchone()
        
        if not run_resources:
            raise StandardError("run_id %s doesn't exist host = %s database = %s" % (run_id, services_host_name, services_database_name))

        db.close()
        return Configuration(pickle.loads(run_resources[0]))

    def create_run_resources_from_history(self,
                                          services_host_name='localhost',
                                          services_database_name='services',
                                          services_user_name=os.environ.get('MYSQLUSERNAME', None),
                                          services_password=os.environ.get('MYSQLPASSWORD', None),
                                          run_id=None,
                                          restart_year=None,
                                          end_year=None
                                          ):
        """Re-creates and returns a resources dictionary given a specific entry in run_activity.
        Entirely based on the pickled "resources" field for that entry, which also
        contains a pickled version of the "run request" (a dictionary) associated with that entry."""
        if not run_id:
            raise StandardError("run_id un-specified")

        resources = self.get_resources_for_run_id_from_history(services_host_name=services_host_name,
                                                               services_user_name=services_user_name,
                                                               services_password=services_password,
                                                               services_database_name=services_database_name,
                                                               run_id=run_id)
        if 'cache_variables' not in resources:
            resources['cache_variables'] = False

        if not os.path.exists(resources['cache_directory']):
            raise StandardError("cache directory doesn't exist: '%s'" % resources['cache_directory'])
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
        resources['flt_directory'] = os.path.join(resources['cache_directory'], str(restart_year - 1))
        resources["years"] = (restart_year, end_year)

        return resources

    def run_run(self, run_resources, run_as_multiprocess=True, run_in_background=False):
        """check run hasn't already been marked running
           log it in to run_activity
           run simulation
           mark run as done/failed
           """
        
        if self.run_activity is not None:
            history_id = self.run_activity.get_new_history_id()
            
            #add history_id to cache directory
            head, tail = os.path.split(run_resources['cache_directory'])
            cache_directory = os.path.join(head, 'run_' +str(history_id)+'.'+tail)
            ### TODO: There is no good reason to be changing Configurations!
            run_resources['cache_directory'] = cache_directory

        else:
            ### TODO: There is no good reason to be changing Configurations!
            cache_directory = run_resources['cache_directory']
            
        # Make the cache_directory if it doesn't exist (doesn't include per-year directories).
        if not os.path.exists(cache_directory):
            os.makedirs(cache_directory)

        if self.run_activity is not None:
            self.run_activity.add_row_to_history(history_id, run_resources, "started")

        try:
            # Test pre-conditions
            model_system_class_path = run_resources.get('model_system', None)
            if model_system_class_path is None:
                raise TypeError, ("The configuration must specify model_system, the"
                    " full Opus path to the model system to be used.")
            
            # Create baseyear cache
            if run_resources['creating_baseyear_cache_configuration'].cache_from_mysql:
                ForkProcess().fork_new_process(
                    run_resources['creating_baseyear_cache_configuration'].cache_scenario_database, run_resources)
            else:
                CacheFltData().run(run_resources)
                
            # Create brand-new output database (deletes any prior contents)
            if 'output_configuration' in run_resources:
                db_config = DatabaseServerConfiguration(
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
                model_system.run_in_one_process(run_resources, run_in_background=run_in_background)
            
            if self.run_activity is not None:
                self.run_activity.add_row_to_history(history_id, run_resources, "done")

        except:
            if self.run_activity is not None:
                self.run_activity.add_row_to_history(history_id, run_resources, "failed")
            raise # This re-raises the last exception

    def restart_run(self, history_id, restart_year,
                    services_host_name,
                    services_database_name,
                    skip_urbansim=False,
                    skip_cache_cleanup=False):
        """Restart the specified run."""

        run_resources = self.create_run_resources_from_history(
           services_host_name=services_host_name,
           services_database_name=services_database_name,
           run_id=history_id,
           restart_year=restart_year)
        try:

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
            self.run_activity.add_row_to_history(history_id, run_resources, "restarted in %d" % run_resources['years'][0])

            exec('from %s import ModelSystem' % model_system)

            # add years run
            model_system = ModelSystem()

            if 'base_year' not in run_resources:
                run_resources['base_year'] = run_resources['years'][0] - 1

            base_year = run_resources['base_year']
            
            model_system.run_multiprocess(run_resources)

            self.run_activity.add_row_to_history(history_id, run_resources, "done")

        except:
            self.run_activity.add_row_to_history(history_id, run_resources, "failed")
            raise

    def get_processor_name(self,run_id, services_host_name, services_user_name, services_password, services_database_name = "services"):
        """ returns the name of the server where these run was processed"""

        db_config = DatabaseServerConfiguration(
            host_name=services_host_name, 
            user_name=services_user_name, 
            password=services_password                                   
        )
        db_server = DatabaseServer(db_config)
        db = db_server.get_database(services_database_name)
        
        run_activity = db.get_table('run_activity')
        query = select(
            columns = [run_activity.c.processor_name],
            whereclause = run_activity.c.run_id==run_id)
        
        results = db.engine.execute(query).fetchone()
        db.close()
        db_server.close()

        return results[0]

    def get_name_for_id(self,run_id, services_host_name, services_user_name, services_password, services_database_name = "services"):
        """ returns the name given to this scenario run"""
        db_config = DatabaseServerConfiguration(
            host_name=services_host_name, 
            user_name=services_user_name, 
            password=services_password                                   
        )
        db_server = DatabaseServer(db_config)
        db = db_server.get_database(services_database_name)

        run_activity = db.get_table('run_activity')
        query = select(
            columns = [run_activity.c.run_name],
            whereclause = run_activity.c.run_id==run_id)
        
        results = db.engine.execute(query).fetchone()
        
        db.close()
        db_server.close()

        return results[0]

    def create_baseyear_cache(self, resources):
        if resources['creating_baseyear_cache_configuration'].cache_from_mysql:
            ForkProcess().fork_new_process(
                resources['creating_baseyear_cache_configuration'].cache_scenario_database, resources)
        else:
            CacheFltData().run(resources)
            

class SimulationRunError(Exception):
    """exception to be raised if the simulation fails at runtime"""
    pass
            
def insert_auto_generated_cache_directory_if_needed(config):
    """Auto-generate a cache directory based upon current date-time."""
    cache_directory_root = config['creating_baseyear_cache_configuration'].cache_directory_root
    date_time_str = strftime('%Y_%m_%d_%H_%M', localtime())

    cache_directory = os.path.join(cache_directory_root, date_time_str)

    config['cache_directory'] = cache_directory