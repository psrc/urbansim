# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

""" This class converts cleaner without-nodata-values files back to raw flt files. """

from biocomplexity.datasets.land_cover_dataset import LandCoverDataset
from biocomplexity.examples.lccm_runner_sample import LccmConfiguration
from biocomplexity.opus_package_info import package
from opus_core.variables.attribute_type import AttributeType
from opus_core.logger import logger
from opus_core.storage_factory import StorageFactory
from numpy import ma, where, float32, int32, ones, put, float64, fromfile
import os

class ConvertToFloat():
    
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
    
    def _create_flt_file(self, current_year, flt_directory_in, flt_directory_out):

        logger.log_status("Convert output data for ", str(current_year))
        
        flt_directory_out = os.path.join(flt_directory_out, 'land_covers')    
        
        if not os.path.exists(flt_directory_out):
            os.makedirs(flt_directory_out)

        lc =  LandCoverDataset(in_storage = StorageFactory().get_storage('flt_storage', storage_location = flt_directory_in))
        relative_x = lc.get_attribute("relative_x")
        relative_y = lc.get_attribute("relative_y")
        flat_indices = relative_x * self.ncols * 1.0 + relative_y
        
        if flat_indices[5*self.ncols:] is None or len(flat_indices[5*self.ncols:]) == 0:
            offset = 0
        else:
            offset = 5*self.ncols
        
        logger.start_block("Converting")
        try:    
            for attr_name in lc.get_primary_attribute_names():
                if attr_name not in ["relative_x", "relative_y"]:
                    attr_name = "lct" #-------------- only output lct now
                    logger.log_status("    ", attr_name)
                    attr = ma.filled(lc.get_attribute(attr_name), self.nodata_values).astype(float32)
                    self._create_flt_file2(os.path.join(flt_directory_out, attr_name+".lf4"), attr, flat_indices, offset)
                    self._create_header(os.path.join(flt_directory_out, attr_name+".hdr")) #<-- added 26 may 09 by mm
                    del attr
                    break #-------------- only output lct now
                    
            lc.load_dataset(attributes='*')
            if lc.get_computed_attribute_names() is not None:        
                flt_directory_out = os.path.join(flt_directory_out, "computed")
                if not os.path.exists(flt_directory_out):
                    os.makedirs(flt_directory_out)
                for attr_name in lc.get_computed_attribute_names():
                    if attr_name not in ["_hidden_id_"]:
                      if attr_name[0:5] == "probs":
                        logger.log_status("    ", attr_name)
                        attr = ma.filled(lc.get_attribute(attr_name), self.nodata_values).astype(float32)
                        self._create_flt_file2(os.path.join(flt_directory_out, attr_name+".lf4"), attr, flat_indices, offset)
                        self._create_header(os.path.join(flt_directory_out, attr_name+".hdr")) #<-- added 26 may 09 by mm
                        del attr
        finally:
#            lc.flush_dataset() # added 23 jun 2009 - not tested...
            logger.end_block()

    def _create_flt_file2(self, file_name, data, flat_indices, offset):
    #    print 'data: %s' % data
    #    print 'flat_indices: %s' % flat_indices
    #    print 'offset: %s' % offset
        if os.path.exists(file_name): # check here to see if ouput exists so we can append new data to it
            #os.remove(file_name)
            content = fromfile(file_name, dtype=float32) # reads in existing file
            put(content.ravel(), flat_indices.astype(int32)[offset:], data[offset:]) # incoprorates existing data using offset (chunk) size
        else:
            content = self.nodata_values*ones(shape=(self.nrows, self.ncols)).astype(float32)
            put(content.ravel(), flat_indices.astype(int32), data) # <-- coerced flat_indices as integer32 type - changed on 26 may 09 by mm
        content.tofile(file_name)

    def _create_header(self, file_name):
        content = \
    """    ncols         %d
    nrows         %d
    xllcorner     %f
    yllcorner     %f
    cellsize      %d
    NODATA_value  %d
    byteorder     LSBFIRST
    """ % (self.ncols, self.nrows, self.xllcorner, self.yllcorner, self.cellsize, self.nodata_values)
        f = open(file_name, mode="w")
        f.write(content)
        f.close()
        
if __name__ == "__main__":
    parent_dir_path = package().get_package_parent_path()
    flt_directory_in = os.path.join(parent_dir_path, "biocomplexity", "data", "LCCM_4County_converted", "1991")
    flt_directory_out = os.path.join(parent_dir_path, "biocomplexity", "data", "LCCM_4County", "2002")
    current_year = 1991
    ConvertToFloat()._create_flt_file(current_year, flt_directory_in, flt_directory_out)

    
    