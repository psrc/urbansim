# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import time, os
from opus_matsim.sustain_city.models.run_travel_model import RunTravelModel
from opus_core.logger import logger
from opus_core.resources import Resources
from opus_matsim.sustain_city.models.pyxb_xml_parser.config_object import MATSimConfigObject
from opus_core import paths

class RunMATSimPsrcTest(RunTravelModel):


    def __init__(self):
        RunTravelModel.__init__(self)
        
    def run(self, config, year):

        # execute the MATSim config generation
        self.start_time = time.time()
        self.__setUp( config )    # setup location
        
        config_obj = MATSimConfigObject(config, year, self.matsim_config_full)
        config_obj.marschall()  # generation process
        self.end_time = time.time()
        
        #try: #tnicolai
        #    import pydevd
        #    pydevd.settrace()
        #except: pass        
        
        # store reults in logfile
        self.dump_results(config, 
                          int ( os.path.getsize(self.matsim_config_full)), 
                          int ( self.end_time-self.start_time ))
        
        # run MATSim 
        # MATSim measures the following values:
        # 1) duration to read the UrbanSim input (parcel- and person table, config)
        # 2) size of MATSim output (travel_data, otheer outputs)
        # 3) duration to write all outputs
        # all measurements are stored in the same logfile
        cmd = """cd %(opus_home)s/opus_matsim ; java %(vmargs)s -cp %(classpath)s %(javaclass)s %(matsim_config_file)s""" % {
                'opus_home': paths.OPUS_HOME,
                'vmargs': "-Xmx2500m",
                'classpath': "libs/log4j/log4j/1.2.15/log4j-1.2.15.jar:libs/jfree/jfreechart/1.0.7/jfreechart-1.0.7.jar:libs/jfree/jcommon/1.0.9/jcommon-1.0.9.jar:classesMATSim:classesToronto:classesTNicolai:classesKai:classesEntry", #  'classpath': "classes:jar/MATSim.jar",
                'javaclass': "playground.tnicolai.urbansim.MATSim4UrbanSimMeasurement",
                'matsim_config_file': self.matsim_config_full } 
        
        logger.log_status('Running command %s' % cmd ) 
        
        cmd_result = os.system(cmd)
        if cmd_result != 0:
            error_msg = "Matsim Run failed. Code returned by cmd was %d" % (cmd_result)
            raise StandardError(error_msg)        
        
    def dump_results(self, config, config_file, duration):
        
        logger.log_status('Loging results...')
        
        file = config['psrc_logfile']
        
        # append measurements to log file
        file_object = open( file , 'a') 
        
        file_object.write('Size of matsim config in MBytes:%f\n'%(config_file/(1024.0**2))) 
        file_object.write('Duration writing config in seconds:%f\n'%duration) 
        file_object.write('\n') 
        
        file_object.flush()
        if not file_object.closed:
            file_object.close()
        
# called from opus via main!
if __name__ == "__main__":
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    (options, args) = parser.parse_args()
    resources = Resources(get_resources_from_file(options.resources_file_name))

    logger.enable_memory_logging()
    RunMATSimPsrcTest().run(resources, options.year)  
        