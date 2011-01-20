# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

""" This converts cleaner without-nodata-values files back to raw flt files. """

from opus_core.variables.attribute_type import AttributeType
from biocomplexity.datasets.land_cover_dataset import LandCoverDataset
from biocomplexity.examples.lccm_runner_sample import LccmConfiguration
from opus_core.logger import logger
from numpy import where, float32, int32, ones, put, float64, fromfile
from opus_core.storage_factory import StorageFactory
from numpy import ma
from optparse import OptionParser
import os

import sys
import shutil
import glob

flt_directory_in = None
flt_directory_out = None

###############################
# CONSTANTS ###################
###############################
ncols = LccmConfiguration.ncols
nrows = LccmConfiguration.nrows
nodata_values = LccmConfiguration.nodata_values
cellsize = LccmConfiguration.cellsize
xllcorner = LccmConfiguration.xllcorner
yllcorner = LccmConfiguration.yllcorner
###############################


def _create_header(file_name):
    content = \
"""ncols         %d
nrows         %d
xllcorner     %f
yllcorner     %f
cellsize      %d
NODATA_value  %d
byteorder     LSBFIRST
""" % (ncols, nrows, xllcorner, yllcorner, cellsize, nodata_values)
    f = open(file_name, mode="w")
    f.write(content)
    f.close()
    
def _create_flt_file(file_name, data, flat_indices, offset):
    if os.path.exists(file_name): # check here to see if ouput exists so we can append new data to it
        #os.remove(file_name)
        content = fromfile(file_name, dtype=float32) # reads in existing file
        put(content.ravel(), flat_indices.astype(int32)[offset:], data[offset:]) # incoprorates existing data using offset (chunk) size
    else:
        content = nodata_values*ones(shape=(nrows, ncols)).astype(float32)
        put(content.ravel(), flat_indices.astype(int32), data) # <-- coerced flat_indices as integer32 type - changed on 26 may 09 by mm
    content.tofile(file_name)

if __name__ == "__main__":
    test_flag = False
    if len(sys.argv) >= 2:
        parser = OptionParser()
        parser.add_option("-i", "--input", dest="input", action="store", type="string")
        parser.add_option("-o", "--output", dest="output", action="store", type="string")
        parser.add_option("-t", "--test", dest="test_flag", action="store_true", default="false")
        (options, args) = parser.parse_args() 
        
        current_year = sys.argv[1]
        
        test_flag = options.test_flag        
    
        flt_directory_in = options.input
        flt_directory_out = options.output
    
        logger.log_status("Convert output data for ", str(current_year))
    
    #todo: how to get 'land_covers' from dataset?
    flt_directory_out = os.path.join(flt_directory_out, 'land_covers')    
    
    if not os.path.exists(flt_directory_out):
        os.makedirs(flt_directory_out)
    
    lc =  LandCoverDataset(in_storage = StorageFactory().get_storage('flt_storage', storage_location = flt_directory_in))
    relative_x = lc.get_attribute("relative_x")
    relative_y = lc.get_attribute("relative_y")
    flat_indices = relative_x * ncols * 1.0 + relative_y
    
    if flat_indices[5*ncols:] is None or len(flat_indices[5*ncols:]) == 0:
        offset = 0
    else:
        offset = 5*ncols
    
    #if os.path.exists("indices.lf4"):
    #    os.remove("indices.lf4")
    #flat_indices.tofile("indices.lf4")
    
    logger.start_block("Converting")
    try:    
        for attr_name in lc.get_primary_attribute_names():
            if attr_name not in ["relative_x", "relative_y"]:
                #attr_name = "lct" #-------------- only output lct now
                logger.log_status("    ", attr_name)
                attr = ma.filled(lc.get_attribute(attr_name), nodata_values).astype(float32)
    #            print attr.size
                _create_flt_file(os.path.join(flt_directory_out, attr_name+".lf4"), attr, flat_indices, offset)
                _create_header(os.path.join(flt_directory_out, attr_name+".hdr")) #<-- added 26 may 09 by mm
                del attr
                #break #-------------- only output lct now
                
        lc.load_dataset(attributes='*')
        if lc.get_computed_attribute_names() is not None:        
            flt_directory_out = os.path.join(flt_directory_out, "computed")
            if not os.path.exists(flt_directory_out):
                os.makedirs(flt_directory_out)
            for attr_name in lc.get_computed_attribute_names():
                if attr_name not in ["_hidden_id_"]:
                    logger.log_status("    ", attr_name)
                    attr = ma.filled(lc.get_attribute(attr_name), nodata_values).astype(float32)
    #                print attr.size
                    _create_flt_file(os.path.join(flt_directory_out, attr_name+".lf4"), attr, flat_indices, offset)
                    _create_header(os.path.join(flt_directory_out, attr_name+".hdr")) #<-- added 26 may 09 by mm
                    del attr
    finally:
        logger.end_block()