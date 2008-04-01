

# Run this FOURTH

use PSRC_2000_baseyear_joel;

# Attach residential-unit data to buildings



# Get non-sf pseudo-buildings

drop table if exists non_sf_pseudo_buildings;
create table non_sf_pseudo_buildings
     (    index non_sf_pseudo_buildings_index_parcel_id (parcel_id)   )
     select group_concat(distinct left(replace(building_use,"Imputed - ",""),4)) as building_uses,
            max(year_built) as newest_year_built,
            min(year_built) as oldest_year_built,
            group_concat(distinct county) as counties,
            sum(built_sqft) as built_sqft_tot,
            max(impute_flag) as impute_flag,
            sum(imputed_sqft) as imputed_sqft_tot,
            max(parcel_code) as parcel_code,
            parcel_id as parcel_id,
            group_concat(distinct generic_use) as generic_uses,
            building_type as building_type,
            max(building_type_id) as building_type_id
     from buildings
     where building_type<>"SF"
     group by parcel_id, building_type;
delete from non_sf_pseudo_buildings where parcel_id is null;

alter table non_sf_pseudo_buildings
     add nsf_id int auto_increment primary key;

# Generate parcel-level mf data
drop table if exists mf_buildings_on_parcel;
create table mf_buildings_on_parcel
     (index index_parcel_id (parcel_id))
     select parcel_id as parcel_id,
            max(built_sqft_tot) as built_sqft_tot,
            max(imputed_sqft_tot) as imputed_sqft_tot
     from non_sf_pseudo_buildings
#     where building_type="MF" or building_type="GQ"
     group by parcel_id;

# Join with mf & sf units on parcel

# Join with sf units data
drop table if exists mf_buildings_on_parcel_1;
create table mf_buildings_on_parcel_1
     (index index_parcel_id (parcel_id))
     select mf.*,
            sf.number_sf_buildings as sf_units
     from mf_buildings_on_parcel as mf
     left outer join sf_buildings_on_parcel as sf
          on mf.parcel_id=sf.parcel_id;

update mf_buildings_on_parcel_1
     set sf_units=0
     where sf_units is null;
     
drop table if exists mf_buildings_on_parcel_2;
create table mf_buildings_on_parcel_2
     (    index index_parcel_id (parcel_id)  )
     select mf.*,
            p.residential_units as tot_units,
            p.residential_units - mf.sf_units as mf_units,
            p.built_sqft_tot as built_sqft_on_parcel,
            p.lot_sqft as lot_sqft_on_parcel
     from mf_buildings_on_parcel_1 as mf
     left outer join parcels as p
          on mf.parcel_id = p.parcel_id;

update mf_buildings_on_parcel_2
     set mf_units = 0,
         tot_units = 0
     where tot_units is null;

update mf_buildings_on_parcel_2
     set mf_units=tot_units
          where mf_units<0;

drop table if exists mf_buildings_on_parcel;
drop table if exists mf_buildings_on_parcel_1;
rename table mf_buildings_on_parcel_2
     to mf_buildings_on_parcel;

# Attach parcel-level res data back to pseudo-buildings
drop table if exists non_sf_pseudo_buildings_new;
create table non_sf_pseudo_buildings_new
     (    index index_nsf_id (nsf_id),
          index index_parcel_id (parcel_id)  )
     select nsf.*,
            p.built_sqft_tot as mf_sqft_on_parcel,
            p.mf_units as mf_units_on_parcel,
            p.built_sqft_on_parcel as tot_sqft_on_parcel,
            p.lot_sqft_on_parcel as lot_sqft_on_parcel
     from non_sf_pseudo_buildings as nsf
     left outer join mf_buildings_on_parcel as p
          on nsf.parcel_id = p.parcel_id;

drop table if exists non_sf_pseudo_buildings;
rename table non_sf_pseudo_buildings_new
     to non_sf_pseudo_buildings;

# Attach full parcels' pseudo-buildings to wedges
drop table if exists non_sf_pseudo_buildings_new;
create table non_sf_pseudo_buildings_new
     (    index index_grid_id (grid_id),
          index index_parcel_id (parcel_id),
          index index_gridcell_parcel_wedge_id (gridcell_parcel_wedge_id)  )
     select b.*,
            w.grid_id,
            w.parcel_fraction,
            w.gridcell_parcel_wedge_id
     from non_sf_pseudo_buildings as b
     left outer join gridcell_parcel_wedges as w
          on w.parcel_id = b.parcel_id;

