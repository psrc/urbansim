# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from travel_model.models.abstract_travel_model import AbstractTravelModel
from opus_core.session_configuration import SessionConfiguration
from opus_core.resources import Resources
from opus_core.logger import logger
import subprocess, sys, os

MAX_ITERATION = 10
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
        tm_config['openamos_configuration'] = tm_config['openamos_configuration_first_iteration']
        config['travel_model_configuration'] = tm_config
        iteration = 0
        while (not (self._is_converged(openamos_convergence_file) and self._is_converged(malta_convergence_file)) ) and iteration <= MAX_ITERATION:
            if iteration == 1:  # switch configuration file for openamos for second and later iterations, 
                                # only need to do it once
                tm_config['openamos_configuration'] = tm_config['openamos_configuration_other_iterations']
                config['travel_model_configuration'] = tm_config
            RunOpenamos().run(config, year)
            RunMalta().run(config, year)
            
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
