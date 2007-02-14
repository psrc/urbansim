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
# 

from washtenaw.estimation.my_estimation_config import my_configuration
from urbansim.estimation.estimator import Estimator
from urbansim.estimation.estimator import update_controller_by_specification_from_module


model_name = 'auto_ownership_choice_model'
from washtenaw.aocm.aocm_estimation_config import run_configuration

run_configuration.merge(my_configuration)
estimator = Estimator(run_configuration, save_estimation_results=False)
estimator.estimate()
#estimator.reestimate("aocm_specification")   