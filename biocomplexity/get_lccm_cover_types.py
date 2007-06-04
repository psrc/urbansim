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

class GetLCCMCoverTypes(object):
    def get_land_cover_types_from_file(self, file_path):
        """Returns a dictionary of every key, value(s) pair 
        single values are cast as ints and multiple values are returned as a list of strings. 
        All keys are cast to upper case."""
        lct_file = open(file_path, 'r')
        lccm_types = {}
        for line in lct_file.readlines():
            comment_place = line.find('#')
            if comment_place != -1:
                line = line[:comment_place]
            data = line.split()
            if data:
                key = data[0]
                lccm_types[key] = data[1:]
                if len(lccm_types[key])== 1:
                    lccm_types[key] = int(lccm_types[key][0])
                    
        return lccm_types
    

from opus_core.tests import opus_unittest
import tempfile
class Test(opus_unittest.OpusTestCase):
    def test_reader(self):
        f = open(tempfile.mktemp(), 'w')
        f.write("""
        A 1
        B 2
        C 3
        ABC A B C""")
        f.close()
        vals = GetLCCMCoverTypes().get_land_cover_types_from_file(f.name)
        self.assertEqual(vals, {'A':1, 'B':2, 'C':3, 'ABC':['A', 'B', 'C']})


if __name__=='__main__':            
    opus_unittest.main()