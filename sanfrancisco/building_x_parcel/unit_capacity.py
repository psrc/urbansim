# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import unique, zeros

class unit_capacity(Variable):
    """ return parcel's unit_capacity for given buildings according to their unit_capacity_name  
    """

    _return_type="int32"
    
    def dependencies(self):
        return [
                "sanfrancisco.building_type.unit_capacity_name",
                "unit_capacity_name=building.disaggregate(building_type.unit_capacity_name)"
                ]

    def compute(self,  dataset_pool):
        bldg_x_parcel = self.get_dataset()
        bt = dataset_pool.get_dataset("building_type")
        results = zeros(bldg_x_parcel.get_2d_index().shape, dtype=self._return_type)
        for unit_capacity_name in unique(bt.get_attribute('unit_capacity_name')):
            self.add_and_solve_dependencies("sanfrancisco.parcel.%s" % unit_capacity_name, dataset_pool)
            is_of_this_unit_capacity_name = bldg_x_parcel.get_attribute('unit_capacity_name')==unit_capacity_name
            results[is_of_this_unit_capacity_name] = bldg_x_parcel.get_attribute(unit_capacity_name)[is_of_this_unit_capacity_name]

        return results

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['sanfrancisco','urbansim'],
            test_data={
            'building_type':
            {
                "building_type_id":array([1,2,3,4]),
                "class_id":array([1,2,1,2]),
                },
            'building_type_classification':
            {
                "class_id":array([1,2]),
                "name": array(["nonresidential","residential"]),
                "unit_name":array(["building_sqft","residential_units"]),
                "unit_capacity_name":array(["building_sqft_capacity","residential_units_capacity"])
                },
            "building":{
                'building_id': array([1, 2, 3, 4, 5]),
                'building_type_id': array([1, 2, 3, 4, 3]),
                'building_sqft': array([1000, 200, 0, 400, 1500]),
                'residential_units': array([0, 2, 0, 40, 5]),
                #                           sqft, ru, sqft, ru, sqft 
                },
            "parcel":{
                'parcel_id': array([1, 2, 3, 4, 5]),
                'building_sqft_capacity':     array([2000, 400, 0, 800, 3000]),
                'residential_units_capacity': array([0, 4, 0, 42, 6]),
                },
                
        }
        )
        
        should_be = array([
            [2000, 400, 0, 800, 3000],
            [0, 4, 0, 42, 6],
            [2000, 400, 0, 800, 3000],
            [0, 4, 0, 42, 6],
            [2000, 400, 0, 800, 3000]
        ])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()