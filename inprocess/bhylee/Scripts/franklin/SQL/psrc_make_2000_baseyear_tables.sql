

use psrc_2000_parcel_baseyear_start;

# Households
drop table if exists households;
create table households
     like GSPSRC_2000_baseyear_change_20060924.households;

insert into households
     select * from GSPSRC_2000_baseyear_change_20060924.households;

# Cities
drop table if exists cities;
create table cities
     like GSPSRC_2000_baseyear_change_20050428.cities;

insert into cities
     select * from GSPSRC_2000_baseyear_change_20050428.cities;

# Counties
drop table if exists counties;
create table counties
     like GSPSRC_2000_baseyear_change_20060427.counties;

insert into counties
     select * from GSPSRC_2000_baseyear_change_20060427.counties;

# Zones
drop table if exists zones;
create table zones
     like GSPSRC_2000_baseyear_change_20051020.zones;

insert into zones
     select * from GSPSRC_2000_baseyear_change_20051020.zones;





















