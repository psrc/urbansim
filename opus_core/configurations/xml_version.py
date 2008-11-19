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

class XmlVersion(object):
    '''Small help class to enable easy version comparison between versions'''
    major = stable = minor = 0
    beta = -1
    
    def __init__(self, version_string = '0.0.0'):
        version_parts = version_string.split('.')
        if not len(version_parts) == 3:
            # should always be three sections
            print('Warning: Incorrect version string format in %s.' %
                  version_string)
            self._print_format()
            return
        try:
            # check if the last part has beta suffix
            minor_beta = version_parts[2].split('-')
            if len(minor_beta) == 2:
                self.minor = int(minor_beta[0])
                self.beta = int(minor_beta[1][4:]) # exclude 'beta' suffix
            elif len(minor_beta) == 1:
                self.minor = int(minor_beta[0])
            else:
                raise ValueError()
            self.major = int(version_parts[0])
            self.stable = int(version_parts[1])
        except ValueError:
            print('Invalid number found in version string "%s"' %version_string)
            self._print_format()
            self.major = self.stable = self.minor = 0
            self.beta = -1
            return

    def __str__(self):
        return ('%d.%d.%d' %(self.major, self.stable, self.minor))
    
    def __cmp__(self, other):
        if isinstance(other, str): # enable comparison with strings
            other = XmlVersion(other)

        if self.major > other.major: return 1
        if self.major < other.major: return -1
        if self.stable > other.stable: return 1
        if self.stable < other.stable: return -1
        if self.minor > other.minor: return 1
        if self.minor < other.minor: return -1
        if self.beta > other.beta: return 1
        if self.beta < other.beta: return -1
        return 0
    
    def _print_format(self):
        print('Correct version string format is: X.X.X[-betaX] (X represents a number).')

class XmlVersionTests(opus_unittest.OpusTestCase):
    
    def test_version_compare(self):
        v1 = XmlVersion('4.2.0')
        v2 = XmlVersion('4.2.2')
        v3 = XmlVersion('4.2.0')
        self.assertTrue(v1 < v2)
        self.assertFalse(v1 > v2)
        self.assertTrue(v1 == v3)
        self.assertTrue(v2 > '4.2.1')
        
        self.assertTrue(XmlVersion('1.0.0-beta3') > '1.0.0')
        self.assertTrue(XmlVersion('1.0.0-beta2') > '1.0.0-beta1')
        
        
    def test_version_string(self):
        v1 = XmlVersion('4.2')
        v2 = XmlVersion('jibberish')
        v3 = XmlVersion('4.3.2.3.3.2.1.3')
        v4 = XmlVersion('1.0.0-beta') # left out beta revision number
        self.assertTrue(v1 == '0.0.0')
        self.assertTrue(v2 == '0.0.0')
        self.assertTrue(v3 == '0.0.0')
        self.assertTrue(v4 == '0.0.0')