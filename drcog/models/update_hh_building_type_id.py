# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.model import Model
from opus_core.logger import logger
from opus_core.session_configuration import SessionConfiguration
import numpy
from numpy import ones, array, where

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

        index_sfdetached = where(household_res_type==1)[0]

        index_townhome = where(household_res_type==2)[0]

        index_apartment = where(household_res_type==3)[0]

        index_condo = where(household_res_type==4)[0]

        household_set.modify_attribute('building_type_id', array(index_sfdetached.size*[20]), index_sfdetached)

        household_set.modify_attribute('building_type_id', array(index_townhome.size*[24]), index_townhome)

        household_set.modify_attribute('building_type_id', array(index_apartment.size*[2]), index_apartment)

        household_set.modify_attribute('building_type_id', array(index_condo.size*[3]), index_condo)