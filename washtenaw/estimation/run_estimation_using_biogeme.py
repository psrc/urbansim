# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from washtenaw.estimation.my_estimation_config_with_biogeme import my_configuration
from urbansim.estimation.estimation_runner import EstimationRunner
from washtenaw.configs.baseline import Baseline
from urbansim.configs.config_changes_for_estimation import ConfigChangesForEstimation

models = {
          'hlcm': ['household_location_choice_model', 'washtenaw.estimation.HLCM_specification', None],
          'elcm-industrial': ['employment_location_choice_model', 'washtenaw.estimation.ELCM_specification', 'industrial'],
          'elcm-commercial': ['employment_location_choice_model', 'washtenaw.estimation.ELCM_specification', 'commercial'],
          'elcm-home_based': ['employment_location_choice_model', 'washtenaw.estimation.ELCM_specification', 'home_based'],
          'lpm': ['land_price_model', 'washtenaw.estimation.LPM_specification', None],
          'dplcm-industrial': ['development_project_location_choice_model', 'washtenaw.estimation.DPLCM_specification', 'industrial'],
          'dplcm-commercial': ['development_project_location_choice_model', 'washtenaw.estimation.DPLCM_specification', 'commercial'],
          'dplcm-residential': ['development_project_location_choice_model', 'washtenaw.estimation.DPLCM_specification', 'residential'],
          'rlsm': ['residential_land_share_model', 'washtenaw.estimation.RLSM_specification', None],
          }

model = 'hlcm'
#model = 'elcm-industrial'
#model = 'elcm-commercial'
#model = 'elcm-homebased'
#model = dplcm-industrial'
#model = 'dplcm-commercial'
#model ='dplcm-residential'
#model = 'lpm'
#model = 'rlsm'

config = Baseline()
config.merge(my_configuration)
config['config_changes_for_estimation'] = ConfigChangesForEstimation()
estimator = EstimationRunner(models[model][0], specification_module=models[model][1], model_group=models[model][2],
                           configuration=config,
                           save_estimation_results=False)
estimator.estimate()
#estimator.reestimate()
