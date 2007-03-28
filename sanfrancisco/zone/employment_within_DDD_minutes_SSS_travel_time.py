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
from variable_functions import my_attribute_label
from numpy import where, zeros, Float32, array
from numpy.nd_image import sum as nd_image_sum

class employment_within_DDD_minutes_SSS_travel_time(Variable):
    """total number of jobs for zones within DDD minutes SSS (mode) travel time,
    """
    def __init__(self, number, mode):
        self.minutes = number
        self.mode = mode
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("travel_data", self.mode),
                my_attribute_label("employment")]
    
    def compute(self,  dataset_pool):
        zone_ids = self.get_dataset().get_id_attribute()
        travel_data = dataset_pool.get_dataset("travel_data")
        within_indicator = (travel_data.get_attribute(self.mode) <= self.minutes)
        
        to_zone_id = travel_data.get_attribute("to_zone_id")
        zone_index = self.get_dataset().get_id_index(to_zone_id)
        num_jobs = self.get_dataset().get_attribute('employment')[zone_index]

        from_zone_id = travel_data.get_attribute("from_zone_id")        
        results = array(nd_image_sum(within_indicator * num_jobs, labels = from_zone_id, index=zone_ids))
        
        return results

if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numpy import array
    from numpy.ma import allclose
    from sanfrancisco.opus_package_info import package
    
    class Tests(unittest.TestCase):
        def get_values(self, number, mode):
            values = VariableTestToolbox().compute_variable(
                "sanfrancisco.zone.employment_within_%s_minutes_%s_travel_time" % (number, mode),
                {"zone":{
                    "zone_id":array([1,3]),
                    "employment":array([10, 1])},
                 "travel_data":{
                     "from_zone_id":array([3,3,1,1]),
                     "to_zone_id":array([1,3,1,3]),
                     mode:array([1.1, 2.2, 3.3, 4.4])}},
                dataset = "zone", package=package())
            return values

        def test_to_2(self):
            values = self.get_values(2, 'hwy')
            should_be = array([0, 10])
            self.assert_(allclose(values, should_be, rtol=1e-4), "Error in employment_within_2_minutes_hwy_travel_time")

        def test_to_4(self):
            values = self.get_values(4, 'bart')
            should_be = array([10, 11])
            self.assert_(allclose(values, should_be, rtol=1e-4), "Error in employment_within_4_minutes_bart_travel_time")

    unittest.main()