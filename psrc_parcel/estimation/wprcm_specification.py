# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

specification = {
    -2: {
     "equation_ids":(1, 0),  # 1:change job; 0:keep job
        "constant":("b1_asc", 0),
         #'tt_to_work = psrc_parcel.person.travel_time_from_home_to_work_drive_alone_hbw_am': ('b1_tt', 0),
         #'has_tt_to_work = psrc_parcel.person.travel_time_from_home_to_work_drive_alone_hbw_am > 0': ('b1_htt', 0), 
         'person.age': ('b1_age', 0),
         'known_age = person.age >= 0': ('b1_hasage', 0),
         'ln_income = ln(person.disaggregate(household.income))': ('b1_lninc', 0),
         'has_income = person.disaggregate(household.income > 0)': ('b1_hasinc', 0),
         }
    }