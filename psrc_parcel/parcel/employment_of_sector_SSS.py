#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from opus_core.variable import Variable
from variable_functions import my_attribute_label

class employment_of_sector_SSS(Variable):
    """employment of_sector_SSS in a given parcel"""

    _return_type="Int32"
    def __init__(self, sector):
        self.sector = sector.lower()
        Variable.__init__(self)
        
    def dependencies(self):
        return [
                "psrc_parcel.building.employment_of_sector_" + self.sector, 
                "psrc_parcel.building.parcel_id", ]

    def compute(self,  dataset_pool):
        building = dataset_pool.get_dataset("building")
        return self.get_dataset().sum_dataset_over_ids(building, "employment_of_sector_"+self.sector)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("building").get_attribute("employment_of_sector_" + self.sector).sum()
        self.do_check("x >= 0 and x <= " + str(size), values)
