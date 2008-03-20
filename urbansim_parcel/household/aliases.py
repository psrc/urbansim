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

aliases = [
   "zone_id = household.disaggregate(urbansim_parcel.building.zone_id)",
   "parcel_id = household.disaggregate(urbansim_parcel.building.parcel_id)",
   "has_person_age_le_3 = household.aggregate(person.age<=3)",
   "has_person_age_le_6 = household.aggregate(person.age<=6)",
   "has_person_age_le_13 = household.aggregate(person.age<=13)",   
   
           ]