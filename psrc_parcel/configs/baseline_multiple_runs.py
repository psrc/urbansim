# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from .baseline import Baseline

class BaselineMultipleRuns(Baseline):
    
    multiple_runs = True
    
    def __init__(self):
        config = Baseline()
        if self.multiple_runs:
            config.sample_inputs()
        config['years'] = (2001, 2005)
        config['number_of_runs'] = 50
        config['seed'] = 1
        config['description'] = 'baseline multiple runs'     
        self.merge(config)

    
if __name__ == "__main__":
    config = BaselineMultipleRuns()
