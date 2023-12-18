# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.opus_exceptions.xml_version_exception import XMLVersionException

class XMLVersion(object):
    """Holds an Opus XML version number of the form 1.0 (i.e. major number, period, minor number), for easy
    comparison.  The default value is 0.0, which is intended to be less than any actual XML version number."""
    def __init__(self, version_string='0.0'):
        # TODO: remove this test for old-style version numbers in a bit (say after May 2009), after there won't be any floating around
        if version_string.startswith('4.2.'):
            raise XMLVersionException('this is an old-style XML configuration number -- please update')
        version_parts = version_string.split('.')
        if not len(version_parts) == 2:
            raise XMLVersionException('invalid format for XML version number')
        try:
            self.major = int(version_parts[0])
            self.minor = int(version_parts[1])
        except ValueError:
            raise XMLVersionException('invalid format for XML version number')

    def __str__(self):
        return '%d.%d' % (self.major, self.minor)
        
    def __cmp__(self, other):
        if isinstance(other, str): # enable comparison with strings
            other = XMLVersion(other)

        if self.major > other.major: return 1
        if self.major < other.major: return -1
        return self.minor.__cmp__(other.minor)
    

from opus_core.tests import opus_unittest
    
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
        
    def test_version_exceptions(self):
        self.assertRaises(XMLVersionException, XMLVersion, 'badstuff')
        self.assertRaises(XMLVersionException, XMLVersion, '4.2.0')
        self.assertRaises(XMLVersionException, XMLVersion, '1.0.0')
        
if __name__ == '__main__':
    opus_unittest.main()
