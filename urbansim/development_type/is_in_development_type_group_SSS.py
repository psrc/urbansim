# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import zeros, int8, bool8

class is_in_development_type_group_SSS(Variable):
    """Returns a boolean indicating whether this gridcell's development type group is
    of given name (by SSS)."""

    def __init__(self, group):
        self.group = group
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("development_group", "group_id"),
                attribute_label("development_group", "name"),
                my_attribute_label("development_type_id"),
                attribute_label("development_type", "development_type_id")]

    def compute(self, dataset_pool):
        result = zeros(self.get_dataset().size(),dtype=int8)
        groups = dataset_pool.get_dataset('development_group')
        group_id = groups.get_id_attribute()[groups.get_attribute("name")==self.group]
        if group_id.size == 0:
            return result
        group_id = group_id[0]
        devtypes = self.get_dataset().get_attribute("development_type_id")
        types_in_group = self.get_dataset().get_types_for_group(group_id)
        for type in types_in_group:
            result = result + (devtypes == type)
        return result.astype(bool8)

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from urbansim.datasets.development_type_dataset import DevelopmentTypeDataset
from numpy import array, arange
from numpy import ma
from opus_core.storage_factory import StorageFactory


#emulates the development type resource and implements the method we're interested in (are_in_group)
class mock_developmenttype(DevelopmentTypeDataset):
    groups = {
              #"development_type_id":"group_id"
              1:[1,2],
              2:[2],
              3:[2]
              }

    def get_types_for_group(self, group):
        ids = arange(self.size())+1
        is_group = array(map(lambda idx: group in self.groups[idx], ids), dtype="bool8")
        return ids[is_group]

    def get_devtype_groups(self):
        pass

class Tests(opus_unittest.OpusTestCase):
    variable_name1 = "urbansim.development_type.is_in_development_type_group_mixed_use"
    variable_name2 = "urbansim.development_type.is_in_development_type_group_high_density_residential"
    def test_my_inputs( self ):

        storage = StorageFactory().get_storage('dict_storage')

        development_type_table_name = 'development_type'
        storage.write_table(
            table_name=development_type_table_name,
            table_data={
                'development_type_id':array([1,2,3])
                }
            )

        development_type_dataset = mock_developmenttype(
            in_storage = storage,
            in_table_name = development_type_table_name,
            use_groups = False
            )

        values = VariableTestToolbox().compute_variable(self.variable_name1,
            data_dictionary = {
                'development_type':development_type_dataset,
                'development_group':{
                    'name':array(['mixed_use', 'high_density_residential']),
                    'group_id':array([1,2])
                    }
                },
            dataset = 'development_type'
            )

        should_be = array( [True, False, False] )

        self.assert_( ma.allequal( values, should_be),
            'Error in ' + self.variable_name1 )

        values = VariableTestToolbox().compute_variable( self.variable_name2,
            data_dictionary = {
                'development_type':development_type_dataset,
                'development_group':{
                    'name':array(['mixed_use', 'high_density_residential', 'low_density_residential']),
                    'group_id':array([1,2,3])
                    }
                },
            dataset = 'development_type'
            )

        should_be = array( [True, True, True] )

        self.assert_( ma.allequal( values, should_be),
            'Error in ' + self.variable_name2 )


if __name__=='__main__':
    opus_unittest.main()