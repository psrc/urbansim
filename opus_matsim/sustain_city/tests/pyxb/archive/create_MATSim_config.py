# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE

import os
import opus_matsim.sustain_city.tests.pyxb as pyxb_test
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_matsim.sustain_city.tests.pyxb import pyxb_matsim_config_parser as xsd_binding

class Create_MATSim_Config(object):
    ''' Creates a configuration file for MATSim
    '''

    def __init__(self, config_path=None, config_file_name=None, destination=None, testRun=True):
        ''' Constructor
        '''
        print "Entering __init__"
        
        # load test urbansim config
        self.config_path = config_path
        if self.config_path == None:
            self.config_path = pyxb_test.__path__[0]
        self.config_name = config_file_name
        if self.config_name == None:
            self.config_name = 'test_urbansim_config.xml'
        self.matsim_config_location = destination
        if self.matsim_config_location == None:
            self.matsim_config_destination = os.path.join( os.environ['OPUS_HOME'], "opus_matsim", "matsim_config")
            if not self.test_path( self.matsim_config_destination ):
                return False
            self.matsim_config_location = os.path.join( self.matsim_config_destination, "test_matsim_config.xml")
        
        self.config_location = os.path.join( self.config_path, self.config_name)
        print "Loding test config file: %s" % self.config_location
        self.config = XMLConfiguration( self.config_location  ).get_run_configuration( "Test" )
        
        # get travel model parameter from the opus dictionary
        self.travel_model_configuration = self.config['travel_model_configuration']
        # get years parameter
        self.years = self.config['years']
        
        # gather all parameters for the MATSim config file
        # network parameter
        self.network_file = self.travel_model_configuration['matsim_network_file']
        self.network_file = os.path.join( os.environ['OPUS_HOME'], "opus_matsim", self.network_file)
        # controler parameter:
        self.first_iteration = self.travel_model_configuration['first_iteration']
        self.last_iteration = self.travel_model_configuration['last_iteration']
        # planCalcScoreType
        self.activityType_0 = self.travel_model_configuration['activityType_0']
        self.activityType_1 = self.travel_model_configuration['activityType_1']
        # urbansim parameter
        self.year = self.years[0]
        self.samplingRate = self.travel_model_configuration['sampling_rate']
        self.temp_directory = self.travel_model_configuration['temp_directory']
        self.isTestRun = testRun
        self.opus_home = os.environ['OPUS_HOME']
        self.firstRun = "FALSE"
        
        # create xml config file
        # return self.build_xml_config()
        print "Leaving __init__"
        
    def test_path(self, path):
        # check if this folder exists
        if not os.path.exists(path):
            # create folder and subfolders if it's not exsist
            try:
                print "Creating MATSim config path %s" % path 
                os.mkdir(path)
            except: return False
        return True
        
    def build_xml_config(self):
        
        print "Entering build_xml_config"
        
        # xml root element (for the xml MATSim config)
        root = xsd_binding.configType.Factory()
        # child nodes of the xml root
        network_elem = xsd_binding.networkType.Factory()
        controler_elem = xsd_binding.controlerType.Factory()
        plan_calc_score_elem = xsd_binding.planCalcScoreType.Factory()
        urbansim_elem = xsd_binding.urbansimParameterType.Factory()
        
        # create content
        network_elem.inputFile = self.network_file
        
        controler_elem.firstIteration = self.first_iteration
        controler_elem.lastIteration = self.last_iteration
        
        plan_calc_score_elem.activityType_0 = self.activityType_0
        plan_calc_score_elem.activityType_1 = self.activityType_1
        
        urbansim_elem.samplingRate = self.samplingRate
        urbansim_elem.year = self.year
        urbansim_elem.tempDirectory = self.temp_directory
        urbansim_elem.isTestRun = self.isTestRun
        urbansim_elem.opusHOME = self.opus_home
        
        root.network = network_elem
        root.controler = controler_elem
        root.planCalcScore = plan_calc_score_elem
        root.urbansimParameter = urbansim_elem

        # convert to dom object
        dom = root.toDOM(element_name='config')
        # print on screen
        prettydom = dom.toprettyxml(encoding="UTF-8")
        print "Created MATSim config\n\n %s" % prettydom

        # write xml config onto hard disc
        file_object = open( self.matsim_config_location, 'w')
        #dom.writexml(file_object, encoding="UTF-8") # no pretty format :-(
        file_object.write(prettydom) # maybe the better way to save matsim config xml ?
        file_object.flush()
        if not file_object.closed:
            file_object.close()
            
        print "Leaving build_xml_config"
        return True
            
if __name__ == "__main__":
    cmc = Create_MATSim_Config()
    cmc.build_xml_config()