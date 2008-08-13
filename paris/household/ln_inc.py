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

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_inc(Variable):
    """Natural log of the inc for this gridcell"""
        
    _return_type="float32"
    inc = "medinc"

    def dependencies(self):
        return [my_attribute_label(self.inc)]

    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.inc))
