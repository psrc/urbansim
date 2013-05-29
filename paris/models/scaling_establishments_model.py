from urbansim.models.scaling_agents_model import ScalingAgentsModel
from opus_core.session_configuration import SessionConfiguration
from opus_core.model import Model
import numpy as np

class ScalingEstablishmentsModel(Model):
    """Places unplaced households.
    """
    def run(self):
    
        dataset_pool = SessionConfiguration().get_dataset_pool()
        
        establishments = dataset_pool.get_dataset('establishment')
        
        buildings = dataset_pool.get_dataset('building')
        
        unplaced = establishments.compute_variables("establishment.building_id==-1")
        index_unplaced = np.where(unplaced==1)[0]
        
        model = ScalingAgentsModel()
        
        model.run(buildings, establishments, index_unplaced)