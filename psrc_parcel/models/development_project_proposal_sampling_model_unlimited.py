# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from psrc_parcel.models.development_project_proposal_sampling_model_with_minimum import DevelopmentProjectProposalSamplingModel as DevelopmentProjectProposalSamplingModelWithMinimum

class DevelopmentProjectProposalSamplingModel(DevelopmentProjectProposalSamplingModelWithMinimum):
    """
    Does not consider any vacancy rates. It builts all proposals possible.
    """

    def _is_target_reached(self, column_value=()):
        return False