# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import copy
from opus_core import ndimage
from numpy import absolute, array, where, take, zeros, ones, concatenate
from opus_core.logger import logger
from opus_core.resources import Resources
from opus_core.coefficients import Coefficients
from opus_core.variables.variable_name import VariableName
from opus_core.simulation_state import SimulationState
from opus_core.misc import load_table_from_text_file, unique
from opus_core.store.attribute_cache import AttributeCache
from opus_core.equation_specification import EquationSpecification
from opus_core.storage_factory import StorageFactory
from opus_core.database_management.database_server import DatabaseServer
from opus_core.session_configuration import SessionConfiguration
from opus_core.simulation.model_explorer import ModelExplorer
from opus_core.model_coordinators.model_system import ModelSystem

class Estimator(ModelExplorer):
    def __init__(self, config=None, save_estimation_results=False):
        if 'cache_directory' not in config or config['cache_directory'] is None:
            raise KeyError("The cache directory must be specified in the "
                "given configuration, giving the filesystem path to the cache "
                "directory containing the data with which to estimate. Please "
                "check that your configuration contains the 'cache_directory' "
                "entry and that it is not None.")

        self.simulation_state = SimulationState(new_instance=True, start_time=config.get('base_year', 0))
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
        estimate_config_changes = self.config.get('config_changes_for_estimation', {}).get('estimate_config', {})
        if len(estimate_config_changes) > 0:
            change = Resources({'models_configuration': {self.model_name: {'controller': {'init': {'arguments': {}}}}}})
            estimate_config_str = self.config['models_configuration'].get(self.model_name, {}).get('controller', {}).get('init', {}).get('arguments', {}).get('estimate_config', '{}')
            estimate_config = Resources({})
            try:
                estimate_config = eval(estimate_config_str)
            except:
                pass
 
            estimate_config.merge(estimate_config_changes)
            self.config.merge(change)
            self.config['models_configuration'][self.model_name]['controller']['init']['arguments']['estimate_config'] = 'Resources(%s)' % estimate_config

    def estimate(self, out_storage=None):
        self.model_system.run(self.config, write_datasets_to_cache_at_end_of_year=False)
        self.extract_coefficients_and_specification()
        
        if self.save_estimation_results:
            self.save_results(out_storage=out_storage)
            self.log_estimation_result()

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

    def predict(self, predicted_choice_id_name, agents_index=None):
        """ Run prediction. Currently makes sense only for choice models."""
        # Create temporary configuration where all words 'estimate' are replaced by 'run'
        tmp_config = Resources(self.config)
        
        if self.agents_index_for_prediction is None:
            self.agents_index_for_prediction = self.get_agent_set_index().copy()
            
        if agents_index is None:
            agents_index = self.agents_index_for_prediction
        
        tmp_config['models_configuration'][self.model_name]['controller']['run']['arguments']['coefficients'] = "coeff_est"
        tmp_config['models_configuration'][self.model_name]['controller']['run']['arguments']['agents_index'] = "agents_index"
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
            dummy_data = zeros(current_choices.size, dtype=current_choices.dtype)-1
            agents.modify_attribute(name=choice_id_name, data=dummy_data) #reset all choices
            
            run_year_namespace["process"] = "run"
            run_year_namespace["coeff_est"] = self.coefficients
            run_year_namespace["agents_index"] = agents_index
            run_year_namespace["processmodel_config"] = tmp_config['models_configuration'][self.model_name]['controller']['run']
            new_choices = self.model_system.do_process(run_year_namespace)
            
            #self.model_system.run(tmp_config, write_datasets_to_cache_at_end_of_year=False)
            #new_choices = agents.get_attribute(choice_id_name).copy()
            agents.modify_attribute(name=choice_id_name, data=current_choices)
            dummy_data[agents_index] = new_choices
            if predicted_choice_id_name not in agents.get_known_attribute_names():
                agents.add_primary_attribute(name=predicted_choice_id_name, data=dummy_data)
            else:
                agents.modify_attribute(name=predicted_choice_id_name, data=dummy_data)
            logger.log_status("Predictions saved into attribute " + predicted_choice_id_name)
            return True
        except Exception, e:
            logger.log_error("Error encountered in prediction: %s" % e)
            logger.log_stack_trace()
        
        return False

    def create_prediction_success_table(self, 
                                        summarize_by=None, 
                                        predicted_choice_id_name=None,
                                        predicted_choice_id_prefix="predicted_",
                                        log_to_file=None,
                                        force_predict=True):
        agents = self.get_agent_set()
        choices = self.get_choice_set()
        choice_id_name = choices.get_id_name()[0]
        
        if self.agents_index_for_prediction is not None:
            agents_index = self.agents_index_for_prediction
        else:
            agents_index = self.get_agent_set_index()

        if predicted_choice_id_name is None or len(predicted_choice_id_name) == 0:
            predicted_choice_id_name = predicted_choice_id_prefix + choice_id_name
            
        if force_predict or (predicted_choice_id_name not in agents.get_known_attribute_names()):
            if not self.predict(predicted_choice_id_name=predicted_choice_id_name,
                                agents_index=agents_index
                                ):
                logger.log_error("Failed to run simulation for prediction; unable to create prediction success table.")
                return

        if log_to_file is not None and len(log_to_file) > 0:
            logger.enable_file_logging(log_to_file)
            
        ## by default, compare predicted choice with observed choice
        ## this is not feasible for location choice model, where the 
        ## alternative set is too large to be useful
        if summarize_by is None:
            summarize_by = "%s.%s" % (agents.dataset_name, choice_id_name)
            
        summarize_dataset_name = VariableName(summarize_by).get_dataset_name()
        if summarize_dataset_name == choices.dataset_name:
            summary_id = choices.compute_variables(summarize_by)
            
            chosen_choice_id = agents.get_attribute_by_index(choices.get_id_name()[0], agents_index)
            predicted_choice_id = agents.get_attribute_by_index(predicted_choice_id_name, agents_index)
            chosen_choice_index = choices.get_id_index(chosen_choice_id)
            predicted_choice_index = choices.get_id_index(predicted_choice_id)
            
            chosen_summary_id = summary_id[chosen_choice_index]
            predicted_summary_id = summary_id[predicted_choice_index]
    
            unique_summary_id = unique(summary_id)
        elif summarize_dataset_name == agents.dataset_name:
            chosen_summary_id = agents.compute_variables(summarize_by)[agents_index]
            
            chosen_choice_id = agents.get_attribute(choice_id_name).copy()
            predicted_choice_id = agents.get_attribute(predicted_choice_id_name)
            agents.modify_attribute(name=choice_id_name, data=predicted_choice_id)
            predicted_summary_id = agents.compute_variables(summarize_by)[agents_index]
            
            agents.modify_attribute(name=choice_id_name, data=chosen_choice_id)
    
            unique_summary_id = unique( concatenate((chosen_summary_id, predicted_summary_id)) )
        else:
            logger.log_error("summarize_by expression '%s' is specified for dataset %s, which is neither the choice_set '%s' nor the agent_set '%s'." 
                             % (summarize_by, summarize_dataset_name, choices.dataset_name, agents.dataset_name))
            return False
            
        # observed on row, predicted on column
        prediction_matrix = zeros( (unique_summary_id.size, unique_summary_id.size), dtype="int32" )

        def _convert_array_to_tab_delimited_string(an_array):
            from numpy import dtype
            if an_array.dtype == dtype('f'):
                return "\t".join(["%5.4f" % item for item in an_array])
            return "\t".join([str(item) for item in an_array])
        
        logger.log_status("Observed_id\tSuccess_rate\t%s" % \
                          _convert_array_to_tab_delimited_string(unique_summary_id) )
        i = 0
        success_rate = zeros( unique_summary_id.size, dtype="float32" )
        for observed_id in unique_summary_id:
            predicted_id = predicted_summary_id[chosen_summary_id==observed_id]
            prediction_matrix[i] = ndimage.sum(ones(predicted_id.size), labels=predicted_id, index=unique_summary_id )
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
            model_name = self.config.get('model_name_for_coefficients', None)
            
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

    def log_estimation_result(self):
        procedure = self.model_system.run_year_namespace["model"].procedure        
        if not hasattr(procedure, 'print_results'):
            logger.log_warning("Estimation procedure %s doesn't have a print_results() method, "  % procedure + \
                               "which is needed to log estimation results.")
            return

        tmp_config = Resources(self.config)
        outputvar = tmp_config['models_configuration'][self.model_name]['controller']['estimate']['arguments']['output']
        results = self.model_system.vardict.get(outputvar, "process_output")[1]
        
        storage_location = AttributeCache().get_storage_location()
        log_file_name = "estimate_models.log" ## one file for all estimation results
        logger.enable_file_logging( os.path.join(storage_location, log_file_name) )
        logger.start_block("%s Estimation Results" % self.model_name)        
        for submodel, submodel_results in results.items():
            logger.log_status( "Submodel %s" % submodel)
            procedure.print_results(submodel_results)
        logger.end_block()
        logger.disable_file_logging()        
    
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

        
    def get_agents_for_estimation(self): 
        return self.get_active_agent_set()
            
    def get_specification(self):
        return self.specification
    
    def cleanup(self, remove_cache=True):
        """Use this only if you don't want to reestimate."""
        self.simulation_state.remove_singleton(delete_cache=remove_cache)
        SessionConfiguration().remove_singleton()

    def export_estimation_data(self, submodel=-2, filename='./estimation_data.txt', wide=True, **kwargs):
        """Exports estimation data into file. For choice models, 'wide' controls if it is in a wide format 
        (such as biogeme format, i.e. one row per observation), or in a long format (i.e. each alternative 
        has one row per observation).
        """
        from opus_core.choice_model import ChoiceModel
        model = self.get_model()
        if isinstance(model, ChoiceModel):
            data = model.model_interaction.convert_data_from_estimation_to_simulation_format(submodel)
            model.export_estimation_data(submodel, 
                                         model.model_interaction.get_chosen_choice_for_submodel(submodel),
                                         data, 
                                         array(model.model_interaction.submodel_coefficients[submodel].get_variable_names()), 
                                         file_name=filename, use_biogeme_data_format=wide, **kwargs)
        else: # regression data
            model.export_estimation_data(submodel, file_name=filename, **kwargs)
        
        
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

