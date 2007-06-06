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

from az_smart.building.has_valid_year_built import has_valid_year_built as building_has_valid_year_built
from variable_functions import my_attribute_label

class has_valid_year_built(building_has_valid_year_built):
    """If proposals have valid start_year or not."""

    year_built = "start_year"

    def dependencies(self):
        return [my_attribute_label(self.year_built)]
