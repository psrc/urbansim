# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
       "is_redevelopable=(parcel.number_of_agents(building)>0)*(urbansim_parcel.parcel.improvement_value / ( urbansim_parcel.parcel.unit_price * urbansim_parcel.parcel.existing_units ) < 0.1)*(parcel.aggregate(urbansim_parcel.building.age_masked, function=mean)>30)",       
           ]
