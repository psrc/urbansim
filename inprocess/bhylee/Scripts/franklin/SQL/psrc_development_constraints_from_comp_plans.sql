

use psrc_2005_data_workspace;

# Create Building table

drop table if exists building_types;
create table if not exists building_types (
     building_type int,
     building_type_description char(38),
     development_constraint_type_id int
     );
insert into building_types
     values ( 1, "Agriculture", 8),
            ( 2, "Civic and Quasi-Public", 7),
            ( 3, "Commercial", 4),
            ( 4, "Condo Residential", 2),
            ( 5, "Government", 7),
            ( 6, "Group Quarters", 8),
            ( 7, "Hospital / Convalescent Center", 8),
            ( 8, "Industrial", 6),
            ( 9, "Military", 7),
            (10, "Mixed-Use", 3),
            (11, "Mobile Home Park", 1),
            (12, "Multi-Family Residential", 2),
            (13, "Office", 3),
            (14, "Outbuilding", 6),
            (15, "Park and Open Space", 6),
            (16, "Parking", 3),
            (17, "Recreation", 3),
            (18, "School", 5),
            (19, "Single Family Residential", 1),
            (20, "Transportation Communication Utilities", 4),
            (21, "Warehousing", 4);


# Import comprehensive plan data

drop table if exists all_parcels_with_cplan_jpf;
create table all_parcels_with_cplan_jpf (
     d_r char(1),
     join_count int,
     county char(5),
     parcel_idn char(25),
     area double,
     x_coord_sp double,
     y_coord_sp double,
     parcelid char(28),
     perimeter double,
     regflu_cle int,
     regflu_c_1 int,
     genuse char(4),
     desc_ char(50),
     resdenl int,
     resdenh int,
     cityname char(30),
     cntyname char(30),
     cityfips int,
     cntyfips int,
     status int,
     annxname char(80),
     brbno int,
     ordno int,
     eff_date date,
     inurbanctr int
     );

load data infile '2005_centroids_regflu.dat' # Created in GIS by overlaying regflu on parcel centerpoints
     into table all_parcels_with_cplan_jpf;

create index apwcpjpf_county_parcel_id 
     on all_parcels_with_cplan_jpf (parcelid);

# add table of development constraint types

drop table if exists development_constraint_types;
create table if not exists development_constraint_types (
     development_constraint_type_id int,
     development_constraint_type_description char(25)
     );

insert into development_constraint_types
     values ( 1, "Single-Family Residential"),
            ( 2, "Multi-Family Residential"),
            ( 3, "Mixed Residential/Commercial"),
            ( 4, "Commercial"),
            ( 5, "Office"),
            ( 6, "Industrial"),
            ( 7, "Government"),
            ( 8, "Other");

# add table of original comprehensive plan types, with 
# codes for a reduced set

drop table if exists comp_plan_types;
create table comp_plan_types (
     comp_plan_id int,
     comp_plan_desc char(34)
     );

create index comp_plan_types_desc on comp_plan_types (comp_plan_desc);

