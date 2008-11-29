#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

import os, sys
from opus_core.session_configuration import SessionConfiguration
from opus_core.resources import Resources
from opus_core.logger import logger
from travel_model.models.abstract_travel_model import AbstractTravelModel

class RunTravelModel(AbstractTravelModel):
    """Run the travel model.
    """

    def run(self, config, year):
        """
        """
        
        logger.start_block("Starting RunTravelModel.run(...)")
        
        travel_model_configuration = config['travel_model_configuration']
        for key in travel_model_configuration:
            logger.log_status( " key: " + key.__str__() )
        
        matsim_config_filename = travel_model_configuration['matsim_config_filename']
        
        cmd = """cd %(opus_home)s/opus_matsim ; java %(vmargs)s -cp %(classpath)s %(javaclass)s %(matsim_config_file)s""" % {
                'opus_home': os.environ['OPUS_HOME'],
                'vmargs': "-Xmx2000m",
                'classpath': "/home/nagel/eclipse/matsim-trunk/classes:jar/MATSim_r3885.jar",
#                'javaclass': "org.matsim.run.Matsim4Urbansim",
                'javaclass': "playground.kai.urbansim.Matsim4Urbansim",
                'matsim_config_file': matsim_config_filename } 
        
# FIXME: (after debugging is finished): 
# (1) replace *.jar by something more up to date
# (2) rm reference to "/home/nagel/eclipse/matsim-trunk/classes"

# TODO:
# - configuration can be made more flexible
        
        logger.log_status('Running command %s' % cmd ) 
        
        cmd_result = os.system(cmd)
        if cmd_result != 0:
            error_msg = "Matsim Run failed. Code returned by cmd was %d" % (cmd_result)
            logger.log_error(error_msg)
            raise StandardError(error_msg)        
        
        logger.end_block()

# called from the framework via main!	    
if __name__ == "__main__":
    try: import wingdbstub
    except: pass
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
    RunTravelModel().run(resources, options.year)    
