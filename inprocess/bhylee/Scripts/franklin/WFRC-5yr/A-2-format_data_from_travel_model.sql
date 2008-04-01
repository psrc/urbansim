# This script updates data based on imported travel data from the WFRC travel model.

use WFRC_1997_scenario_5yr;

# Create indices

create index 
  index_HighwayTimes_from_zone_id_to_zone_id 
  on HighwayTimes 
  (from_zone_id, to_zone_id);

create index
  index_AccessLogsum_from_zone_id_to_zone_id 
  on AccessLogsum 
  (from_zone_id, to_zone_id);

# Integrate data from the travel model's "####_HighwayTimes.tab" 
# into UrbanSim's "zones" table:

drop table if exists zones;

create table zones
  select ht1.from_zone_id as zone_id,
    ht1.hwytime as travel_time_to_airport,
    ht2.hwytime as travel_time_to_cbd
  from HighwayTimes as ht1, 
    HighwayTimes as ht2
  where ht1.from_zone_id = ht2.from_zone_id
    and ht1.to_zone_id = 425
    and ht2.to_zone_id = 459;

create index zones_zone_id
  on zones
  (zone_id);

drop table HighwayTimes;

# Integrate data from the travel model's "####_AccessLogsum.tab" 
# into UrbanSim's "travel_data" table:

drop table if exists travel_data;

alter ignore table AccessLogsum
  rename to travel_data;

alter ignore table travel_data
  add column logsum3 double after logsum2;

update ignore travel_data
  set logsum3 = logsum2;

# Later, we'll also need to integrate the travel model's
# "####CarOwnershipProbabilities.tab" into UrbanSim, somewhere.