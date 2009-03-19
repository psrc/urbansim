# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class development_type_name(Variable):
    """return development type name"""

    def dependencies(self):
        return [my_attribute_label("development_type_id")]

    def compute(self, dataset_pool):
        devtype = dataset_pool.get_dataset('development_type')
        names = devtype.get_attribute('name')
        ids = self.get_dataset().get_attribute('development_type_id')
        devtype_index = devtype.get_id_index(ids)
        return names[devtype_index]

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.development_type_dataset import DevelopmentTypeDataset
from numpy import array, alltrue
class Tests(opus_unittest.OpusTestCase):
    variable_name = "randstad.gridcell.development_type_name"

    def test_my_inputs(self):
        """"""
        storage = StorageFactory().get_storage('dict_storage')

        devtype_table_name = 'devtype'        
        storage.write_table(
                table_name=devtype_table_name,
                table_data={
                    'development_type_id':array([1,2,3]),
                    'name':array(['residential', 'commercial', 'industrial'])
                    }
            )
        
        devtype=DevelopmentTypeDataset(
            in_storage = storage,
            in_table_name = devtype_table_name,
            id_name='development_type_id',
            use_groups=False,
            )
            
        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'gridcell':{ 
                    'development_type_id':array([1, 1, 2, 3])
                    },
                'development_type':devtype
                }, 
            dataset = 'gridcell'
            )
            
        should_be = array(['residential', 'residential', 'commercial', 'industrial'])
        
        self.assert_(alltrue(values == should_be), 
            'Error in ' + self.variable_name )


if __name__=='__main__':
    opus_unittest.main()