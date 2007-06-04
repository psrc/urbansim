#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

class developable_residential_units(Variable):
    """"""

    developable_max = "developable_maximum_residential_units"
    def dependencies(self):
        return [my_attribute_label(self.developable_max)]

    def compute(self, dataset_pool):
        max = self.get_dataset().get_attribute(self.developable_max)
        return max

    def post_check(self, values, dataset_pool):
        global_max = self.get_dataset().get_attribute(self.developable_max).max()
        self.do_check("x >= 0 and x <= %s" % global_max, values)
                        