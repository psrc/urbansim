# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class fazdistrict_id(Variable):
    """The Forecast Analysis Zone id of this household. """

    gc_fazdistrict_id = "fazdistrict_id"
    
    def dependencies(self):
        return [my_attribute_label("grid_id"), attribute_label("gridcell", self.gc_fazdistrict_id)]
        
    def compute(self, dataset_pool):
        developmentprojects = self.get_dataset()
        gridcells = dataset_pool.get_dataset('gridcell')
        return developmentprojects.get_join_data(gridcells, name=self.gc_fazdistrict_id)
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.development_project.fazdistrict_id"

    def test_my_inputs(self):
        grid_id = array([2, 1, 3])
        fazdistrict_id = array([4, 5, 6])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"development_project":{ 
                "grid_id":grid_id}, 
             "gridcell":{ 
                "fazdistrict_id":fazdistrict_id} }, 
            dataset = "development_project")
        should_be = array([5,4,6])
        
        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()