# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import re

class LagVariableParser(object):
    """Methods to parse the name of a lag variable.
    """
    def is_short_name_for_lag_variable(self, short_name):
        """Pattern matches for lag variable short name and return true if attribute is a lag varaible
            false otherwise"""
        match = re.search("^[a-z_0-9]+_lag[0-9]+$", short_name)
        return match != None
            
    def parse_lag_variable_short_name(self, short_name):
        """Returns a tuple of the lag attribute's short name and the lag delay"""
        short_name_match = re.search("[a-z_0-9]+_lag", short_name)
        lag_short_name = short_name[:short_name_match.end()-4]
        lag_offset = int(short_name[short_name_match.end():])
        return (lag_short_name, lag_offset)
    
    def add_this_lag_offset_to_this_short_name(self, short_name, lag_offset):
        """"""
        if self.is_short_name_for_lag_variable(short_name):
            short_name, dependent_lag_offset = self.parse_lag_variable_short_name(short_name)
            lag_offset += dependent_lag_offset
            
        return '%s_lag%d' % (short_name, lag_offset)
        
from opus_core.tests import opus_unittest
class LagVariableParserTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.parser = LagVariableParser()
        
    def test_parse_lag_variable_short_name(self):
        self.assertEqual(self.parser.parse_lag_variable_short_name('a_lag42'), ('a', 42))
        
    def test_is_short_name_for_lag_variable(self):
        self.assertTrue(self.parser.is_short_name_for_lag_variable('a_lag1'))
        self.assertTrue(self.parser.is_short_name_for_lag_variable('a_lag01'))
        self.assertTrue(not self.parser.is_short_name_for_lag_variable('a_lag_1'))
        self.assertTrue(not self.parser.is_short_name_for_lag_variable('lag1'))
        self.assertTrue(not self.parser.is_short_name_for_lag_variable('_lag1'))
        self.assertTrue(not self.parser.is_short_name_for_lag_variable('a_lag.1'))
# TODO: we want the following two to be true
        self.assertTrue(not self.parser.is_short_name_for_lag_variable('-a_lag1'))
        self.assertTrue(not self.parser.is_short_name_for_lag_variable('a_lag1aa'))
#        self.assert_(not self.parser.is_short_name_for_lag_variable('a_lag1_lag1'))

    def test_add_this_lag_offset_to_this_short_name(self):
        self.assertEqual(self.parser.add_this_lag_offset_to_this_short_name('a_lag1', 2),
            'a_lag3')
        self.assertEqual(self.parser.add_this_lag_offset_to_this_short_name('abc', 5),
            'abc_lag5')
        self.assertEqual(self.parser.add_this_lag_offset_to_this_short_name('abcd', 3),
            'abcd_lag3')
        self.assertEqual(self.parser.add_this_lag_offset_to_this_short_name('abc_lag9', 6),
            'abc_lag15')
        
        
if __name__ == '__main__': 
    opus_unittest.main() 
