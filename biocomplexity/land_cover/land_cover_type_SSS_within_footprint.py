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
#

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from scipy.ndimage import correlate
from numpy import ma
from numpy import equal, int32

class land_cover_type_SSS_within_footprint(Variable):
    """Sums land covers of type SSS (short string version, predefined) over footprint"""

    land_cover_types = 'lct'

    def __init__(self, lct_type):
        Variable.__init__(self)
        self.lct_type = lct_type

    def dependencies(self):
        return [my_attribute_label(self.land_cover_types)]

    def compute(self, dataset_pool):
        constants = dataset_pool.get_dataset('constants')
        footprint = constants["FOOTPRINT"]
        lct = ma.filled(self.get_dataset().get_2d_attribute(self.land_cover_types), 0)
        temp = equal(lct, constants[self.lct_type.upper()])
        values = correlate(temp.astype(int32), footprint, mode="reflect")
        return self.get_dataset().flatten_by_id(ma.filled(values, 0))


from numpy import array

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "biocomplexity.land_cover.land_cover_type_ag_within_footprint"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='land_covers',
            table_data={
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
                "lct": array([4, 4, 5, 1])
            }
        )
        
        dataset_pool = DatasetPool(package_order=['biocomplexity'],
                                   storage=storage)
        footprint = array([[0,1,0], [1,1,1], [0,1,0]])
        dataset_pool._add_dataset(
            'constant',
            {
                "FOOTPRINT": footprint,
                'AG': 4,
            }
        )

        gridcell = dataset_pool.get_dataset('land_cover')
        gridcell.compute_variables(self.variable_name, 
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)
        
        should_be = array([4, 4, 1, 1])
        
        self.assert_(ma.allequal( values, should_be), 
                     msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()