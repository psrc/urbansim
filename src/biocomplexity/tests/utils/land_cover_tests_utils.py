#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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
import tempfile
import shutil

"""Helper functions for lccm test"""

def make_input_data(source_flt_directory, input_variables):
    """Given a flt_directory as a land_cover dataset input storage,
           and a list of attributes
       This function will:
           - create a new temporary directory: 'temp_dir'/land_covers
           - copy provided attributes to this temporary directory
           - return the new temporary directory path
    """
    dest_flt_directory = tempfile.mkdtemp(prefix='biocomplexity')
    os.makedirs(os.path.join(dest_flt_directory, "land_covers"))

    for v in input_variables:
        # check the name file inside: biocomplexity/data/small_test_set_1995/land_cover
        if v.lower() == "relative_x" or v.lower() == "relative_y":
            shutil.copy(os.path.join(source_flt_directory, "land_covers", v.upper()+".li4"), 
                                     os.path.join(dest_flt_directory, "land_covers"))
        elif v.lower() == "land_cover_grid_id_index":
            shutil.copy(os.path.join(source_flt_directory, "land_covers", v.lower()+".li4"), 
                                     os.path.join(dest_flt_directory, "land_covers"))
        else:
            shutil.copy(os.path.join(source_flt_directory, "land_covers", v.upper()+".lf4"), 
                                     os.path.join(dest_flt_directory, "land_covers"))
                                
    return dest_flt_directory



from opus_core.tests import opus_unittest

if __name__ == "__main__":
    class TestUtils(opus_unittest.OpusTestCase):
        def test_make_input_data(self):
            source_flt_directory = tempfile.mkdtemp()
            os.makedirs(os.path.join(source_flt_directory, "land_covers"))
            f = open(os.path.join(source_flt_directory, "land_covers", "a.lf4"), "w")
            f.write('\n')
            f.close()
            dest_flt_directory = make_input_data(source_flt_directory, ["a"])
            self.assert_(os.path.exists(os.path.join(dest_flt_directory, "land_covers", "a.lf4")))
               
    opus_unittest.main()
