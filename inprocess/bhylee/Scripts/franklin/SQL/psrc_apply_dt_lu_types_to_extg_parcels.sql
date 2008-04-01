
# This script applies land use types to parcels on 
# the basis of the contents of their buildings, 
# mirroring the land use types used in the 
# development templates.

# Use a working database

use psrc_2005_data_workspace_franklin;

# Create new land use types table

drop table if exists land_use_types_new;
create table land_use_types_new (
     land_use_type_id int primary key auto_increment,
     description varchar(50) not null,
     land_use_name varchar(64),
     unit_name varchar(32));

create index lu_types_name
     on land_use_types_new (land_use_name);

insert into land_use_types_new (land_use_name, unit_name)
     select distinct development_type,
            density_type
     from psrc_2005_parcel_baseyear_start.development_templates
     order by development_type;

insert into land_use_types_new (land_use_name, unit_name) values
     ("gov", "far"),
     ("other", "far"),
     ("vacant", "1");

delete from land_use_types_new
     where land_use_name = "sfr_plat";

update land_use_types_new
     set land_use_name = "sfr"
     where land_use_name = "sfr_parcel";


# Add building data for land use type categories

drop table if exists buildings;
create table buildings
     like psrc_2005_parcel_baseyear_start.buildings;
insert into buildings
     select * from psrc_2005_parcel_baseyear_start.buildings;

alter table buildings
     add sqft_com int,
     add sqft_off int,
     add sqft_ind int,
     add sqft_tcu int,
     add sqft_war int,
     add sqft_gov int,
     add sqft_oth int,
     add units_sfr int,
     add units_mfa int,
     add units_mfc int,
     add is_vacant int;

update buildings
     set sqft_com = 0, sqft_off = 0, sqft_ind = 0, sqft_tcu = 0, 
         sqft_war = 0, sqft_gov = 0, sqft_oth = 0,
         units_sfr = 0, units_mfa = 0, units_mfc = 0,
         is_vacant = 0;

update buildings
     set sqft_oth = non_residential_sqft
     where building_type_id = 1; # Agr
update buildings
     set sqft_gov = non_residential_sqft
     where building_type_id = 2; # Civ
update buildings
     set sqft_com = non_residential_sqft
     where building_type_id = 3; # Com
update buildings
     set units_mfc = residential_units
     where building_type_id = 4; # Con
update buildings
     set sqft_gov = non_residential_sqft
     where building_type_id = 5; # Gov
update buildings
     set sqft_oth = non_residential_sqft
     where building_type_id = 6; # GQ
update buildings
     set sqft_gov = non_residential_sqft
     where building_type_id = 7; # Hos
update buildings
     set sqft_ind = non_residential_sqft
     where building_type_id = 8; # Ind
update buildings
     set sqft_gov = non_residential_sqft
     where building_type_id = 9; # Mil
update buildings
     set sqft_com = non_residential_sqft,
         units_mfc = residential_units
     where building_type_id = 10; # Mix
update buildings
     set units_sfr = residential_units
     where building_type_id = 11; # Mob
update buildings
     set units_mfa = residential_units
     where building_type_id = 12; # Apt
update buildings
     set sqft_off = non_residential_sqft
     where building_type_id = 13; # Off
update buildings
     set sqft_oth = 0
     where building_type_id = 14; # Out
update buildings
     set sqft_oth = non_residential_sqft
     where building_type_id = 15; # POS
update buildings
     set sqft_oth = 0
     where building_type_id = 16; # Pkg
update buildings
     set sqft_oth = non_residential_sqft
     where building_type_id = 17; # Rec
update buildings
     set sqft_gov = non_residential_sqft
     where building_type_id = 18; # Sch
update buildings
     set units_sfr = residential_units
     where building_type_id = 19; # SFR
update buildings
     set sqft_tcu = non_residential_sqft,
         units_mfc = residential_units
     where building_type_id = 20; # TCU
update buildings
     set sqft_war = non_residential_sqft,
         units_mfc = residential_units
     where building_type_id = 21; # War
update buildings
     set sqft_oth = non_residential_sqft
     where building_type_id = 22; # No Code
