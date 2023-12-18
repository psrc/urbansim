# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


from opus_core.variables.variable import Variable, ln
from biocomplexity.land_cover.variable_functions import my_attribute_label
from scipy.ndimage import distance_transform_edt
from numpy import zeros, logical_not, float32, equal
from numpy import ma


class ddt1(Variable):
    """ln_distance_to_development:
            ln ((distance in meters to nearest pixel with LCT from 1 to 3) + 1) / 10
       - need {'constant':{"CELLSIZE":30, "ALL_URBAN":['HU', 'MU', 'LU'],
               'HU': 1, 'MU': 2, 'LU': 3}} in resources when compute

    """
    land_cover_type = 'lct'
    standardization_constant_distance = 10.0

    def dependencies(self):
        return [my_attribute_label(self.land_cover_type)]

    def compute(self, dataset_pool):
        constants = dataset_pool.get_dataset('constants')
        cellsize = constants["CELLSIZE"]
        all_urban_types = constants["ALL_URBAN"]
        all_urban_types = [constants[key] for key in all_urban_types]
        lct = ma.filled(self.get_dataset().get_2d_attribute(self.land_cover_type), 0)
        is_lct_all_urban = zeros(shape=lct.shape, dtype="int32")
        for urban_type in all_urban_types:
            is_lct_all_urban += equal(lct, urban_type)
        temp = logical_not(is_lct_all_urban)
        dd = ln(cellsize*(distance_transform_edt(temp))+1) / self.standardization_constant_distance
        return self.get_dataset().flatten_by_id(dd).astype(float32)



from numpy import array

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

from biocomplexity.tests.expected_data_test import ExpectedDataTest

class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.ddt1"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='land_covers',
            table_data={
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
                "lct": array([11,2,4,3])
            }
        )

        dataset_pool = DatasetPool(package_order=['biocomplexity'],
                                   storage=storage)
        dataset_pool._add_dataset(
            'constant',
            {
                "CELLSIZE":30,
                "ALL_URBAN":['HU', 'MU', 'LU'],
                'HU': 1,
                'MU': 2,
                'LU': 3
            }
        )

        gridcell = dataset_pool.get_dataset('land_cover')
        gridcell.compute_variables(self.variable_name,
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)

        should_be = array([1, 0, 1, 0], dtype=float32)
        should_be = ln(30*distance_transform_edt(should_be)+1) / ddt1.standardization_constant_distance

        self.assertTrue(ma.allclose( values, should_be, rtol=1e-7),
                     msg = "Error in " + self.variable_name)

    def test_on_expected_data(self):
        self.do_test_on_expected_data(["lct","relative_x","relative_y"], {'constant':{
                "CELLSIZE":30,
                "ALL_URBAN":['HU', 'MU', 'LU'],
                'HU': 1,
                'MU': 2,
                'LU': 3}})


if __name__ == "__main__":
    opus_unittest.main()