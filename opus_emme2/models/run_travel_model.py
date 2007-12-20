#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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


from opus_core.resources import Resources
from numpy import array, float32, ones
import os
from opus_core.logger import logger
from opus_emme2.models.abstract_emme2_travel_model import AbstractEmme2TravelModel
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration

class RunTravelModel(AbstractEmme2TravelModel):
    """Run the travel model.
    """

    def run(self, config, year, output_file=None):
        """Runs the emme2 executables, using appropriate info from config. 
        Assumes the emme2 input files are present. 
        Raise an exception if the emme2 run fails. 
        """        
        emme2_dir = self.get_emme2_dir(config, year)
        logger.log_status('Using emme2 dir %s for year %d' % (emme2_dir, year))
        os.chdir(emme2_dir)
        emme2_batch_file_path = config['travel_model_configuration'][year]['emme2_batch_file_name']
        if output_file is None:
            log_file_path = os.path.join(config['cache_directory'], 'emme2_%d_log.txt' % year)
        else:
            log_file_path = output_file
            
        if re.search("^sftp://", log_file_path):  # if cache_directory is a remote sftp URL, redirect log file to tempdir/run_xxxx
            import tempfile
            from urlparse import urlparse
            log_file_path = urlparse(log_file_path).path
            log_file_path = os.path.join(tempfile.gettempdir(), 
                                         os.path.basename( os.path.dirname(log_file_path) ), #run_xxxx.2007_12_19_16_32
                                         os.path.basename(log_file_path))
            os.makedirs( os.path.dirname(log_file_path) )

        cmd = """cmd /c "%(emme2_batch_file_name)s" > %(log_file_path)s""" % {
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
                         package_order_exceptions=resources['dataset_pool_configuration'].package_order_exceptions,                              
                         in_storage=AttributeCache())

#    logger.enable_memory_logging()
    RunTravelModel().run(resources, options.year, options.output_file)
