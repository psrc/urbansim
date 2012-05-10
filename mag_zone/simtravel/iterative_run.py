# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from travel_model.models.abstract_travel_model import AbstractTravelModel
from opus_core.session_configuration import SessionConfiguration
from opus_core.resources import Resources
from opus_core.logger import logger
import subprocess, sys, os, copy, shutil
from mag_zone.simtravel.run_openamos import RunOpenamos
from mag_zone.simtravel.run_malta import RunMalta

MAX_ITERATION = 1
class IterativeRun(AbstractTravelModel):
    """
    """

    def run(self, config, year):
        """
        iteratively run openamos and malta until files indicating convergence are set to True (1)
        """
        
        tm_config = config['travel_model_configuration']
        openamos_convergence_file = tm_config.get("openamos_convergence_file",
                                         os.path.join(
                                             os.path.split(tm_config["openamos_path"])[0], 
                                             'openamos_convergence.txt')
                                         )
        malta_convergence_file = tm_config.get("malta_convergence_file",
                                         os.path.join(
                                             os.path.split(tm_config["malta_path"])[0], 
                                             'malta_convergence.txt')
                                         )
        #tm_config['openamos_configuration'] = tm_config['openamos_configuration_first_iteration']
        #config['travel_model_configuration'] = tm_config

        openamosBeforeConfig = copy.deepcopy(tm_config['openamos_configuration'])
        openamosAfterConfig = copy.deepcopy(tm_config['openamos_configuration_after_iterations'])


        iteration = 0
        while (not (self._is_converged(openamos_convergence_file) and self._is_converged(malta_convergence_file)) ) and iteration <= MAX_ITERATION:
            #if iteration == 1:  # switch configuration file for openamos for second and later iterations, 
            #                    # only need to do it once

            # Run the models for building activity-travle skeletons
            tm_config['openamos_configuration'] = openamosBeforeConfig
            config['travel_model_configuration'] = tm_config
            setupCache = 1
            backupResults = 0
            RunOpenamos().run(config, year, iteration+1, setupCache, backupResults)

            RunMalta().run(config, year, iteration+1)


            # Run the models for post processing the outputs ... 
            tm_config['openamos_configuration'] = openamosAfterConfig
            config['travel_model_configuration'] = tm_config
            setupCache = 0
            backupResults = 1
            RunOpenamos().run(config, year, iteration+1, setupCache, backupResults)


            # Copy the link travel times file
            loc = os.path.split(tm_config["malta_path"])[0]
            fileLocLinkTimes = os.path.join(loc, "output_linkTrvTime.dat")
            projectLoc = tm_config.get("project_path")
            copyLinkTimesToLoc = os.path.join(projectLoc, "iteration_%d" %(iteration+1), "output_linkTrvTime.dat")
            shutil.copyfile(fileLocLinkTimes, copyLinkTimesToLoc)
        
            # Copy the travel distances file
            fileLocTrvDist = os.path.join(loc, "tmp_output_arrVeh.txt")
            copyTrvDistToLoc = os.path.join(projectLoc, "iteration_%d" %(iteration+1), "tmp_output_arrVeh.txt")
            shutil.copyfile(fileLocTrvDist, copyTrvDistToLoc)

            iteration += 1
            
    def _is_converged(self, convergence_file):
        with open(convergence_file) as f:
            return eval(f.readline().strip())
        
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
    IterativeRun().run(resources, options.year)    
