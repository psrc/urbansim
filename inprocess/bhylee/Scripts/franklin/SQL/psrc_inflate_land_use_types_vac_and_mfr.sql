
########################################################
# This script inflates the number of land use types to #
# split out Vacant into Developable and Undevelopable, #
# and split out MFR into Condo and Apartment. Requires #
# Parcel data with columns for land use type and       #
# plan type, and the Land Use type table.              #
########################################################

use psrc_2005_data_workspace;



# Modify land_use_types table

# Need to do this in a temporary table to satisfy primary key:
drop table if exists temp_land_use_types;
create temporary table temp_land_use_types
     select * from land_use_types;

update temp_land_use_types
     set land_use_type_id = land_use_type_id + 1
     where land_use_type_id > 14;
update temp_land_use_types
     set land_use_type_id = land_use_type_id + 1
     where land_use_type_id > 26;

# Edit existing codes:
update temp_land_use_types
     set description = "Multi-Family Residential",
         unit_name = "residential_units"
     where land_use_type_id = 14;
update temp_land_use_types
     set description = "Vacant Developable",
         unit_name = "parcel_sqft"
     where land_use_type_id = 26;

# Insert new codes
insert into temp_land_use_types values
     (15, "Condo Residential", "multi-family residential", "residential_units"),
     (27, "Vacant Undevelopable", "vacant", "parcel_sqft");

delete from land_use_types; # CAREFUL HERE - BE SURE YOU'RE READY TO DO THIS
insert into land_use_types
     select * from temp_land_use_types
     order by land_use_type_id;

drop table if exists temp_land_use_types;

# Now update the parcel data

# Move up the existing land use codes:
update parcels
     set land_use_type_id = land_use_type_id + 1
     where land_use_type_id > 14;
update parcels
     set land_use_type_id = land_use_type_id + 1
     where land_use_type_id > 26;

# Update vacant undevelopable based on plan_type_description:
update parcels
     set land_use_type_id = 27
     where land_use_type_id = 26
       and plan_type_id = 18;

# For MFR, need to go back to the land use reclassification,
# modify it, and re-join to parcels

# Update land use reclassification table:
update land_use_generic_reclass_2005
     set generic_land_use_1 = "Condo Residential"
     where land_use_description like "%Condominium(Residential)%"
        or land_use_description like "%Condominium(Mixed Use)%"
        or land_use_description like "%Condominium(M Home Pk)%"
        or land_use_description like "%Condo, residential%"
        or land_use_description like "%SFR Condominium Detached%"
        or land_use_description like "%SFR Condominium CommonWall%"
        or land_use_description like "%SFR Condominium MFR%"
        or land_use_description like "%SFR Condominium Project%";

# Make integer codes for join matching and add indices:
alter table land_use_generic_reclass_2005
     add column (county_num int,
                 county_land_use_code_num int);

update land_use_generic_reclass_2005
     set county_num = cast(county as unsigned),
         county_land_use_code_num = cast(county_land_use_code as unsigned);

create index lu_reclass_co_lu_code
     on land_use_generic_reclass_2005 (county_num, county_land_use_code_num);

alter table all_parcels_gis
     add column (county_num int,
                 county_land_use_code_num int);

update all_parcels_gis
     set county_num = cast(county as unsigned),
         county_land_use_code_num = cast(Land_Use as unsigned);

create index all_parcels_gis_co_lu_code
     on all_parcels_gis (county_num, county_land_use_code_num);

# Join to create land use classifications by parcel:
drop table if exists temp_parcel_land_use;
create temporary table temp_parcel_land_use
     select p.ID_PARCEL,
            l.generic_land_use_1
     from all_parcels_gis as p
     left join land_use_generic_reclass_2005 l
          on p.county_num = l.county_num
         and p.county_land_use_code_num = l.county_land_use_code_num;

create index tmp_glu_ID_PARCEL on temp_parcel_land_use (ID_PARCEL);
create index tmp_glu_glu on temp_parcel_land_use (generic_land_use_1);
create index parcels_glu on parcels (GenericLandUse1);

# Update parcel records based on that temp table
update parcels p, temp_parcel_land_use l
     set p.GenericLandUse1 = "Condo Residential",
         p.land_use_type_id = 15
     where p.id_parcel = l.ID_PARCEL
       and l.generic_land_use_1 = "Condo Residential";

# Drop the temp table
drop table if exists temp_parcel_land_use;

# Done!
