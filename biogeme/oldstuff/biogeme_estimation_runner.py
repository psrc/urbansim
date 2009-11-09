# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

class BiogemeEstimationRunner(object):
    """Runs a biogeme estimation as a separate process"""
    
    def __init__(self, config):
        self.config = config
    
    def run(self):
        """Issues the system call to run the biogeme process and returns 
        success or failure.  Output will be piped to the terminal."""
        args = [self.config.path_to_biogeme, self.config.model_name] + self.config.data_files
        os.spawnv(os.P_WAIT, self.config.path_to_biogeme, args)

class BiogemeConfiguration(object):
    """Holds configuration info for a biogeme run"""
    
    def __init__(self, path_to_biogeme, model_name, path_to_data, data_files, output_directory=None):
        """Initialize the configuration object with arguments corresponding to
        the command line arguments for a biogeme invocation.
        path_to_biogeme: absolute path to the biogeme executable
        model_name: name of the model
        path_to_data: absolute path of the directory containing the biogeme input
            files.  Must contain a model specification file model_name.mod, as
            well as the files listed in data_files
        data_files: a list of one or more data file names relative to path_to_data
        output_directory: optionally, a directory to place biogeme's output
        See http://roso.epfl.ch/biogeme for details on biogeme invocation."""
        self.path_to_biogeme= path_to_biogeme
        self.path_to_data = path_to_data
        self.model_name = os.path.join(path_to_data, model_name)
        self.data_files = []
        for file in data_files:
            self.data_files.append(os.path.join(path_to_data, file))
        self.output_directory = output_directory
    