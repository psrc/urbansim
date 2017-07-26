# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import logical_and, where, logical_not, array, concatenate
from opus_core.logger import logger
from opus_core.misc import unique
from opus_core.datasets.dataset import DatasetSubset
from psrc_parcel.models.development_project_proposal_sampling_model_with_minimum import DevelopmentProjectProposalSamplingModel

class DevelopmentProposalSamplingModelBySubarea(DevelopmentProjectProposalSamplingModel):

    def __init__(self, proposal_set, subarea_id_name, **kwargs):
        super(DevelopmentProposalSamplingModelBySubarea, self).__init__(proposal_set, **kwargs)
        self.subarea_id_name = subarea_id_name
     
    def run(self, **kwargs):
        """Runs the parent model for each subarea separately.
        """
        buildings = self.dataset_pool.get_dataset("building")
        buildings.compute_variables([
            "psrc_parcel.building.occupied_spaces",
            "psrc_parcel.building.total_spaces",
                                "occupied_units_for_jobs = psrc_parcel.building.number_of_non_home_based_jobs",
                                "units_for_jobs = psrc_parcel.building.total_non_home_based_job_space",
                                "occupied_residential_units = urbansim_parcel.building.number_of_households",
                                "urbansim_parcel.building.existing_units",
                                    ], dataset_pool=self.dataset_pool)
        buildings.compute_one_variable_with_unknown_package(variable_name="%s" % (self.subarea_id_name), dataset_pool=self.dataset_pool)
        # keep copy of the weights
        original_weight = self.weight.copy()
        self.all_demolished_buildings = array([], dtype='int32')
        
        regions = self.proposal_set.compute_one_variable_with_unknown_package(variable_name="%s" % (self.subarea_id_name), dataset_pool=self.dataset_pool)

        unique_regions = unique(regions)
        original_status = self.proposal_set.get_attribute("status_id").copy()
        self.proposal_set.add_primary_attribute(name='original_status_id', data=original_status)
        bldgs_regions = buildings.get_attribute(self.subarea_id_name)
        for area_index in range(unique_regions.size):
            self.area_id = unique_regions[area_index]            
            status = self.proposal_set.get_attribute("status_id")
            where_area = regions == self.area_id
            idx_area_in_proposal = where(where_area)[0]
            if idx_area_in_proposal.size <= 0:
                logger.log_status("No proposals for area %s" % self.area_id)
                continue
            bldgs_area_idx = where(bldgs_regions == self.area_id)[0]
            bldgs_subset = DatasetSubset(buildings, index=bldgs_area_idx)
            self.dataset_pool.replace_dataset('building', bldgs_subset)
            idx_out_area_not_active_not_refused = where(logical_and(logical_and(status != self.proposal_set.id_active, 
                                                                               status != self.proposal_set.id_refused),
                                                                    logical_not(where_area)))[0]
            status[idx_area_in_proposal] = self.proposal_set['original_status_id'][idx_area_in_proposal]
            status[idx_out_area_not_active_not_refused] = self.proposal_set.id_not_available
            self.proposal_set.modify_attribute(name="status_id", data=status)
            self.weight[:] = original_weight[:]
            
            logger.log_status("\nDPSM for area %s" % self.area_id)
            dummy, demolished_bldgs = DevelopmentProjectProposalSamplingModel.run(self, **kwargs)
                
            self.all_demolished_buildings = concatenate((self.all_demolished_buildings, demolished_bldgs))
            status = self.proposal_set.get_attribute("status_id")
            self.proposal_set.modify_attribute(name="original_status_id", data=status[idx_area_in_proposal], index=idx_area_in_proposal)
            where_not_active = where(status[idx_area_in_proposal] != self.proposal_set.id_active)[0]
            status[idx_area_in_proposal[where_not_active]] = self.proposal_set.id_refused
            self.proposal_set.modify_attribute(name="status_id", data=status)
                
        # set all proposals that were not set to 'active' to their original status
        idx = where(status != self.proposal_set.id_active)[0]
        self.proposal_set.set_values_of_one_attribute("status_id", original_status[idx], idx)
        self.dataset_pool.replace_dataset('building', buildings)
        return (self.proposal_set, self.all_demolished_buildings)
