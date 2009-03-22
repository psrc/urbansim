# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
   "employment_of_sector_cie = zone.aggregate(sanfrancisco.building.employment_of_sector_cie, intermediates=[parcel])",
   "employment_of_sector_med = zone.aggregate(sanfrancisco.building.employment_of_sector_med, intermediates=[parcel])",
   "employment_of_sector_mips = zone.aggregate(sanfrancisco.building.employment_of_sector_mips, intermediates=[parcel])",
   "employment_of_sector_pdr = zone.aggregate(sanfrancisco.building.employment_of_sector_pdr, intermediates=[parcel])",   
   "employment_of_sector_visitor = zone.aggregate(sanfrancisco.building.employment_of_sector_visitor, intermediates=[parcel])",
   "employment_of_sector_retailent = zone.aggregate(sanfrancisco.building.employment_of_sector_retailent, intermediates=[parcel])",

]