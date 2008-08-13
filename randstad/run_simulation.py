#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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