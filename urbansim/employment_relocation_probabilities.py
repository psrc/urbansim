# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.relocation_probabilities import relocation_probabilities

class employment_relocation_probabilities(relocation_probabilities):
    agent_set = 'job'
    rate_set = 'annual_job_relocation_rate'
    