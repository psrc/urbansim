# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import logical_or, zeros, int32, ones, float32, where
from scipy.ndimage import correlate, label, find_objects
from numpy import ma
from opus_core.variables.variable import Variable, ln
from biocomplexity.land_cover.variable_functions import my_attribute_label

class SSSmps(Variable):
    """Computes the mean size of all patches of covertypes of interest
                that are (partially) within each cell's footprint
    - The covertypes of interest are determined by the first character of this variable.
    - These are then translated into land_cover numbers from the constants resources.
    - need {"constants":{"FOOTPRINT":footprint,"HU":1...,"ALL_URBAN": ['HU', 'MU', 'LU']}}
       in resources when compute, where footprint=ones(shape=(5,5)).
    """

    land_cover_type = 'lct'
    standardization_constant_MPS = 10.0

    def __init__(self, covertype_symbol):
        Variable.__init__(self)
        self.covertype_symbol = covertype_symbol

    def dependencies(self):
        return [my_attribute_label(self.land_cover_type)]

    def compute(self, dataset_pool):
        constants = dataset_pool.get_dataset('constants')
        covertypes_of_interest = self._cover_type_translation(constants)
        lct = ma.filled(self.get_dataset().get_2d_attribute(self.land_cover_type), 0)
        footprint = constants['FOOTPRINT']
        is_lct_of_interest = reduce(lambda prev_answer, lct_num: logical_or(prev_answer, lct==lct_num),
                                    covertypes_of_interest,
                                    zeros(shape=lct.shape, dtype=int32))

        summed =  self._compute_patch_size_of_cover_types(is_lct_of_interest, footprint)
        return self.get_dataset().flatten_by_id(ln(summed + 1)
                                    / self.standardization_constant_MPS )

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
        pcount_corr = ma.masked_array(correlate(patchcount, footprint, mode="reflect", cval=0.0))
        psize_corr = correlate(patchsizes, footprint, mode="reflect", cval=0.0)
        return ma.filled(psize_corr / pcount_corr, 0)

    def _cover_type_translation(self, lookup_dict):
        "returns a list of lct number types based on the first_letter_of_name"
        if self.covertype_symbol == 'a':
            covertypes_of_interest = lookup_dict['ALL_URBAN']
        elif self.covertype_symbol == 'h':
            return [lookup_dict['HU']]
        elif self.covertype_symbol == 'm':
            covertypes_of_interest = lookup_dict['MED_LIGHT_URBAN']
        elif self.covertype_symbol == 'hm':
            covertypes_of_interest = lookup_dict['HEAVY_MED_URBAN']
        elif self.covertype_symbol == 'f':
            covertypes_of_interest = lookup_dict['FOREST']
        elif self.covertype_symbol == 'g':
            return [lookup_dict['GR']]
        else:
            raise RuntimeError("Sorry. Variable biocomplexity.land_cover.SSSmps was unable to meaningfully" + \
                               " translate characters SSS for variable instantiation %smps." % self.covertype_symbol)

        return map(lambda key: lookup_dict[key], covertypes_of_interest)


from numpy import array

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

from biocomplexity.tests.expected_data_test import ExpectedDataTest

class Tests(ExpectedDataTest):

    def test_my_inputs_for_hmps(self):
        variable_name = "biocomplexity.land_cover.hmps"
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
        dataset_pool._add_dataset(
            'constant',
            {
                "FOOTPRINT": array([[0,1,0], [1,1,1], [0,1,0]]),
                'HU': 1,
            }
        )

        land_cover = dataset_pool.get_dataset('land_cover')
        land_cover.compute_variables(variable_name,
                                     dataset_pool=dataset_pool)
        values = land_cover.get_attribute(variable_name)

        should_be = array([2, 2, 2, 2], dtype=float32)
        should_be = ln(should_be + 1) / SSSmps.standardization_constant_MPS

        self.assert_(ma.allclose( values, should_be, rtol=1e-7),
                     msg = "Error in " + variable_name)

    def test_my_inputs_for_amps(self):
        variable_name = "biocomplexity.land_cover.amps"
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='land_covers',
            table_data={
                'relative_x': array([1,2,3,1,2,3,1,2,3]),
                'relative_y': array([1,1,1,2,2,2,3,3,3]),
                "lct": array([1, 2, 3, 4, 5, 4, 3, 5, 1]),
            }
        )

        dataset_pool = DatasetPool(package_order=['biocomplexity'],
                                   storage=storage)
        dataset_pool._add_dataset(
            'constant',
            {
                "FOOTPRINT": array([[0,1,0], [1,1,1], [0,1,0]]),
                "ALL_URBAN": ['HU', 'MU', 'LU'],
                'HU': 1,
                'MU': 2,
                'LU': 3
            }
        )

        land_cover = dataset_pool.get_dataset('land_cover')
        land_cover.compute_variables(variable_name,
                                     dataset_pool=dataset_pool)
        values = land_cover.get_attribute(variable_name)

        should_be = array([3, 3, 3, 2, 3, 2, 1, 1, 1], dtype=float32)
        should_be = ln(should_be + 1) / SSSmps.standardization_constant_MPS

        self.assert_(ma.allclose( values, should_be, rtol=1e-7),
                     msg = "Error in " + variable_name)

    def test_no_translation(self):
        variable_name = "biocomplexity.land_cover.xmps"
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='land_covers',
            table_data={
                'relative_x': array([1,2,3,1,2,3,1,2,3]),
                'relative_y': array([1,1,1,2,2,2,3,3,3]),
                "lct": array([1, 2, 3, 4, 5, 4, 3, 5, 1]),
            }
        )

        dataset_pool = DatasetPool(package_order=['biocomplexity'],
                                   storage=storage)
        dataset_pool._add_dataset(
            'constant',
            {
                "FOOTPRINT": array([[0,1,0], [1,1,1], [0,1,0]]),
                "ALL_URBAN": ['HU', 'MU', 'LU'],
                'HU': 1,
                'MU': 2,
                'LU': 3
            }
        )

        land_cover = dataset_pool.get_dataset('land_cover')
        self.assertRaises(RuntimeError,
                          land_cover.compute_variables,
                          variable_name,
                          dataset_pool=dataset_pool)

    def test_on_expected_data(self):
        self.variable_name = "biocomplexity.land_cover.fmps"
        footprint = ones(shape=(5,5))
        self.do_test_on_expected_data(["relative_x","relative_y","lct"],
                                       {"constants":{"FOOTPRINT":footprint,
                                                     "ALL_URBAN": ['HU', 'MU', 'LU'],
                                                     'HU': 1,'MU': 2,'LU': 3,
                                                     'MF':6, 'CF':7,
                                                     'FOREST':['MF','CF'],
                                                     'GR':5}},
                                       element_atol=0.05)


if __name__=='__main__':
    opus_unittest.main()