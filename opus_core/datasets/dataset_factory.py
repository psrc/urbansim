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

from opus_core.logger import logger
from opus_core.class_factory import ClassFactory

class DatasetFactory(object):
    """Conventions for dataset, module, class, and table names of datasets:
        - a dataset name is all lower case with '_', such as 'my_grizzly_bear'
        - the corresponding dataset is implemented in a module 'my_grizzly_bears.py'
        - the input data for this dataset is in table 'my_grizzly_bears'
        - the dataset class is called 'MyGrizzlyBearDataset'
    Any exceptions to this convention should be listed in the 'exceptions' list to allow
    dataset names, tables, modules, and classes to be determined.
    """
    
    # The exceptions list is a list of tuples
    #      (dataset_name, table_name, module_name, dataset_class_name)
    # module_name and dataset_class_name may be None; if so the generic Dataset class should be used.
    exceptions = [
       # doesn't work ... ('base_year', 'base_year', 'urbansim_constant_dataset', 'UrbansimConstantDataset'), 
        ('city', 'cities', 'city_dataset', 'CityDataset'), 
        ('building_sqft_per_job', 'building_sqft_per_job', 'building_sqft_per_job_dataset', 'BuildingSqftPerJobDataset'), 
        ('county', 'counties', 'county_dataset', 'CountyDataset'),
        ('demolition_cost_per_sqft', 'demolition_cost_per_sqft', 'demolition_cost_per_sqft_dataset', 'DemolitionCostPerSqftDataset'),
        ('development_event_history', 'development_event_history', 'development_event_history_dataset', 'DevelopmentEventHistoryDataset'),
        ('faz', 'fazes', 'faz_dataset', 'FazDataset'),
        ('household', 'households_for_estimation', 'household_dataset', 'HouseholdDataset'), 
        ('household_characteristic', 'household_characteristics_for_ht', 'household_characteristic_dataset', 'HouseholdCharacteristicDataset'), 
        ('job', 'jobs_for_estimation', 'job_dataset', 'JobDataset'), 
        ('race', 'race_names', 'race_dataset', 'RaceDataset'), 
        ('target_vacancy', 'target_vacancies', 'target_vacancy_dataset', 'TargetVacancyDataset'), 
        ('travel_data', 'travel_data', 'travel_data_dataset', 'TravelDataDataset'), 
        ]

    def get_dataset(self, dataset_name, subdir="datasets", package="opus_core", 
                    arguments={}, debug=0):
        """If the conventions in the class comment are followed or if the dataset name is
        appropriately listed in 'exceptions', this method returns a Dataset object,
        such as MyGrizzlyBearSet for the given package and subdirectory.
        'arguments' is a dictionary with keyword arguments passed to the dataset constructor.
        """
        (table_name, module_name, class_name) =  self._table_module_class_names_for_dataset(dataset_name)
        if module_name is None or class_name is None:
            return None
        if subdir:
            module_full_name = package + "." + subdir + "." + module_name
        else:
            module_full_name = package + "."  + module_name
        return ClassFactory().get_class(module_full_name, class_name=class_name,
                                        arguments=arguments, debug=debug)
 
    def search_for_dataset(self, dataset_name, package_order, **kwargs):
        for package_name in package_order:
            try:
                dataset = self.get_dataset(dataset_name, package=package_name, **kwargs)
                if dataset is not None:
                    break
            except ImportError:
                continue
        else:
            from opus_core.datasets.dataset import Dataset
            args = kwargs.get('arguments', {})
            storage=args.get('in_storage', None)
            try:
                dataset = Dataset(in_storage=storage, dataset_name=dataset_name, in_table_name=dataset_name, id_name="%s_id" % dataset_name)
            except:
                logger.log_warning("Could not create a generic Dataset '%s'." % dataset_name)
                raise
        return dataset
    
    def dataset_name_for_table(self, table_name):
        """
        Return the dataset name for this table, e.g. 'gridcell' for table 'gridcells'.
        If the table name is in 'exceptions', return the appropriate dataset name; otherwise
        just remove the final 's' from the table_name.  Note that just removing the final 's'
        won't work for words like 'cities', so these need to be in 'exceptions'.
        """
        for t in DatasetFactory.exceptions:
            if t[1]==table_name:
                return t[0]
        if not table_name.endswith('s'):
            raise ValueError, "table name %s doesn't end with 's' and not listed in 'exceptions' -- couldn't determine dataset name" % table_name
        return table_name[:-1]
     
    def compose_interaction_dataset_name(self, dataset1_name, dataset2_name):
        """Return a tuple with the module name and dataset name for an interaction dataset, given the dataset names
        for the two components"""
        (table1_name, module1_name, class1_name) =  self._table_module_class_names_for_dataset(dataset1_name)
        (table2_name, module2_name, class2_name) =  self._table_module_class_names_for_dataset(dataset2_name)
        return (module1_name + '_x_' + module2_name, class1_name[:-3] + class2_name)
        
    def create_datasets_from_flt(self, datasets_to_create, package_name, additional_arguments={}):
        """
        Returns a dictionary containing all of the loaded datasets.
        'datasets_to_create' is a dictionary where keys are the dataset names, values are dictionaries
        that can contain 'package_name' and 'arguments' (containing arguments to be passed 
        to the dataset constructor).
        additional_arguments is a dictionary specifying additional arguments for the constructor,
        e.g. in_storage.
        """
        datasets = {}
        # load required data from FLT files
        logger.log_status("Loading datasets from FLT cache")

        args = {}
        args.update(additional_arguments)
        for dataset_name, dataset_info in datasets_to_create.iteritems():
            argstmp = args.copy()
            
            if "arguments" in dataset_info.keys():
                argstmp.update(dataset_info["arguments"])
                
            datasets[dataset_name] = self.get_dataset(
                dataset_name, 
                package=dataset_info.get('package_name', package_name),
                subdir='datasets',
                arguments=argstmp)
                
            argstmp.clear()
            
        return datasets
    
    def _table_module_class_names_for_dataset(self, dataset_name):
        """
        Return a tuple consisting of the table name, the module name, and the class name for this dataset, e.g.
        ('development_events', 'development_event_dataset', 'DevelopmentEventDataset') for dataset 'development_event'.
        """
        # first check the exceptions
        for t in DatasetFactory.exceptions:
            if t[0]==dataset_name:
                return t[1:]
        table_name = dataset_name + 's'
        module_name = dataset_name + '_dataset'
        split_names = dataset_name.split('_')
        class_name = "".join(map(lambda name: name.capitalize(), split_names)) + "Dataset"
        return (table_name, module_name, class_name)


