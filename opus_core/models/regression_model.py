# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.misc import DebugPrinter, unique
from opus_core.regression_model_factory import RegressionModelFactory
from opus_core.specified_coefficients import SpecifiedCoefficients, SpecifiedCoefficientsFor1Submodel
from opus_core.resources import Resources
from opus_core.coefficients import create_coefficient_from_specification
from opus_core.chunk_model import ChunkModel
from opus_core.model_component_creator import ModelComponentCreator
from opus_core.variables.variable_name import VariableName
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory
from opus_core.model import prepare_specification_and_coefficients, get_specification_for_estimation
from opus_core.logger import logger
from numpy import arange, zeros, float32, ndarray, array, where, inf, concatenate, asarray
from numpy import isinf, isnan, inf, nan, nan_to_num
from time import time

class RegressionModel(ChunkModel):

    model_name = "Regression Model"
    model_short_name = "RM"

    def __init__(self, regression_procedure="opus_core.linear_regression",
                  submodel_string=None,
                  run_config=None, estimate_config=None, debuglevel=0, dataset_pool=None):
 
        self.debug = DebugPrinter(debuglevel)

        self.dataset_pool = self.create_dataset_pool(dataset_pool)

        self.regression = RegressionModelFactory().get_model(name=regression_procedure)
        if self.regression == None:
            raise StandardError, "No regression procedure given."

        self.submodel_string = submodel_string

        self.run_config = run_config
        if self.run_config == None:
            self.run_config = Resources()
        if not isinstance(self.run_config,Resources) and isinstance(self.run_config, dict):
            self.run_config = Resources(self.run_config)

        self.estimate_config = estimate_config
        if self.estimate_config == None:
            self.estimate_config = Resources()
        if not isinstance(self.estimate_config,Resources) and isinstance(self.estimate_config, dict):
            self.estimate_config = Resources(self.estimate_config)
            
        self.data = {}
        self.coefficient_names = {}
        self.coefficient_names_all = {}
        ChunkModel.__init__(self)
        self.get_status_for_gui().initialize_pieces(3, pieces_description = array(['initialization', 'computing variables', 'submodel: 1']))

    def run(self, specification, coefficients, dataset, index=None, chunk_specification=None,
            data_objects=None, run_config=None, initial_values=None, procedure=None, debuglevel=0):
        """'specification' is of type EquationSpecification,
            'coefficients' is of type Coefficients,
            'dataset' is of type Dataset,
            'index' are indices of individuals in dataset for which
                        the model runs. If it is None, the whole dataset is considered.
            'chunk_specification' determines  number of chunks in which the simulation is processed.
            'data_objects' is a dictionary where each key is the name of an data object
            ('zone', ...) and its value is an object of class  Dataset.
           'run_config' is of type Resources, it gives additional arguments for the run.
           If 'procedure' is given, it overwrites the regression_procedure of the constructor.
           'initial_values' is an array of the initial values of the results. It will be overwritten
           by the results for those elements that are handled by the model (defined by submodels in the specification).
           By default the results are initialized with 0.
            'debuglevel' overwrites the constructor 'debuglevel'.
        """
        self.debug.flag = debuglevel
        if run_config == None:
            run_config = Resources()
        if not isinstance(run_config,Resources) and isinstance(run_config, dict):
            run_config = Resources(run_config)
        self.run_config = run_config.merge_with_defaults(self.run_config)
        self.run_config.merge({"debug":self.debug})
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        self.dataset_name = dataset.get_dataset_name()
        self.dataset_pool.replace_dataset(self.dataset_name, dataset)
        
        if procedure is not None: 
            self.regression = RegressionModelFactory().get_model(name=procedure)
        if initial_values is None:
            self.initial_values = zeros((dataset.size(),), dtype=float32)
        else:
            self.initial_values = zeros((dataset.size(),), dtype=initial_values.dtype)
            self.initial_values[index] = initial_values
            
        if dataset.size()<=0: # no data loaded yet
            dataset.get_id_attribute()
        if index is None:
            index = arange(dataset.size())
            
        result = ChunkModel.run(self, chunk_specification, dataset, index, float32,
                                 specification=specification, coefficients=coefficients)
        return result

    def run_chunk (self, index, dataset, specification, coefficients):
        self.specified_coefficients = SpecifiedCoefficients().create(coefficients, specification, neqs=1)
        compute_resources = Resources({"debug":self.debug})
        submodels = self.specified_coefficients.get_submodels()
        self.get_status_for_gui().update_pieces_using_submodels(submodels=submodels, leave_pieces=2)
        self.map_agents_to_submodels(submodels, self.submodel_string, dataset, index,
                                      dataset_pool=self.dataset_pool, resources = compute_resources)
        variables = self.specified_coefficients.get_full_variable_names_without_constants()
        self.debug.print_debug("Compute variables ...",4)
        self.increment_current_status_piece()
        dataset.compute_variables(variables, dataset_pool = self.dataset_pool, resources = compute_resources)
        data = {}
        coef = {}
        outcome=self.initial_values[index].copy()
        for submodel in submodels:
            coef[submodel] = SpecifiedCoefficientsFor1Submodel(self.specified_coefficients,submodel)
            self.coefficient_names[submodel] = coef[submodel].get_coefficient_names_without_constant()[0,:]
            self.coefficient_names_all[submodel] = coef[submodel].get_coefficient_names()[0,:]
            self.debug.print_debug("Compute regression for submodel " +str(submodel),4)
            self.increment_current_status_piece()
            self.data[submodel] = dataset.create_regression_data(coef[submodel],
                                                                index = index[self.observations_mapping[submodel]])
            nan_index = where(isnan(self.data[submodel]))[1]
            inf_index = where(isinf(self.data[submodel]))[1]
            vnames = asarray(coef[submodel].get_variable_names())
            if nan_index.size > 0:
                nan_var_index = unique(nan_index)
                self.data[submodel] = nan_to_num(self.data[submodel])
                logger.log_warning("NaN(Not A Number) is returned from variable %s; it is replaced with %s." % (vnames[nan_var_index], nan_to_num(nan)))
                #raise ValueError, "NaN(Not A Number) is returned from variable %s; check the model specification table and/or attribute values used in the computation for the variable." % vnames[nan_var_index]
            if inf_index.size > 0:
                inf_var_index = unique(inf_index)
                self.data[submodel] = nan_to_num(self.data[submodel])
                logger.log_warning("Inf is returned from variable %s; it is replaced with %s." % (vnames[inf_var_index], nan_to_num(inf)))
                #raise ValueError, "Inf is returned from variable %s; check the model specification table and/or attribute values used in the computation for the variable." % vnames[inf_var_index]
            
            if (self.data[submodel].shape[0] > 0) and (self.data[submodel].size > 0): # observations for this submodel available
                outcome[self.observations_mapping[submodel]] = \
                    self.regression.run(self.data[submodel], coef[submodel].get_coefficient_values()[0,:],
                        resources=self.run_config).astype(outcome.dtype)
        return outcome

    def correct_infinite_values(self, dataset, outcome_attribute_name, maxvalue=1e+38, clip_all_larger_values=False):
        """Check if the model resulted in infinite values. If yes,
        print warning and clip the values to maxvalue. 
        If clip_all_larger_values is True, all values larger than maxvalue are clip to maxvalue.
        """
        infidx = where(dataset.get_attribute(outcome_attribute_name) == inf)[0]

        if infidx.size > 0:
            logger.log_warning("Infinite values in %s. Clipped to %s." % (outcome_attribute_name, maxvalue))
            dataset.set_values_of_one_attribute(outcome_attribute_name, maxvalue, infidx)
        if clip_all_larger_values:
            idx = where(dataset.get_attribute(outcome_attribute_name) > maxvalue)[0]
            if idx.size > 0:
                logger.log_warning("Values in %s larger than %s. Clipped to %s." % (outcome_attribute_name, maxvalue, maxvalue))
                dataset.set_values_of_one_attribute(outcome_attribute_name, maxvalue, idx)
            
    def estimate(self, specification, dataset, outcome_attribute, index = None, procedure=None, data_objects=None,
                        estimate_config=None,  debuglevel=0):
        """'specification' is of type EquationSpecification,
            'dataset' is of type Dataset,
            'outcome_attribute' - string that determines the dependent variable,
            'index' are indices of individuals in dataset for which
                    the model runs. If it is None, the whole dataset is considered.
            'procedure' - name of the estimation procedure. If it is None,
                there should be an entry "estimation" in 'estimate_config' that determines the procedure. The class
                must have a method 'run' that takes as arguments 'data', 'regression_procedure' and 'resources'.
                It returns a dictionary with entries 'estimators', 'standard_errors' and 't_values' (all 1D numpy arrays).
            'data_objects' is a dictionary where each key is the name of an data object
                    ('zone', ...) and its value is an object of class  Dataset.
            'estimate_config' is of type Resources, it gives additional arguments for the estimation procedure.
            'debuglevel' overwrites the class 'debuglevel'.
        """
        #import wingdbstub
        self.debug.flag = debuglevel
        if estimate_config is None:
            estimate_config = Resources()
        if not isinstance(estimate_config,Resources) and isinstance(estimate_config, dict):
            estimate_config = Resources(estimate_config)
        self.estimate_config = estimate_config.merge_with_defaults(self.estimate_config)
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        self.procedure=procedure
        if self.procedure is None:
            self.procedure = self.estimate_config.get("estimation", None)
        if self.procedure is not None:
            self.procedure = ModelComponentCreator().get_model_component(self.procedure)
        else:
            logger.log_warning("No estimation procedure given, or problems with loading the corresponding module.")

        compute_resources = Resources({"debug":self.debug})
        if dataset.size()<=0: # no data loaded yet
            dataset.get_id_attribute()
        if index is None:
            index = arange(dataset.size())
        if not isinstance(index,ndarray):
            index=array(index)

        estimation_size_agents = self.estimate_config.get("estimation_size_agents", None) # should be a proportion of the agent_set
        if estimation_size_agents is None:
            estimation_size_agents = 1.0
        else:
            estimation_size_agents = max(min(estimation_size_agents,1.0),0.0) # between 0 and 1

        if estimation_size_agents < 1.0:
            self.debug.print_debug("Sampling agents for estimation ...",3)
            estimation_idx = sample_noreplace(arange(index.size),
                                                         int(index.size*estimation_size_agents))
        else:
            estimation_idx = arange(index.size)

        estimation_idx = index[estimation_idx]
        self.debug.print_debug("Number of observations for estimation: " + str(estimation_idx.size),2)
        if estimation_idx.size <= 0:
            self.debug.print_debug("Nothing to be done.",2)
            return (None, None)

        coefficients = create_coefficient_from_specification(specification)
        self.specified_coefficients = SpecifiedCoefficients().create(coefficients, specification, neqs=1)
        submodels = self.specified_coefficients.get_submodels()
        self.get_status_for_gui().update_pieces_using_submodels(submodels=submodels, leave_pieces=2)
        self.map_agents_to_submodels(submodels, self.submodel_string, dataset, estimation_idx,
                                      dataset_pool=self.dataset_pool, resources = compute_resources,
                                      submodel_size_max=self.estimate_config.get('submodel_size_max', None))
        variables = self.specified_coefficients.get_full_variable_names_without_constants()
        self.debug.print_debug("Compute variables ...",4)
        self.increment_current_status_piece()
        dataset.compute_variables(variables, dataset_pool=self.dataset_pool, resources = compute_resources)

        coef = {}
        estimated_coef={}
        self.outcome = {}
        dataset.compute_variables([outcome_attribute], dataset_pool=self.dataset_pool, resources=compute_resources)
        regression_resources=Resources(estimate_config)
        regression_resources.merge({"debug":self.debug})
        outcome_variable_name = VariableName(outcome_attribute)
        for submodel in submodels:
            coef[submodel] = SpecifiedCoefficientsFor1Submodel(self.specified_coefficients,submodel)
            self.increment_current_status_piece()
            logger.log_status("Estimate regression for submodel " +str(submodel),
                               tags=["estimate"], verbosity_level=2)
            #logger.log_status("Number of observations: " +str(self.observations_mapping[submodel].size),
                               #tags=["estimate"], verbosity_level=2)
            self.data[submodel] = dataset.create_regression_data_for_estimation(coef[submodel],
                                                            index = estimation_idx[self.observations_mapping[submodel]])
            self.coefficient_names[submodel] = coef[submodel].get_coefficient_names_without_constant()[0,:]
            self.coefficient_names_all[submodel] = self.coefficient_names[submodel] # should correspond to the self.data array (which does not contain constant in estimation) 
            if (self.data[submodel].shape[0] > 0) and (self.data[submodel].size > 0) and (self.procedure is not None): # observations for this submodel available
                self.outcome[submodel] = dataset.get_attribute_by_index(outcome_variable_name.get_alias(), estimation_idx[self.observations_mapping[submodel]])   
                regression_resources.merge({"outcome":  self.outcome[submodel]})
                regression_resources.merge({"coefficient_names":self.coefficient_names[submodel].tolist(),
                            "constant_position": coef[submodel].get_constants_positions()})
                regression_resources.merge({"submodel": submodel})
                estimated_coef[submodel] = self.procedure.run(self.data[submodel], self.regression,
                                                        resources=regression_resources)
                if "estimators" in estimated_coef[submodel].keys():
                    coef[submodel].set_coefficient_values(estimated_coef[submodel]["estimators"])
                if "standard_errors" in estimated_coef[submodel].keys():
                    coef[submodel].set_standard_errors(estimated_coef[submodel]["standard_errors"])
                if "other_measures" in estimated_coef[submodel].keys():
                    for measure in estimated_coef[submodel]["other_measures"].keys():
                        coef[submodel].set_measure(measure,
                              estimated_coef[submodel]["other_measures"][measure])
                if "other_info" in estimated_coef[submodel].keys():
                    for info in estimated_coef[submodel]["other_info"]:
                        coef[submodel].set_other_info(info,
                              estimated_coef[submodel]["other_info"][info])
        coefficients.fill_coefficients(coef)
        self.specified_coefficients.coefficients = coefficients
        self.save_predicted_values_and_errors(specification, coefficients, dataset, outcome_variable_name, index=index, data_objects=data_objects)
            
        return (coefficients, estimated_coef)

    def prepare_for_run(self, dataset=None, dataset_filter=None, filter_threshold=0, **kwargs):
        spec, coef = prepare_specification_and_coefficients(**kwargs)
        if (dataset is not None) and (dataset_filter is not None):
            filter_values = dataset.compute_variables([dataset_filter], dataset_pool=self.dataset_pool)
            index = where(filter_values > filter_threshold)[0]
        else:
            index = None
        return (spec, coef, index)

    def prepare_for_estimate(self, dataset=None, dataset_filter=None, filter_threshold=0, **kwargs):
        spec = get_specification_for_estimation(**kwargs)
        if (dataset is not None) and (dataset_filter is not None):
            filter_values = dataset.compute_variables([dataset_filter], dataset_pool=self.dataset_pool)
            index = where(filter_values > filter_threshold)[0]
        else:
            index = None
        return (spec, index)
    
    def get_data_as_dataset(self, submodel=-2):
        """Like get_all_data, but the returning value is a Dataset containing attributes that
        correspond to the data columns. Their names are coefficient names."""
        all_data = self.get_all_data(submodel)
        if all_data is None:
            return None
        names = self.coefficient_names_all[submodel]
        if names is None:
            return None
        dataset_data = {}
        for i in range(names.size):
            dataset_data[names[i]] = all_data[:, i].reshape(all_data.shape[0])
        dataset_data["id"] = arange(all_data.shape[0])+1
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='dataset', table_data=dataset_data)
        ds = Dataset(in_storage=storage, id_name="id", in_table_name='dataset')
        return ds

    def get_agent_set(self):
        return self.dataset_pool.get_dataset(self.dataset_name)
    
    def get_agent_set_index(self):
        return self.observations_mapping["index"]
    
    def get_agent_set_index_for_submodel(self, submodel):
        return self.observations_mapping[submodel]
    
    def save_predicted_values_and_errors(self, specification, coefficients, dataset, outcome_variable, index=None, data_objects=None):
        if self.estimate_config.get('save_predicted_values_and_errors', False):
            logger.log_status('Computing predicted values and residuals.')
            original_values = dataset.get_attribute_by_index(outcome_variable, index)
            predicted_values = zeros(dataset.size(), dtype='float32')
            predicted_values[index] = self.run_after_estimation(specification, coefficients, dataset, index=index, data_objects=data_objects)
            predicted_attribute_name = 'predicted_%s' % outcome_variable.get_alias()
            dataset.add_primary_attribute(name=predicted_attribute_name, data=predicted_values)
            dataset.flush_attribute(predicted_attribute_name)
            predicted_error_attribute_name = 'residuals_%s' % outcome_variable.get_alias()
            error_values = zeros(dataset.size(), dtype='float32')
            error_values[index] = (original_values - predicted_values[index]).astype(error_values.dtype)
            dataset.add_primary_attribute(name=predicted_error_attribute_name, data = error_values)
            dataset.flush_attribute(predicted_error_attribute_name)
            logger.log_status('Predicted values saved as %s (for the %s dataset)' % (predicted_attribute_name, dataset.get_dataset_name()))
            logger.log_status('Residuals saved as %s (for the %s dataset)' % (predicted_error_attribute_name, dataset.get_dataset_name()))
        
    def export_estimation_data(self, submodel=-2, file_name='./estimation_data_regression.txt', delimiter = '\t'):
        import os
        from numpy import newaxis
        data = concatenate((self.outcome[submodel][...,newaxis], self.get_all_data(submodel=submodel)), axis=1)
        header = ['outcome'] + self.get_coefficient_names(submodel).tolist()
        nrows = data.shape[0]
        file_name_root, file_name_ext = os.path.splitext(file_name)
        out_file = "%s_submodel_%s.txt" % (file_name_root, submodel)
        fh = open(out_file,'w')
        fh.write(delimiter.join(header) + '\n')   #file header
        for row in range(nrows):
            line = [str(x) for x in data[row,]]
            fh.write(delimiter.join(line) + '\n')
        fh.flush()
        fh.close
        print 'Data written into %s' % out_file
        
    def run_after_estimation(self, *args, **kwargs):
        return self.run(*args, **kwargs)
            
    def _get_status_total_pieces(self):
        return ChunkModel._get_status_total_pieces(self) * self.get_status_for_gui().get_total_number_of_pieces()
    
    def _get_status_current_piece(self):
        return ChunkModel._get_status_current_piece(self)*self.get_status_for_gui().get_total_number_of_pieces() + self.get_status_for_gui().get_current_piece()
        
    def _get_status_piece_description(self):
        return "%s %s" % (ChunkModel._get_status_piece_description(self), self.get_status_for_gui().get_current_piece_description())
    
    def get_specified_coefficients(self):
        return self.specified_coefficients
    
