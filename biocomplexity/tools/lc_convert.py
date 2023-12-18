# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
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
from time import time
import os

import shutil
import sys

t1 = time()
parent_dir_path = package().get_package_parent_path()

# 1. directory of the input data
flt_directory_in = os.path.join(parent_dir_path, "biocomplexity", "data", "LCCM_4County", "2044")
flt_directory_in = os.path.join(parent_dir_path, "biocomplexity", "uncertainty", "_bm_LCCM_output_a9599_10x", "lc02_07_obs_probs", "2007")
#flt_directory_in = sys.argv[0]

# 2. directory of the output data
flt_directory_out = os.path.join(parent_dir_path, "biocomplexity", "data", "LCCM_4County_converted", "2044")
flt_directory_out = os.path.join(parent_dir_path, "biocomplexity", "uncertainty", "_bm_LCCM_output_a9599_10x", "converted_lc02_07_obs_probs", "2007")
#flt_directory_out = sys.argv[1]

# 3. set here the type of the attributes - not needed as all data are compressed and encoded as numpy float32 (.lf4) data;
#    though, still need valuetypes {} is legacy for write_dataset method
#valuetypes = {}
#valuetypes = {
#"lct":"int8", "sample_bin":"bool8", "devgrid_id":"int32", "crit":"bool8", "de":"bool8", "di":"bool8", "dc":"bool8",
#"dos":"bool8", "di":"bool8", "dres":"bool8", "dmu":"bool8", "pub":"bool8", "blmz":"bool8", "sslp":"bool8", "tbl":"bool8",
#"ugl":"bool8", "sample_urb_partition0":"bool8", "sample_urb_partition":"bool8", "partition":"int16",
#}

if __name__ == "__main__":
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
        
        print(flt_directory_out)
        
        test_flag = options.test_flag
        
#        shutil.rmtree(flt_directory_out)
#        os.mkdir(flt_directory_out)
        
        logger.log_status("Convert input data from ", str(input_year))
    
    lc =  LandCoverDataset(in_storage = StorageFactory().get_storage('flt_storage', storage_location = flt_directory_in), 
        out_storage = StorageFactory().get_storage('flt_storage', storage_location = flt_directory_out))
    
    lc.get_header() # added 23 june 2009 by mm
    mask = lc.get_mask()
    idx = where(mask==0)[0]
    lcsubset = DatasetSubset(lc, idx)
    print("Converting:")
    lcsubset.write_dataset(attributes=["relative_x"], out_table_name="land_covers")
    #lcsubset.write_dataset(attributes=["relative_x"], out_table_name="land_covers",
    #                            valuetypes=valuetypes)
    lc.delete_one_attribute("relative_x")
    lcsubset.write_dataset(attributes=["relative_y"], out_table_name="land_covers")
    #lcsubset.write_dataset(attributes=["relative_y"], out_table_name="land_covers",
    #                            valuetypes=valuetypes)
    lc.delete_one_attribute("relative_y")
#    srcdir = os.path.join(flt_directory_out, "land_covers", "computed")
#    shutil.move(os.path.join(srcdir,"relative_x.li4"), os.path.join(flt_directory_out, "land_covers"))
#    shutil.move(os.path.join(srcdir,"relative_y.li4"), os.path.join(flt_directory_out, "land_covers"))
#    shutil.rmtree(srcdir)
    for attr in lc.get_primary_attribute_names():
        print("   ", attr)
        lcsubset.write_dataset(attributes=[attr], out_table_name="land_covers")
    #    lcsubset.write_dataset(attributes=[attr], out_table_name="land_covers",
    #                            valuetypes=valuetypes)
        lc.delete_one_attribute(attr)
    logger.log_status("Data conversion done. " + str(time()-t1) + " s")
