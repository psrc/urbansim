# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
   "zone_id = household.disaggregate(urbansim_parcel.building.zone_id)",
   "parcel_id = household.disaggregate(urbansim_parcel.building.parcel_id)",
   "grid_id = household.disaggregate(urbansim_parcel.building.grid_id)",
   "persons_with_age_le_3 = household.aggregate(person.age<=3)",
   "persons_with_age_le_6 = household.aggregate(person.age<=6)",
   "persons_with_age_le_13 = household.aggregate(person.age<=13)",   
   "persons_with_age_le_16 = household.aggregate(person.age<=16)",      
   "persons_with_age_le_18 = household.aggregate(person.age<=18)",
   "number_of_adults = household.aggregate(person.age>=18)",
   "faz_id = household.disaggregate(zone.faz_id, intermediates=[parcel, building])",
#   "large_area_id = household.disaggregate(faz.large_area_id, intermediates=[zone, parcel, building])",
   "large_area_id = household.disaggregate(parcel.large_area_id, intermediates=[building])",   
   "county_id = household.disaggregate(parcel.county_id, intermediates=[building])",   
   
   "dummy_id = urbansim_parcel.household.faz_id * 100 + household.persons",
   'number_of_non_home_based_workers = household.aggregate(urbansim_parcel.person.is_non_home_based_worker)',
   'number_of_non_home_based_workers_with_job = household.aggregate(urbansim_parcel.person.is_non_home_based_worker_with_job)',
   'residence_zone_id = household.disaggregate(parcel.zone_id,intermediates=[building])',
   'residence_area_type_id = household.disaggregate(zone.area_type_id,intermediates=[parcel, building])',
   'residence_district_id = household.disaggregate(zone.district_id,intermediates=[parcel, building])',
   'residence_faz_id = household.disaggregate(zone.faz_id,intermediates=[parcel, building])',
   'residence_large_area_id = household.disaggregate(faz.large_area_id,intermediates=[zone, parcel, building])',
   "cars_category=0*(household.cars==0)+1*(household.cars==1)+2*(household.cars==2)+3*(household.cars>=3)"
           ]
