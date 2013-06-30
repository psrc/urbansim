# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.model import Model
from opus_core.logger import logger
from opus_core.session_configuration import SessionConfiguration
import numpy as np

class Updater(Model):
    """Performs any data consistency operations.
    """
    model_name = "Updater"

    def run(self):
        """Keeps household building type id attribute consistent with residential_building_type_id. 
        """
        dataset_pool = SessionConfiguration().get_dataset_pool()

        household_set = dataset_pool.get_dataset('household')
        
        household_set.delete_one_attribute('county')
        
        county = household_set.compute_variables('_county = household.disaggregate(parcel.county_id, intermediates=[building])')
        
        household_set.add_primary_attribute(name='county', data=county)