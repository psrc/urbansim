# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from washtenaw.estimation.my_estimation_config import my_configuration
from urbansim.estimation.estimator import Estimator
from urbansim.estimation.estimator import update_controller_by_specification_from_module


model_name = 'auto_ownership_choice_model'
from washtenaw.aocm.aocm_estimation_config import run_configuration

run_configuration.merge(my_configuration)
estimator = Estimator(run_configuration, save_estimation_results=False)
estimator.estimate()
#estimator.reestimate("aocm_specification")   