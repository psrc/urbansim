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

from numpy import absolute, array, where, take, zeros, ones
from opus_core.logger import logger
from opus_core.resources import Resources
from opus_core.coefficients import Coefficients
from opus_core.variables.variable_name import VariableName
from opus_core.simulation_state import SimulationState
from opus_core.misc import load_table_from_text_file, unique_values
from opus_core.store.attribute_cache import AttributeCache
from opus_core.datasets.dataset import Dataset
from opus_core.equation_specification import EquationSpecification
from opus_core.storage_factory import StorageFactory
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
from opus_core.session_configuration import SessionConfiguration
from urbansim.model_coordinators.model_system import ModelSystem

class Estimator(object):
    def __init__(self, config=None, save_estimation_results=False):
        if 'cache_directory' not in config or config['cache_directory'] is None:
            raise KeyError("The cache directory must be specified in the "
                "given configuration, giving the filesystem path to the cache "
                "directory containing the data with which to estimate. Please "
                "check that your configuration contains the 'cache_directory' "
                "entry and that it is not None.")

        self.simulation_state = SimulationState(new_instance=True)
        self.simulation_state.set_cache_directory(config['cache_directory'])

        SessionConfiguration(new_instance=True,
                             package_order=config['dataset_pool_configuration'].package_order,
                             package_order_exceptions=config['dataset_pool_configuration'].package_order_exceptions,
                             in_storage=AttributeCache())
        self.config = Resources(config)
        self.save_estimation_results = save_estimation_results
        self.debuglevel = self.config.get("debuglevel", 4)
        self.model_system = ModelSystem()

        models = self.config.get('models',[])

        self.model_name = None
        if "model_name" in config.keys():
            self.model_name = config["model_name"]
        else:
            for model in models:
                if isinstance(model, dict):
                    model_name = model.keys()[0]
                    if (model[model_name] == "estimate") or (isinstance(model[model_name], list)
                        and ("estimate" in model[model_name])):
                            self.model_name = model_name
                            break

    def estimate(self, out_storage=None):
        self.model_system.run(self.config, write_datasets_to_cache_at_end_of_year=False)
        self.extract_coefficients_and_specification()

        if self.save_estimation_results:
            self.save_results(out_storage=out_storage)

    def reestimate(self, specification_module_name, out_storage=None, type=None, submodels=None):
        """specification_module_name is name of a module that contains a dictionary called
        'specification'. 'type' is the name of model member, such as 'commercial', 'residential'. The specification dictionary
        is expected to have an entry of this name. If 'submodels' is given (list or a number),
        the restimation is done only for those submodels.
        """
        exec("import " + specification_module_name)
        eval("reload (" + specification_module_name + ")")
        exec("specification_dict =" + specification_module_name + ".specification")
        if type is not None:
            specification_dict = specification_dict[type]
        if submodels is not None: #remove all submodels but the given ones from specification
            submodels_to_be_deleted = specification_dict.keys()
            if not isinstance(submodels, list):
                submodels = [submodels]
            for sm in submodels:
                if sm not in submodels_to_be_deleted:
                    raise ValueError, "Submodel %s not in the specification." % sm
                submodels_to_be_deleted.remove(sm)
                if "_definition_" in submodels_to_be_deleted:
                    submodels_to_be_deleted.remove("_definition_")
            for sm in submodels_to_be_deleted:
                del specification_dict[sm]
        specification = EquationSpecification(specification_dict=specification_dict)
        new_namespace = self.model_system.run_year_namespace
        new_namespace["specification"] = specification
        self.model_system.do_process(new_namespace)
        self.extract_coefficients_and_specification()
        if self.save_estimation_results:
            self.save_results(out_storage=out_storage)

    def predict(self):
        """ Run prediction. Currently makes sense only for choice models."""
        # Create temporary configuration where all words 'estimate' are replaced by 'run'
        tmp_config = Resources(self.config)
        models = tmp_config.get('models',[])
        for model in models:
            if isinstance(model, dict):
                model_name = model.keys()[0]
                if (model[model_name] == "estimate"):
                    model[model_name] = 'run'
                elif (isinstance(model[model_name], list) and ("estimate" in model[model_name])):
                    for i in range(len(model[model_name])):
                        if model[model_name][i] == 'estimate':
                            model[model_name][i] = 'run'
        tmp_config['models'] = models
        # save current locations of agents
        is_choice_model = True
        try:
            agents = self.get_agent_set()
            choice_id_name = self.get_choice_set().get_id_name()[0]
            current_choices = agents.get_attribute(choice_id_name).copy()
        except:
            is_choice_model = False
        # run the model
        self.model_system.run(tmp_config, write_datasets_to_cache_at_end_of_year=False)
        # replace new chices with the original ones and put predictions into new attribute
        if is_choice_model:
            agents = self.get_agent_set()
            new_choices = agents.get_attribute(choice_id_name).copy()
            agents.modify_attribute(name=choice_id_name, data=current_choices)
            agents.add_primary_attribute(name='predicted_%s' % choice_id_name, data=new_choices)
            logger.log_status("Predictions saved into attribute 'predicted_%s'" % choice_id_name)
        
    def save_results(self, out_storage=None, model_name=None):
        if self.specification is None or self.coefficients is None:
            raise ValueError, "model specification or coefficient is None"

        #invalid = self.coefficients.is_invalid()
        if False:
            logger.log_warning('Invalid coefficients. Not saving results!')
            return

        if model_name is None:
            if self.model_name is not None:
                model_name = self.model_name
            else:
                raise ValueError, "model_name unspecified"

        out_storage_available = True
        if out_storage:
            pass
        elif 'output_configuration' in self.config:
            try:
                config = DatabaseServerConfiguration(
                    host_name = self.config['output_configuration'].host_name,
                    user_name = self.config['output_configuration'].user_name,
                    password = self.config['output_configuration'].password
                )
                db_server = DatabaseServer(config)
                database_name = self.config["output_configuration"].database_name
    
                if not db_server.has_database(database_name):
                    db_server.create_database(database_name)
    
                output_db = db_server.get_database(database_name)
                out_storage = StorageFactory().get_storage(
                    type='sql_storage',
                    storage_location=output_db)
            except:
                logger.log_warning("Problem with connecting database given by 'output_configuration'.")
                out_storage_available = False
        else:
            logger.log_warning("No output_configuration given.")
            out_storage_available = False

        # the original model name of development_project_lcm is too long as a mysql db table name, truncate it
        if model_name.rfind("_development_project_location_choice_model") >=0:
            model_name = model_name.replace('_project', '')
        specification_table = '%s_specification' % model_name
        coefficients_table = '%s_coefficients' % model_name
        if out_storage_available:
            logger.start_block("Writing specification and coefficients into storage given by 'output_configuration'")
            self.specification.write(out_storage=out_storage, out_table_name=specification_table)
            self.coefficients.write(out_storage=out_storage, out_table_name=coefficients_table)
            logger.end_block()
        logger.start_block("Writing specification and coefficients into %s" % AttributeCache().get_storage_location())
        self.specification.write(out_storage=AttributeCache(), out_table_name=specification_table)
        self.coefficients.write(out_storage=AttributeCache(), out_table_name=coefficients_table)
        logger.end_block()

    def extract_coefficients_and_specification(self):
        for key in self.model_system.run_year_namespace.keys():
            if isinstance(self.model_system.run_year_namespace[key], Coefficients):
                self.coefficients = self.model_system.run_year_namespace[key]
            if isinstance(self.model_system.run_year_namespace[key], EquationSpecification):
                self.specification = self.model_system.run_year_namespace[key]
       #for key in self.model_system.vardict.keys():
