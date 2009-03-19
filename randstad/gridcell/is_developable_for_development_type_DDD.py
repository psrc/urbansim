# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros, logical_or, where
from variable_functions import my_attribute_label

class is_developable_for_development_type_DDD(Variable):
    """Boolean indicating whether the gridcell is developable to convert to landuse type DDD"""

    def __init__(self, number):
        self.tnumber = number
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label('development_type_id')]

    def compute(self, dataset_pool):
        filter = dataset_pool.get_dataset('development_filter')
        idx_to_id = where(filter.get_attribute('to_development_type_id')==self.tnumber)
        valid_from_ids = filter.get_attribute('from_development_type_id')[idx_to_id]
        results = zeros(self.get_dataset().size(), dtype="?")
        for id in valid_from_ids:
            results = logical_or(results, self.get_dataset().get_attribute('development_type_id')==id)
        return results

    def post_check(self, values, dataset_pool):
        self.do_check("x == True or x == False", values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
#from opus_core.datasets.dataset import Dataset
from urbansim.datasets.dataset import Dataset
from numpy import array
from numpy import ma
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "randstad.gridcell.is_developable_for_development_type_2"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        landuse_filter_table_name = 'landuse_filter'
        storage.write_table(
                table_name=landuse_filter_table_name,
                table_data={
                     'id':array([1,2,3,4]),
                     'from_development_type_id':array([1,1,3,5]),
                     'to_development_type_id':array([4,6,2,2])
                     },
            )

        landuse_filter = Dataset(
            id_name = 'id',
            in_storage = storage,
            in_table_name = landuse_filter_table_name,
            )

        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'gridcell':{
                    'development_type_id':array([1,2,5])
                    },
                'development_filter':landuse_filter
                },
            dataset = 'gridcell'
            )

        should_be = array([0, 0, 1])

        self.assert_(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()