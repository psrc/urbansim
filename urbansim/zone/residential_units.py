# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from abstract_sum_from_gridcells import abstract_sum_from_gridcells

class residential_units(abstract_sum_from_gridcells):
    """Number of residential units are in the zone.
    """
    _return_type="int32"
    gc_variable = "residential_units"


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.residential_units"

    def test_my_inputs(self):
        resunits = array([120,30,54,24]) 
        some_gridcell_zone_ids = array([3,2,1,1]) #zi[i]=(zone the ith gridcell belongs to)

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{
                "zone_id":array([1,2,3])}, 
            "gridcell":{ 
                "residential_units":resunits,
                "zone_id":some_gridcell_zone_ids}}, 
            dataset = "zone")
        should_be = array([78, 30, 120])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=0), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()