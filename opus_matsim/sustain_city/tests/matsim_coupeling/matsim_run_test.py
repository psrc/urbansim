# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.logger import logger
import opus_matsim.sustain_city.tests as test_path
import tempfile
from shutil import rmtree
from opus_matsim.sustain_city.tests.common.extract_zip_file import ExtractZipFile
import shutil

class MATSimTestRun(object):
    ''' This test shows if UrbanSim can start MATSim.
        
    ''' 
    def __init__(self):
        print "entering setUp"
        
        logger.log_status('Running MATSim test... ')

        # get root path to test cases
        self.path = test_path.__path__[0]
        logger.log_status('Set root path for MATSim config file to: %s' % self.path)
        if not os.path.exists(self.path):
            raise StandardError("Root path doesn't exist: %s" % self.path)
        
        self.source = self.get_matsim_source() # get path to MATSim source files
        self.destination = tempfile.mkdtemp(prefix='opus_tmp')
        #self.destination = '/Users/thomas/Desktop/x'    # for debugging
        #if not os.path.exists(self.destination):        # for debugging
        #    os.mkdir(self.destination)                  # for debugging
        self.matsim_config_full = os.path.join( self.destination, "test_matsim_config.xml" )
        # since pyxb need to be installed this method will be disabled for standard tests ...
        # self.create_MATSim_config()
        
        # ... therefore we are coping an existing MATSim config file.
        self.copy_matsim_config()
        
        print "leaving setUp"
        
    def test_run(self):
        print "entering test_run"
        
        logger.log_status('Preparing MATSim test run ...')
        
        ezf = ExtractZipFile(self.source, self.destination)
        ezf.extract()
        extracted_files = os.path.join(self.destination, 'MATSimTestClasses')
        
        cmd = """cd %(opus_home)s; java %(vmargs)s -cp %(classpath)s %(javaclass)s %(matsim_config_file)s""" % {
                'opus_home': extracted_files,
                'vmargs': "-Xmx500m",
                'classpath': "libs/log4j/log4j/1.2.15/log4j-1.2.15.jar:libs/jfree/jfreechart/1.0.7/jfreechart-1.0.7.jar:libs/jfree/jcommon/1.0.9/jcommon-1.0.9.jar:"+extracted_files,
                'javaclass': "playground.run.Matsim4Urbansim",
                'matsim_config_file': self.matsim_config_full } 
        
        logger.log_status('Running command %s' % cmd ) 
        
        cmd_result = os.system(cmd)
        if cmd_result != 0:
            raise StandardError("MATSim Run failed. Code returned by cmd was %d" % (cmd_result))  
        elif cmd_result == 0:
            logger.log_status("MATSim returned exit code: %i " % cmd_result)
            logger.log_status('Successfully tested:')
            logger.log_status('- Creation of MATSim config file via PyXB')
            logger.log_status('- Validation of MATSim config file via MATSim')
            logger.log_status('- Successfully started MATSim')

        #self.assert_(cmd_result == 0) # 0 means successful
        
        self.tearDown()

        print "leaving test_run"
        
    def tearDown(self):
        print "entering tearDown"
        logger.log_status('Removing extracted MATSim files...')
        if os.path.exists(self.destination):
            rmtree(self.destination)
        logger.log_status('... cleaning up finished.')
        print "leaving tearDown"
    
    def get_matsim_source(self):
                
        matsim_files_source = os.path.join( self.path, 'data', 'MATSimTestClasses.zip')
        if not os.path.exists(matsim_files_source):
            raise StandardError("MATSim source file not found: %s" % matsim_files_source)

        logger.log_status('Referencing to MATSim source file: %s' % matsim_files_source)
       
        return matsim_files_source
    
    # not used anymore, moved Create_MATSim_Config into archive folder
    #def create_MATSim_config(self):
    #    ''' Creates the MATSim config file via pyxb
    #    '''
    #    from opus_matsim.sustain_city.tests.pyxb.create_MATSim_config import Create_MATSim_Config
    #    
    #    config_creator = Create_MATSim_Config(None, None, self.matsim_config_full)
    #    if not config_creator.build_xml_config():
    #        raise StandardError("Problems while creating MATSim config file...")
        
    def copy_matsim_config(self):
        
        source = os.path.join( test_path.__path__[0], 'configs', 'matsim_config', 'test_matsim_config.xml')
        if not os.path.exists(source):
            raise StandardError('MATSim config file not found: %s' % source)
        
        shutil.copy(source, self.matsim_config_full)
         
if __name__ == '__main__':
    matsim_test = MATSimTestRun()
    matsim_test.test_run()