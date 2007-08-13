
drop table if exists buildings_backup_20070813;
create table buildings_backup_20070813 select * from buildings;

drop table if exists parcels_backup_20070813;
create table parcels_backup_20070813 select * from parcels;

drop table if exists buildings_01;
drop table if exists parcels_01;

create table parcels_01 select
mapblklot, mapblklot as blklot, block_num, lot_num, from_st, to_st, street as street_name, type as street_type, odd_even,
'' as neighorhood, taz, dbiusetype as use_type, landuse, land_val as land_value,
zoning, height_lim as heightlimit, far as far_allowed, census_tra as census_tract, shape_length as perimeter, shape_area as area,
mips_possible, cie_possible, med_possible, ret_possible, vis_possible, pdr_possible
from luse01;

create table buildings_01 select
mapblklot, mapblklot as blklot, landuse as building_use, restype, land_val as land_value, struc_val as structure_value,
stories, resunits as residential_units, bldg_sqft as building_sqft, yr_built as year_built,
totalusesq as total_uses, cie, med, mips, retail_ent as retail, pdr, visitor
from luse01;

create index blklot_index on parcels_01 (blklot);
create index blklot_index on buildings_01 (blklot);

alter table parcels_01 add parcel_id int auto_increment primary key;
alter table buildings_01 add building_id int auto_increment primary key;


alter table buildings_01 add building_use_id int, add parcel_id int, add unit_price double;
update buildings_01 b, parcels_01 p set b.parcel_id=p.parcel_id where b.blklot=p.blklot;
update buildings_01 b, building_use u set b.building_use_id=u.building_use_id where b.building_use <> 'resident'
       and b.building_use=u.building_use;
update buildings_01 b, building_use u set b.building_use_id=u.building_use_id where b.building_use = 'resident'
       and b.restype=u.building_use;


update buildings_01 set unit_price = (land_value + structure_value) / building_sqft where building_use <> 'resident'
       and building_sqft > 0;
update buildings_01 set unit_price = (land_value + structure_value) / residential_units where building_use = 'resident'
       and residential_units > 0;

update buildings_01 set unit_price = 0 where unit_price is null;
update buildings_01 set building_use_id = 0 where building_use_id is null;

#create second backup just to be sure...
drop table if exists buildings_backup_20070813_02;
create table buildings_backup_20070813_02 select * from buildings;

drop table if exists parcels_backup_20070813_02;
create table parcels_backup_20070813_02 select * from parcels;

drop table if exists buildings;
drop table if exists parcels;
create table buildings select * from buildings_01;
create table parcels select * from parcels_01;