#            if key.rfind("coefficients") >=0:
#                if isinstance(self.model_system.vardict[key], tuple):
#                    self.coefficients = self.model_system.vardict[key][0]
#                else:
#                    self.coefficients = self.model_system.vardict[key]
#            if key.rfind("specification") >=0:
#                if isinstance(self.model_system.vardict[key], tuple):
#                    self.specification = self.model_system.vardict[key][0]
#                else:
#                    self.specification = self.model_system.vardict[key]

    def get_data(self, coefficient, submodel=-2):
        return self.get_model().get_data(coefficient, submodel)

    def get_coefficient_names(self, submodel=-2):
        return self.get_model().get_coefficient_names(submodel)

    def get_data_as_dataset(self, submodel=-2):
        return self.get_model().get_data_as_dataset(submodel)

    def get_model(self):
        return self.model_system.run_year_namespace["model"]
        
    def get_choice_set(self): # works only for choice models
        return self.get_model().model_interaction.interaction_datasets[0].get_dataset(2)
    
    def get_choice_set_index(self): # works only for choice models
        return self.get_model().model_interaction.interaction_datasets[0].get_index(2)
        
    def get_choice_set_index_for_submodel(self, submodel): # works only for choice models
        index = self.get_choice_set_index()
        return take (index, indices=self.get_agent_set_index_for_submodel(submodel), axis=0)
    
    def get_agent_set(self): # works only for choice models
        return self.get_model().model_interaction.interaction_datasets[0].get_dataset(1)
    
    def get_agent_set_index(self): # works only for choice models
        return self.get_model().model_interaction.interaction_datasets[0].get_index(1)
        
    def get_agent_set_index_for_submodel(self, submodel):
        model = self.get_model()
        return model.observations_mapping[submodel]
    
    def plot_correlation(self, submodel=-2):
        ds = self.get_data_as_dataset(submodel)
        attrs = [attr for attr in ds.get_known_attribute_names() if attr not in ds.get_id_name()]
        ds.correlation_image(attrs)
        
    def plot_choice_set(self):
        choice_set = self.get_choice_set()
        result = zeros(choice_set.size(), dtype='int16')
        result[unique_values(self.get_choice_set_index().ravel())] = 1
        choice_set.add_attribute(name='__sampled_for_estimation__', data=result)
        choice_set.plot_map('__sampled_for_estimation__', background=-1)
        choice_set.delete_one_attribute('__sampled_for_estimation__')
        
    def plot_choice_set_attribute(self, name):
        choice_set = self.get_choice_set()
        filter_var = ones(choice_set.size(), dtype='int16')
        filter_var[unique_values(self.get_choice_set_index().ravel())] = 0
        choice_set.add_attribute(name='__choice_set_filter_for_estimation__', data=filter_var)
        choice_set.plot_map(name, filter='__choice_set_filter_for_estimation__')
        choice_set.delete_one_attribute('__choice_set_filter_for_estimation__')
        
    def cleanup(self, remove_cache=True):
        """Use this only if you don't want to reestimate."""
        self.simulation_state.remove_singleton(delete_cache=remove_cache)
        SessionConfiguration().remove_singleton()


