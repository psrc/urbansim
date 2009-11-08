#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

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