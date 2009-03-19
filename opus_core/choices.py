# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.model_component import ModelComponent

class Choices(ModelComponent):
    """ Class for computing choices. Serves as a parent class for user defined choices classes.     
    """
    def run(self, *args, **kwargs):
        pass

