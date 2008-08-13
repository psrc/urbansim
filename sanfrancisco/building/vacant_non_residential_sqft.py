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
from opus_core.misc import clip_to_zero_if_needed

class vacant_non_residential_sqft(Variable):
    """"""

    _return_type="int32"
    
    def dependencies(self):
        return [
               #"_vacant_building_sqft=sanfrancisco.building.nonresidential_building_sqft - sanfrancisco.building.occupied_sqft", 
                "_vacant_nonresidential_sqft=building.non_residential_sqft - sanfrancisco.building.occupied_sqft"]

    def compute(self,  dataset_pool):
        return clip_to_zero_if_needed( self.get_dataset().get_attribute("_vacant_nonresidential_sqft") )

    def post_check(self,  values, dataset_pool=None):
        size = self.get_dataset().get_attribute("building_sqft").max()
        self.do_check("x >= 0 and x <= " + str(size), values)
