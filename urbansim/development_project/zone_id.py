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
from variable_functions import my_attribute_label

class zone_id(Variable):
    """The Trafic Analysis Zone id of this project. """

    gc_zone_id = "zone_id"
    
    def dependencies(self):
        return [my_attribute_label("grid_id"), "gridcell.%s" % self.gc_zone_id]
        
    def compute(self, dataset_pool):
        developmentprojects = self.get_dataset()
        gridcells = dataset_pool.get_dataset('gridcell')
        return developmentprojects.get_join_data(gridcells, name=self.gc_zone_id)
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.development_project.zone_id"

    def test_my_inputs(self):
        grid_id = array([2, 1, 3])
        zone_id = array([4, 5, 6])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"development_project":{ 
                "grid_id":grid_id}, 
             "gridcell":{ 
                "zone_id":zone_id} }, 
            dataset = "development_project")
        should_be = array([5,4,6])
        
        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()