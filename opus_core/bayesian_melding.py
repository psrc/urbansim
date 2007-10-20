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
from opus_core.datasets.dataset import DatasetSubset
from opus_core.resources import Resources
from opus_core.session_configuration import SessionConfiguration

class BayesianMelding:

    caches_file_name = "cache_directories"
    weights_file_name = "weights"
    variance_file_name = "variance"
    bias_file_name = "bias"
    # pairs of inverse transformations
    transformation_pairs = {"sqrt": "**2", "log":"exp", "exp": "log", "**2": "sqrt"}

    def __init__(self, cache_directory, cache_with_true_data=None,
                 datasets_with_true_data = None,
                 year_with_true_data=0,
                 known_output=[], transformation=None, inverse_transformation=None,
                 base_year=0, scaling_parents={}, package_order=['core']):
        """ Class used in the Basesian melding analysis.
        'cache_directory' is the first directory created by start_run_set.py. It should
        contain a file called 'cache_directories' which contains a list of all caches that
        belong to this set of runs. This list is read and stored in self.cache_set.
        'cache_with_true_data' is the cache directory, where the true data are stored.
        Alternatively, 'datasests_with_true_data' can be passed, which is a dictionary of
        pairs (dataset name, dataset). It has priority over cache_with_true_data'.
        'year_with_true_data' is the year from which we have true data.
        'known_output' is a list of variable names about which we have data available.
        """
        file = os.path.join(cache_directory, self.caches_file_name)
        if not os.path.exists(file):
            raise StandardError, "Directory %s must contain a file '%s'." % (cache_directory,
                                                                             self.caches_file_name)
        self.cache_directory = cache_directory
        self.cache_set = load_from_text_file(file) # it is a array
        self.number_of_runs = self.cache_set.size
        self.cache_with_true_data = cache_with_true_data
        self.true_datasets = datasets_with_true_data
        self.cache_storage_with_true_data = None
        self.package_order = package_order
        self.transformation = transformation
        if inverse_transformation is not None:
            self.transformation_pairs[self.transformation] = inverse_transformation
        self.base_year = base_year
        self.year_with_true_data = year_with_true_data
        self.known_output = []
        self.datasets_to_create = []
        for var in known_output:
            varname = VariableName(var)
            self.known_output.append(varname)
            self.datasets_to_create.append(varname.get_dataset_name())
        self.propagation_factor = None
        self.y = {}
        self.y_match_to_datasets = {}
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
        if self.true_datasets is None:
            dataset_pool = self.setup_environment(self.cache_with_true_data, self.year_with_true_data)
            self.true_datasets = self.get_datasets(dataset_pool)
        iout = -1
        for variable in self.known_output:
            dataset = variable.get_dataset_name()
            iout += 1
            self.true_datasets[dataset].compute_variables(variable, resources=Resources(self.true_datasets))
            self.y[iout] = try_transformation(self.true_datasets[dataset].get_attribute(variable),
                                              self.transformation)
            self.y_match_to_datasets[iout] = dataset

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
        for variable in self.known_output:
            dataset = variable.get_dataset_name()
            iout += 1
            dimension_reduced = False
            for i in range(self.number_of_runs):
                dataset_pool = self.setup_environment(self.cache_set[i], self.year_with_true_data)
                simulated_datasets = self.get_datasets(dataset_pool)
                ds = simulated_datasets[dataset]
                ds.compute_variables(variable, resources=Resources(simulated_datasets))
                if i == 0: # first run
                    self.mu[iout] = zeros((ds.size(), self.number_of_runs),
                                          dtype=float32)
                    ids = ds.get_id_attribute()
                else:
                    if ds.size() > self.mu[iout].shape[0]:
                        ds = DatasetSubset(simulated_datasets[dataset], simulated_datasets[dataset].get_id_index(ids))
                        dimension_reduced = True
                scale = self.get_scales(ds, i+1, variable)
                self.mu[iout][:,i] = try_transformation(scale * ds.get_attribute(variable), self.transformation)
            if dimension_reduced:
                self.y[iout] = self.y[iout][self.true_datasets[self.y_match_to_datasets[iout]].get_id_index(ids)]

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

    def setup_environment(self, cache_directory, year):
        ss = SimulationState(new_instance=True)
        ss.set_cache_directory(cache_directory)
        ss.set_current_time(year)
        ac = AttributeCache()
        storage = ac.get_flt_storage_for_year(year)
        package_order = self.package_order
        sc = SessionConfiguration(new_instance=True,
                             package_order=package_order,
                             in_storage=ac)
        return sc.get_dataset_pool()

    def set_propagation_factor(self, year):
        self.propagation_factor = (year - self.base_year)/float(self.year_with_true_data-self.base_year)

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
        dataset = variable_name.get_dataset_name()
        for i in range(self.number_of_runs):
            dataset_pool = self.setup_environment(self.cache_set[i], year)
            simulated_datasets = self.get_datasets(dataset_pool)
            simulated_datasets[dataset].compute_variables(variable_name)
            if i == 0: # first run
                self.m = zeros((simulated_datasets[dataset].size(), self.number_of_runs),
                                      dtype=float32)
            self.m[:, i] = try_transformation(simulated_datasets[dataset].get_attribute(variable_name),
                                                    self.transformation)


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
            self.use_bias_and_variance_index = 0
        else:
            variable_list = map(lambda x: x.get_full_name(), self.known_output)
            self.use_bias_and_variance_index = variable_list.index(use_bias_and_variance_from)

        self.compute_m(year, quantity_of_interest)
        procedure_class = ModelComponentCreator().get_model_component(procedure)
        self.simulated_values = procedure_class.run(self, **kwargs)
        if self.transformation is not None: # need to transform back
            self.simulated_values = try_transformation(self.simulated_values,
                                                       self.transformation_pairs[self.transformation])
        return self.simulated_values

    def compute_true_data(self, year, quantity_of_interest):
        variable_name = VariableName(quantity_of_interest)
        dataset_name = variable_name.get_dataset_name()
        dataset_pool = self.setup_environment(self.cache_with_true_data, year)
        datasets = self.get_datasets(dataset_pool)
        datasets[dataset_name].compute_variables(variable_name)
        self.true_data_of_quantity_of_interest = datasets[dataset_name].get_attribute(variable_name)

    def compute_and_write_true_data(self, year, quantity_of_interest, filename):
        self.compute_true_data(year, quantity_of_interest)
        self.write_true_data_for_quantity(filename)

    def write_simulated_values(self, filename):
        write_table_to_text_file(filename, self.simulated_values)

    def write_values_from_multiple_runs(self, filename, transformed_back=True):
        write_table_to_text_file(filename, self.get_predicted_values(transformed_back=transformed_back))

    def write_true_data_for_quantity(self, filename):
        write_to_text_file(filename, self.true_data_of_quantity_of_interest, delimiter=' ')

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