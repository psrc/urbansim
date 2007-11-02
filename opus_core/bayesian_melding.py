#
# Opus software. Copyright (C) 1998-2007 University of Washington
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

# This is under construction !!!

import os
from numpy import ones, zeros, float32, array, arange, transpose, reshape, sort, maximum
from scipy import ndimage
from opus_core.model_component_creator import ModelComponentCreator
from opus_core.misc import load_from_text_file, write_to_text_file, try_transformation, write_table_to_text_file
from opus_core.variables.variable_name import VariableName
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.datasets.dataset import DatasetSubset, Dataset
from opus_core.datasets.interaction_dataset import InteractionDataset
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.resources import Resources
from opus_core.session_configuration import SessionConfiguration
from opus_core.storage_factory import StorageFactory

class ObservedData:
    def __init__(self, directory, year, storage_type='tab_storage', is_cache=False, package_order=['core']):
        """'directory' is a directory, where the observed data are stored.
        The type of those data is given in 'storage_type'. If it is opus cache, 
        set it to 'flt_storage' and set the argument 'is_cache' to True.
        'package_order' gives the order of packages for creating the necessary datasets.
        'year' is the year from which we have the observed data.
        
        The class keeps a list of objects of type ObservedDataOneQuantity in self.observed_data_collection, 
        each of which stores information about one quantity measure. Use the method 'add_quantity' to create
        this list.
        """
        self.year = year
        self.dataset_pool = None
        self.storage = None
        self.package_order = package_order
        
        if is_cache:
            self.dataset_pool = setup_environment(directory, self.year, package_order)
        else:
            self.storage = StorageFactory().get_storage(storage_type, storage_location=directory)
            
        self.observed_data_collection = []
 
    def get_storage(self):
        return self.storage
    
    def get_dataset_pool(self):
        return self.dataset_pool
    
    def get_package_order(self):
        return self.package_order
    
    def add_quantity(self, variable_name, filename, **kwargs):
        self.observed_data_collection.append(ObservedDataOneQuantity(variable_name, self, filename, **kwargs))
        
    def get_variable_names(self):
        return map(lambda x: x.get_variable_name(), self.get_quantity_objects())
        
    def get_quantity_objects(self):
        return self.observed_data_collection
    
    def get_year(self):
        return self.year
    
    def get_values_for_quantity(variable_name):
        alias = VariableName(variable_name).get_alias()
        for q in self.get_quantity_objects():
            if q.get_variable_name().get_alias() == alias:
                return q.get_values()
                
class ObservedDataOneQuantity:
    """  Class for storing information about one quantity measure. It is to be grouped in 
    an object of class ObservedData.
    """
    def __init__(self, variable_name, observed_data, filename=None,  **kwargs):
        """  'variable_name' is a quantity about which we have data available.
        'observed_data' is of type ObservedData, it is the grouping parent. 
        'filename' is the name of file where 
        the data is stored. It can be None, if the observed_data.directory is a cache.
        Remaining arguments are passed into DatasetFactory, thus it can contain information about how 
        to create the corresponding dataset.
        """
        self.variable_name = VariableName(variable_name)
        self.dataset_name = self.variable_name.get_dataset_name()
        dataset_pool = observed_data.get_dataset_pool()
        if dataset_pool is None:
            kwargs.update({'in_storage':observed_data.get_storage(), 'in_table_name': filename})
            try:
                self.dataset = DatasetFactory().search_for_dataset(self.dataset_name, observed_data.get_package_order(), arguments=kwargs)
            except: # take generic dataset
                self.dataset = Dataset(dataset_name=self.dataset_name, **kwargs)
        else:
            self.dataset = dataset_pool.get_dataset(self.dataset_name)
        self.dataset.compute_variables([self.variable_name], dataset_pool=dataset_pool)
                
    def get_values(self):
        return self.dataset.get_attribute(self.variable_name)
        
    def get_variable_name(self):
        return self.variable_name
    
    def get_dataset(self):
        return self.dataset
    
    def get_dataset_name(self):
        return self.dataset_name
        
