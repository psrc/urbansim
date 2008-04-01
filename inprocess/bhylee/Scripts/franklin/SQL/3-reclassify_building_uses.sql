# This script adds, to the buildings table, some more general
# use classes and building types.

# Run this THIRD

use PSRC_2000_baseyear_joel;

update buildings
     set description=building_use
     where description="Imputed";
update buildings
     set description=building_use
     where description="BASEMENT UNFINISHED (703)";
update buildings
     set description=building_use
     where description="BASEMENT SEMIFINISHED (702)";
update buildings
     set description=building_use
     where description="BASEMENT FINISHED (701)";

drop table if exists building_uses;
create table building_uses
     (building_use_id int,
      description char(50),
      descforlookup char(50),
      generic char(50),
      type char(5),
      type_id int);
    
create index building_uses_index_building_use_id 
     on building_uses (building_use_id);
create index building_uses_index_description 
     on building_uses (description(50));

create index buildings_index_description
     on buildings (description(50));

load data infile 'building_uses.tab'
     into table building_uses
     (building_use_id, description, descforlookup, generic, type, type_id);     

drop table if exists buildings_new;
create table buildings_new
     (index index_building_id (building_id),
      index index_description (description(50)),
      index index_parcel_id (parcel_id),
      index index_building_use_id (building_use_id))
     select b.building_id as building_id, b.building_use as building_use, 
            b.description as description, b.year_built as year_built,
            b.county as county, b.built_sqft as built_sqft, 
            b.impute_flag as impute_flag, b.imputed_sqft as imputed_sqft, 
            b.parcel_code as parcel_code, b.parcel_id as parcel_id,
            b.building_use_id as building_use_id, u.generic as generic_use, 
            u.type as building_type, u.type_id as building_type_id
     from buildings as b
          left join building_uses as u
          on b.description=u.description;

delete from buildings_new
     where description is null and built_sqft=0;

drop table if exists buildings;
rename table buildings_new
     to buildings;

# also create new building_types table

drop table if exists building_types;
create table building_types
     select * from GSPSRC_2000_baseyear_change_20060926.building_types;

alter table building_types
     add building_type char(5);

update building_types set building_type = "C" where building_type_id = 1;
update building_types set building_type = "G" where building_type_id = 2;
update building_types set building_type = "I" where building_type_id = 3;
update building_types set building_type = "R" where building_type_id = 4;

insert into building_types 
          (building_type, building_type_id, name, units, is_residential)
     values    (  "SF",     5,   "single-family residential",    "residential_units",     1),
               (  "MF",     6,   "multi-family residential",     "residential_units",     1),
               (  "GQ",     7,   "group quarters",               "residential_units",     1);