update buildings
     set is_vacant = 1
     where building_type_id = 23; # Vacant

# Aggregate building data for each parcel

drop table if exists parcel_buildings;
create table parcel_buildings
     select parcel_id,
            sum(sqft_com) as sqft_com,
            sum(sqft_off) as sqft_off,
            sum(sqft_ind) as sqft_ind,
            sum(sqft_tcu) as sqft_tcu,
            sum(sqft_war) as sqft_war,
            sum(sqft_com+sqft_off+sqft_ind+sqft_tcu+sqft_war) as sqft_nonres,
            sum(sqft_gov) as sqft_gov,
            sum(residential_units*sqft_per_unit) as sqft_res,
            sum(sqft_com+sqft_off+sqft_ind+sqft_tcu+sqft_war+sqft_gov+
                residential_units*sqft_per_unit) as building_sqft,
            sum(sqft_oth) as sqft_oth,
            sum(units_sfr) as units_sfr,
            sum(units_mfa) as units_mfa,
            sum(units_mfc) as units_mfc,
            -1 as is_mixed_use,
            -1 as mix_com_ind,
            -1 as mix_com_off,
            -1 as mix_com_ware,
            -1 as mix_off_ind,
            -1 as mix_off_ware,
            -1 as mix_ind_ware,
            -1 as mix_com_res,
            -1 as mix_off_res,
            -1 as mix_ware_res,
            "not assigned yet" as land_use_type_name_1,
            "not assigned yet" as land_use_type_name_2,
            "not assigned yet" as land_use_name,
            -1 as land_use_type_id
     from buildings
     group by parcel_id;

create index parcel_buildings_parcel_id
     on parcel_buildings (parcel_id);
create index parcel_buildings_lu_name
     on parcel_buildings (land_use_name);

# Classify mixed-use parcels if there is no
# dominant building type (i.e. > 85%)

# Start with the assumption of mixed use...
update parcel_buildings
     set is_mixed_use = 1;

#...and disprove by looking for dominant uses...
update parcel_buildings
     set is_mixed_use = 0
     where 100*sqft_com/sqft_nonres > 85
        or 100*sqft_off/sqft_nonres > 85
        or 100*sqft_ind/sqft_nonres > 85
        or 100*sqft_tcu/sqft_nonres > 85
        or 100*sqft_war/sqft_nonres > 85;
update parcel_buildings
     set is_mixed_use = 0
     where sqft_nonres = 0;

#...yet, make an exception for nonres/res combos:
update parcel_buildings
     set is_mixed_use = 1
     where sqft_nonres > 0
       and sqft_res > 0;

# Now classify the mixed-use parcels

# Find #1 use:
update parcel_buildings
     set land_use_type_name_1 = "com"
     where sqft_com > 0
       and sqft_com >= sqft_off
       and sqft_com >= sqft_ind
       and sqft_com >= sqft_tcu
       and sqft_com >= sqft_war
       and sqft_com >= sqft_res;
update parcel_buildings
     set land_use_type_name_1 = "off"
     where sqft_off > 0
       and sqft_off >  sqft_com
       and sqft_off >= sqft_ind
       and sqft_off >= sqft_tcu
       and sqft_off >= sqft_war
       and sqft_off >= sqft_res;
update parcel_buildings
     set land_use_type_name_1 = "ind"
     where sqft_ind > 0
       and sqft_ind >  sqft_off
       and sqft_ind >  sqft_com
       and sqft_ind >= sqft_tcu
       and sqft_ind >= sqft_war
       and sqft_ind >= sqft_res;
update parcel_buildings
     set land_use_type_name_1 = "tcu"
     where sqft_tcu > 0
       and sqft_tcu >  sqft_off
       and sqft_tcu >  sqft_ind
       and sqft_tcu >  sqft_com
       and sqft_tcu >= sqft_war
       and sqft_tcu >= sqft_res;
update parcel_buildings
     set land_use_type_name_1 = "ware"
     where sqft_war > 0
       and sqft_war >  sqft_off
       and sqft_war >  sqft_ind
       and sqft_war >  sqft_tcu
       and sqft_war >  sqft_com
       and sqft_war >= sqft_res;
