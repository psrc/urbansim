# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE


from opus_core.logger import logger

from urbansim.estimation.estimation_runner import EstimationRunner as UrbansimEstimationRunner
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

class EstimationRunner(object):

    def run_estimation(self, estimation_config, model_name, save_estimation_results=True):
        config = Baseline()
        config.merge(estimation_config)
        config['config_changes_for_estimation'] = ConfigChangesForEstimation()
        logger.start_block('Estimating %s' % model_name)
        try:
            estimator = UrbansimEstimationRunner(
                models[model_name][0], 
                specification_module=models[model_name][1], model_group=models[model_name][2],
                configuration=config,
                save_estimation_results=save_estimation_results
                )
            estimator.estimate()
            
        finally:
            logger.end_block()
        
if __name__ == '__main__':
    #model_name = 'lpm'
    #model_name = 'hlcm'
    #model_name = 'elcm-industrial'
    #model_name = 'elcm-commercial'
    ###model_name = 'elcm-home_based'
    #model_name = 'dplcm-industrial'
    #model_name = 'dplcm-commercial'
    model_name = 'dplcm-residential'
    #model_name = 'rlsm'

    from washtenaw.estimation.my_estimation_config import my_configuration
    
    EstimationRunner().run_estimation(my_configuration, model_name)