
create index households_from_synthesizer_HHID 
     on households_from_synthesizer (HHID);
create index households_from_synthesizer_TAZ 
     on households_from_synthesizer (TAZ);

create index households_from_synthesizer_PERSONS 
     on households_from_synthesizer (PERSONS);
create index households_from_synthesizer_HINC 
     on households_from_synthesizer (HINC);

# Create table of households sorted by TAZ, HH-size, and income,
# along with a new rank variable

drop table if exists hh_from_syn_2;
create table hh_from_syn_2
     like households_from_synthesizer;

alter table hh_from_syn_2
     add column fuzzy_income int,
     add column fuzzy_hhsize int;

# Insert sorted data

insert into hh_from_syn_2 (HHID, TAZ, SERIALNO, PUMA5, HINC, PERSONS, HHT, UNITTYPE, NOC, BLDGSZ, 
                           TENURE, hinccat1, hinccat2, hhagecat, hsizecat, hfamily, hunittype, 
                           hNOCcat, hwrkrcat, h0005, h0611, h1215, h1617, h1824, h2534, h3549, 
                           h5064, h6579, h80up, hworkers, hwork_f, hwork_p, huniv, hnwork, hretire, 
                           hpresch, hschpred, hschdriv, htypdwel, hownrent, hadnwst, hadwpst, 
                           hadkids, bucketBin, originalPUMA)
     select *
     from households_from_synthesizer
     order by TAZ, PERSONS, HINC;


# Disturb the rank variables a bit to introduce some randomness:

update hh_from_syn_2
     set fuzzy_income = round(HINC * (0.75+rand()/2)),
         fuzzy_hhsize = round(PERSONS * (0.75+rand()/2));

update hh_from_syn_2
     set fuzzy_hhsize = 1
     where fuzzy_hhsize < 1;

create index hh_from_syn_2_taz_size_inc
     on hh_from_syn_2 (TAZ, fuzzy_hhsize, fuzzy_income);

# Create a rank variable

drop table if exists hh_from_syn_3;
create table hh_from_syn_3
     like hh_from_syn_2;

alter table hh_from_syn_3
     add column new_id int primary key auto_increment,
     add column rank int;


insert into hh_from_syn_3 (HHID, TAZ, SERIALNO, PUMA5, HINC, PERSONS, HHT, UNITTYPE, NOC, BLDGSZ, 
                           TENURE, hinccat1, hinccat2, hhagecat, hsizecat, hfamily, hunittype, 
                           hNOCcat, hwrkrcat, h0005, h0611, h1215, h1617, h1824, h2534, h3549, 
                           h5064, h6579, h80up, hworkers, hwork_f, hwork_p, huniv, hnwork, hretire, 
                           hpresch, hschpred, hschdriv, htypdwel, hownrent, hadnwst, hadwpst, 
                           hadkids, bucketBin, originalPUMA, fuzzy_income, fuzzy_hhsize)
     select *
     from hh_from_syn_2
     order by TAZ, fuzzy_hhsize, fuzzy_income;

update hh_from_syn_3
     set rank = new_id;

create index hh_from_syn_3_TAZ
     on hh_from_syn_3 (TAZ);

drop table if exists hh_from_syn_2;

# Determine minimum rank within each taz

drop table if exists taz_hhs;
create table taz_hhs
     select TAZ,
            min(rank) as min_rank_in_taz
     from hh_from_syn_3
     group by TAZ;

create index taz_hhs_taz
     on taz_hhs (TAZ);

drop table if exists hh_from_syn_4;
create table hh_from_syn_4
     select h.*,
            t.min_rank_in_taz,
            0 as rank_within_taz
     from hh_from_syn_3 as h
     left join taz_hhs as t
          on h.TAZ = t.TAZ;

create index hh_from_syn_4_taz_rank
     on hh_from_syn_4 (TAZ, rank_within_taz);

# assign new rank within taz

update hh_from_syn_4
     set rank_within_taz = rank - min_rank_in_taz + 1;

drop table if exists hh_from_syn_3;

# Repeat this kind of exercise with residential units

# first, create a table of residential units from buildings

drop table if exists bldgs_2;

create table bldgs_2 (
     building_id int,
     parcel_id int,
     taz int,
     units int,
     total_value int,
     num_bedrooms int,
     bedrooms_per_unit int,
     value_per_unit int,
     fuzzy_bedrooms_per_unit int,
     fuzzy_value_per_unit int);