update parcel_buildings
     set land_use_type_name_1 = "res"
     where sqft_res > 0
       and sqft_res >  sqft_off
       and sqft_res >  sqft_ind
       and sqft_res >  sqft_tcu
       and sqft_res >  sqft_com
       and sqft_res >  sqft_war;
update parcel_buildings
     set land_use_type_name_1 = "gov",
         is_mixed_use = 0
     where sqft_gov > 0;
update parcel_buildings
     set land_use_type_name_1 = "oth",
         is_mixed_use = 0
     where land_use_type_name_1 = "not assigned yet";
update parcel_buildings
     set land_use_type_name_1 = "vac",
         is_mixed_use = 0
     where building_sqft + sqft_oth = 0;

# Find #2 use:
update parcel_buildings
     set land_use_type_name_2 = "com"
     where (land_use_type_name_1 = "off" and sqft_com>0 and sqft_com>=sqft_ind and sqft_com>=sqft_tcu and sqft_com>=sqft_war)
        or (land_use_type_name_1 = "ind" and sqft_com>0 and sqft_com>=sqft_off and sqft_com>=sqft_tcu and sqft_com>=sqft_war)
        or (land_use_type_name_1 = "tcu" and sqft_com>0 and sqft_com>=sqft_off and sqft_com>=sqft_ind and sqft_com>=sqft_war)
        or (land_use_type_name_1 = "ware" and sqft_com>0 and sqft_com>=sqft_off and sqft_com>=sqft_ind and sqft_com>=sqft_tcu)
        or (land_use_type_name_1 = "res" and sqft_com>0 and sqft_com>=sqft_off and sqft_com>=sqft_ind and sqft_com>=sqft_tcu and sqft_com>=sqft_war);
update parcel_buildings
     set land_use_type_name_2 = "off"
     where (land_use_type_name_1 = "com" and sqft_off>0 and sqft_off>=sqft_ind and sqft_off>=sqft_tcu and sqft_off>=sqft_war)
        or (land_use_type_name_1 = "ind" and sqft_off>0 and sqft_off>sqft_com and sqft_off>=sqft_tcu and sqft_off>=sqft_war)
        or (land_use_type_name_1 = "tcu" and sqft_off>0 and sqft_off>sqft_com and sqft_off>=sqft_ind and sqft_off>=sqft_war)
        or (land_use_type_name_1 = "ware" and sqft_off>0 and sqft_off>sqft_com and sqft_off>=sqft_ind and sqft_off>=sqft_tcu)
        or (land_use_type_name_1 = "res" and sqft_off>0 and sqft_off>sqft_com and sqft_off>=sqft_ind and sqft_off>=sqft_tcu and sqft_off>=sqft_war);
update parcel_buildings
     set land_use_type_name_2 = "ind"
     where (land_use_type_name_1 = "off" and sqft_ind>0 and sqft_ind>sqft_com and sqft_ind>=sqft_tcu and sqft_ind>=sqft_war)
        or (land_use_type_name_1 = "com" and sqft_ind>0 and sqft_ind>sqft_off and sqft_ind>=sqft_tcu and sqft_ind>=sqft_war)
        or (land_use_type_name_1 = "tcu" and sqft_ind>0 and sqft_ind>sqft_off and sqft_ind>sqft_com and sqft_ind>=sqft_war)
        or (land_use_type_name_1 = "ware" and sqft_ind>0 and sqft_ind>sqft_off and sqft_ind>sqft_com and sqft_ind>=sqft_tcu)
        or (land_use_type_name_1 = "res" and sqft_ind>0 and sqft_ind>sqft_off and sqft_ind>sqft_com and sqft_ind>=sqft_tcu and sqft_ind>=sqft_war);
