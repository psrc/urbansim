# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.relocation_probabilities import relocation_probabilities

class business_relocation_probabilities(relocation_probabilities):
    agent_set = 'business'
    rate_set = 'business_relocation_rate'
