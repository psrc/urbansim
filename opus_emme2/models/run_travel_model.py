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

from urbansim.datasets.travel_data_dataset import TravelDataDataset
from opus_core.store.mysql_storage import mysql_storage
from urbansim.datasets.zone_dataset import ZoneDataset
from opus_core.resources import Resources
from numpy import array, float32, ones
from os.path import join
import os
from opus_core.logger import logger
from opus_core.model import Model
from opus_emme2.models.abstract_emme2_travel_model import AbstractEmme2TravelModel
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration

class RunTravelModel(AbstractEmme2TravelModel):
    """Run the travel model.
    """

    def run(self, config, year):
        """Runs the emme2 executables, using appropriate info from config. 
        Assumes the emme2 input files are present. 
        Raise an exception if the emme2 run fails. 
        """        
        emme2_dir = self.get_emme2_dir(config, year)
        logger.log_status('Using emme2 dir %s for year %d' % (emme2_dir, year))
        os.chdir(emme2_dir)
        cache_directory = config['cache_directory']
        emme2_batch_file_path = config['travel_model_configuration'][year]['emme2_batch_file_name']
        log_file_path = os.path.join(cache_directory, 'emme2_%d_log.txt' % year)
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
    (options, args) = parser.parse_args()
   
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))
    
    SessionConfiguration(new_instance=True,
                         package_order=resources['dataset_pool_configuration'].package_order,
                         package_order_exceptions=resources['dataset_pool_configuration'].package_order_exceptions,                              
                         in_storage=AttributeCache())

#    logger.enable_memory_logging()
    RunTravelModel().run(resources, options.year)