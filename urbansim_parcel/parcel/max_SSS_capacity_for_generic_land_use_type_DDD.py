# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label

class max_SSS_capacity_for_generic_land_use_type_DDD(Variable):
    """ minimum SSS capacity (far, units_per_acre, etc) allowed by development constraints
    
    """

    def __init__(self, constraint_type, generic_land_use_type):
        Variable.__init__(self)
        self.constraint_type = constraint_type
        self.generic_land_use_type = generic_land_use_type

    def dependencies(self):
        return ["development_constraint.constraint_type"]

    def compute(self,  dataset_pool):
        parcels = dataset_pool.get_dataset("parcel")
        constraints = dataset_pool.get_dataset("development_constraint") 
        parcels.get_development_constraints(constraints, dataset_pool, consider_constraints_as_rules=True)
        
        constraint = parcels.development_constraints[self.generic_land_use_type][self.constraint_type][:, 1]  #max constraint
        
        return constraint

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={
            'development_constraint':
            {
                'constraint_id': array([1,2,3,4]),
                'is_constrained': array([0, 1, 1, 0]),
                'generic_land_use_type_id': array([1, 1, 2, 2]),
                'constraint_type':array(['units_per_acre','units_per_acre', 'far', 'far']),                
                'minimum': array([1,  0,   0,  0]),
                'maximum': array([3, 0.2, 10, 100]),                
            },
            'parcel':
            {
                "parcel_id":        array([1,   2,    3]),
                "is_constrained":   array([1,   0,    1]),
            },
            'generic_land_use_type':
            {
                "generic_land_use_type_id":        array([1,   2]),
                "generic_land_use_type_name":      array(['',  '']),
            },
            }
        )
        
        should_be = array([10, 100, 10])
        
        instance_name = 'urbansim_parcel.parcel.max_far_capacity_for_generic_land_use_type_2'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
