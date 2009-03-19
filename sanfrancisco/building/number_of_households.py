# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class number_of_households(Variable):
    """Number of households in a given building"""

    _return_type="int32"
    
    def dependencies(self):
        return ["_number_of_households=building.number_of_agents(household)"]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_number_of_households")

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("household").size()
        self.do_check("x >= 0 and x <= " + str(size), values)
