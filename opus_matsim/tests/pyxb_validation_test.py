# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE

import os, opus_matsim
from opus_core.logger import logger
from lxml import etree
from opus_core.tests import opus_unittest

class PyxbValidation(opus_unittest.OpusTestCase):
    """ This test validates the generated xml MATSim configuration while using pyxb's own validation process.
    """
    
    def setUp(self):
        print("entering __setUp")
        self.config_location = os.path.join(opus_matsim.__path__[0], 'tests', 'testdata', 'pyxb_data')
        print("leaving __setUp")

    def tearDown(self):
        print("entering tearDown")
#        # Turn off the logger, so we can delete the cache directory.
#        logger.disable_all_file_logging()
        print("leaving tearDown")

    def cleanup_test_run(self):
        print("entering cleanup_test_run")
        print("leaving cleanup_test_run")
    
    def test_run(self):
        print("Entering test run")
        
        # xml config
        config_file = os.path.join( self.config_location, "test_config.xml")
        # xsd
        xsd_file = os.path.join( self.config_location, "test_xsd.xsd")
        
        # load xml and xsd
        logger.log_status("Loading XML file: {0}".format(config_file))
        library = open(config_file)
        
        logger.log_status("Loading XSD file: {0}".format(xsd_file))
        schema = open(xsd_file)
        
        # create object instance of xsd for xml validation
        xmlschema_doc = etree.parse(schema)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        # parsing xml file
        library_doc = etree.parse(library)
        
        logger.log_status( "Validating XML" )
        
        result = xmlschema.validate(library_doc)

        self.assertTrue(result == True)
                
        logger.log_status("Leaving test run")

if __name__ == "__main__":
    opus_unittest.main()