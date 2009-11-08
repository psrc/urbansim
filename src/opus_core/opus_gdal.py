#
# Opus software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

import os
from time import localtime, strftime, time
import Numeric as numeric

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

        import gdal.gdal as gdal
        import gdal.gdalnumeric as gdalnumeric

        driver = gdal.GetDriverByName(format)

        tdata = numeric.array(attribute_values_in_2d_array.tolist())
        tdata = numeric.transpose(tdata)

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
from opus_core.logger import logger

class VariableTests(opus_unittest.OpusTestCase):

    def setUp(self):
        temp_hd, temp_name = tempfile.mkstemp()
        os.close(temp_hd)
        self.temp_dir, self.temp_file = os.path.split(temp_name)

    try: import gdal
    except:
        logger.log_warning("Could not import gdal library."
            " Skipping test_input_numpy_array_output_geotiff.")
    else:
        def test_input_numpy_array_output_geotiff(self):
            from gdal.gdalconst import GA_ReadOnly
            import gdal.gdal as gdal
            import gdal.gdalnumeric as gdalnumeric

            twoD_array = arange(24).reshape(4,6)
            OpusGDAL().input_numpy_array_output_geotiff(twoD_array,
                                                   output_directory=self.temp_dir,
                                                   output_file_name=self.temp_file)
            filename = os.path.join(self.temp_dir, self.temp_file)
            dataset = gdalnumeric.LoadFile( filename, GA_ReadOnly )
            dataset = numeric.transpose(dataset)
            tdata = array(dataset.tolist())
            self.assert_(ma.allequal(twoD_array, tdata))

    def tearDown(self):
        os.remove(os.path.join(self.temp_dir, self.temp_file))

if __name__ == "__main__":
    try: import gdal
    except: print "Could not import gdal library."
    else:
        opus_unittest.main()