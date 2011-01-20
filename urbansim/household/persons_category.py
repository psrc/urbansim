# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import array

class persons_category(Variable):
    """
    return 
    1 for 1 persons
    2 for 2 persons
    3 for 2+ persons
    """

    def dependencies(self):
        return [my_attribute_label("persons")]

    def compute(self, dataset_pool):
        hhs = self.get_dataset()
        bins = array([1, 2])
        results = hhs.categorize("persons", bins) + 1

        return results

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household.persons_category"

    def test_my_inputs( self ):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1, 2, 3, 4]),
                'persons': array([1, 2, 3, 5]),
            }
        )
               
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household = dataset_pool.get_dataset('household')
        household.compute_variables(self.variable_name, 
                                    dataset_pool=dataset_pool)
        values = household.get_attribute(self.variable_name)

        should_be = array( [1, 2, 3, 3] )
        
        self.assert_(ma.allequal(values, should_be,), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()