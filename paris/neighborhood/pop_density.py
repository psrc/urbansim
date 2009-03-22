# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import where, exp

class pop_density(Variable):
    """Returns a population in 1000's per square kilometer"""

    dept = "dept"

    def dependencies(self):
        return ["neighborhood.lpoprp99","neighborhood.areakm2"]

    def compute(self, dataset_pool):
        lpop = self.get_dataset().get_attribute("lpoprp99")
        areakm2 = self.get_dataset().get_attribute("areakm2")
        pop = exp(lpop)
        pop1k = pop/1000
        density = pop1k/areakm2
        return density


