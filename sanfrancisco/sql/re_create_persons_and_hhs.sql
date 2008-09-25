SELECT * FROM sanfrancisco_baseyear_change_20080121.business b;

create database sanfrancisco_baseyear_change_20080125;

create table scenario_information
SELECT * FROM sanfrancisco_baseyear_change_20080121.scenario_information s;
SELECT * FROM persons p order by rand() limit 100;

select household_id, count(*) from persons group by household_id having count(*) > 1;

SELECT * FROM persons p where household_id between 32385 and 32485;

create table households
select household_id, household_size as persons, zone_id as homestaz,
household_size, adults, age_of_head, nfulltime, nparttim as nparttime, autos,
income as income, race_id, zone_id
from persons group by household_id;

create index household_id_index on households(household_id);
create index household_id_index on persons(household_id);

# set the age_of_head and race_id of household to that of the head of the household
update households h inner join persons p using (household_id)
set h.age_of_head = p.age_of_head, h.race_id = p.race_id
where p.relat = 1;

alter table households add building_id int default -1;

SELECT * FROM households h order by rand() limit 100;

update sanfrancisco_baseyear_start.scenario_information set parent_database_url='sanfrancisco_baseyear_change_20080125';
create table households SELECT * FROM sanfrancisco_baseyear_change_20080125.households h;
create table households_syn SELECT * FROM sanfrancisco_baseyear_change_20080121.households_syn h;

create table households_for_estimation
SELECT * FROM households h where building_id > 0 order by rand() limit 5000;

select * from households where building_id <= 0;

alter table households change building_id building_id int;
alter table households_for_estimation change building_id building_id int;
describe sanfrancisco_baseyear_change_20080121.households;

update households set income = income /1000;
update households_for_estimation set income = income /1000;
select persons, count(*) from households_for_estimation group by persons;

SELECT count(*) FROM psrc_2005_parcel_baseyear_data_prep_business_zip.jobs j;
SELECT count(*) FROM psrc_2005_parcel_baseyear_flattened.jobs j;

SELECT * FROM sanfrancisco_baseyear_change_20080121.business b;

create database sanfrancisco_baseyear_change_20080129;
create table scenario_information
SELECT * FROM sanfrancisco_baseyear_change_20080125.scenario_information s;

create table development_event_history
SELECT * FROM sanfrancisco_baseyear_flattened.development_event_history d;

SELECT * FROM development_event_history d;
create table development_event_history
SELECT * FROM sanfrancisco_baseyear_change_20071120.buildings b
where year_built >=1990;


create index blklot_index on development_event_history_backup (blklot);
create index mapblklot_index on development_event_history_backup (mapblklot);

create index building_id_index on development_event_history_backup (building_id);
create index parcel_id_index on development_event_history_backup (parcel_id);

create index building_id_index on sanfrancisco_baseyear_flattened.buildings  (building_id);
create index blklot_index on sanfrancisco_baseyear_flattened.buildings  (blklot(10));
create index parcel_id_index on sanfrancisco_baseyear_flattened.parcels  (parcel_id);
create index blklot_index on sanfrancisco_baseyear_flattened.parcels  (blklot(10));

select d.* from development_event_history_backup d left outer join sanfrancisco_baseyear_flattened.buildings b
  using (blklot)
where b.blklot is null;

select count(*) from development_event_history d;

select d.* from development_event_history_backup d left outer join sanfrancisco_baseyear_flattened.parcels b
  using (parcel_id)
where b.parcel_id is null;

alter table development_event_history add scheduled_year int;
update development_event_history set scheduled_year = year_built;
update sanfrancisco_baseyear_start.scenario_information set parent_database_url='sanfrancisco_baseyear_change_20080129';

create table development_event_history
SELECT * FROM sanfrancisco_baseyear_change_20080129.development_event_history d;

show tables;

SELECT * FROM building_use_classification b;