update parcel_buildings
     set land_use_type_name_2 = "tcu"
     where (land_use_type_name_1 = "off" and sqft_tcu>0 and sqft_tcu>sqft_ind and sqft_tcu>sqft_com and sqft_tcu>=sqft_war)
        or (land_use_type_name_1 = "ind" and sqft_tcu>0 and sqft_tcu>sqft_off and sqft_tcu>sqft_com and sqft_tcu>=sqft_war)
        or (land_use_type_name_1 = "com" and sqft_tcu>0 and sqft_tcu>sqft_off and sqft_tcu>sqft_ind and sqft_tcu>=sqft_war)
        or (land_use_type_name_1 = "ware" and sqft_tcu>0 and sqft_tcu>sqft_off and sqft_tcu>sqft_ind and sqft_tcu>sqft_com)
        or (land_use_type_name_1 = "res" and sqft_tcu>0 and sqft_tcu>sqft_off and sqft_tcu>sqft_ind and sqft_tcu>sqft_com and sqft_tcu>=sqft_war);
update parcel_buildings
     set land_use_type_name_2 = "ware"
     where (land_use_type_name_1 = "off" and sqft_war>0 and sqft_war>sqft_ind and sqft_war>sqft_tcu and sqft_war>sqft_com)
        or (land_use_type_name_1 = "ind" and sqft_war>0 and sqft_war>sqft_off and sqft_war>sqft_tcu and sqft_war>sqft_com)
        or (land_use_type_name_1 = "tcu" and sqft_war>0 and sqft_war>sqft_off and sqft_war>sqft_ind and sqft_war>sqft_com)
        or (land_use_type_name_1 = "com" and sqft_war>0 and sqft_war>sqft_off and sqft_war>sqft_ind and sqft_war>sqft_tcu)
        or (land_use_type_name_1 = "res" and sqft_war>0 and sqft_war>sqft_off and sqft_war>sqft_ind and sqft_war>sqft_tcu and sqft_war>sqft_com);
update parcel_buildings
     set land_use_type_name_2 = "res"
     where (land_use_type_name_1 = "com" and sqft_res>0)
        or (land_use_type_name_1 = "off" and sqft_res>0)
        or (land_use_type_name_1 = "ind" and sqft_res>0)
        or (land_use_type_name_1 = "tcu" and sqft_res>0)
        or (land_use_type_name_1 = "ware" and sqft_res>0);
update parcel_buildings
     set land_use_type_name_2 = "vac"
     where land_use_type_name_1 = "vac";


# Mark the different kinds of recognized mixed uses

update parcel_buildings
     set mix_com_ind = 0,
         mix_com_off = 0,
         mix_com_ware = 0,
         mix_off_ind = 0,
         mix_off_ware = 0,
         mix_ind_ware = 0,
         mix_com_res = 0,
         mix_off_res = 0,
         mix_ware_res = 0;

update parcel_buildings
     set mix_com_ind = 1,
         land_use_name = "mix_com_ind"
     where is_mixed_use = 1
       and ((land_use_type_name_1 = "com" and land_use_type_name_2 = "ind")
        or  (land_use_type_name_2 = "com" and land_use_type_name_1 = "ind"));
update parcel_buildings
     set mix_com_off = 1,
         land_use_name = "mix_com_off"
     where is_mixed_use = 1
       and ((land_use_type_name_1 = "com" and land_use_type_name_2 = "off")
        or  (land_use_type_name_2 = "com" and land_use_type_name_1 = "off"));
update parcel_buildings
     set mix_com_ware = 1,
         land_use_name = "mix_com_ware"
     where is_mixed_use = 1
       and ((land_use_type_name_1 = "com" and land_use_type_name_2 = "war")
        or  (land_use_type_name_2 = "com" and land_use_type_name_1 = "war"));
update parcel_buildings
     set mix_off_ind = 1,
         land_use_name = "mix_off_ind"
     where is_mixed_use = 1
       and ((land_use_type_name_1 = "off" and land_use_type_name_2 = "ind")
        or  (land_use_type_name_2 = "off" and land_use_type_name_1 = "ind"));
update parcel_buildings
     set mix_off_ware = 1,
         land_use_name = "mix_off_ware"
     where is_mixed_use = 1
       and ((land_use_type_name_1 = "off" and land_use_type_name_2 = "ware")
        or  (land_use_type_name_2 = "off" and land_use_type_name_1 = "ware"));
update parcel_buildings
     set mix_ind_ware = 1,
         land_use_name = "mix_ind_ware"
     where is_mixed_use = 1
       and ((land_use_type_name_1 = "ind" and land_use_type_name_2 = "ware")
        or  (land_use_type_name_2 = "ind" and land_use_type_name_1 = "ware"));
