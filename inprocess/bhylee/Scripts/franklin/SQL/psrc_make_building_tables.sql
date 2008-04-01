

use psrc_2005_data_workspace;

#######################################
# Make temporary building types table #
#######################################

drop table if exists temp_buildings;
create table temp_buildings
     like psrc_2005_data_revised_2.building;
insert into temp_buildings
     select * 
     from psrc_2005_data_revised_2.building;
create index temp_buildings_gbt1 on temp_buildings (general_building_type_1);
create index temp_buildings_gbt1d on temp_buildings (general_building_type_1_description);
create index temp_buildings_gbt2 on temp_buildings (general_building_type_2);
create index temp_buildings_gbt2d on temp_buildings (general_building_type_2_description);

# Make the ID the primary key
alter table temp_buildings
     change building_id
            building_id int auto_increment;

# Assign blanks to "No Code"
update temp_buildings
     set general_building_type_1_description = "No Code",
         general_building_type_2_description = "other"
     where general_building_type_1 = 0;
# Make the auxiliary Mobile Home Park buildings Outbuildings
update temp_buildings
     set general_building_type_1_description = "Outbuilding",
         general_building_type_1 = 15
     where general_building_type_1_description = "Mobile Home Park";
# Make the Mobile Homes single family
update temp_buildings
     set general_building_type_2_description = "single family residential",
         general_building_type_2 = 1
     where general_building_type_1_description = "Mobile Home";
# Separate out government uses
update temp_buildings
     set general_building_type_2_description = "government",
         general_building_type_2 = 7
     where general_building_type_1_description = "Civic and Quasi-Public"
        or general_building_type_1_description = "Government"
        or general_building_type_1_description = "Hospital / Convalescent Center"
        or general_building_type_1_description = "Military";
# Change "No Code" codes to something else
update temp_buildings
     set general_building_type_1 = 23
     where general_building_type_1 = 0;
update temp_buildings
     set general_building_type_2 = 8
     where general_building_type_2 = 0;
# Correct multi-family codes
update temp_buildings
     set general_building_type_2 = 2
     where general_building_type_2_description = "multi-family residential";
# Shift down IDs
update temp_buildings
     set general_building_type_1 = general_building_type_1 - 1
     where general_building_type_1 >= 13;          

####################################
# Create a table of building types #
####################################

drop table if exists building_types;
create table building_types (
     building_type_id int,
     description varchar(50),
     generic_building_type_id int,
     generic_building_type_description varchar(50));

insert into building_types
     select distinct general_building_type_1, 
                     general_building_type_1_description, 
                     general_building_type_2, 
                     general_building_type_2_description 
     from temp_buildings
     order by general_building_type_1;

# Make the ID the primary key
alter table building_types
     add primary key (building_type_id);
alter table building_types
     change building_type_id
            building_type_id int auto_increment;

# Add an entry for "No Building" (remove this later)
insert into building_types (description, generic_building_type_id, generic_building_type_description)
     values ("No Building", 9, "no building");

# Create a table of generic building types

drop table if exists generic_building_types;
create table generic_building_types (
     generic_building_type_id int,
     description varchar(50));

insert into generic_building_types (generic_building_type_id, description)
     select distinct generic_building_type_id,
                     generic_building_type_description
     from building_types
     order by generic_building_type_id;

# Make the ID the primary key
alter table generic_building_types
     add primary key (generic_building_type_id);
alter table generic_building_types
     change generic_building_type_id
            generic_building_type_id int auto_increment;


########################
# Make buildings table #
########################

drop table if exists buildings;
create table buildings (
     building_id int(11) primary key,
     parcel_id int(10),
     outbuilding_flag int(3),
     building_sqft int(11),
     stories int(5),
     footprint_sqft int(11),
     year_built int(5),
     building_quality varchar(50),
     building_condition varchar(50),
     residential_units int(11),
     number_of_bedrooms int(3),
     number_of_bathrooms double(5,2),
     building_use varchar(50),
     building_use_description varchar(100),
     building_type_id int(5),
     building_type_description varchar(50),
     generic_building_type_id int(5),
     generic_building_type_description varchar(50),
     county_id int(5),
     county varchar(5),
     id_subparcel varchar(30),
     id_parcel varchar(28),
     subparcel_flag int(11),
     parcel_portion_sqft int(11),
     total_value int(11),
     tax_exempt int(1),
     zone_id int(5));

