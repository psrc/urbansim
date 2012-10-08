# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.model import Model
from opus_core.logger import logger
from opus_core.session_configuration import SessionConfiguration
import numpy
from numpy import ones, array

class UpdateHhBuildingTypeId(Model):
    """Keeps household building type id attribute consistent with residential_building_type_id.
    """
    model_name = "BuildingTypeUpdater"

    def run(self):
        """Keeps household building type id attribute consistent with residential_building_type_id. 
        """
        dataset_pool = SessionConfiguration().get_dataset_pool()

        household_set = dataset_pool.get_dataset('household')

        household_res_type = household_set.get_attribute('residential_building_type_id')

        #index_update_building_type = where(household_res_type>0)[0]

        #household_set.modify_attribute('building_type_id', household_res_type[index_update_building_type], index_update_building_type)

        household_set.modify_attribute('building_type_id', household_res_type)