update parcel_buildings
     set mix_com_res = 1,
         land_use_name = "mix_com_res"
     where is_mixed_use = 1
       and ((land_use_type_name_1 = "com" and land_use_type_name_2 = "res")
        or  (land_use_type_name_2 = "com" and land_use_type_name_1 = "res"));
update parcel_buildings
     set mix_off_res = 1,
         land_use_name = "mix_off_res"
     where is_mixed_use = 1
       and ((land_use_type_name_1 = "off" and land_use_type_name_2 = "res")
        or  (land_use_type_name_2 = "off" and land_use_type_name_1 = "res"));
update parcel_buildings
     set mix_ware_res = 1,
         land_use_name = "mix_ware_res"
     where is_mixed_use = 1
       and ((land_use_type_name_1 = "ware" and land_use_type_name_2 = "res")
        or  (land_use_type_name_2 = "ware" and land_use_type_name_1 = "res"));

update parcel_buildings
     set is_mixed_use = 0
     where mix_com_ind  + mix_com_off  + mix_com_ware + mix_off_ind  + mix_off_ware +
           mix_ind_ware + mix_com_res  + mix_off_res  + mix_ware_res = 0;

# Set land use types for single-uses
update parcel_buildings
     set land_use_name = "com"
     where land_use_type_name_1 = "com"
       and is_mixed_use = 0;
update parcel_buildings
     set land_use_name = "ind"
     where land_use_type_name_1 = "ind"
       and is_mixed_use = 0;
update parcel_buildings
     set land_use_name = "mfr_apartment"
     where land_use_type_name_1 = "res"
       and units_mfa > units_sfr
       and units_mfa > units_mfc
       and is_mixed_use = 0;
update parcel_buildings
     set land_use_name = "mfr_condo"
     where land_use_type_name_1 = "res"
       and units_mfc > units_sfr
       and units_mfc >= units_mfa
       and is_mixed_use = 0;
update parcel_buildings
     set land_use_name = "off"
     where land_use_type_name_1 = "off"
       and is_mixed_use = 0;
update parcel_buildings
     set land_use_name = "tcu"
     where land_use_type_name_1 = "tcu"
       and is_mixed_use = 0;
update parcel_buildings
     set land_use_name = "ware"
     where land_use_type_name_1 = "ware"
       and is_mixed_use = 0;
update parcel_buildings
     set land_use_name = "sfr"
     where land_use_type_name_1 = "res"
       and units_sfr >= units_mfc
       and units_sfr >= units_mfa
       and is_mixed_use = 0;
update parcel_buildings
     set land_use_name = "gov"
     where land_use_type_name_1 = "gov";
update parcel_buildings
     set land_use_name = "other"
     where land_use_type_name_1 = "oth";
update parcel_buildings
     set land_use_name = "vacant"
     where land_use_type_name_1 = "vac";

# Match up with land use types table for IDs

update parcel_buildings p, land_use_types_new l
     set p.land_use_type_id = l.land_use_type_id
     where p.land_use_name = l.land_use_name;

# Update the actual parcels table

drop table if exists parcels;
create table parcels
     like psrc_2005_parcel_baseyear_start.parcels;

insert into parcels
     select * from psrc_2005_parcel_baseyear_start.parcels;

update parcels as p, parcel_buildings as b
     set p.land_use_type_id = b.land_use_type_id
     where p.parcel_id = b.parcel_id;

# if needed...
alter table parcels 
     drop column land_use_type_id_old, 
     drop column land_use_type_id_new;
create index parcels_land_use_type_id
     on parcels (land_use_type_id);
# (end "if needed")

# Expand "names" and add descriptions in Land Use Types table

update land_use_types_new
     set land_use_name = "commercial",
         description = "Commercial"
     where land_use_name = "com";
update land_use_types_new
     set land_use_name = "industrial",
         description = "Industrial"
     where land_use_name = "ind";
update land_use_types_new
     set land_use_name = "multi_family_apartment",
         description = "Multi-Family Apartment"
     where land_use_name = "mfr_apartment";
