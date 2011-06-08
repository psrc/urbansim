# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
       "is_redevelopable=(parcel.number_of_agents(building)>0)*(urbansim_parcel.parcel.improvement_value / ( urbansim_parcel.parcel.unit_price * urbansim_parcel.parcel.existing_units ) < 0.1)*(parcel.aggregate(urbansim_parcel.building.age_masked, function=mean)>30)",       
       "total_price=parcel.land_value+parcel.aggregate(building.improvement_value)",
       "yard_sqft_per_unit = safe_array_divide( parcel.parcel_sqft-parcel.aggregate(building.land_area), (urbansim_parcel.parcel.residential_units).astype(float32) )",
       "residential_units = parcel.aggregate(building.residential_units)",
       "number_of_private_schools = parcel.aggregate(school.public==0)",
       "number_of_public_schools = parcel.aggregate(school.public)",
       "number_of_schools = parcel.number_of_agents(school)",
       "number_of_good_public_schools = parcel.aggregate(school.public * (school.total_score >= 8))",
           ]
