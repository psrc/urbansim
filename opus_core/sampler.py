# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.model_component import ModelComponent

class Sampler(ModelComponent):
    def run(self):
        """required for children class"""
        raise NotImplementedError, "Method 'run' is not implemented for this sampler."
            