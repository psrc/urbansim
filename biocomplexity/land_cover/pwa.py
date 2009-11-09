# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import float32, arcsin, sqrt
from numpy import ma
from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label

class pwa(Variable):
    """Percent water within footprint.
      - need {"constants":{"FOOTPRINT":footprint,"OW":12}} in resources
          when compute, where footprint=ones(shape=(5,5), dtype="int32")."""
    land_cover_type_ow_within_footprint = 'land_cover_type_ow_within_footprint' # ow->open_water
    footprint_size = 'footprint_size'

    def dependencies(self):
        return [my_attribute_label(self.land_cover_type_ow_within_footprint),
                my_attribute_label(self.footprint_size)]

    def compute(self, dataset_pool):
        den = self.get_dataset().get_attribute(self.footprint_size).astype(float32)
        pct = self.get_dataset().get_attribute(self.land_cover_type_ow_within_footprint)
        return ma.filled(arcsin(sqrt(pct/den)), 0)


from numpy import array

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

from biocomplexity.tests.expected_data_test import ExpectedDataTest

class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.pwa"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='land_covers',
            table_data={
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
                "land_cover_type_ow_within_footprint": array([3, 2, 1, 0]),
                "footprint_size": array([5, 4, 5, 5])
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

        should_be = array([3, 2, 1, 0], dtype=float32) / array([5, 4, 5, 5], dtype=float32)
        should_be = arcsin(sqrt(should_be))

        self.assert_(ma.allclose( values, should_be, rtol=1e-7),
                     msg = "Error in " + self.variable_name)

    def test_on_expected_data(self):
        from numpy import ones
        footprint = ones(shape=(5,5), dtype="int32")
        self.do_test_on_expected_data(["lct","relative_x","relative_y"],
                                       {"constants":{"FOOTPRINT":footprint,"OW":12}},
                                      element_atol=0.07)


if __name__=='__main__':
    opus_unittest.main()