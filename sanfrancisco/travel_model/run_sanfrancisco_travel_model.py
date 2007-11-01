#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

from opus_core.store.flt_storage import flt_storage
from opus_core.resources import Resources
from numpy import array, float32, ones
from os.path import join
import os, sys
from opus_core.logger import logger
from travel_model.models.run_travel_model import RunTravelModel
from opus_core.misc import module_path_from_opus_path
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration

class RunSanfranciscoTravelModel(RunTravelModel):
    """Run the travel model.
    """

    def run(self, config, year, *args, **kwargs):
        """Runs the travel model, using appropriate info from config. 
        """
        tm_config = config["travel_model_configuration"]
        tm_data_dir = tm_config["directory"]

        year_dir = tm_config[year]  #'2001\\urbansim'
        dir_part1,dir_part2 = os.path.split(year_dir)
#        while dir_part1:
#            dir_part1, dir_part2 = os.path.split(dir_part1)
        project_year_dir = os.path.join(tm_data_dir, dir_part1)   #C:/SF/2001
        
        logger.log_status('Start travel model from directory %s for year %d' % (project_year_dir, year))

        logger.log_status('Running travel model ...')
        cmdline = tm_config['travel_model_command'] + ' ' + project_year_dir
        os.system(cmdline)

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
    
#    options.resources_file_name = "c:\urbansim_cache\semcog_test_tm.pickle"
#    options.year = 2001   
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))

    SessionConfiguration(new_instance=True,
                         package_order=resources['dataset_pool_configuration'].package_order,
                         package_order_exceptions=resources['dataset_pool_configuration'].package_order_exceptions,                              
                         in_storage=AttributeCache())

#    logger.enable_memory_logging()
    RunSanfranciscoTravelModel().run(resources, options.year)    
