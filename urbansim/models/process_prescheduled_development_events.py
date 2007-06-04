#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.model import Model
from opus_core.logger import logger
from urbansim.datasets.development_event_dataset import DevelopmentEventDataset

class ProcessPrescheduledDevelopmentEvents(Model):
    """Process any pre-scheduled development events.
       Currently, these can only be from exogenous development events.
    """
    model_name = "ProcessPrescheduledDevelopmentEvents"
    
    def run (self, storage, in_table="development_events_exogenous",
               out_table="development_events_exogenous"):

        
        if not storage.has_table(in_table):
            logger.log_status('No exogenous developments.')
            return
        
        development_events = DevelopmentEventDataset(
            in_storage=storage, 
            in_table_name=in_table, out_table_name=out_table)

        return development_events   