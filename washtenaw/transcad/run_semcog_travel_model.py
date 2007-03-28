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

from opus_core.store.mysql_storage import mysql_storage
from opus_core.store.flt_storage import flt_storage
from opus_core.resources import Resources
from numpy import array, Float32, ones
from os.path import join
import os, sys
from opus_core.logger import logger
from travel_model.models.run_travel_model import RunTravelModel
from opus_core.misc import module_path_from_opus_path
from washtenaw.travel_model.run_transcad_macro import run_transcad_macro
import win32pdhutil, win32api, win32process
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from washtenaw.travel_model.set_project_ini_file import set_project_ini_file

class RunSemcogTravelModel(RunTravelModel):
    """Run the travel model.
    """

    def run(self, config, year, *args, **kwargs):
        """Runs the travel model, using appropriate info from config. 
        """
        tm_config = config["travel_model_configuration"]
        tm_data_dir = tm_config["directory"]
        self.prepare_for_run(tm_config, year)

        year_dir = tm_config[year]  #'CoreEA0511202006\\urbansim\\2001'
        dir_part1,dir_part2 = os.path.split(year_dir)
        while dir_part1:
            dir_part1, dir_part2 = os.path.split(dir_part1)
        project_year_dir = os.path.join(tm_data_dir, dir_part2)   #C:/SEMCOG_baseline/CoreEA0511202006
        
        logger.log_status('Start travel model from directory %s for year %d' % (project_year_dir, year))
        for macroname, ui_db_file in tm_config['macro']['run_semcog_travel_model'].iteritems():
            ui_db_file = os.path.join(tm_config['directory'], ui_db_file)

        loops = 1
        logger.log_status('Running travel model ...')
        run_transcad_macro(macroname, ui_db_file, loops)  

    def prepare_for_run(self, config, year):
        """before calling travel model macro, check if transcad program is running, if not, try to start trascad binary process"""

        set_project_ini_file(config, year)
        
        cmdline = config['transcad_binary']
        head, tail = os.path.split(cmdline)
        procname, ext = os.path.splitext(tail)  #tcw
        
        start_process = False
        try:
            win32pdhutil.GetPerformanceAttributes('Process','ID Process',procname)
            pids = win32pdhutil.FindPerformanceAttributesByName (procname)
        except:
            start_process = True
        else:
            if len(pids)==0:
                start_process = True

        if start_process:
            #transcad not started, try to start it            
            try:
                cmdline = win32api.GetShortPathName(cmdline)
                os.system('start /B "start TransCAD" ' + cmdline)  #start TransCAD in background
                #procHandles = win32process.CreateProcess(None, cmdline, None, None, 0, 0, None, None,
                                     #win32process.STARTUPINFO())
            except:
                logger.log_error( "Unable to start TransCAD in %s; it must be running to invoke travel model macro." % cmdline)
                sys.exit(1)

      #otherwise transcad is running, do nothing

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from optparse import OptionParser
    from opus_core.utils.file_utilities import get_resources_from_file
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

    logger.enable_memory_logging()
    RunSemcogTravelModel().run(resources, options.year)    
