# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.simulation.run_simulation import RunSimulation
from urbansim.model_coordinators.model_system import ModelSystem
from randstad.run_config.randstad_baseline import run_configuration as my_configuration
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration

config = AbstractUrbansimConfiguration()

simulation = RunSimulation()
run_configuration = config.copy()
run_configuration.merge(my_configuration)
simulation.prepare_and_run(run_configuration, 
                            simulation_instance=ModelSystem(),
                            remove_cache=True)