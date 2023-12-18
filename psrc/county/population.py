# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from .variable_functions import my_attribute_label
from opus_core.logger import logger

class population(Variable):
    """Number of people in county"""
    _return_type="int32"

    def dependencies(self):
        return [attribute_label("gridcell", "county_id"), 
                attribute_label("gridcell", "population"), 
                my_attribute_label("county_id")]

    def compute(self, dataset_pool):
        gridcell = dataset_pool.get_dataset('gridcell')
        return self.get_dataset().sum_over_ids(gridcell.get_attribute("county_id"), 
                                   gridcell.get_attribute("population"))

    def post_check(self, values, dataset_pool):
        size = dataset_pool.get_dataset('gridcell').get_attribute("population").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
    
class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.county.population"
 
    def test_my_inputs(self):
        population = array([21,22,27,42]) 
        gridcell_county_ids = array([1,2,1,3]) 
        grid_id = array([1,2,3,4])
            
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"county":{
                "county_id":array([1,2, 3])}, \
            "gridcell":{ \
                "population":population,\
                "county_id":gridcell_county_ids, \
                "grid_id":grid_id}}, \
            dataset = "county")

        should_be = array([48, 22, 42])
            
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), \
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()