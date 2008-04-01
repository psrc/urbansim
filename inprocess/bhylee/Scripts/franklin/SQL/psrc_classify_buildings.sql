# Classifies buildings by building_type,
# starting with the classification table
# from 2005 workspace, but adding rows
# for additional types.

use PSRC_parcels_all_counties;

# Get old reclassification table from 2005 workspace

drop table if exists building_type_reclass;
create table building_type_reclass
     like psrc_2005_data_revised_2.building_type_reclass_2005;

insert into building_type_reclass
     select * from psrc_2005_data_revised_2.building_type_reclass_2005;

update building_type_reclass
     set general_category = "Industrial"
     where general_category = "Mining";

update building_type_reclass
     set general_category = "Mobile Home",
         general_category_code = 11
     where general_category = "Mobile Home Park";

update building_type_reclass
     set general_category_code = general_category_code - 1
     where general_category_code >= 12;

# Match to 2000 buildings to find what's matched and what isn't

drop table if exists buildings_2;
create table buildings_2
     select b.*,
            t.ID as building_use_id,
            t.general_category_code as building_type_id,
            t.general_category as building_type,
            t.building_type as generic_building_type_id,
            t.building_type_desc as generic_building_type
     from buildings as b
     left join building_type_reclass as t
          on b.county = t.County and
             b.building_use = t.building_use_code;

create index buildings_2_county_building_use
     on buildings_2 (county, building_use);

# View distinct classifications to find NULL (generic) building types
#select distinct county, 
#                building_use, 
#                description, 
#                building_type_id, 
#                building_type, 
#                generic_building_type_id, 
#                generic_building_type 
#     from buildings_2 
#     order by county, building_use;

# Add rows to reclassify building uses with null types

insert into building_type_reclass(County, building_use_code, building_use_description, 
                                  general_category, general_category_code, housing_units_snohomish, 
                                  building_type, building_type_desc)
     values ("033", "111", "SF Residential", "Single Family Residential", 19, NULL, 1, "single family residential"),
            ("033", "112", "MF Residential (2&3Plex)", "Multi-Family Residential", 12, NULL, 2, "multi-family residential"),
            ("033", "113", "Condominium Residential", "Condo Residential", 4, NULL, 2, "multi-family residential"),
            ("033", "114", "Condominium Res (APT Use)", "Condo Residential", 4, NULL, 2, "multi-family residential"),
            ("033", "115", "Condominium (Commercial Use)", "Condo Residential", 4, NULL, 2, "multi-family residential"),
            ("033", "116", "Condominium (Mixed Use)", "Condo Residential", 4, NULL, 2, "multi-family residential"),
            ("033", "117", "Condominium Res (Mobile Home)", "Condo Residential", 4, NULL, 2, "multi-family residential"),
            ("033", "118", "Condominium Res (Floating Home)", "Condo Residential", 4, NULL, 2, "multi-family residential"),
            ("033", "636", NULL, "No Code", 0, NULL, 0, "other"),
            ("033", "Imputed - Agriculture", "Imputed - Agriculture", "Agriculture", 1, NULL, 0, "other"),
            ("033", "Imputed - Civic and Quasi-Public", "Imputed - Civic and Quasi-Public", "Civic and Quasi-Public", 2, NULL, 0, "other"),
            ("033", "Imputed - Commercial", "Imputed - Commercial", "Commercial", 3, NULL, 4, "commercial"),
            ("033", "Imputed - Government", "Imputed - Government", "Government", 5, NULL, 0, "other"),
            ("033", "Imputed - Group Quarters", "Imputed - Group Quarters", "Group Quarters", 6, NULL, 0, "other"),
            ("033", "Imputed - Industrial", "Imputed - Industrial", "Industrial", 8, NULL, 5, "industrial"),
            ("033", "Imputed - Mining", "Imputed - Mining", "Industrial", 8, NULL, 5, "industrial"),
            ("033", "Imputed - Mobile Home Park", "Imputed - Mobile Home Park", "Mobile Home", 11, NULL, 1, "single family residential"),
            ("033", "Imputed - Multi-Family Residential", "Imputed - Multi-Family Residential", "Multi-Family Residential", 12, NULL, 2, "multi-family residential"),
            ("033", "Imputed - Office", "Imputed - Office", "Office", 13, NULL, 3, "office"),
            ("033", "Imputed - Park and Open Space", "Imputed - Park and Open Space", "Park and Open Space", 15, NULL, 0, "other"),
            ("033", "Imputed - Parking", "Imputed - Parking", "Parking", 16, NULL, 0, "other"),
            ("033", "Imputed - Recreation", "Imputed - Recreation", "Recreation", 17, NULL, 0, "other"),
            ("033", "Imputed - Right-of-Way", "Imputed - Right-of-Way", "No Code", 0, NULL, 0, "other"),
            ("033", "Imputed - School", "Imputed - School", "School", 18, NULL, 0, "other"),
            ("033", "Imputed - Single Family Residential", "Imputed - Single Family Residential", "Single Family Residential", 19, NULL, 1, "single family residential"),
            ("033", "Imputed - Transportation Communication Utilities", "Imputed - Transportation Communication Utilities", "Transportation Communication Utilities", 20, NULL, 5, "industrial"),
            ("033", "Imputed - Vacant", "Imputed - Vacant", "No Code", 0, NULL, 0, "other"),
            ("033", "Imputed - Warehousing", "Imputed - Warehousing", "Warehousing", 21, NULL, 5, "industrial"),
            ("035", NULL, NULL, "No Code", 0, NULL, 0, "other"),
            ("035", "Relocatable Office", "Relocatable Office", "Office", 13, NULL, 3, "office"),
            ("035", "Resturant", "Resturant", "Commercial", 3, NULL, 4, "commercial"),
            ("035", "Storage Hangar", "Storage Hangar", "Transportation Communication Utilities", 20, NULL, 5, "industrial");

