create table buildings
select
grid_id,
year_built,
4 as building_type_id,
residential_units,
0 as sqft,
residential_improvement_value as improvement_value
from gridcells
where
residential_units > 0;

insert into buildings
select
grid_id,
year_built,
1 as building_type_id,
0 as residential_units,
commercial_sqft as sqft,
commercial_improvement_value as improvement_value
from gridcells
where
commercial_sqft > 0;

insert into buildings
select
grid_id,
year_built,
3 as building_type_id,
0 as residential_units,
industrial_sqft as sqft,
industrial_improvement_value as improvement_value
from gridcells
where
industrial_sqft > 0;

insert into buildings
select
grid_id,
year_built,
2 as building_type_id,
0 as residential_units,
governmental_sqft as sqft,
governmental_improvement_value as improvement_value
from gridcells
where
governmental_sqft > 0;

alter table buildings
add building_id int auto_increment primary key;
