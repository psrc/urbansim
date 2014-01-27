# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# This is under construction !!!

import os
import gc
from numpy import ones, zeros, float32, array, arange, transpose, reshape, sort, maximum, mean, where, concatenate
from numpy import round_, argsort, resize, average, ndarray, sqrt, newaxis
from scipy.stats import norm
from opus_core import ndimage
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
from opus_core.multiple_runs import MultipleRuns, setup_environment
from opus_core.plot_functions import plot_one_boxplot_r
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
    
    def get_values_for_quantity(self, variable_name):
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
        if self.variable_name.get_alias() not in self.dataset.get_known_attribute_names():
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
        
class BayesianMelding(MultipleRuns):

    weights_file_name = "weights"
    variance_file_name = "variance"
    bias_file_name = "bias"
    
    def __init__(self, cache_file_location, observed_data,
                 base_year=0,  prefix='run_', package_order=['core'], additional_datasets={},
                 overwrite_cache_directories_file=False):
        """ Class used in the Bayesian melding analysis.
        'cache_file_location' is location (either file or directory) with information about all caches
        (see doc string for MultipleRuns).
        'observed_data' is an object of ObservedData that contains all the information about observed data.
        """
        MultipleRuns.__init__(self, cache_file_location, prefix=prefix, package_order=package_order, 
                              additional_datasets=additional_datasets,
                              overwrite_cache_directories_file=overwrite_cache_directories_file)
        self.output_directory = os.path.join(os.path.split(self.full_cache_file_name)[0], 'bm_output')
        logger.log_status('Output directory set to %s.' % self.output_directory)
        if not os.path.exists(self.output_directory):
            os.mkdir(self.output_directory)
        self.observed_data = observed_data
        self.base_year = base_year
        self.propagation_factor = {}
        self.additive_propagation = {}
        self.y = {}
        self.mu = {}
        self.ahat = {}
        self.v = {}
        self.weight_components = {}
        self.simulated_values = None
        self.weights = None
    
    def compute_y(self):
        iout = -1
        for quantity in self.observed_data.get_quantity_objects():
            iout += 1
            self.y[iout] = quantity.get_transformed_values()

    def compute_weights(self, procedure="opus_core.bm_normal_weights", **kwargs):
        """ Launches the run method of the given 'procedure'. This should return the actual BM weights.
        The method passes self as first argument into the run method.
        If 'procedure' is not given, the method returns equal weights.
        """
        self.compute_y()
        self.estimate_mu()
        self.estimate_bias()
        self.estimate_variance()
        if procedure is not None:
            procedure_class = ModelComponentCreator().get_model_component(procedure)
            self.weights, self.weight_components = procedure_class.run(self, **kwargs)
        else:
            self.weights = 1.0/self.number_of_runs * ones(self.number_of_runs)
        write_to_text_file(os.path.join(self.output_directory, self.weights_file_name),
                           self.weights)
        return self.weights
    
    def _compute_variable_for_one_run(self, run_index, variable, dataset_name, year, quantity):
        dataset_pool = self._setup_environment(self.cache_set[run_index], year)
        for mds_name, ids in quantity.get_matching_datasets().iteritems():
            mds = dataset_pool.get_dataset(mds_name)
            mds.subset_by_ids(ids, flush_attributes_if_not_loaded=False)
        ds = dataset_pool.get_dataset(dataset_name)
        ds.compute_variables(variable, dataset_pool=dataset_pool)            
        return ds
    
    def estimate_mu(self):
        iout = -1
        self.values_from_mr = {}
        for quantity in self.observed_data.get_quantity_objects():
            dataset_name = quantity.get_dataset_name()
            variable = quantity.get_variable_name()
            iout += 1
            dimension_reduced = False
            quantity_ids = quantity.get_dataset().get_id_attribute()
            for i in range(self.number_of_runs):
                ds = self._compute_variable_for_one_run(i, variable, dataset_name, self.get_calibration_year(), quantity)
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
                
            self.values_from_mr[variable.get_expression()] = self.mu[iout]
            if dimension_reduced:
                self.y[iout] = self.y[iout][quantity.get_dataset().get_id_index(ids)]

    def get_calibration_year(self):
        return self.observed_data.get_year()
        
    def get_scales(self, dataset, run, variable):
        return ones(dataset.size(), dtype="int32")

    def estimate_bias(self):
        mode="wb"
        for l in self.mu.keys():
            self.ahat[l] = (reshape(self.y[l], (self.y[l].size,1)) - self.mu[l]).mean()
            # for zone-specific bias
            #self.ahat[l] = mean(reshape(self.y[l], (self.y[l].size,1)) - self.mu[l], axis=1)
            if l > 0:
                mode="ab" # add to existing file
            write_to_text_file(os.path.join(self.output_directory, self.bias_file_name),
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
            write_to_text_file(os.path.join(self.output_directory, self.variance_file_name),
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

    def get_base_year(self):
        return self.base_year
    
    def get_variance_for_quantity(self):
        return self.v[self.use_bias_and_variance_index]

    def get_weight_components(self):
        return self.weight_components
    
    def set_propagation_factor(self, year, factor=1, additive=False, what='both'):
        """factor is used to multiply the number of years between calibration and projection.
            If no propagation is desired, set factor to 0 and additive to True. 
            'what' can be 'bias', 'variance' or 'both'
        """
        pname = what
        if what == 'both':
            pname = 'bias'
        if additive:
            self.propagation_factor[pname] = factor*(year - self.get_calibration_year())
        else:
            self.propagation_factor[pname] = factor*(year - self.get_base_year())/float(self.get_calibration_year() - self.get_base_year())
            
        self.additive_propagation[pname] = additive
        if what == 'both':
            self.propagation_factor['variance'] = self.propagation_factor['bias']
            self.additive_propagation['variance'] = self.additive_propagation['bias']

    def get_propagation_factor(self, what='variance'):
        return self.propagation_factor[what]

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
            ds = self._compute_variable_for_one_run(i, variable_name, dataset_name, year, self.observed_data.get_quantity_object(quantity_of_interest))
            if i == 0: # first run
                self.m = zeros((ds.size(), self.number_of_runs), dtype=float32)
                self.m_ids = ds.get_id_attribute()
            self.m[:, i] = try_transformation(ds.get_attribute(variable_name), self.transformation_pair_for_prediction[0])


    def get_posterior_component_mean(self):
        if self.additive_propagation['bias']:
            bias = self.get_bias_for_quantity()  + self.get_propagation_factor(what='bias')
        else:
            bias = self.get_bias_for_quantity()*self.get_propagation_factor(what='bias')
        return bias + self.get_predicted_values()

    def get_posterior_component_variance(self):
        if self.additive_propagation['variance']:
            return self.get_variance_for_quantity()+self.get_propagation_factor(what='variance')
        return self.get_variance_for_quantity()*self.get_propagation_factor(what='variance')

    def get_bias_and_variance_from_files(self):
        bias = array(load_from_text_file(
                         os.path.join(self.output_directory, self.bias_file_name),
                                                 convert_to_float=True))
        variance = array(load_from_text_file(
                                 os.path.join(self.output_directory, self.variance_file_name),
                                                 convert_to_float=True))
        if variance.ndim == 1:
            variance.reshape(variance.size, 1)
        ahat={}
        v = {}
        for l in range(bias.size):
            ahat[l] = bias[l]            
            v[l] = variance[l,:]
        return (ahat, v)

    def get_weights_from_file(self):
        file = os.path.join(self.output_directory, self.weights_file_name)
        if not os.path.exists(file):
            raise StandardError, "Directory %s must contain a file '%s'. Use method 'compute_weights'." % (self.output_directory,
                                                                             self.weights_file_name)
        return array(load_from_text_file(file, convert_to_float=True))

    def generate_posterior_distribution(self, year, quantity_of_interest, procedure="opus_core.bm_normal_posterior",
                                        use_bias_and_variance_from=None, transformed_back=True, aggregate_to=None,
                                        intermediates=[], propagation_factor=[0,0],  
                                        additive_propagation=[False,False], **kwargs):
        """
        'quantity_of_interest' is a variable name about which we want to get the posterior distribution.
        If there is multiple known_output, it must be made clear from which one the bias and variance
        is to be used (argument use_bias_and_variance_from). If it is None, the first known output is used.
        """
        self.set_posterior(year, quantity_of_interest, use_bias_and_variance_from, propagation_factor=propagation_factor,
                           additive_propagation=additive_propagation)
        procedure_class = ModelComponentCreator().get_model_component(procedure)
        self.simulated_values = procedure_class.run(self, **kwargs)
        if transformed_back and (self.transformation_pair_for_prediction[0] is not None): # need to transform back
            self.simulated_values = try_transformation(self.simulated_values,
                                                       self.transformation_pair_for_prediction[1])
        self.simulated_values_ids = self.m_ids
        if aggregate_to is not None:
            (self.simulated_values, self.simulated_values_ids) = self.aggregate(self.simulated_values, 
                                                   aggregate_from=VariableName(quantity_of_interest).get_dataset_name(),
                                                   aggregate_to=aggregate_to, intermediates=intermediates)
                
        return self.simulated_values

    def aggregate(self, values, aggregate_from, aggregate_to, intermediates=[]):
        dataset_pool = self._setup_environment(self.cache_set[0], self.get_base_year())
        ds_from = dataset_pool.get_dataset(aggregate_from)
        dataset_names = intermediates + [aggregate_to]
        new_values = values.copy()
        for dataset_name in dataset_names:
            aggr_values = new_values.copy()
            ds_to = dataset_pool.get_dataset(dataset_name)
            ids = ds_from.get_attribute(ds_to.get_id_name()[0])
            new_values = zeros((ds_to.size(), aggr_values.shape[1]), dtype=values.dtype)
            for i in range(aggr_values.shape[1]):
                new_values[:,i] = ndimage.sum(aggr_values[:,i], labels=ids, index=ds_to.get_id_attribute())
            ds_from = ds_to
        return (new_values, ds_to.get_id_attribute())
            
            
            
    def set_posterior(self, year, quantity_of_interest, use_bias_and_variance_from=None, propagation_factor=[0,0],
                       additive_propagation=[False, False]):
        self.set_propagation_factor(year, factor=propagation_factor[0], 
                                    additive=additive_propagation[0], what='bias')
        self.set_propagation_factor(year, factor=propagation_factor[1], 
                                    additive=additive_propagation[1], what='variance')
        if self.weights is None:
            self.weights = self.get_weights_from_file()
        if not self.ahat or not self.v:
            self.ahat, self.v = self.get_bias_and_variance_from_files()

        if use_bias_and_variance_from is None:
            use_bias_and_variance_from = quantity_of_interest
            

        self.use_bias_and_variance_index = self.get_index_for_quantity(use_bias_and_variance_from)
        #from numpy import sqrt
#        C=2194832
#        C=1428041
#        K=self.mu[self.use_bias_and_variance_index].shape[0]
#        D=(self.mu[self.use_bias_and_variance_index]**2).sum()+self.v[self.use_bias_and_variance_index]*K-C
#        tmp = sqrt((2*self.mu[self.use_bias_and_variance_index].sum())**2 - 4*K*D)
        #self.ahat[self.use_bias_and_variance_index] = -2*self.mu[self.use_bias_and_variance_index].sum()
        self.transformation_pair_for_prediction = self.observed_data.get_quantity_object_by_index(self.use_bias_and_variance_index).get_transformation_pair()
        self.compute_m(year, quantity_of_interest)
        
    def get_index_for_quantity(self, variable_name):
        variable_list = self.get_short_variable_names()
        short_name = VariableName(variable_name).get_alias()
        if short_name not in variable_list:
            raise ValueError, "Quantity %s is not among observed data." % variable_name
        return variable_list.index(short_name)
        
    def get_variable_names(self):
        return map(lambda x: x.get_expression(), self.observed_data.get_variable_names())
    
    def get_short_variable_names(self):
        return map(lambda x: x.get_alias(), self.observed_data.get_variable_names())
    
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
        
    def write_weight_components(self, filename):
        l = len(self.get_weight_components().keys())
        weight_matrix = zeros((l, self.number_of_runs))
        for i in range(l):
            weight_matrix[i,:] = self.get_weight_components()[i]
        write_table_to_text_file(filename, weight_matrix)
        
    def export_weights_posterior_mean_and_variance(self, years, quantity_of_interest, directory, filename=None, 
                                                     use_bias_and_variance_from=None, ids = None, **kwargs):
        for year in years:
            self.set_posterior(year, quantity_of_interest, use_bias_and_variance_from, **kwargs)
            if filename is None:
                filename = quantity_of_interest
            file = os.path.join(directory, str(year) + '_' + filename)
            write_to_text_file(file, concatenate((array([0.]), self.get_weights())), delimiter=' ')
            write_to_text_file(file, concatenate((array([0.]), self.get_posterior_component_variance())), mode='a', delimiter=' ')
            variable_list = self.get_variable_names()
            quantity_index = variable_list.index(quantity_of_interest)
            if ids is None:
                ids = self.m_ids
            means = zeros((ids.size, self.number_of_runs+1))
            means[:,0] = ids
            means[:,1:means.shape[1]] = self.get_posterior_component_mean()
            write_table_to_text_file(file, means, mode='a')            

    def export_bm_parameters_of_one_quantity(self, quantity_of_interest, filepath, add_to_file=True, run_index=None):
        variable_list = self.get_variable_names()
        quantity_index = variable_list.index(quantity_of_interest)
        mode = 'a'
        if not add_to_file:
            mode = 'w'
        if run_index is None:
            idx = argsort(self.get_weight_components()[quantity_index])[-1]
        else: 
            idx = run_index
        write_to_text_file(filepath, array([variable_list[quantity_index]]), mode=mode)
        write_to_text_file(filepath, array([self.get_bias()[quantity_index], self.get_variance()[quantity_index][idx]]), 
                           mode='a', delimiter=' ')
        
    def export_bm_parameters(self, directory, filename=None, quantities=None, run_index=None):
        """Writes BM parameters (bias and variance) for each quantity to a file. The variance parameter is either 
        the one computed for a run given by run_index, or (if it is not given) for the run with the highest weight.
        
        """
        if filename is None:
            filename = 'bm_parameters_' + str(self.get_calibration_year())
        if run_index is not None:
            filename = '%s_run_%s' % (filename, run_index) 
        file = os.path.join(directory, filename)
        if quantities is None:
            variable_list = self.get_variable_names()
        else:
            variable_list = quantities
        write_to_text_file(file, array([self.get_base_year(), self.get_calibration_year()]), delimiter=' ')
        for quant in variable_list:
            self.export_bm_parameters_of_one_quantity(quant, file, add_to_file=True, run_index=run_index)
            
        
    def get_quantity_from_simulated_values(self, function):
        """'function' is a character string specifying a function of the scipy.ndimage package (e.g. mean,
        standard_deviation, variance).
        This function is applied to the simulated values (per dimension).
        """
        labels = self._get_label_of_simulated_values()
        idx = (arange(labels.shape[0])+1).astype('int32')
        return eval("array(ndimage.%s(self.simulated_values, labels=labels, index=idx))" % function)

    def _get_label_of_simulated_values(self):
        self._check_simulated_values()
        return transpose(reshape(array(self.simulated_values.shape[1]*range(self.simulated_values.shape[0])),
                              (self.simulated_values.shape[1], self.simulated_values.shape[0])) + 1)

    def _check_simulated_values(self):
        if self.simulated_values is None:
            raise StandardError, "Values were not simulated yet. Use method 'generate_posterior_distribution'."

    def get_quantiles(self, quantiles):
        """Returns a matrix where each column corresponds to one element of the quantiles array.
        """
        if not isinstance(quantiles, ndarray):
            quantiles = array(quantiles)
        sorted_values = sort(self.simulated_values, axis=1)
        result = zeros((sorted_values.shape[0], quantiles.size))
        n = sorted_values.shape[1]
        for i in range(quantiles.size):
            result[:,i] = sorted_values[:, int(n * quantiles[i])]
        return result

    def get_probability_interval(self, interval, exact=True, **kwargs):
        """Returns an array with two columns. First column contains the lower bound, the second column contains the 
        upper bound of the given probability interval.
        If exact is False, the quantiles are derived from simulated values, i.e. the generate_posterior_distribution method
        has to be called prior to this. Otherwise the set_posterior method is required prior to this call, 
        in order to get exact intervals for the right settings.
        """
        alpha = (1-interval/100.0)/2.0
        if not exact:
            self._check_simulated_values()
            return self.get_quantiles([alpha, 1-alpha])
        return concatenate((self.get_exact_quantile(alpha, **kwargs)[:,newaxis], self.get_exact_quantile(1-alpha, **kwargs)[:,newaxis]), axis=1)
        
    def get_exact_quantile(self, alpha, transformed_back=True, truncated=True, **kwargs):
        vars = self.get_posterior_component_variance()
        means = self.get_posterior_component_mean()
        if means.ndim < 2:
            means = means[:,newaxis]
        weights = self.get_weights()
        sig = sqrt(vars)
        res = zeros(means.shape[0])
        for i in range(means.shape[0]):
            res[i] = bmaquant(alpha, weights, means[i,:], sig, **kwargs)
        if truncated: # truncate at 0
            res = maximum(res, 0)
        if transformed_back and (self.transformation_pair_for_prediction[0] is not None): 
            res = try_transformation(res, self.transformation_pair_for_prediction[1])
        return res
    

        
    def export_confidence_intervals(self, confidence_levels, filename, delimiter='\t'):
        """Export confidence intervals into a file. 
        confidence_levels is a list of desired confidence levels. 
        The resulting file has a id column, 'mean' column and for each level 
        its lower bound and upper bound columns.
        The method generate_posterior_distribution should be called prior to this method.
        """
        if not isinstance(confidence_levels, list):
            confidence_levels = [confidence_levels]
        lcl = len(confidence_levels)
        result = zeros((self.simulated_values_ids.size, 2+2*lcl), dtype='float32')
        result[:,0] = self.simulated_values_ids
        result[:,1] = self.get_quantity_from_simulated_values("mean")
        clheader = []
        for cl in confidence_levels:
            clheader = clheader + ['lower_%s' % cl, 'upper_%s' % cl]
        write_to_text_file(filename, ['id', 'mean'] + clheader, delimiter=delimiter)
        i = 2
        for cl in confidence_levels:
            ci = self.get_probability_interval(cl/100.0)
            result[:,i:(i+2)] = ci
            i = i+2
        write_table_to_text_file(filename, result, mode='a', delimiter=delimiter)
        
    def get_m_ids(self):
        return self.m_ids
    
    def get_variables_for_dataset(self, dataset_name):
        """Rerturn variable names of the observed quantities that match the given dataset_name."""
        return [var for var in self.get_variable_names() if VariableName(var).get_dataset_name() == dataset_name]

    def get_index_of_n_highest_weights(self, n=1):
        w = self.get_weights()
        return argsort(w)[-n:w.size]
    
    def get_index_of_weights_over_threshold(self, threshold=0):
        w = self.get_weights()
        return where(w >= threshold)[0]
    
    def get_index_of_n_highest_component_weights(self, component_index, n=1):
        w = self.get_weight_components()[component_index]
        return argsort(w)[-n:w.size]
    
    def get_index_of_component_weights_over_threshold(self, component_index, threshold=0):
        w = self.get_weight_components()[component_index]
        return where(w >= threshold)[0]
    
    def plot_boxplot_r(self, filename=None, n_highest_weights=1, n_highest_weights_for_quantity=1, weight_threshold=None, logy=False):
        from rpy import r
        logstring = ''
        if logy:
            logstring='y'
            
        if filename is not None:
            r.pdf(file=filename)
    
        for var, values in self.values_from_mr.iteritems():
            plot_one_boxplot_r(values, var, logstring)
            if values.ndim == 1:
                v = resize(values, (1, values.size))
            else:
                v = values
            ivar = self.get_index_for_quantity(var)
            if weight_threshold is not None:
                for i in range(0, v.shape[0]):
                    iw = self.get_index_of_component_weights_over_threshold(ivar, weight_threshold)
                    if iw.size > 0:
                        r.points(i+1, v[i:(i+iw.size),iw], col='yellow', cex=0.5)
                    iw = self.get_index_of_weights_over_threshold(weight_threshold)
                    if iw.size > 0:
                        r.points(i+1, v[i:(i+iw.size),iw], col='blue', cex=0.5)
            if n_highest_weights_for_quantity > 0:
                for i in range(0, v.shape[0]):
                    r.points(i+1, v[i,self.get_index_of_n_highest_component_weights(ivar, n_highest_weights_for_quantity)], col='green', cex=0.5)
            if n_highest_weights > 0:
                for i in range(0, v.shape[0]):
                    r.points(i+1, v[i,self.get_index_of_n_highest_weights(n_highest_weights)], col='red', cex=0.5)
                    
        if filename is not None:
            r.dev_off()
      
def bmaquant(alpha, weights, means, sigma, niter=14):
    def bmacdf(x, w, m, s):
        return (w * norm.cdf(x*ones(m.size), m, s)).sum()
   
    # initialize lower and upper bound
    lower = (means - 3*sigma).min()
    upper = (means + 3*sigma).max()
    Flower = bmacdf(lower, weights, means, sigma)
    Fupper = bmacdf(upper, weights, means, sigma)
    if Flower > alpha or Fupper < alpha:
        raise ValueError, 'Something wrong with means and variances.'
    # Bisection method
    for iter in range(niter):
        mid = (lower+upper)/2.
        Fmid = bmacdf(mid, weights, means, sigma)
        if Fmid > alpha:
            upper = mid
        else:
            lower = mid
    return mid
        
class BayesianMeldingFromFile(BayesianMelding):
    """ Class to be used if bm parameters were stored previously using export_bm_parameters of BayesianMelding class.
        It can be passed into bm_normal_posterior.py.
    """
    def __init__(self, filename, package_order=['core'], additional_datasets={}, cache_file_location=None, 
                 transformation_pair = (None, None), **kwargs):
        """The file 'filename' has the following structure:
        1. line: base_year calibration_year 
        2 lines per each variable: 
            1. variable_name
            2. bias variance  
        """
        content = load_from_text_file(filename)
        nvar = (content.size-1)/2
        self.base_year, self.year = map(lambda x: int(x), content[0].split(' '))
        self.variable_names = []
        self.ahat = {}
        self.v = {}
        self.weight_components = {}
        self.package_order = package_order
        if cache_file_location is not None: 
            BayesianMelding.set_cache_attributes(self, cache_file_location, **kwargs)
        self.number_of_runs = len(self.cache_set)
        self.weights = array(self.number_of_runs * [1./float(self.number_of_runs)])
        counter = 1
        for i in range(nvar):
            self.variable_names.append(content[counter])
            counter += 1
            splitted_row = content[counter].split(' ')
            self.ahat[i], self.v[i] = map(lambda x: array([float(x)]), splitted_row)
            self.ahat[i] = array(self.number_of_runs * [self.ahat[i][0]])
            self.v[i] = array(self.number_of_runs * [self.v[i][0]])
            self.weight_components[i] = array(self.number_of_runs * [1./float(self.number_of_runs)])
            counter += 1
        self.additional_datasets = additional_datasets
        self.transformation_pair_for_prediction = transformation_pair
        self.propagation_factor = {}
        self.additive_propagation = {}
                 
    def get_calibration_year(self):
        return self.year
     
    def get_variable_names(self):
        return self.variable_names
    
    def get_short_variable_names(self):
        return map(lambda x: VariableName(x).get_alias(), self.get_variable_names())
    
    def generate_posterior_distribution(self, year, quantity_of_interest, cache_directory=None, values=None, ids=None, 
                                        procedure="opus_core.bm_normal_posterior", use_bias_and_variance_from=None, 
                                        transformed_back=True, aggregate_to=None,
                                        intermediates=[], propagation_factor=[0,0],  
                                        additive_propagation=[False,False], **kwargs):

        if (values is None or ids is None) and (self.cache_set is None):
            raise StandardError, "values and ids must be give if the BM object is initialized without cache_file_location."
            
        self.set_posterior(year, quantity_of_interest, values=values, ids=ids, use_bias_and_variance_from=use_bias_and_variance_from, 
                           propagation_factor=propagation_factor, 
                           additive_propagation=additive_propagation)
        procedure_class = ModelComponentCreator().get_model_component(procedure)
        self.simulated_values = procedure_class.run(self, **kwargs)
        if transformed_back and (self.transformation_pair_for_prediction[0] is not None): # need to transform back
            self.simulated_values = try_transformation(self.simulated_values,
                                                       self.transformation_pair_for_prediction[1])
        self.simulated_values_ids = self.m_ids
        if aggregate_to is not None:
            (self.simulated_values, self.simulated_values_ids) = self.aggregate(self.simulated_values, 
                                                   aggregate_from=VariableName(quantity_of_interest).get_dataset_name(),
                                                   aggregate_to=aggregate_to, intermediates=intermediates)
        return self.simulated_values
        
    def set_posterior(self, year, quantity_of_interest, values=None, ids=None, use_bias_and_variance_from=None, 
                      propagation_factor=[0,0], additive_propagation=[False,False]):
        self.set_propagation_factor(year, factor=propagation_factor[0], 
                                    additive=additive_propagation[0], what='bias')
        self.set_propagation_factor(year, factor=propagation_factor[1], 
                                    additive=additive_propagation[1], what='variance')
        if use_bias_and_variance_from is None:
            use_bias_and_variance_from = quantity_of_interest
            
        self.use_bias_and_variance_index = self.get_index_for_quantity(use_bias_and_variance_from)
        self.compute_m(year, quantity_of_interest, values, ids)
        
    def get_index_for_quantity(self, variable_name):
        variable_list = self.get_short_variable_names()
        short_name = VariableName(variable_name).get_alias()
        if short_name not in variable_list:
            raise ValueError, "Quantity %s not found." % variable_name
        return variable_list.index(short_name)
    
    def _get_m_from_values(self, values, ids):
        self.m = values
        self.m_ids = ids
        if self.m.ndim < 2:
            self.m = resize(self.m, (self.m.size, 1))
        self.m = try_transformation(self.m, self.transformation_pair_for_prediction[0])

    def compute_m(self, year, quantity_of_interest, values=None, ids=None):
        if (values is not None) and (ids is not None):
            self._get_m_from_values(values, ids)
            return
        variable_name = VariableName(quantity_of_interest)
        dataset_name = variable_name.get_dataset_name()
        for i in range(self.cache_set.size):
            ds = self._compute_variable_for_one_run(i, variable_name, dataset_name, year)
            if i == 0: # first run
                m = zeros((ds.size(), self.cache_set.size), dtype=float32)
                self.m_ids = ds.get_id_attribute()
            m[:, i] = try_transformation(ds.get_attribute(variable_name), self.transformation_pair_for_prediction[0])
        #self.m = resize(average(m, axis=1), (m.shape[0], 1))
        self.m = m
            
    def _compute_variable_for_one_run(self, run_index, variable, dataset_name, year, dummy=None):
        return MultipleRuns._compute_variable_for_one_run(self, run_index, variable, dataset_name, year)


import os
from opus_core.tests import opus_unittest
import tempfile

from shutil import rmtree

from numpy import array, arange, allclose, array_equal

from opus_core.cache.create_test_attribute_cache import CreateTestAttributeCache
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset

class Tests(opus_unittest.OpusTestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        self.cache_dir = os.path.join(self.temp_dir, 'run_1')
        self.observed_file = os.path.join(self.temp_dir, 'observed_data')
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
            
    def _create_cache_data(self):
        test_data = {
            2000: { # base year
                'households':{
                    'id': arange(50)+1,
                    'location_id':array(10*[1] + 25*[2] + 15*[3])
                    },
                'locations': {
                    'location_id': array([1,2,3]) # hhs: 10, 25, 15           
                    }
                },
            2005: { # present year
                'households':{
                    'household_id': arange(60)+1,
                    'location_id':array(5*[1] + 10*[3] + 15*[2] + 20*[3] + 10*[1])
                    },
                'locations': {
                    'location_id': array([1,2,3])  # hhs: 15, 15, 30          
                    }
                },
            2010: { # future year
                'households':{
                    'household_id': arange(80)+1,
                    'location_id':array(15*[1] + 10*[3] + 20*[2] + 25*[3] + 10*[1])
                    },
                'locations': {
                    'location_id': array([1,2,3])  # hhs: 25, 20, 35          
                    }
                }
        }
        cache_creator = CreateTestAttributeCache()
        cache_creator.create_attribute_cache_with_data(self.cache_dir, test_data)
        
    def _create_observed_data_file(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name = 'locations',
                        table_data = {'location_id': arange(3) + 1,
                                      'number_of_households': array([18, 14, 32])
                                      }
                        )
        dataset = Dataset(in_storage = storage, 
                           in_table_name='locations',
                           id_name='location_id' 
                           )
        outstorage = StorageFactory().get_storage('tab_storage', storage_location = self.temp_dir)
        dataset.write_dataset(out_storage=outstorage, out_table_name=self.observed_file)
        
    def test_bayesian_melding(self):
        # set up run cache and observed data file
        self._create_cache_data() # here it contains only one run cache, but can have multiple caches
        self._create_observed_data_file()
        indicator = 'number_of_households = location.number_of_agents(household)'
        # Initiate the observed data object
        observed_data = ObservedData(self.temp_dir, 
                                 year=2005, # from what year are the observed data 
                                 storage_type='tab_storage', # in what format
                                 package_order=['opus_core'])
        # Do this for each quantity of interest
        observed_data.add_quantity(
                variable_name = indicator, # What variable does the observed data correspond to
                filename = self.observed_file, # In what file are values of this variable
                transformation = 'sqrt' # What transformation should be performed (can be set to None)
        )
        
        bm = BayesianMelding(self.temp_dir, 
                         observed_data,                        
                         base_year=2000, 
                         prefix='run_', # within 'cache_directory' filter only directories with this prefix
                         overwrite_cache_directories_file=True,
                         package_order=['opus_core'])
        # Main computation
        weights = bm.compute_weights()
        self.assertEqual(weights.size, 1) # size one because only one run
        self.assertEqual(weights[0], 1) 
        
        # get bias and variance
        bias = bm.get_bias()
        variance = bm.get_variance()
        # the above are dictionaries for each indicator, here only one:
        # bm.observed_data.get_variable_names()
        
        # Export results for later use
        bm.export_bm_parameters(self.temp_dir, filename='bm_parameters')
        # Reload results 
        bmf = BayesianMeldingFromFile(os.path.join(self.temp_dir, 'bm_parameters'), package_order=['opus_core'],
                                      cache_file_location=self.temp_dir, prefix='run_', 
                                      overwrite_cache_directories_file=True, transformation_pair = ("sqrt", "**2"))
        self.assert_(allclose(bmf.get_bias()[0], bias[0]))
        self.assert_(allclose(bmf.get_variance()[0], variance[0]))
        
        # posterior distribution for future years
        posterior = bmf.generate_posterior_distribution(year=2010, 
                                    quantity_of_interest=indicator,
                                    replicates=10, propagation_factor=[0,1])
        self.assert_(array_equal(posterior.shape, [3,10])) # 3 rows (1 row per location), 10 samples
        pi = bmf.get_probability_interval(80)
        bmf.export_confidence_intervals([80, 95], os.path.join(self.temp_dir, 'CIs'))
        
if __name__=='__main__':
    opus_unittest.main()