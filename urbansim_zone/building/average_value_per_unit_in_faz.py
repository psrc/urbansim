# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from numpy import ones, zeros, column_stack, logical_and, all
from opus_core.misc import ndsum

class average_value_per_unit_in_faz(Variable):
    """"""
    
    def dependencies(self):
        return ["building.average_value_per_unit",
                "building.building_type_id", 
                "building.zone_id",
                "faz_id = building.disaggregate(zone.faz_id)"]
        
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        results = zeros(ds.size(), dtype=ds.get_attribute("average_value_per_unit").dtype)
        labels = column_stack([ds.get_attribute_as_column("faz_id"), ds.get_attribute_as_column("building_type_id")])
        values, indices1 = ndsum(ds.get_attribute("average_value_per_unit"), labels)
        counts, indices2 = ndsum(ones(ds.size()), labels)
        for i1, i2 in zip(indices1, indices2):
            assert all(i1 == i2)
        for faz_id, building_type_id, result, count in zip(indices1[0], indices1[1], values, counts):
            results[logical_and(ds.get_attribute("faz_id")==faz_id, ds.get_attribute("building_type_id")==building_type_id)] = float(result) / count

        return results

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
            {
                'building_id':            array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                'zone_id':                array([1, 2, 3, 4, 1, 2, 3, 2, 3, 4]),
            #   'faz_id':                 array([1, 2, 3, 1, 1, 2, 3, 2, 3, 1]) 
                'building_type_id':       array([1, 1, 1, 1, 1, 2, 2, 2, 2, 2]),
                'average_value_per_unit': array([19.0, 2000.0, 310.0, 400.0, 0.0, 5000.0, 300.0, 45.0, 79.0, 200.0]),
                },
            'zone':
            {
                'zone_id':array([1, 2, 3, 4]),
                'faz_id' :array([1, 2, 3, 1]) 
             },
           }
        )
        
        should_be = array([139.666667, 2000, 310, 139.6666667, 139.6666667, 2522.5, 189.5, 2522.5, 189.5, 200])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()