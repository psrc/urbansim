# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.rate_based_probabilities import rate_based_probabilities

class business_relocation_probabilities(rate_based_probabilities):
    agent_set = 'establishment'
    rate_set = 'business_relocation_rate'
