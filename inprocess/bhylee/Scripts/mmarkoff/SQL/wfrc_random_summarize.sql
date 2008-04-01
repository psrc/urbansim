# generate tables summarizing the output we wish to compare
# script assuming a database has been selected.

#aggregate by gridcell, TAZ, smldist, city, region, county


# Population totals
create table pop_grid
	select a.grid_id, a.YEAR, sum(b.PERSONS) as pop
from households_exported a inner join households_constants b
  on a.HOUSEHOLD_ID = b.HOUSEHOLD_ID
group by grid_id, YEAR;

create table pop_TAZ
	select a.zone_id, a.YEAR, sum(b.pop) as pop
from households_exported a inner join pop_grid b
  on a.grid_id = b.grid_id
group by zone_id, YEAR;

create table pop_distsml
	select a.distsml, a.YEAR, sum(b.pop) as pop
from WFRC_1997_baseyear.zones a inner join pop_TAZ b
  on a.zone_id = b.zone_id
group by distsml, YEAR;

create table pop_city
# city_id in gridcells tabel in baseyear

create table pop_region

create table pop_county
	select a.county, a.YEAR, sum(b.pop) as pop
from WFRC_1997_baseyear.zones a inner join pop_TAZ b
  on a.zone_id = b.zone_id
group by county, YEAR;


# Employment totals

# Housing units

# Non-res sqft