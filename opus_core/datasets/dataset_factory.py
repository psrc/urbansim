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
        - an dataset name is all lower case with '_', such as 'my_grizzly_bear'
        - the corresponding dataset is implemented in a module 'my_grizzly_bears.py'
        - the input data for this dataset is in table 'my_grizzly_bears'
        - the dataset is called 'MyGrizzlyBearSet'
    """
    def get_dataset(self, dataset_name, subdir="datasets", package="opus_core", 
                    arguments={}, debug=0):
        """If the above conventions are fulfilled, this method returns a Dataset object, such
           as MyGrizzlyBearSet for the given package and subdirectory.
           'arguments' is a dictionary with keyword arguments passed to the dataset constructor.
        """
        module_name = self._module_name_for_dataset(dataset_name)
        class_name = self.class_name_for_dataset(dataset_name)
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
                break
            except ImportError:
                continue
        else:
            raise Exception("Dataset '%s' not found in any of the "
                    "packages: '%s'." % (dataset_name, "', '".join(package_order)))
        return dataset
    
    def class_name_for_dataset(self, dataset_name):
        """
        Return the class name for this dataset, e.g. 'DevelopmentEventDataset' for 
        dataset 'development_event'.
        """
        split_names = dataset_name.split('_')
        class_name = "".join(map(lambda name: name.capitalize(), split_names)) + "Dataset"
        return class_name
    
    def _module_name_for_dataset(self, dataset_name):
        """
        Return the module name for this dataset, e.g. 'gridcell_dataset' for dataset 'gridcell'.
        In Opus, the convention is that the class name is same as the module name.
        """
        return '%s_dataset' % dataset_name
       
    %TODO: the method below is incorrect 
    def table_name_for_dataset(self, dataset_name):
        """
        Return the table name for this dataset, e.g. 'gridcells' for dataset 'gridcell'.
        In Opus, the convention is that the table name is same as the module name.
        """
        return self._module_name_for_dataset(dataset_name)
     
    def compose_interaction_dataset_name(self, dataset1_name, dataset2_name):
        module1 = self._module_name_for_dataset(dataset1_name)
        dataset1_class_name = self.class_name_for_dataset(dataset1_name)
        module2 = self._module_name_for_dataset(dataset2_name)
        dataset2_class_name = self.class_name_for_dataset(dataset2_name)
        return (module1 + '_x_' + module2, dataset1_class_name[:-3] + dataset2_class_name)
        
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


from opus_core.tests import opus_unittest
class DatasetFactoryTests(opus_unittest.OpusTestCase):
    def test_translations(self):
        factory = DatasetFactory()
        self.assertEqual(factory._module_name_for_dataset('foo'), 'foo_dataset')
        self.assertEqual(factory._module_name_for_dataset('foo_bar'), 'foo_bar_dataset')
        self.assertEqual(factory.class_name_for_dataset('development_event'), 'DevelopmentEventDataset')
        self.assertEqual(factory.class_name_for_dataset('my_city'), 'MyCityDataset')
        self.assertEqual(factory.class_name_for_dataset('taz'), 'TazDataset')
        self.assertEqual(factory.class_name_for_dataset('some_moss'), 'SomeMossDataset')
        self.assertEqual(factory.class_name_for_dataset('my_data'), 'MyDataDataset')
                         
    def test_get_dataset(self):
        factory = DatasetFactory()
        ds = factory.get_dataset("alldata")
        idname = ds.get_id_name()[0]
        self.assertEqual(idname, "id")
        self.assertEqual(ds.size(), 1)
        
        
if __name__ == '__main__':
    opus_unittest.main()