# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


from numpy import ma
import os.path

from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.datasets.dataset import Dataset
from opus_core.misc import opus_path_for_variable_from_module_path
from opus_core.variables.variable_family_name_translator import VariableFamilyNameTranslator


class VariableTester(object):
    """A class providing a simple api to do unit tests of Opus variables."""

    def __init__(self, file_path, package_order, test_data):
        """
        file_path is the directory path to the module defining the variable
            to be tested.  The name of the variable to be tested is extracted
            from this path.  As a special case, if the file_path ends in tests/variablename.py, 
            we assume that this is a tests subdirectory with just a unit test, and 
            remove the tests/ part to find the module name.
        package_order is the sequence of Opus packages in which to look for the
            dataset class modules for the datasets used in this test.
        test_data is a dictionary of data for the datasets to use in this test,
            where the key is the name of the dataset and the values are
            dictionaries containing the attribute data in numpy containers,
            e.g.:

            test_data={
                'gridcell':{
                    'grid_id': array([1, 2]),
                    'attribute_1': array([10, 20]),
                    },
                'household':{
                    'household_id': array([1, 2]),
                    'grid_id': array([1, 2]),
                },
                }
            If the dataset does not its own class to be created with, it must have
            an attribute 'id' which is the unique identifier of the dataset.
        """
        (dirname, filename) = os.path.split(file_path)
        (front, lastdir) = os.path.split(dirname)
        if lastdir=='tests':
            self.file_path = os.path.join(front,filename)
        else:
            self.file_path = file_path
        storage = StorageFactory().get_storage('dict_storage')
        self.dataset_pool = DatasetPool(package_order=package_order)
        for dataset_name, attribute_dict in test_data.iteritems():
            storage.write_table(table_name=dataset_name, table_data=attribute_dict)
        for dataset_name, attribute_dict in test_data.iteritems(): # the two loops are needed because
            dataset = None                                         # of possible dependencies of one dataset on another
            for package in package_order:
                try: # try to create a specific dataset using given packages
                    dataset = DatasetFactory().get_dataset(dataset_name, package=package,
                                                           arguments={"in_table_name": dataset_name,
                                                                      "in_storage": storage})
                    break
                except:
                    local_resources = {
                        'dataset_name': dataset_name,
                        'in_table_name': dataset_name,
                        'package': package,
                        'in_storage': storage
                        #'values': attribute_dict
                    }
                    try:
                        dataset = DatasetFactory().get_dataset(dataset_name, package=package,
                                                           arguments={"resources": local_resources})
                        break
                    except:
                        pass
            if dataset is None:
                try: # try to create general dataset
                    dataset = Dataset(dataset_name=dataset_name,
                                      id_name="id",
                                      in_table_name=dataset_name,
                                      in_storage=storage)

                except:
                    raise StandardError, "Error in creating dataset %s." % dataset_name
            self.dataset_pool._add_dataset(dataset_name, dataset)

    def _get_attribute(self, given_variable_name=None):
        """Compute and then return the value of this attribute."""
        variable_name = opus_path_for_variable_from_module_path(self.file_path)
        if given_variable_name and \
           VariableFamilyNameTranslator().compare_instance_name_of_module_to_variable_name(
               given_variable_name,
               variable_name):
            variable_name = given_variable_name
        dataset_name = variable_name.split('.')[1]
        dataset = self.dataset_pool.get_dataset(dataset_name)
        dataset.compute_variables(variable_name, self.dataset_pool)
        return dataset.get_attribute(variable_name)

    def test_is_equal_for_variable_defined_by_this_module(self, test_class, should_be):
        """Complain if the variable of the calling module is not within
        this tolerance of these should_be values."""
        values = self._get_attribute()

        test_class.assert_(ma.allequal(values, should_be),
                           "Error in %s: \n Expected %s \n Actual   %s" % (
                               self.file_path, should_be, values))

    def test_is_close_for_variable_defined_by_this_module(self, test_class, should_be, rtol=1e-7):
        """Complain if the variable of the calling module is not within
        this tolerance of these should_be values."""
        values = self._get_attribute()

        test_class.assert_(ma.allclose(values, should_be, rtol),
                           "Error in %s: \n Expected %s \n Actual   %s" % (
                               self.file_path, should_be, values))



    def test_is_equal_for_family_variable(self, test_class, should_be, variable_name=None):
        """Complain if the variable of the calling module is not within
        this tolerance of these should_be values.

        The variable_name must be an instance of the family variable defined
        by the calling module.
        """

        values = self._get_attribute(variable_name)

        test_class.assert_(ma.allequal(values, should_be),
                           "Error in %s: \n Expected %s \n Actual   %s" % (
                               self.file_path, should_be, values))

    def test_is_close_for_family_variable(self, test_class, should_be, variable_name=None, rtol=1e-7):
        """Complain if the variable of the calling module is not within
        this tolerance of these should_be values.

        The variable_name must be an instance of the family variable defined
        by the calling module.
        """

        values = self._get_attribute(variable_name)

        test_class.assert_(ma.allclose(values, should_be, rtol),
                           "Error in %s: \n Expected %s \n Actual   %s" % (
                               self.file_path, should_be, values))

import os

from numpy import array

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    """Since an Opus variable must exist in a module with the same name and in
    a directory of the dataset name, we use the opus_core/test/attr1_times_2
    module for this test."""
    def test(self):
        tester = VariableTester(
            os.path.join('anything_you_want_here', 'opus_core', 'test', 'attr1_times_2.py'),
            package_order=['opus_core'],
            test_data={
                'test':{
                    'id': array([1, 2]),
                    'attr1': array([1, 2]),
                    },
            }
        )

        should_be = array([1*2, 2*2])

        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()