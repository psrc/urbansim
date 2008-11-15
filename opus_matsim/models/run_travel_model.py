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
        
        emme2_batch_file_path = self.get_emme2_batch_file_path(year)
        emme2_dir, emme2_batch_file_name = os.path.split(emme2_batch_file_path)
        logger.log_status('Using emme2 dir %s for year %d' % (emme2_dir, year))
        os.chdir(emme2_dir)
        if output_file is None:
            log_file_path = os.path.join(self.config['cache_directory'], 'emme2_%d_log.txt' % year)
        else:
            log_file_path = output_file
        
        cmd = """%(system_cmd)s"%(emme2_batch_file_name)s" > %(log_file_path)s""" % {
                'system_cmd': self.config['travel_model_configuration'].get('system_command', 'cmd /c '),
                'emme2_batch_file_name':emme2_batch_file_path, 
                'log_file_path':log_file_path,
                } 
        logger.log_status('Running command %s' % cmd)
        cmd_result = os.system(cmd)
        if cmd_result != 0:
            error_msg = "Emme2 Run failed. Code returned by cmd was %d" % (cmd_result)
            logger.log_error(error_msg)
            raise StandardError(error_msg)        

#        tm_config = config['travel_model_configuration']
#	
#        #Get config params
#        visum_dir, fileName = tm_config[year]['version']
#	visum_version_number = tm_config['visum_version_number']
#        
#        #Startup Visum
#        Visum = load_version_file(visum_dir, fileName)
#
#        #Load procedure file and execute
#        parFileName = tm_config[year]['procedure_file']	
#        try:
#	    Visum.Procedures.Open(parFileName)
#	    Visum.Procedures.Execute()
#        except Exception:
#	    error_msg = "Loading and executing procedures file failed"
#	    raise StandardError(error_msg)
#
#	#Save version file
#	#This saves over the existing version file
#        try:
#        	Visum.SaveVersion(fileName)
#        except Exception:
#        	error_msg = "Saving version file failed"
#        	raise StandardError(error_msg)
        
        logger.end_block()
	    
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
