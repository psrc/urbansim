#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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
from numpy import zeros

class developable_maximum_commercial_sqft(Variable):
    """How many commercial sqft are at most developable for each gridcell after applying
    development constraints."""

    _return_type = "int32"
    commercial_sqft = "commercial_sqft"
    total_maximum = "total_maximum_development_commercial"

    def dependencies(self):
        return [my_attribute_label(self.commercial_sqft),
                my_attribute_label(self.total_maximum)
                 ]

    def compute(self, dataset_pool):
        is_developable = self.get_dataset().get_attribute(self.total_maximum) > 0
        result = zeros((self.get_dataset().size(),),dtype=self._return_type)
        values = self.get_dataset().get_attribute_by_index(self.total_maximum, is_developable) - \
            self.get_dataset().get_attribute_by_index(self.commercial_sqft, is_developable)
        result[is_developable] = values.astype(self._return_type)
        return result

    def post_check(self, values, dataset_pool):
        upper_limit = 4000000   #TODO replace hard-coded upper limit with config or constant
        self.do_check("x >= 0 and x <= %s" % upper_limit, values)
