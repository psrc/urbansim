# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.model import Model
from opus_core.logger import logger
from opus_core.session_configuration import SessionConfiguration
import numpy
from numpy import ones, array, where, logical_and, around
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from urbansim.datasets.control_total_dataset import ControlTotalDataset

class TestModel(Model):
    """Zonal Gov-Ed Jobs Model.
    """
    model_name = "gov_ed_jobs_model"

    def run(self):
        """Runs the test model. 
        """

        dataset_pool = SessionConfiguration().get_dataset_pool()

        zone_set = dataset_pool.get_dataset('zone')

        zone_sqft_per_job = zone_set.compute_variables('_sqft_per_employee = safe_array_divide(zone.aggregate(building.non_residential_sqft,intermediates=[parcel]),zone.aggregate(establishment.employees,intermediates=[building,parcel]))')
        