insert into building_type_reclass(County, building_use_code, building_use_description, 
                                  general_category, general_category_code, housing_units_snohomish, 
                                  building_type, building_type_desc)
     values ("053", "1", "1 Story", "No Code", 0, NULL, 0, "other"),
            ("053", "112", "Condo unit", "Condo Residential", 4, NULL, 2, "multi-family residential"),
            ("053", "1133", "Prefabricated Storage Shed Buildings", "Outbuilding", 14, NULL, 0, "other"),
            ("053", "115", "MH on Vacant Land", "Mobile Home", 11, NULL, 1, "single family residential"),
            ("053", "116", "Apts w/4-19 Units", "Multi-Family Residential", 12, NULL, 1, "multi-family residential"),
            ("053", "117", "Apts w/20+ Units", "Multi-Family Residential", 12, NULL, 1, "multi-family residential"),
            ("053", "141", "Tanks  *CODE", "Industrial", 8, NULL, 5, "industrial"),
            ("053", "1460", "Mixed Retail w/ Office Units", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "1473", "Material Shelters", "Industrial", 8, NULL, 5, "industrial"),
            ("053", "154", "Steel Tank Low Stress - Above ground", "Industrial", 8, NULL, 5, "industrial"),
            ("053", "156", "Welded Steel Water Tank", "Industrial", 8, NULL, 5, "industrial"),
            ("053", "160", "Galvanized SteelTank", "Industrial", 8, NULL, 5, "industrial"),
            ("053", "167", "Fiber Coated Steel Dbl Wall Underground Fuel Tank", "Industrial", 8, NULL, 5, "industrial"),
            ("053", "168", "Welded Underground Fuel Tank", "Industrial", 8, NULL, 5, "industrial"),
            ("053", "169", "Bolted Steel Underground Tank", "Industrial", 8, NULL, 5, "industrial"),
            ("053", "175", "Welded Pressure", "Industrial", 8, NULL, 5, "industrial"),
            ("053", "201", "Bulk Oil", "Industrial", 8, NULL, 5, "industrial"),
            ("053", "204", "Computer Centers", "Office", 13, NULL, 3, "office"),
            ("053", "208", "Golf Course  *CODE", "Recreation", 17, NULL, 0, "other"),
            ("053", "216", "Radio & TV Stations", "Transportation Communication Utilities", 20, NULL, 5, "industrial"),
            ("053", "225", "Guest Houses", "Single Family Residential", 19, NULL, 1, "single family residential"),
            ("053", "226", "Bath Houses", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "301", "Armory", "Military", 9, NULL, 0, "other"),
            ("053", "302", "Auditorium", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "303", "Showroom", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "306", "Bowling Alley", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "313", "Convlsnt Hosp Nursing Home", "Hospital / Convalescent Center", 7, NULL, 0, "other"),
            ("053", "314", "Country Club", "Recreation", 17, NULL, 0, "other"),
            ("053", "315", "Creamery", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "321", "Dormitory Residence Halls", "Group Quarters", 6, NULL, 0, "other"),
            ("053", "323", "Fraternal Building", "Recreation", 17, NULL, 0, "other"),
            ("053", "324", "Fraternity", "Group Quarters", 6, NULL, 0, "other"),
            ("053", "330", "Home For the Elderly", "Hospital / Convalescent Center", 7, NULL, 0, "other"),
            ("053", "331", "Hospital", "Hospital / Convalescent Center", 7, NULL, 0, "other"),
            ("053", "332", "Hotel", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "333", "Indust Heavy Manufacturing", "Industrial", 8, NULL, 5, "industrial"),
            ("053", "335", "Jail", "Government", 5, NULL, 0, "other"),
            ("053", "336", "Laundromat", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "338", "Loft - Industrial", "Industrial", 8, NULL, 5, "industrial"),
            ("053", "339", "Lumber Storage - Horizontal", "Warehousing", 21, NULL, 5, "industrial"),
            ("053", "342", "Mortuary", "Civic and Quasi-Public", 2, NULL, 0, "other"),
            ("053", "343", "Motel", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "345", "Parking Structure", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "346", "Post Office", "Government", 5, NULL, 0, "other"),
            ("053", "356", "School - Classroom", "School", 18, NULL, 0, "other"),
            ("053", "358", "School - Gymnasium", "School", 18, NULL, 0, "other"),
            ("053", "377", "College - Entire", "School", 18, NULL, 0, "other"),
            ("053", "381", "Veterinary Hospital", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "403", "Shower Building", "Outbuilding", 14, NULL, 0, "other"),
            ("053", "404", "Shed - Utility", "Outbuilding", 14, NULL, 0, "other"),
            ("053", "408", "Service Station", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "414", "Regional Shopping Center", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "418", "Health Club", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "423", "Mini Lube Garage", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "424", "Group Care Homes", "Hospital / Convalescent Center", 7, NULL, 0, "other"),
            ("053", "432", "Restroom Building/Concessions", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "483", "Fitness Center", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "484", "High School", "School", 18, NULL, 0, "other"),
            ("053", "487", "Vocational Schools", "School", 18, NULL, 0, "other"),
            ("053", "518", "Lath Shade Shelter", "Outbuilding", 14, NULL, 0, "other"),
            ("053", "519", "Greenhouse Shade Shelters", "Outbuilding", 14, NULL, 0, "other"),
            ("053", "523", "Golf Cart Storage Bldgs", "Outbuilding", 14, NULL, 0, "other"),
            ("053", "530", "Restaurants - Cafeterias", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "585", "Mechanical Penthouse", "Industrial", 8, NULL, 5, "industrial"),
            ("053", "598", "Relocatable Classroom", "School", 18, NULL, 0, "other"),
            ("053", "605", "Church", "Civic and Quasi-Public", 2, NULL, 0, "other"),
            ("053", "660", "Fixed Steel Towers", "Industrial", 8, NULL, 5, "industrial"),
            ("053", "665", "Ice Skating Rink", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "670", "Grandstand and Bleachers", "Recreation", 17, NULL, 0, "other"),
            ("053", "675", "Permanently Installed Scales", "Industrial", 8, NULL, 5, "industrial"),
            ("053", "810", "Stadiums", "Commercial", 3, NULL, 4, "commercial"),
            ("053", "Imputed - Transportation Communication Utilities", "Imputed - Transportation Communication Utilities", 
               "Transportation Communication Utilities", 20, NULL, 5, "industrial");

