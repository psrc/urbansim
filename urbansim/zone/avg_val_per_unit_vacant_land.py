# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from opus_core.misc import safe_array_divide

class avg_val_per_unit_vacant_land(Variable):
    """Aggregated over gridcells"""

    _return_type = "float32"
            
    def dependencies(self):
        return [attribute_label("gridcell", "total_value_vacant_land"), 
                 attribute_label("gridcell", "zone_id"), 
                 my_attribute_label("vacant_land_sqft")]
    
    def compute(self, dataset_pool):
        vl = self.get_dataset().get_attribute("vacant_land_sqft").astype("float32")
        return safe_array_divide(self.get_dataset().sum_dataset_over_ids(dataset_pool.get_dataset('gridcell'),
                "total_value_vacant_land"), vl)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.avg_val_per_unit_vacant_land"

    def test_my_inputs(self):
        avg_value = array([22,22,27,42, 9]) 
        some_gridcell_zone_ids = array([1,2,1,3, 2]) 
        grid_id = array([1,2,3,4,5])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{
                "zone_id":array([1,2, 3])},
            "gridcell":{ 
                "avg_val_per_unit_vacant_land":avg_value,
                "vacant_land_sqft": array([2, 5, 0, 10, 3]),
                "zone_id":some_gridcell_zone_ids, 
                "grid_id":grid_id}}, 
            dataset = "zone")
        should_be = array([22, 137/8.0, 42])
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-4), True, msg = "Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()