update land_use_types_new
     set land_use_name = "multi_family_condominium",
         description = "Multi-Family Condiminium"
     where land_use_name = "mfr_condo";
update land_use_types_new
     set land_use_name = "mixed_commercial_industrial",
         description = "Mixed Commercial/Industrial"
     where land_use_name = "mix_com_ind";
update land_use_types_new
     set land_use_name = "mixed_commercial_office",
         description = "Mixed Commercial/Office"
     where land_use_name = "mix_com_off";
update land_use_types_new
     set land_use_name = "mixed_commercial_residential",
         description = "Mixed Commercial/Residential"
     where land_use_name = "mix_com_res";
update land_use_types_new
     set land_use_name = "mixed_commercial_warehousing",
         description = "Mixed Commercial/Warehousing"
     where land_use_name = "mix_com_ware";
update land_use_types_new
     set land_use_name = "mixed_industrial_warehousing",
         description = "Mixed Industrial/Warehousing"
     where land_use_name = "mix_ind_ware";
update land_use_types_new
     set land_use_name = "mixed_office_industrial",
         description = "Mixed Office/Industrial"
     where land_use_name = "mix_off_ind";
update land_use_types_new
     set land_use_name = "mixed_office_residential",
         description = "Mixed Office/Residential"
     where land_use_name = "mix_off_res";
update land_use_types_new
     set land_use_name = "mixed_office_warehousing",
         description = "Mixed Office/Warehousing"
     where land_use_name = "mix_off_ware";
update land_use_types_new
     set land_use_name = "mixed_warehousing_residential",
         description = "Mixed Warehousing/Residential"
     where land_use_name = "Mix_ware_res";
update land_use_types_new
     set land_use_name = "office",
         description = "Office"
     where land_use_name = "off";
update land_use_types_new
     set land_use_name = "single_family_residential",
         description = "Single Family Residential"
     where land_use_name = "sfr";
update land_use_types_new
     set land_use_name = "tcu",
         description = "Transportation, Communications, Utilities"
     where land_use_name = "tcu";
update land_use_types_new
     set land_use_name = "warehousing",
         description = "Warehousing"
     where land_use_name = "ware";
update land_use_types_new
     set land_use_name = "government",
         description = "Government"
     where land_use_name = "gov";
update land_use_types_new
     set land_use_name = "other",
         description = "Other"
     where land_use_name = "other";
update land_use_types_new
     set land_use_name = "vacant",
         description = "Vacant"
     where land_use_name = "vacant";

# Convert density units to absolute units
update land_use_types_new
     set unit_name = "building_sqft"
     where unit_name = "far";
update land_use_types_new
     set unit_name = "residential_units"
     where unit_name = "units_per_acre";
update land_use_types_new
     set unit_name = "parcel_sqft"
     where unit_name = "1";


# Enter into a new change database

create database psrc_2005_parcel_baseyear_change_20070524;
use psrc_2005_parcel_baseyear_change_20070524;

create table scenario_information
     like psrc_2005_parcel_baseyear_change_20070523.scenario_information;
insert into scenario_information
     select * from psrc_2005_parcel_baseyear_change_20070523.scenario_information;
update scenario_information
     set PARENT_DATABASE_URL = "jdbc:mysql://trondheim.cs.washington.edu/psrc_2005_parcel_baseyear_change_20070523";

create table parcels
     like psrc_2005_data_workspace_franklin.parcels;
insert into parcels
     select * from psrc_2005_data_workspace_franklin.parcels;

create table land_use_types
     like psrc_2005_data_workspace_franklin.land_use_types_new;
insert into land_use_types
     select * from psrc_2005_data_workspace_franklin.land_use_types_new;

create table change_log
     like psrc_2005_parcel_baseyear_change_20070523.change_log;
insert into change_log values
     ("update","parcels","joel","fixed some land use type designations"),
     ("update","land_use_types","joel","consolidated sfr types");

# When ready to finalize, update the psrc_2005_parcel_baseyear database:
update psrc_2005_parcel_baseyear.scenario_information
     set PARENT_DATABASE_URL = "jdbc:mysql://trondheim.cs.washington.edu/psrc_2005_parcel_baseyear_change_20070524";



