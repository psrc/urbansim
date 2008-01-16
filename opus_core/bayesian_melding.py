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
from numpy import ones, zeros, float32, array, arange, transpose, reshape, sort, maximum, mean, where, concatenate, round_
from scipy import ndimage
from opus_core.model_component_creator import ModelComponentCreator
from opus_core.misc import load_from_text_file, write_to_text_file, try_transformation, write_table_to_text_file, load_table_from_text_file
from opus_core.variables.variable_name import VariableName
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.datasets.dataset import DatasetSubset, Dataset
from opus_core.datasets.interaction_dataset import InteractionDataset
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.session_configuration import SessionConfiguration
from opus_core.storage_factory import StorageFactory
from opus_core.logger import logger

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
        return self.get_quantity_objects()[self.get_index_for_quantity(variable_name)].get_values()
                
    def get_quantity_object_by_index(self, index):
        return self.get_quantity_objects()[index]
        
    def get_quantity_object(self, variable_name):
        return self.get_quantity_objects()[self.get_index_for_quantity(variable_name)]
        
    def get_index_for_quantity(self, variable_name):
        alias = VariableName(variable_name).get_alias()
        for iq in range(len(self.get_quantity_objects())):
            q = self.get_quantity_objects()[iq]
            if q.get_variable_name().get_alias() == alias:
                return iq
                             
class ObservedDataOneQuantity:
    """  Class for storing information about one quantity measure. It is to be grouped in 
    an object of class ObservedData.
    """
    # pairs of inverse transformations
    transformation_pairs = {"sqrt": "**2", "log":"exp", "exp": "log", "**2": "sqrt"}

    def __init__(self, variable_name, observed_data, filename=None,  transformation=None, inverse_transformation=None, 
                 filter=None, match=False, dependent_datasets={}, **kwargs):
        """  'variable_name' is a quantity about which we have data available.
        'observed_data' is of type ObservedData, it is the grouping parent. 
        'filename' is the name of file where 
        the data is stored. It can be None, if the observed_data.directory is a cache.
        'transformation' is an operation to be performed on the data (e.g. sqrt, log),
        'inverse_transformation' is the inverse function of 'transformation'. If it not given, it
        is determined automatically.
        'filter' is a variable that will be applied to both, the observed data and the simulated data.
        'match' (logical) determines if the dataset should be matched (by ids) with the simulated dataset. Elements
        that don't match are eliminated from the simulated dataset.
        'dependent_datasets' (if any) should be a dictionary of dataset_name:{'filename': filename, 'match': True|False, **kwargs}. 
        They will be added to the dataset_pool. 
        Remaining arguments are passed into DatasetFactory, thus it can contain information about how 
        to create the corresponding dataset.
        """
        self.variable_name = VariableName(variable_name)
        self.dataset_name = self.variable_name.get_dataset_name()
        dataset_pool = observed_data.get_dataset_pool()
        self.matching_datasets = {}
        
        if dataset_pool is None:
            kwargs.update({'in_storage':observed_data.get_storage(), 'in_table_name': filename})
            try:
                self.dataset = DatasetFactory().search_for_dataset(self.dataset_name, observed_data.get_package_order(), arguments=kwargs)
            except: # take generic dataset
                self.dataset = Dataset(dataset_name=self.dataset_name, **kwargs)
        else:
            self.dataset = dataset_pool.get_dataset(self.dataset_name)
        if match:
            self.add_match(self.dataset)
        for dep_dataset_name, info in dependent_datasets.iteritems():
            if dataset_pool is None:
                dataset_pool = DatasetPool(storage=observed_data.get_storage(), package_order=observed_data.get_package_order())
            info.update({'in_storage':observed_data.get_storage(), 'in_table_name': info.get('filename')})
            del info['filename']
            match = False
            if 'match' in info.keys():
                match = info['match']
                del info['match']
            try:
                dep_dataset = DatasetFactory().search_for_dataset(dep_dataset_name, observed_data.get_package_order(), arguments=info)
            except:
                dep_dataset = Dataset(dataset_name=dep_dataset_name, **info)
            dataset_pool.replace_dataset(dep_dataset_name, dep_dataset)
            if match:
                self.add_match(dep_dataset)
            
        self.dataset.compute_variables([self.variable_name], dataset_pool=dataset_pool)
        if filter is not None:
            filter_values = self.dataset.compute_variables([filter], dataset_pool=dataset_pool)
            idx = where(filter_values > 0)[0]
            self.add_match(self.dataset, idx)
            self.dataset.subset_by_index(idx)
        self.transformation = transformation
        self.inverse_transformation = inverse_transformation
        if (self.transformation is not None) and (self.inverse_transformation is None):
            self.inverse_transformation = self.transformation_pairs[self.transformation]
                
    def get_values(self):
        return self.dataset.get_attribute(self.variable_name)
        
    def get_transformed_values(self):
        return try_transformation(self.get_values(), self.transformation)
        
    def get_variable_name(self):
        return self.variable_name
    
    def get_dataset(self):
        return self.dataset
    
    def get_dataset_name(self):
        return self.dataset_name
    
    def get_transformation(self):
        return self.transformation
    
    def get_transformation_pair(self):
        return (self.transformation, self.inverse_transformation)
    
    def add_match(self, dataset, index = None):
        dataset_name = dataset.get_dataset_name()
        result = zeros(dataset.size(), dtype='bool8')
        idx = index
        if index is None:
            idx = arange(dataset.size())
        result[idx] = 1
        if dataset_name in self.matching_datasets.keys():
            tmp = zeros(dataset.size(), dtype='bool8')
            tmp[dataset.get_id_index(self.matching_datasets[dataset_name])]=1
            result = result*tmp
        self.matching_datasets[dataset_name] = dataset.get_id_attribute()[where(result)]
        
    def get_matching_datasets(self):
        return self.matching_datasets
        
