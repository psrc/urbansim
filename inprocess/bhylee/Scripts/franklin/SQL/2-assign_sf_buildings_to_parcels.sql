

# Run this SECOND

use PSRC_2000_baseyear_joel;

# Randomly select wedges from parcels - do three random draws, 
# for up to 4 sf buildings per parcel

# Create random numbers
alter table gridcell_parcel_wedges 
     add (     random1 float, random2 float, random3 float, random4 float,
               weighted_random1 float, weighted_random2 float, 
               weighted_random3 float, weighted_random4 float    );
update gridcell_parcel_wedges 
     set random1=rand(), random2=rand(), random3=rand(), random4=rand();
# Weight random numbers by size of wedge
update gridcell_parcel_wedges 
     set weighted_random1=random1*parcel_fraction,
         weighted_random2=random2*parcel_fraction,
         weighted_random3=random3*parcel_fraction,
         weighted_random4=random4*parcel_fraction;
# Choose maximum of weighted random number, from each parcel, as indicator of chosen
drop table if exists parcels_from_wedges;
create table parcels_from_wedges
     (    index parcels_from_wedges_index_parcel_id (parcel_id)  )
     select parcel_id, 
            max(weighted_random1) as max_wtrand1,
            max(weighted_random2) as max_wtrand2,
            max(weighted_random3) as max_wtrand3,
            max(weighted_random4) as max_wtrand4
     from gridcell_parcel_wedges
     group by parcel_id;     
# Associate random-indicator with all wedges
drop table if exists wedges_new;
create table wedges_new
     select w.*, p.max_wtrand1, p.max_wtrand2, p.max_wtrand3, p.max_wtrand4 
          from gridcell_parcel_wedges as w 
          left join parcels_from_wedges as p 
               on w.parcel_id=p.parcel_id;
drop table if exists gridcell_parcel_wedges;
create table gridcell_parcel_wedges
     (    index wedges_index_wedge_id (gridcell_parcel_wedge_id),
          index wedges_index_parcel_id (parcel_id),
          index wedges_index_grid_id (grid_id)         )
     select * from wedges_new;

drop table if exists wedges_new;

# Identify chosen wedge from each parcel
alter table gridcell_parcel_wedges
     add (chosen_1 bit, chosen_2 bit, chosen_3 bit, chosen_4 bit);
update gridcell_parcel_wedges
     set chosen_1=(weighted_random1=max_wtrand1),
         chosen_2=(weighted_random2=max_wtrand2),
         chosen_3=(weighted_random3=max_wtrand3),
         chosen_4=(weighted_random4=max_wtrand4);
# Check totals to ensure only one is chosen from each parcel
drop table if exists check_choices;
create table check_choices
     select parcel_id,
            sum(chosen_1) as check_1,
            sum(chosen_2) as check_2,
            sum(chosen_3) as check_3,
            sum(chosen_4) as check_4
          from gridcell_parcel_wedges
          group by parcel_id;
delete from check_choices
     where (check_1=1) and (check_2=1) and (check_3=1) and (check_4=1);
select * from check_choices;
drop table check_choices;
# Create list of only chosen wedges
drop table if exists chosen_wedges;
create table chosen_wedges
     (    index chosen_wedges_index_wedge_id (gridcell_parcel_wedge_id),
          index chosen_wedges_index_parcel_id (parcel_id),
          index chosen_wedges_index_grid_id (grid_id)       )
     select * from gridcell_parcel_wedges
     where (   (chosen_1=TRUE) 
             | (chosen_2=TRUE) 
             | (chosen_3=TRUE) 
             | (chosen_4=TRUE)     );

# Get single-family residences

drop table if exists single_family_buildings;
create table single_family_buildings
     (    index single_family_buildings_index_building_id (building_id),
          index single_family_buildings_index_parcel_id (parcel_id)        )
     select * 
     from buildings
     where building_type="SF"
     order by parcel_id, building_id;

delete from single_family_buildings where parcel_id is null;

# Create an index of sf-building within each parcel
alter table single_family_buildings
     drop building_id;
alter table single_family_buildings
     add sfdu_id int auto_increment key;
     

# Check for multiple SF buildings on the same parcel
drop table if exists sf_buildings_on_parcel;
create table sf_buildings_on_parcel
     (    index sf_buildings_on_parcel_index_parcel_id (parcel_id)    )
     select parcel_id, 
            count(*) as number_sf_buildings,
            min(sfdu_id) as min_sfdu_id
     from single_family_buildings
     group by parcel_id;
