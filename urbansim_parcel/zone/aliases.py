# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

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