class BayesianMelding:

    caches_file_name = "cache_directories"
    weights_file_name = "weights"
    variance_file_name = "variance"
    bias_file_name = "bias"
    
    def __init__(self, cache_directory, observed_data,
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
        self.base_year = base_year
        self.propagation_factor = None
        self.y = {}
        self.mu = {}
        self.ahat = {}
        self.v = {}
        self.weight_components = {}
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
            self.y[iout] = quantity.get_transformed_values()

    def compute_scalings(self):
        for dir in self.scaling_parent_datasets.keys():
            dataset_pool = self.setup_environment(dir, self.base_year)
            self.scaling_parent_datasets[dir] = self.get_datasets(dataset_pool)
            for variable in self.known_output:
                dataset = variable.get_dataset_name()
                self.scaling_parent_datasets[dir][dataset].compute_variables(variable, dataset_pool=dataset_pool)

        for run in self.scaling_child_datasets.keys():
            dataset_pool = self.setup_environment(self.cache_set[run-1], self.base_year)
            self.scaling_child_datasets[run] = self.get_datasets(dataset_pool)
            for variable in self.known_output:
                dataset = variable.get_dataset_name()
                self.scaling_child_datasets[run][dataset].compute_variables(variable, dataset_pool=dataset_pool)

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
            self.weights, self.weight_components = procedure_class.run(self, **kwargs)
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
                ds = self._compute_variable(i, variable, dataset_name, self.observed_data.get_year(), quantity)
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
                self.mu[iout][:,i] = try_transformation(values, quantity.get_transformation())
                
            if dimension_reduced:
                self.y[iout] = self.y[iout][quantity.get_dataset().get_id_index(ids)]

    def _compute_variable(self, run_index, variable, dataset_name, year, quantity):
        dataset_pool = setup_environment(self.cache_set[run_index], year, self.package_order)
        for mds_name, ids in quantity.get_matching_datasets().iteritems():
            mds = dataset_pool.get_dataset(mds_name)
            mds.subset_by_ids(ids, flush_attributes_if_not_loaded=False)
        ds = dataset_pool.get_dataset(dataset_name)
        ds.compute_variables(variable, dataset_pool=dataset_pool)            
        return ds
    
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
            # for zone-specific bias
            #self.ahat[l] = mean(reshape(self.y[l], (self.y[l].size,1)) - self.mu[l], axis=1)
            if l > 0:
                mode="ab" # add to existing file
            write_to_text_file(os.path.join(self.cache_directory, self.bias_file_name),
                           array([self.ahat[l]]), mode=mode)
                           # for zone-specific bias
                           #self.ahat[l], mode=mode, delimiter=" ")

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

    def get_expected_values_by_index(self, index, transformed_back=True):
        transformation, inverse_transformation = self.observed_data.get_quantity_object_by_index(index).get_transformation_pair()
        if transformed_back and (transformation is not None):
            return try_transformation(self.mu[index], inverse_transformation)
        return self.mu[index]
        
    def get_observed_data_by_index(self, index, transformed_back=True):
        transformation, inverse_transformation = self.observed_data.get_quantity_object_by_index(index).get_transformation_pair()
        if transformed_back and (transformation is not None):
            return try_transformation(self.y[index], inverse_transformation)
        return self.y[index]
    
    def get_bias(self):
        return self.ahat

    def get_bias_for_quantity(self):
        return self.ahat[self.use_bias_and_variance_index]

    def get_data_for_quantity(self, transformed_back=True):
        transformation, inverse_transformation = self.observed_data.get_quantity_object_by_index(self.use_bias_and_variance_index).get_transformation_pair()
        if transformed_back and (transformation is not None):
            return try_transformation(self.y[self.use_bias_and_variance_index], inverse_transformation)
        return self.y[self.use_bias_and_variance_index]

    def get_data(self):
        return self.y

    def get_variance(self):
        return self.v

    def get_variance_for_quantity(self):
        return self.v[self.use_bias_and_variance_index]

    def get_weight_components(self):
        return self.weight_components
    
    def set_propagation_factor(self, year):
        self.propagation_factor = (year - self.base_year)/float(self.observed_data.get_year() - self.base_year)

    def get_propagation_factor(self):
        return self.propagation_factor

    def get_predicted_values(self, transformed_back=False):
        if transformed_back and (self.transformation_pair_for_prediction[0] is not None):
            return try_transformation(self.m, self.transformation_pair_for_prediction[1])
        return self.m

    def get_weights(self):
        return self.weights

    def compute_m(self, year, quantity_of_interest):
        variable_name = VariableName(quantity_of_interest)
        dataset_name = variable_name.get_dataset_name()
        for i in range(self.number_of_runs):
            ds = self._compute_variable(i, variable_name, dataset_name, year, self.observed_data.get_quantity_object(quantity_of_interest))
            if i == 0: # first run
                self.m = zeros((ds.size(), self.number_of_runs), dtype=float32)
                self.m_ids = ds.get_id_attribute()
            self.m[:, i] = try_transformation(ds.get_attribute(variable_name), self.transformation_pair_for_prediction[0])


    def get_posterior_component_mean(self):
        return self.get_bias_for_quantity()*self.get_propagation_factor() + self.get_predicted_values()
        # for zone-specific bias
        #bias = self.get_bias_for_quantity()
        #return reshape(bias, (bias.size, 1)) + self.get_predicted_values()

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
        # for zone-specific bias
        #for l in range(bias.shape[0]):
            #ahat[l] = bias[l,:]
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
                                        use_bias_and_variance_from=None, transformed_back=True, **kwargs):
        """
        'quantity_of_interest' is a varible name about which we want to get the posterior distribution.
        If there is multiple known_output, it must be made clear from which one the bias and variance
        is to be used (argument use_bias_and_variance_from) If it is None, the first known output is used.
        """
        self.set_posterior(year, quantity_of_interest, use_bias_and_variance_from)
        procedure_class = ModelComponentCreator().get_model_component(procedure)
        self.simulated_values = procedure_class.run(self, **kwargs)
        if transformed_back and (self.transformation_pair_for_prediction[0] is not None): # need to transform back
            self.simulated_values = try_transformation(self.simulated_values,
                                                       self.transformation_pair_for_prediction[1])
        return self.simulated_values

    def set_posterior(self, year, quantity_of_interest, use_bias_and_variance_from=None):
        self.set_propagation_factor(year)
        self.weights = self.get_weights_from_file()
        self.ahat, self.v = self.get_bias_and_variance_from_files()

        if use_bias_and_variance_from is None:
            use_bias_and_variance_from = quantity_of_interest
        variable_list = map(lambda x: x.get_expression(), self.observed_data.get_variable_names())
        if use_bias_and_variance_from not in variable_list:
            raise ValueError, "Quantity %s is not among observed data." % use_bias_and_variance_from
        self.use_bias_and_variance_index = variable_list.index(use_bias_and_variance_from)
        self.transformation_pair_for_prediction = self.observed_data.get_quantity_object_by_index(self.use_bias_and_variance_index).get_transformation_pair()
        self.compute_m(year, quantity_of_interest)
        
    def write_simulated_values(self, filename):
        write_table_to_text_file(filename, self.simulated_values)
        
    def write_expected_values(self, filename, index, transformed_back=True):
        write_table_to_text_file(filename, self.get_expected_values_by_index(index, transformed_back))

    def write_observed_data(self, filename, index, transformed_back=True):
        write_to_text_file(filename, self.get_observed_data_by_index(index, transformed_back), delimiter=' ')
        
    def write_values_from_multiple_runs(self, filename, transformed_back=True):
        write_table_to_text_file(filename, self.get_predicted_values(transformed_back=transformed_back))

    def write_observed_data_for_quantity(self, quantity_of_interest, filename):
        data = self.observed_data.get_values_for_quantity(quantity_of_interest)
        write_to_text_file(filename, data, delimiter=' ')
        
    def write_posterior_mean_and_variance(self, mean_filename=None, variance_filename=None):
        if mean_filename is not None:
            write_table_to_text_file(mean_filename, self.get_posterior_component_mean())
        if variance_filename is not None:
            write_to_text_file(variance_filename, self.get_posterior_component_variance(), delimiter=' ')
            
    def export_weights_posterior_mean_and_variance(self, years, quantity_of_interest, directory, filename=None, 
                                                     use_bias_and_variance_from=None, ids = None):
        for year in years:
            self.set_posterior(year, quantity_of_interest, use_bias_and_variance_from)
            if filename is None:
                filename = quantity_of_interest
            file = os.path.join(directory, str(year) + '_' + filename)
            write_to_text_file(file, concatenate((array([0.]), self.get_weights())), delimiter=' ')
            write_to_text_file(file, concatenate((array([0.]), self.get_posterior_component_variance())), mode='a', delimiter=' ')
            variable_list = map(lambda x: x.get_expression(), self.observed_data.get_variable_names())
            quantity_index = variable_list.index(quantity_of_interest)
            if ids is None:
                ids = self.m_ids
            means = zeros((ids.size, self.number_of_runs+1))
            means[:,0] = ids
            means[self.observed_data.get_quantity_objects()[quantity_index].get_dataset().get_id_index(ids),1:means.shape[1]] = self.get_posterior_component_mean()
            write_table_to_text_file(file, means, mode='a')            

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
        
    def get_m_ids(self):
        return self.m_ids
    