insert into buildings
     select building_id as building_id,
            parcel_id as parcel_id,
            outbuilding_flag as outbuilding_flag,
            building_sf as building_sqft,
            stories as stories,
            footprint as footprint_sqft,
            year_built as year_built,
            building_quality as building_quality,
            building_condition as building_condition,
            number_of_units as residential_units,
            bedrooms as number_of_bedrooms,
            bathrooms as number_of_bathrooms,
            building_use as building_use,
            building_use_description as building_use_description,
            general_building_type_1 as building_type_id,
            general_building_type_1_description as building_type_description,
            general_building_type_2 as generic_building_type_id,
            general_building_type_2_description as generic_building_type_description,
            NULL as county_id,
            county,
            id_subparcel as id_subparcel,
            id_parcel as id_parcel,
            subparcel_flag,
            area_portion as parcel_portion_sqft,
            value_portion as total_value,
            tax_exempt as tax_exempt,
            NULL as zone_id
     from temp_buildings;
            
alter table buildings
     change building_id
            building_id int auto_increment;



###########################################
# Add pseudo-buildings for "No Buildings" #
###########################################

# Create temporary table of parcels with buildings

drop table if exists temp_parcels_with_buildings;
create table temp_parcels_with_buildings
     select parcel_id, 
            count(*) as number_buildings
     from psrc_2005_data_revised_2.building
     group by parcel_id;

create index temp_parcels_with_buildings_parcel_id
     on temp_parcels_with_buildings (parcel_id);

drop table if exists temp_parcels_without_buildings;
create table temp_parcels_without_buildings
     select p.parcel_id as parcel_id,
            p.land_value_parcel as land_value_parcel,
            p.improvement_value_parcel as improvement_value_parcel,
            p.tax_exempt_flag as tax_exempt_flag,
            p.parcel_size_sf as parcel_size_sf,
            p.taz_id as taz_id,
            p.id_parcel as id_parcel,
            p.county as county,
            b.number_buildings as number_buildings
     from psrc_2005_data_revised_2.parcel as p
     left join temp_parcels_with_buildings as b
          on p.parcel_id=b.parcel_id;

create index temp_parcels_without_buildings_parcel_id
     on temp_parcels_without_buildings (parcel_id);

delete from temp_parcels_without_buildings
     where number_buildings is not null;

insert into buildings (parcel_id, outbuilding_flag, building_sqft, stories, 
                       year_built, building_quality, building_condition, 
                       residential_units, number_of_bedrooms, number_of_bathrooms,
                       building_use, building_use_description, building_type_id,
                       building_type_description, generic_building_type_id,
                       generic_building_type_description, county_id, county,
                       id_subparcel, id_parcel, subparcel_flag,
                       parcel_portion_sqft, total_value,
                       tax_exempt)
     select parcel_id as parcel_id,
            0 as outbuilding_flag,
            0 as building_sqft,
            0 as stories,
            NULL as year_built,
            NULL as building_quality,
            NULL as building_condition,
            0 as residential_units,
            0 as number_of_bedrooms,
            0 as number_of_bathrooms,
            NULL as building_use,
            NULL as building_use_description,
            23 as building_type_id,
            "No Building" as building_type_description,
            0 as generic_building_type_id,
            "no building" as generic_building_type_description,
            NULL as county_id,
            county as county,
            NULL as id_subparcel,
            id_parcel as id_parcel,
            NULL as subparcel_flag,
            parcel_size_sf as parcel_portion_sqft,
            land_value_parcel+improvement_value_parcel as total_value,
            tax_exempt_flag as tax_exempt
     from temp_parcels_without_buildings;


######################
# Make parcels table #
######################

