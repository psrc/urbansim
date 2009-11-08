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
from numpy import zeros, logical_and

class household_size_category(Variable):
    """recoding of household size for use as submodel string """

    _return_type="int32"
    
    def dependencies(self):
        return ["household.household_size"
                ]

    def compute(self,  dataset_pool):
        hhs = self.get_dataset().get_attribute("household_size")
        results = zeros(hhs.size) + 3  #by default, categorize to 3
        results[hhs==1] = 1            #change to 1 if household size is 1
        results[hhs==2] = 2            #change to 2 if household size is 2
        return results

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("person").size()
        self.do_check("x >= 0 and x <= " + str(size), values)