insert into building_type_reclass(County, building_use_code, building_use_description, 
                                  general_category, general_category_code, housing_units_snohomish, 
                                  building_type, building_type_desc)
     values ("061", NULL, NULL, "No Code", 0, NULL, 0, "other"),
            ("061", "FRATHSE", "FRATHSE", "Group Quarters", 6, NULL, 0, "other"),
            ("061", "Imputed - Agriculture", "Imputed - Agriculture", "Agriculture", 1, NULL, 0, "other"),
            ("061", "Imputed - Civic and Quasi-Public", "Imputed - Civic and Quasi-Public", "Civic and Quasi-Public", 2, NULL, 0, "other"),
            ("061", "Imputed - Commercial", "Imputed - Commercial", "Commercial", 3, NULL, 4, "commercial"),
            ("061", "Imputed - Fisheries", "Imputed - Fisheries", "Industrial", 8, NULL, 5, "industrial"),
            ("061", "Imputed - Forest - harvestable", "Imputed - Forest - harvestable", "Industrial", 8, NULL, 5, "industrial"),
            ("061", "Imputed - Government", "Imputed - Government", "Government", 5, NULL, 0, "other"),
            ("061", "Imputed - Group Quarters", "Imputed - Group Quarters", "Group Quarters", 6, NULL, 0, "other"),
            ("061", "Imputed - Industrial", "Imputed - Industrial", "Industrial", 8, NULL, 5, "industrial"),
            ("061", "Imputed - Military", "Imputed - Military", "Military", 9, NULL, 0, "other"),
            ("061", "Imputed - Mining", "Imputed - Mining", "Industrial", 8, NULL, 5, "industrial"),
            ("061", "Imputed - Mobile Home Park", "Imputed - Mobile Home Park", "Mobile Home", 11, NULL, 1, "single family residential"),
            ("061", "Imputed - Multi-Family Residential", "Imputed - Multi-Family Residential", "Multi-Family Residential", 12, NULL, 2, "multi-family residential"),
            ("061", "Imputed - Office", "Imputed - Office", "Office", 13, NULL, 3, "office"),
            ("061", "Imputed - Park and Open Space", "Imputed - Park and Open Space", "Park and Open Space", 15, NULL, 0, "other"),
            ("061", "Imputed - Parking", "Imputed - Parking", "Parking", 16, NULL, 0, "other"),
            ("061", "Imputed - Recreation", "Imputed - Recreation", "Recreation", 17, NULL, 0, "other"),
            ("061", "Imputed - Right-of-Way", "Imputed - Right-of-Way", "No Code", 0, NULL, 0, "other"),
            ("061", "Imputed - School", "Imputed - School", "School", 18, NULL, 0, "other"),
            ("061", "Imputed - Single Family Residential", "Imputed - Single Family Residential", "Single Family Residential", 19, NULL, 1, "single family residential"),
            ("061", "Imputed - Transportation Communication Utilities", "Imputed - Transportation Communication Utilities", "Transportation Communication Utilities", 20, NULL, 5, "industrial"),
            ("061", "Imputed - Vacant", "Imputed - Vacant", "No Code", 0, NULL, 0, "other"),
            ("061", "Imputed - Warehousing", "Imputed - Warehousing", "Warehousing", 21, NULL, 5, "industrial"),
            ("061", "Imputed - Water", "Imputed - Water", "No Code", 0, NULL, 0, "other"),
            ("061", "LOBBY", "LOBBY", "Commercial", 3, NULL, 4, "commercial"),
            ("061", "SCHADMIN", "SCHADMIN", "School", 18, NULL, 0, "other"),
            ("061", "SERVICE", "SERVICE", "Commercial", 3, NULL, 4, "commercial"),
            ("061", "SERVICEB", "SERVICEB", "Commercial", 3, NULL, 4, "commercial"),
            ("061", "SKATING", "SKATING", "Commercial", 3, NULL, 4, "commercial");

