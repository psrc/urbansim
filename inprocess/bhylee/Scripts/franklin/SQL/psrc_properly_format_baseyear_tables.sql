

use psrc_2005_parcel_baseyear_start;


alter table buildings
     change footprint_sqft
          land_area int(11),
     add non_residential_sqft int(11),
     add sqft_per_unit int(11),
     change id_parcel
          assessors_parcel_id varchar(28),
     add building_quality_type_id int;

# Do calcs for non-residential buildings:
update buildings
     set non_residential_sqft = building_sqft,
         sqft_per_unit = 0
     where residential_units = 0;

# Do calcs for residential buildings:
update buildings
     set non_residential_sqft = 0,
         sqft_per_unit = building_sqft / residential_units
     where residential_units > 0;

# Do calcs for mixed-use buildings:
update buildings
     set non_residential_sqft = building_sqft * (2/stories)
     where stories > 10 # very tall buildings
       and building_type_id = 10;
update buildings
     set non_residential_sqft = building_sqft * (1/stories)
     where stories > 1 and stories <= 10 # multi-storey buildings
       and building_type_id = 10;
update buildings
     set non_residential_sqft = building_sqft / 2
     where stories = 1 # one-story-buildings
       and building_type_id = 10;
update buildings
     set sqft_per_unit = (building_sqft - non_residential_sqft) / residential_units
     where residential_units > 0
       and building_type_id = 10;

# Create table of building quality levels

drop table if exists building_qualities;
create table building_qualities (
     building_quality_id int primary key auto_increment,
     building_quality_name varchar(20));

create index building_qualities_names
     on building_qualities (building_quality_name);

insert into building_qualities (building_quality_name)
     select distinct building_quality
     from buildings
     order by building_quality;

create index buildings_building_quality
     on buildings (building_quality);

update buildings as b, building_qualities as q
     set b.building_quality_id = q.building_quality_id
     where b.building_quality = q.building_quality_name;

alter table buildings
     drop outbuilding_flag,
     drop building_quality,
     drop building_condition,
     drop number_of_bedrooms,
     drop number_of_bathrooms,
     drop building_use,
     drop building_use_description,
     drop building_type_description,
     drop generic_building_type_id,
     drop generic_building_type_description,
     drop id_subparcel,
     drop county,
     drop subparcel_flag,
     drop attributed_parcel_sqft,
     drop is_duplicate,
     drop total_value;
     

building_quality <- put in lookup


alter table buildings
     change building_quality_type_id
          building_quality_id int;


# Restore building_sqft

alter table buildings
     add building_sqft int(11);

update buildings
     set building_sqft = non_residential_sqft + residential_units * sqft_per_unit;
