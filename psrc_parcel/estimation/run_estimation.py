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

from urbansim.estimation.estimator import Estimator
from urbansim.estimation.estimator import update_controller_by_specification_from_module
from urbansim.estimation.estimator import plot_utility_diagnose
from urbansim.estimation.estimator import plot_correlation_diagnose
from psrc_parcel.configs.baseline import Baseline

class EstimationRunner(object):

    def run_estimation(self, estimation_config, model, save_estimation_results=True, diagnose=False):
        self.model = model
        self.spec_file = "%s_specification" % model[0].lower()
        ### TODO: Re-write this
        type = None
        add_member_prefix = False
        baseline_config = Baseline()
        if len(model) > 2:
            type = model[2]
            if len(model) > 3:
                add_member_prefix = model[3]
        if type is None:
            exec("from urbansim_parcel.estimation.%s_estimation_config import run_configuration" % model[0].lower())
            run_configuration["models_configuration"][self.model[1]]["controller"].replace(baseline_config["models_configuration"][self.model[1]]["controller"])
            run_configuration = update_controller_by_specification_from_module(
                                run_configuration, model[1],
                                "psrc_parcel.estimation.%s" % self.spec_file)
        else:
            exec("from urbansim_parcel.estimation.%s_estimation_config import %s_configuration as config" % (model[0].lower(),
                  model[0].lower()))
            conf = config(type, add_member_prefix)
            run_configuration = conf.get_configuration()
            run_configuration["models_configuration"][conf.model_name]["controller"].replace(
                                                                 baseline_config["models_configuration"][conf.model_name]["controller"])
            run_configuration = conf.get_updated_configuration_from_module(
                                     run_configuration, "psrc_parcel.estimation.%s" % self.spec_file)

        if diagnose and self.model[0] != 'REPM':  #only works for LCM and derivatives
            model_name = model[1]
            #if type is not None:
                #model_name = "%s_%s" % (type, model_name)
            run_configuration["models_configuration"][model_name]["controller"]["estimate"]["arguments"]["procedure"]=\
                "'opus_core.bhhh_mnl_estimation_with_diagnose'"
                
        run_configuration.replace(estimation_config)
        self.estimator = Estimator(run_configuration, save_estimation_results=save_estimation_results)
        self.estimator.estimate()

    def reestimate(self, submodels=None):
        if len(self.model) > 2:
            self.estimator.reestimate(self.spec_file, type=self.model[2], submodels=submodels)
        else:
            self.estimator.reestimate(self.spec_file, submodels=submodels)
    def save_results(self):
        self.estimator.save_results()
        
    def plot_utility(self, submodel=-2):
        plot_utility_diagnose('util_submodel_%s' % submodel)
        
    def plot_correlation(self, submodel=-2):
        plot_correlation_diagnose('correlation_submodel_%s' % submodel)

if __name__ == '__main__':
    model = ("REPM", "real_estate_price_model")
#    model = ("HLCM", "household_location_choice_model")
#    model = ("ELCM", "employment_location_choice_model", "home_based", True)
#    model = ("ELCM", "employment_location_choice_model", "non_home_based", False)


    from my_estimation_config import my_configuration
    er = EstimationRunner()
    er.run_estimation(my_configuration, model, save_estimation_results=False, diagnose=False)
    
