# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

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
        if "TRAVELMODELDATAROOT" in os.environ:
            drive = os.environ['TRAVELMODELDATAROOT']
        else:
            logger.log_warning("TRAVELMODELDATAROOT is not set; will try to use the current drive")
            drive = '\\'
        if 'directory' in config['travel_model_configuration']:
            return os.path.join(drive, config['travel_model_configuration']['directory'])
        else:
            return drive
            
    def run_travel_model_macro(self):
        raise NotImplementedError("subclass responsibility")
        
    
    def prepare_for_run(self, config, year):
        raise NotImplementedError("subclass responsibility")