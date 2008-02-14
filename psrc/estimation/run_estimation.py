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

from urbansim.estimation.estimator import Estimator
from urbansim.estimation.estimator import update_controller_by_specification_from_module
from urbansim.estimation.estimator import plot_utility_diagnose
from urbansim.estimation.estimator import plot_correlation_diagnose

class EstimationRunner(object):
    def run_estimation(self, estimation_config, model, save_estimation_results=True, diagnose=False):
        self.model = model
        self.spec_file = "estimation_%s_variables" % model[0]
        ### TODO: Re-write this
        type = None
        add_member_prefix = False
        if len(model) > 2:
            type = model[2]
            if len(model) > 3:
                add_member_prefix = model[3]
        if type is None:#HBCM, AOCM, HLCM, LPM, RLSM
            exec("from urbansim.configs.%s_estimation_config import run_configuration" % model[0].lower())
            run_configuration = update_controller_by_specification_from_module(
                                run_configuration, model[1],
                                "psrc.estimation.%s" % self.spec_file)
        elif len(model)==4:#ELCM
            exec("from psrc.config.%s_estimation_config import %s_configuration as config" % (model[0].lower(),
                  model[0].lower()))
            run_configuration = config(type, add_member_prefix).get_configuration()
        else: #DPLCM, RWZCM
            exec("from psrc.config.%s_estimation_config import %s_configuration as config" % (model[0].lower(),
                  model[0].lower()))
            run_configuration = config(type).get_configuration()

        if diagnose and model[0] not in ('LPM', 'RLSM'):
            model_name = model[1]
            if type is not None:
                model_name = "%s_%s" % (type, model_name)
            run_configuration["models_configuration"][model_name]["controller"]["estimate"]["arguments"]["procedure"]=\
                "'opus_core.bhhh_mnl_estimation_with_diagnose'"
                
        run_configuration.merge(estimation_config)
        self.estimator = Estimator(run_configuration, save_estimation_results=save_estimation_results)
        self.estimator.estimate()

    def reestimate(self, submodels=None):
        if len(self.model) > 2:
            self.estimator.reestimate(self.spec_file, type=self.model[2], submodels=submodels)
        else:
            self.estimator.reestimate(self.spec_file, submodels=submodels)
    
    def plot_utility(self, submodel=-2):
        plot_utility_diagnose('util_submodel_%s' % submodel)
        
    def plot_correlation(self, submodel=-2):
        plot_correlation_diagnose('correlation_submodel_%s' % submodel)

if __name__ == '__main__':
    #model = ("HBCM", "home_based_choice_model")
    #model = ("AOCM", "auto_ownership_choice_model")
    #model = ("HLCM", "household_location_choice_model")
    #model = ("WHLCM", "worker_specific_household_location_choice_model") #HLCM with worker specific accessibility variables
    #model = ("ELCM", "employment_location_choice_model", "industrial", False) # uses general ELCM and therefore type will not
                                                                                                  # be added to the model name
                                                                                                  
    #model = ("ELCM", "employment_location_choice_model", "commercial", False)
    #model = ("ELCM", "employment_location_choice_model", "home_based", False)
    
    #model = ("RWZCM", "workplace_choice_model_for_resident", "dummy")
    
    #model = ("LPM", "land_price_model")
    #model = ("RLSM", "residential_land_share_model")
    #model = ("DPLCM", "development_project_location_choice_model", "industrial")
    #model = ("DPLCM", "development_project_location_choice_model", "commercial")
    model = ("DPLCM", "development_project_location_choice_model", "residential")

    from my_estimation_config import my_configuration
    er = EstimationRunner()
    er.run_estimation(my_configuration, model, diagnose=True)