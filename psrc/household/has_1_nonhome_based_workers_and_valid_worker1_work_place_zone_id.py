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
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from opus_core.logger import logger
from numpy import logical_and

class has_1_nonhome_based_workers_and_valid_worker1_work_place_zone_id(Variable):
    """return if a household has DDD nonhome based worker"""
    
    _return_type="bool8"

    def dependencies(self):
        return ["psrc.household.number_of_nonhome_based_workers",
                "psrc.household.worker1_work_place_zone_id",
                ]

    def compute(self, dataset_pool):
        households = self.get_dataset()
        return logical_and((households.get_attribute("number_of_nonhome_based_workers") == 1),
                           (households.get_attribute("worker1_work_place_zone_id") > 0))