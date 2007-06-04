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
from numpy import where, exp

class pop_density(Variable):
    """Returns a population in 1000's per square kilometer"""

    dept = "dept"

    def dependencies(self):
        return ["neighborhood.lpoprp99","neighborhood.areakm2"]

    def compute(self, dataset_pool):
        lpop = self.get_dataset().get_attribute("lpoprp99")
        areakm2 = self.get_dataset().get_attribute("areakm2")
        pop = exp(lpop)
        pop1k = pop/1000
        density = pop1k/areakm2
        return density


