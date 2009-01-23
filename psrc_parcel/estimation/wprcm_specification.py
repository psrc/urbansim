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