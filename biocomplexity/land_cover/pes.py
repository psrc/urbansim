# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label
from numpy import arcsin, sqrt, zeros, float32, maximum, ravel, equal, int32
from numpy import ma
from scipy.ndimage import correlate


class pes(Variable):
    """percentage_pixels_of_same_land_cover_class_within_150_grid_cell
        arcsin( square root ((sum over p in cell.150m, if LCTx == focal_cell_land_cover)
                / number of valid (not water) pixels in 150 m window ))
       - need {"constants":{"FOOTPRINT":footprint}} in resources when compute
           where footprint=ones(shape=(5,5))."""
    land_cover_type = 'lct'
    footprint_size = 'footprint_size'

    def dependencies(self):
        return [my_attribute_label(self.footprint_size)]

    def compute(self, dataset_pool):
        constants = dataset_pool.get_dataset('constant')
        fs = ma.filled(self.get_dataset().get_2d_attribute(self.footprint_size).astype(float32), 0)
        lct = ma.filled(self.get_dataset().get_2d_attribute(self.land_cover_type), 0)
        x = zeros(shape=lct.shape, dtype=float32)
        max_type = int(maximum.reduce(ravel(lct)))
        for itype in range(1, max_type+1):
            temp = equal(lct, itype).astype(int32)
            summed = correlate(ma.filled(temp, 0.0),
                               constants['FOOTPRINT'],
                               mode="reflect")
            x += temp * ma.filled(summed / ma.masked_where(fs==0, fs), 0.0)
        return self.get_dataset().flatten_by_id(arcsin(sqrt(x)))


from numpy import array

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

from biocomplexity.tests.expected_data_test import ExpectedDataTest

class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.pes"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='land_covers',
            table_data={
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
                "lct": array([3, 2, 1, 0]),
                "footprint_size": array([5, 5, 5, 5])
            }
        )

        dataset_pool = DatasetPool(package_order=['biocomplexity'],
                                   storage=storage)
        footprint = array([[0,1,0], [1,1,1], [0,1,0]])
        dataset_pool._add_dataset(
            'constant',
            {
                "FOOTPRINT": footprint,
            }
        )

        gridcell = dataset_pool.get_dataset('land_cover')
        gridcell.compute_variables(self.variable_name,
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)

        should_be = array([3,3,3,0]) / array([5, 5, 5, 5], dtype=float32)
        should_be = arcsin(sqrt(should_be))

        self.assert_(ma.allclose( values, should_be, rtol=1e-7),
                     msg = "Error in " + self.variable_name)

    def test_on_expected_data(self):
        from numpy import ones
        footprint = ones(shape=(5,5), dtype="int32")
        self.do_test_on_expected_data(["lct","relative_x","relative_y"],
                                        {"constants":{"FOOTPRINT":footprint}},
                                       element_atol=0.162)


if __name__ == "__main__":
    opus_unittest.main()