def get_specification_for_estimation(specification_dict=None, specification_storage=None,
                                        specification_table = None):
    if specification_dict is not None:
        return EquationSpecification(specification_dict=specification_dict)
    from opus_core.choice_model import prepare_specification_and_coefficients
    (specification, dummy) = prepare_specification_and_coefficients(specification_storage, specification_table)
    return specification

def update_controller_by_specification_from_module(run_configuration, model_name, specification_module):
    controller = run_configuration["models_configuration"][model_name]["controller"]
    controller["import"][specification_module] = "specification as spec"
    controller["prepare_for_estimate"]["arguments"]["specification_dict"] = "spec"
    controller["prepare_for_estimate"]["arguments"]["specification_storage"] = "None"

    run_configuration["models_configuration"][model_name]["controller"].merge(controller)
    return run_configuration

def plot_utility_diagnose(filename):
    from opus_core.plot_functions import plot_barchart
    data, coef_names = load_table_from_text_file(filename, convert_to_float=True, header=True)
    plot_barchart(data[2,:], labels = coef_names)

def plot_correlation_diagnose(filename):
    from opus_core.plot_functions import plot_matplot
    data, coef_names = load_table_from_text_file(filename, convert_to_float=True, header=True)
    plot_matplot(absolute(data), xlabels = coef_names, ylabels=coef_names)

