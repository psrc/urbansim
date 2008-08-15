#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

aliases = [
  'all_trips = faz.aggregate(psrc.zone.trip_mode_bike + psrc.zone.trip_mode_drive_alone + psrc.zone.trip_mode_walk + psrc.zone.trip_mode_park_ride  + psrc.zone.trip_mode_share_ride2 + psrc.zone.trip_mode_share_ride3 + psrc.zone.trip_mode_transit)',
  'mode_split_drive_alone = faz.aggregate(psrc.zone.trip_mode_drive_alone)/(psrc.faz.all_trips).astype(float32)',
  'mode_split_transit = faz.aggregate(psrc.zone.trip_mode_transit)/(psrc.faz.all_trips).astype(float32)',
  'mode_split_share_ride = faz.aggregate(psrc.zone.trip_mode_share_ride2+psrc.zone.trip_mode_share_ride3)/(psrc.faz.all_trips).astype(float32)',
           ]