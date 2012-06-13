# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import maximum

class number_of_hh_of_type_DDD(Variable):
    """total number of households of type DDD"""

    _return_type="int32"
    def __init__(self, type_id):
        self.type_id = type_id
        Variable.__init__(self)
        
    def dependencies(self):
        return [
                "_hhs{0}=(building.aggregate(household.lenght_of_tenure<2)>0)*(building.aggregate(numpy.logical_and(household.hh_type=={0}, household.lenght_of_tenure<2))) + (building.aggregate(household.lenght_of_tenure<2)<1)".format(self.type_id)
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset()['_hhs{0}'.format(self.type_id)]

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x >= 0")

