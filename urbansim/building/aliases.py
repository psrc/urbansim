
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
           "is_condo_residential=building.disaggregate(building_type.building_type_name=='condo_residential')",
           "is_single_family_residential=building.disaggregate(building_type.building_type_name == 'single_family_residential')",
           "is_multi_family_residential=building.disaggregate(building_type.building_type_name =='multi_family_residential')"
           ]