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
   "hhincq1 = zone.aggregate(sanfrancisco.household.in_income_quartile_1, intermediates=[building,parcel])",
   "hhincq2 = zone.aggregate(sanfrancisco.household.in_income_quartile_2, intermediates=[building,parcel])",
   "hhincq3 = zone.aggregate(sanfrancisco.household.in_income_quartile_3, intermediates=[building,parcel])",
   "hhincq4 = zone.aggregate(sanfrancisco.household.in_income_quartile_4, intermediates=[building,parcel])",
   "avgincq1 = safe_array_divide(zone.aggregate(where(sanfrancisco.household.in_income_quartile_1,household.income,0),intermediates=[building,parcel]),hhincq1)",
   "avgincq2 = safe_array_divide(zone.aggregate(where(sanfrancisco.household.in_income_quartile_2,household.income,0),intermediates=[building,parcel]),hhincq2)",
   "avgincq3 = safe_array_divide(zone.aggregate(where(sanfrancisco.household.in_income_quartile_3,household.income,0),intermediates=[building,parcel]),hhincq3)",
   "avgincq4 = safe_array_divide(zone.aggregate(where(sanfrancisco.household.in_income_quartile_4,household.income,0),intermediates=[building,parcel]),hhincq4)",
   "empres = zone.aggregate(sanfrancisco.household.nfulltime, intermediates=[building, parcel])+zone.aggregate(sanfrancisco.household.nparttime, intermediates=[building, parcel])",
   ]