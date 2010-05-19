# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class employment_of_activity_SSS(Variable):
    """Number of employment of activity SSS"""

    _return_type="int32"
    def __init__(self, activity_name):
        self.activity_name = activity_name.lower()
        Variable.__init__(self)
        
    def dependencies(self):
        return [
                "_employment_of_acitivity_%s = (sanfrancisco.business.is_activity_%s * sanfrancisco.business.employment).astype(int32)" % (self.activity_name, self.activity_name),
                ]

    def compute(self,  dataset_pool):
        business = dataset_pool.get_dataset("business")
        return self.get_dataset().sum_dataset_over_ids(business, attribute_name="_employment_of_activity_%s" % self.activity_name)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("building").size()
        self.do_check("x >= 0 and x <= " + str(size), values)
