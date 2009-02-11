#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

##!!!!!!!!!!!
# Calling this script is equivalent to do the following from the command line (e.g. for non-home-based ELCM):
#
# python urbansim/tools/start_estimation.py -c psrc_parcel.configs.baseline_estimation --model=employment_location_choice_model --group=non_home_based -s psrc_parcel.estimation.elcm_specification
#
# Make you private changes in psrc_parcel.configs.baseline_estimation.
#!!!!!!!!!!!!


from urbansim.estimation.estimation_runner import EstimationRunner
from psrc_parcel.configs.baseline import Baseline
from urbansim_parcel.configs.config_changes_for_estimation import ConfigChangesForEstimation
from psrc_parcel.estimation.my_estimation_config import my_configuration

models = {
          'hlcm': ['household_location_choice_model', 'psrc_parcel.estimation.hlcm_specification', None],
          'elcm-non-home-based': ['employment_location_choice_model', 'psrc_parcel.estimation.elcm_specification', 'non_home_based'],
          'elcm-home_based': ['employment_location_choice_model', 'psrc_parcel.estimation.elcm_specification', 'home_based'],
          'repm': ['real_estate_price_model', 'psrc_parcel.estimation.repm_specification', None],
          'wcm' : ['workplace_choice_model_for_resident', 'wcm_specification', None],
          'wahcm': ['work_at_home_choice_model', 'wahcm_specification', None],
          'dppcm': ['development_project_proposal_choice_model', 'dppcm_specification', None]
          }

if __name__ == '__main__':
    try: import wingdbstub
    except: pass
    model = 'hlcm'
    #model = 'elcm-non-home-based'
    #model = 'elcm-home_based'
    #model = 'repm'
    #model = 'wcm'
    #model = 'wahcm'
    #model = 'dppcm'

    config = Baseline()
    if 'models_in_year' in config.keys():
        del config['models_in_year']    
    config.merge(my_configuration)
    config['config_changes_for_estimation'] = ConfigChangesForEstimation()
    ## set base_year and years to 2006 for HLCM for the psrc_parcel project
    config['config_changes_for_estimation']['household_location_choice_model'].merge({'base_year': 2006, 'years':(2006, 2006)})
    
    er = EstimationRunner(models[model][0], specification_module=models[model][1], model_group=models[model][2],
                           configuration=config, save_estimation_results=False)
    er.estimate()
    #er.predict()
    #er.create_prediction_success_table(geography_id_expression='choice.is_chosen')
