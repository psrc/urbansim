# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from sanfrancisco.configs.baseline import Baseline
#from config_for_multiple_runs import ConfigForMultipleRuns
from urbansim.simulation.run_simulation import RunSimulation
from urbansim.model_coordinators.model_system import ModelSystem

simulation = RunSimulation()
run_configuration = Baseline()
#run_configuration = ConfigForMultipleRuns()
simulation.prepare_and_run(run_configuration, 
                            simulation_instance=ModelSystem(),
                            remove_cache=run_configuration.get('remove_cache', False))