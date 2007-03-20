---
##there is no restype field, residence couldnt be classified to residential building use type
create table parcels_98 select
blklot as mapblklot, blklot, block_num, lot_num, from_ as from_st, to_ as to_st, streetname as street_name, type as street_type, odd_even,
'' as neighorhood, null as taz, use_type as use_type, landuse, 0.0 as land_value,
zoning, height_lim as heightlimit, allowfar as far_allowed, null as census_tract, shape_length as perimeter, shape_area as area
from luse98;

create table buildings_98 select
blklot as mapblklot, blklot, landuse as building_use, '' as restype, 0.0 as structure_value,
stories, resunits as residential_units, 0 as bedrooms, bldg_sqft as building_sqft, 0 as year_built,
bldg_sqft as total_uses, 0 as cie, 0 as med, 0 as mips, 0 as retail, 0 as pdr, 0 as visitor
from luse98;

create index blklot_index on parcels_98 (blklot);
create index blklot_index on buildings_98 (blklot);

alter table parcels_98 add parcel_id int;
alter table buildings_98 add building_id int;

update parcels_98 p1, parcels_00 p0 set p1.parcel_id=p0.parcel_id where p0.blklot=p1.blklot;
update buildings_98 b1, buildings_00 b0 set b1.building_id=b0.building_id where b0.blklot=b1.blklot;

alter table buildings_98 add building_use_id int, add parcel_id int, add sale_price int, add unit_price double;
update buildings_98 b, parcels_98 p set b.parcel_id=p.parcel_id where b.blklot=p.blklot;
update buildings_98 b, building_use u set b.building_use_id=u.building_use_id where b.building_use <> 'residential'
       and b.building_use=u.building_use;
update buildings_98 b, building_use u set b.building_use_id=u.building_use_id where b.building_use = 'residential'
       and b.restype=u.building_use;
update buildings_98 b, assessors_data.sales06 s set b.sale_price=s.sale_price where b.blklot=s.blklot and s.sale_year=1998;
update buildings_98 set unit_price = sale_price / building_sqft where building_use <> 'residential'
       and building_sqft > 0;
update buildings_98 set unit_price = sale_price / residential_units where building_use = 'residential'
       and residential_units > 0;

---

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
update buildings_00 b, assessors_data.sales06 s set b.sale_price=s.sale_price where b.blklot=s.blklot and s.sale_year=2000;
update buildings_00 set unit_price = sale_price / building_sqft where building_use <> 'resident'
       and building_sqft > 0;
update buildings_00 set unit_price = sale_price / residential_units where building_use = 'resident'
       and residential_units > 0;

---
create table parcels_01 select
mapblklot, mapblklot as blklot, block_num, lot_num, from_st, to_st, street as street_name, type as street_type, odd_even,
'' as neighorhood, taz, dbiusetype as use_type, landuse, land_val as land_value,
zoning, height_lim as heightlimit, far as far_allowed, census_tra as census_tract, shape_length as perimeter, shape_area as area
from luse01;

create table buildings_01 select
mapblklot, mapblklot as blklot, landuse as building_use, restype, struc_val as structure_value,
stories, resunits as residential_units, null as bedrooms, bldg_sqft as building_sqft, yr_built as year_built,
totalusesq as total_uses, cie, med, mips, retail_ent as retail, pdr, visitor
from luse01;

create index blklot_index on parcels_01 (blklot);
create index blklot_index on buildings_01 (blklot);

alter table parcels_01 add parcel_id int;
alter table buildings_01 add building_id int;

update parcels_01 p1, parcels_00 p0 set p1.parcel_id=p0.parcel_id where p0.blklot=p1.blklot;
update buildings_01 b1, buildings_00 b0 set b1.building_id=b0.building_id where b0.blklot=b1.blklot;

alter table buildings_01 add building_use_id int, add parcel_id int, add sale_price int, add unit_price double;
update buildings_01 b, parcels_01 p set b.parcel_id=p.parcel_id where b.blklot=p.blklot;
update buildings_01 b, building_use u set b.building_use_id=u.building_use_id where b.building_use <> 'resident'
       and b.building_use=u.building_use;
update buildings_01 b, building_use u set b.building_use_id=u.building_use_id where b.building_use = 'resident'
       and b.restype=u.building_use;
