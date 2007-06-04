#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class number_of_jobs_without_resource_construction_sectors(Variable):
    """How many jobs are in the county, excluding those in resource and construction sectors.
"""
    _return_type="int32"
    
    
    def dependencies(self):
        return ["psrc.gridcell.number_of_jobs_without_resource_construction_sectors", 
                attribute_label("gridcell", "county_id")]
    
    def compute(self, dataset_pool):
        return self.get_dataset().sum_dataset_over_ids(dataset_pool.get_dataset('gridcell'), 
                "number_of_jobs_without_resource_construction_sectors")


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
    
class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.county.number_of_jobs_without_resource_construction_sectors"
 
    def test_my_inputs(self):
        number_of_jobs = array([21,22,27,42]) 
        some_gridcell_county_ids = array([1,2,1,3]) #zi[i]=(zone the ith gridcell belongs to)
        grid_id = array([1,2,3,4])
          
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"county":{
                "county_id":array([1,2, 3])}, \
            "gridcell":{ \
                "number_of_jobs_without_resource_construction_sectors":number_of_jobs,\
                "county_id":some_gridcell_county_ids, \
                "grid_id":grid_id}}, \
            dataset = "county")
        should_be = array([48, 22, 42])
          
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), \
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()