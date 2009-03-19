# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label
from numpy import arcsin, sqrt, float32, not_equal, logical_not, zeros, logical_or, int32
from scipy.ndimage import correlate
from numpy import ma

class pSSS(Variable):
    """ Percent covertype SSS, excluding open_water.
    Over footprint fp: sum(lc type SSS) / (size(fp) - sum(lc type open_water))
      - need {'constants':{"FOOTPRINT":footprint,"MF":6...,"OW":12}}
          in resources when compute, where footprint=ones(shape=(5,5)). """

    land_cover_type_ow_within_footprint = 'land_cover_type_ow_within_footprint'
    footprint_size = 'footprint_size'
    land_cover_types = 'lct'

    def __init__(self, postfix):
        if postfix == 'cd':     # one special case
            lct = 'cdev'
        else:
            lct = postfix
        self.lct_type = lct
        #self.land_cover_type_within_footprint = "land_cover_type_%s_within_footprint" % lct
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.land_cover_types)]
        #my_attribute_label(self.land_cover_type_ow_within_footprint),
                #my_attribute_label(self.land_cover_type_within_footprint),
#                my_attribute_label(self.footprint_size)]

    def compute(self, dataset_pool):
        constant = dataset_pool.get_dataset('constant')
        footprint = constant['FOOTPRINT']
        #denominator = dataset.get_attribute(self.footprint_size) - dataset.get_attribute(self.land_cover_type_ow_within_footprint)
        lct = ma.filled(self.get_dataset().get_2d_attribute(self.land_cover_types), 0)
        covertypes_of_interest = self._cover_type_translation(constant)
        is_lct_of_interest = reduce(lambda prev_answer, lct_num: logical_or(prev_answer, lct==lct_num),
                                    covertypes_of_interest,
                                    zeros(shape=lct.shape)).astype(int32)
        lct_mask = logical_not(self.get_dataset().get_mask(is_2d_version=True))

        temp = not_equal(lct, constant['OW'])

        denominator = correlate((temp&lct_mask).astype(int32), footprint, mode='reflect');
        #denominator = dataset.flatten_by_id(denominator);

        values = correlate(is_lct_of_interest, footprint, mode="reflect")

        #pct = dataset.get_attribute(self.land_cover_type_within_footprint).astype(float32) / \
        pct = values.astype(float32) / \
               ma.masked_where(denominator==0, denominator)
        pct = ma.filled(pct, 0.0)
        return self.get_dataset().flatten_by_id(arcsin(sqrt(pct)))

    def _cover_type_translation(self, lookup_dict):
        """returns a list of lct number types based on the lct_type_name
         if no such lct type is found, return None """
        if self.lct_type == 'a':
            covertypes_of_interest = lookup_dict['ALL_URBAN']
        elif self.lct_type == 'mlu':
            covertypes_of_interest = lookup_dict['MED_LIGHT_URBAN']
        elif self.lct_type == 'for':
            covertypes_of_interest = lookup_dict['FOREST']
        elif self.lct_type == 'mhu':
            covertypes_of_interest = lookup_dict['MED_HIGH_URBAN']
        elif self.lct_type == 'grag':
            covertypes_of_interest = lookup_dict['GRASS_AND_AG']
        elif self.lct_type.lower() in lookup_dict.keys():
            return [lookup_dict[self.lct_type.lower()]]
        elif self.lct_type.upper() in lookup_dict.keys():
            return [lookup_dict[self.lct_type.upper()]]
        else:
            raise RuntimeError("Sorry. Variable biocomplexity.land_cover.pSSS was unable to meaningfully" + \
                   " translate characters SSS for variable instantiation p%s." % self.lct_type)

        return map(lambda key: lookup_dict[key], covertypes_of_interest)



from numpy import array

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

from biocomplexity.tests.expected_data_test import ExpectedDataTest

class Tests(ExpectedDataTest):

    def test_my_inputs_tree_test(self):
        variable_name = "biocomplexity.land_cover.pcc"
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='land_covers',
            table_data={
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
                "lct": array([12, 8, 8, 15])
            }
        )

        dataset_pool = DatasetPool(package_order=['biocomplexity'],
                                   storage=storage)
        dataset_pool._add_dataset(
            'constant',
            {
                "FOOTPRINT": array([[0,1,0], [1,1,1], [0,1,0]]),
                "CC":8,
                "OW":12
            }
        )

        land_cover = dataset_pool.get_dataset('land_cover')
        land_cover.compute_variables(variable_name,
                                     dataset_pool=dataset_pool)
        values = land_cover.get_attribute(variable_name)

        cc_within_fp = array([2, 3, 3, 2])
        ow_within_fp = array([3, 1, 1, 0])
        should_be = cc_within_fp / (5.0 - ow_within_fp)
        should_be = arcsin(sqrt(should_be))

        self.assert_(ma.allclose( values, should_be, rtol=1e-7),
                     msg = "Error in " + variable_name)

    def test_my_inputs_tree_lookup_test(self):
        variable_name = "biocomplexity.land_cover.pmhu"
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='land_covers',
            table_data={
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
                "lct": array([12, 1, 2, 15])
            }
        )

        dataset_pool = DatasetPool(package_order=['biocomplexity'],
                                   storage=storage)
        dataset_pool._add_dataset(
            'constant',
            {
                "FOOTPRINT": array([[0,1,0], [1,1,1], [0,1,0]]),
                "HU":1,
                "MU":2,
                "MED_HIGH_URBAN":["HU","MU"],
                "OW":12
            }
        )

        land_cover = dataset_pool.get_dataset('land_cover')
        land_cover.compute_variables(variable_name,
                                     dataset_pool=dataset_pool)
        values = land_cover.get_attribute(variable_name)

        mhu_within_fp = array([2, 3, 3, 2])
        ow_within_fp = array([3, 1, 1, 0])
        should_be = mhu_within_fp / (5.0 - ow_within_fp)
        should_be = arcsin(sqrt(should_be))

        self.assert_(ma.allclose( values, should_be, rtol=1e-7),
                     msg = "Error in " + variable_name)

    def test_on_expected_data(self):
        self.variable_name = "biocomplexity.land_cover.pmf"
        from numpy import ones
        footprint = ones(shape=(5,5), dtype="int32")
        self.do_test_on_expected_data(["lct","relative_x","relative_y"],
                                       {'constants':{"FOOTPRINT":footprint,"MF":6,"OW":12}},
                                      element_atol=0.15)


if __name__=='__main__':
    opus_unittest.main()