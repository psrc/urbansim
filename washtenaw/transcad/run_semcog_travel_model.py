# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.resources import Resources
from numpy import array, float32, ones
import os, sys, time
from opus_core.logger import logger
from travel_model.models.run_travel_model import RunTravelModel
from washtenaw.travel_model.run_transcad_macro import run_transcad_macro
import win32pdhutil, win32api, win32process
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from washtenaw.transcad.set_project_ini_file import set_project_ini_file, get_project_year_dir

class RunSemcogTravelModel(RunTravelModel):
    """Run the travel model.
    """

    def run(self, config, year, *args, **kwargs):
        """Runs the travel model, using appropriate info from config. 
        """
        tm_config = config["travel_model_configuration"]
        self.prepare_for_run(tm_config, year)
        
        project_year_dir = get_project_year_dir(tm_config, year)
#        year_dir = tm_config[year]  #'CoreEA0511202006\\urbansim\\2001'
#        dir_part1,dir_part2 = os.path.split(year_dir)
#        while dir_part1:
#            dir_part1, dir_part2 = os.path.split(dir_part1)
#        project_year_dir = os.path.join(tm_data_dir, dir_part2)   #C:/SEMCOG_baseline/CoreEA0511202006
        
        logger.log_status('Start travel model from directory %s for year %d' % (project_year_dir, year))
        #for macroname, ui_db_file in tm_config['macro']['run_semcog_travel_model'].iteritems():
            #pass 
        macroname, ui_db_file = tm_config['macro']['run_semcog_travel_model'], tm_config['ui_file']

        loops = 1
        logger.log_status('Running travel model ...')
        tcwcmd = win32api.GetShortPathName(tm_config['transcad_binary'])

        os.system('start /B "start TransCAD" %s' % tcwcmd)  #start TransCAD in background
        time.sleep(1)
        #os.system("%s -a %s -ai '%s'" % (tcwcmd, ui_db_file, macroname))
        run_transcad_macro(macroname, ui_db_file, loops)
        
        try:
            pass
            ##win32process.TerminateProcess(self.hProcess, 0)
        except:
            logger.log_warning("The code has problem to terminate the TransCAD it started.")

    def prepare_for_run(self, config, year, check_tcw_process=False):
        """before calling travel model macro, check if transcad GUI is running, 
        if not, try to start transcad binary process"""
        ## TODO: TransCAD COM server is very picky about tcw.exe process in memory
        ## as of April 2007, a tcw process started by python won't work
        ## so manually start TransCAD program is needed before running this script
        
        set_project_ini_file(config, year)
        if not check_tcw_process:
            return
        
        cmdline = config['transcad_binary']
        head, tail = os.path.split(cmdline)
        procname, ext = os.path.splitext(tail)  #tcw
        
        kill_process = False
        start_program = False
        tc_program_classname = "tcFrame"  #ClassName for TransCAD program
        try:
            hwnd=win32gui.FindWindow(tc_program_classname, None)
        except:
            start_program = True  # No Transcand Window found, we'll need to start TransCAD program
        else:
            try:
                #first check if tcw process is in memory
                win32pdhutil.GetPerformanceAttributes('Process','ID Process',procname)
                pids=win32pdhutil.FindPerformanceAttributesByName(procname)
                for pid in pids:
                    win32process.TerminateProcess(pid)
                start_program = True
            except:
                raise RuntimeError, "Unable to kill TransCAD process in memory"
            
        ##transcad not started, try to start it
        if start_program:
            try:
                pass
                cmdline = win32api.GetShortPathName(cmdline)
                cmdline = cmdline + " -q"
                os.system('start /B "start TransCAD" ' + cmdline)  #start TransCAD in background
                time.sleep(9)
                #procHandles = win32process.CreateProcess(None, cmdline, None, None, 0, 0, None, None,
                                     #win32process.STARTUPINFO())
                #self.hProcess, hThread, PId, TId = procHandles
            except:
                logger.log_error( "Unable to start TransCAD in %s; it must be running to invoke travel model macro." % cmdline)
                sys.exit(1)

      #otherwise transcad is running, do nothing

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

    logger.enable_memory_logging()
    RunSemcogTravelModel().run(resources, options.year)    
