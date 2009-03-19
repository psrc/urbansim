# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class persons(Variable):
    """number of persons in a given household"""

    _return_type="int32"
    
    def dependencies(self):
        return ["_persons=household.number_of_agents(person)"
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_persons")

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("person").size()
        self.do_check("x >= 0 and x <= " + str(size), values)
