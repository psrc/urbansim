# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.model_component import ModelComponent

class Utilities(ModelComponent):
    """ Class for computing utilities. Serves as a parent class for user defined utilities classes.     
    """
    def run(self, *args, **kwargs):
        pass

    def get_dependent_datasets(self):
        return [] 
