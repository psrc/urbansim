# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


import os
from shutil import rmtree

from numpy import ma
from numpy import array, sum

from opus_core.logger import logger
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool  import DatasetPool

from biocomplexity.datasets.land_cover_dataset import LandCoverDataset
from biocomplexity.opus_package_info import package


class ExpectedDataTest(opus_unittest.OpusTestCase):
    """ A abstract test case class to be inherited by all land cover variables,
        it has a test case to test on expected data with computed values.
        - Not all variables has expected data to be tested, check flt_directory
        - Provide needed input files, and resources for testing.
    """
    
    def _max_distance_between_two_elements(self, array1, array2):
        """Helper function to determind the max distance between in 2 arrays,
            comparing element in order"""
        # move 2 arrays by this delta to make them all have positive values
        delta = abs(min(min(array1), min(array2)))
        return max(abs((array1+delta)-(array2+delta)))

    def do_test_on_expected_data(self, input_variables_list, input_resources=None, 
                                 element_atol=None, sum_atol=None):
        from biocomplexity.datasets.land_cover_dataset import LandCoverDataset
        from biocomplexity.tests.utils.land_cover_tests_utils import make_input_data            
        
        import os
        
        package_dir_path = package().get_package_path()
        flt_directory = os.path.join(package_dir_path, "data", "small_test_set_opus", "1995")
        #flt_directory = r"C:\eclipse\LCCM_small_test_set_converted\1991"
        expected_lc = LandCoverDataset(in_storage = StorageFactory().get_storage('flt_storage', storage_location = flt_directory))
        expected_lc.load_dataset()            
        
        temp_dir = make_input_data(flt_directory, input_variables_list)
        try:
            lc = LandCoverDataset(in_storage = StorageFactory().get_storage(
                'flt_storage', 
                storage_location=temp_dir),
                out_storage = StorageFactory().get_storage('flt_storage', storage_location = r"c:/tmp"))
            lc.load_dataset()
            
            dataset_pool = DatasetPool(
                package_order=['biocomplexity'],
                storage=StorageFactory().get_storage('flt_storage', storage_location=temp_dir))
            dataset_pool._add_dataset('land_cover', lc)
            lc.compute_variables(self.variable_name, resources=input_resources, 
                                 dataset_pool=dataset_pool)
            
            #lc.write_dataset(attributes='*')
            
            lc_values = lc.get_attribute(self.variable_name)
            expected_values = expected_lc.get_attribute(self.variable_name)    
            
            if sum_atol is None: sum_atol = 1e-8
            if element_atol is None: element_atol = 1e-8
            
            if (not ma.allclose(lc_values, expected_values, atol=element_atol)):
                logger.log_status("comparision using element-atol=%f, sum-atol=%f" % (element_atol, sum_atol))
                logger.log_status("      computed      expected");
                logger.log_status("sum: ", lc_values.sum(), expected_values.sum())
                logger.log_status("max: ", max(lc_values), max(expected_values))
                logger.log_status("min: ", min(lc_values), min(expected_values))
                
                c1 = 0
                c2 = 0
                for (i,j) in zip(lc_values, expected_values):
                    if i != 0:
                        c1 = c1 + 1
                    if j != 0:
                        c2 = c2 + 1
                        
                logger.log_status("# non-zeros values: ", c1, c2)
                logger.log_status("max distance between 2 elements: %f" % 
                                            self._max_distance_between_two_elements(lc_values,expected_values))
                logger.log_status(lc_values, expected_values)
                count = 0
                total = 0
                for (i,j) in zip(lc_values, expected_values):
                    if i != j:
                        count = count + 1
                    total = total + 1
                logger.log_status("# different elements = %d, over %d, with a %f percentage" \
                                % (count, total, count*1.0/total))
            
            #self.assert_(ma.allclose(lc_values.sum(), expected_values.sum(), atol=sum_atol))
            self.assert_(ma.allclose(lc_values, expected_values, atol=element_atol))
        finally:
            if os.path.exists(temp_dir):
                rmtree(temp_dir)
            
