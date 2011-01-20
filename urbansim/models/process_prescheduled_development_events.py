# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.model import Model
from opus_core.logger import logger
from urbansim.datasets.development_event_dataset import DevelopmentEventDataset

class ProcessPrescheduledDevelopmentEvents(Model):
    """Create a class object from any pre-scheduled development events.
    """
    model_name = "ProcessPrescheduledDevelopmentEvents"
    
    def run (self, storage, in_table="development_events",
               out_table="development_events"):

        
        if not storage.has_table(in_table):
            logger.log_status('No exogenous developments.')
            return
        
        development_events = DevelopmentEventDataset(
            in_storage=storage, 
            in_table_name=in_table, out_table_name=out_table)

        return development_events   