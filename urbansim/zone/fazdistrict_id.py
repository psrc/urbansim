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
from urbansim.functions import attribute_label

class fazdistrict_id(Variable):
    """The fazdistrict id of this zone"""
    
    faz_fazdistrict_id = "fazdistrict_id"
    
    def dependencies(self):
        return [my_attribute_label("faz_id"), 
                attribute_label("faz", self.faz_fazdistrict_id)]

    def compute(self, dataset_pool):
        fazes = dataset_pool.get_dataset('faz')
        return self.get_dataset().get_join_data(fazes, name=self.faz_fazdistrict_id)



from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.fazdistrict_id"

    def test_my_inputs(self):
        faz_id = array([4, 5, 6])
        fazdistrict_id = array([1,2,1])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "faz_id":faz_id}, 
             "faz":{
                "faz_id":faz_id, 
                "fazdistrict_id":fazdistrict_id}}, 
            dataset = "zone")
        should_be = array([1,2,1])
        
        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()