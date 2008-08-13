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

class average_income(Variable):
    """average income in a given zone"""

    _return_type="int32"
    
    def dependencies(self):
        return ["sanfrancisco.household.zone_id", 
                "_average_income=zone.aggregate(household.income, function=mean)"
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_average_income")

    def post_check(self,  values, dataset_pool=None):
        imin = dataset_pool.get_dataset("household").get_attribute("income").min()
        imax = dataset_pool.get_dataset("household").get_attribute("income").max()
        self.do_check("x >= %s and x <= %s" % (imin, imax), values)
