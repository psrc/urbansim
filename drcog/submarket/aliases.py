# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
   "county_id = submarket.aggregate(building.disaggregate(parcel.county_id),function=median)",
   "residential_units = submarket.aggregate(building.residential_units)",
   "households = submarket.number_of_agents(household)",
           ]
