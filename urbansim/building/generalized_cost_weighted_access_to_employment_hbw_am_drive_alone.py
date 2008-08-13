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

class generalized_cost_weighted_access_to_employment_hbw_am_drive_alone(Variable):
    """
    """
    _return_type="float32"
    
    def dependencies(self):
        return ["_generalized_cost_weighted_access_to_employment_hbw_am_drive_alone=building.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone)"]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("_generalized_cost_weighted_access_to_employment_hbw_am_drive_alone")
        
    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
