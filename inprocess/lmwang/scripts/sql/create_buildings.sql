## re-create buildings from psrc_2005_data_revised_2 and psrc_2005_data_workspace:

create database psrc_2005_parcel_baseyear_data_prep_buildings;
use psrc_2005_parcel_baseyear_data_prep_buildings;

create table building_qualities
select county, building_quality from psrc_2005_data_revised_2.building b1
group by county, building_quality
order by county, building_quality;

alter table building_qualities
add building_quality_id int auto_increment key first,
add index (county, building_quality);

alter table psrc_2005_data_revised_2.building add index (county, building_use);
alter table psrc_2005_data_workspace.building_use_correspondences add index (county, building_use);

drop table if exists buildings;
create table buildings
select building_id, parcel_id, id_parcel as assessor_parcel_id, c.building_type_id, q.building_quality_id,
building_sf as building_sqft, stories, footprint, number_of_units as residential_units,
bedrooms as _bedrooms, bathrooms as _bathrooms,
year_built, tax_exempt
from psrc_2005_data_revised_2.building b
 inner join psrc_2005_data_workspace.building_use_correspondences c using (county, building_use)
 inner join psrc_2005_parcel_baseyear_data_prep_buildings.building_qualities q using (county, building_quality);

drop table if exists buildings_summary_by_parcel;
create table buildings_summary_by_parcel
select parcel_id, count(*) as num_of_buildings,
sum(building_sqft) as total_building_sqft,
sum(footprint) as total_footprint
from buildings
group by parcel_id;

##split parcel_area to building portion to footprint, split improvement_value portion to building_sf
alter table buildings
  add land_area int after footprint,
  add non_residential_sqft int after building_sqft,
  add sqft_per_unit int after residential_units,
  add improvement_value int after year_built,
  add index (parcel_id);

alter table buildings_summary_by_parcel add index (parcel_id);
alter table psrc_2005_data_revised_2.parcel add index (parcel_id);

update buildings b
  inner join buildings_summary_by_parcel s using (parcel_id)
  inner join psrc_2005_data_revised_2.parcel p on b.parcel_id = p.parcel_id
set b.land_area = p.parcel_size_sf * b.footprint / s.total_footprint,
    b.improvement_value = p.improvement_value_parcel * b.building_sqft / s.total_building_sqft
;

## calc non_residential_sqft and sqft_per_unit, copied from Joel's script psrc_properly_format_baseyear_tables.sql

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


#delete from building where building_sf is negative
delete from buildings where building_sqft < 0;  # 3 buildings removed

## impute land_area according to density constraints and improvement_value:

alter table buildings add _alloted_parcel_sqft int after land_area;
update buildings set _alloted_parcel_sqft = land_area;

drop table if exists development_constraints_flattened;
create table development_constraints_flattened
select plan_type_id,
min(if(constraint_type='units_per_acre', minimum, 2e30)) as min_upa,
max(if(constraint_type='units_per_acre', maximum, 0)) as max_upa,
min(if(constraint_type='far', minimum, 2e30)) as min_far,
max(if(constraint_type='far', maximum, 0)) as max_far,

sum(if(constraint_type='units_per_acre' and generic_land_use_type_id=1, minimum, 0)) as glu1_min_upa,
sum(if(constraint_type='units_per_acre' and generic_land_use_type_id=1, maximum, 0)) as glu1_max_upa,
sum(if(constraint_type='far' and generic_land_use_type_id=1, minimum, 0)) as glu1_min_far,
sum(if(constraint_type='far' and generic_land_use_type_id=1, maximum, 0)) as glu1_max_far,

sum(if(constraint_type='units_per_acre' and generic_land_use_type_id=2, minimum, 0)) as glu2_min_upa,
sum(if(constraint_type='units_per_acre' and generic_land_use_type_id=2, maximum, 0)) as glu2_max_upa,
sum(if(constraint_type='far' and generic_land_use_type_id=2, minimum, 0)) as glu2_min_far,
sum(if(constraint_type='far' and generic_land_use_type_id=2, maximum, 0)) as glu2_max_far,

sum(if(constraint_type='units_per_acre' and generic_land_use_type_id=3, minimum, 0)) as glu3_min_upa,
sum(if(constraint_type='units_per_acre' and generic_land_use_type_id=3, maximum, 0)) as glu3_max_upa,
sum(if(constraint_type='far' and generic_land_use_type_id=3, minimum, 0)) as glu3_min_far,
sum(if(constraint_type='far' and generic_land_use_type_id=3, maximum, 0)) as glu3_max_far,

sum(if(constraint_type='units_per_acre' and generic_land_use_type_id=4, minimum, 0)) as glu4_min_upa,
sum(if(constraint_type='units_per_acre' and generic_land_use_type_id=4, maximum, 0)) as glu4_max_upa,
sum(if(constraint_type='far' and generic_land_use_type_id=4, minimum, 0)) as glu4_min_far,
sum(if(constraint_type='far' and generic_land_use_type_id=4, maximum, 0)) as glu4_max_far,

