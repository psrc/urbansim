# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
    "avg_trip_weighted_zone_logsum = ((psrc_parcel.household.income_breaks_34000_64000_102000==1) * building.disaggregate(psrc.zone.trip_weighted_average_logsum_hbw_am_income_1)) + ((psrc_parcel.household.income_breaks_34000_64000_102000==2) * building.disaggregate(psrc.zone.trip_weighted_average_logsum_hbw_am_income_2)) + ((psrc_parcel.household.income_breaks_34000_64000_102000==3) * building.disaggregate(psrc.zone.trip_weighted_average_logsum_hbw_am_income_3)) + ((psrc_parcel.household.income_breaks_34000_64000_102000==4) * building.disaggregate(psrc.zone.trip_weighted_average_logsum_hbw_am_income_4))",
    "avg_trip_weighted_zone_gen_cost_if_no_workers = (urbansim_parcel.household.number_of_workers_with_job==0)*building.disaggregate(psrc.zone.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone, intermediates=[parcel])",
    "income_minus_toll = (clip_to_zero(household.income - psrc_parcel.household_x_building.sum_annual_toll_from_home_to_work)).astype(float32)"
]