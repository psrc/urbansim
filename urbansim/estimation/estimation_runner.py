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


from opus_core.configuration import Configuration
from urbansim.estimation.estimator import Estimator
from urbansim.estimation.estimator import plot_utility_diagnose
from urbansim.estimation.estimator import update_controller_by_specification_from_module

class EstimationRunner(Estimator):
     
    def __init__(self, model, specification_module=None, model_group=None,
                  configuration={}, save_estimation_results=False):
        """
        If 'specification_module' is given, it contains the specification defined as a dictionary in a module.
        If it is None, the specification is taken from the cache.
        'configuration' is an Opus configuration. It can contain an entry 'config_changes_for_estimation' which is a dictionary
        where keys are model names and values are controller changes for that model.
        If save_estimation_results is True, the estimation results are saved in the oputput configuration 
        (if given in 'configuration') and in the cache.
        """
        self.specification_module = specification_module
        self.model_group = model_group
        
        config = Configuration(configuration)
        config_changes = config.get('config_changes_for_estimation', {})
        
        if model_group is None:
            if model in config_changes.keys():
                config.merge(config_changes[model])
            if specification_module is not None:
                config = update_controller_by_specification_from_module(
                                config, model, specification_module)
        else:
            if model in config_changes.keys():
                if model_group in config_changes[model]:
                    config.merge(config_changes[model][model_group])
                else:
                    config.merge(config_changes[model])       
            if specification_module is not None:
                if '%s_%s' % (model_group, model) in config["models_configuration"].keys():
                    model_name_in_configuration = '%s_%s' % (model_group, model)
                else:
                    model_name_in_configuration = model
                config = update_controller_by_specification_from_module(config, model_name_in_configuration, specification_module)
                config["models_configuration"][model_name_in_configuration]["controller"]["prepare_for_estimate"]["arguments"]["specification_dict"] = "spec['%s']" % model_group
            config['model_name'] = '%s_%s' % (model_group, model)
            
        Estimator.__init__(self, config, save_estimation_results=save_estimation_results)

    def reestimate(self, submodels=None):
        """Launch a re-estimation without recomputing all variables. 'submodels' is a list or single number of submodels to re-estimate.
        If it is None, all submodels are re-estimated.
        """
        Estimator.reestimate(self, self.specification_module, type=self.model_group, submodels=submodels)
        
    def plot_utility(self, submodel=-2):
        """In order to use this method, the estimation must be run with a procedure that creates a file 'util_submodel_x' 
            (e.g. with bhhh_mnl_estimation_with_diagnose)
        """
        plot_utility_diagnose('util_submodel_%s' % submodel)