insert into comp_plan_types values
     (392, "Single Family Residential Areas"),
     (305, "Residential"),
     (193, "Moderate Density Single Family"),
     (116, "Intensity 1 (Residential)"),
     (307, "Residential 10"),
     (140, "Low Density Residential"),
     (392, "Residential Single Family"),
     (204, "Multi-Family Residential Areas"),
     (393, "Single Family High-Density Residen"),
     (193, "Low-Moderate Density Residential"),
     (393, "Single Family High Density"),
     (193, "Single Family Medium Density"),
     (392, "Single Family Residential"),
     (369, "SF-6 Six Units/Acre Maximum"),
     (358, "Rural Separator"),
     (150, "Low Urban Density Residential"),
     (319, "Residential 5"),
     (68, "County Urban Res 4-12 Unit/Acre"),
     (140, "Residential Low Density"),
     (251, "Intensity 2 (Parks, Open Space)"),
     (38, "Intensity 3 (Commercial)"),
     (49, "Commercial/Mixed Use in Centers/Vi"),
     (112, "Industrial"),
     (319, "Single Family (6)"),
     (319, "Residential V5"),
     (185, "Mixed Use District"),
     (383, "High Density Single Family Residen"),
     (358, "Rural Residential - RD (1du/2.3ac)"),
     (140, "Residential Low"),
     (319, "Single Family 5du/ac"),
     (358, "Rural"),
     (9, "Agriculture"),
     (307, "Residential V10"),
     (307, "Single Family, R-9.6"),
     (376, "Single Family 3du/ac"),
     (386, "Single Family Low Density"),
     (309, "Residential 2 (15,000 Sq. Ft.-8,40"),
     (38, "Commercial"),
     (319, "Residential 2-5du/ac"),
     (112, "Intensity 4 (Industrial)"),
     (193, "Medium Density Residential"),
     (50, "Commercial/Mixed Use not in Center"),
     (401, "Single Family, R-8.4"),
     (383, "High Density Residential"),
     (157, "Master Planned Community"),
     (400, "Single Family, R-15"),
     (251, "Parks,recreation,and open space"),
     (77, "Duplex, Mobile Home,Single Family"),
     (383, "Single Family Residential, High"),
     (193, "Moderate Density Residential"),
     (319, "Single Family Suburban 4.5du-ac"),
     (358, "Rural/Semi-Rural");
insert into comp_plan_types values
     (305, "Housing"),
     (393, "Single Family Residential, Mod/Hig"),
     (193, "Single Family Medium-Density Resid"),
     (185, "Mixed"),
     (314, "Residential 2-5du/ac, Office-Prof,"),
     (140, "Low Density Residential 2"),
     (319, "High Density - 5 Units Per Acre"),
     (407, "Suburban"),
     (193, "Medium Density Single Family Resid"),
     (339, "Residential Urban"),
     (74, "Downtown Areas"),
     (418, "Right of Way"),
     (319, "Single Family (5)"),
     (228, "Employment Based Center"),
     (305, "Residential Options"),
     (376, "R-16 (16000 sq ft)"),
     (204, "Multi-Family"),
     (74, "Major Urban Center"),
     (334, "Residential R20"),
     (418, "Right-of-Way"),
     (228, "Community Business"),
     (74, "City Center"),
     (418, "Water"),
     (358, "Rural Buffer Residential"),
     (319, "Single Family 6du/ac"),
     (193, "Single Family Residential, Moderat"),
     (228, "Employment Center"),
     (185, "Mixed Use"),
     (375, "Single Family 2du/ac"),
     (383, "High Urban Density Residential"),
     (13, "Auto Oriented Commercial"),
     (74, "Downtown Commercial"),
     (194, "Moderate Urban Density"),
     (418, "Street/Highway/Alley Rights-of-Way"),
     (74, "Center Downtown"),
     (38, "General Commercial"),
     (126, "Light Industrial"),
     (180, "Mixed Single and Multi-Family"),
     (74, "Downtown"),
     (418, "ROW"),
     (71, "Forest Land"),
     (162, "Medium Density Multifamily"),
     (401, "SF-8 Eight Units/Acre Maximum"),
     (137, "Low Density Multifamily"),
     (228, "Office"),
     (228, "Professional Office"),
     (334, "R-20 (20000 Sq ft)"),
     (193, "Residential Medium Density"),
     (376, "SF-3 Three Units/Acre Maximum");
