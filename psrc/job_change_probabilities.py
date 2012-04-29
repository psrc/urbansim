# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.upc.rate_based_probabilities import rate_based_probabilities

class job_change_probabilities(rate_based_probabilities):
    agent_set = 'person'
    rate_set = 'job_change_rate'
