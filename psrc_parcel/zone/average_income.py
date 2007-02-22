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

class average_income(Variable):
    """average income in a given zone"""

    _return_type="Int32"
    
    def dependencies(self):
        return ["psrc_parcel.household.zone_id", 
                "psrc_parcel.household.income", 
                my_attribute_label("zone_id")]

    def compute(self,  dataset_pool):
        households = dataset_pool.get_dataset("household")
        return self.get_dataset().aggregate_dataset_over_ids(households, "mean", "income")

    def post_check(self,  values, dataset_pool=None):
        imin = dataset_pool.get_dataset("household").get_attribute("income").min()
        imax = dataset_pool.get_dataset("household").get_attribute("income").max()
        self.do_check("x >= %s and x <= %s" % (imin, imax), values)

if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numarray import array
    from numarray.ma import allclose
    from opus_core.resources import Resources
    from psrc_parcel.datasets.parcels import ParcelSet
    
    class Tests(unittest.TestCase):
        variable_name = "psrc_parcel.zone.average_income"
        def test(self):

            values = VariableTestToolbox().compute_variable(self.variable_name, \
                {"zone":{
                     "zone_id":array([1,2,3,4])}, \
                 "household":{
                              "zone_id":array([1, 1, 4, 4, 1, 2]),
                              "income":array([10, 0, 7, 2, 3, 5]),
                              }}, \
                dataset = "zone")
            should_be = array([13/3, 5.0, 0, 9/2])
            
            self.assertEqual(allclose(values, should_be, rtol=1e-20), \
                             True, msg = "Error in " + self.variable_name)
    unittest.main()