insert into comp_plan_types values
     (94, "Heavy Commercial"),
     (137, "Multifamily Low Density"),
     (177, "Mixed Commercial/High Density Resi"),
     (180, "Mixed Residential Established SF D"),
     (124, "Large Lot Residential"),
     (369, "Residential 3 (8,400 Sq. Ft.-6,223"),
     (376, "Single Family Residential 15000 sq"),
     (407, "Residential Suburban"),
     (153, "Manufacturing Center"),
     (228, "Employment Area Vacant"),
     (386, "Single Family Residential, Low"),
     (251, "Public, Private Parks, Conservatio"),
     (307, "Residential 6-10du/ac"),
     (38, "Commercial/Business"),
     (400, "Residential 11-15du/ac, Office-Pro"),
     (251, "Public Open Space"),
     (221, "Neighborhood Center"),
     (350, "Rural Activity Center"),
     (358, "Residential Rural"),
     (153, "Manufacturing Park"),
     (57, "Community Commercial"),
     (228, "Employment Area - Commercial"),
     (26, "Center Suburban"),
     (56, "Community Center"),
     (44, "Commercial, Industrial, Agricultur"),
     (383, "High Density Residential District"),
     (229, "Office / Residential"),
     (162, "Multifamily Medium Density"),
     (190, "Mixed, Limited Multifamily"),
     (20, "Business Park"),
     (221, "Neighborhood Business"),
     (204, "Residential Multi-Family Infill"),
     (74, "Tukwila Urban Center"),
     (140, "Low Density Residential 1"),
     (193, "Medium Density Residential DD"),
     (269, "Public Facilities"),
     (251, "Open Space"),
     (99, "High Density Multifamily"),
     (94, "Commercial High Intensity"),
     (125, "Light Commercial"),
     (68, "Single Family, R-12"),
     (264, "Major Institutional"),
     (131, "Light Manufacturing/Warehousing"),
     (193, "Medium Density Residential TDR"),
     (233, "Office/Multi-Family"),
     (204, "Multifamily Residential"),
     (66, "County Urban Res 1 Unit/Acre"),
     (299, "Regional Commercial"),
     (269, "Public & Quasi-Public"),
     (71, "Designated Forest Land"),
     (251, "Parks and Recreation");
insert into comp_plan_types values
     (193, "Medium Density Residential(4.1 to"),
     (254, "Pedestrian Oriented Commercial"),
     (209, "Multi-Family (24)"),
     (140, "Low Density Residential 1 CD"),
     (376, "Single Family (3)"),
     (48, "Commercial/Light Industrial"),
     (400, "Residential 4 (6,223 Sq. Ft.-2,904"),
     (49, "Mixed Use Town Center"),
     (193, "Medium Density - 4 Units Per Acre"),
     (99, "Multifamily High Density"),
     (209, "Multifamily Medium 14.52du-ac"),
     (96, "Heavy Industrial"),
     (228, "Office, Limited Business"),
     (376, "Single Family 3du/ac SEA"),
     (415, "Urban Village"),
     (74, "Cultural and Business District"),
     (49, "Mixed-Use-Town-Center"),
     (369, "Mixed Residential 7.26du-ac"),
     (251, "Public Parks-Schools-Rec-Open Spac"),
     (38, "Retail"),
     (131, "Light Manufacturing"),
     (400, "Residential 11-15du/ac"),
     (350, "Acitvity Center"),
     (293, "R-40 Single Dwelling Unit"),
     (140, "Low Density Residential 1 DD"),
     (153, "Manufacturing/Industrial Center -"),
     (99, "Multifamily High 29du-ac"),
     (9, "Agricultural"),
     (209, "Multi-Family (18)"),
     (140, "Low Density Residential 2 DD"),
     (251, "Park/Open Space"),
     (132, "Limited Commercial"),
     (375, "Residential 1 (21,780 Sq. Ft.-15,0"),
     (193, "Single Family Residential 12000 sq"),
     (74, "City Center Frame"),
     (251, "Park"),
     (362, "Schools"),
     (251, "Open Space & Parks"),
     (269, "Public Facility"),
     (204, "Multi-Family Residential"),
     (20, "Business & Advanced Technology"),
     (49, "Central Business Mixed-Use Ove"),
     (11, "Aviation Business Center"),
     (269, "Public"),
     (228, "Commercial/Business Employment Cen"),
     (20, "Employment Park 1"),
     (93, "Government"),
     (96, "Heavy Manufacturing");