class BayesianMelding:

    caches_file_name = "cache_directories"
    weights_file_name = "weights"
    variance_file_name = "variance"
    bias_file_name = "bias"
    # pairs of inverse transformations
    transformation_pairs = {"sqrt": "**2", "log":"exp", "exp": "log", "**2": "sqrt"}

    def __init__(self, cache_directory, observed_data, transformation=None, inverse_transformation=None,
                 base_year=0, scaling_parents={}, package_order=['core']):
        """ Class used in the Bayesian melding analysis.
        'cache_directory' is the first directory created by start_run_set.py. It should
        contain a file called 'cache_directories' which contains a list of all caches that
        belong to this set of runs. This list is read and stored in self.cache_set.
        'observed_data' is an object of ObservedData that contains all the information about observed data.
        """
        file = os.path.join(cache_directory, self.caches_file_name)
        if not os.path.exists(file):
            raise StandardError, "Directory %s must contain a file '%s'." % (cache_directory,
                                                                             self.caches_file_name)
        self.cache_directory = cache_directory
        self.cache_set = load_from_text_file(file) # it is an array
        self.number_of_runs = self.cache_set.size
        self.observed_data = observed_data
        self.package_order = package_order
        self.transformation = transformation
        if inverse_transformation is not None:
            self.transformation_pairs[self.transformation] = inverse_transformation
        self.base_year = base_year
        self.propagation_factor = None
        self.y = {}
        self.mu = {}
        self.ahat = {}
        self.v = {}
        self.simulated_values = None
        self.scaling_parents = scaling_parents
        self.scaling_parent_datasets = {}
        self.scaling_child_datasets = {}
        for run, dir in self.scaling_parents.iteritems():
            if dir not in self.scaling_parent_datasets.keys():
                self.scaling_parent_datasets[dir] = {}
            self.scaling_child_datasets[run] = {}

    def get_datasets(self, dataset_pool):
        result = {}
        for dataset in self.datasets_to_create:
            result[dataset] = dataset_pool.get_dataset(dataset)
        return result
    
    def compute_y(self):
        iout = -1
        for quantity in self.observed_data.get_quantity_objects():
            iout += 1
            self.y[iout] = try_transformation(quantity.get_values(), self.transformation)

    def compute_scalings(self):
        for dir in self.scaling_parent_datasets.keys():
            dataset_pool = self.setup_environment(dir, self.base_year)
            self.scaling_parent_datasets[dir] = self.get_datasets(dataset_pool)
            for variable in self.known_output:
                dataset = variable.get_dataset_name()
                self.scaling_parent_datasets[dir][dataset].compute_variables(variable, resources=Resources(self.scaling_parent_datasets[dir]))

        for run in self.scaling_child_datasets.keys():
            dataset_pool = self.setup_environment(self.cache_set[run-1], self.base_year)
            self.scaling_child_datasets[run] = self.get_datasets(dataset_pool)
            for variable in self.known_output:
                dataset = variable.get_dataset_name()
                self.scaling_child_datasets[run][dataset].compute_variables(variable, resources=Resources(self.scaling_child_datasets[run]))

    def compute_weights(self, procedure="opus_core.bm_normal_weights", **kwargs):
        """ Launches the run method of the given 'procedure'. This should return the actual BM weights.
        The method passes self as first argument into the run method.
        If 'procedure' is not given, the method returns equal weights.
        The result is written into file called 'weights' into the cache directory
        given in the init method.
        """
        self.compute_y()
        self.compute_scalings()
        self.estimate_mu()
        self.estimate_bias()
        self.estimate_variance()
        if procedure is not None:
            procedure_class = ModelComponentCreator().get_model_component(procedure)
            self.weights = procedure_class.run(self, **kwargs)
        else:
            self.weights = 1.0/self.number_of_runs * ones(self.number_of_runs)
        write_to_text_file(os.path.join(self.cache_directory, self.weights_file_name),
                           self.weights)
        return self.weights

    def estimate_mu(self):
        iout = -1
        for quantity in self.observed_data.get_quantity_objects():
            dataset_name = quantity.get_dataset_name()
            variable = quantity.get_variable_name()
            iout += 1
            dimension_reduced = False
            quantity_ids = quantity.get_dataset().get_id_attribute()
            for i in range(self.number_of_runs):
                dataset_pool = setup_environment(self.cache_set[i], self.observed_data.get_year(), self.package_order)
                ds = dataset_pool.get_dataset(dataset_name)
                ds.compute_variables(variable, dataset_pool=dataset_pool)
                if isinstance(ds, InteractionDataset):
                    ds = ds.get_flatten_dataset()
                if i == 0: # first run
                    self.mu[iout] = zeros((self.y[iout].size, self.number_of_runs), dtype=float32)
                    ids = ds.get_id_attribute()
                else:
                    if ds.size() > ids.shape[0]:
                        ds = DatasetSubset(ds, ds.get_id_index(ids))
                        dimension_reduced = True
                scale = self.get_scales(ds, i+1, variable)
                matching_index = ds.get_id_index(quantity_ids)
                values = scale[matching_index] * ds.get_attribute(variable)[matching_index]
                self.mu[iout][:,i] = try_transformation(values, self.transformation)
                
            if dimension_reduced:
                self.y[iout] = self.y[iout][quantity.get_dataset().get_id_index(ids)]

    def get_scales(self, dataset, run, variable):
        if run in self.scaling_parents.keys():
            dataset_name = dataset.get_dataset_name()
            scaling_parent_ds = self.scaling_parent_datasets[self.scaling_parents[run]][dataset_name]
            parent_values = scaling_parent_ds.get_attribute_by_index(variable, scaling_parent_ds.get_id_index(dataset.get_id_attribute()))
            child_values = self.scaling_child_datasets[run][dataset_name].get_attribute(variable)
            return parent_values/maximum(1.0,child_values.astype(float32))
        return ones(dataset.size(), dtype="int32")

    def estimate_bias(self):
        mode="wb"
        for l in self.mu.keys():
            self.ahat[l] = (reshape(self.y[l], (self.y[l].size,1)) - self.mu[l]).mean()
            if l > 0:
                mode="ab" # add to existing file
            write_to_text_file(os.path.join(self.cache_directory, self.bias_file_name),
                           array([self.ahat[l]]), mode=mode)

    def estimate_variance(self):
        mode="wb"
        for l in self.mu.keys():
            self.v[l] = zeros(self.number_of_runs, dtype=float32)
            for i in range(self.number_of_runs):
                self.v[l][i] = ((self.y[l] - self.ahat[l] - self.mu[l][:,i])**2.0).mean()
            if l > 0:
                mode="ab" # add to existing file
            write_to_text_file(os.path.join(self.cache_directory, self.variance_file_name),
                           self.v[l], mode=mode, delimiter=" ")

    def get_expected_values(self):
        return self.mu

    def get_bias(self):
        return self.ahat

    def get_bias_for_quantity(self):
        return self.ahat[self.use_bias_and_variance_index]

    def get_data_for_quantity(self, transformed_back=True):
        if transformed_back and (self.transformation is not None):
            return try_transformation(self.y[self.use_bias_and_variance_index], self.transformation_pairs[self.transformation])
        return self.y[self.use_bias_and_variance_index]

    def get_data(self):
        return self.y

    def get_variance(self):
        return self.v

    def get_variance_for_quantity(self):
        return self.v[self.use_bias_and_variance_index]

    def set_propagation_factor(self, year):
        self.propagation_factor = (year - self.base_year)/float(self.observed_data.get_year() - self.base_year)

    def get_propagation_factor(self):
        return self.propagation_factor

    def get_predicted_values(self, transformed_back=False):
        if transformed_back and (self.transformation is not None):
            return try_transformation(self.m, self.transformation_pairs[self.transformation])
        return self.m

    def get_weights(self):
        return self.weights

    def compute_m(self, year, quantity_of_interest):
        variable_name = VariableName(quantity_of_interest)
        dataset_name = variable_name.get_dataset_name()
        for i in range(self.number_of_runs):
            dataset_pool = setup_environment(self.cache_set[i], year, self.package_order)
            ds = dataset_pool.get_dataset(dataset_name)
            ds.compute_variables(variable_name)
            if i == 0: # first run
                self.m = zeros((ds.size(), self.number_of_runs), dtype=float32)
            self.m[:, i] = try_transformation(ds.get_attribute(variable_name), self.transformation)


    def get_posterior_component_mean(self):
        return self.get_bias_for_quantity()*self.get_propagation_factor() + self.get_predicted_values()

    def get_posterior_component_variance(self):
        return self.get_variance_for_quantity()*self.get_propagation_factor()

    def get_bias_and_variance_from_files(self):
        bias = array(load_from_text_file(
                         os.path.join(self.cache_directory, self.bias_file_name),
                                                 convert_to_float=True))
        variance = array(load_from_text_file(
                                 os.path.join(self.cache_directory, self.variance_file_name),
                                                 convert_to_float=True))
        ahat={}
        v = {}
        for l in range(bias.size):
            ahat[l] = bias[l]
            v[l] = variance[l,:]
        return (ahat, v)

    def get_weights_from_file(self):
        file = os.path.join(self.cache_directory, self.weights_file_name)
        if not os.path.exists(file):
            raise StandardError, "Directory %s must contain a file '%s'. Use method 'compute_weights'." % (self.cache_directory,
                                                                             self.weights_file_name)
        return array(load_from_text_file(file, convert_to_float=True))

    def generate_posterior_distribution(self, year, quantity_of_interest, procedure="opus_core.bm_normal_posterior",
                                        use_bias_and_variance_from=None, **kwargs):
        """
        'quantity_of_interest' is a varible name about which we want to get the posterior distribution.
        If there is multiple known_output, it must be made clear from which one the bias and variance
        is to be used (argument use_bias_and_variance_from) If it is None, the first known output is used.
        """
        self.set_propagation_factor(year)
        self.weights = self.get_weights_from_file()
        self.ahat, self.v = self.get_bias_and_variance_from_files()

        if use_bias_and_variance_from is None:
            use_bias_and_variance_from = quantity_of_interest
        variable_list = map(lambda x: x.get_expression(), self.observed_data.get_variable_names())
        if use_bias_and_variance_from not in variable_list:
            raise ValueError, "Quantity %s is not among observed data." % use_bias_and_variance_from
        self.use_bias_and_variance_index = variable_list.index(use_bias_and_variance_from)

        self.compute_m(year, quantity_of_interest)
        procedure_class = ModelComponentCreator().get_model_component(procedure)
        self.simulated_values = procedure_class.run(self, **kwargs)
        if self.transformation is not None: # need to transform back
            self.simulated_values = try_transformation(self.simulated_values,
                                                       self.transformation_pairs[self.transformation])
        return self.simulated_values

    def write_simulated_values(self, filename):
        write_table_to_text_file(filename, self.simulated_values)

    def write_values_from_multiple_runs(self, filename, transformed_back=True):
        write_table_to_text_file(filename, self.get_predicted_values(transformed_back=transformed_back))

    def write_observed_data_for_quantity(self, quantity_of_interest, filename):
        data = self.observed_data.get_values_for_quantity(quantity_of_interest)
        write_to_text_file(filename, data, delimiter=' ')

    def get_quantity_from_simulated_values(self, function):
        """'function' is a character string specifying a function of the scipy.ndimage package (e.g. mean,
        standard_deviation, variance).
        This function is applied to the simulated values (per dimension).
        """
        labels = self._get_label_of_simulated_values()
        return eval("array(ndimage.%s(self.simulated_values, labels=labels, index=arange(labels.shape[0])+1))" %
                    function)

    def _get_label_of_simulated_values(self):
        self._check_simulated_values()
        return transpose(reshape(array(self.simulated_values.shape[1]*range(self.simulated_values.shape[0])),
                              (self.simulated_values.shape[1], self.simulated_values.shape[0])) + 1)

    def _check_simulated_values(self):
        if self.simulated_values is None:
            raise StandardError, "Values were not simulated yet. Use method 'generate_posterior_distribution'."

    def get_probability_interval(self, probability):
        """Returns an array with two rows. First row contains the mins, the second row contains the max values
        that correspond to the given probability interval.
        """
        self._check_simulated_values()
        sorted_values = sort(self.simulated_values, axis=1)
        tmp = (1-probability)/2.0
        n = sorted_values.shape[1]
        minvalues = sorted_values[:, int(n * tmp)]
        maxvalues = sorted_values[:, int(n * (1-tmp))]
        return array([minvalues, maxvalues])
        
def setup_environment(cache_directory, year, package_order):
    ss = SimulationState(new_instance=True)
    ss.set_cache_directory(cache_directory)
    ss.set_current_time(year)
    ac = AttributeCache()
    storage = ac.get_flt_storage_for_year(year)
    sc = SessionConfiguration(new_instance=True,
                         package_order=package_order,
                         in_storage=ac)
    return sc.get_dataset_pool()