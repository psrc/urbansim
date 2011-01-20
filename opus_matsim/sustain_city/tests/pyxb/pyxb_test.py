# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE

import os
from opus_matsim.sustain_city.models.pyxb_xml_parser import update_xml_parser
import opus_matsim.sustain_city.tests.pyxb as pyxb_path
from opus_core.logger import logger

class PyXBTest(object):
    ''' Testing automatic generation of the PyXB binding class.
        The PyXB binding class is needed to create the MATSim configuration via a xsd.
    '''
    
    def __init__(self):
        logger.log_status("Entering setup")
        
        logger.log_status('Testing automatic generation of the PyXB binding class.')
        logger.log_status('The PyXB binding class is needed to create the MATSim configuration via a xsd.')
        
        # destination folder for genereated pyxb binding class
        self.binding_class_destination = pyxb_path.__path__[0]
        # point to test xsd
        self.xsd_file = os.path.join( self.binding_class_destination, 'test_xsd.xsd')
        logger.log_status("Leaving setup")
        
    def test_run(self):
        logger.log_status("Entering test run")
        
        logger.log_status( "Creating a new binding class" )
        # starts creating a new binding class
        return_code = update_xml_parser.UpdateBindingClass().run( self.xsd_file, self.binding_class_destination, None, True )
        self.assertTrue(return_code == 1)
        logger.log_status( "Leaving test run" )
        
if __name__ == "__main__":
    pyxb_test = PyXBTest()
    pyxb_test.test_run()