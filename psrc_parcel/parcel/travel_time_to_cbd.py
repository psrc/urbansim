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
from urbansim.functions import attribute_label
from numarray.nd_image import correlate
from numarray.ma import filled
from opus_core.logger import logger

class travel_time_to_cbd(Variable):
    """get travel_time_to_cbd from gridcell"""

    def dependencies(self):
        return [attribute_label('gridcell', "grid_id"),
                attribute_label('gridcell', "travel_time_to_CBD"),
                my_attribute_label('grid_id')]

    def compute(self,  dataset_pool):
        gcs = dataset_pool.get_dataset("gridcell")
        parcels = self.get_dataset()
        return parcels.get_join_data(gcs, "travel_time_to_CBD")

    def post_check(self,  values, dataset_pool):
        units_max = dataset_pool.get_dataset('gridcell').get_attribute("travel_time_to_CBD").max()
        self.do_check("0 <= x and x <= " + str(units_max), filled(values,0))

if __name__=='__main__':
    logger.log_status("running test")
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numarray import array
    from numarray.ma import allclose
    from opus_core.resources import Resources
    from psrc_parcel.datasets.parcels import ParcelSet
    class Tests(unittest.TestCase):
        variable_name = "psrc_parcel.parcel.travel_time_to_cbd"

        def test_my_inputs(self):
            travel_time_to_cbd = array([100, 1000, 1500])
            
            resources = Resources({'data':
                                   {"parcel_id":array([1,2,3,4,5]),
                                    "grid_id":array([1, 1, 3, 2, 3])
                                    },
                                  })
            parcels = ParcelSet(resources=resources, in_storage_type="RAM")

            values = VariableTestToolbox().compute_variable(self.variable_name, \
                { "gridcell":{ \
                      "grid_id":array([1, 2, 3]),
                      "travel_time_to_CBD":travel_time_to_cbd}, \
                  "parcel":parcels }, \
                  dataset = "parcel" )
            should_be = array([100.0, 100.0, 1500.0, 1000.0, 1500.0])

            self.assertEqual(allclose(values, should_be, rtol=1e-7), \
                             True, msg = "Error in " + self.variable_name)

    unittest.main()