insert into comp_plan_types values
     (269, "Public and Private Facilities and"),
     (38, "General Commercial DD"),
     (419, "Waterfront"),
     (269, "Public/Semi-Public Use"),
     (56, "Community Facility"),
     (94, "Intensive Commercial"),
     (292, "R-30 (30000 sq ft)"),
     (221, "Neighborhood Commercial Center"),
     (251, "Park and Open Space"),
     (334, "R-20A Single Dwelling Unit"),
     (228, "Business"),
     (22, "Business/Industrial Park"),
     (400, "Residential 11-15du/ac, OP, CB, Li"),
     (322, "Residential Agriculture"),
     (264, "Center Institution"),
     (13, "Intersection Commercial"),
     (126, "Light Industry"),
     (386, "Low Density Single Family Resident"),
     (221, "Neighborhood Commercial"),
     (66, "SF-1 One Unit/Acre Maximum"),
     (228, "Employment Centers"),
     (251, "Parks/Open Space"),
     (74, "City Center Core"),
     (62, "Constrained Residential"),
     (204, "Multi-Family, R-2"),
     (221, "Neighborhood Market"),
     (269, "Public and Quasi-public facilities"),
     (334, "R-20 Single Dwelling Unit"),
     (322, "Residential-Agriculture"),
     (74, "City Center Commercial"),
     (221, "Neighborhood commercial"),
     (257, "Planned Residential"),
     (204, "Residential Multi-Family"),
     (160, "Medical Facilities"),
     (49, "Regional Commercial Mixed Use"),
     (56, "Community Facilities"),
     (99, "High Density Multi-Family Resident"),
     (187, "Mixed Use Planned Development"),
     (257, "Residential Planned Neighborhood"),
     (319, "Residential 2-5du/ac, unlocated Pa"),
     (204, "Multi Family"),
     (17, "Sensitive Area Buffer"),
     (13, "Auto/General Commercial"),
     (204, "Multi Family Residential"),
     (74, "Downtown Commercial SEA"),
     (68, "County Urban Res 12+/Acre"),
     (100, "High Density Residential DD"),
     (251, "Parks and Open Space");
insert into comp_plan_types values
     (251, "Public Parks"),
     (251, "Secondary Open Space"),
     (74, "Central Business District"),
     (63, "Convenience Commercial"),
     (76, "Downtown Residential Districts"),
     (418, "Lake"),
     (17, "Buffer"),
     (112, "Employment Area - Industrial"),
     (269, "Public Use"),
     (251, "Recreation"),
     (66, "Residential 1du/ac unlocated Open"),
     (20, "Employment Park 2"),
     (228, "Office-Professional"),
     (321, "Residential 6-10du/ac, Office-Prof"),
     (414, "Urban Housing Densities"),
     (228, "Employment Area - Office"),
     (251, "Housing / Open space"),
     (191, "Mobile Home Park"),
     (413, "Urban Growth Reserve"),
     (11, "Airport District"),
     (132, "Commercial Low Intensity"),
     (344, "Retirement Facility"),
     (251, "Recreational"),
     (66, "Single Family 1du/ac"),
     (418, "Railroad Rights-of-Way"),
     (386, "Single Family Low-Density Resident"),
     (88, "Fairgrounds"),
     (264, "Public-Institutional"),
     (264, "Public/Institutional"),
     (335, "Residential Reserve"),
     (178, "Mixed Medium Density Residential/C"),
     (25, "Center Office Residential"),
     (386, "Park - Single Family Low Density"),
     (251, "Parks"),
     (251, "Recreation/Open Space"),
     (376, "Rural Residential - 3 Units Per Ac"),
     (74, "Central Business"),
     (132, "Commercial, low impact"),
     (251, "Parks and Public Places"),
     (42, "Commercial Medium Intensity"),
     (193, "Medium density residential"),
     (210, "Multi-Family (12)"),
     (50, "Pedestrian-Oriented Mixed Use Comm"),
     (272, "Public Facility - Office"),
     (384, "Single Family Institution"),
     (13, "Automobile-Oriented District"),
     (65, "Corridor Commercial"),
     (171, "Mid-Rise Office District");
