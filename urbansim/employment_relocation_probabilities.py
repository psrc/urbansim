# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.relocation_probabilities import relocation_probabilities

class employment_relocation_probabilities(relocation_probabilities):
    agent_set = 'job'
    rate_set = 'job_relocation_rate'
    