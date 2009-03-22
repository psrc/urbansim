# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import where

class SSS_sqft(Variable):
    """building space of given type."""

    _return_type="int32"

    def __init__(self, type):
        self.is_type_variable = "is_building_type_%s" % type
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.is_type_variable),
                my_attribute_label("sqft")]

    def compute(self, dataset_pool):
        buildings = self.get_dataset()
        sqft = buildings.get_attribute("sqft")
        return where(buildings.get_attribute(self.is_type_variable), sqft, 0)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)



from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from urbansim.datasets.building_type_dataset import BuildingTypeDataset
from numpy import array
from numpy import ma
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.building.commercial_sqft"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        building_types_table_name = 'building_types'
        storage.write_table(
                table_name=building_types_table_name,
                table_data={
                    'building_type_id':array([1,2]),
                    'name': array(['foo', 'commercial'])
                    }
            )

        building_types = BuildingTypeDataset(in_storage=storage, in_table_name=building_types_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'building': {
                    'building_type_id': array([1,2,1,2,1,1]),
                    'sqft': array([100, 350, 1000, 0, 430, 95])
                    },
                'building_type': building_types
                },
            dataset = 'building'
            )

        should_be = array([0, 350, 0, 0, 0, 0])

        self.assertEqual(ma.allequal(values, should_be), True, msg = 'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()