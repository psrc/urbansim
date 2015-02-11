# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import where, in1d, ones
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.datasets.dataset_pool import DatasetPool
from urbansim_parcel.models.building_construction_model import BuildingConstructionModel


class BuildingConstructionModelMPDs(BuildingConstructionModel):
    """ Construction model that allows to load MPDs from base year and build the ones for the particular simulation year.
    No developer model necessary.
    """
    def prepare_for_run(self, building_dataset):
        start_year = SimulationState().get_start_time()
        storage = AttributeCache().get_flt_storage_for_year(start_year)
        dataset_pool = DatasetPool(package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'], storage=storage) # dataset pool from base year
        proposal_set = dataset_pool.get_dataset('development_project_proposal')
        year = SimulationState().get_current_time()
        is_active = where(proposal_set['start_year']==year)[0]
        proposal_set.modify_attribute(name='status_id', data=proposal_set.id_active, index=is_active)
        proposal_component_set = dataset_pool.get_dataset('development_project_proposal_component')
        is_active_comp = in1d(proposal_component_set['proposal_id'], proposal_set['proposal_id'][is_active])
        proposal_component_set.remove_elements(where(is_active_comp==0)[0])
        to_be_demolished = building_dataset['building_id'][in1d(building_dataset['parcel_id'], proposal_set['parcel_id'][is_active])]
        return (proposal_set, proposal_component_set, to_be_demolished)
    