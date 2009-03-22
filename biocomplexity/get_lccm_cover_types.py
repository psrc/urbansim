# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

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