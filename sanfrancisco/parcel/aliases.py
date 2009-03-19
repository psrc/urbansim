# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
       "number_of_businesses = parcel.aggregate(sanfrancisco.building.number_of_businesses)",
       "employment = parcel.aggregate(sanfrancisco.building.employment)",
       "number_of_households = parcel.aggregate(sanfrancisco.building.number_of_households)",
       "population = parcel.aggregate(sanfrancisco.building.population)", 
           ]