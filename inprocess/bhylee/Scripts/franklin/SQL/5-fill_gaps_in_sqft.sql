

# Run this FIFTH

use PSRC_2000_baseyear_joel;

alter table pseudo_buildings
     add bldg_lot_area_impute_flag int(1);

create index index_building_type
     on pseudo_buildings (building_type);

# impute lot areas for buildings whose floor areas
# are known, but floor areas for other buildings on
# the parcel are not known
update pseudo_buildings as b, floor_area_ratios as far
     set  b.bldg_lot_area = b.built_sqft / far.far,
          b.bldg_lot_area_impute_flag = 1
     where     b.bldg_lot_area is null
          and  b.built_sqft is not null
          and  b.building_type = far.building_type;

# aggregate to parcel for known-so-far totals

drop table if exists pseudo_buildings_on_parcels;
create table pseudo_buildings_on_parcels
     select    parcel_id,
               sum(built_sqft) as built_sqft_kn,
               sum(bldg_lot_area) as lot_sqft_kn
     from pseudo_buildings
     where built_sqft is not null
     group by parcel_id;

create index index_parcel_id
     on pseudo_buildings_on_parcels (parcel_id);


# attach to parcels table

drop table if exists parcels_new;
create table parcels_new
     select    p.*,
               b.built_sqft_kn as built_sqft_kn,
               b.lot_sqft_kn as lot_sqft_kn
     from parcels as p
     left join pseudo_buildings_on_parcels as b
          on p.parcel_id = b.parcel_id;

create index index_parcel_id
     on parcels_new (parcel_id);

drop table if exists parcels;
rename table parcels_new
     to parcels;

# aggregate to parcel the proxy-size of unknown buildings

alter table pseudo_buildings
     add proxy_size int(11);

update pseudo_buildings as b, floor_area_ratios as f
     set b.proxy_size = f.avg_sqft
     where     b.building_type=f.building_type
           and b.built_sqft is null;

drop table if exists unknowns_on_parcels;
create table unknowns_on_parcels
     select    parcel_id,
               count(*) as num_unkn_bldgs,
               sum(proxy_size) as built_sqft_unkn
     from pseudo_buildings
     where built_sqft is null
     group by parcel_id;

create index index_parcel_id
     on unknowns_on_parcels (parcel_id);

# attach to parcels table

drop table if exists parcels_new;
create table parcels_new
     select    p.*,
               u.num_unkn_bldgs as num_unkn_bldgs,
               u.built_sqft_unkn as built_sqft_unkn
     from parcels as p
     left join unknowns_on_parcels as u
          on p.parcel_id = u.parcel_id;

create index index_parcel_id
     on parcels_new (parcel_id);

drop table if exists parcels;
rename table parcels_new
     to parcels;


# impute lot size for pseudo-buildings

update parcels
     set built_sqft_kn = 0
     where built_sqft_kn is null;
update parcels
     set lot_sqft_kn = 0
     where lot_sqft_kn is null;


alter table pseudo_buildings
     add built_sqft_impute_flag int(1);

update pseudo_buildings as b, parcels as p
     set  b.bldg_lot_area = (p.lot_sqft - p.lot_sqft_kn) * (b.proxy_size / p.built_sqft_unkn),
          b.bldg_lot_area_impute_flag = 1
     where     b.parcel_id = p.parcel_id
           and b.bldg_lot_area is null;

# impute building size
update pseudo_buildings 
     set built_sqft_impute_flag = NULL,
         built_sqft = NULL
     where built_sqft_impute_flag = 1; # delete

update pseudo_buildings as b, floor_area_ratios as far
     set  b.built_sqft = b.bldg_lot_area * far.far,
          b.built_sqft_impute_flag = 1
     where     b.building_type = far.building_type
           and b.built_sqft is null;
