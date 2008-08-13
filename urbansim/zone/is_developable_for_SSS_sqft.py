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

class is_developable_for_SSS_sqft(Variable):
    """"""

    def __init__(self, type):
        self.developable_max = "total_maximum_development_%s" % type
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.developable_max)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.developable_max) > 0
                       