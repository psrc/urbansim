#matching hh_res parcels to buildings

create table hb01_qno_parcel ENGINE = MyISAM
select QNO, id_parcel, parcel_id from hh_res;

create table hb02_parcel ENGINE = MyISAM
select id_parcel, parcel_id from hb01_QNO_parcel group by id_parcel;
#3851 unique id_parcel

create index id_parcel_id using btree on hb02_parcel (id_parcel);
create index parcel_id_id using btree on hb02_parcel (parcel_id);

create table hb03_parcel_buildings ENGINE = MyISAM
select h.id_parcel as id_parcel_h, h.parcel_id as parcel_id_h, b.* from hb02_parcel as h
left join psrc_2005_data_workspace.buildings as b
on h.parcel_id = b.parcel_id;
#4315 records of buildings

create table hb04_id_parcel_count ENGINE = MyISAM
select id_parcel, count(*) as number from hb03_parcel_buildings 
group by id_parcel order by number desc;
#3851 unique id_parcel; 240 id_parcel with multiple buildings

#####################################################################################

#matching hh_matched_parcels to buildings

create table hb11_qno_parcel (index QNO_id using btree (QNO), 
index parcelid_id using btree (parcelid)) ENGINE = MyISAM
select QNO, parcelid from hh_matched_parcels where PMATCH=1 and parcelid is not null;
#4231 households

create table hb12_parcel (index parcelid_id using btree (parcelid)) ENGINE = MyISAM
select parcelid, count(*) as number from hb11_qno_parcel group by parcelid
order by number desc, parcelid;
#4164 unique parcels

#psrc_2005_data_workspace.buildings
	1280332 records
	building_type_description:
		'Agriculture', 1846
		'Civic and Quasi-Public', 2740
		'Commercial', 19460
		'Condo Residential', 5659
		'Government', 926
		'Group Quarters', 430
		'Hospital / Convalescent Center', 825
		'Industrial', 3490
		'Military', 10
		'Mixed-Use', 611
		'Mobile Home', 30350
		'Multi-Family Residential', 38460
		'No Building', 185065
		'No Code', 15415
		'Office', 10854
		'Outbuilding', 40057
		'Park and Open Space', 7
		'Parking', 1149
		'Recreation', 1531
		'School', 2910
		'Single Family Residential', 906776
		'Transportation Communication Utilities', 1194
		'Warehousing', 10567

create table hb13_parcel_bldg ENGINE = MyISAM
select h.*, b.* from hb12_parcel as h left join psrc_2005_data_workspace.buildings as b
on h.parcelid = b.id_parcel where building_id is not null;
create index parcelid_id using btree on hb13_parcel_bldg (parcelid);
#5629 buildings matched

create table hb14_parcel_bldgnum (index parcelid_id using btree (parcelid)) ENGINE = MyISAM
select parcelid, count(*) as buildings from hb13_parcel_bldg
group by parcelid order by buildings desc;
#4138 unique parcels matched to buildings

create table hb15_parcel_onebldg ENGINE = MyISAM
select b.* from hb14_parcel_bldgnum as h left join psrc_2005_data_workspace.buildings as b
on h.parcelid = b.id_parcel where buildings = 1;
create index id_parcel_id using btree on hb15_parcel_onebldg (id_parcel);
#3850 parcels with only one building

select building_type_description, count(*) as number 
from hb15_parcel_onebldg group by building_type_description;
	'Civic and Quasi-Public', 1
	'Commercial', 18
	'Condo Residential', 111
	'Hospital / Convalescent Center', 4
	'Industrial', 3
	'Mixed-Use', 4
	'Mobile Home', 24
	'Multi-Family Residential', 404
	'No Building', 115
	'No Code', 7
	'Office', 10
	'Outbuilding', 2
	'Recreation', 10
	'School', 2
	'Single Family Residential', 3134
	'Warehousing', 1

