from urbansim.models.scaling_agents_model import ScalingAgentsModel
from opus_core.session_configuration import SessionConfiguration
from opus_core.model import Model
import numpy as np
from opus_core.logger import logger
from numpy import ones, array, where, logical_and, around
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from urbansim.datasets.control_total_dataset import ControlTotalDataset

class SkimSwapper(Model):
    """Swap skims.
    """
    def run(self):
    
        dataset_pool = SessionConfiguration().get_dataset_pool()
        
        z_scen0 = dataset_pool.get_dataset('zones_scen0')
        
        tcd = z_scen0['tcd']
        tco = z_scen0['tco']
        vpd = z_scen0['vpd']
        vpo = z_scen0['vpo']
        
        zones = dataset_pool.get_dataset('zone')
        
        zones.modify_attribute('tcd', tcd)
        zones.modify_attribute('tco', tco)
        zones.modify_attribute('vpd', vpd)
        zones.modify_attribute('vpo', vpo)
        
        z_scen0.delete_one_attribute('tcd')
        z_scen0.delete_one_attribute('tco')
        z_scen0.delete_one_attribute('vpd')
        z_scen0.delete_one_attribute('vpo')
        
        
        