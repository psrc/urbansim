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

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset import Dataset
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array

class Tests(opus_unittest.OpusTestCase):
    """various tests of error handling"""
 
    # for a fully-qualified variable and an ordinary dataset (not an interaction set), the dataset name 
    # component of the variable name must match the name of the owner dataset
    def test_mismatched_dataset_name_fully_qualified_variable(self):
        expr = "opus_core.tests.a_test_variable"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='testzz',
            table_data={
                "a_dependent_variable":array([1,5,10]),
                "id":array([1,3,4])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='testzz', id_name="id", dataset_name="testzz")
        self.assertRaises(StandardError, dataset.compute_variables, [expr])
        
    def test_mismatched_dataset_name_expression(self):
        expr = "sqrt(opus_core.tests.a_test_variable)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='testzz',
            table_data={
                "a_dependent_variable":array([1,5,10]),
                "id":array([1,3,4])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='testzz', id_name="id", dataset_name="testzz")
        self.assertRaises(StandardError, dataset.compute_variables, [expr])

    def test_aggregate_bad_list(self):
        # the 'intermediates' argument must be a list -- test this
        expr = "zone.aggregate(2*gridcell.my_variable, intermediates=None)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='zones',
            table_data={
                'zone_id':array([1,2]),
                }
            )
        storage.write_table(
            table_name='gridcells',
            table_data={
                'my_variable':array([4,8,0.5,1]), 
                'grid_id':array([1,2,3,4]),
                'zone_id':array([1,2,1,2]),
                }
            )
        zone_dataset = Dataset(in_storage=storage, in_table_name='zones', id_name="zone_id", dataset_name='zone')
        gridcell_dataset = Dataset(in_storage=storage, in_table_name='gridcells', id_name="grid_id", dataset_name='gridcell')
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('gridcell', gridcell_dataset)
        dataset_pool._add_dataset('zone', zone_dataset)
        self.assertRaises(ValueError, zone_dataset.compute_variables, [expr], dataset_pool=dataset_pool)
               
    def test_aggregate_bad_function(self):
        # the 'function' argument must be a single name -- test this
        expr = "zone.aggregate(2*gridcell.my_variable, function=3+4)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='zones',
            table_data={
                'zone_id':array([1,2]),
                }
            )
        storage.write_table(
            table_name='gridcells',
            table_data={
                'my_variable':array([4,8,0.5,1]), 
                'grid_id':array([1,2,3,4]),
                'zone_id':array([1,2,1,2]),
                }
            )
        zone_dataset = Dataset(in_storage=storage, in_table_name='zones', id_name="zone_id", dataset_name='zone')
        gridcell_dataset = Dataset(in_storage=storage, in_table_name='gridcells', id_name="grid_id", dataset_name='gridcell')
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('gridcell', gridcell_dataset)
        dataset_pool._add_dataset('zone', zone_dataset)
        self.assertRaises(ValueError, zone_dataset.compute_variables, [expr], dataset_pool=dataset_pool)
               
    def test_bogus_alias_for_primary_attribute(self):
        # persons is used as an alias and is also a primary attribute
        expr = "persons = junk"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='tests',
            table_data={
                "persons":array([1,5,10]),
                "id":array([1,3,4])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='tests', id_name="id", dataset_name="tests")
        self.assertRaises(ValueError, dataset.compute_variables, [expr])

    def test_duplicate_alias1(self):
        exprs = ["x = opus_core.tests.a_test_variable", "x = a_dependent_variable"]
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='tests',
            table_data={
                "a_dependent_variable":array([1,5,10]),
                "id":array([1,3,4])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='tests', id_name="id", dataset_name="tests")
        self.assertRaises(ValueError, dataset.compute_variables, exprs)

    def test_duplicate_alias2(self):
        exprs = ["x = a_dependent_variable", "x = opus_core.tests.a_test_variable"]
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='tests',
            table_data={
                "a_dependent_variable":array([1,5,10]),
                "id":array([1,3,4])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='tests', id_name="id", dataset_name="tests")
        self.assertRaises(ValueError, dataset.compute_variables, exprs)

    def test_two_statements(self):
        # test the case of giving two statements
        expr = "x=2*var1\ny=var2"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset',
            table_data={"var1": array([4,-8,0.5,1]), "var2": array([3,3,7,7]), "id": array([1,2,3,4])}
            )
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        self.assertRaises(ValueError, dataset.compute_variables, [expr])

    def test_syntax_error(self):
        expr = "x = 2 var1"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset',
            table_data={"var1": array([4,-8,0.5,1]), "id": array([1,2,3,4])}
            )
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        self.assertRaises(SyntaxError, dataset.compute_variables, [expr])

if __name__=='__main__':
    opus_unittest.main()
