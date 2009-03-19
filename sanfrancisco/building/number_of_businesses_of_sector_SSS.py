# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class number_of_businesses_of_sector_SSS(Variable):
    """Number of businesses of_sector_SSS in a given parcel"""

    _return_type="int32"
    def __init__(self, sector):
        self.sector = sector.lower()
        Variable.__init__(self)
        
    def dependencies(self):
        return [
                "is_of_sector_%s = sanfrancisco.business.is_of_sector_%s" % (self.sector, self.sector),
                "_number_of_businesses_of_sector_%s = building.aggregate(business.is_of_sector_%s)" % (self.sector, self.sector)
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_number_of_businesses_of_sector_%s" % self.sector)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("building").size()
        self.do_check("x >= 0 and x <= " + str(size), values)
