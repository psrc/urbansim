# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

##!!!!!!!!!!!
# Calling this script is equivalent to do the following from the command line (e.g. for nonresidential BLDGLCM):
#
# python urbansim/tools/start_estimation.py -c sanfrancisco.configs.baseline_estimation --model=building_location_choice_model --group=nonresidential -s sanfrancisco.estimation.bldglcm_specification --save-results
#
# Make you private changes in sanfrancisco.configs.baseline_estimation.
#!!!!!!!!!!!!

from sanfrancisco.estimation.my_estimation_config import my_configuration
from urbansim.estimation.estimation_runner import EstimationRunner
from sanfrancisco.configs.baseline import Baseline
from sanfrancisco.configs.config_changes_for_estimation import ConfigChangesForEstimation

models = {
          'hlcm': ['household_location_choice_model', 'sanfrancisco.estimation.hlcm_specification', None],
          'blcm': ['business_location_choice_model', 'sanfrancisco.estimation.blcm_specification', None],
          'repm': ['real_estate_price_model', 'sanfrancisco.estimation.repm_specification', None],
          "BLDGLCM-nonres": ["building_location_choice_model", 'sanfrancisco.estimation.bldglcm_specification', "nonresidential"],
          "BLDGLCM-res": ["building_location_choice_model", 'sanfrancisco.estimation.bldglcm_specification', "residential"],
          }

if __name__ == '__main__':
#    model = 'repm'
#    model = 'hlcm'
#    model = 'blcm'
#    model = "BLDGLCM-nonres"
    model = "BLDGLCM-res"

    config = Baseline()
    config.merge(my_configuration)
    config['config_changes_for_estimation'] = ConfigChangesForEstimation()
    er = EstimationRunner(models[model][0], specification_module=models[model][1], model_group=models[model][2],
                           configuration=config, save_estimation_results=True)
    er.estimate()
    