create table hb16_parcel_onebldg_res (index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select * from hb15_parcel_onebldg where building_type_description = 'Condo Residential'
or building_type_description = 'Hospital / Convalescent Center'
or building_type_description = 'Mixed-Use' or building_type_description = 'Mobile Home'
or building_type_description = 'Multi-Family Residential'
or building_type_description = 'Single Family Residential';
#3681 parcels with only one building with residential use

create table hb17_parcel_multibldg ENGINE = MyISAM
select b.* from hb14_parcel_bldgnum as h left join psrc_2005_data_workspace.buildings as b
on h.parcelid = b.id_parcel where buildings > 1;
create index id_parcel_id using btree on hb17_parcel_multibldg (id_parcel);
#1779 buildings matched to 288 parcels with multiple buildings

select building_type_description, count(*) as number 
from hb17_parcel_multibldg group by building_type_description;
	'Civic and Quasi-Public', 6
	'Commercial', 31
	'Condo Residential', 32
	'Group Quarters', 2
	'Hospital / Convalescent Center', 4
	'Industrial', 4
	'Mobile Home', 1070
	'Multi-Family Residential', 191
	'No Code', 40
	'Office', 10
	'Outbuilding', 106
	'Parking', 6
	'Recreation', 28
	'School', 7
	'Single Family Residential', 220
	'Transportation Communication Utilities', 1
	'Warehousing', 21

create table hb18_parcel_multibldg_res (index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select * from hb17_parcel_multibldg where building_type_description = 'Condo Residential'
or building_type_description = 'Hospital / Convalescent Center'
or building_type_description = 'Mixed-Use' or building_type_description = 'Mobile Home'
or building_type_description = 'Multi-Family Residential'
or building_type_description = 'Single Family Residential';
#1517 residential buildings on 272 parcels with multiple buildings

create table hb19_parcel_multibldg_resnum ENGINE = MyISAM
select id_parcel, count(*) as number from hb18_parcel_multibldg_res group by id_parcel
order by number;
create index id_parcel_id using btree on hb19_parcel_multibldg_resnum (id_parcel);

create table hb20_parcel_multibldg_res_onebldg (index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select h.* from hb19_parcel_multibldg_resnum as a left join hb18_parcel_multibldg_res as h
on a.id_parcel = h.id_parcel where a.number = 1;
#154 parcels with multiple buildings with only one residential building

create table hb21_parcel_multibldg_res_multibldg (index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select h.* from hb19_parcel_multibldg_resnum as a left join hb18_parcel_multibldg_res as h
on a.id_parcel = h.id_parcel where a.number > 1;
#1363 residential buildings on 118 parcels with multiple residential buildings

create table hb22_parcel_multibldg_res_multibldg1st (index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select * from hb21_parcel_multibldg_res_multibldg where building_sqft > 700 group by id_parcel;
#117 parcels matched to the 1st building on the list with more than 700sqft

create table hb23_parcel_bldg_res (index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select a.* from hb16_parcel_onebldg_res as a
union all
select b.* from hb20_parcel_multibldg_res_onebldg as b
union all
select c.* from hb22_parcel_multibldg_res_multibldg1st as c;
#3952 parcels matched to residential buildings

create table hb24_QNO_parcel_bldg_res ENGINE = MyISAM
select a.*, b.* from hb11_qno_parcel as a left join hb23_parcel_bldg_res as b
on a.parcelid = b.id_parcel where building_id is not null;
create index QNO_id using btree on hb24_QNO_parcel_bldg_res (QNO);
#4002 households matched to residential buildings

#####################################################################################

create table hh_res_buildings ENGINE = MyISAM
select b.*, a.building_id, a.parcel_id, c.children, d.income from hb24_QNO_parcel_bldg_res as a
left join hh_matched_parcels as b on a.QNO = b.QNO
left join h01_children as c on a.QNO = c.QNO
left join h02_income as d on a.QNO = d.QNO
where a.QNO is not null;

#####################################################################################

create table households_for_estimation_temp ENGINE = MyISAM
select QNO as household_id, HHNUMPPL as persons, WRKRS2 as workers, income, children,
HHNUMVEH as cars, parcel_id, building_id from hh_res_buildings;

alter table households_for_estimation_temp add column age_of_head int after workers,
add column race_id int after children, add column in_control int;

update households_for_estimation_temp set household_id = 6000000+household_id, 
age_of_head = -1, race_id = -1, in_control = 1;

#####################################################################################

#match building attributes with household survey attributes
create table hh4est_1 (index QNO_id using btree (QNO), index building_id_id using btree (building_id),
index parcel_id_id using btree (parcel_id), index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select b.*, c.children, d.income,
a.building_id, a.parcel_id, a.outbuilding_flag, a.building_sqft, a.stories, a.footprint_sqft, 
a.year_built, a.building_quality, a.building_condition, a.residential_units, a.number_of_bedrooms, 
a.number_of_bathrooms, a.building_use, a.building_use_description, a.building_type_id, a.building_type_description, 
a.generic_building_type_id, a.generic_building_type_description, a.county_id, a.county as county_bldg, a.id_subparcel, 
a.id_parcel, a.subparcel_flag, a.attributed_parcel_sqft, a.total_value, a.tax_exempt, a.is_duplicate
from hb24_QNO_parcel_bldg_res as a
left join hh_matched_parcels as b on a.QNO = b.QNO
left join h01_children as c on a.QNO = c.QNO
left join h02_income as d on a.QNO = d.QNO
where a.QNO is not null;

#match with parcel attributes
create table hh4est_2 (index QNO_id using btree (QNO), index building_id_id using btree (building_id),
index parcel_id_id using btree (parcel_id), index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select a.*, 
b.land_value, b.improvement_value, b.tax_exempt_flag, b.parcel_sqft, b.parcel_sqft_in_gis, b.x_coord_sp as x_coord_sp_parcel,
b.y_coord_sp as y_coord_sp_parcel, b.x_coord_utm, b.y_coord_utm, b.grid_id, b.zone_id, b.census_block, b.city, b.city_id, 
b.is_inside_urban_growth_boundary, b.id_plat, b.plan_type_id, b.plan_type_description, b.num_building_records
from hh4est_1 as a left join psrc_2005_data_workspace.parcels as b on a.id_parcel = b.id_parcel;

create table hh4est_r (index QNO_id using btree (QNO), index building_id_id using btree (building_id),
index parcel_id_id using btree (parcel_id), index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select QNO, HHNUMVEH, HHNUMPPL, WRKRS2, CHOMEOWN, CHOMETYP, CHOMEAGE, CHOMEYR, CHOMEARE, CHOMEAR2, HOMEADDR, HOMECITY,
HOMESTAT, HOMEZIP, County, children, income, building_id, parcel_id, outbuilding_flag, building_sqft, stories,
footprint_sqft, year_built, residential_units, number_of_bedrooms, number_of_bathrooms, building_use, 
building_use_description, building_type_id, building_type_description, generic_building_type_id,
generic_building_type_description, id_subparcel, id_parcel, attributed_parcel_sqft, total_value, tax_exempt,
land_value, improvement_value, tax_exempt_flag, parcel_sqft, parcel_sqft_in_gis, city, is_inside_urban_growth_boundary,
num_building_records from hh4est_2;

#####################################################################################

#hb16 to hb24 from above but with only 'Condo Residential','Multi-Family Residential', and 'Single Family Residential'

#####################################################################################


create table hb16x_parcel_onebldg_res (index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select * from hb15_parcel_onebldg where building_type_description = 'Condo Residential'
or building_type_description = 'Multi-Family Residential'
or building_type_description = 'Single Family Residential';
#3649 parcels with only one building with residential use

create table hb18x_parcel_multibldg_res (index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select * from hb17_parcel_multibldg where building_type_description = 'Condo Residential'
or building_type_description = 'Multi-Family Residential'
or building_type_description = 'Single Family Residential';
#443 residential buildings on 243 parcels with multiple buildings

create table hb19x_parcel_multibldg_resnum ENGINE = MyISAM
select id_parcel, count(*) as number from hb18x_parcel_multibldg_res group by id_parcel
order by number;
create index id_parcel_id using btree on hb19x_parcel_multibldg_resnum (id_parcel);

create table hb20x_parcel_multibldg_res_onebldg (index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select h.* from hb19x_parcel_multibldg_resnum as a left join hb18x_parcel_multibldg_res as h
on a.id_parcel = h.id_parcel where a.number = 1;
#144 parcels with multiple buildings with only one residential building

create table hb21x_parcel_multibldg_res_multibldg (index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select h.* from hb19x_parcel_multibldg_resnum as a left join hb18x_parcel_multibldg_res as h
on a.id_parcel = h.id_parcel where a.number > 1;
#299 residential buildings on 99 parcels with multiple residential buildings

create table hb22x_parcel_multibldg_res_multibldg1st (index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select * from hb21x_parcel_multibldg_res_multibldg where building_sqft > 700 group by id_parcel;
#99 parcels matched to the 1st building on the list with more than 700sqft

create table hb23x_parcel_bldg_res (index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select a.* from hb16x_parcel_onebldg_res as a
union all
select b.* from hb20x_parcel_multibldg_res_onebldg as b
union all
select c.* from hb22x_parcel_multibldg_res_multibldg1st as c;
#3892 parcels matched to residential buildings

create table hb24x_QNO_parcel_bldg_res ENGINE = MyISAM
select a.*, b.* from hb11_qno_parcel as a left join hb23x_parcel_bldg_res as b
on a.parcelid = b.id_parcel where building_id is not null;
create index QNO_id using btree on hb24x_QNO_parcel_bldg_res (QNO);
#3939 households matched to residential buildings

create table hh_resx_buildings ENGINE = MyISAM
select b.*, a.building_id, a.parcel_id, c.children, d.income from hb24x_QNO_parcel_bldg_res as a
left join hh_matched_parcels as b on a.QNO = b.QNO
left join h01_children as c on a.QNO = c.QNO
left join h02_income as d on a.QNO = d.QNO
where a.QNO is not null;
create index parcel_id_id using btree on hh_resx_buildings (parcel_id);
 
#add grid_id
create table hh_resx_buildings_grid ENGINE = MyISAM
select a.*, b.grid_id from hh_resx_buildings as a left join psrc_2005_data_workspace.parcels as b on a.parcel_id = b.parcel_id;

create table householdsx_for_estimation_temp ENGINE = MyISAM
select QNO as household_id, grid_id, HHNUMPPL as persons, WRKRS2 as workers, income, children,
HHNUMVEH as cars, parcel_id, building_id from hh_resx_buildings_grid;

alter table householdsx_for_estimation_temp add column age_of_head int after workers,
add column race_id int after children, add column in_control int;

update householdsx_for_estimation_temp set household_id = 6000000+household_id, 
age_of_head = -1, race_id = -1, in_control = 1;

#match building attributes with household survey attributes
create table hh4est_1x (index QNO_id using btree (QNO), index building_id_id using btree (building_id),
index parcel_id_id using btree (parcel_id), index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select b.*, c.children, d.income,
a.building_id, a.parcel_id, a.outbuilding_flag, a.building_sqft, a.stories, a.footprint_sqft, 
a.year_built, a.building_quality, a.building_condition, a.residential_units, a.number_of_bedrooms, 
a.number_of_bathrooms, a.building_use, a.building_use_description, a.building_type_id, a.building_type_description, 
a.generic_building_type_id, a.generic_building_type_description, a.county_id, a.county as county_bldg, a.id_subparcel, 
a.id_parcel, a.subparcel_flag, a.attributed_parcel_sqft, a.total_value, a.tax_exempt, a.is_duplicate
from hb24x_QNO_parcel_bldg_res as a
left join hh_matched_parcels as b on a.QNO = b.QNO
left join h01_children as c on a.QNO = c.QNO
left join h02_income as d on a.QNO = d.QNO
where a.QNO is not null;

#match with parcel attributes
create table hh4est_2x (index QNO_id using btree (QNO), index building_id_id using btree (building_id),
index parcel_id_id using btree (parcel_id), index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select a.*, 
b.land_value, b.improvement_value, b.tax_exempt_flag, b.parcel_sqft, b.parcel_sqft_in_gis, b.x_coord_sp as x_coord_sp_parcel,
b.y_coord_sp as y_coord_sp_parcel, b.x_coord_utm, b.y_coord_utm, b.grid_id, b.zone_id, b.census_block, b.city, b.city_id, 
b.is_inside_urban_growth_boundary, b.id_plat, b.plan_type_id, b.plan_type_description, b.num_building_records
from hh4est_1x as a left join psrc_2005_data_workspace.parcels as b on a.id_parcel = b.id_parcel;

create table hh4est_rx (index QNO_id using btree (QNO), index building_id_id using btree (building_id),
index parcel_id_id using btree (parcel_id), index id_parcel_id using btree (id_parcel)) ENGINE = MyISAM
select QNO, HHNUMVEH, HHNUMPPL, WRKRS2, CHOMEOWN, CHOMETYP, CHOMEAGE, CHOMEYR, CHOMEARE, CHOMEAR2, HOMEADDR, HOMECITY,
HOMESTAT, HOMEZIP, County, children, income, building_id, parcel_id, outbuilding_flag, building_sqft, stories,
footprint_sqft, year_built, residential_units, number_of_bedrooms, number_of_bathrooms, building_use, 
building_use_description, building_type_id, building_type_description, generic_building_type_id,
generic_building_type_description, id_subparcel, id_parcel, attributed_parcel_sqft, total_value, tax_exempt,
land_value, improvement_value, tax_exempt_flag, parcel_sqft, parcel_sqft_in_gis, city, is_inside_urban_growth_boundary,
num_building_records from hh4est_2x;


#####################################################################################
