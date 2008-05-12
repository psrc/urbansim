
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

aliases = [
           "number_of_young_households=gridcell.aggregate(urbansim.household.is_young)",
           "number_of_home_owners=gridcell.aggregate(urbansim.household.is_home_owner)",           
           "number_of_home_renters=gridcell.aggregate(urbansim.household.is_home_renter)",
           "number_of_households_with_children=gridcell.aggregate(urbansim.household.has_children)",
           ]