from numpy import ma
from opus_core.tests import opus_unittest
from opus_core.equation_specification import EquationSpecification

class RegressionModelTests(opus_unittest.OpusTestCase):
    def test_estimation_without_procedure(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='dataset',
            table_data={
                "id":array([1,2,3,4]),
                "attr1":array([4,7,2,1]),
                "attr2":array([6.8,2.6,0,1]),
                "submodel_id": array([1,2,2,1]),
                "outcome": array([0,1,0,1])
                }
            )

        ds = Dataset(in_storage=storage, in_table_name='dataset', id_name="id")
        specification = EquationSpecification(
                          variables=array(["constant", "attr2", "attr1"]),
                          coefficients=array(["constant", "ba2", "ba1"]))

        model = RegressionModel()
        model.estimate(specification, ds, "outcome")
        data_attr1 = model.get_data("ba1")
        self.assert_(ma.allequal(ds.get_attribute("attr1"), data_attr1),
                     msg = "Error in getting data from regression model")

        specification_2subm = EquationSpecification(
                          variables=array(["constant", "attr2", "constant", "attr1"]),
                          coefficients=array(["constant", "ba2", "constant", "ba1"]),
                          submodels = array([1,1,2,2]))

        model = RegressionModel(submodel_string="submodel_id")
        model.estimate(specification_2subm, ds, "outcome")
        data_attr1 = model.get_data("ba1", 1)
        self.assert_(data_attr1 == None, msg = "Error in getting data from regression model with multiple submodels.")
        data_attr1 = model.get_data("ba1", 2)
        self.assert_(ma.allequal(ds.get_attribute("attr1")[1:3], data_attr1),
                     msg = "Error in getting data from regression model with multiple submodels.")
        d = model.get_data_as_dataset(2)
        self.assert_(ma.allequal(ds.get_attribute("attr1")[1:3], d.get_attribute("ba1")),
                     msg = "Error in getting data from regression model with multiple submodels.")

    def test_estimation_with_restricted_submodel_size(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='dataset',
            table_data={
                "id":array([1,2,3,4,5,6,7,8,9,10]),
                "attr1":array([4,7,2,1,5,4,5,3,2,1]),
                "attr2":array([6.8,2.6,0,1,0,4.3,2.1,6,8,7,]),
                "submodel_id": array([1,2,2,1,1,1,2,1,1,1]),
                "outcome": array([0,1,0,1,1,1,0,0,1,1])
                }
            )

        ds = Dataset(in_storage=storage, in_table_name='dataset', id_name="id")
        specification_2subm = EquationSpecification(
                          variables=array(["constant", "attr2", "constant", "attr1"]),
                          coefficients=array(["constant", "ba2", "constant", "ba1"]),
                          submodels = array([1,1,2,2]))

        model = RegressionModel(submodel_string="submodel_id", estimate_config={'submodel_size_max': 5})
        model.estimate(specification_2subm, ds, "outcome", procedure='opus_core.estimate_linear_regression')

        data_attr1 = model.get_data("ba1", 1)
        self.assert_(data_attr1 == None, msg = "Error in getting data from regression model with multiple submodels.")
        data_attr1 = model.get_data("ba2", 1)
        self.assert_(data_attr1.size == 5, msg = "Error in sub-sampling data in regression model.")
        data_attr1 = model.get_data("ba1", 2)
        self.assert_(ma.allequal(ds.get_attribute("attr1")[array([1, 2, 6])], data_attr1),
                     msg = "Error in getting data from regression model with multiple submodels.")


if __name__ == "__main__":
    opus_unittest.main()
