-- Get the number of households by zone_id
drop table if exists hh_by_zone;
create table hh_by_zone
select hh.zone_id, count(*) as num_hh from households as hh group by hh.zone_id;
-- Get the number of residential_units by zone_id
drop table if exists res_units_by_zone;
create table res_units_by_zone
select b.zone_id, sum(residential_units) as res_units from buildings as b group by b.zone_id;

-- Calculate the number of units to build or demolish
-- for a vacancy rate of 7%
drop table if exists units_to_build;
create table units_to_build
SELECT
  h.zone_id,
  h.num_hh as occupied_units,
  r.res_units as total_units,
  -- (r.res_units-num_hh) as available_units,
  -- (r.res_units-num_hh)/res_units as vac_rate,
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

-- Clean up tables
drop table if exists hh_by_zone;
drop table if exists res_units_by_zone;