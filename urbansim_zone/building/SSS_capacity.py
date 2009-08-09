# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros, argsort, logical_and

class SSS_capacity(Variable):
    """ [residential_units | non_residential_sqft] capacity
    The results are obtained by matching buildings to development_constraints
    """

    def __init__(self, space_type):
        self.capacity_type = space_type + "_capacity"
        Variable.__init__(self)

    def dependencies(self):
        return ["building.zone_id",
                "building.building_type_id", 
                "development_constraint.zone_id",
                "development_constraint.building_type_id",
                "development_constraint." + self.capacity_type]

    def compute(self, dataset_pool):
        buildings = self.get_dataset()
        zone_ids = buildings.get_attribute("zone_id")
        building_type_ids = buildings.get_attribute("building_type_id")
        constraints = -1 + zeros(buildings.size())
        
        development_constraints = dataset_pool.get_dataset("development_constraint")
        constraint_zone_ids = development_constraints.get_attribute("zone_id")
        constraint_building_type_ids = development_constraints.get_attribute("building_type_id")
        capacity = development_constraints.get_attribute(self.capacity_type)
        # sort with descending order on building_type, so building type id of "-2" is parsed last
        desc_order = argsort(constraint_building_type_ids)[::-1]
        constraint_zone_ids = constraint_zone_ids[desc_order]
        constraint_building_type_ids  = constraint_building_type_ids[desc_order]
        capacity = capacity[desc_order]
        
        for i in range(development_constraints.size()):
            zone_id = constraint_zone_ids[i]
            building_type_id = constraint_building_type_ids[i] 
            if building_type_id != -2:
                is_building_affected = logical_and( zone_ids==zone_id,
                                                             building_type_ids==building_type_id)
            else:
                is_building_affected = zone_ids==zone_id
            constraints[logical_and(is_building_affected, constraints==-1)] = capacity[i]
            
        return constraints

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)


from opus_core.tests import opus_unittest
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester


class Tests(opus_unittest.OpusTestCase):

    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_zone','urbansim'],
            test_data={
            'building':
            {"building_id":         array([1,  2, 3, 4,  5]),
             "zone_id":             array([1,  1, 3, 2,  2]),
             "building_type_id":    array([1,  2, 1, 1,  2]),
             },
            'development_constraint':
            {
             "constraint_id":                 array([1, 2, 3, 4, 5]),
             "zone_id":                       array([1, 1, 2, 2, 3]),
             "building_type_id":              array([1, 2, 2,-2,-2]),
             "residential_units_capacity":    array([7, 0, 3, 1, 4]),
             "non_residential_sqft_capacity": array([1, 8, 0, 2, 5])
             },
             
           }
        )
        
        should_be = array([7, 0, 4, 1, 3])
        instance_name = 'urbansim_zone.building.residential_units_capacity'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

        should_be = array([1, 8, 5, 2, 0])
        instance_name = 'urbansim_zone.building.non_residential_sqft_capacity'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)        
if __name__=='__main__':
    opus_unittest.main()