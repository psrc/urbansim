#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

from psrc_parcel.configs.baseline import Baseline
#from config_for_multiple_runs import ConfigForMultipleRuns
from urbansim.simulation.run_simulation import RunSimulation
from urbansim.model_coordinators.model_system import ModelSystem

simulation = RunSimulation()
run_configuration = Baseline()
#run_configuration = ConfigForMultipleRuns()
simulation.prepare_and_run(run_configuration, 
                            simulation_instance=ModelSystem(),
                            remove_cache=run_configuration.get('remove_cache', False))