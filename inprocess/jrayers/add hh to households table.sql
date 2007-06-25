-- TAZes 597 and 598

-- TAZes 597 and 598 are adjacent to each other and
-- should contain a total of 2548 and 1373 households
-- respectively (according to block level household
-- counts from the 2000 census).
-- This portion of the script will randomly
-- draw households from the surrounding TAZes and copy
-- them into TAZes 597 and 598.

-- Create a new table of all households from the
-- surrounding TAZes
drop table if exists hh_for_597_598;
create table hh_for_597_598
select *
from households_from_synthesizer
where
  taz = 586 or
  taz = 587 or
  taz = 594 or
  taz = 596 or
  taz = 599 or
  taz = 600 or
  taz = 602 or
  taz = 604 or
  taz = 605;

-- Create a new table of 2548 randomly selected
-- households for TAZ 597
drop table if exists rand_hh_for_597;
create table rand_hh_for_597
select *
from hh_for_597_598
order by rand()
limit 2548;

-- Reset TAZ id
update rand_hh_for_597
set TAZ = 597;

-- Create a new table of 1373 randomly selected
-- households for TAZ 5978
drop table if exists rand_hh_for_598;
create table rand_hh_for_598
select *
from hh_for_597_598
order by rand()
limit 1373;

-- Reset TAZ id
update rand_hh_for_598
set TAZ = 598;


-- TAZ 765

-- This procedure repeats the above procedure for TAZ 765
-- Create a new table of all households from the
-- surrounding TAZes
drop table if exists hh_for_765;
create table hh_for_765
select *
from households_from_synthesizer
where
  taz = 761 or
  taz = 764 or
  taz = 766 or
  taz = 769;

-- Create a new table of 971 randomly selected
-- households for TAZ 765
drop table if exists rand_hh_for_765;
create table rand_hh_for_765
select *
from hh_for_765
order by rand()
limit 971;

-- Reset TAZ id
update rand_hh_for_765
set TAZ = 765;

-- Copy all original household records into
-- a new table
drop table if exists households_from_synthesizer_tmp;
create table households_from_synthesizer_tmp
select * from households_from_synthesizer;

-- Insert randomly selected records from TAZes
-- 597, 598, and 765
insert into households_from_synthesizer_tmp
select * from rand_hh_for_597;
insert into households_from_synthesizer_tmp
select * from rand_hh_for_598;
insert into households_from_synthesizer_tmp
select * from rand_hh_for_765;

-- Remove and re-number household id field
alter table households_from_synthesizer_tmp
drop column HHID;
alter table households_from_synthesizer_tmp
add HHID int auto_increment primary key;


-- Create new households_from_synthesizer table
drop table if exists households_from_synthesizer_new;
create table households_from_synthesizer_new
    (
     household_id int,
     building_id int,
     parcel_id int,
     zone_id int,
     persons int,
     workers int,
     age_of_head int,
     income int,
     children int,
     race_id int
    );

insert into households_from_synthesizer_new
     select HHID,
            -1,
            -1,
            TAZ,
            PERSONS,
            hworkers,
            -1,
            HINC,
            (h0005+h0611+h1215+h1617),
            -1
     from households_from_synthesizer_tmp;

-- Clean up temporary tables
drop table if exists hh_for_597_598;
drop table if exists hh_for_765;
drop table if exists rand_hh_for_597;
drop table if exists rand_hh_for_598;
drop table if exists rand_hh_for_765;
drop table if exists households_from_synthesizer_tmp;