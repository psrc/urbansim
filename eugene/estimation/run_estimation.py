# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

##!!!!!!!!!!!
# Calling this script is equivalent to do the following from the command line (e.g. for industrial ELCM):
#
# python urbansim/tools/start_estimation.py -c eugene.configs.baseline_estimation --model=employment_location_choice_model --group=industrial -s eugene.estimation.ELCM_specification --save-results
#
# If you use the command above, make you private changes in eugene.configs.baseline_estimation.
#!!!!!!!!!!!!


from eugene.estimation.my_estimation_config import my_configuration
from urbansim.estimation.estimation_runner import EstimationRunner
from eugene.configs.baseline import Baseline
from urbansim.configs.config_changes_for_estimation import ConfigChangesForEstimation

models = {
          'hlcm': ['household_location_choice_model', 'eugene.estimation.HLCM_specification', None],
          'elcm-industrial': ['employment_location_choice_model', 'eugene.estimation.ELCM_specification', 'industrial'],
          'elcm-commercial': ['employment_location_choice_model', 'eugene.estimation.ELCM_specification', 'commercial'],
          'elcm-home_based': ['employment_location_choice_model', 'eugene.estimation.ELCM_specification', 'home_based'],
          'lpm': ['land_price_model', 'eugene.estimation.LPM_specification', None],
          'dplcm-industrial': ['development_project_location_choice_model', 'eugene.estimation.DPLCM_specification', 'industrial'],
          'dplcm-commercial': ['development_project_location_choice_model', 'eugene.estimation.DPLCM_specification', 'commercial'],
          'dplcm-residential': ['development_project_location_choice_model', 'eugene.estimation.DPLCM_specification', 'residential'],
          'rlsm': ['residential_land_share_model', 'eugene.estimation.RLSM_specification', None],
          }

#model = 'hlcm'
#model = 'elcm-industrial'
#model = 'elcm-commercial'
#model = 'elcm-home_based'
model = 'dplcm-industrial'
#model = 'dplcm-commercial'
#model ='dplcm-residential'
#model = 'lpm'
#model = 'rlsm'

config = Baseline()
config.merge(my_configuration)
config['config_changes_for_estimation'] = ConfigChangesForEstimation()
estimator = EstimationRunner(models[model][0], specification_module=models[model][1], model_group=models[model][2],
                           configuration=config,
                           save_estimation_results=True)
estimator.estimate()
#estimator.reestimate()
#estimator.reestimate(submodels=[])
