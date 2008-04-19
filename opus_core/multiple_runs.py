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
from opus_core.misc import load_from_text_file, write_table_to_text_file, write_to_text_file
from opus_core.plot_functions import plot_values_as_boxplot_r
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.variables.variable_name import VariableName
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from opus_core.logger import logger

class MultipleRuns:
    """ This is a class to support obtaining results from multiple runs."""

    caches_file_name = "cache_directories"
    
    def __init__(self, cache_file_location, prefix='run_', package_order=['core']):
        """'cache_file_location' is either a file that contains a list of all caches that
        belong to this set of runs (one line per directory). Alternatively, it can be a directory. In such a case
        the code looks for a file called "cache_directories" (value of self.caches_file_name) in this location.
        If it exists, it should contain a list of all caches as described above. If such file does not exist,
        it is created from all entries in 'cache_file_location' that have the given 'prefix'. 
        
        The list of all caches is stored in self.cache_set.
        """
        self.set_cache_attributes(cache_file_location, prefix=prefix)
        self.number_of_runs = self.cache_set.size
        self.package_order = package_order
        self.values_from_mr = {}
        
    def set_cache_attributes(self, cache_file_location, prefix=''):
        if os.path.isfile(cache_file_location):
            self._set_cache_set(cache_file_location)
            return
        if os.path.isdir(cache_file_location):
            filename = os.path.join(cache_file_location, self.caches_file_name)
            if os.path.exists(filename):
                self._set_cache_set(filename)
                return
            create_file_cache_directories(directory=cache_file_location, prefix=prefix, file_name=self.caches_file_name)
            self._set_cache_set(filename)
            return 
        raise StandardError, "Location %s not found." % (cache_file_location)
        
    def _set_cache_set(self, filename):
        self.cache_set = load_from_text_file(filename)
        self.full_cache_file_name = filename
        logger.log_status('Multiple Runs consist of %s runs (loaded from %s)' % (self.cache_set.size, filename))
        
    def _compute_variable_for_one_run(self, run_index, variable, dataset_name, year):
        dataset_pool = setup_environment(self.cache_set[run_index], year, self.package_order)
        try:
            ds = dataset_pool.get_dataset(dataset_name)
        except:
            logger.log_warning('Dataset %s could not be loaded from dataset pool using package order %s' % (dataset_name, self.package_order))
            logger.log_warning('Generic dataset will be created.')
            ds = Dataset(in_table_name=dataset_name, in_storage=dataset_pool.get_storage(), dataset_name=dataset_name, id_name=[])
            dataset_pool._add_dataset(dataset_name, ds)
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
            
    def export_values_from_mr(self, directory, prefix=''):
        vars = self.values_from_mr.keys()
        for var in vars:
            filename = os.path.join(directory, "%s%s" % (prefix, VariableName(var).get_alias()))
            write_table_to_text_file(filename, self.values_from_mr[var])
            
    def plot_current_values_as_boxplot_r(self, filename=None, logy=False):
        """Create a set of boxplots (using R), one plot per variable in self.values_from_mr.
        (see docstring in plot_functions.plot_values_as_boxplot_r)
        """
        plot_values_as_boxplot_r(self.values_from_mr, filename=filename, logy=logy)
        

    
def create_file_cache_directories(directory, prefix='', file_name='cache_directories'):
    logger.start_block('Creating file %s in %s' % (file_name, directory))
    all_dirs = os.listdir(directory)
    all_dirs = [x for x in all_dirs if x.startswith(prefix)]
    if not prefix.startswith('.'):
        all_dirs = [x for x in all_dirs if not x.startswith('.')]

    for i in range(len(all_dirs)):
        all_dirs[i] = os.path.join(directory, all_dirs[i])
        
    write_to_text_file(os.path.join(directory, file_name), all_dirs)
    logger.end_block()
               
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

if __name__=='__main__':
    from opus_core.multiple_runs import MultipleRuns
    mr = MultipleRuns('/Users/hana/urbansim_cache/psrc/parcel/bm/0416')
    mr.set_values_from_mr(2005, ['urbansim_parcel.zone.number_of_households'])
    