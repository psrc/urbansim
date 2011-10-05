# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE

import os
from opus_matsim.models.pyxb_xml_parser import update_xml_parser
from opus_core.logger import logger
#from opus_core.tests import opus_unittest
from shutil import rmtree
import opus_matsim, tempfile

#class PyXBBindingClassGeneration(opus_unittest.OpusTestCase):
class PyXBBindingClassGeneration():
    ''' Testing automatic generation of the PyXB binding class.
        The PyXB binding class is needed to create the MATSim configuration via a xsd.
        
        This test was removed from automatic unit_test since the pyxb is none of UrbanSim standard
        packages. 
        This test needs to be executed manually!
    '''
    
    def setUp(self):
        print "entering __setUp"
        logger.log_status('Testing automatic generation of the PyXB binding class.')
        logger.log_status('The PyXB binding class is needed to create the MATSim configuration via a xsd.')
        # point to test xsd
        self.xsd_file = os.path.join(opus_matsim.__path__[0], 'tests', 'testdata', 'pyxb_data', 'test_xsd.xsd')
        # destination folder for generated pyxb binding class
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        print "leaving __setUp"

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
        return_code = update_xml_parser.UpdateBindingClass().run( self.xsd_file, self.temp_dir, None, False )
        
        #self.assertTrue(return_code == 1)
        if return_code == 1:
            print "PyxB binding class generation was successful !"
        else:
            print "Error while generating PyxB binding class!"
        
        logger.log_status( "Leaving test run" )
        
if __name__ == "__main__":
#    opus_unittest.main()
    test = PyXBBindingClassGeneration()
    test.setUp()
    test.test_run()
    test.tearDown()
    test.cleanup_test_run()   