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

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class residential_units(Variable):
    """residential units in a given parcel"""

    _return_type="int32"
    
    def dependencies(self):
        return ["_residential_units = parcel.aggregate(building.residential_units)"
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_residential_units")

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("building").get_attribute("residential_units").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)
