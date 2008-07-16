#
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

aliases = [
   "average_income = zone.aggregate(urbansim_parcel.household.income, function=mean)",
   "employment = zone.number_of_agents(job)",
   "number_of_jobs = zone.number_of_agents(job)",
   "number_of_households = zone.number_of_agents(household)",
   "population = zone.aggregate(household.persons)"
           ]

for group in ['retail', 'manu', 'wtcu', 'fires', 'gov', 'edu']:
    aliases.append("number_of_jobs_of_sector_group_%s = zone.aggregate(urbansim_parcel.building.number_of_jobs_of_sector_group_%s)" % (group, group))
    
for sec, group in [(1, 'mining'), (2, 'constr')]:
    aliases.append("number_of_jobs_of_sector_group_%s = zone.aggregate(urbansim_parcel.building.number_of_jobs_of_sector_%s)" % (group, sec))
