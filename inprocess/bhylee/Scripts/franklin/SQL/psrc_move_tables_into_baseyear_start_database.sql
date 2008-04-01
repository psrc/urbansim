

use psrc_2005_parcel_baseyear_start;

create table households
     like psrc_2005_data_workspace.households;

insert into households
     select * from psrc_2005_data_workspace.households;

create table buildings
     like psrc_2005_data_workspace.buildings;

insert into buildings
     select * from psrc_2005_data_workspace.buildings;

create table parcels
     like psrc_2005_data_workspace.parcels;

insert into parcels
     select * from psrc_2005_data_workspace.parcels;

create table households_for_estimation
     like psrc_2005_data_workspace.households_for_estimation;

insert into households_for_estimation
     select * from psrc_2005_data_workspace.households_for_estimation;

create table building_types
     like psrc_2005_data_workspace.building_types;

insert into building_types
     select * from psrc_2005_data_workspace.building_types;

create table generic_building_types
     like psrc_2005_data_workspace.generic_building_types;

insert into generic_building_types
     select * from psrc_2005_data_workspace.generic_building_types;

create table land_use_types
     like psrc_2005_data_workspace.land_use_types;

insert into land_use_types
     select * from psrc_2005_data_workspace.land_use_types;

create table development_templates
     like psrc_2005_data_workspace.development_templates;

insert into development_templates
     select * from psrc_2005_data_workspace.development_templates;

create table development_template_components
     like psrc_2005_data_workspace.development_template_components;

insert into development_template_components
     select * from psrc_2005_data_workspace.development_template_components;

create table development_constraints
     like psrc_2005_data_workspace.development_constraints;

insert into development_constraints
     select * from psrc_2005_data_workspace.development_constraints;

create table target_vacancies
     like psrc_2005_data_workspace.target_vacancies;

insert into target_vacancies
     select * from psrc_2005_data_workspace.target_vacancies;




create table zones
     like psrc_2005_parcel_baseyear.zones;

insert into zones
     select * from psrc_2005_parcel_baseyear.zones;

drop table psrc_2005_parcel_baseyear.zones;

create table travel_data
     like psrc_2005_parcel_baseyear.travel_data;

insert into travel_data
     select * from psrc_2005_parcel_baseyear.travel_data;

drop table psrc_2005_parcel_baseyear.travel_data;

create table urbansim_constants
     like psrc_2005_parcel_baseyear.urbansim_constants;

insert into urbansim_constants
     select * from psrc_2005_parcel_baseyear.urbansim_constants;

drop table psrc_2005_parcel_baseyear.urbansim_constants;

create table gridcells
     like psrc_2005_parcel_baseyear.gridcells;

insert into gridcells
     select * from psrc_2005_parcel_baseyear.gridcells;

drop table psrc_2005_parcel_baseyear.gridcells;

create table jobs
     like psrc_2005_parcel_baseyear.jobs;

insert into jobs
     select * from psrc_2005_parcel_baseyear.jobs;

drop table psrc_2005_parcel_baseyear.jobs;

create table employment_sectors
     like psrc_2005_parcel_baseyear.employment_sectors;

insert into employment_sectors
     select * from psrc_2005_parcel_baseyear.employment_sectors;

drop table psrc_2005_parcel_baseyear.employment_sectors;

create table employment_adhoc_sector_groups
     like psrc_2005_parcel_baseyear.employment_adhoc_sector_groups;

insert into employment_adhoc_sector_groups
     select * from psrc_2005_parcel_baseyear.employment_adhoc_sector_groups;

drop table psrc_2005_parcel_baseyear.employment_adhoc_sector_groups;

create table employment_adhoc_sector_group_definitions
     like psrc_2005_parcel_baseyear.employment_adhoc_sector_group_definitions;

insert into employment_adhoc_sector_group_definitions
     select * from psrc_2005_parcel_baseyear.employment_adhoc_sector_group_definitions;

drop table psrc_2005_parcel_baseyear.employment_adhoc_sector_group_definitions;




