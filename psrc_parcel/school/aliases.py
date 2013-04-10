# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
   "zone_id = school.disaggregate(parcel.zone_id)",
   "faz_id = school.disaggregate(zone.faz_id, intermediates=[parcel])",
   "school_district_id = school.disaggregate(parcel.school_district_id)",
   "is_in_category_1 = (school.category == 'K') + (school.category == 'D')",
   "is_in_category_2 = (school.category == 'E') + (school.category == 'EM') + (school.category == 'EMH')",
   "is_in_category_3 = (school.category == 'M') + (school.category == 'EM') + (school.category == 'EMH')  + (school.category == 'MH')",
   "is_in_category_4 = (school.category == 'H') + (school.category == 'MH') + (school.category == 'EMH')",
   "is_in_category_5 = school.category == 'U'"
   ]