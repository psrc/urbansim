# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
           "resacre = zone.aggregate((parcel.shape_area*0.000247105381)*((parcel.shape_area*0.000247105381)<5)*parcel.aggregate(building.residential_units>0))",
           "ciacre = zone.aggregate((parcel.shape_area*0.000247105381)*parcel.aggregate(building.non_residential_sqft>0))",
           "taz = zone.zone_id",
           ##HACK, as the county_id in counties is meaningless and cannot be related to any zone attribute
           "county_id = zone.aggregate(parcel.county_id, function=median)", 
           "alldata_id = 1 + (zone.zone_id * 0)",
]
