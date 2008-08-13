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

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
   "employment_of_sector_cie = zone.aggregate(sanfrancisco.building.employment_of_sector_cie, intermediates=[parcel])",
   "employment_of_sector_med = zone.aggregate(sanfrancisco.building.employment_of_sector_med, intermediates=[parcel])",
   "employment_of_sector_mips = zone.aggregate(sanfrancisco.building.employment_of_sector_mips, intermediates=[parcel])",
   "employment_of_sector_pdr = zone.aggregate(sanfrancisco.building.employment_of_sector_pdr, intermediates=[parcel])",   
   "employment_of_sector_visitor = zone.aggregate(sanfrancisco.building.employment_of_sector_visitor, intermediates=[parcel])",
   "employment_of_sector_retailent = zone.aggregate(sanfrancisco.building.employment_of_sector_retailent, intermediates=[parcel])",

]