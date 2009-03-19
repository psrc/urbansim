# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

aliases = [
  'all_trips = faz.aggregate(psrc.zone.trip_mode_bike + psrc.zone.trip_mode_drive_alone + psrc.zone.trip_mode_walk + psrc.zone.trip_mode_park_ride  + psrc.zone.trip_mode_share_ride2 + psrc.zone.trip_mode_share_ride3 + psrc.zone.trip_mode_transit)',
  'mode_split_drive_alone = faz.aggregate(psrc.zone.trip_mode_drive_alone)/(psrc.faz.all_trips).astype(float32)',
  'mode_split_transit = faz.aggregate(psrc.zone.trip_mode_transit)/(psrc.faz.all_trips).astype(float32)',
  'mode_split_share_ride = faz.aggregate(psrc.zone.trip_mode_share_ride2+psrc.zone.trip_mode_share_ride3)/(psrc.faz.all_trips).astype(float32)',
           ]