# Apply new reclassifications to buildings

update buildings_2 as b, building_type_reclass as r
     set b.building_type_id = r.general_category_code,
         b.building_type = r.general_category,
         b.generic_building_type_id = r.building_type,
         b.generic_building_type = r.building_type_desc
     where b.county = r.County
       and b.building_use = r.building_use_code
       and b.building_type_id is null;

update buildings_2 as b
     set b.building_type_id = 0,
         b.building_type = "No Code",
         b.generic_building_type_id = 0,
         b.generic_building_type = "other"
     where b.building_use is null;

# Format buildings table and place into baseyear database

drop table if exists psrc_2000_parcel_baseyear_start.buildings;
create table psrc_2000_parcel_baseyear_start.buildings (
     building_id int primary key auto_increment,
     parcel_id int,
     land_area int,
     non_residential_sqft int,
     residential_units int,
     sqft_per_unit int,
     year_built int,
     zone_id int);

insert into psrc_2000_parcel_baseyear_start.buildings
          (parcel_id, land_area, non_residential_sqft, residential_units,
           sqft_per_unit, year_built, zone_id)
     select NULL as parcel_id,
            NULL as land_area,
            built_sqft as non_residential_sqft,
            NULL as residential_units,
            NULL as sqft_per_unit,
            year_built as year_built,
            NULL as zone_id
     from buildings_2;



# Now do the same thing to parcels

drop table if exists land_use_generic_reclass;
create table land_use_generic_reclass
     like psrc_2005_data_workspace.land_use_generic_reclass_2005;

insert into land_use_generic_reclass
     select * from psrc_2005_data_workspace.land_use_generic_reclass_2005;

# Match to 2000 parcels to find what's matched and what isn't

drop table if exists parcels_2;
create table parcels_2
     select b.*,
            t.land_use_description as land_use_description,
            t.generic_land_use_1 as generic_land_use_1,
            t.generic_land_use_2 as generic_land_use_2
     from parcels as b
     left join land_use_generic_reclass as t
          on b.county = t.County and
             b.county_land_use_code = t.county_land_use_code;

create index parcels_2_county_parcel_use
     on parcels_2 (county, parcel_use);





