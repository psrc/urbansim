
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
    "hh_size = person.disaggregate(household.persons)",
    "hh_child = person.disaggregate(household.children > 0)",
    "hh_income = person.disaggregate(household.income)",
    "hh_workers = person.disaggregate(household.workers)",
    "person.age",
    "person.edu",       
#    "hh_income_x_work_at_home = person.disaggregate(household.income) * (choice.work_at_home==1)",
#    "hh_size_x_work_at_home = person.disaggregate(household.persons) * (choice.work_at_home==1)",
    ]

specification = {}

specification = {
    "_definition_": all_variables,                               
    -2:
    {
        "equation_ids":(0, 1),
        #"constant":(0, "act_1"),
        #"person.disaggregate(household.persons)":(0, "beta1_hhsize")   
        #"hh_size":(0, "beta1_hhsize")   
        "person.disaggregate(household.children > 0)":(0, "beta1_haschild")
        #"hh_child":(0, "beta1_haschild")   
        #"person.disaggregate(household.income)":(0, "beta1_income")   
        #"hh_income":(0, "beta1_income")   
        #"person.disaggregate(household.workers)":(0, "beta1_workers"),
        #"person.hh_workers":(0, "beta1_workers"),
        #"age":(0, "beta1_age")   
    }
}
