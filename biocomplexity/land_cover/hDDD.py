# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable, ln
from .variable_functions import my_attribute_label
from numpy import ones
from scipy.ndimage import correlate
from numpy import ma

class hDDD(Variable):
    """residential_units_recently_added_within_DDD_window -
     - the number of residential units added in the last three years
     inclusive of the current year
         ln (residential_units_recently_added_within_DDD_window_cell + 1) / 10
     - correlates data from house_add(Residential units recently added)
     with footprint width=DDD, where DDD is of the distance-unit dimension.
     - need {'constant':{"CELLSIZE":30}} in resources when compute."""

    house_add = "house_add4"
    _return_type = "float32"

    def __init__(self, number):
        Variable.__init__(self)
        self.footprint_width = int(number)

    def dependencies(self):
        return [my_attribute_label(self.house_add)]

    def compute(self, dataset_pool):
        cellsize = dataset_pool.get_dataset('constants')['CELLSIZE']
        fpdimension = int(self.footprint_width / cellsize)
        fp = ones((fpdimension, fpdimension), dtype="int32")
        summed = correlate( ma.filled( self.get_dataset().get_2d_attribute( self.house_add ), 0.0 ), \
                            fp, mode="reflect" )
        return self.get_dataset().flatten_by_id( ln(summed+1)/10 )


from numpy import array

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

from biocomplexity.tests.expected_data_test import ExpectedDataTest

class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.h450"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='land_covers',
            table_data={
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
                "house_add4":array([0, 2, 5, 15])
            }
        )

        dataset_pool = DatasetPool(package_order=['biocomplexity'],
                                   storage=storage)
        dataset_pool._add_dataset(
            'constant',
            {
                 "CELLSIZE":150  # this results in a 3x3 grid, (450/150)x(450/150)
            }
        )

        gridcell = dataset_pool.get_dataset('land_cover')
        gridcell.compute_variables(self.variable_name,
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)

        should_be = array([2*2+5*2+15, 2*4+5+15*2, 2+5*4+15*2, 2*2+5*2+15*4])
        should_be = ln(should_be + 1) / 10.0

        self.assertTrue(ma.allclose( values, should_be, rtol=1e-7),
                     msg = "Error in " + self.variable_name)

    def atest_on_expected_data(self):
        self.do_test_on_expected_data(["house_add","relative_x","relative_y","lct"],
                                        {'constant':{"CELLSIZE":30}})


if __name__=='__main__':
    opus_unittest.main()