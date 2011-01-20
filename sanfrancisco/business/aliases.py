# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
           "activity_name=business.disaggregate(activity.activity_name)",
           "parcel_id=business.disaggregate(building.parcel_id)",
           "zone_id=business.disaggregate(parcel.zone_id, intermediates=[building])"
           ]
