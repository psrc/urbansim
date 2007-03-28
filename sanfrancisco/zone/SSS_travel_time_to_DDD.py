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

from opus_core.logger import logger
from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import where, zeros, Float32

class SSS_travel_time_to_DDD(Variable):
    """Travel time by mode SSS to the zone whose ID is the DDD.
    """
    def __init__(self, mode, number):
        self.mode = mode
        self.dzone_id = number
        self.my_name = "%s_travel_time_to_%s" % (self.mode, self.dzone_id)
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("travel_data", self.mode),
                attribute_label("travel_data", "from_zone_id"),
                attribute_label("travel_data", "to_zone_id")
                ]
    
    def compute(self,  dataset_pool):
        zone_id = self.get_dataset().get_id_attribute()
        keys = map(lambda x: (x, self.dzone_id), zone_id)
        travel_data = dataset_pool.get_dataset("travel_data")
        try:
            time = travel_data.get_attribute_by_id(self.mode, keys)
        except:
            logger.log_warning("Variable %s returns zeros, since zone number %d is not in zoneset." % (self.my_name, self.dzone_id))
            time = zeros(self.get_dataset().size(), type=Float32)
        return time

if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numpy import array
    from numpy.ma import allclose
    from psrc.opus_package_info import package
    
    class Tests(unittest.TestCase):
        def get_values(self, number):
            values = VariableTestToolbox().compute_variable(
                "sanfrancisco.zone.hwy_travel_time_to_%d" % number,
                {"zone":{
                    "zone_id":array([1,3])},
                 "travel_data":{
                     "from_zone_id":array([3,3,1,1]),
                     "to_zone_id":array([1,3,1,3]),
                     "hwy":array([1.1, 2.2, 3.3, 4.4])}},
                dataset = "zone", package=package())
            return values

        def test_to_1(self):
            values = self.get_values(1)
            should_be = array([3.3, 1.1])
            self.assert_(allclose(values, should_be, rtol=1e-4), "Error in hwy_travel_time_to_1")

        def test_to_3(self):
            values = self.get_values(3)
            should_be = array([4.4, 2.2])
            self.assert_(allclose(values, should_be, rtol=1e-4), "Error in hwy_travel_time_to_3")

    unittest.main()