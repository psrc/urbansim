from urbansim.models.scaling_agents_model import ScalingAgentsModel
from opus_core.session_configuration import SessionConfiguration
from opus_core.model import Model
import numpy as np

class ScalingHouseholdsModel(Model):
    """Places unplaced households.
    """
    def run(self):
    
        dataset_pool = SessionConfiguration().get_dataset_pool()
        
        households = dataset_pool.get_dataset('household')
        
        buildings = dataset_pool.get_dataset('building')
        
        unplaced = households.compute_variables("household.building_id==-1")
        index_unplaced = np.where(unplaced==1)[0]
        
        model = ScalingAgentsModel()
        
        model.run(buildings, households, index_unplaced)