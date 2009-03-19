# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class has_DDD_units(Variable):
    """Boolean indicating whether the parcel has DDD residential units"""

    def __init__(self, number):
        Variable.__init__(self)
        self.tnumber = number

    def dependencies(self):
        return ["_has_%s_units = parcel.residential_units == %s" % (self.tnumber, self.tnumber)]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute( "_has_%s_units" % self.tnumber )

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x == True or x == False", values)
