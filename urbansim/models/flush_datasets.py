# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.model import Model

class FlushDatasets(Model):
    """Model for flushing given datasets into cache. This is especially useful, when we want 
    to flush dataset only in certain years, not every year, or not after each model 
    (which is done by the model system).
    """
    def run(self, datasets=[]):
        """
        Flush datasets given in the argument 'datasets' into cache.
        """
        for dataset in datasets:
            dataset.flush_dataset()
