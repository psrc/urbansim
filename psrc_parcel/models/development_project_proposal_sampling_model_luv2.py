# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import zeros, logical_and, where, logical_not, logical_or, arange
from opus_core.logger import logger
from psrc_parcel.models.development_project_proposal_sampling_model_with_minimum import DevelopmentProjectProposalSamplingModel
from opus_core.simulation_state import SimulationState

class DevelopmentProjectProposalSamplingModelLuv2(DevelopmentProjectProposalSamplingModel):
    """ In addition to its parent considers parcels attributes that can shut off development depending on the current growth. 
    """
    
    #def run(self, n=500, 
            #realestate_dataset_name = 'building',
            #current_year=None, **kwargs):
        #if current_year is None:
            #year = SimulationState().get_current_time()
        #else:
            #year = current_year
        #next_years = arange(year+1, year+5)
        #next_luv_year = next_years[where(next_years % 5 == 0)][0]
        #self.cap_res_variable = "development_project_proposal.disaggregate(city.aggregate(urbansim_parcel.parcel.number_of_households), intermediates=[parcel]) < 1.01*building.disaggregate(psrc_parcel.city.household_control_total_2015, intermediates=[parcel])"
        #return DevelopmentProjectProposalSamplingModel.run(self, n=n, realestate_dataset_name=realestate_dataset_name, current_year=year, **kwargs)
        
    def run(self, *args, **kwargs):
        self.block_capped_proposals()
        return DevelopmentProjectProposalSamplingModel.run(self, *args, **kwargs)

    def block_capped_proposals(self):
        """ Set weights to zero for proposals located on parcels where the cap development models
        flagged the corresponding target as achieved. Planned proposals are not affected,
        since they are accepted with force_accepting=True.
        """
        self.proposal_set.compute_variables(['is_res = development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.is_residential) > 0',
                                             'is_nonres = development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.is_residential==0) > 0',
                                             'residential_target_reached = development_project_proposal.disaggregate(parcel.residential_target_achieved)',
                                             'nonresidential_target_reached = development_project_proposal.disaggregate(parcel.nonresidential_target_achieved)'
                                             ],
                                                    dataset_pool=self.dataset_pool)
        remove_ind = where(logical_and(self.weight > 0,
                                       logical_or(logical_and(self.proposal_set['is_res'], self.proposal_set['residential_target_reached']),
                                                  logical_and(self.proposal_set['is_nonres'], self.proposal_set['nonresidential_target_reached']))))[0]
        self.weight[remove_ind] = 0.0
        logger.log_status("Blocked %s proposals due to sufficient growth." % remove_ind.size)

