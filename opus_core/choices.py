# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.model_component import ModelComponent

class Choices(ModelComponent):
    """ Class for computing choices. Serves as a parent class for user defined choices classes.     
    """
    def run(self, *args, **kwargs):
        pass