update buildings_01 b, assessors_data.sales06 s set b.sale_price=s.sale_price where b.blklot=s.blklot and s.sale_year=2001;
update buildings_01 set unit_price = sale_price / building_sqft where building_use <> 'resident'
       and building_sqft > 0;
update buildings_01 set unit_price = sale_price / residential_units where building_use = 'resident'
       and residential_units > 0;

---
create table parcels_02 select
mapblklot, blklot, block_num, lot_num, from_st, to_st, street as street_name, type as street_type, '' as odd_even,
neighborho as neighorhood, newtaz as taz, usetype as use_type, landuse, landval as land_value,
zoning, heightlimi as heightlimit, 0.0 as far_allowed, censustrac as census_tract, 
shape_length as perimeter, shape_area as area
from luse02;

create table buildings_02 select
mapblklot, blklot, landuse as building_use, restype, strucval as structure_value,
stories, resunits as residential_units, bdrms as bedrooms, bldgsqft as building_sqft, yrbuilt as year_built,
total_uses as total_uses, cie, 0 as med, mips, retail, pdr, 0 as visitor
from luse02;

create index blklot_index on parcels_02 (blklot);
create index blklot_index on buildings_02 (blklot);

alter table parcels_02 add parcel_id int;
alter table buildings_02 add building_id int;

update parcels_02 p2, parcels_00 p0 set p2.parcel_id=p0.parcel_id where p0.blklot=p2.blklot;
update buildings_02 b2, buildings_00 b0 set b2.building_id=b0.building_id where b0.blklot=b2.blklot;

alter table buildings_02 add building_use_id int, add parcel_id int, add sale_price int, add unit_price double;
update buildings_02 b, parcels_02 p set b.parcel_id=p.parcel_id where b.blklot=p.blklot;
update buildings_02 b, building_use u set b.building_use_id=u.building_use_id where b.building_use <> 'resident'
       and b.building_use=u.building_use;
update buildings_02 b, building_use u set b.building_use_id=u.building_use_id where b.building_use = 'resident'
       and b.restype=u.building_use;
update buildings_02 b, assessors_data.sales06 s set b.sale_price=s.sale_price where b.blklot=s.blklot and s.sale_year=2002;
update buildings_02 set unit_price = sale_price / building_sqft where building_use <> 'resident'
       and building_sqft > 0;
update buildings_02 set unit_price = sale_price / residential_units where building_use = 'resident'
       and residential_units > 0;

---
create table parcels_03 select
mapblklot, blklot, block_num, lot_num, from_st, to_st, street as street_name, type as street_type, '' as odd_even,
newneighbo as neighorhood, newtaz as taz, usetype as use_type, landuse, landval as land_value,
zoning, heightlimi as heightlimit, 0.0 as far_allowed, censustrac as census_tract, 
shape_length as perimeter, shape_area as area
from luse03;

create table buildings_03 select
mapblklot, blklot, landuse as building_use, restype, strucval as structure_value,
stories, resunits as residential_units, bdrms as bedrooms, bldgsqft as building_sqft, yrbuilt as year_built,
total_uses as total_uses, cie, 0 as med, mips, retail, pdr, 0 as visitor
from luse03;

create index blklot_index on parcels_03 (blklot);
create index blklot_index on buildings_03 (blklot);

alter table parcels_03 add parcel_id int;
alter table buildings_03 add building_id int;

update parcels_03 p3, parcels_00 p0 set p3.parcel_id=p0.parcel_id where p0.blklot=p3.blklot;
update buildings_03 b3, buildings_00 b0 set b3.building_id=b0.building_id where b0.blklot=b3.blklot;


alter table buildings_03 add building_use_id int, add parcel_id int, add sale_price int, add unit_price double;
update buildings_03 b, parcels_03 p set b.parcel_id=p.parcel_id where b.blklot=p.blklot;
update buildings_03 b, building_use u set b.building_use_id=u.building_use_id where b.building_use <> 'resident'
       and b.building_use=u.building_use;
update buildings_03 b, building_use u set b.building_use_id=u.building_use_id where b.building_use = 'resident'
       and b.restype=u.building_use;
update buildings_03 b, assessors_data.sales06 s set b.sale_price=s.sale_price where b.blklot=s.blklot and s.sale_year=2003;
update buildings_03 set unit_price = sale_price / building_sqft where building_use <> 'resident'
       and building_sqft > 0;
