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
