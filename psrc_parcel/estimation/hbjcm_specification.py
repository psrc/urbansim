
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
    #"hh_size = person.disaggregate(household.persons)",
    #"hh_children = person.disaggregate(household.children > 0)",
    #"hh_income = person.disaggregate(household.income)",
    #"hh_workers = person.disaggregate(household.workers)",
    #"person.age",
    #"person.edu",       

    #"hh_size_x_work_at_home = person.disaggregate(household.persons) * (choice.work_at_home==1)",
    #"hh_children_x_work_at_home = person.disaggregate(household.children > 0) * (choice.work_at_home==1)",
    #"hh_income_x_work_at_home = person.disaggregate(household.income) * (choice.work_at_home==1)",
    #"hh_workers_x_work_at_home = ( person.disaggregate(household.workers) - 1 ) * (choice.work_at_home==1)",    
   ]

specification = {}

specification = {
    "_definition_": all_variables,                               
    
    -2:{
        "equation_ids":(1, 2),  # 1:work-at-home; 2:work non-home-based
        "constant":(0, "act_2"),
        #"person.disaggregate(household.persons)":("beta1_hhsize", 0),
        #"person.disaggregate(household.children > 0)":("beta1_haschild", 0),
        "person.disaggregate(household.income)":("beta1_income", 0),
        #"age3=person.disaggregate(urbansim_parcel.household.persons_with_age_le_3>0)":("beta1_age3", 0),
        #"age6=person.disaggregate(urbansim_parcel.household.persons_with_age_le_6>0)":("beta1_age6", 0),
        #"age13=person.disaggregate(urbansim_parcel.household.persons_with_age_le_13>0)":("beta1_age13", 0),
        #"age16=person.disaggregate(urbansim_parcel.household.persons_with_age_le_16>0)":("beta1_age16", 0),
        #"age18=person.disaggregate(urbansim_parcel.household.persons_with_age_le_18>0)":("beta1_age18", 0),        
        #"person.disaggregate(household.workers-1)":("beta1_workers", 0),
        "person.age":("beta1_age", 0),
        "person.edu":("beta1_edu", 0),
        "person.employment_status==2":("beta1_parttm", 0), ##part time worker
    }

}
