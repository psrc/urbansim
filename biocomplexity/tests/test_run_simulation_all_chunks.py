# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


import os
import shutil
from opus_core.tests import opus_unittest

from biocomplexity.examples.run_simulation_all_chunks import Simulation
from biocomplexity.datasets.land_cover_dataset import LandCoverDataset
from biocomplexity.opus_package_info import package


class TestRunSimulationAllChunks(opus_unittest.OpusTestCase):
    """Test on running the simulation for multiple years, transition between
    the input and output steps."""
    
    def Mtest_run_simulation_all_chunks(self):
        """ test if the simulation run without errors"""
        
        package_dir_path = package().get_package_path()
        parent_dir_path = package().get_package_parent_path()
        base_directory = os.path.join(package_dir_path, "data",
                                      "small_test_set_opus", "1991")
        
        urbansim_cache_directory = os.path.join(parent_dir_path, "urbansim_cache", 
                                                "data", "2006_02_14__11_43")
        years = [2003,2007]
        coefficients = "land_cover_change_model_coefficients_small_test"
        specification = "land_cover_change_model_specification_small_test"
        Simulation().run(base_directory, urbansim_cache_directory, years,
                         None, None, coefficients, specification,
                         convert_flt=False, convert_input=False)
        self._clean_up_land_cover_cache(urbansim_cache_directory, years)

    def _clean_up_land_cover_cache(self, urbansim_cache_directory, years):
        lc_in_table_name = LandCoverDataset.in_table_name_default # 'land_covers'
        for year in years:
            shutil.rmtree(os.path.join(urbansim_cache_directory, str(year), lc_in_table_name))
        
        
if __name__ == "__main__":
    opus_unittest.main()
    
