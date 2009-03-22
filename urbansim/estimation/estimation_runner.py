# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


from opus_core.configuration import Configuration
from urbansim.estimation.estimator import Estimator
from urbansim.estimation.estimator import plot_utility_diagnose
from urbansim.estimation.estimator import update_controller_by_specification_from_module, update_controller_by_specification_from_dict

class EstimationRunner(Estimator):

    def __init__(self, model, specification_module=None,
                 xml_configuration=None, model_group=None, configuration={},
                 save_estimation_results=False):
        """
        If 'specification_module' is given, it contains the specification defined as a dictionary in a module.
        Alternatively, the specification can be passed in an xml format in the 'xml_configuration' argument
        (which should be an instance of XMLConfiguration).
        If both of those arguments are None, the specification is taken from the cache.
        'configuration' is an Opus configuration.
        It can contain an entry 'config_changes_for_estimation' which is a dictionary
        where keys are model names and values are controller changes for that model.
        If 'configuration' is None, it is taken from 'xml_configuration'.
        If xml_configuration is used, and if it has a non-empty expression library, the dictionary representing
        the expression library is added to the configuration under the key 'expression_library'.
        If save_estimation_results is True, the estimation results are saved in the output configuration
        (if given in 'configuration') and in the cache.
        """
        self.specification_module = specification_module
        self.xml_configuration = xml_configuration
        self.model_group = model_group
        self.estimated_model = model

        if configuration is None:
            if self.xml_configuration is None:
                raise StandardError, "Either dictionary based or XML based configuration must be given."
            config = self.xml_configuration.get_estimation_configuration(model, model_group)
        else:
            config = Configuration(configuration)
        config_changes = config.get('config_changes_for_estimation', {})

        specification_dict=None
        if self.xml_configuration is not None:
            specification_dict = self.xml_configuration.get_estimation_specification(model, model_group)

        if model_group is None:
            if model in config_changes.keys():
                config.merge(config_changes[model])
            else:
                config['models'] = [{model: ["estimate"]}]
            if specification_module is not None:
                config = update_controller_by_specification_from_module(
                                config, model, specification_module)
            elif specification_dict is not None:
                config = update_controller_by_specification_from_dict(config, model, specification_dict)
        else:
            if model in config_changes.keys():
                if model_group in config_changes[model]:
                    config.merge(config_changes[model][model_group])
                else:
                    config.merge(config_changes[model])
            else:
                config['models'] = [{model: {"group_members": [{model_group: ["estimate"]}]}}]
            if (specification_module is not None) or (specification_dict is not None):
                if '%s_%s' % (model_group, model) in config["models_configuration"].keys():
                    model_name_in_configuration = '%s_%s' % (model_group, model)
                else:
                    model_name_in_configuration = model
                if specification_module is not None:
                    config = update_controller_by_specification_from_module(config, model_name_in_configuration, specification_module)
                    config["models_configuration"][model_name_in_configuration]["controller"]["prepare_for_estimate"]["arguments"]["specification_dict"] = "spec['%s']" % model_group
                else:
                    config = update_controller_by_specification_from_dict(config, model, specification_dict[model_group])

            config['model'] = '%s_%s' % (model_group, model)

        Estimator.__init__(self, config, save_estimation_results=save_estimation_results)

    def reestimate(self, submodels=None, reload_xml_file=True):
        """Launch a re-estimation without recomputing all variables. 'submodels' is a list or single number of submodels to re-estimate.
        If it is None, all submodels are re-estimated.  If self.xml_configuration is not None and reload_xml_file is True, re-read
        the contents of the xml configuration file in case it has changed.  This will usually be what you want to do when
        using reestimate from the command line -- but not from the GUI (since with the GUI, the XMLConfiguration might have been
        edited but not yet saved back to the file).
        """
        specification_dict=None
        if self.xml_configuration is not None:
            if reload_xml_file:
                self.xml_configuration.initialize_from_xml_file()
            specification_dict = self.xml_configuration.get_estimation_specification(self.estimated_model)
        Estimator.reestimate(self, self.specification_module, specification_dict=specification_dict, type=self.model_group, submodels=submodels)

    def plot_utility(self, submodel=-2):
        """In order to use this method, the estimation must be run with a procedure that creates a file 'util_submodel_x'
            (e.g. with bhhh_mnl_estimation_with_diagnose)
        """
        plot_utility_diagnose('util_submodel_%s' % submodel)

