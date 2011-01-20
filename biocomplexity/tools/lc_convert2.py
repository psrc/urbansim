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
import gc

class LCCMInputConvert():
    # 1. directory of the input and output data
#    flt_directory_in = None
#    flt_directory_out = None
#    parent_dir_path = package().get_package_parent_path()
#    flt_directory_in = os.path.join(parent_dir_path, "biocomplexity", "data", "LCCM_4County", "2035")
#    flt_directory_out = os.path.join(parent_dir_path, "biocomplexity", "data", "LCCM_4County_converted", "2035")
    
    def _convert_lccm_input(self, flt_directory_in, flt_directory_out):
        gc.collect()
        t1 = time()
        lc =  LandCoverDataset(in_storage = StorageFactory().get_storage('flt_storage', storage_location = flt_directory_in), 
            out_storage = StorageFactory().get_storage('flt_storage', storage_location = flt_directory_out))
#        lc.get_header() # added 23 june 2009 by mm
        mask = lc.get_mask()
        idx = where(mask==0)[0]
        lcsubset = DatasetSubset(lc, idx)
        print "Converting:"
        lcsubset.write_dataset(attributes=["relative_x"], out_table_name="land_covers")
        lc.delete_one_attribute("relative_x")
        lcsubset.write_dataset(attributes=["relative_y"], out_table_name="land_covers")
        lc.delete_one_attribute("relative_y")
        lc.flush_dataset()
        gc.collect()
#        lc_names = lc.get_primary_attribute_names()
        for attr in lc.get_primary_attribute_names():
            print "   ", attr
            lcsubset.write_dataset(attributes=[attr], out_table_name="land_covers")
            lc.delete_one_attribute(attr)
        logger.log_status("Data conversion done. " + str(time()-t1) + " s")
