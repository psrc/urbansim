# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import copy
from scipy import ndimage
from numpy import absolute, array, where, take, zeros, ones, unique, concatenate
from opus_core.logger import logger
from opus_core.resources import Resources
from opus_core.coefficients import Coefficients
from opus_core.variables.variable_name import VariableName
from opus_core.simulation_state import SimulationState
from opus_core.misc import load_table_from_text_file, unique_values
from opus_core.store.attribute_cache import AttributeCache
from opus_core.equation_specification import EquationSpecification
from opus_core.storage_factory import StorageFactory
from opus_core.database_management.database_server import DatabaseServer
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
                             in_storage=AttributeCache())
        self.config = Resources(config)
        self.save_estimation_results = save_estimation_results
        self.debuglevel = self.config.get("debuglevel", 4)
        self.model_system = ModelSystem()
        self.agents_index_for_prediction = None
        
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

    def reestimate(self, specification_module_name=None, specification_dict=None, out_storage=None, type=None, submodels=None):
        """specification_module_name is name of a module that contains a dictionary called
        'specification'. If it is not given, the argument specification_dict must be given which is a dictionary object.
        'type' is the name of model member, such as 'commercial', 'residential'. The specification dictionary
        is expected to have an entry of this name. If 'submodels' is given (list or a number),
        the restimation is done only for those submodels.
        """
        if specification_module_name is not None:
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
        self.specification = EquationSpecification(specification_dict=specification_dict)
        new_namespace = self.model_system.run_year_namespace
        keys_coeff_spec = self.get_keys_for_coefficients_and_specification()
        new_namespace[keys_coeff_spec["specification"]] = self.specification
        self.coefficients, coeff_dict_dummy = self.model_system.do_process(new_namespace)
        ## update run_year_namespce since it's not been updated by do_process
        self.model_system.run_year_namespace = new_namespace
        self.model_system.run_year_namespace[keys_coeff_spec["coefficients"]] = self.coefficients
        
        ## this gets coeff and spec from run_year_namespce and is only updated in _run_year method
        #self.extract_coefficients_and_specification()  
        if self.save_estimation_results:
            self.save_results(out_storage=out_storage)

    def predict(self, predicted_choice_id_prefix="predicted_", predicted_choice_id_name=None):
        """ Run prediction. Currently makes sense only for choice models."""
        # Create temporary configuration where all words 'estimate' are replaced by 'run'
        tmp_config = Resources(self.config)
        
        if self.agents_index_for_prediction is None:
            self.agents_index_for_prediction = self.get_agent_set_index().copy()
            
        tmp_config['models_configuration'][self.model_name]['controller']['run']['arguments']['agents_index'] = "index"
        tmp_config['models_configuration'][self.model_name]['controller']['run']['arguments']['chunk_specification'] = "{'nchunks':1}"

        ### save specification and coefficients to cache (no matter the save_estimation_results flag)
        ### so that the prepare_for_run method could load specification and coefficients from there
        #output_configuration = self.config['output_configuration']
        #del self.config['output_configuration']
        #self.save_results()
        
        #self.config['output_configuration'] = output_configuration
        
        #self.model_system.run_year_namespace["coefficients"] = self.coefficients
        #del tmp_config['models_configuration'][self.model_name]['controller']['prepare_for_run']
        
        try:
            run_year_namespace = copy.copy(self.model_system.run_year_namespace)
        except:
            logger.log_error("The estimate() method must be run first")
            return False
        
        try:
            agents = self.get_agent_set()
            choice_id_name = self.get_choice_set().get_id_name()[0]
            # save current locations of agents
            current_choices = agents.get_attribute(choice_id_name).copy()

            if predicted_choice_id_name is None or len(predicted_choice_id_name) == 0:
                predicted_choice_id_name = predicted_choice_id_prefix + choice_id_name

            run_year_namespace["process"] = "run"
            run_year_namespace["processmodel_config"] = tmp_config['models_configuration'][self.model_name]['controller']['run']
            self.model_system.do_process(run_year_namespace)
            
            #self.model_system.run(tmp_config, write_datasets_to_cache_at_end_of_year=False)
            new_choices = agents.get_attribute(choice_id_name).copy()
            agents.modify_attribute(name=choice_id_name, data=current_choices)
            if predicted_choice_id_name not in agents.get_known_attribute_names():
                agents.add_primary_attribute(name=predicted_choice_id_name, data=new_choices)
            else:
                agents.modify_attribute(name=predicted_choice_id_name, data=new_choices)
            logger.log_status("Predictions saved into attribute " + predicted_choice_id_name)
            return True
        except Exception, e:
            logger.log_error("Error encountered in prediction: %s" % e)
            logger.log_stack_trace()
        
        return False

    def create_prediction_success_table(self, 
                                        geography_id_expression="fazdistrict_id=building.disaggregate(faz.fazdistrict_id, intermediates=[zone, parcel])",
                                        predicted_choice_id_prefix="predicted_", 
                                        predicted_choice_id_name=None,
                                        log_to_file=None,
                                        force_predict=True):
        agents = self.get_agent_set()
        choices = self.get_choice_set()
        choice_id_name = choices.get_id_name()[0]
        if predicted_choice_id_name is None or len(predicted_choice_id_name) == 0:
            predicted_choice_id_name = predicted_choice_id_prefix + choice_id_name
            
        if force_predict or (predicted_choice_id_name not in agents.get_known_attribute_names()):
            if not self.predict(predicted_choice_id_prefix=predicted_choice_id_prefix, 
                                predicted_choice_id_name=predicted_choice_id_name):
                return

        if log_to_file is not None and len(log_to_file) > 0:
            logger.enable_file_logging(log_to_file)
            
        if self.agents_index_for_prediction is not None:
            agents_index = self.agents_index_for_prediction
        else:
            agents_index = self.get_agent_set_index()
            
        geography_expression_dataset_name = VariableName(geography_id_expression).get_dataset_name()
        if geography_expression_dataset_name == choices.dataset_name:
            geography_id = choices.compute_variables(geography_id_expression)
            
            chosen_choice_id = agents.get_attribute_by_index(choices.get_id_name()[0], agents_index)
            predicted_choice_id = agents.get_attribute_by_index(predicted_choice_id_name, agents_index)
            chosen_choice_index = choices.get_id_index(chosen_choice_id)
            predicted_choice_index = choices.get_id_index(predicted_choice_id)
            
            chosen_geography_id = geography_id[chosen_choice_index]
            predicted_geography_id = geography_id[predicted_choice_index]
    
            unique_geography_id = unique(geography_id)
        elif geography_expression_dataset_name == agents.dataset_name:
            chosen_geography_id = agents.compute_variables(geography_id_expression)[agents_index]
            
            chosen_choice_id = agents.get_attribute(choice_id_name).copy()
            predicted_choice_id = agents.get_attribute(predicted_choice_id_name)
            agents.modify_attribute(name=choice_id_name, data=predicted_choice_id)
            predicted_geography_id = agents.compute_variables(geography_id_expression)[agents_index]
            
            agents.modify_attribute(name=choice_id_name, data=chosen_choice_id)
    
            unique_geography_id = unique( concatenate((chosen_geography_id, predicted_geography_id)) )
        else:
            logger.log_error("geography expression %s is specified for an unknown dataset" % geography_id_expression)
            return False
            
        # observed on row, predicted on column
        prediction_matrix = zeros( (unique_geography_id.size, unique_geography_id.size), dtype="int32" )

        def _convert_array_to_tab_delimited_string(an_array):
            from numpy import dtype
            if an_array.dtype == dtype('f'):
                return "\t".join(["%5.4f" % item for item in an_array])
            return "\t".join([str(item) for item in an_array])
        
        logger.log_status("Observed_id\tSuccess_rate\t%s" % \
                          _convert_array_to_tab_delimited_string(unique_geography_id) )
        i = 0
        success_rate = zeros( unique_geography_id.size, dtype="float32" )
        for observed_id in unique_geography_id:
            predicted_id = predicted_geography_id[chosen_geography_id==observed_id]
            prediction_matrix[i] = ndimage.sum(ones(predicted_id.size), labels=predicted_id, index=unique_geography_id )
            if prediction_matrix[i].sum() > 0:
                if prediction_matrix[i].sum() > 0:
                    success_rate[i] = float(prediction_matrix[i, i]) / prediction_matrix[i].sum()
                else:
                    success_rate[i] = 0
            logger.log_status("%s\t\t%5.4f\t\t%s" % (observed_id, success_rate[i], 
                                              _convert_array_to_tab_delimited_string(prediction_matrix[i]) ) )
            i+=1

        success_rate2 = zeros( i, dtype="float32" )
        for j in range(i):
            if prediction_matrix[j, :].sum() > 0:
                success_rate2[j]=float(prediction_matrix[:,j].sum()) / prediction_matrix[j, :].sum()
            else:
                success_rate2[j]=0
        logger.log_status("%s\t\t%s\t\t%s" % (' ', ' ', 
                                                 _convert_array_to_tab_delimited_string( success_rate2 ) ))
        logger.disable_file_logging(filename=log_to_file)

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
        elif 'estimation_database_configuration' in self.config:
            try:
                db_server = DatabaseServer(self.config['estimation_database_configuration'])
                database_name = self.config["estimation_database_configuration"].database_name
    
                if not db_server.has_database(database_name):
                    db_server.create_database(database_name)
    
                output_db = db_server.get_database(database_name)
                out_storage = StorageFactory().get_storage(
                    type='sql_storage',
                    storage_location=output_db)
            except:
                logger.log_warning("Problem with connecting database given by 'estimation_database_configuration'.")
                out_storage_available = False
        else:
            logger.log_warning("No estimation_database_configuration given.")
            out_storage_available = False

        # the original model name of development_project_lcm is too long as a mysql db table name, truncate it
        if model_name.rfind("_development_project_location_choice_model") >=0:
            model_name = model_name.replace('_project', '')
        specification_table = '%s_specification' % model_name
        coefficients_table = '%s_coefficients' % model_name
        if out_storage_available:
            logger.start_block("Writing specification and coefficients into storage given by 'estimation_database_configuration'")
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

    def get_keys_for_coefficients_and_specification(self):
        result = {}
        for key in self.model_system.run_year_namespace.keys():
            if isinstance(self.model_system.run_year_namespace[key], Coefficients):
                result['coefficients'] = key
            if isinstance(self.model_system.run_year_namespace[key], EquationSpecification):
                result['specification'] = key
        if not result.has_key('coefficients'):
            logger.log_warning("No Coefficients object is found in the name space of model_system ")
        if not result.has_key('specification'):
            logger.log_warning("No EquationSpecification object is found in the name space of model_system ")
        
        return result
            
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
        #for information on matplot styles: http://matplotlib.sourceforge.net/tutorial.html
        #particularly useful information on this webpage on "Interactive navigation" using "toolbar2"
        
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

def update_controller_by_specification_from_module(run_configuration, model_name, specification_module):
    controller = run_configuration["models_configuration"][model_name]["controller"]
    controller["import"][specification_module] = "specification as spec"
    controller["prepare_for_estimate"]["arguments"]["specification_dict"] = "spec"
    controller["prepare_for_estimate"]["arguments"]["specification_storage"] = "None"

    run_configuration["models_configuration"][model_name]["controller"].merge(controller)
    return run_configuration

def update_controller_by_specification_from_dict(run_configuration, model_name, specification_dict):
    controller = run_configuration["models_configuration"][model_name]["controller"]
    controller["prepare_for_estimate"]["arguments"]["specification_dict"] = "%s" % specification_dict
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

