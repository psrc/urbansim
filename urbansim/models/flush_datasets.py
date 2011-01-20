# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

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