insert into comp_plan_types values
     (221, "Neighborhood Business Tourist"),
     (319, "Single Family 5du/ac SEA"),
     (269, "City Facilities"),
     (264, "Institutions"),
     (299, "Regional Business"),
     (412, "Urban Growth Area"),
     (53, "Common Wall Single Family (12)"),
     (114, "Industrial Tourist District Ov"),
     (135, "Local Business"),
     (201, "Multi-Family (36)"),
     (204, "Multi-Family, R-3"),
     (323, "Residential Commercial Center"),
     (393, "Residential High Density"),
     (60, "Community/Utility"),
     (131, "Light Manufacturing  DD"),
     (186, "Mixed Use Office"),
     (262, "Private Open Space"),
     (405, "Stuck River SPA"),
     (70, "Design District"),
     (13, "Interchange Commercial"),
     (131, "Light Manufacturing Transit Overla"),
     (251, "Linear Park"),
     (137, "Low Density Multifamily SEA"),
     (251, "Open space, parks, & public facili"),
     (305, "Residential Vacant Lots"),
     (381, "Single Family Estates 1.24du-ac"),
     (140, "Low density residential"),
     (140, "Low Density Residential(2 to 4 DU/"),
     (251, "Open space / Recreation"),
     (243, "Park - Single Family Medium Densit"),
     (251, "Quasi-Public Parks-Schools-Rec-Ope"),
     (403, "Special Study Area"),
     (74, "City Center Commercial SEA"),
     (36, "Civic-Educational"),
     (52, "Commerical / Housing"),
     (20, "Corporate Park"),
     (233, "Multi-Family (36) and or Commercia"),
     (217, "Multifamily Medium Mixed Use 14.52"),
     (269, "Public Use Facilities"),
     (305, "Residential - with Conditional Use"),
     (60, "Utility"),
     (228, "Commercial Office"),
     (54, "Common Wall Single Family (9)"),
     (358, "Conservancy Residential 1du-5ac"),
     (251, "Limited Open Space"),
     (157, "Master Planned Development"),
     (196, "Muckleshoot Tribe of Indians"),
     (213, "Multifamily High Mixed Use 29du-ac"),
     (48, "Office-Professional, Light Industr");
insert into comp_plan_types values
     (20, "Office Park"),
     (251, "Potential Parks"),
     (274, "Public Facility - Single Family Hi"),
     (269, "Public Uses"),
     (358, "Rural Residential"),
     (362, "School"),
     (12, "Airport Industrial"),
     (393, "High Density Residential TDR"),
     (153, "Manufacturing/Research Park"),
     (157, "Master Planned Development (Mixed"),
     (49, "Mixed-Use Node"),
     (49, "Mixed-Use Town Center"),
     (49, "Mixed Use Commercial Core, Future"),
     (240, "Park - Multi-Family Medium Density"),
     (418, "ROAD"),
     (406, "Study Area"),
     (10, "Airport"),
     (39, "Commercial / Recreational"),
     (393, "High density residential"),
     (418, "Highway"),
     (185, "MIxed Use"),
     (210, "Multi Family Residential 8-12du/ac"),
     (251, "Primary Open Space"),
     (275, "Public Facility - Single Family Me"),
     (299, "Regional Commercial SEA"),
     (358, "Rural Residential (1du/5ac basic)"),
     (359, "Ruston Planned Development"),
     (358, "Semi-Rural"),
     (411, "Tukwila Valley South"),
     (87, "Evergreen Highlands JPA"),
     (139, "Low Density Res 2 Transit Ovly"),
     (195, "Mt Rainier Vista SPA"),
     (209, "Multi Family Residential 12-24du/a"),
     (251, "Open Space Wilkeson Watershed"),
     (251, "Open Space/Critical Areas"),
     (241, "Park - Single Family High Density"),
     (259, "Potential Annexation Area"),
     (271, "Public Facility - Multi-Family Med"),
     (285, "Public/Institutional Mixed-Use"),
     (314, "Residential 2-5, 11-15, Office-Pro"),
     (257, "Residential Planned Developmen"),
     (398, "Single Family Urban Residential"),
     (418, "Water/Right of Way"),
     (22, "Business Park & Light Industri"),
     (39, "Commercial/Recreation"),
     (251, "Future Neighborhood Park"),
     (177, "High Density Residential Mixed"),
     (112, "Industrial Joint Planning Area"),
     (140, "Low Density Residential 1 C");
