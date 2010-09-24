# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


import os
import shutil
from opus_core.tests import opus_unittest

from biocomplexity.examples.run_simulation_all_chunks import Simulation
from biocomplexity.datasets.land_cover_dataset import LandCoverDataset
from biocomplexity.opus_package_info import package
from tempfile import mkdtemp

import sys, zipfile, os, os.path

def unzip_files_into_dir(file, dir):
#    os.mkdir(dir, 0777)
    zfobj = zipfile.ZipFile(file)
    for name in zfobj.namelist():
        if name.endswith('/'):
            os.mkdir(os.path.join(dir, name))
        else:
            outfile = open(os.path.join(dir, name), 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()

class TestRunSimulationAllChunks(opus_unittest.OpusTestCase):
    """Test on running the simulation for multiple years, transition between
    the input and output steps."""

    def setUp(self):
        package_dir_path = package().get_package_path()
        self.base_directory = os.path.join(package_dir_path, "data",
                                      "small_test_set_opus", "1991")
        
        zipped_cache = os.path.join(package_dir_path, "data", "sample_cache.zip")
        self.cache_dir = mkdtemp(prefix='tmp_biocomplexity')
        unzip_files_into_dir(zipped_cache, self.cache_dir)        
        self.urbansim_cache_directory = os.path.join(self.cache_dir, "urbansim_cache", 
                                                     "data", "2006_02_14__11_43")
        
    def tearDown(self):
        shutil.rmtree(self.cache_dir)
    
    def test_run_simulation_all_chunks(self):
        """ test if the simulation run without errors"""
        
        years = [2003,2007]
        coefficients = "lccm_coefficients_small_test"
        specification = "lccm_specification_small_test"
        Simulation().run(self.base_directory, self.urbansim_cache_directory, years,
                         None, None, coefficients, specification,
                         convert_flt=False, convert_input=False)
        
        
if __name__ == "__main__":
    opus_unittest.main()
    