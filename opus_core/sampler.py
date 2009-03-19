# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.model_component import ModelComponent

class Sampler(ModelComponent):
    def run(self):
        """required for children class"""
        raise NotImplementedError, "Method 'run' is not implemented for this sampler."
            