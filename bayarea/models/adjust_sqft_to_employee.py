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

class AdjustSqFtToEmployee(Model):
    """
    Adjust a building's square feet to agree with that required by employees
    """
    model_name = "adjust_sqft_to_employee"

    def run(self, year=None, years_to_run=[]):
        if year not in years_to_run:
            return

        logger.log_status("Finding buildings with employees exceeding amount allowed by square feet...")
        dataset_pool = SessionConfiguration().get_dataset_pool()
        building = dataset_pool.get_dataset('building')
	establishment = dataset_pool.get_dataset('establishment')
	building_sqft_per_employee = dataset_pool.get_dataset('building_sqft_per_employee')
        employees = establishment.get_attribute('employees')
        building_type_ids = establishment.compute_variables('establishment.disaggregate(building.building_type_id)')
	building_sqft = building.get_attribute('building_sqft')
	sqft_required_per_employee = establishment.compute_variables('_sqft_required_per_employee=establishment.disaggregate(building.disaggregate(building_sqft_per_employee.building_sqft_per_employee))')
	#establishment.add_primary_attribute(name='building_type_id', data=building_type_ids)
	#establishment.add_primary_attribute(name='sqft_required_per_employee', data=sqft_required_per_employee)
        required_sqft_in_building = building.compute_variables('_required_sqft_in_building = building.aggregate(establishment.employees*_sqft_required_per_employee)')
	#sqft_required_total = employees*sqft_required_per_employee
        overassigned = building.compute_variables('_overassigned = _required_sqft_in_building > building.building_sqft')
        idx_overassigned = where(overassigned)[0]
        num_overassigned = len(idx_overassigned)
        logger.log_status("Found %d overassigned buildings" % num_overassigned)
        new_building_sqft = required_sqft_in_building[idx_overassigned]
        building.modify_attribute('building_sqft', new_building_sqft, idx_overassigned)
        overassigned=building.compute_variables('_overassigned=_required_sqft_in_building>building.building_sqft')
        idx_overassigned = where(overassigned)[0]
        num_overassigned = len(idx_overassigned)
        logger.log_status("Found %d overassigned buildings" % num_overassigned)