insert into comp_plan_types values
     (388, "Medium Density Res. Tourist Di"),
     (217, "Medium Density Residential Mix"),
     (186, "Mixed Use, R11-15, Office-Prof, Co"),
     (186, "Office Mixed-Use Overlay"),
     (48, "Planned Commercial/Industrial"),
     (157, "Planned Community"),
     (126, "Public Facility - Light Industrial"),
     (228, "Public Facility - Office Limited B"),
     (305, "RES"),
     (305, "Residential Non-Conforming Use"),
     (357, "Rural Protection"),
     (360, "Sand Point Reuse Area"),
     (366, "Sensitive"),
     (345, "Transit Facility");

# update all_parcels_with_cplan_jpf with reduced comp_plan_type codes

create index apwcpjpf_desc on all_parcels_with_cplan_jpf (desc_);

alter table all_parcels_with_cplan_jpf
     add column desc_trunc char(34),
     add column comp_plan_id int;

update all_parcels_with_cplan_jpf
     set desc_trunc = left(desc_,34);

create index apwcpjpf_desc_trunc on all_parcels_with_cplan_jpf (desc_trunc);

update all_parcels_with_cplan_jpf as p, comp_plan_types as c
     set p.comp_plan_id = c.comp_plan_id
     where p.desc_trunc = c.comp_plan_desc;

# Add use-specific columns to buildings data

alter table all_buildings_collapsed
     add column (development_constraint_type_id integer,
                 units_single_family integer,
                 units_multi_family integer,
                 sqft_single_family integer,
                 sqft_multi_family integer,
                 sqft_commercial integer,
                 sqft_government integer,
                 sqft_industrial integer);

create index all_buildings_collapsed_general_category 
     on all_buildings_collapsed (GeneralCategory);

update all_buildings_collapsed b, building_types t
     set b.development_constraint_type_id = t.development_constraint_type_id
     where b.GeneralCategory like t.building_type_description;

update all_buildings_collapsed
     set development_constraint_type_id = 1
     where GeneralCategory = "Mobile Home";

update all_buildings_collapsed 
     set units_single_family = NumberofUnits 
     where development_constraint_type_id = 1;
update all_buildings_collapsed 
     set units_single_family = 0 
     where development_constraint_type_id != 1 ;
update all_buildings_collapsed 
     set units_multi_family = NumberofUnits 
     where development_constraint_type_id = 2
          or development_constraint_type_id = 3;
update all_buildings_collapsed 
     set units_multi_family = 0 
     where development_constraint_type_id != 2
          and development_constraint_type_id != 3;

update all_buildings_collapsed 
     set sqft_single_family = BldgSF 
     where development_constraint_type_id = 1;
update all_buildings_collapsed 
     set sqft_single_family = 0 
     where development_constraint_type_id != 1;
update all_buildings_collapsed 
     set sqft_multi_family = BldgSF 
     where development_constraint_type_id = 2;
update all_buildings_collapsed 
     set sqft_multi_family = 0 
     where development_constraint_type_id != 2;
update all_buildings_collapsed 
     set sqft_commercial = BldgSF 
     where development_constraint_type_id = 3;
update all_buildings_collapsed 
     set sqft_commercial = 0 
     where development_constraint_type_id != 3;
update all_buildings_collapsed 
     set sqft_industrial = BldgSF 
     where development_constraint_type_id = 4;
update all_buildings_collapsed 
     set sqft_industrial = 0 
     where development_constraint_type_id != 4;
update all_buildings_collapsed 
     set sqft_government = BldgSF 
     where development_constraint_type_id = 5;
update all_buildings_collapsed 
     set sqft_government = 0 
     where development_constraint_type_id != 5;


# Aggregate building parts to parcels

