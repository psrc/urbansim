# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.agent_relocation_model import AgentRelocationModel
from opus_core.logger import logger
from numpy import zeros

class MarriageEligibilityModel(AgentRelocationModel):
    """
    """
    model_name = "Marriage Eligibility Model"

    def run(self, person_set, household_set, resources=None):
        index = AgentRelocationModel.run(self, person_set, resources=resources)

        logger.log_status("%s persons are in the marriage market." % (index.size) )

        person_ds_name, person_id_name = person_set.get_dataset_name(), person_set.get_id_name()[0]
        hh_ds_name, hh_id_name = person_set.get_dataset_name(), household_set.get_id_name()[0]

        #Flag the pool of individuals that are eligible to get married
        person_set.add_attribute(name='marriage_eligible', data=zeros(person_set.size(), dtype='b'))
        person_set['marriage_eligible'][index] = True