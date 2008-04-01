# Determine maximums by development type
#Assumes the presence of table development_type_maximums in the baseyear

##this file creates the following tables in the baseyear:
#devtypes_by_plantypes
#development_constraints_expanded
#constrained_development_types
#constraints_with_maximums
#gridcells_by_constraints
#gridcell_maximums

# use WFRC_1997_baseyear;

# Create a version of development_constraints that is searchable
# by development types bound by commas

drop table if exists development_constraints_expanded;
create table development_constraints_expanded
     select 
          constraint_id,
          city_id,
          county_id,
          is_in_wetland,
          is_outside_urban_growth_boundary,
          is_in_stream_buffer,
          is_on_steep_slope,
          is_in_floodplain,
          plantype_x,
          concat(',',devtype_x,',') as devtype_x
     from development_constraints;

# Create a table of development constraints crossed by development types,

drop table if exists constrained_development_types;
create table constrained_development_types
     select 
          dc.*,
          dt.*
     from development_constraints_expanded as dc
          inner join development_types as dt
               on dc.constraint_id=dc.constraint_id;

# Delete the development types that are prohibited by each constraint

delete from constrained_development_types
     where devtype_x like concat('%,',development_type_id,',%');

# Set maximums to zero if all development types are prohibited by the constraint

update constrained_development_types
     set max_units=0, 
          max_sqft=0
     where devtype_x like "%ALL%";

# Aggregate constraints, across ALLOWED development types, for the maximums

drop table if exists constraints_with_maximums;
create table constraints_with_maximums
     select constraint_id,
          max(max_units) as max_units,
          max(max_sqft) as max_sqft
     from constrained_development_types
     group by constraint_id;

# Combine maximums back into development constraints expanded table

alter table development_constraints_expanded
     add column max_units int,
     add column max_sqft int;

update development_constraints_expanded as dc
     left join constraints_with_maximums as cm
          on dc.constraint_id=cm.constraint_id
     set dc.max_units=cm.max_units,
          dc.max_sqft=cm.max_sqft;

# Create a table of gridcells by constraints

drop table if exists gridcells_by_constraints;
create table gridcells_by_constraints
     select gc.grid_id as grid_id,
          gc.development_type_id as g_development_type,
          gc.city_id as g_city_id,
          gc.county_id as g_county_id,
          if(gc.percent_wetland>0,1,0) as g_is_in_wetland,
          gc.is_outside_urban_growth_boundary as g_is_outside_ugb,
          if(gc.percent_stream_buffer>0,1,0) as g_is_in_stream_buffer,
          if(gc.percent_slope>0,1,0) as g_is_on_steep_slope,
          if(gc.percent_floodplain>0,1,0) as g_is_in_floodplain,
          gc.plan_type_id as g_plan_type_id,
          dc.constraint_id as constraint_id,
          dc.city_id as c_city_id,
          dc.county_id as c_county_id,
          dc.is_in_wetland as c_is_in_wetland,
          dc.is_outside_urban_growth_boundary as c_is_outside_ugb,
          dc.is_in_stream_buffer as c_is_in_stream_buffer,
          dc.is_on_steep_slope as c_is_on_steep_slope,
          dc.is_in_floodplain as c_is_in_floodplain,
          cast(dc.plantype_x as signed) as c_plan_type_id,
          dc.max_units as max_units,
          dc.max_sqft as max_sqft,
          1 as constraint_applies
     from gridcells as gc
          left join development_constraints_expanded as dc
               on gc.grid_id=gc.grid_id;

create index gridcells_by_constraints_grid_id_index
     on gridcells_by_constraints (grid_id);

# Identify constraints that don't apply to the gridcell
# Use the standard of a criterion both caring (i.e. not being -1)
# and failing to find a match with the gridcell;
# otherwise the constraint still applies.

update gridcells_by_constraints
     set constraint_applies=0
     where c_city_id<>-1 and c_city_id<>g_city_id;

update gridcells_by_constraints
     set constraint_applies=0
     where c_county_id<>-1 and c_county_id<>g_county_id;

update gridcells_by_constraints
     set constraint_applies=0
     where c_is_in_wetland<>-1 and c_is_in_wetland<>g_is_in_wetland;

update gridcells_by_constraints
     set constraint_applies=0
     where c_is_outside_ugb<>-1 and c_is_outside_ugb<>g_is_outside_ugb;

update gridcells_by_constraints
     set constraint_applies=0
     where c_is_in_stream_buffer<>-1 and c_is_in_stream_buffer<>g_is_in_stream_buffer;

update gridcells_by_constraints
     set constraint_applies=0
     where c_is_on_steep_slope<>-1 and c_is_on_steep_slope<>g_is_on_steep_slope;

update gridcells_by_constraints
     set constraint_applies=0
     where c_is_in_floodplain<>-1 and c_is_in_floodplain<>g_is_in_floodplain;

update gridcells_by_constraints
     set constraint_applies=0
     where c_plan_type_id<>-1 and c_plan_type_id<>g_plan_type_id;

# Delete non-applicable constraints

delete from gridcells_by_constraints
     where constraint_applies=0;

# Generate specification-based maximums by development type

drop table if exists development_type_maximums;
create table development_type_maximums
     select idt.development_type_id as development_type_id,
          max(udt.max_units) as max_units,
          max(udt.max_sqft) as max_sqft
     from (development_types as idt
     inner join initial_to_ultimate_development_types as iu
          on idt.development_type_id=iu.initial_development_type_id)
     inner join development_types as udt
          on iu.ultimate_development_type_id=udt.development_type_id
     group by idt.development_type_id;

# Aggregate to gridcells
     #note that inclusion of dev type isn't necessary, but useful for spot checking
drop table if exists gridcell_capacity;
create table gridcell_capacity
     select gc.grid_id,
          gc.g_development_type as development_type_id,
          if(min(gc.max_units)<dm.max_units, min(gc.max_units), dm.max_units) as max_units,
          if(min(gc.max_sqft)<dm.max_sqft, min(gc.max_sqft), dm.max_sqft) as max_sqft
     from gridcells_by_constraints as gc, development_type_maximums as dm
     where gc.g_development_type = dm.development_type_id
     group by gc.grid_id;     
create index gridcell_capacity_grid_id
     on gridcell_capacity (grid_id);     
     
