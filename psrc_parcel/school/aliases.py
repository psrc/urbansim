# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
   "zone_id = school.disaggregate(parcel.zone_id)",
   "faz_id = school.disaggregate(zone.faz_id, intermediates=[parcel])",
   "school_district_id = school.disaggregate(parcel.school_district_id)",
   ]