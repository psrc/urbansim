# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from numpy import zeros

class existing_units(Variable):
    """total number of units (residential units or sqft), which are defined by land_use_types
    """
    _return_type = "int32"
    
    def dependencies(self):
        return [my_attribute_label("unit_name"),
                my_attribute_label("building_sqft"),
                my_attribute_label("residential_units"),
                my_attribute_label("parcel_sqft"),
                ]

    def compute(self, dataset_pool):
        parcels = self.get_dataset()
        unit_name = parcels.get_attribute("unit_name")
        results = zeros(parcels.size(), dtype=self._return_type)
        for name in ["building_sqft", "parcel_sqft", "residential_units"]:
            w = unit_name == name
            results[w] = parcels.get_attribute(name)[w].astype(self._return_type)
        return results

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from numpy import array, int32
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
            'parcel':
            {
                "parcel_id":        array([1,   2,    3]),
                "land_use_type_id": array([1,   2,    3 ]),
                "parcel_sqft": array([1, 50,  200],dtype=int32),
            },
            'building':
            {
                "building_id":array([1, 2, 3, 4]),
                "parcel_id":  array([1, 1, 2, 3]),
                "building_sqft": array([1000, 0, 2000, 3000]),
                "residential_units": array([0, 7, 4,   2]),
            },
            'land_use_type':
            {
                "land_use_type_id":array([1,  2, 3]),
                "unit_name":  array(["residential_units", "parcel_sqft", "building_sqft"])
            }
        })
        should_be = array([7, 50, 3000])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