drop table if exists all_buildings_by_parcel_jpf;
create table all_buildings_by_parcel_jpf
     select ID_PARCEL,
          group_concat(BuildingUseCode) as BuildingUseCodes,
          sum(BldgSF) as BldgSF,
          avg(Stories) as Stories,
          sum(Footprint) as Footprint,
          max(YearBuilt) as YearBuilt,
          sum(NumberofUnits) as NumberofUnits,
          sum(Bedrooms) as Bedrooms,
          sum(BathFull) as BathFull,
          sum(Bath3Qtr) as Bath3Qtr,
          sum(BathHalf) as BathHalf,
          sum(Bathrooms) as Bathrooms,
          group_concat(BuildingUseDescription) as BuildingUseDescriptions,
          group_concat(GeneralCategory) as GeneralCategories,
          sum(NumberofBuildingsParcel) as NumberofBuildingsParcel,
          sum(NumberofOutbuildingsParcel) as NumberofOutbuildingsParcel,
          sum(units_single_family) as units_single_family,
          sum(units_multi_family) as units_multi_family,
          sum(sqft_single_family) as sqft_single_family,
          sum(sqft_multi_family) as sqft_multi_family,
          sum(sqft_commercial) as sqft_commercial,
          sum(sqft_government) as sqft_government,
          sum(sqft_industrial) as sqft_industrial
     from all_buildings_collapsed
     group by ID_PARCEL;

create index abbpjpf_county_id_parcel on all_buildings_by_parcel_jpf (ID_PARCEL);

# Clear entries with no parcel id
delete from all_buildings_by_parcel_jpf where ID_PARCEL="0";

# Merge parcels, buildings, and comp plan data

drop table if exists all_parcels_merged_jpf;
create table all_parcels_merged_jpf
     select bg.ID_PARCEL as ID_PARCEL,
          bg.BuildingUseCodes as BuildingUseCodes,
          bg.BldgSF as BldgSF,
          bg.Stories as Stories,
          bg.Footprint as Footprint,
          bg.YearBuilt as YearBuilt,
          bg.NumberofUnits as NumberofUnits,
          bg.Bedrooms as Bedrooms,
          bg.BathFull as BathFull,
          bg.Bath3Qtr as Bath3Qtr,
          bg.BathHalf as BathHalf,
          bg.Bathrooms as Bathrooms,
          bg.BuildingUseDescriptions as BuildingUseDescriptions,
          bg.GeneralCategories as GeneralCategories,
          bg.NumberofBuildingsParcel as NumberofBuildingsParcel,
          bg.NumberofOutbuildingsParcel as NumberofOutbuildingsParcel,
          bg.units_single_family as units_single_family,
          bg.units_multi_family as units_multi_family,
          bg.sqft_single_family as sqft_single_family,
          bg.sqft_multi_family as sqft_multi_family,
          bg.sqft_commercial as sqft_commercial,
          bg.sqft_government as sqft_government,
          bg.sqft_industrial as sqft_industrial,
          pt.inurbanctr as InUrbanCenter,
          pt.genuse as GenericUse,
          pt.comp_plan_id as comp_plan_id,
          pt.desc_ as Description,
          pt.resdenl as MinResDensity,
          pt.resdenh as MaxResDensity,
          pc.Size_Acres as SizeAcres,
          pc.Size_SF as SizeSF
     from all_buildings_by_parcel_jpf as bg
          left join all_parcels_gis as pc
               on bg.ID_PARCEL = pc.ID_PARCEL
          left join all_parcels_with_cplan_jpf as pt
               on bg.ID_PARCEL = pt.parcelid;

create index all_parcels_merged_jpf_county_parcel on all_parcels_merged_jpf (ID_PARCEL);

# Export to a text file

select * from all_parcels_merged_jpf into outfile 'parcels_merged.tab';




drop table if exists constraint_plan_types;
create table constraints (
     constraint_id int primary key auto_increment,
     is_in_urban_center int,
     comprehensive_plan_description char(50),
     min_residential_density int,
     max_residential_density int
     );

insert into plan_types (is_in_urban_center,
                        comprehensive_plan_description, 
                        min_residential_density, 
                        max_residential_density)
     select distinct p.InUrbanCenter,
                     p.Description, 
                     p.MinResDensity, 
                     p.MaxResDensity  
     from all_parcels_merged_jpf p 
     order by p.Description;



     where p.Description = c.comp_plan_desc;
