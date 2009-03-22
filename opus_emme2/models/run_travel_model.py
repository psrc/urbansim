# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import re
from opus_core.resources import Resources
from numpy import array, float32, ones
import os
from opus_core.logger import logger
from opus_emme2.models.abstract_emme2_travel_model import AbstractEmme2TravelModel
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.sftp_flt_storage import redirect_sftp_url_to_local_tempdir

class RunTravelModel(AbstractEmme2TravelModel):
    """Run the travel model.
    """
        
    def run(self, year, output_file=None):
        """Runs the emme2 executables, using appropriate info from config. 
        Assumes the emme2 input files are present. 
        Raise an exception if the emme2 run fails. 
        """        
        emme2_batch_file_path = self.get_emme2_batch_file_path(year)
        emme2_dir, emme2_batch_file_name = os.path.split(emme2_batch_file_path)
        logger.log_status('Using emme2 dir %s for year %d' % (emme2_dir, year))
        os.chdir(emme2_dir)
        if output_file is None:
            log_file_path = os.path.join(self.config['cache_directory'], 'emme2_%d_log.txt' % year)
        else:
            log_file_path = output_file
        
        # if log_file_path is a remote sftp URL, redirect the log file to tempdir           
        log_file_path = redirect_sftp_url_to_local_tempdir(log_file_path)
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
    parser.add_option("-o", "--output-file", dest="output_file", action="store", type="string",
                      help="Output log file. If not given, it is written into urbansim cache directory.")
    (options, args) = parser.parse_args()
   
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))
    
    SessionConfiguration(new_instance=True,
                         package_order=resources['dataset_pool_configuration'].package_order,                             
                         in_storage=AttributeCache())

#    logger.enable_memory_logging()
    RunTravelModel(resources).run(options.year, options.output_file)