drop table if exists parcels;
create table parcels (
     parcel_id int(10) primary key,
     land_value int(12),
     improvement_value int(12),
     total_value int(12),
     tax_exempt_flag int(5),
     parcel_sqft int(11),
     parcel_sqft_in_gis int(20),
     x_coord_sp double(15,5),
     y_coord_sp double(15,5),
     x_coord_utm double(15,5),
     y_coord_utm double(15,5),
     grid_id int(10),
     zone_id int(4),
     census_block varchar(20),
     city varchar(50),
     city_id int(5),
     is_inside_urban_growth_boundary int(1),
     county char(3),
     county_id int(5),
     id_parcel varchar(28),
     id_plat varchar(13),
     plan_type_id int(5),
     plan_type_description varchar(50));

insert into parcels
     select parcel_id as parcel_id,
            land_value_parcel as land_value,
            improvement_value_parcel as improvement_value,
            land_value_parcel+improvement_value_parcel as total_value,
            tax_exempt_flag as tax_exempt_flag,
            parcel_size_sf as parcel_sqft,
            parcel_size_sf_gis as parcel_sqft_in_gis,
            x_coord_sp as x_coord_sp,
            y_coord_sp as y_coord_sp,
            x_utm as x_coord_utm,
            y_utm as y_coord_utm,
            grid_id as grid_id,
            taz_id as zone_id,
            block_id as census_block,
            city as city,
            NULL as city_id,
            ugb_flag as is_inside_urban_growth_boundary,
            county as county,
            NULL as county_id,
            id_parcel as id_parcel,
            id_plat as id_plat,
            NULL as plan_type_id,
            NULL as plan_type_description
     from psrc_2005_data_revised_2.parcel;

alter table parcels
     change parcel_id
            parcel_id int auto_increment;

# Set up correspondence between comprehensive plan "desc"
# and new "GPT" plan_types, using R output

drop table if exists temp_comp_plan_types;
create table temp_comp_plan_types (
     comp_plan_id int(5),
     plan_type_id int(5),
     plan_type_description varchar(50));

create index comp_plan_types_comp_plan_id
     on temp_comp_plan_types (comp_plan_id);

insert into temp_comp_plan_types
     select distinct CPLANID as comp_plan_id,
                     GPTCODE as plan_type_id,
                     GPT as plan_type_description
     from parcel_plan_types
     order by CPLANID;

alter table all_parcels_merged_jpf
     add column (plan_type_id int(5),
                 plan_type_description varchar(50));

create index all_parcels_merged_comp_plan_id
     on all_parcels_merged_jpf (comp_plan_id);

drop table if exists all_parcel_plan_types;
create table all_parcel_plan_types
     select p.*,
            c.plan_type_id as plan_type_id,
            c.plan_type_description as plan_type_description
     from all_parcels_merged_jpf as p
     left join temp_comp_plan_types as c
          on p.comp_plan_id = c.comp_plan_id;

create index all_parcels_plan_types_id_parcel
     on all_parcel_plan_types (ID_PARCEL);

create index parcels_id_parcel
     on parcels (id_parcel);

drop table if exists parcels_with_plan_types;
create table parcels_with_plan_types
#explain
     select p.*,
            c.plan_type_id,
            c.plan_type_description
     from parcels as p
     left join all_parcel_plan_types as c
          on p.id_parcel = c.ID_PARCEL;

alter table parcels_with_plan_types
     change parcel_id
            parcel_id int primary key auto_increment;

# As a temporary fix, set null plan types to undevelopable
update parcels_with_plan_types
     set plan_type_id = 18,
         plan_type_description = "Undevelopable"
     where plan_type_id is null;

drop table if exists parcels;
rename table parcels_with_plan_types
     to parcels;

#############################
# Clean up temporary tables #
#############################

drop table if exists temp_buildings;
drop table if exists temp_parcels_with_buildings;
drop table if exists temp_parcels_without_buildings;
drop table if exists temp_comp_plan_types;
drop table if exists all_parcel_plan_types;
drop table if exists parcels_with_plan_types;