insert into bldgs_2
     select b.building_id as building_id,
            b.parcel_id as parcel_id,
            p.zone_id as taz,
            b.residential_units as units,
            b.total_value as total_value,
            b.number_of_bedrooms as num_bedrooms,
            b.number_of_bedrooms/b.residential_units as bedrooms_per_unit,
            b.total_value/b.residential_units as value_per_unit,
            NULL as fuzzy_bedrooms_per_unit,
            NULL as fuzzy_value_per_unit
     from buildings as b
     left join parcels as p
          on b.parcel_id = p.parcel_id
     where b.residential_units > 0;

update bldgs_2
     set fuzzy_bedrooms_per_unit = round(bedrooms_per_unit * (0.75+rand()/2)),
         fuzzy_value_per_unit = round(value_per_unit * (0.75+rand()/2));

update bldgs_2
     set fuzzy_bedrooms_per_unit = 1
     where fuzzy_bedrooms_per_unit < 1;

drop procedure if exists make_residential_units;
delimiter //
create procedure make_residential_units ()
     begin
          declare units_left int;
          select sum(units)
               from bldgs_2
               group by NULL
               into units_left;
          
          drop table if exists residential_units;
          create table residential_units (
               residential_unit_id int primary key auto_increment,
               building_id int,
               parcel_id int,
               taz int,
               unit_bedrooms int,
               unit_value int);
          
          while (not isnull(units_left)) do
               insert into residential_units (building_id, parcel_id, 
                                              taz, unit_bedrooms, 
                                              unit_value)
                    select building_id,
                           parcel_id,
                           taz,
                           fuzzy_bedrooms_per_unit,
                           fuzzy_value_per_unit
                    from bldgs_2;
               
               update bldgs_2
                    set units = units - 1;
               delete from bldgs_2
                    where units <= 0;
               
               select sum(units)
                    from bldgs_2
                    group by NULL
                    into units_left;
          end while;
     end//
delimiter ;

# the end condition doesn't work; need to monitor using:
#    select sum(units) from bldgs_2;
# or, when it gets really low:
#    select * from bldgs_2;
# and when it gets to empty, manually stop.

call make_residential_units ();

create index residential_units_taz_bedrooms_value
     on residential_units (taz, unit_bedrooms, unit_value);

drop table if exists res_units_2;
create table res_units_2 (
     residential_unit_id int,
     building_id int,
     parcel_id int,
     taz int,
     unit_bedrooms int,
     unit_value int,
     new_id int primary key auto_increment);

insert into res_units_2 (residential_unit_id, building_id, parcel_id, 
                         taz, unit_bedrooms, unit_value)
     select *
     from residential_units
     order by taz, unit_bedrooms, unit_value;

delete from res_units_2
     where taz is null or taz=0;


# Determine minimum rank within each taz

drop table if exists taz_units;
create table taz_units
     select taz,
            min(new_id) as min_rank_in_taz
     from res_units_2
     group by taz;

create index taz_units_taz
     on taz_units (TAZ);

drop table if exists res_units_3;
create table res_units_3
     select u.*,
            t.min_rank_in_taz,
            0 as rank_within_taz
     from res_units_2 as u
     left join taz_units as t
          on u.taz = t.taz;

create index res_units_3_taz_rank
     on res_units_3 (taz, rank_within_taz);

# assign new rank within taz

update res_units_3
     set rank_within_taz = new_id - min_rank_in_taz + 1;

drop table if exists res_units_2;

# Match residential units to households

drop table if exists households_with_res_units;

create table households_with_res_units
     select h.*,
            u.residential_unit_id,
            u.building_id,
            u.parcel_id,
            u.unit_bedrooms,
            u.unit_value
     from hh_from_syn_4 as h
     left join res_units_3 u
          on h.TAZ = u.taz
               and h.rank_within_taz = u.rank_within_taz;

# Match households to residential units

drop table if exists res_units_with_households;

create table res_units_with_households
     select u.*,
            h.HHID as household_id,
            h.HINC,
            h.PERSONS
     from res_units_3 as u
     left join hh_from_syn_4 h
          on h.TAZ = u.taz
               and h.rank_within_taz = u.rank_within_taz;

# Test the results

# Check for unplaced households:

select count(*) from households_with_res_units where residential_unit_id is null;
select taz, count(*) from households_with_res_units where residential_unit_id is null group by taz;

select count(*) from res_units_with_households where household_id is null;
select taz, count(*) from res_units_with_households where household_id is null group by taz;

# Create final households table

drop table if exists households;
create table households (
     household_id int,
     building_id int,
     parcel_id int,
     zone_id int,
     persons int,
     workers int,
     age_of_head int,
     income int,
     children int,
     race_id int,
     cars int);

insert into households
     select HHID,
            building_id,
            parcel_id,
            TAZ,
            PERSONS,
            hworkers,
            NULL,
            HINC,
            (h0005+h0611+h1215+h1617),
            NULL,
            hNOCcat
     from households_with_res_units;





