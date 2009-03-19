# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.relocation_probabilities import relocation_probabilities

class household_relocation_probabilities(relocation_probabilities):
    agent_set = 'household'
    rate_set = 'household_relocation_rate'