sum(if(constraint_type='units_per_acre' and generic_land_use_type_id=5, minimum, 0)) as glu5_min_upa,
sum(if(constraint_type='units_per_acre' and generic_land_use_type_id=5, maximum, 0)) as glu5_max_upa,
sum(if(constraint_type='far' and generic_land_use_type_id=5, minimum, 0)) as glu5_min_far,
sum(if(constraint_type='far' and generic_land_use_type_id=5, maximum, 0)) as glu5_max_far,

sum(if(constraint_type='units_per_acre' and generic_land_use_type_id=6, minimum, 0)) as glu6_min_upa,
sum(if(constraint_type='units_per_acre' and generic_land_use_type_id=6, maximum, 0)) as glu6_max_upa,
sum(if(constraint_type='far' and generic_land_use_type_id=6, minimum, 0)) as glu6_min_far,
sum(if(constraint_type='far' and generic_land_use_type_id=6, maximum, 0)) as glu6_max_far,

sum(if(constraint_type='units_per_acre' and generic_land_use_type_id=7, minimum, 0)) as glu7_min_upa,
sum(if(constraint_type='units_per_acre' and generic_land_use_type_id=7, maximum, 0)) as glu7_max_upa,
sum(if(constraint_type='far' and generic_land_use_type_id=7, minimum, 0)) as glu7_min_far,
sum(if(constraint_type='far' and generic_land_use_type_id=7, maximum, 0)) as glu7_max_far,

sum(if(constraint_type='units_per_acre' and generic_land_use_type_id=8, minimum, 0)) as glu8_min_upa,
sum(if(constraint_type='units_per_acre' and generic_land_use_type_id=8, maximum, 0)) as glu8_max_upa,
sum(if(constraint_type='far' and generic_land_use_type_id=8, minimum, 0)) as glu8_min_far,
sum(if(constraint_type='far' and generic_land_use_type_id=8, maximum, 0)) as glu8_max_far

from psrc_2005_parcel_baseyear_change_20080606.development_constraints
group by plan_type_id;

alter table psrc_2005_parcel_baseyear_change_20080606.parcels
  add index (parcel_id), add index (plan_type_id);
alter table development_constraints_flattened add index (plan_type_id);


## impute land_area according to density constraints and improvement_value:
### 1. SFH
###    a. no change if improvement_value > 200k
###    b. shrink land_area for parcels with existing dev density below 1/2.5
###       of the max_density in development constraint
### 2. MFH
###    a. shrink land_area for parcels with existing dev density below 1/2.5
###       of the max_density in development constraint


## SFH
update
#select b.*, 43560*residential_units/c.max_upa as land_area_imputed, p.plan_type_id, c.max_upa from
  buildings b
  inner join psrc_2005_parcel_baseyear_change_20080606.parcels p using (parcel_id)
  inner join development_constraints_flattened c using (plan_type_id)
set land_area = 43560*residential_units/c.max_upa
where b.improvement_value < 200000 and b.building_type_id = 19 and
residential_units/(land_area / 43560) * 2.5 < c.max_upa
and b.residential_units > 0;

## MFH
update
#select b.*, 43560*residential_units/c.max_upa as land_area_imputed, p.plan_type_id, c.max_upa from
  buildings b
  inner join psrc_2005_parcel_baseyear_change_20080606.parcels p using (parcel_id)
  inner join development_constraints_flattened c using (plan_type_id)
set land_area = 43560*residential_units/c.max_upa
where b.building_type_id in (4, 12) and
residential_units/(land_area / 43560) * 2.5 < c.max_upa
and b.residential_units > 0;


## add average/premium to building_qualities
SELECT * FROM building_qualities b;
alter table building_qualities add quality_string varchar(8) default 'average', add is_premium int default 0;

update building_qualities
set quality_string='premium', is_premium=1
where building_quality in ('comm-6', 'comm-7', 'comm-8',
                           'res-8', 'res-9', 'res-10', 'res-11', 'res-12', 'res-13', 'res-20',
                           'Good', 'Very Good', 'Excellent',
                              'Good Plus','Very Good Plus',
                              'Exc',      'VGd'
 );

# Condo/Commercial:

#2  LOW COST
#3  LOW/AVERAGE
#4  AVERAGE
#5  AVERAGE/GOOD
#6  GOOD
#7  GOOD/EXCELLENT
#8  EXCELLENT
#
#Residential:
#
#1  Cabin
#2  Substandard
#3  Poor
#4  Low
#5  Fair
#6  Low Average
#7  Average
#8  Good
#9  Better
#10 Very Good
#11 Excellent
#12 Luxury
#13 Mansion
#20 Exceptional Properties

alter table buildings drop is_premium;
alter table buildings add is_premium int default 0 after building_quality_id;
alter table buildings add index (building_quality_id);

update buildings b inner join building_qualities q using (building_quality_id)
set b.is_premium = q.is_premium;

