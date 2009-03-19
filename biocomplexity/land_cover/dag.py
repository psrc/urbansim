# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE


from opus_core.variables.variable import Variable, ln
from numpy import int32, less_equal, ones, bool8, float32, where, zeros
from scipy.ndimage import correlate, distance_transform_edt, label, find_objects
from numpy import ma
from biocomplexity.land_cover.variable_functions import my_attribute_label


class dag(Variable):
    """ln_distance_to_agricultural_area (distance copmuted variable):
        ln (( pixel distance to nearest pixel with ag_mps > 400 30-m pixels) + 1) / 10
       - need {'constant':{"FOOTPRINT":footprint, 'AG':10}} in resources when compute
       where footprint=ones(shape=(5,5))
    """

    land_cover_type = 'lct'
    standardization_constant_distance = 10.0
    _return_type = "float32"

    def dependencies(self):
        return [my_attribute_label(self.land_cover_type)]

    def compute(self, dataset_pool):
        constants = dataset_pool.get_dataset('constant')
        ag = constants["AG"]
        lct = ma.filled(self.get_dataset().get_2d_attribute(self.land_cover_type), 0)
        footprint = constants['FOOTPRINT']
        is_lct_ag = lct==ag
        summed = self._compute_patch_size_of_cover_types(is_lct_ag, footprint)
        summed = less_equal(summed, 400).astype(bool8)
        distances = distance_transform_edt(summed)
        return self.get_dataset().flatten_by_id(ln(distances + 1)
                                   / self.standardization_constant_distance )

    def _compute_patch_size_of_cover_types(self, lct, footprint):
        """Computes the mean size of all patches of covertypes of interest
        that are (partially) within each cell's footprint"""
        eightway_structure = ones((3,3), dtype="int32") # put this to class variable will result in error
        patchsizes = zeros(shape=lct.shape, dtype=float32)
        patchcount = zeros(shape=lct.shape, dtype=float32)

        labels, n  = label(lct, eightway_structure)
        slices = find_objects(labels)
        # Summing the 0/1 mask gives the patch size
        for ip in range(n):
            locmask = where(labels[slices[ip]]==(ip+1),lct[slices[ip]],0)
            patchcount[slices[ip]] += locmask
            patchsizes[slices[ip]] += locmask.sum()*locmask
            del locmask
        pcount_corr = correlate(patchcount, footprint, mode="reflect", cval=0.0)
        psize_corr = correlate(patchsizes, footprint, mode="reflect", cval=0.0)
        nonzeros = where (pcount_corr <> 0)
        result = zeros(psize_corr.shape, dtype=float32)
        result[nonzeros] = psize_corr[nonzeros]/pcount_corr[nonzeros]
        return result


from numpy import array, ravel, transpose

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

from biocomplexity.tests.expected_data_test import ExpectedDataTest

class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.dag"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='land_covers',
            table_data={
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
                "lct": array([10,10,4,3])
            }
        )

        dataset_pool = DatasetPool(package_order=['biocomplexity'],
                                   storage=storage)
        footprint = array([[0,1,0], [1,1,1], [0,1,0]])
        dataset_pool._add_dataset(
            'constant',
            {
                "FOOTPRINT": footprint,
                'AG': 10,
            }
        )

        gridcell = dataset_pool.get_dataset('land_cover')
        gridcell.compute_variables(self.variable_name,
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)

        should_be = array([[1,1],[0,0]])
        should_be = correlate(ma.filled(should_be.astype(int32), 0), footprint, mode="reflect")
        should_be = less_equal((should_be/5.0), 400)
        should_be = ln(distance_transform_edt(should_be)+1) / dag.standardization_constant_distance
        should_be = ravel(transpose(should_be)) # flatten by id

        self.assert_(ma.allclose( values, should_be, rtol=1e-7),
                     msg = "Error in " + self.variable_name)

    def test_on_expected_data(self):
        footprint = ones(shape=(5,5), dtype="int32")
        self.do_test_on_expected_data(["lct","relative_x","relative_y"],
                                       {'constant':{"FOOTPRINT":footprint, 'AG':10}})


if __name__ == "__main__":
    opus_unittest.main()
