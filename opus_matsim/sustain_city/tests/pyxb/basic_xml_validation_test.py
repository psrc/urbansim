# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE

import os, sys
from lxml import etree
import opus_matsim.sustain_city.tests as test_path
import opus_matsim.sustain_city.tests.pyxb as pyxb_test
from opus_core.logger import logger
import shutil

class Basic_XSD_Validation(object):
    """ This test validates the generated xml MATSim configuration while using pyxb's own validation process.
    """
    
    def __init__(self, config_path=None, config_file_name=None, xsd_file_name=None):
        print "Entering setup"
        
        logger.log_status('Validation test of genereated MATSim configuration via xsd...')
        
        # xml destination
        self.matsim_config_file = self.matsim_config_destination = os.path.join( os.environ['OPUS_HOME'], "opus_matsim", "matsim_config", "test_matsim_config.xml")
        
        # create xml config file (only possible if pyxb is installed) ...
        # from opus_matsim.sustain_city.tests.pyxb.create_MATSim_config import Create_MATSim_Config
        # config_creator = Create_MATSim_Config(config_path, config_file_name, self.matsim_config_file)
        # if not config_creator.build_xml_config():
        #    logger.log_error("Problems while creating MATSim config file...")
        #    sys.exit()
        
        # ... therefore we are copying a matsim confing file
        logger.log_note('An exsisting configuration file will be used for this test, since PyXB needed to be installed to create the MATSim configuration.')
        # If the automatic generation of the MATSim configuration is desierd, please enable "Create_MATSim_Config" and disable "self.copy_matsim_config()" function in this test class.
        self.copy_matsim_config()
        
        self.config_path = config_path
        if self.config_path == None:
            self.config_path = pyxb_test.__path__[0]
        self.config_name = config_file_name
        if self.config_name == None:
            self.config_name = 'test_urbansim_config.xml'
        self.xsd_name = xsd_file_name
        if self.xsd_name == None:
            self.xsd_name = 'test_xsd.xsd'

        # get xsd location
        self.xsd_file = os.path.join(self.config_path, self.xsd_name)
        if not os.path.exists( self.xsd_file ):
            sys.exit()
        
        print "Leaving setup"
        
    def tearDown(self):
        print "Entering tearDown"
        if os.path.exists(self.matsim_config_file):
            os.remove(self.matsim_config_file)
        print "Leaving tearDown"
    
    def test_run(self):
        print "Entering test run"
        
        # load xml and xsd
        logger.log_status("Loading XML file: {0}".format(self.matsim_config_file))
        library = open(self.matsim_config_file)
        
        logger.log_status("Loading XSD file: {0}".format(self.xsd_file))
        schema = open(self.xsd_file)
        
        # create object instance of xsd for xml validation
        xmlschema_doc = etree.parse(schema)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        # parsing xml file
        library_doc = etree.parse(library)
        
        logger.log_status( "Validationg XML" )
        
        result = xmlschema.validate(library_doc)
        
        if result: logger.log_status("Valid XML")
        else: logger.log_status("Invalid XML")

        #self.assertEqual(result, True)
        self.tearDown()
                
        logger.log_status("Leaving test run")
        
    def load(self, path):
        if not os.path.exists(path):
            logger.log_error("File %s not found!" % path)
            sys.exit()
        logger.log_status("Loading file: {0}".format( path ))
        return open(self.matsim_config_file)
    
    def copy_matsim_config(self):
        
        source = os.path.join( test_path.__path__[0], 'configs', 'matsim_config', 'test_matsim_config.xml')
        if not os.path.exists(source):
            raise StandardError('MATSim config file not found: %s' % source)
        
        shutil.copy(source, self.matsim_config_file)
        
if __name__ == "__main__":
    basic_validation = Basic_XSD_Validation()
    basic_validation.test_run()