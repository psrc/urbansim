
-- This is the most updated script:

-- Get the number of households by zone_id
drop table if exists hh_by_zone;
create table hh_by_zone
select hh.zone_id, count(*) as num_hh
from households as hh group by hh.zone_id;

-- Get the number of residential_units by zone_id
drop table if exists res_units_by_zone;
create table res_units_by_zone
select b.zone_id, sum(residential_units) as res_units
from buildings as b group by b.zone_id;

-- Calculate the number of units to build or demolish
-- for a vacancy rate of 7%
drop table if exists units_to_build;
create table units_to_build
SELECT
  h.zone_id,
  h.num_hh as occupied_units,
  r.res_units as total_units,
  -- (r.res_units-num_hh) as available_units,
  (r.res_units-num_hh)/res_units as vac_rate,
  round((h.num_hh * 1.07)-h.num_hh) + h.num_hh as target_units,
  (round((h.num_hh * 1.07)-h.num_hh) + h.num_hh) - r.res_units as units_to_build
from hh_by_zone as h
left join res_units_by_zone as r
on h.zone_id = r.zone_id
order by units_to_build;


-- Manually insert units_to_build value to deal
-- with NULLs in the table
update units_to_build
set units_to_build = 27 where units_to_build is null;

-- Add a field proportion_to_del and update it
alter table units_to_build
add column proportion_to_del double;
update units_to_build
set proportion_to_del = (abs(units_to_build))/total_units;

-- Update proportion_to_delete
update units_to_build
set proportion_to_del = 0
where units_to_build > 0;

-- Creates a table of sf units by zone
drop table if exists sf_units_by_zone;
create table sf_units_by_zone
select zone_id, sum(residential_units) as total_sf_units
from buildings where residential_units = 1 group by zone_id;

-- Creates a table of sf units to delete
drop table if exists sf_units_to_delete;
create table sf_units_to_delete
select
  s.zone_id,
  round(proportion_to_del*total_sf_units) as sf_units_to_delete_in_zone
from units_to_build u
inner join sf_units_by_zone s
on u.zone_id = s.zone_id
order by zone_id;

-- Deletes records with no sf units to delete
delete from sf_units_to_delete
where sf_units_to_delete_in_zone = 0;

-- Liming's script for creating a table of random sf units to delete
-- from the buildings table using the above

create table if not exists tmp_ordered_num
select zone_id as dummy from buildings;

alter table tmp_ordered_num add ordered_id int auto_increment primary key;

delete from tmp_ordered_num where ordered_id > 801;

drop table if exists expanded_delete_table;
create table expanded_delete_table
select zone_id, sf_units_to_delete_in_zone, ordered_id
from tmp_ordered_num t inner join sf_units_to_delete a
on t.ordered_id <= a.sf_units_to_delete_in_zone;

set @ordered_id = 0;
set @zone_id = 0;

drop table if exists tmp_ordered_buildings;
create table tmp_ordered_buildings
select
building_id,
if(@zone_id = zone_id, @ordered_id:=@ordered_id+1, @ordered_id:=1) as ordered_id1,
@zone_id:=zone_id as zone_id1
from (select * from buildings order by zone_id, rand()) as ordered_building
where residential_units = 1;

-- Creates a table of SF units to delete
create index zone_id_order_id_index1 on tmp_ordered_buildings(zone_id1, ordered_id1);
create index zone_id_order_id_index1 on expanded_delete_table(zone_id, ordered_id);
drop table if exists sf_homes_to_delete;
create table sf_homes_to_delete
select * from tmp_ordered_buildings inner join expanded_delete_table on
zone_id = zone_id1 and ordered_id = ordered_id1;

-- Deletes sf units from buildings table
create index building_id_index1 on buildings(building_id);
create index building_id_index1 on sf_homes_to_delete(building_id);
delete from buildings b
using buildings b, sf_homes_to_delete s
where b.building_id = s.building_id;


-- MULTI-FAMILY UNITS UPDATE
-- Creates a table of mf units by zone
create table mf_units_by_zone
select zone_id, sum(residential_units) as total_mf_units from buildings where residential_units > 1 group by zone_id;

/*
-- Creates a table of mf units to delete
create table mf_units_to_delete
select
  m.zone_id,
  round(proportion_to_del*total_mf_units) as mf_units_to_delete_in_zone
from units_to_build u
inner join mf_units_by_zone m
on u.zone_id = m.zone_id
order by zone_id;

-- Deletes records with no mf units to delete
delete from mf_units_to_delete
where mf_units_to_delete_in_zone = 0;
*/

-- Creates a table of new mf unit numbers to replace old ones
create table new_mf_units
select
building_id,
residential_units - (round(residential_units * proportion_to_del)) as new_units
from buildings b inner join units_to_build m on
b.zone_id = m.zone_id
where b.residential_units > 1;

-- Create building_id indexes
create index building_id_index3 on buildings(building_id);
create index building_id_index4 on new_mf_units(building_id);

-- Updates buildings table with new mf unit numbers
update buildings b, new_mf_units n
set b.residential_units = n.new_units
where b.building_id = n.building_id;

-- DIAGNOSTICS
-- Run this if you want to recalculate new vacancy rates
-- to check on the difference

-- Get the number of residential_units by zone_id
drop table if exists res_units_by_zone_NEW;
create table res_units_by_zone_NEW
select b.zone_id, sum(residential_units) as res_units
from buildings as b group by b.zone_id;

-- Calculate the number of units to build or demolish
-- for a vacancy rate of 7%
drop table if exists units_to_build_NEW;
create table units_to_build_NEW
SELECT
  h.zone_id,
  h.num_hh as occupied_units,
  r.res_units as total_units,
  -- (r.res_units-num_hh) as available_units,
  (r.res_units-num_hh)/res_units as vac_rate,
  round((h.num_hh * 1.07)-h.num_hh) + h.num_hh as target_units,
  (round((h.num_hh * 1.07)-h.num_hh) + h.num_hh) - r.res_units as units_to_build
from hh_by_zone as h
left join res_units_by_zone_NEW as r
on h.zone_id = r.zone_id
order by units_to_build;


/*
-- CLEAN UP
-- These lines clean up all unnecessary tables
drop table if exists expanded_delete_table;
drop table if exists hh_by_zone;
drop table if exists mf_units_by_zone;
drop table if exists new_mf_units;
drop table if exists res_units_by_zone;
drop table if exists res_units_by_zone_NEW;
drop table if exists sf_homes_to_delete;
drop table if exists sf_units_by_zone;
drop table if exists sf_units_to_delete;
drop table if exists tmp_ordered_buildings;
drop table if exists tmp_ordered_num;
drop table if exists units_to_build;
drop table if exists units_to_build_NEW;