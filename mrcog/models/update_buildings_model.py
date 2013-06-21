# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.model import Model
from opus_core.logger import logger
from opus_core.session_configuration import SessionConfiguration
from opus_core.simulation_state import SimulationState
import numpy as np

from IPython import embed

class UpdateBuildingsModel(Model):
    """Performs needed building update operations for buildings generated by DPLCM.
    """
    model_name = "Update Buildings Model"

    def run(self, urbancanvas=False):
        """Performs needed building update operations for buildings generated by DPLCM.
        """
        current_year = SimulationState().get_current_time()
        dataset_pool = SessionConfiguration().get_dataset_pool()
        
        building_set = dataset_pool.get_dataset('building')
        
        bld_index = np.where(building_set['year_built']==-1)[0]
        building_set.modify_attribute('year_built', np.array(bld_index.size*[current_year]), bld_index)
        
        if urbancanvas:
            import pandas as pd
            b_dict = {}
            attrib_names = building_set.get_attribute_names()
            for attrib in attrib_names:
                b_dict[attrib] = building_set[attrib]
            building_df = pd.DataFrame(b_dict)
            embed()
            ##need to load urbansim buildings (which represent some base-year synthesis) back to the db.
            ##select nextval('developmentprojects_seq')