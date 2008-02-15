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

import os
import gc
from numpy import zeros, arange
from opus_core.session_configuration import SessionConfiguration
from opus_core.misc import load_from_text_file, write_table_to_text_file
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.variables.variable_name import VariableName
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from opus_core.logger import logger

class MultipleRuns:
    """ This is a class to support obtaining results from multiple runs."""

    caches_file_name = "cache_directories"
    
    def __init__(self, cache_directory, package_order=['core']):
        """'cache_directory' must contain a file called 'cache_directories' which contains a list of all caches that
        belong to this set of runs (one line per directory). This list is read and stored in self.cache_set.
        """
        self.set_cache_attributes(cache_directory)
        self.number_of_runs = self.cache_set.size
        self.package_order = package_order
        self.values_from_mr = {}
        
    def set_cache_attributes(self, cache_directory):
        file = os.path.join(cache_directory, self.caches_file_name)
        if not os.path.exists(file):
            raise StandardError, "Directory %s must contain a file '%s'." % (cache_directory,
                                                                             self.caches_file_name)
        self.cache_directory = cache_directory
        self.cache_set = load_from_text_file(file) # it is an array
        
    def _compute_variable_for_one_run(self, run_index, variable, dataset_name, year):
        dataset_pool = setup_environment(self.cache_set[run_index], year, self.package_order)
        ds = dataset_pool.get_dataset(dataset_name)
        ds.compute_variables(variable, dataset_pool=dataset_pool)            
        return ds
    
    def compute_values_from_multiple_runs(self, year, quantity_of_interest, dtype='float32'):
        """
        'quantity_of_interest' is a variable name in its fully-qualified name.
        Return a matrix of size (dataset.size x number_of_runs), with values of the variable
        for eeach dataset member and run. Dataset is the one to which the 
        quantity_of_interest belongs to. 
        """
        variable_name = VariableName(quantity_of_interest)
        dataset_name = variable_name.get_dataset_name()
        for i in range(self.cache_set.size):
            ds = self._compute_variable_for_one_run(i, variable_name, dataset_name, year)
            if i == 0: # first run
                result = zeros((ds.size(), self.cache_set.size), dtype=dtype)
            result[:, i] = ds.get_attribute(variable_name)
        return result
        
    def get_dataset_from_first_run(self, year, dataset_name):
        dataset_pool = setup_environment(self.cache_set[0], year, self.package_order)
        return dataset_pool.get_dataset(dataset_name)
    
    def get_datasets_from_multiple_runs(self, year, quantities_of_interest, dataset_name, name_attribute=None):
        """Return a dictionary of datasets. Their attributes are the given 'quantities_of_interest', each element
        corresponds to one run. Each dataset correspond to one element in 'dataset_name'. 'name_attribute' 
        should be an attribute of 'dataset_name' and it is used as keys for the resulting dictionary.
        If it is None, the id_name attribute of dataset_name is used.
        """
        ds0 = self.get_dataset_from_first_run(year, dataset_name)
        if name_attribute is None:
            dataset_names = ds0.get_id_attribute()
        else:
            dataset_names = ds0.get_attribute(name_attribute)
        self.set_values_from_mr(year, quantities_of_interest)
        storage = StorageFactory().get_storage('dict_storage')
        result = {}
        for i in range(ds0.size()):
            storage_table_name = dataset_names[i]
            table_data = {'id': arange(self.number_of_runs)}
            for var in quantities_of_interest:
                table_data[VariableName(var).get_alias()] = self.values_from_mr[var][i,:]
            storage.write_table(
                table_name=storage_table_name,
                table_data=table_data
                )
            result[dataset_names[i]] = Dataset(in_storage=storage, in_table_name=storage_table_name, id_name="id", dataset_name=dataset_name)
        return result
            
    def set_values_from_mr(self, year, quantities_of_interest):
        self.values_from_mr = {}
        for var in quantities_of_interest:
            self.values_from_mr[var] = self.compute_values_from_multiple_runs(year, var)
            
    def export_values_from_mr(self, directory):
        vars = self.values_from_mr.keys()
        for var in vars:
            filename = os.path.join(directory, VariableName(var).get_alias())
            write_table_to_text_file(filename, self.values_from_mr[var])
        
            
def setup_environment(cache_directory, year, package_order):
    gc.collect()
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
