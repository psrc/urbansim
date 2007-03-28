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

class SSS_occupied(Variable):
    """units occupied by consumers for building_type name SSS"""

    _return_type="Int32"
    def __init__(self, sector):
        self.type_name = building_type.lower()
        Variable.__init__(self)
        
    def dependencies(self):
        return []

    def compute(self,  dataset_pool):
        building_types = dataset_pool.get_dataset("build_type")
        consumption = building_types.get_attribute("consumption")[where(builing_types.get_attribute("type_name")==self.type_name)]

        buildings = self.get_dataset()
        buildings.compute_variables("occupied = building.%s" % consumption)
        return buildings.get_attribute(occupied)

    def post_check(self,  values, dataset_pool=None):
#        size = dataset_pool.get_dataset("building").size()
        self.do_check("x >= 0")
