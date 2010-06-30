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

from numpy import sometrue, array, ravel, logical_not, zeros, float32, maximum, equal, int32
from numpy import arcsin, sqrt
from numpy import ma
from scipy.ndimage import maximum_filter, correlate

from opus_core.variables.variable import Variable

from biocomplexity.land_cover.variable_functions import my_attribute_label

class shei(Variable):
    """Shannon's evenness index (SHEI), computed in a 5x5 moving window
      - need {"constants":{"FOOTPRINT":footprint}} in resources when compute
           where footprint=ones(shape=(5,5))"""
    land_cover_type = 'lct'
    
    def dependencies(self):
        return [my_attribute_label(self.land_cover_type)]     
        
    def _get_cover_types(self, lct):
        """Return a list of landcover types present in the lct grid"""
        x = []
        max_type = int(maximum.reduce(ravel(lct)))
        for itype in range(1, max_type+1):
            if sometrue(ravel(lct) == itype):
                x = x + [itype]
        return array(x)
        
    def _count_covertypes_within_window(self, lct, cover_type_list, footprint):
        """Return integer array indicating the number of different covertypes
        of interest that are within the moving window (footprint)"""
        m = zeros(shape=lct.shape, dtype=int32)
        for cover_type in cover_type_list:
            m += maximum_filter(equal(lct, cover_type), footprint=footprint)
        return m
        
    def _compute_pct_cover_type_within_footprint(self, lct, cover_type, footprint, lct_mask):
        """Calculates percentage of one covertype within the footprint"""
        temp = equal(lct, cover_type)
        # use ma.masked_array to prevent divide-by-zero warnings
        mask_invert = logical_not(lct_mask)  # in numpy import ma.masked, 0 == valid
        pixels = ma.masked_array(correlate(mask_invert.astype(int32), footprint, mode="reflect"))
        values = correlate(temp.astype(int32), footprint, mode="reflect")
        return ma.filled(values / pixels.astype(float32), 0)
        
    def _compute_shannon_evenness_index(self, lct, footprint, lct_mask):        
        """Compute Shannon's evenness index"""
        cover_types_list = self._get_cover_types(lct)
        numerator_sum = ma.masked_array(zeros(shape=lct.shape, dtype=float32),
                                           mask=lct_mask)
        for cover_type in cover_types_list:
            pi = self._compute_pct_cover_type_within_footprint(lct, cover_type, footprint, lct_mask)
            numerator_sum += pi*ma.filled(ma.log(pi), 0)

        m = self._count_covertypes_within_window(lct, cover_types_list, footprint)

        return ma.filled(-numerator_sum / ma.log(m), 0).astype(float32)
    
    def compute(self, dataset_pool):
        constants = dataset_pool.get_dataset('constants')
        footprint = constants["FOOTPRINT"]
        lct = ma.filled(self.get_dataset().get_2d_attribute(self.land_cover_type), 0)
        lct_mask = self.get_dataset().get_mask(is_2d_version=True)
        shei = self._compute_shannon_evenness_index(lct, footprint, lct_mask)
        return self.get_dataset().flatten_by_id(arcsin(sqrt(shei)))

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

from biocomplexity.tests.expected_data_test import ExpectedDataTest

class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.shei"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='land_covers',
            table_data={
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
                "lct": array([1, 2, 1, 4]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['biocomplexity'],
                                   storage=storage)

        gridcell = dataset_pool.get_dataset('land_cover')
        gridcell.compute_variables(self.variable_name, 
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)
        
        should_be = array([1.42948067, 1.18391383, 1.42948103, 1.18391371])
        
        self.assert_(ma.allclose( values, should_be, rtol=1e-6), 
                     msg = "Error in " + self.variable_name)

    def test_on_expected_data(self):
        self.do_test_on_expected_data(["relative_x","relative_y","lct"],
                                      element_atol=0.3)


if __name__ == "__main__":            
    opus_unittest.main()