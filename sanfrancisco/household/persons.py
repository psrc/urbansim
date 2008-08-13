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

class persons(Variable):
    """number of persons in a given household"""

    _return_type="int32"
    
    def dependencies(self):
        return ["_persons=household.number_of_agents(person)"
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_persons")

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("person").size()
        self.do_check("x >= 0 and x <= " + str(size), values)
