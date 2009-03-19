# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE


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

parent_dir_path = package().get_package_parent_path()
# directory of the input data
#flt_directory_in = os.path.join(parent_dir_path, "LCCM_small_test_set_opus", "LCCM_4County", "1999")
flt_directory_in =  r"C:\eclipse\LCCM_4County\1995"
#flt_directory_in = os.path.join(parent_dir_path, "LCCM_Urban_Partition", "full_area", "1991")
#flt_directory_in = os.path.join(parent_dir_path, "LCCM_Urban_Partition", "1991")

#directory of the output data
#flt_directory_out = os.path.join(parent_dir_path, "LCCM_small_test_set_opus", "LCCM_4County", "converted", "1995")
flt_directory_out =  r"C:\eclipse\LCCM_4County\data_for_urban\1995"
#flt_directory_out = os.path.join(parent_dir_path, "LCCM_Urban_Partition", "land_covers_convert", "1991")

# set here the type of the attributes
valuetypes = {"lct":"int8", "sample_bin":"bool8",
"devgrid_id":"int32",
"crit":"bool8",
"de":"bool8",
"di":"bool8",
"dc":"bool8",
"dos":"bool8",
"di":"bool8",
"dres":"bool8",
"dmu":"bool8",
"pub":"bool8",
"blmz":"bool8",
"sslp":"bool8",
"tbl":"bool8",
"ugl":"bool8",
"sample_urb_partition0":"bool8",
"sample_urb_partition":"bool8",
"partition":"int16",
}

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
    out_storage = StorageFactory().get_storage('flt_storage', storage_location = flt_directory_out))

mask = lc.get_mask()
idx = where(mask==0)[0]
lcsubset = DatasetSubset(lc, idx)
print "Converting:"
lcsubset.write_dataset(attributes=["relative_x"], out_table_name="land_covers",
                            valuetypes=valuetypes)
lc.delete_one_attribute("relative_x")
lcsubset.write_dataset(attributes=["relative_y"], out_table_name="land_covers",
                            valuetypes=valuetypes)
lc.delete_one_attribute("relative_y")
srcdir = os.path.join(flt_directory_out, "land_covers", "computed")
shutil.move(os.path.join(srcdir,"relative_x.li4"), os.path.join(flt_directory_out, "land_covers"))
shutil.move(os.path.join(srcdir,"relative_y.lf4"), os.path.join(flt_directory_out, "land_covers"))
shutil.rmtree(srcdir)
for attr in lc.get_primary_attribute_names():
    print "   ", attr
    lcsubset.write_dataset(attributes=[attr], out_table_name="land_covers",
                            valuetypes=valuetypes)
    lc.delete_one_attribute(attr)

print "done."