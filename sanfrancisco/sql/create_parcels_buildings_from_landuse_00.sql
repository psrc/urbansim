

create table parcels_00 select
blklot as mapblklot, blklot, from_ as from_st, to_ as to_st, streetname as street_name, type as street_type,
odd_even, '' as neighorhood, null as taz, use_type, landuse, land_val as land_value,
zoning, height_lim as heightlimit, far_allowd, null as census_tract, perimeter, area
from luse00;

alter table parcels_00 add parcel_id int auto_increment primary key;

create table buildings_00 select
blklot as mapblklot, blklot, landuse as building_use, residtype as restype, struc_val as structure_value, stories,
residunits as residential_units, null as bedrooms, bldg_sqft as building_sqft,
yr_built as year_built, bldg_sqft as total_uses, 0 as cie, 0 as med, 0 as mips,
0 as retail, 0 as pdr, 0 as visitor
from luse00;

alter table buildings_00 add building_id int auto_increment primary key;

create index blklot_index on parcels_00 (blklot);
create index blklot_index on buildings_00 (blklot);

alter table buildings_00 add building_use_id int, add parcel_id int, add sale_price int, add unit_price double;
update buildings_00 b, parcels_00 p set b.parcel_id=p.parcel_id where b.blklot=p.blklot;
update buildings_00 b, building_use u set b.building_use_id=u.building_use_id where b.building_use <> 'resident'
       and b.building_use=u.building_use;
update buildings_00 b, building_use u set b.building_use_id=u.building_use_id where b.building_use = 'resident'
       and b.restype=u.building_use;


