# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

##!!!!!!!!!!!
# Calling this script is equivalent to do the following from the command line (e.g. for industrial ELCM):
#
# python urbansim/tools/start_estimation.py -c psrc.configs.baseline_estimation --model=employment_location_choice_model --group=industrial -s psrc.estimation.psrc.estimation_ELCM_variables --save-results
#
# Make you private changes in psrc.configs.baseline_estimation.
#!!!!!!!!!!!!

from psrc.estimation.my_estimation_config import my_configuration
from urbansim.estimation.estimation_runner import EstimationRunner
from psrc.configs.baseline import Baseline
from urbansim.configs.config_changes_for_estimation import ConfigChangesForEstimation

models = {
          'hlcm': ['household_location_choice_model', 'psrc.estimation.psrc.estimation_HLCM_variables', None],
          'elcm-industrial': ['employment_location_choice_model', 'psrc.estimation.psrc.estimation_ELCM_variables', 'industrial'],
          'elcm-commercial': ['employment_location_choice_model', 'psrc.estimation.psrc.estimation_ELCM_variables', 'commercial'],
          'elcm-home_based': ['employment_location_choice_model', 'psrc.estimation.psrc.estimation_ELCM_variables', 'home_based'],
          'lpm': ['land_price_model', 'psrc.estimation.psrc.estimation_LPM_variables', None],
          'dplcm-industrial': ['development_project_location_choice_model', 'psrc.estimation.psrc.estimation_DPLCM_variables', 'industrial'],
          'dplcm-commercial': ['development_project_location_choice_model', 'psrc.estimation.psrc.estimation_DPLCM_variables', 'commercial'],
          'dplcm-residential': ['development_project_location_choice_model', 'psrc.estimation.psrc.estimation_DPLCM_variables', 'residential'],
          'rlsm': ['residential_land_share_model', 'psrc.estimation.psrc.estimation_RLSM_variables', None],
          }

if __name__ == '__main__':
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