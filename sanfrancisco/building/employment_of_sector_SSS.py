# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class employment_of_sector_SSS(Variable):
    """Number of businesses of_sector_SSS in a given parcel"""

    _return_type="int32"
    def __init__(self, sector):
        self.sector = sector.lower()
        Variable.__init__(self)
        
    def dependencies(self):
        return [
                "_employment_of_sector_%s = ( sanfrancisco.business.is_of_sector_%s * sanfrancisco.business.employment ).astype(int32)" % (self.sector, self.sector),
                "_employment_of_sector_%s = building.aggregate(business._employment_of_sector_%s)" % (self.sector, self.sector)
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_employment_of_sector_%s" % self.sector)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("building").size()
        self.do_check("x >= 0 and x <= " + str(size), values)
