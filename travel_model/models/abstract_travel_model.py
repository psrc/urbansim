# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os
from opus_core.model import Model
from opus_core.logger import logger

class AbstractTravelModel(Model):
    """Basic functionality used by all of the transcad models.
    Must be subclassed before use.
    """
    
    def get_travel_model_data_dir(self, config, *args, **kwargs):
        """Returns the full path to the directory for travel model-urbansim data exchange,
        """
        if os.environ.has_key("TRAVELMODELDATAROOT"):
            drive = os.environ['TRAVELMODELDATAROOT']
        else:
            logger.log_warning("TRAVELMODELDATAROOT is not set; will try to use the current drive")
            drive = '\\'
        if config['travel_model_configuration'].has_key('directory'):
            return os.path.join(drive, config['travel_model_configuration']['directory'])
        else:
            return drive
            
    def run_travel_model_macro(self):
        raise NotImplementedError, "subclass responsibility"
        
    
    def prepare_for_run(self, config, year):
        raise NotImplementedError, "subclass responsibility"