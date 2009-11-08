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

from opus_core.misc import DebugPrinter
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
from opus_core.logger import logger
from numpy import arange, zeros, float32, ndarray, array
from time import time

class RegressionModel(ChunkModel):

    model_name = "Regression Model"
    model_short_name = "RM"

    def __init__(self, model_configuration=None, regression_procedure="opus_core.linear_regression",
                  submodel_string=None,
                  run_config=None, estimate_config=None, debuglevel=None, dataset_pool=None):
        dl = debuglevel
        if debuglevel is None and model_configuration is not None and 'debuglevel' in model_configuration:
            dl = self.model_configuration["debuglevel"] # which attribute determines submodels
        self.debug = DebugPrinter(dl)

        self.dataset_pool = self.create_dataset_pool(dataset_pool)

        rp = regression_procedure
        if regression_procedure is None and model_configuration is not None and 'regression_procedure' in model_configuration:
            rp = self.model_configuration["regression_procedure"] # which attribute determines submodels
        self.regression = RegressionModelFactory().get_model(name=rp)
        if self.regression == None:
            raise StandardError, "No regression procedure given."

        self.submodel_string = submodel_string
        if submodel_string is None and model_configuration is not None and 'submodel_string' in model_configuration:
            self.submodel_string = self.model_configuration["submodel_string"] # which attribute determines submodels

        self.run_config = run_config
        if run_config is None and model_configuration is not None and 'run_config' in model_configuration:
            self.run_config = self.model_configuration["run_config"]
        if self.run_config == None:
            self.run_config = Resources()

        self.estimate_config = estimate_config
        if estimate_config is None and model_configuration is not None and 'estimate_config' in model_configuration:
            self.estimate_config = self.model_configuration["estimate_config"]
        if self.estimate_config == None:
            self.estimate_config = Resources()
        self.data = {}
        self.coefficient_names = {}

    def run(self, specification, coefficients, dataset, index=None, chunk_specification=None,
            data_objects=None, run_config=None, debuglevel=0):
        """'specification' is of type EquationSpecification,
            'coefficients' is of type Coefficients,
            'dataset' is of type Dataset,
            'index' are indices of individuals in dataset for which
                        the model runs. If it is None, the whole dataset is considered.
            'chunk_specification' determines  number of chunks in which the simulation is processed.
            'data_objects' is a dictionary where each key is the name of an data object
            ('zone', ...) and its value is an object of class  Dataset.
           'run_config' is of type Resources, it gives additional arguments for the run.
            'debuglevel' overwrites the constructor 'debuglevel'.
        """
        self.debug.flag = debuglevel
        if run_config == None:
            run_config = Resources()
        self.run_config = run_config.merge_with_defaults(self.run_config)
        self.run_config.merge({"debug":self.debug})
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        if dataset.size()<=0: # no data loaded yet
            dataset.get_id_attribute()
        if index == None:
            index = arange(dataset.size())
        result = ChunkModel.run(self, chunk_specification, dataset, index, float32,
                                 specification=specification, coefficients=coefficients)
        return result

    def run_chunk (self, index, dataset, specification, coefficients):
        specified_coefficients = SpecifiedCoefficients().create(coefficients, specification, neqs=1)
        compute_resources = Resources({"debug":self.debug})
        submodels = specified_coefficients.get_submodels()
        self.map_agents_to_submodels(submodels, self.submodel_string, dataset, index,
                                      dataset_pool=self.dataset_pool, resources = compute_resources)
        variables = specified_coefficients.get_full_variable_names_without_constants()
        self.debug.print_debug("Compute variables ...",4)
        dataset.compute_variables(variables, dataset_pool = self.dataset_pool, resources = compute_resources)

        data = {}
        coef = {}
        outcome=zeros((index.size,), dtype=float32)
        for submodel in submodels:
            coef[submodel] = SpecifiedCoefficientsFor1Submodel(specified_coefficients,submodel)
            self.debug.print_debug("Compute regression for submodel " +str(submodel),4)
            data[submodel] = dataset.create_regression_data(coef[submodel],
                                                                index = index[self.observations_mapping[submodel]])
            if (data[submodel].shape[0] > 0) and (data[submodel].size > 0): # observations for this submodel available
                outcome[self.observations_mapping[submodel]] = \
                    self.regression.run(data[submodel], coef[submodel].get_coefficient_values()[0,:],
                        resources=self.run_config).astype(float32)
        return outcome

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
        if estimate_config == None:
            estimate_config = Resources()
        self.estimate_config = estimate_config.merge_with_defaults(self.estimate_config)
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        self.procedure=procedure
        if self.procedure == None:
            self.procedure = self.estimate_config.get("estimation", None)
        if self.procedure is not None:
            self.procedure = ModelComponentCreator().get_model_component(self.procedure)
        else:
            logger.log_warning("No estimation procedure given, or problems with loading the corresponding module.")

        compute_resources = Resources({"debug":self.debug})
        if dataset.size()<=0: # no data loaded yet
            dataset.get_id_attribute()
        if index == None:
            index = arange(dataset.size())
        if not isinstance(index,ndarray):
            index=array(index)

        estimation_size_agents = self.estimate_config.get("estimation_size_agents", None) # should be a proportion of the agent_set
        if estimation_size_agents == None:
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
        specified_coefficients = SpecifiedCoefficients().create(coefficients, specification, neqs=1)
        submodels = specified_coefficients.get_submodels()
        self.map_agents_to_submodels(submodels, self.submodel_string, dataset, estimation_idx,
                                      dataset_pool=self.dataset_pool, resources = compute_resources)
        variables = specified_coefficients.get_full_variable_names_without_constants()
        self.debug.print_debug("Compute variables ...",4)
        dataset.compute_variables(variables, dataset_pool=self.dataset_pool, resources = compute_resources)

        coef = {}
        estimated_coef={}
        dataset.compute_variables([outcome_attribute], dataset_pool=self.dataset_pool, resources=compute_resources)
        regression_resources=Resources(estimate_config)
        regression_resources.merge({"debug":self.debug})
        outcome_variable_name = VariableName(outcome_attribute)
        for submodel in submodels:
            coef[submodel] = SpecifiedCoefficientsFor1Submodel(specified_coefficients,submodel)
            logger.log_status("Estimate regression for submodel " +str(submodel),
                               tags=["estimate"], verbosity_level=2)
            logger.log_status("Number of observations: " +str(self.observations_mapping[submodel].size),
                               tags=["estimate"], verbosity_level=2)
            self.data[submodel] = dataset.create_regression_data_for_estimation(coef[submodel],
                                                            index = estimation_idx[self.observations_mapping[submodel]])
            self.coefficient_names[submodel] = coef[submodel].get_coefficient_names_without_constant()[0,:]
            if (self.data[submodel].shape[0] > 0) and (self.data[submodel].size > 0) and (self.procedure is not None): # observations for this submodel available
                regression_resources.merge({"outcome":
                    dataset.get_attribute_by_index(
                        outcome_variable_name.get_alias(), estimation_idx[self.observations_mapping[submodel]])})
                regression_resources.merge({"coefficient_names":self.coefficient_names[submodel].tolist(),
                            "constant_position": coef[submodel].get_constants_positions()})
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
        return (coefficients, estimated_coef)

    def prepare_for_run(self, *args, **kwargs):
        from opus_core.choice_model import prepare_specification_and_coefficients
        return prepare_specification_and_coefficients(*args, **kwargs)

    def get_data_as_dataset(self, submodel=-2):
        """Like get_all_data, but the retuning value is a Dataset containing attributes that
        correspond to the data columns. Their names are coefficient names."""
        all_data = self.get_all_data(submodel)
        if all_data is None:
            return None
        names = self.get_coefficient_names(submodel)
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


if __name__ == "__main__":
    opus_unittest.main()