# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros, maximum, where, logical_and

class max_developable_capacity(Variable):
    """ Maximum capacity over all generic land use types and over far, units_per_acre and units_per_lot
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
        for glu in list(parcels.development_constraints.keys()):
            if  glu == 'index':
                continue
            if 'far' in parcels.development_constraints[glu].keys():
                result = maximum(result, parcels.development_constraints[glu]['far'][:, 1]*parcels['parcel_sqft'])  #max constraint
            if 'units_per_acre' in parcels.development_constraints[glu].keys():
                #res_constraints = parcels.development_constraints[glu]['units_per_acre'][:, 1] * 5.96 * 1/43560.0# median of units_per_acre over templates times acre-to-sqft converter
                result = maximum(result, parcels.development_constraints[glu]['units_per_acre'][:, 1] /43560.0 * parcels['parcel_sqft'] * 1553) # median of building sqft per unit
            if 'units_per_lot' in parcels.development_constraints[glu].keys():
                units_per_lot = parcels.development_constraints[glu]['units_per_lot'][:, 1]
                result = maximum(result, (units_per_lot > 0) * where(
                                          parcels['parcel_sqft'] <= 10000, where(units_per_lot == 1, 500, 250) * units_per_lot * parcels['parcel_sqft']/1000, # small lots
                                          where(units_per_lot == 1, ((parcels['parcel_sqft'] - 10000)/1000 - 1) * 300 + 3300, # larger lots
                                                where(logical_and(units_per_lot > 1, units_per_lot < 4), units_per_lot * (((parcels['parcel_sqft']-10000)/1000 - 1) * 250 + (2750 - (500*(units_per_lot - 2)))),
                                                      units_per_lot * (((parcels['parcel_sqft'] - 10000)/1000 - 1) * 175 + (1925 - (275*(units_per_lot - 4)))))
                                                )
                                          ))
        return result

from opus_core.tests import opus_unittest
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
                'constraint_id': array([1,2,3,4, 5]),
                'is_constrained': array([0, 1, 1, 0, 1]),
                'generic_land_use_type_id': array([1, 1, 2, 2, 1]),
                'constraint_type':array(['units_per_acre','units_per_acre', 'far', 'far', 'units_per_lot']),                
                'minimum': array([1,  0,   0,  0, 2]),
                'maximum': array([3, 0.2, 10, 100, 6]),                
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
        # the FAR constraints dominate
        should_be = array([700, 2000, 50])
        
        instance_name = 'psrc_parcel.parcel.max_developable_capacity'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)
        
    def test_my_inputs_residential(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={
            'development_constraint':
            {
                'constraint_id': array([1,2,3, 4]),
                'is_constrained': array([1, 1, 1, 1]),
                'generic_land_use_type_id': array([1, 1, 1, 1]),
                'constraint_type':array(['units_per_acre','units_per_acre', 'units_per_lot', 'units_per_lot']),                
                'minimum': array([1,  0, 2, 2]),
                'maximum': array([3, 0.2, 6, 5]),                
            },
            'parcel':
            {
                "parcel_id":        array([1,   2,    3]),
                "is_constrained":   array([1,   1,    1]),
                'parcel_sqft': array([700, 9500, 10500])
            },
            'generic_land_use_type':
            {
                "generic_land_use_type_id":        array([1,   2]),
                "generic_land_use_type_name":      array(['',  '']),
            },
            }
        )
        # constraint 4 is selected as the minimum over maximum and determines the values here
        should_be = array([875, 11875, 7812.5])
        
        instance_name = 'psrc_parcel.parcel.max_developable_capacity'
        tester.test_is_close_for_family_variable(self, should_be, instance_name)        

if __name__=='__main__':
    opus_unittest.main()
