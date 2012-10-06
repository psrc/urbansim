# Opus/UrbanSim urban simulation software.
# Copyright (C) 2012 University of California, Berkeley
# See opus_core/LICENSE

from opus_core.model import Model
from opus_core.logger import logger
from opus_core.session_configuration import SessionConfiguration
import numpy
from numpy import ones, array, where, logical_and, logical_or, around
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from urbansim.datasets.control_total_dataset import ControlTotalDataset

class AdjustDUToHH(Model):
    """
    Adjust a building's dwelling units to agree with assigned households
    """
    model_name = "adjust_du_to_hh"

    def run(self, year=None, years_to_run=[]):
        if year not in years_to_run:
            return

        logger.log_status("Finding buildings with over-assigned households...")
        dataset_pool = SessionConfiguration().get_dataset_pool()
        building = dataset_pool.get_dataset('building')
        assigned_households = building.compute_variables('_assigned_hh = building.number_of_agents(household)')
        building_type_ids = building.get_attribute('building_type_id')
        overassigned = building.compute_variables('_overassigned = _assigned_hh > building.residential_units')
        idx_overassigned = where(overassigned)[0]
        num_overassigned = len(idx_overassigned)
        logger.log_status("Found %d overassigned buildings" % num_overassigned)
        new_res_units = building.get_attribute('_assigned_hh')[idx_overassigned]
        building.modify_attribute('residential_units', new_res_units, idx_overassigned)

        # make all over-assigned buildings of type 3
        idx_sf_overassigned = where(logical_and(overassigned, logical_or(building_type_ids == 1,
                                                                         building_type_ids == 2)))[0]
        new_building_ids = ones(idx_sf_overassigned.size, dtype="i4")*3
        building.modify_attribute('building_type_id', new_building_ids, idx_sf_overassigned)

        # recalculate overassignment to see how we did
        overassigned = building.compute_variables('_overassigned = _assigned_hh > building.residential_units')
        idx_overassigned = where(overassigned)[0]
        num_overassigned = len(idx_overassigned)
        logger.log_status("%d overassigned remain" % num_overassigned)
