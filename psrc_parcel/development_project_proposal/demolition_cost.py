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
from numarray import zeros

class demolition_cost(Variable):
    """return a dummy demolition cost (0s).
       it may be an outcome attribute from a model, 
       thus this variable is not needed
       """ 

    def dependencies(self):
        return []

    def compute(self, dataset_pool):
        return zeros(self.get_dataset().size())

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
    