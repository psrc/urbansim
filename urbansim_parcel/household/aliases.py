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
   "grid_id = household.disaggregate(urbansim_parcel.building.grid_id)",
   "persons_with_age_le_3 = household.aggregate(person.age<=3)",
   "persons_with_age_le_6 = household.aggregate(person.age<=6)",
   "persons_with_age_le_13 = household.aggregate(person.age<=13)",   
   "persons_with_age_le_16 = household.aggregate(person.age<=16)",      
   "persons_with_age_le_18 = household.aggregate(person.age<=18)",

   "faz_id = household.disaggregate(zone.faz_id, intermediates=[parcel, building])",
   "dummy_id = urbansim_parcel.household.faz_id * 100 + household.persons",
   'number_of_non_home_based_workers = household.aggregate(urbansim_parcel.person.is_non_home_based_worker)',
   'number_of_non_home_based_workers_with_job = household.aggregate(urbansim_parcel.person.is_non_home_based_worker_with_job)'
           ]