# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import zeros, logical_and, where, logical_not, logical_or
from opus_core.logger import logger
from psrc_parcel.models.development_project_proposal_sampling_model_with_minimum import DevelopmentProjectProposalSamplingModel

class DevelopmentProjectProposalSamplingModelLuv2(DevelopmentProjectProposalSamplingModel):
    """ In addition to its parent considers parcels attributes that can shut off development depending on the current growth. 
    """
        
    def consider_proposals(self, proposal_indexes, force_accepting=False):
        if proposal_indexes.size == 0:
            return
        is_proposal_rejected = zeros(proposal_indexes.size, dtype="bool")
        sites = self.proposal_set["parcel_id"][proposal_indexes]
        self.proposal_set.compute_variables(['is_res = development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.is_residential) > 0',
                                             'is_nonres = development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.is_residential==0) > 0',
                                             'residential_target_reached = development_project_proposal.disaggregate(parcel.residential_target_achieved)',
                                             'nonresidential_target_reached = development_project_proposal.disaggregate(parcel.nonresidential_target_achieved)'
                                             ],
                                                    dataset_pool=self.dataset_pool)
        remove_ind = logical_or(logical_and(self.proposal_set['is_res'], self.proposal_set['residential_target_reached']),
                                logical_and(self.proposal_set['is_nonres'], self.proposal_set['nonresidential_target_reached']))
        is_proposal_rejected = logical_or(is_proposal_rejected, remove_ind[proposal_indexes])
        logger.log_status("Blocked %s proposals due to sufficient growth." % remove_ind[proposal_indexes].sum())
        for i, proposal_index in enumerate(proposal_indexes):
            if not is_proposal_rejected[i] and ((self.weight[proposal_index] > 0) or force_accepting):
                accepted = self.consider_proposal(proposal_index, force_accepting=force_accepting)
                if accepted:
                    is_proposal_rejected[ sites == sites[i]] = True
                    
