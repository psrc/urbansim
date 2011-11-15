# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros, maximum

class max_developable_capacity(Variable):
    """ Maximum capacity over all generic land use types and over far and units_per_acre 
        allowed by development constraints. 
        The median of building sqft per unit (1553) is used.
        Obsolete: The units-to-sqft conversion is approximated by taking the median density over residential templates, which is 5.96 units_per_acre.
    """

    def dependencies(self):
        return ["development_constraint.constraint_type"]

    def compute(self,  dataset_pool):
        parcels = dataset_pool.get_dataset("parcel")
        constraints = dataset_pool.get_dataset("development_constraint") 
        parcels.get_development_constraints(constraints, dataset_pool, consider_constraints_as_rules=True)
        result = zeros(parcels.size())
        # iterate over GLU types
        for glu in parcels.development_constraints.keys():
            if  glu == 'index':
                continue
            result = maximum(result, parcels.development_constraints[glu]['far'][:, 1]*parcels['parcel_sqft'])  #max constraint
            #res_constraints = parcels.development_constraints[glu]['units_per_acre'][:, 1] * 5.96 * 1/43560.0# median of units_per_acre over templates times acre-to-sqft converter
            res_constraints = parcels.development_constraints[glu]['units_per_acre'][:, 1] /43560.0 * parcels['parcel_sqft'] * 1553 # median of building sqft per unit
            result = maximum(result, res_constraints)
        return result

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
                'parcel_sqft': array([70, 20, 5])
            },
            'generic_land_use_type':
            {
                "generic_land_use_type_id":        array([1,   2]),
                "generic_land_use_type_name":      array(['',  '']),
            },
            }
        )
        
        should_be = array([700, 2000, 50])
        
        instance_name = 'psrc_parcel.parcel.max_developable_capacity'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
