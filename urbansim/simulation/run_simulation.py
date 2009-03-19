# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os

from shutil import rmtree

from opus_core.logger import logger
from opus_core.resources import Resources
from opus_core.fork_process import ForkProcess
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.store.utils.cache_flt_data import CacheFltData
from opus_core.session_configuration import SessionConfiguration

from urbansim.model_coordinators.model_system import ModelSystem

class RunSimulation(object):
    def prepare_for_simulation(self, config, cache_directory=None):
        self.config = Resources(config)
        base_cache_dir = self.config['creating_baseyear_cache_configuration'].cache_directory_root
        
        self.simulation_state = SimulationState(new_instance=True, base_cache_dir=base_cache_dir)

        ### TODO: Get rid of this! There is no good reason to be changing the 
        ###       Configuration.
        if self.config['cache_directory'] is None:
            self.config['cache_directory'] = self.simulation_state.get_cache_directory()

        SessionConfiguration(new_instance=True,
                             package_order=self.config['dataset_pool_configuration'].package_order,
                             in_storage=AttributeCache())
        
        if config['creating_baseyear_cache_configuration'].cache_from_database:
            ForkProcess().fork_new_process(self.config['creating_baseyear_cache_configuration'].cache_scenario_database, self.config)
        else:
            CacheFltData().run(self.config)

    def run_simulation(self, simulation_instance=None):
        if simulation_instance is None:
            simulation_instance = ModelSystem()
        simulation_instance.run(self.config)
        #simulation_instance.run_multiprocess(self.config, is_run_subset=True)
        logger.log_status("Data cache in %s" % self.simulation_state.get_cache_directory())
        
    def cleanup(self, remove_cache=True):
        """Remove all outputs of this simulation."""    
        self.simulation_state.remove_singleton(delete_cache=remove_cache)
        SessionConfiguration().remove_singleton()
        if remove_cache:
            cache_dir = self.config['cache_directory']
            if os.path.exists(cache_dir):
                rmtree(cache_dir)

    def prepare_and_run(self, run_configuration, simulation_instance=None, remove_cache=True):
        self.prepare_for_simulation(run_configuration)
        self.run_simulation(simulation_instance)
        self.cleanup(remove_cache)