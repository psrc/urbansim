# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.relocation_probabilities import relocation_probabilities

class job_change_probabilities(relocation_probabilities):
    agent_set = 'person'
    rate_set = 'job_change_rate'
