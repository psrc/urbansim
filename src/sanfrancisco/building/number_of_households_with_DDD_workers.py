#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

class number_of_households_with_DDD_workers(Variable):
    """Number of households with DDD workers"""

    _return_type="int32"
    def __init__(self, nworkers):
        self.nworkers = nworkers
        Variable.__init__(self)
        
    def dependencies(self):
        return [
                "_number_of_households_with_%s_workers = building.aggregate(sanfrancisco.household.has_%s_workers)" % (self.nworkers, self.nworkers),
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_number_of_households_with_%s_workers" % self.nworkers)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("household").size()
        self.do_check("x >= 0 and x <= " + str(size), values)
