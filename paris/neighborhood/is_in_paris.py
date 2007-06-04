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
from numpy import where

class is_in_paris(Variable):
    """Returns a boolean indicating if the neighborhood is in Paris"""

    dept = "dept"

    def dependencies(self):
        return ["neighborhood.dept"]

    def compute(self, dataset_pool):
        dept = self.get_dataset().get_attribute("dept")
        return where(dept == 75, True, False)

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)


