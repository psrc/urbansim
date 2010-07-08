# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
    

from biocomplexity.datasets.land_cover_dataset import LandCoverDataset
from biocomplexity.opus_package_info import package
from opus_core.datasets.dataset import DatasetSubset
from opus_core.storage_factory import StorageFactory
from opus_core.logger import logger
from numpy import where
from time import time
import os, sys

t1 = time()

parent_dir_path = package().get_package_parent_path()

# 1. Directory of the input data - input directory that contains all data to be read-in 
#    at full geographic extent;  in binary float format with .lf4 and .li4 file extensions
#flt_directory_in = sys.argv[0]
flt_directory_in = os.path.join(parent_dir_path, "biocomplexity", "uncertainty", "_bm_LCCM_output_a9599_10x", "lc02_07_obs_probs")
#flt_directory_in = os.path.join(parent_dir_path, "biocomplexity", "data", "LCCM_4County")
#flt_directory_in = os.path.join(parent_dir_path, "biocomplexity", "data", "LCCM_output_a9902c_v4")

# 2. Directory of the output data - directory where subsetted data are created; uncomment needed directory path
#flt_directory_out = sys.argv[1]
flt_directory_out = os.path.join(parent_dir_path, "biocomplexity", "uncertainty", "_bm_LCCM_output_a9599_10x", "smpl_lc02_07_obs_probs")
#flt_directory_out = os.path.join(parent_dir_path, "biocomplexity", "data", "data_for_estimation_all")
#flt_directory_out = os.path.join(parent_dir_path, "biocomplexity", "uncertainty", "_bm_LCCM_output_a9902c_v4", "run_4")

# 3. Index attribute - raster representing sampling design for logit model estimation; binary float with .lf4 file extension
#    uncomment necessary sample file
#index_attribute = "sall_91_95_0"
#index_attribute = "sall_95_99_0"
#index_attribute = "sall_99_02_0b"
#index_attribute = "sa9902_9195_0"
#index_attribute = "sa9902_9599_0"
#index_attribute = "sall_99_02_0v1"
#index_attribute = sys.argv[2]
index_attribute = "lc0207_100k_0"

# 4. Years - date pair of input data; year is concatenated to flt_directory_in specified in #1
#years = [1991, 1995]
#years = [1995, 1999]
#years = [2002]
#years = sys.argv[3]
years = [2007, 2007]

lc1 =  LandCoverDataset(in_storage = StorageFactory().get_storage('flt_storage', 
        storage_location = os.path.join(flt_directory_in, str(years[0]))),
    out_storage = StorageFactory().get_storage('flt_storage', 
        storage_location = os.path.join(flt_directory_out, str(years[0]))))

agents_index = where(lc1.get_attribute(index_attribute))[0]
lc1subset = DatasetSubset(lc1, agents_index)
print "Writing set 1:"
for attr in lc1.get_primary_attribute_names():
    print "   ", attr
    lc1subset.write_dataset(attributes=[attr], out_table_name="land_covers")
    lc1.delete_one_attribute(attr) # leaving this line in causes the processing of every other input data file; commenting it causes memory error
    
lc2 =  LandCoverDataset(in_storage = StorageFactory().get_storage('flt_storage', 
        storage_location = os.path.join(flt_directory_in, str(years[1]))),
    out_storage = StorageFactory().get_storage('flt_storage',
        storage_location = os.path.join(flt_directory_out, str(years[1]))))
                  
lc2subset = DatasetSubset(lc2, agents_index)
print "Writing set 2:"
for attr in lc2.get_primary_attribute_names():
    print "   ", attr
    lc2subset.write_dataset(attributes=[attr], out_table_name="land_covers")
    lc2.delete_one_attribute(attr) # leaving this line in causes the processing of every other input data file ; commenting it causes memory error             
logger.log_status("Data storage done. " + str(time()-t1) + " s")