from numpy import array
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory

class DatasetFactoryTests(opus_unittest.OpusTestCase):
    def test_translations(self):
        factory = DatasetFactory()
        self.assertEqual(factory._table_module_class_names_for_dataset('gridcell'), ('gridcells','gridcell_dataset', 'GridcellDataset'))
        self.assertEqual(factory._table_module_class_names_for_dataset('development_event'), ('development_events','development_event_dataset', 'DevelopmentEventDataset'))
        self.assertEqual(factory.dataset_name_for_table('gridcells'), 'gridcell')
        self.assertEqual(factory.dataset_name_for_table('cities'), 'city')
        self.assertEqual(factory.compose_interaction_dataset_name('gridcell', 'household'), ('gridcell_dataset_x_household_dataset', 'GridcellDataHouseholdDataset'))
        self.assertEqual(factory.compose_interaction_dataset_name('squid_a', 'clam_b'), ('squid_a_dataset_x_clam_b_dataset', 'SquidADataClamBDataset'))
                         
    def test_get_dataset(self):
        factory = DatasetFactory()
        ds = factory.get_dataset("alldata")
        idname = ds.get_id_name()[0]
        self.assertEqual(idname, "id")
        self.assertEqual(ds.size(), 1)
        
    def test_create_generic_dataset(self):
        storage = StorageFactory().get_storage('dict_storage')
        data = {'attr1': array([1,3,4]), 'table_id': array([1,2,3])}
        storage.write_table(table_name = 'table', table_data = data)
        factory = DatasetFactory()
        ds = factory.search_for_dataset('table', ['opus_core'], arguments={'in_storage': storage})
        self.assertEqual(ds.get_id_name()[0], 'table_id')
        self.assertEqual(ds.get_dataset_name(), 'table')
        self.assertEqual(ds.size(), 3)
        
if __name__ == '__main__':
    opus_unittest.main()