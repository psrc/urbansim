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

from variable_functions import my_attribute_label
from urbansim_parcel.building.age_masked import age_masked

class building_age(age_masked):
    """The age of buildings in proposals, computed by subtracting the year built
    from the current simulation year. All values that have year_built <= urbansim_constant["absolute_min_year"]
    are masked.
    """

    year_built = "start_year"

    def dependencies(self):
        return [my_attribute_label(self.year_built), my_attribute_label("has_valid_year_built")]
