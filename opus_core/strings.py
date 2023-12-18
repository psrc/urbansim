# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

"""Collection of useful miscellaneous functions and definitions"""

# define very basic operations without importing anything from opus_core

def create_list_string(list_, sep='\n'):
    """Returns a string of the list elements separated by sep."""
    # a very efficient function
    return sep.join(list_)

def indent_text(text, depth=4):
    """
    Indent every line of the text by the same amount of spaces.
    """
    indent = ' ' * depth
    return create_list_string([indent + line for line in text.split('\n')])

from opus_core.tests import opus_unittest

class StringsTests(opus_unittest.OpusTestCase):
    def test_indent_text(self):
        self.assertEqual(indent_text('a\nb\n', 2), '  a\n  b\n  ')
        self.assertEqual(indent_text('a\nb\n'), '    a\n    b\n    ')
             
    def test_create_list_string(self):
        self.assertEqual(create_list_string(['aa', 'b', '', ' dd'], 'SEP'), 'aaSEPbSEPSEP dd')
        self.assertEqual(create_list_string(['aa', 'b', '', ' dd']), 'aa\nb\n\n dd')
        
if __name__ == "__main__":
    opus_unittest.main()
