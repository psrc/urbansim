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
    