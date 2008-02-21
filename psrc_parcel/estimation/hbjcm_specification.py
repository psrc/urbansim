
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

all_variables = [
    "hh_income_x_work_at_home = person.disaggregate(household.income) * (choice.work_at_home==1)",
    "hh_size_x_work_at_home = person.disaggregate(household.persons) * (choice.work_at_home==1)",
#         "hh_size",
#         "person.age",
#         "person.age",
#         "person.work_at_home",
#         "person.edu",         

    ]

specification = {}

specification = {
    "_definition_": all_variables,                               
    -2:
        [
#         "hh_income_x_work_at_home",
         "work_at_home=(choice.work_at_home==1)"
         ],                             
}
