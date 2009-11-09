# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import resize, array

class nonhome_based_workers_category(Variable):
    """return if a household has DDD nonhome based worker"""

    def dependencies(self):
        return ["psrc.household.number_of_nonhome_based_workers"]

    def compute(self, dataset_pool):
        nhb_workers = self.get_dataset().get_attribute("number_of_nonhome_based_workers")
        results = resize(array([-1], dtype="int16"), nhb_workers.size)
        results[nhb_workers == 0] = 0
        results[nhb_workers == 1] = 1
        results[nhb_workers >= 2] = 2
        return results