drop table if exists non_sf_pseudo_buildings;
rename table non_sf_pseudo_buildings_new
     to non_sf_pseudo_buildings;

# delete no-parcel rows and fill in zeros
delete from non_sf_pseudo_buildings where parcel_id is null;
update non_sf_pseudo_buildings 
     set mf_sqft_on_parcel = 0
     where mf_sqft_on_parcel is null;
update non_sf_pseudo_buildings 
     set mf_units_on_parcel = 0
     where mf_units_on_parcel is null;


# compute units that should be on the pseudo-building's wedge
alter table non_sf_pseudo_buildings
     add (     sqft_proportion double,
               mf_units int(11));
update non_sf_pseudo_buildings
     set  mf_units = round(mf_units_on_parcel*parcel_fraction)
     where building_type = "MF" or building_type = "GQ";
update non_sf_pseudo_buildings
     set mf_units = 0
     where building_type <> "MF" and building_type <> "GQ";

# Combine with SF buildings

drop table if exists pseudo_buildings;
create table pseudo_buildings
     (    pseudo_building_id int auto_increment, 
               primary key (pseudo_building_id),
          building_uses longtext,
          year_built double,
          counties longtext,
          built_sqft double,
          impute_flag tinyint(4),
          imputed_sqft double,
          parcel_code varchar(10),
          parcel_id bigint(20),
          generic_uses longtext,
          building_type char(5),
          building_type_id int(11),
          sfdu_id int(11),
          nsf_id int(11),
          units int(11),
          tot_sqft_on_parcel double,
          lot_sqft_on_parcel int(11),
          grid_id int(11),
          parcel_fraction double(20,3),
          gridcell_parcel_wedge_id int(11),
          sqft_proportion double,
          bldg_lot_area double,
          index index_parcel_id (parcel_id),
          index index_grid_id (grid_id)      );

# insert single-family
insert into pseudo_buildings 
     (         building_uses,                year_built,                   counties, 
               built_sqft,                   impute_flag,                  imputed_sqft, 
               parcel_code,                  parcel_id,                    generic_uses,
               building_type,                building_type_id,             sfdu_id, 
               units,                        tot_sqft_on_parcel,           lot_sqft_on_parcel,
               grid_id    )
     select    left(replace(building_use,"Imputed - ",""),4), year_built,  county,
               built_sqft,                   impute_flag,                  imputed_sqft,
               parcel_code,                  parcel_id,                    generic_use,
               building_type,                building_type_id,             sfdu_id,
               1,                            built_sqft_on_parcel,         lot_sqft_on_parcel,
               grid_id
     from single_family_buildings;

# insert non-single-family
insert into pseudo_buildings
          (    building_uses,                year_built,                   counties,      
               built_sqft,                   impute_flag,                  imputed_sqft,
               parcel_code,                  parcel_id,                    generic_uses,  
               building_type,                building_type_id,             nsf_id, 
               units,                        tot_sqft_on_parcel,           lot_sqft_on_parcel,
               grid_id,                      parcel_fraction,              gridcell_parcel_wedge_id,     
               sqft_proportion     )
               
     select    building_uses,                newest_year_built,            counties,
               built_sqft_tot,               impute_flag,                  imputed_sqft_tot,
               parcel_code,                  parcel_id,                    generic_uses,
               building_type,                building_type_id,             nsf_id,
               mf_units,                     tot_sqft_on_parcel,           lot_sqft_on_parcel,
               grid_id,                      parcel_fraction,              gridcell_parcel_wedge_id,
               sqft_proportion
     from non_sf_pseudo_buildings;

# estimate lot area used by the building
update pseudo_buildings
     set bldg_lot_area = built_sqft*lot_sqft_on_parcel/tot_sqft_on_parcel;

# Get average FARs for nonzero-sqft buildings
drop table if exists floor_area_ratios;
create table floor_area_ratios
     select    count(*),
               building_type, 
               avg(tot_sqft_on_parcel/lot_sqft_on_parcel) as far,
               avg(built_sqft) as avg_sqft
     from pseudo_buildings
     where built_sqft<>0 and built_sqft is not null
     group by building_type;
select * from floor_area_ratios;

create index index_building_type
     on floor_area_ratios (building_type);

# Estimate building floor areas for zero-data
#update table pseudo_buildings as b, floor_area_ratios as f
#     set b.built_sqft = 


