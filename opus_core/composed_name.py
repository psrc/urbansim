#
# Opus software. Copyright (C) 2005-2008 University of Washington
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

import re
import string

class ComposedName(object):
    """Class for parsing a name of type 'opus_core.myclass'.
    Class attribute self.full_name is then 'opus_core.myclass', self._short_name is 'myclass'
    and self.package_name is 'opus_core'.
    """
    def __init__(self, name):
        self._full_name = name
        self._package_name, self._short_name = self.parse_name(name)

    def parse_name(self, fullname):
        """Parse the given argument and return a tuple of 
        (package_name, short_name).
        """ 
        splitname = re.split("\.", fullname)
        lsplit = len(splitname)
        if (lsplit <= 1):
            return (None, fullname) 
        pkg_name = string.join(splitname[0:(lsplit-1)],'.')
        short_name = splitname[lsplit-1]
        return (pkg_name, short_name) 
    
    def get_package_name(self):
        return self._package_name
    
    def get_full_name(self):
        return self._full_name
    
    def get_short_name(self):
        return self._short_name

from opus_core.tests import opus_unittest   
class ComposedNameTests(opus_unittest.OpusTestCase):
    def test_composed_name1(self):
        name = ComposedName("opus_core.mnl_probabilities")
        self.assertEqual(name.get_package_name(), 
                         "opus_core", msg = "Error in get_package_name()")
        self.assertEqual(name.get_short_name(), 
                         "mnl_probabilities", msg = "Error in get_short_name()")    
                                     
    def test_composed_name2(self):
        name = ComposedName("linear_utilities")
        self.assertEqual(name.get_package_name(), 
                         None, msg = "Error in get_package_name()")
        self.assertEqual(name.get_short_name(), 
                         "linear_utilities", msg = "Error in get_short_name()")  
                                                                                                                                                 
if __name__=='__main__':
    opus_unittest.main()
    