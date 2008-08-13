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
from numpy import where

class empscaled(Variable):
    """Returns a boolean indicating if the neighborhood is in Paris"""

    dept = "dept"

    def dependencies(self):
        return ["neighborhood.emptot9"]

    def compute(self, dataset_pool):
        emptot9 = self.get_dataset().get_attribute("emptot9")
        return emptot9/1000

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)


