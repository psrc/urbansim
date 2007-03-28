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
from variable_functions import my_attribute_label

class number_of_households_with_DDD_workers(Variable):
    """Number of households with DDD workers in a given parcel"""

    _return_type="int32"
    def __init__(self, nworkers):
        self.variable = "number_of_households_with_%s_workers" % nworkers
        Variable.__init__(self)
        
    def dependencies(self):
        return ["sanfrancisco.building.parcel_id", 
                "sanfrancisco.building.%s" % self.variable, 
                my_attribute_label("parcel_id")]

    def compute(self,  dataset_pool):
        buildings = dataset_pool.get_dataset("building")
        return self.get_dataset().sum_dataset_over_ids(buildings, self.variable)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("building").get_attribute(self.variable).sum()
        self.do_check("x >= 0 and x <= " + str(size), values)
