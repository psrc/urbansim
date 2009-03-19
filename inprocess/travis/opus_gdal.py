# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os
from time import localtime, strftime, time
from opus_core.logger import logger

try:
    try:
        from osgeo import gdal
        from osgeo.gdalconst import *
        gdal.TermProgress = gdal.TermProgress_nocb
    except ImportError:
        import gdal
        from gdalconst import *
     
    try:
        import numpy as Numeric
        Numeric.arrayrange = Numeric.arange
    except ImportError:
        import Numeric
     
    try:
        from osgeo import gdal_array as gdalnumeric
    except ImportError:
        import gdal.gdalnumeric as gdalnumeric
except:
    logger.log_warning("Could not import gdal library or Numeric (or both).")
    
else:
    
    class OpusGDAL(object):
    
        def input_numpy_array_output_geotiff(self, attribute_values_in_2d_array,
                                          prototype_dataset=None,
                                          format="GTiff",
                                          output_directory=None,
                                          output_file_name=None,
                                          ):
            """
            This method accepts numpy array objects, x, y and attribute_values and converts them to a GeoTiff image.
    
            twoD_attribute_values - 2d attribute values, could be return value from Dataset.get_2d_attribute();
            prototype_dataset - prototype dataset that includes the same projection and goetransform info,
                                must be in a format that can be opened by gdal.Open();
            format - default "GTiff" for GeoTiff format, possible options "PNG" and any other formats GDAL support;
            output_directory and output_file_name indicate where to save the output,
                                if unspecified, save to current directory and use time stamp as file name (without file extension).
            """
    
    
            driver = gdal.GetDriverByName(format)
    
            tdata = Numeric.array(attribute_values_in_2d_array.tolist())
            tdata = Numeric.transpose(tdata)
            
            min_val = min(Numeric.argmin(tdata))
            if min_val >= 0:
                null_substitute = -1
            else:
                null_substitute = min_val + min_val * 10
                
            for i in range(len(tdata)):
                for j in range(len(tdata[i])):
                    if tdata[i][j] == 999999:
                        tdata[i][j] = null_substitute
            
            if prototype_dataset is not None:
                imgds = gdalnumeric.OpenArray(tdata, prototype_ds=prototype_dataset)
            else:
                imgds = gdalnumeric.OpenArray(tdata)
    
            if output_directory is None:
                output_directory = "."
            elif not os.path.exists(output_directory):
                os.mkdir(output_directory)
    
            if output_file_name is None:
                output_file_name = strftime("%Y_%m_%d_%H_%M.", localtime()) + format.lower()
    
            sfilename = os.path.join(output_directory, output_file_name)
            #try:
            imgds = driver.CreateCopy( sfilename, imgds )
                #imgds = gdal.Open(sfilename)
            #except:
            #    raise RuntimeError, "Error saving array into image"
    
    
    from opus_core.tests import opus_unittest
    from numpy import arange, array, reshape
    from numpy import ma
    import tempfile, os
    
    class VariableTests(opus_unittest.OpusTestCase):
    
        def setUp(self):
            temp_hd, temp_name = tempfile.mkstemp()
            os.close(temp_hd)
            self.temp_dir, self.temp_file = os.path.split(temp_name)
    
            def test_input_numpy_array_output_geotiff(self):
    
                twoD_array = arange(24).reshape(4,6)
                OpusGDAL().input_numpy_array_output_geotiff(twoD_array,
                                                       output_directory=self.temp_dir,
                                                       output_file_name=self.temp_file)
                filename = os.path.join(self.temp_dir, self.temp_file)
                dataset = gdalnumeric.LoadFile( filename, gdal.gdalconst.GA_ReadOnly )
                dataset = Numeric.transpose(dataset)
                tdata = array(dataset.tolist())
                self.assert_(ma.allequal(twoD_array, tdata))
    
        def tearDown(self):
            os.remove(os.path.join(self.temp_dir, self.temp_file))
    
    if __name__ == "__main__":
        opus_unittest.main()