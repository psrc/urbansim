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

from opus_core.variable import Variable
from variable_functions import my_attribute_label
from opus_core.misc import clip_to_zero_if_needed

class vacant_building_sqft(Variable):
    """"""

    _return_type="Int32"
    
    def dependencies(self):
        return ["psrc_parcel.building.nonresidential_building_sqft", 
                "psrc_parcel.building.occupied_sqft", 
                my_attribute_label("building_id")]

    def compute(self,  dataset_pool):
        return clip_to_zero_if_needed(
               self.get_dataset().get_attribute("nonresidential_building_sqft") - \
               self.get_dataset().get_attribute("occupied_sqft"))

    def post_check(self,  values, dataset_pool=None):
        size = self.get_dataset().get_attribute("building_sqft").max()
        self.do_check("x >= 0 and x <= " + str(size), values)
