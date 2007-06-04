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
from variable_functions import my_attribute_label

class travel_time_hbw_am_drive_alone_to_cbd(Variable):
    """Travel time to the CBD zone whose ID is the 129.
    The travel time used is for the home-based-work am trips by auto with 
    drive-alone.
    """
    #TODO: eliminate hard-coded constant.
    cbd_zone = "129"
    variable_name = "travel_time_hbw_am_drive_alone_to_"+cbd_zone
    def dependencies(self):
        return [my_attribute_label(self.variable_name)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.variable_name)
