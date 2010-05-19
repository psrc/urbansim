# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class number_of_businesses_of_activity_SSS(Variable):
    """Number of businesses of activity SSS"""

    _return_type="int32"
    def __init__(self, activity):
        self.activity = activity.lower()
        Variable.__init__(self)
        
    def dependencies(self):
        return [
                "is_of_activity_%s = sanfrancisco.business.is_activity_%s" % (self.activity, self.activity),
                "_number_of_businesses_of_activity_%s = building.aggregate(business.is_of_activity_%s)" % (self.activity, self.activity)
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_number_of_businesses_of_activity_%s" % self.activity)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("building").size()
        self.do_check("x >= 0 and x <= " + str(size), values)
