# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
    "avg_trip_weighted_zone_logsum = ((psrc_parcel.household.income_breaks_34000_64000_102000==1) * building.disaggregate(psrc.zone.trip_weighted_average_logsum_hbw_am_income_1)) + ((psrc_parcel.household.income_breaks_34000_64000_102000==2) * building.disaggregate(psrc.zone.trip_weighted_average_logsum_hbw_am_income_2)) + ((psrc_parcel.household.income_breaks_34000_64000_102000==3) * building.disaggregate(psrc.zone.trip_weighted_average_logsum_hbw_am_income_3)) + ((psrc_parcel.household.income_breaks_34000_64000_102000==4) * building.disaggregate(psrc.zone.trip_weighted_average_logsum_hbw_am_income_4))"
]