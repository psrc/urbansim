# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE

import os
from opus_matsim.models.pyxb_xml_parser import update_xml_parser
from opus_core.logger import logger
from opus_core.tests import opus_unittest
from shutil import rmtree
import opus_matsim, tempfile

class PyXBBindigClassGeneration(opus_unittest.OpusTestCase):
    ''' Testing automatic generation of the PyXB binding class.
        The PyXB binding class is needed to create the MATSim configuration via a xsd.
    '''
    
    def setUp(self):
        print "entering setUp"
        logger.log_status('Testing automatic generation of the PyXB binding class.')
        logger.log_status('The PyXB binding class is needed to create the MATSim configuration via a xsd.')
        # point to test xsd
        self.xsd_file = os.path.join(opus_matsim.__path__[0], 'tests', 'testdata', 'pyxb_data', 'test_xsd.xsd')
        # destination folder for generated pyxb binding class
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        print "leaving setUp"

    def tearDown(self):
        print "entering tearDown"
#        # Turn off the logger, so we can delete the cache directory.
#        logger.disable_all_file_logging()
        print "leaving tearDown"

    def cleanup_test_run(self):
        print "entering cleanup_test_run"
#        cache_dir = self.resources['cache_directory']
#        if os.path.exists(cache_dir):
#            rmtree(cache_dir)
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        print "leaving cleanup_test_run"
        
    def test_run(self):
        logger.log_status("Entering test run")
        
        logger.log_status( "Creating a new binding class" )
        # starts creating a new binding class
        return_code = update_xml_parser.UpdateBindingClass().run( self.xsd_file, self.temp_dir, None, True )
        
        self.assertTrue(return_code == 1)
        logger.log_status( "Leaving test run" )
        
if __name__ == "__main__":
    opus_unittest.main()
    