drop table if exists sf_on_parcel_histogram;
create table sf_on_parcel_histogram
     select number_sf_buildings, count(*) as freq
     from sf_buildings_on_parcel
     group by number_sf_buildings;

# Develop sub-identifier for sf-building-on-parcel
drop table if exists single_family_buildings_new;
create table single_family_buildings_new
     (index single_family_buildings_index_sfdu_id (sfdu_id),
      index single_family_buildings_index_parcel_id (parcel_id))
     select b.*, p.min_sfdu_id
     from single_family_buildings as b
     left join sf_buildings_on_parcel as p
          on b.parcel_id=p.parcel_id;

drop table if exists single_family_buildings;
rename table single_family_buildings_new
     to single_family_buildings;

alter table single_family_buildings
     add sf_on_parcel_id int;

update single_family_buildings
     set sf_on_parcel_id = sfdu_id - min_sfdu_id + 1;

# Link grid_id to first-sf-buildings, then second, then third, then fourth...
drop table if exists single_family_buildings_1;
create table single_family_buildings_1
     (    index single_family_buildings_1_index_sfdu_id (sfdu_id),
          index single_family_buildings_1_index_parcel_id (parcel_id),
          index single_family_buildings_1_index_grid_id (grid_id)     )
     select b.*, w.grid_id
     from single_family_buildings as b
     left join gridcell_parcel_wedges as w
          on b.parcel_id=w.parcel_id
     where b.sf_on_parcel_id=1 and w.chosen_1=TRUE;
drop table if exists single_family_buildings_2;
create table single_family_buildings_2
     (    index single_family_buildings_2_index_sfdu_id (sfdu_id),
          index single_family_buildings_2_index_parcel_id (parcel_id),
          index single_family_buildings_2_index_grid_id (grid_id)     )
     select b.*, w.grid_id
     from single_family_buildings as b
     left join gridcell_parcel_wedges as w
          on b.parcel_id=w.parcel_id
     where b.sf_on_parcel_id=2 and w.chosen_2=TRUE;
drop table if exists single_family_buildings_3;
create table single_family_buildings_3
     (    index single_family_buildings_3_index_sfdu_id (sfdu_id),
          index single_family_buildings_3_index_parcel_id (parcel_id),
          index single_family_buildings_3_index_grid_id (grid_id)     )
     select b.*, w.grid_id
     from single_family_buildings as b
     left join gridcell_parcel_wedges as w
          on b.parcel_id=w.parcel_id
     where b.sf_on_parcel_id=3 and w.chosen_3=TRUE;
drop table if exists single_family_buildings_4;
create table single_family_buildings_4
     (    index single_family_buildings_4_index_sfdu_id (sfdu_id),
          index single_family_buildings_4_index_parcel_id (parcel_id),
          index single_family_buildings_4_index_grid_id (grid_id)     )
     select b.*, w.grid_id
     from single_family_buildings as b
     left join gridcell_parcel_wedges as w
          on b.parcel_id=w.parcel_id
     where b.sf_on_parcel_id=4 and w.chosen_4=TRUE;

# Join them together
insert into single_family_buildings_1
     select * from single_family_buildings_2;
insert into single_family_buildings_1
     select * from single_family_buildings_3;
insert into single_family_buildings_1
     select * from single_family_buildings_4;
drop table if exists single_family_buildings_2;
drop table if exists single_family_buildings_3;
drop table if exists single_family_buildings_4;

drop table if exists single_family_buildings;
rename table single_family_buildings_1
     to single_family_buildings;

# Attach parcel data on total building area and developed lot area

drop table if exists single_family_buildings_new;
create table single_family_buildings_new
     (    index index_sfdu_id (sfdu_id),
          index index_parcel_id (parcel_id),
          index index_grid_id (grid_id)      )
     select sf.*,
            p.built_sqft_tot as built_sqft_on_parcel,
            p.lot_sqft as lot_sqft_on_parcel,
            sf.built_sqft*p.lot_sqft/p.built_sqft_tot as building_lot_area
     from single_family_buildings as sf
     left join parcels as p
          on sf.parcel_id = p.parcel_id;

update single_family_buildings_new
     set building_lot_area = 0
     where built_sqft_on_parcel=0;
