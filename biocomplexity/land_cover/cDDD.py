# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable, ln
from variable_functions import my_attribute_label
from numpy import ones
from scipy.ndimage import correlate
from numpy import ma

class cDDD(Variable):
    """commercial_sqft_recently_added_within_DDDm_window -
       - the number of commercial square feet added in the last
       three years inclusive of the current year:
           ln (commercial_sqft_recently_added_within_DDD_window + 1) / 10
       - correlates data from comm_add(Commercial
       square feet recently added) with footprint width=DDD,
       where DDD is in the unit dimension.
       - need {'constants':{"CELLSIZE":30}} in resources when compute
    """

    comm_add = "comm_add4"
    _return_type = "float32"

    def __init__(self, number):
        self.footprint_width = int(number)
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.comm_add)]

    def compute(self, dataset_pool):
        cellsize = dataset_pool.get_dataset('constants')['CELLSIZE']
        fpdimension = int(self.footprint_width / cellsize)
        fp = ones((fpdimension, fpdimension), dtype="int32")
        summed = correlate( ma.filled( self.get_dataset().get_2d_attribute( self.comm_add ), 0.0 ), \
                            fp, mode="reflect" )
        return ln(self.get_dataset().flatten_by_id(summed)+1)/10.0


from numpy import array

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

from biocomplexity.tests.expected_data_test import ExpectedDataTest

class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.c750"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='land_covers',
            table_data={
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
                "comm_add4": array([1, 2, 5, 15])
            }
        )

        dataset_pool = DatasetPool(package_order=['biocomplexity'],
                                   storage=storage)
        dataset_pool._add_dataset(
            'constant',
            {
                "CELLSIZE": 250    # this results in a 3x3 grid, (750/250)x(750/250)
            }
        )

        gridcell = dataset_pool.get_dataset('land_cover')
        gridcell.compute_variables(self.variable_name,
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)

        should_be = array([1*4+2*2+5*2+15, 1*2+2*4+5+15*2, 1*2+2+5*4+15*2, 1+2*2+5*2+15*4])
        should_be = ln(should_be + 1) / 10.0

        self.assert_(ma.allclose( values, should_be, rtol=1e-7),
                     msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()