from urbansim.models.scaling_agents_model import ScalingAgentsModel
from opus_core.session_configuration import SessionConfiguration
from opus_core.model import Model
import numpy as np
from opus_core.logger import logger
from numpy import ones, array, where, logical_and, around
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from urbansim.datasets.control_total_dataset import ControlTotalDataset

class EmploymentDiagnoser(Model):
    """Diagnose employment issues.
    """
    def run(self):
    
        dataset_pool = SessionConfiguration().get_dataset_pool()
        
        estabs = dataset_pool.get_dataset('establishment')
        
        extant = estabs.compute_variables("establishment.disappeared==0")
        
        index_extant = np.where(extant==1)[0]
        
        logger.log_status("num establishments: %s" %(index_extant.size) )
  
        unplaced = estabs.compute_variables("(establishment.building_id==-1)*(establishment.disappeared==0)")
        index_unplaced = np.where(unplaced==1)[0]
        
        logger.log_status("num unplaced establishments: %s" %(index_unplaced.size) )
        
        employment = estabs.get_attribute('employment')
        
        logger.log_status("avg employees in all establishments: %s" %(np.average(employment[extant])) )
        
        logger.log_status("avg employees in unplaced establishments: %s" %(np.average(employment[index_unplaced])) )
        
        
        