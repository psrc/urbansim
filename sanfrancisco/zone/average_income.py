# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class average_income(Variable):
    """average income in a given zone"""

    _return_type="int32"
    
    def dependencies(self):
        return ["sanfrancisco.household.zone_id", 
                "_average_income=zone.aggregate(household.income, function=mean)"
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_average_income")

    def post_check(self,  values, dataset_pool=None):
        imin = dataset_pool.get_dataset("household").get_attribute("income").min()
        imax = dataset_pool.get_dataset("household").get_attribute("income").max()
        self.do_check("x >= %s and x <= %s" % (imin, imax), values)
