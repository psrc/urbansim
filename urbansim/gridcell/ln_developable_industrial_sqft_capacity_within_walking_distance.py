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

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_developable_industrial_sqft_capacity_within_walking_distance(Variable):
    """Natural log of the developable_industrial_sqft_capacity_within_walking_distance for this gridcell"""
    
    _return_type="float32"    
    industrial_sqft_wwd = "developable_industrial_sqft_capacity_within_walking_distance"

    def dependencies(self):
        return [my_attribute_label(self.industrial_sqft_wwd)]

    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.industrial_sqft_wwd))

#this is a special case of commercial_sqft_within_walking_distance, so the unnittest is there
#the ln_bounded function is tested in ln_commercial_sqft