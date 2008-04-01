# This script divides parcel-level data on single-family
# residences, multi-family buildings, and commercial,
# industrial, and government buildings up into a smaller
# geography, representing a union of parcels and gridcells.
# Variables include residential dwelling units, developed 
# land coverage (sqft), built-land coverage (i.e. footprint,
# sqft), and usable floor area (sqft).

# Run this FIRST

use PSRC_2000_baseyear_joel;

# Bring in building data
drop table if exists buildings;
create table buildings 
     select * from PSRC_2000_baseyear_parcels.buildings;
alter table buildings 
     add building_id int auto_increment primary key;

# convert parcel_id into a numeric column
alter table buildings 
     add parcel_code varchar(10);
update buildings 
     set parcel_code=parcel_id;
alter table buildings
     drop parcel_id;
alter table buildings
     add parcel_id bigint;
update buildings
     set parcel_id=cast(parcel_code as signed);
create index buildings_index_parcel_id 
     on buildings (parcel_id);

# make numeric column building_use_id
alter table buildings
     add building_use_id int;
update buildings
     set building_use_id=cast(building_use as signed);
create index buildings_index_building_use_id
     on buildings (building_use_id);

# combine imputed sqftages and make them NULL if zero
update buildings
     set built_sqft=imputed_sqft
     where built_sqft=0;
update buildings
     set built_sqft=NULL
     where built_sqft=0;

# Bring in parcel data
drop table if exists parcels;
create table parcels 
     select * from PSRC_2000_baseyear_parcels.parcels;

# convert parcel_id into a numeric column
alter table parcels 
     add parcel_code varchar(10);
update parcels 
     set parcel_code=parcel_id;
alter table parcels 
     drop parcel_id;
alter table parcels 
     add parcel_id bigint;
update parcels 
     set parcel_id=cast(parcel_code as signed);
create index parcels_index_parcel_id 
     on parcels (parcel_id);

# Set some nulls for bad data
update parcels
     set land_value=NULL
     where land_value=0;

# analyze the parcels table for duplicate parcel_id's
drop table if exists parcel_tabulations;
create table parcel_tabulations
     select parcel_id, count(*) as num, 
            group_concat(cast(land_use as char)) 
     from parcels 
     group by parcel_id 
     order by num desc;
# *** view it here before deleting ***
drop table if exists parcel_tabulations;

drop table if exists parcels_aggregated;
create table parcels_aggregated
     (parcel_id bigint(20), built_sqft int(11), improvement_value int(11),
      land_value int(11), lot_sqft int(11), acres double(8,3),
      residential_units int(11), residential_units_imputed double,
      year_built int(11), county mediumtext, city mediumtext,
      land_use_imputed_flag int(11), census_block varchar(18),
      census_tract varchar(18), taxexempt_binary tinyint(4),
      undevelopable int(11), year_built_imputed_flag int(11),
      zone int(11), parcel_code varchar(10))
     select parcel_id as parcel_id,
          sum(built_sqft) as built_sqft,
          sum(improvement_value) as improvement_value,
          sum(land_value) as land_value,
          sum(lot_sqft) as lot_sqft,
          sum(acres) as acres,
          sum(residential_units) as residential_units,
          sum(residential_units_imputed) as residential_units_imputed,
          max(year_built) as year_built,
          min(county) as county,
          min(city) as city,
          max(land_use_imputed_flag) as land_use_imputed_flag,
          min(census_block) as census_block,
          min(census_tract) as census_tract,
          min(taxexempt_binary) as taxexempt_binary,
          max(undevelopable) as undevelopable,
          max(year_built_imputed_flag) as year_built_imputed_flag,
          min(zone) as zone,
          min(parcel_code) as parcel_code
     from parcels
     group by parcel_id
     order by parcel_id;

create index parcels_index_parcel_id 
     on parcels_aggregated (parcel_id);

drop table if exists parcels;
rename table parcels_aggregated
     to parcels;


# Bring in gricell data
drop table if exists gridcells;
create table gridcells 
     (index gridcells_index_grid_id (grid_id))
     select * from GSPSRC_2000_baseyear_change_20060926.gridcells;

# Bring in parcel-wedge intersect data (i.e. wedges)
drop table if exists gridcell_parcel_wedges;
create table gridcell_parcel_wedges 
     (index wedges_index_parcel_id (parcel_id),
      index wedges_index_grid_id (grid_id))
     select * from PSRC_parcels_all_counties.parcel_fractions_in_gridcells;

# create identifier
alter table gridcell_parcel_wedges 
     add gridcell_parcel_wedge_id int auto_increment primary key;
create index wedges_index_wedge_id 
     on gridcell_parcel_wedges (gridcell_parcel_wedge_id);

# convert parcel_id to numeric
alter table gridcell_parcel_wedges 
     add parcel_code varchar(10);
update gridcell_parcel_wedges 
     set parcel_code=parcel_id;
alter table gridcell_parcel_wedges 
     drop parcel_id;
alter table gridcell_parcel_wedges 
     add parcel_id bigint;
update gridcell_parcel_wedges 
     set parcel_id=cast(parcel_code as signed);
#create index wedges_index_parcel_id 
#     on gridcell_parcel_wedges (parcel_id);
#create index wedges_index_grid_id 
#     on gridcell_parcel_wedges (grid_id);


# Get total building area within each parcel, and attach to parcel data

# aggregate building areas to parcel level
drop table if exists buildings_on_parcel;
create table buildings_on_parcel
     (    index index_parcel_id (parcel_id)  )
     select parcel_id as parcel_id,
            sum(built_sqft) as built_sqft_tot
     from buildings
     group by parcel_id;

# attach total building areas to other parcel data

drop table if exists parcels_new;
create table parcels_new
     select p.*,
            b.built_sqft_tot
     from parcels as p
     left join buildings_on_parcel b
          on b.parcel_id=p.parcel_id;

create index parcels_index_parcel_id 
     on parcels_new (parcel_id);

drop table if exists parcels;
rename table parcels_new
     to parcels;

