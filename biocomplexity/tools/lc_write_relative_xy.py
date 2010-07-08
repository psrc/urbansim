# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


""" This converts given raw flt files with-nodata-values to cleaner without
    nodata-values files. """

from biocomplexity.datasets.land_cover_dataset import LandCoverDataset
from biocomplexity.examples.lccm_runner_sample import LccmConfiguration
from biocomplexity.opus_package_info import package
from opus_core.datasets.dataset import DatasetSubset
from opus_core.storage_factory import StorageFactory
from opus_core.logger import logger
from numpy import where
from optparse import OptionParser
import os

import shutil
import sys

if __name__ == "__main__":
    parent_dir_path = package().get_package_parent_path()
    
    # directory of the data 
#    flt_directory_in = os.path.join(parent_dir_path, "biocomplexity", "data", "LCCM_small_test_set_opus", "1995")
    flt_directory_in = os.path.join(parent_dir_path, "biocomplexity", "data", "LCCM_4County", "2002")
    flt_directory_out = flt_directory_in
    
    # set here the type of the attributes
    valuetypes = {}
    
    test_flag = False
    if len(sys.argv) >= 2:
        parser = OptionParser()
        parser.add_option("-i", "--input", dest="input", action="store", type="string")
        parser.add_option("-o", "--output", dest="output", action="store", type="string")
        parser.add_option("-t", "--test", dest="test_flag", action="store_true", default="false")
        (options, args) = parser.parse_args()    
        
        input_year = sys.argv[1]   
    
        flt_directory_in = options.input
        flt_directory_out = options.output
        
        print flt_directory_out
        
        test_flag = options.test_flag
        
        shutil.rmtree(flt_directory_out)
        os.mkdir(flt_directory_out)
        
        logger.log_status("Convert input data from ", str(input_year))
    
    lc =  LandCoverDataset(in_storage = StorageFactory().get_storage('flt_storage', storage_location = flt_directory_in), 
        out_storage = StorageFactory().get_storage('flt_storage', storage_location = flt_directory_out), debuglevel=4)
    
    lc.get_header()
    
#    mask = lc.get_mask()
#    idx = where(mask==0)[0]
#    lcsubset = DatasetSubset(lc, idx)
    print "Creating and writing relative_x and relative_y:"
    lc.write_dataset(attributes=["relative_x"], out_table_name="land_covers",
                                valuetypes=valuetypes)
    lc.delete_one_attribute("relative_x")
    lc.write_dataset(attributes=["relative_y"], out_table_name="land_covers",
                                valuetypes=valuetypes)
    lc.delete_one_attribute("relative_y")
    
    print "done."