# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from shutil import rmtree

from opus_core.logger import logger
from opus_core.resources import Resources
from opus_core.singleton import Singleton
from opus_core.fork_process import ForkProcess
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.database_management.database_server import DatabaseServer
from opus_core.session_configuration import SessionConfiguration

from opus_core.model_coordinators.model_system import ModelSystem


class RunSimulationFromMysql:
    def prepare_for_simulation(self, run_configuration, cache_directory=None):
        self.config = Resources(run_configuration)
        self.simulation_state = SimulationState(new_instance=True, base_cache_dir=cache_directory)

        ### TODO: Get rid of this! There is no good reason to be changing the
        ###       Configuration.
        if self.config['cache_directory'] is None:
            self.config['cache_directory'] = self.simulation_state.get_cache_directory()

        SessionConfiguration(new_instance=True,
                             package_order=self.config['dataset_pool_configuration'].package_order,
                             in_storage=AttributeCache())
        
        ForkProcess().fork_new_process(self.config['creating_baseyear_cache_configuration'].cache_scenario_database, self.config)
        
        # Create output database (normally done by run manager)
        if 'estimation_database_configuration' in self.config:
            db_server = DatabaseServer(self.config['estimation_database_configuration'])
            if not db_server.has_database(self.config['estimation_database_configuration'].database_name):
                db_server.create_database(self.config['estimation_database_configuration'].database_name)
                   
    def run_simulation(self, simulation_instance=None):
        logger.start_block('Simulation on database %s' 
            % self.config['scenario_database_configuration'].database_name)
        try:
            if simulation_instance is None:
                simulation_instance = ModelSystem()
            simulation_instance.run(self.config)
            #simulation_instance.run_multiprocess(self.config, is_run_subset=True)
        finally:
            logger.end_block()
        logger.log_status("Data cache in %s" % self.simulation_state.get_cache_directory())
        
    def cleanup(self, remove_cache, remove_output_database):
        """Remove all outputs of this simulation."""
        self.simulation_state.remove_singleton(delete_cache=remove_cache)
        # Remove SessionConfiguration singleton, if it exists
        Singleton().remove_singleton_for_class(SessionConfiguration)
        
        cache_dir = self.config['cache_directory']
        if os.path.exists(cache_dir):
            rmtree(cache_dir)
        if remove_output_database and ('estimation_database_configuration' in self.config):
            db_server = DatabaseServer(self.config['estimation_database_configuration'])
            db_server.drop_database(self.config['estimation_database_configuration'].database_name)

    def prepare_and_run(self, run_configuration, simulation_instance=None, remove_cache=True):
        self.prepare_for_simulation(run_configuration)
        self.run_simulation(simulation_instance)
        self.cleanup(remove_cache)
        