#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

from opus_core.variable import Variable
from variable_functions import my_attribute_label

class population(Variable):
    """Number of households in a given parcel"""

    _return_type="Int32"
    
    def dependencies(self):
        return ["sanfrancisco.household.building_id", 
                "sanfrancisco.household.persons", 
                my_attribute_label("building_id")]

    def compute(self,  dataset_pool):
        households = dataset_pool.get_dataset("household")
        return self.get_dataset().sum_dataset_over_ids(households, "persons")

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("household").get_attribute("persons").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)

if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numarray import array
    from numarray.ma import allclose
    from opus_core.resources import Resources
    from sanfrancisco.datasets.building_dataset import BuildingDataset
    from opus_core.storage_factory import StorageFactory        
    class Tests(unittest.TestCase):
        variable_name = "sanfrancisco.building.population"
        def test(self):

            values = VariableTestToolbox().compute_variable(self.variable_name, \
                {"building":{"building_id": array([1,2,3,4,5,6]),}, \
                 "household":{
                              "building_id":array([1,2,2,2,1,5]),
                              "persons":array([2,1,1,5,3,7]),
                              }}, \
                dataset = "building")
            should_be = array([5,7,0,0,7,0])
            
            self.assertEqual(allclose(values, should_be, rtol=1e-20), \
                             True, msg = "Error in " + self.variable_name)
    unittest.main()