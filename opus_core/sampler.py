# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.model_component import ModelComponent
from opus_core.datasets.interaction_dataset import InteractionDataset

class Sampler(ModelComponent):
    
    def run(self):
        """required for children class"""
        raise NotImplementedError, "Method 'run' is not implemented for this sampler."
    
    def create_interaction_dataset(self, dataset1, dataset2, index1=None, index2=None):
        return InteractionDataset(dataset1=dataset1, dataset2=dataset2,
                                  index1=index1, index2=index2)
            