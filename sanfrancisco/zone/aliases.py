# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
   "average_income=zone.aggregate(household.income, intermediates=[building,parcel], function=mean)",
   "employment = sanfrancisco.zone.aggregate_employment_from_building",
   "employment_of_activity_cie = zone.aggregate(where(sanfrancisco.business.activity=='CIE',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
   "employment_of_activity_med = zone.aggregate(where(sanfrancisco.business.activity=='MED',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
   "employment_of_activity_mips = zone.aggregate(where(sanfrancisco.business.activity=='MIPS',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
   "employment_of_activity_pdr = zone.aggregate(where(sanfrancisco.business.activity=='PDR',sanfrancisco.business.employment,0), intermediates=[building, parcel])",   
   "employment_of_activity_visitor = zone.aggregate(where(sanfrancisco.business.activity=='VISITOR',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
   "employment_of_activity_retailent = zone.aggregate(where(sanfrancisco.business.activity=='RETAIL/ENT',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
   "number_of_households=zone.aggregate(sanfrancisco.building.number_of_households, intermediates=[parcel])",
   "population=zone.aggregate(sanfrancisco.building.population, intermediates=[parcel])",
   ]