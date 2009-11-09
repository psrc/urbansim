# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros, float32

class time(Variable):
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        choice_names = ds.get_attribute_of_dataset("names", 2)
        result = zeros(ds.size()[0], dtype=float32)
        for ichoice in range(ds.get_reduced_m()):
            result[:, ichoice] = ds.get_attribute_of_dataset(choice_names[ichoice] + "_time")
        return result