def setup_environment(cache_directory, year, package_order):
    ss = SimulationState(new_instance=True)
    ss.set_cache_directory(cache_directory)
    ss.set_current_time(year)
    ac = AttributeCache()
    storage = ac.get_flt_storage_for_year(year)
    sc = SessionConfiguration(new_instance=True,
                         package_order=package_order,
                         in_storage=ac)
    logger.log_status("Setup environment for year %s. Use cache directory %s." % (year, storage.get_storage_location()))
    return sc.get_dataset_pool()


class BayesianMeldingFromFile(BayesianMelding):
    """ Class to be used if weights, means and variances were stored previously using export_weights_posterior_mean_and_variance of BayesianMelding class.
        It can be passed into bm_normal_posterior.py.
    """
    def __init__(self, filename):
        """The file 'filename' must have weights in first line, variances in second line and rest are the means. 
        """
        table = load_table_from_text_file(filename, convert_to_float=True)[0]
        self.weights = table[0,1:table.shape[1]]
        self.variance = table[1,1:table.shape[1]]
        self.means = table[2:table.shape[0],1:table.shape[1]]
        self.m_ids = round_(table[2:table.shape[0],0])
        
    def get_posterior_component_mean(self):
        return self.means
    
    def get_posterior_component_variance(self):
        return self.variance
    