update buildings_03 set unit_price = sale_price / residential_units where building_use = 'resident'
       and residential_units > 0;

---
create table parcels_04 select
mapblklot, blklot, block_num, lot_num, from_st, to_st, street as street_name, st_type as street_type, '' as odd_even,
neighborho as neighorhood, taz as taz, usetype as use_type, landuse, landval as land_value,
zoning, heightlimi as heightlimit, 0.0 as far_allowed, censustrac as census_tract, 
shape_length as perimeter, shape_area as area
from luse04;

create table buildings_04 select
mapblklot, blklot, landuse as building_use, restype, strucval as structure_value,
stories, resunits as residential_units, bdrms as bedrooms, bldgsqft as building_sqft, yrbuilt as year_built,
total_uses as total_uses, cie, med, mips, retail, pdr, visitor
from luse04;

create index blklot_index on parcels_04 (blklot);
create index blklot_index on buildings_04 (blklot);

alter table parcels_04 add parcel_id int;
alter table buildings_04 add building_id int;

update parcels_04 p4, parcels_00 p0 set p4.parcel_id=p0.parcel_id where p0.blklot=p4.blklot;
update buildings_04 b4, buildings_00 b0 set b4.building_id=b0.building_id where b0.blklot=b4.blklot;


alter table buildings_04 add building_use_id int, add parcel_id int, add sale_price int, add unit_price double;
update buildings_04 b, parcels_04 p set b.parcel_id=p.parcel_id where b.blklot=p.blklot;
update buildings_04 b, building_use u set b.building_use_id=u.building_use_id where b.building_use <> 'resident'
       and b.building_use=u.building_use;
update buildings_04 b, building_use u set b.building_use_id=u.building_use_id where b.building_use = 'resident'
       and b.restype=u.building_use;
update buildings_04 b, assessors_data.sales06 s set b.sale_price=s.sale_price where b.blklot=s.blklot and s.sale_year=2004;
update buildings_04 set unit_price = sale_price / building_sqft where building_use <> 'resident'
       and building_sqft > 0;
update buildings_04 set unit_price = sale_price / residential_units where building_use = 'resident'
       and residential_units > 0;

---
create table parcels_05 select
mapblklot, blklot, block_num, lot_num, from_st, to_st, street as street_name, st_type as street_type, odd_even,
neighborho as neighorhood, taz, usetype as use_type, landuse, landval as land_value,
zoning, heightlimi as heightlimit, null as FAR_ALLOWD, censustrac as census_tract, shape_length, shape_area
from luse05;

create table buildings_05 select
mapblklot, blklot, landuse as building_use, restype, strucval as structure_value,
stories, resunits as residential_units, bdrms as bedrooms, bldgsqft as building_sqft, yrbuilt as year_built,
total_uses, cie, med, mips, retail, pdr, visitor
from luse05;

create index blklot_index on parcels_05 (blklot);
create index blklot_index on buildings_05 (blklot);

alter table parcels_05 add parcel_id int;
alter table buildings_05 add building_id int;

update parcels_05 p5, parcels_00 p0 set p5.parcel_id=p0.parcel_id where p0.blklot=p5.blklot;
update buildings_05 b5, buildings_00 b0 set b5.building_id=b0.building_id where b0.blklot=b5.blklot;


alter table buildings_05 add building_use_id int, add parcel_id int, add sale_price int, add unit_price double;
update buildings_05 b, parcels_05 p set b.parcel_id=p.parcel_id where b.blklot=p.blklot;
update buildings_05 b, building_use u set b.building_use_id=u.building_use_id where b.building_use <> 'resident'
       and b.building_use=u.building_use;
update buildings_05 b, building_use u set b.building_use_id=u.building_use_id where b.building_use = 'resident'
       and b.restype=u.building_use;
update buildings_05 b, assessors_data.sales06 s set b.sale_price=s.sale_price where b.blklot=s.blklot and s.sale_year=2005;
update buildings_05 set unit_price = sale_price / building_sqft where building_use <> 'resident'
       and building_sqft > 0;
update buildings_05 set unit_price = sale_price / residential_units where building_use = 'resident'
       and residential_units > 0;
