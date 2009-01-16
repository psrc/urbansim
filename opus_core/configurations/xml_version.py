#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from opus_core.tests import opus_unittest

class XMLVersion(object):
    """Holds an Opus XML version number of the form 1.0 (i.e. major number, period, minor number), for easy
    comparison.  The default value is 0.0, which is intended to be less than any actual XML version number."""
    def __init__(self, version_string='0.0'):
        if version_string.startswith('4.2'):
            raise ValueError, 'this is an old-style XML configuration number -- please update'
        version_parts = version_string.split('.')
        if not len(version_parts) == 2:
            raise ValueError, 'invalid format for XML version number'
        try:
            self.major = int(version_parts[0])
            self.minor = int(version_parts[1])
        except ValueError:
            raise ValueError, 'invalid format for XML version number'

    def __str__(self):
        return '%d.%d' % (self.major, self.minor)
        
    def __cmp__(self, other):
        if isinstance(other, str): # enable comparison with strings
            other = XMLVersion(other)

        if self.major > other.major: return 1
        if self.major < other.major: return -1
        return self.minor.__cmp__(other.minor)
    
class XMLVersionTests(opus_unittest.OpusTestCase):
    
    def test_version_compare(self):
        v0 = XMLVersion()
        v1 = XMLVersion('1.1')
        v2 = XMLVersion('1.2')
        v3 = XMLVersion('3.0')
        self.assertTrue(v0 < v1)
        self.assertTrue(v1 < v2)
        self.assertTrue(v2 < v3)
        self.assertFalse(v1 > v2)
        self.assertTrue(v1 == v1)
        self.assertTrue(v3 > v1)
        
    def test_version_string(self):
        self.assertTrue(XMLVersion('1.2') == '1.2')
        self.assertTrue(XMLVersion('1.2') > '1.0')
        self.assertTrue(XMLVersion('1.2') < '2.0')
        
if __name__ == '__main__':
    opus_unittest.main()
