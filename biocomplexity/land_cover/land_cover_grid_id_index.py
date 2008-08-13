#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import take, where, arange, zeros, ones


class land_cover_grid_id_index(Variable):
    """Given:
           - land_cover.devgrid_id, which maps lct id to urbansim grid_id
           - gridcell.grid_id
       This variable will return the index of grid_id for lct.
       This variable is used in computing devt, de, house_den, house_add,
           comm_den, and comm_add.

       For instance,
       Input:
           - devgrid_id: [1,1,2,3]
                   (lct 1 and 2 has grid id 1, lct 3 has grid_id 2, and...)
           - grid_id [1,2,3,5,7] (no duplicates)
       Output:
           [0,0,1,2]
    """
    grid_id = "grid_id"
    urbansim_mapping = "devgrid_id"

    def dependencies(self):
        # need dependency on commercial_sqft_lag_xxx too
        return [attribute_label("gridcell", self.grid_id),
                my_attribute_label(self.urbansim_mapping)]

    def compute(self, dataset_pool):
        lct_gridid_mapping = self.get_dataset().get_attribute(self.urbansim_mapping)
        lct_gridid_mapping_index = (-1*ones(lct_gridid_mapping.size)).astype("int32")
        nonnegative = where(lct_gridid_mapping > 0)[0]
        lct_gridid_mapping_index[nonnegative] = dataset_pool.get_dataset('gridcell').get_id_index(
                    lct_gridid_mapping[nonnegative])
        return lct_gridid_mapping_index # MUST return -1 if no mapping



from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest
#class Tests(opus_unittest.OpusTestCase):
class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.land_cover_grid_id_index"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name,
            {"land_cover":{
                "devgrid_id":array([1, 1, 2, 3, 7, 5, 2, -9999])},
             "gridcell":{
                "grid_id": array([1, 2, 3, 5, 7])}},
            dataset = "land_cover")
        should_be = array([0, 0, 1, 2, 4, 3, 1, -1])

        self.assert_(ma.allclose(values, should_be, rtol=1E-5),
                     msg = "Error in " + self.variable_name)


if __name__ == "__main__":
    opus_unittest.main()