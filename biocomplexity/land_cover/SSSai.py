# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


from numpy import float32, arcsin, sqrt, int32, floor, power, where, zeros, logical_or
from numpy import ma
from scipy.ndimage import correlate

from opus_core.variables.variable import Variable

from biocomplexity.land_cover.variable_functions import my_attribute_label

class SSSai(Variable):
    """Landscape Metric Computed Variables
        - aggregation_index_'urban_type'_within_150_grid_cell.
        - need {"constants":{"FOOTPRINT":footprint, 'GR':5...}} in resources when compute
       where footprint=ones(shape=(5,5))
    """
    land_cover_type = 'lct'
    _return_type = "float32"
    def __init__(self, covertype_symbol):
        Variable.__init__(self)
        self.covertype_symbol = covertype_symbol

    def dependencies(self):
        return [my_attribute_label(self.land_cover_type)]

    def _find_adjacency(self, lctmask, p1, p2, footprint):
        """helper function for aggregation index computation
        Detects a specific one-way adjacency within each cell's neighborhood,
        between the two points specified by the tuples p1 and p2."""
        adjfp = zeros(shape=footprint.shape, dtype=float32)
        adjfp[p1] = 0.5     # correlate with weights of 0.5 to count
        adjfp[p2] = 0.5        # adjacencies in one direction only
        # do correlation; setting output_type=int32 truncates result, skipping
        # pairs that are not "real" adjacencies
        return correlate(lctmask, adjfp, mode="constant", cval=0.0).astype(int32)

    def compute(self, dataset_pool):
        constants = dataset_pool.get_dataset('constants')
        footprint = constants["FOOTPRINT"]
        covertypes_of_interest = self._cover_type_translation(constants)
        lct = ma.filled(self.get_dataset().get_2d_attribute(self.land_cover_type), 0)
        is_lct_of_interest = reduce(lambda prev_answer, lct_num: logical_or(prev_answer, lct==lct_num),
                                    covertypes_of_interest,
                                    zeros(shape=lct.shape, dtype=int32))
        # maxg: maximum number of possible like-adjacencies within a window
        # a_i: # of cells of target covertypes within moving window
        a_i = correlate(ma.filled(is_lct_of_interest.astype(int32), 0),
                               footprint, mode="reflect", cval=0.0)
        n = floor(sqrt(a_i))
        m = a_i - power(n, 2)
        maxg = 2*n*(n-1)
        maxg += where(m==0, 0, where(m<=n, (2*m-1), where(m>n, (2*m-2), 0)))

        # detect all adjacencies by systematically checking each possibility
        # within the 5x5 footprint window
        gii = ma.masked_array(zeros(shape=lct.shape, dtype=int32))
        for ri in range(0, footprint.shape[0]):
            for ci in range(0, footprint.shape[1]-1):
                gii += self._find_adjacency(is_lct_of_interest, (ri,ci), (ri,ci+1), footprint)

        for ri in range(0, footprint.shape[0]-1):
            for ci in range(0, footprint.shape[1]):
                gii += self._find_adjacency(is_lct_of_interest, (ri,ci), (ri+1,ci), footprint)

        #assert ma.alltrue(ravel(gii<=maxg))
        return self.get_dataset().flatten_by_id(arcsin(sqrt(ma.filled(gii/maxg, 0))))

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
        elif self.covertype_symbol == 'grag':
            covertypes_of_interest = lookup_dict['GRASS_AND_AG']
        elif self.covertype_symbol == 'f':
            covertypes_of_interest = lookup_dict['FOREST']
        elif self.covertype_symbol == 'g':
            return [lookup_dict['GR']]
        else:
            raise RuntimeError("Sorry. Variable biocomplexity.land_cover.SSSai was unable to meaningfully" + \
                               " translate characters SSS for variable instantiation %sai." % self.covertype_symbol)

        return map(lambda key: lookup_dict[key], covertypes_of_interest)


from numpy import array

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

from biocomplexity.tests.expected_data_test import ExpectedDataTest

class Tests(ExpectedDataTest):

    def test_my_inputs(self):
        variable_name = "biocomplexity.land_cover.hai"
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

        should_be = arcsin(sqrt(array([0.25, 0, 0.25, 0])))

        self.assert_(ma.allclose( values, should_be, rtol=1e-7),
                     msg = "Error in " + variable_name)

    def test_my_inputs_convert(self):
        variable_name = "biocomplexity.land_cover.hmai"
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='land_covers',
            table_data={
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
                "lct": array([1, 3, 2, 4])
            }
        )

        dataset_pool = DatasetPool(package_order=['biocomplexity'],
                                   storage=storage)
        dataset_pool._add_dataset(
            'constant',
            {
                "FOOTPRINT": array([[0,1,0], [1,1,1], [0,1,0]]),
                'HEAVY_MED_URBAN':['HU','MU'],
                'MU': 2,
                'HU': 1,
            }
        )

        land_cover = dataset_pool.get_dataset('land_cover')
        land_cover.compute_variables(variable_name,
                                     dataset_pool=dataset_pool)
        values = land_cover.get_attribute(variable_name)

        should_be = arcsin(sqrt(array([0.25, 0, 0.25, 0])))

        self.assert_(ma.allclose( values, should_be, rtol=1e-7),
                     msg = "Error in " + variable_name)

    def atest_on_expected_data(self):
        self.variable_name = "biocomplexity.land_cover.gai"
        from numpy import ones
        footprint = ones(shape=(5,5), dtype="int32")
        self.do_test_on_expected_data(["relative_x","relative_y","lct"],
                                       {"constants":{"FOOTPRINT":footprint, 'HU':1, 'GR':5}})


if __name__ == "__main__":
    opus_unittest.main()
