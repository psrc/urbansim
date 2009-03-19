# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.estimation.estimation_runner import EstimationRunner
from pag_parcel.configs.baseline import Baseline
from urbansim_parcel.configs.config_changes_for_estimation import ConfigChangesForEstimation
from pag_parcel.estimation.my_estimation_config import my_configuration

models = {
          'repm': ['real_estate_price_model', 'pag_parcel.estimation.repm_specification', None],
          }

if __name__ == '__main__':
    try: import wingdbstub
    except: pass

    model = 'repm'

    config = Baseline()
    if 'models_in_year' in config.keys():
        del config['models_in_year']    
    config.merge(my_configuration)
    config['config_changes_for_estimation'] = ConfigChangesForEstimation()
    er = EstimationRunner(models[model][0], specification_module=models[model][1], model_group=models[model][2],
                           configuration=config, save_estimation_results=False)
    er.estimate()
 
    from my_estimation_config import my_configuration
    er = EstimationRunner()
    er.run_estimation(my_configuration, model, diagnose=False)
    