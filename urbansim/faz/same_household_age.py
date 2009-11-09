# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import ones
from urbansim.functions import attribute_label

class same_household_age(Variable):
    """This variable is not meant to return a useful value but to (re-)create the same_age_table of the faz dataset
    whenever one of the dependent variables changes."""
    def dependencies(self):
        return [attribute_label("household", "age_of_head"), attribute_label("household", "faz_id")]

    def compute(self, dataset_pool):
        self.get_dataset().create_same_age_table(dataset_pool.get_dataset('household'))
        return ones((self.get_dataset().size(),))
