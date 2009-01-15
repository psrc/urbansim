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

specification = {
    -2: {
     "equation_ids":(1, 0),  # 1:move; 0:stay
        "constant":("b1_asc", 0),
         'ln_income = ln(household.income)': ('b1_lninc', 0),
         'has_income = household.income > 0': ('b1_hasinc', 0),
         #'household.income': ('b1_inc', 0),
         'urbansim_parcel.household.hh_adults_mean_age': ('b1_age', 0),
         #'change_in_tt_to_work = psrc_parcel.household.max_drive_alone_hbw_am_travel_time_from_home_to_work - psrc_parcel.household.max_drive_alone_hbw_am_travel_time_from_home_to_work_lag1', 'change_in_tt_to_work'
         'tt_to_work = psrc_parcel.household.max_drive_alone_hbw_am_travel_time_from_home_to_work': ('b1_tt', 0),
         #'urbansim.household.has_workers': ('b1_hasw', 0),
         #'has_nhb_workers_with_job = urbansim_parcel.household.number_of_non_home_based_workers_with_job > 0': ('b1_haswj', 0)
         'has_tt_to_work = psrc_parcel.household.max_drive_alone_hbw_am_travel_time_from_home_to_work > 0': ('b1_htt', 0),
         }
    }