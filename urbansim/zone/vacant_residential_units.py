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
from urbansim.gridcell.vacant_residential_units import vacant_residential_units as gc_vacant_residential_units

class vacant_residential_units(gc_vacant_residential_units):
    """The residential_units - number_of_households. """

    def dependencies(self):
        return [my_attribute_label(self.number_of_households), 
                my_attribute_label(self.residential_units)]
