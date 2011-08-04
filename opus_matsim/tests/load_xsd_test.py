# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE
from opus_core.tests import opus_unittest
from opus_core.logger import logger
import urllib2
import opus_matsim
import os, tempfile

class XSDLoadTest(opus_unittest.OpusTestCase):


    def setUp(self):
        logger.log_status('entering setUp')
        self.current_location = os.path.join(opus_matsim.__path__[0], 'tests')
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        self.xsd_source = 'http://matsim.org/files/dtd/MATSim4UrbanSimConfigSchema.xsd'
        logger.log_status('leaving setUp')


    def tearDown(self):
        logger.log_status('entering tearDown')
        logger.log_status('Removing loaded/stored file: %s ...' %self.xsd_destination)
        if os.path.exists(self.xsd_destination):
            os.remove(self.xsd_destination)
        logger.log_status('... removing finished.')
        logger.log_status('leaving tearDown')

    def test_run(self):
        
        logger.log_status('entering test_run')
        
        self.xsd_destination = os.path.join(self.temp_dir, 'MATSim4UrbanSimConfigSchema.xsd')
        logger.log_status('Loading xsd file from: %s' %self.xsd_source)
        
        response = urllib2.urlopen( self.xsd_source )
        xsd = response.read()
        
        logger.log_status('Storing xsd file at: %s' %self.xsd_destination)
        outfile = open( self.xsd_destination, 'w')
        outfile.write( xsd )
        outfile.flush()
        outfile.close()

        self.assertTrue( os.path.exists(self.xsd_destination) )
        
        logger.log_status('leaving test_run')

if __name__ == "__main__":
    opus_unittest.main()
    