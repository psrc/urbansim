# this script matches establishment (businesses) to buildings
# Input:
#   est2000_rev: establishment of 2000, matched to 2000 PIN
#   est2000_0619new: establishment of 2000, with new NAICS code
#   employment_control_total_zone_2000_flattened - zonal employment control total by sector
#   parcels: 2005 parcels table (in psrc_2005_parcel_baseyear_flattened)
#   buildings: 2005 buildings table unrolled to 2000 (in psrc_2005_parcel_baseyear_data_prep_start)
#   corr_kit_sno: correspondent table mapping 2000 PIN to 2005 PIN for kitsap and snohomish county

#1. create internal parcel_id (matching to 2005) in est2000_rev table
drop table if exists est2000_rev;
create table est2000_rev select * from est2000_rev_original;
alter table est2000_rev
change parcel_id pin varchar(64),
add parcel_id int,
add id_parcel2000 varchar(64),
add id_parcel2005 varchar(64);

update est2000_rev set id_parcel2000 = concat(county, pin);
update est2000_rev set id_parcel2005 = id_parcel2000;

create index id_parcel2000_index on est2000_rev (id_parcel2000);

#mapping from 2000 PIN to 2005 PIN for Kitsap and Snohomish
#original corr_kitsap and corr_snohomish provided by Andrew Bjorn

#create table corr_kit_sno
#(id_parcel2005 varchar(64),
# id_parcel2000 varchar(64)
#);

#insert into corr_kit_sno
#select concat("035", SAPN) as id_parcel2005,
#concat("035", PIN) as id_parcel2000
#from corr_kitsap;

#insert into corr_kit_sno
#select concat("061", parcel_id) as id_parcel2005,
#concat("061", PID) as id_parcel2000
#from corr_snohomish;

#create index id_parcel2000_index on corr_kit_sno (id_parcel2000);

update est2000_rev e,  corr_kit_sno c
set e.id_parcel2005 = c.id_parcel2005
where e.id_parcel2000 = c.id_parcel2000;

create index id_parcel2005_index on est2000_rev (id_parcel2005);
create index id_parcel_index on psrc_2005_parcel_baseyear_flattened.parcels (id_parcel);

update est2000_rev e, psrc_2005_parcel_baseyear_flattened.parcels p
set e. parcel_id = p.parcel_id
where e.id_parcel2005 = p.id_parcel;

##update est2000_rev set id_parcel2005 =
##where county = 061;
##create index county_pin_index on est2000_rev(county, pin);
##alter table est2000_rev add parcel_id int;

##update est_match_bldg as e, parcels2000 as p
##set e.parcel_id = p.parcel_id
##where e.county = p.county
##and e.pin = p.pin;




#2. re-code sector, add two new variables (count of est in parcel, sum of jobs) in est table, and delete some records

# sector change (between 18 and 19)
alter table est2000_rev add psef_sector_rev_c int;
update est2000_rev
set psef_sector_rev_c=psef_sector;

update est2000_rev
set psef_sector_rev_c=18
where psef_sector=19;

update est2000_rev
set psef_sector_rev_c=19
where psef_sector=18;

alter table est2000_rev drop psef_sector, change psef_sector_rev_c psef_sector int;

# sector change
# private schools assigned "Education" (change from "education services")
#update est2000_rev set PSEF_sector = 18 where NAICS_rev = 611110;
# K-12 assigned to "Education"
#update est2000_rev set PSEF_sector = 18 where SIC=-9931;
# create a separate sector for government
#update est2000_rev set PSEF_sector = 19 where SIC=-9928 or SIC=-9929 or SIC=-9930 or SIC=-9932;


alter table est2000_rev add num_est_in_parcel int, add njobs_in_prcl int;

drop table if exists tmp_parcel_employer_counts;
create table tmp_parcel_employer_counts
select parcel_id, count(*) as ct1 from est2000_rev group by PARCEL_ID;

create index parcel_id_index on est2000_rev(parcel_id);
create index parcel_id_index on tmp_parcel_employer_counts(parcel_id);

update est2000_rev as e, tmp_parcel_employer_counts as c
set e.num_est_in_parcel = c.ct1
where e.parcel_id = c.parcel_id;
drop table tmp_parcel_employer_counts;

update est2000_rev set num_est_in_parcel = 0 where parcel_id <= 0 or parcel_id is null;

drop table if exists tmp_parcel_jobs_sum;
create table tmp_parcel_jobs_sum
select parcel_id, sum(jobs00) as sum1 from est2000_rev group by PARCEL_ID;

create index parcel_id_index1 on est2000_rev(parcel_id);
create index parcel_id_index1 on tmp_parcel_jobs_sum(parcel_id);

update est2000_rev as e, tmp_parcel_jobs_sum as s
set e.njobs_in_prcl = s.sum1
where e.parcel_id = s.parcel_id;
drop table tmp_parcel_jobs_sum;


# remove Temp Help Services from est table
drop table if exists est2000_rev_help_srv_DEL;
create table est2000_rev_help_srv_DEL
select * from est2000_rev where jobs00 = 0 or NAICS_rev = 561320;
delete from est2000_rev where jobs00 = 0 or NAICS_rev = 561320;

# Puget Sound Naval Shipyard employment in Bremerton (TAZ894) from Gov to Manuf
update est2000_rev
set psef_sector=4
where employer_id="GOVED1878";

#Deletes establishments and buildings with no parcel id and places them into new tables
## keep those establishments to be assign by their taz
drop table if exists est2000_rev_noparcelid;
create table est2000_rev_noparcelid
select * from est2000_rev where parcel_id <= 0 or parcel_id is null;

#delete from est2000_rev
#where parcel_id <= 0 or parcel_id is null;
## keep those establishments to be assign by their taz
update est2000_rev set parcel_id = -1 
where parcel_id <= 0 or parcel_id is null;


#3. add three new variables (conversion, count, sum) to building table and delete some records
drop table if exists buildings;
create table buildings 
select *, 0.9 * non_residential_sqft as building_sqft_10vac
from psrc_2005_parcel_baseyear_data_prep_start.buildings;

alter table buildings
##add building_sqft_10vac int, 
add sum_building_sqft_10vac_in_parcel int, 
add num_bldg_in_parcel int;

##ALTER TABLE buildings ADD building_id int auto_increment key;
##delete from buildings where year_built > 2000;
##delete from buildings where building_sqft <= 100;
# delete outbuildings
##delete from buildings where building_type_id = 14;

##update buildings set building_sqft_10vac = 0.9*building_sqft;

drop table if exists tmp_building_counts_in_parcel;
create table tmp_building_counts_in_parcel
select parcel_id, count(*) as ct2 from buildings group by PARCEL_ID;
create index parcel_id_index on buildings(parcel_id);
create index parcel_id_index on tmp_building_counts_in_parcel(parcel_id);

update buildings as e, tmp_building_counts_in_parcel as c
set e.num_bldg_in_parcel = c.ct2
where e.parcel_id = c.parcel_id;
drop table tmp_building_counts_in_parcel;

drop table if exists tmp_parcel_bldgsqft_sum;
create table tmp_parcel_bldgsqft_sum
select parcel_id, sum(building_sqft_10vac) as sum2 from buildings group by PARCEL_ID;
create index parcel_id_index1 on buildings(parcel_id);
create index parcel_id_index1 on tmp_parcel_bldgsqft_sum(parcel_id);

update buildings as e, tmp_parcel_bldgsqft_sum as s
set e.sum_building_sqft_10vac_in_parcel = s.sum2
where e.parcel_id = s.parcel_id;
drop table tmp_parcel_bldgsqft_sum;

drop table if exists buildings_noparcelid_DEL;
create table buildings_noparcelid_DEL
select * from buildings where parcel_id <= 0 or parcel_id is null;

delete from buildings
where parcel_id <= 0 or parcel_id is null;

# join est and bldg tables and assign join_flag, match_flag, and final_flag for further analyses
# union join

create index parcel_id_index2 on est2000_rev (parcel_id);
create index parcel_id_index2 on buildings (parcel_id);

drop table if exists tmp_est00_match_bldg2005;
create table tmp_est00_match_bldg2005
select e.*, b.building_id, b.parcel_id as building_parcel_id, b.year_built, b.non_residential_sqft, b.tax_exempt,
 b.building_type_id, b.building_sqft_10vac, b.sum_building_sqft_10vac_in_parcel, b.zone_id as building_taz,
 b.num_bldg_in_parcel
##, b.assessors_parcel_id
from est2000_rev as e left outer join buildings as b
on (e.parcel_id = b.parcel_id);

insert into tmp_est00_match_bldg2005
select e.*, b.building_id, b.parcel_id as building_parcel_id, b.year_built, b.non_residential_sqft,b.tax_exempt,
 b.building_type_id, b.building_sqft_10vac, b.sum_building_sqft_10vac_in_parcel, b.zone_id as building_taz,
 b.num_bldg_in_parcel
##, b.assessors_parcel_id
from est2000_rev as e right outer join buildings as b
on (e.parcel_id = b.parcel_id)
where e.parcel_id is null;


# create join_flag

alter table tmp_est00_match_bldg2005 add join_flag int; #add match_flag int, add final_flag int;

update tmp_est00_match_bldg2005 set join_flag = 1 where num_est_in_parcel = 1 and num_bldg_in_parcel = 1;
update tmp_est00_match_bldg2005 set join_flag = 2 where num_est_in_parcel > 1 and num_bldg_in_parcel = 1;
update tmp_est00_match_bldg2005 set join_flag = 3 where num_est_in_parcel = 1 and num_bldg_in_parcel > 1;
update tmp_est00_match_bldg2005 set join_flag = 4 where num_est_in_parcel > 1 and num_bldg_in_parcel > 1;
update tmp_est00_match_bldg2005 set join_flag = 5 where building_parcel_id is null;
update tmp_est00_match_bldg2005 set join_flag = 6 where parcel_id is null;
update tmp_est00_match_bldg2005 set join_flag = 7 where (parcel_id is null or parcel_id <=0) and employer_id is not null;

#4. update home_based flag

alter table tmp_est00_match_bldg2005 add home_based int default -1, add taz_est int;
update tmp_est00_match_bldg2005
set home_based = 1 #home_based
where join_flag in (1,2,3,4);


update tmp_est00_match_bldg2005
set home_based = 2 #non_home_based
where (join_flag in (1,2,3,4) and jobs00>2);

drop table if exists tmp_est00_match_bldg2005_nonhome;
create table tmp_est00_match_bldg2005_nonhome
select parcel_id from tmp_est00_match_bldg2005
where (join_flag in (1,2,3,4) and building_type_id in (0,1,2,3,5,7,8,9,10,13,14,15,16,17,18,20,21))
group by parcel_id;

create index parcel_id_index on tmp_est00_match_bldg2005(parcel_id);
create index parcel_id_index on tmp_est00_match_bldg2005_nonhome(parcel_id);

update tmp_est00_match_bldg2005 as org, tmp_est00_match_bldg2005_nonhome as nonhome
set org.home_based = 2
where join_flag in (1,2,3,4) and org.parcel_id = nonhome.parcel_id;

drop table tmp_est00_match_bldg2005_nonhome;


update tmp_est00_match_bldg2005
set taz_est = 1
where join_flag in (5,7);

update tmp_est00_match_bldg2005
set taz_est = 2
where (join_flag = 5 and psef_sector in (18,19)) or (join_flag in (1,2,3,4));


drop table if exists tmp_est00_match_bldg2005_flag123457;
create table tmp_est00_match_bldg2005_flag123457
select distinct employer_id, parcel_id, id_parcel2000, id_parcel2005, naics_rev, jobs00, PSEF_sector,
TAZ, join_flag, home_based, taz_est
from tmp_est00_match_bldg2005
where join_flag in (1,2,3,4,5,7);

drop table if exists tmp_est00_match_bldg2005_flag12bldg;
create table tmp_est00_match_bldg2005_flag12bldg
select distinct building_id, building_sqft_10vac, parcel_id
from tmp_est00_match_bldg2005
where join_flag in (1,2);

drop table if exists tmp_est00_match_bldg2005_flag123457_flag12bldg;
create table tmp_est00_match_bldg2005_flag123457_flag12bldg
select * from tmp_est00_match_bldg2005_flag123457;

alter table tmp_est00_match_bldg2005_flag123457_flag12bldg add building_id int, add building_sqft_10vac int;

create index parcel_id_index on tmp_est00_match_bldg2005_flag123457_flag12bldg(parcel_id);
create index parcel_id_index on tmp_est00_match_bldg2005_flag12bldg(parcel_id);

update tmp_est00_match_bldg2005_flag123457_flag12bldg as a, tmp_est00_match_bldg2005_flag12bldg as b
set a.building_id = b.building_id, a.building_sqft_10vac = b.building_sqft_10vac
where a.parcel_id = b.parcel_id;


#5. update NAICS code with est2000_new

alter table tmp_est00_match_bldg2005_flag123457_flag12bldg 
add decision varchar(64), 
add resource varchar (32),
add new_naics int, 
add psef_sector_he19 int, 
add psef_sector_he18 int, 
add new_psef_sector_he19 int,
add new_psef_sector_he18 int, 
add taz_psrc varchar(16), 
add taz_rev varchar(16), 
add primname varchar(64),
add category varchar(32), 
add sector_description varchar(64), 
drop psef_sector;

create index employer_id_index on tmp_est00_match_bldg2005_flag123457_flag12bldg (employer_id);
create index employer_id_index on est2000_0619new (employer_id);

update tmp_est00_match_bldg2005_flag123457_flag12bldg a, est2000_0619new b
set a.decision=b.decision, 
a.resource=b.resource, 
a.new_naics=b.new_naics,
 a.psef_sector_he19=b.psef_sector_he19, 
 a.psef_sector_he18=b.psef_sector_he18,
 a.new_psef_sector_he19=b.new_psef_sector_he19, 
 a.new_psef_sector_he18=b.new_psef_sector_he18,
 a.taz_psrc=b.taz_psrc, 
 a.taz_rev = b.TAZ_rev, 
 a.primname=b.primname,
 a.category=b.category, 
 a.sector_description=b.sector_description
where a.employer_id = b.employer_id;


#6. set impute_building_sqft flag (indicating whether building_sqft needs to be imputed)

alter table tmp_est00_match_bldg2005_flag123457_flag12bldg add impute_building_sqft_flag int;
update tmp_est00_match_bldg2005_flag123457_flag12bldg set impute_building_sqft_flag = 0;

#and ? or?
update tmp_est00_match_bldg2005_flag123457_flag12bldg set impute_building_sqft_flag = 1
where decision = 'PSRC_MATCHED';

update tmp_est00_match_bldg2005_flag123457_flag12bldg set impute_building_sqft_flag = 1
where new_psef_sector_he19 in (3,4,5,8,9,10,15,16,18,19);

update tmp_est00_match_bldg2005_flag123457_flag12bldg b, psrc_2005_parcel_baseyear_flattened.parcels p
set impute_building_sqft_flag = 1
where b.id_parcel2005 = p.id_parcel and p.tax_exempt_flag = 1;


#7. remove est from parcel if its taz doesnt match to the taz as in parcel
# and reset null values

alter table tmp_est00_match_bldg2005_flag123457_flag12bldg
add sector_id int, add zone_id int;
update tmp_est00_match_bldg2005_flag123457_flag12bldg
set sector_id = new_psef_sector_he19, zone_id = taz_rev;

create index id_parcel2005_index on tmp_est00_match_bldg2005_flag123457_flag12bldg (id_parcel2005);
create index id_parcel_index on psrc_2005_parcel_baseyear_flattened.parcels (id_parcel);

# unplace (into no parcel_id) those having parcel_id but falling into different tazs than
# ones parcels_ids in parcels table indicate: set taz to -1 for such establishments

update tmp_est00_match_bldg2005_flag123457_flag12bldg b, psrc_2005_parcel_baseyear_flattened.parcels p
set b.join_flag = 71, b.parcel_id = -1
where b.id_parcel2005 = p.id_parcel and b.zone_id <> p.zone_id;


# reset null values

update tmp_est00_match_bldg2005_flag123457_flag12bldg
set id_parcel2000 = -1 where id_parcel2000 is null;

update tmp_est00_match_bldg2005_flag123457_flag12bldg
set id_parcel2005 = -1 where id_parcel2005 is null;

update tmp_est00_match_bldg2005_flag123457_flag12bldg
set home_based = -1 where home_based is null;

update tmp_est00_match_bldg2005_flag123457_flag12bldg
set building_id = -1 where building_id is null;

update tmp_est00_match_bldg2005_flag123457_flag12bldg
set building_sqft_10vac = 0 where building_sqft_10vac is null;


#8. handle gap jobs (difference between control total and est)

-- #gap jobs
-- #flatten zonal control totals
-- drop table if exists employment_control_total_zone_2000_flattened;
-- create table employment_control_total_zone_2000_flattened (
-- zone_id int,
-- sector_id int,
-- jobs int
-- );

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 1 as sector_id, `1`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 2 as sector_id, `2`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 3 as sector_id, `3`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 4 as sector_id, `4`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 5 as sector_id, `5`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 6 as sector_id, `6`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 7 as sector_id, `7`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 8 as sector_id, `8`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 9 as sector_id, `9`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 10 as sector_id, `10`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 11 as sector_id, `11`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 12 as sector_id, `12`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 13 as sector_id, `13`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 14 as sector_id, `14`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 15 as sector_id, `15`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 16 as sector_id, `16`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 17 as sector_id, `17`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 18 as sector_id, `18`
-- FROM employment_control_total_zone_2000 e;

-- insert into employment_control_total_zone_2000_flattened
-- SELECT taz00, 19 as sector_id, `19`
-- FROM employment_control_total_zone_2000 e;

drop table if exists tmp_sum_jobs_flattened;
create table tmp_sum_jobs_flattened
select zone_id, sector_id, sum(jobs00) as jobs
from tmp_est00_match_bldg2005_flag123457_flag12bldg
group by zone_id, sector_id;

create index zone_id_sector_id_index on
employment_control_total_zone_2000_flattened (zone_id, sector_id);
create index zone_id_sector_id_index on tmp_sum_jobs_flattened (zone_id, sector_id);


## a bug in this script is fixed on 11/28/2007
insert into tmp_est00_match_bldg2005_flag123457_flag12bldg
(parcel_id, id_parcel2000, id_parcel2005, naics_rev, taz, home_based, taz_est, building_id,
building_sqft_10vac, decision, resource, new_naics, psef_sector_he19, psef_sector_he18, new_psef_sector_he19,
new_psef_sector_he18, taz_psrc, taz_rev, primname, category, sector_description,
zone_id, sector_id, jobs00, join_flag, impute_building_sqft_flag)
select -1 as parcel_id, '-1' as id_parcel2000, '-1' as id_parcel2005,
'' as naics_rev, t.zone_id as taz, -1 as home_based, 1 as taz_est, -1 as building_id,
-1 as building_sqft_10vac, '' as decsion, '' as resource, -1 as new_naics,
t.sector_id as psef_sector_he19, t.sector_id as psef_sector_he18, t.sector_id as new_psef_sector_he19,
t.sector_id as new_psef_sector_he18, t.sector_id as taz_psrc, t.sector_id as taz_rev, '' as primname,
'' as category, '' as sector_description, t.zone_id, t.sector_id, t.jobs - if(s.jobs is NULL,0, s.jobs) as jobs00, 73 as join_flag,
0 as impute_building_sqft_flag
from employment_control_total_zone_2000_flattened t left outer join tmp_sum_jobs_flattened s
on t.zone_id = s.zone_id and t.sector_id = s.sector_id
where t.jobs - if(s.jobs is NULL,0, s.jobs) >= 0;


#9. create building_sqft_per_job table

#avg by building_type_id for each zone
create index building_id_index on tmp_est00_match_bldg2005_flag123457_flag12bldg(building_id);
create index building_id_index on buildings(building_id);

drop table if exists building_sqft_per_job_zone;
create table building_sqft_per_job_zone
select taz as zone_id, building_type_id, avg(e.building_sqft_10vac / jobs00 ) as building_sqft_per_job
from tmp_est00_match_bldg2005_flag123457_flag12bldg e inner join buildings b
using (building_id) where e.building_id > 0 and e.building_sqft_10vac > 0 and e.jobs00 > 0
group by taz, building_type_id;

#region-wise average by building_type_id
drop table if exists building_sqft_per_job_region;
create table building_sqft_per_job_region
select building_type_id,avg(e.building_sqft_10vac / jobs00 ) as building_sqft_per_job
from tmp_est00_match_bldg2005_flag123457_flag12bldg e inner join buildings b
using (building_id) where e.building_id > 0 and e.building_sqft_10vac > 0 and e.jobs00 > 0
group by building_type_id;

#exhaustive combination of zone_id and building_type_id
drop table if exists building_sqft_per_job;
create table building_sqft_per_job
select zone_id, b2.building_type_id
from (select distinct zone_id from building_sqft_per_job_zone) as b1 inner join building_sqft_per_job_region b2;

alter table building_sqft_per_job add building_sqft_per_job float, add imputed_flag int;

create index zone_id_building_type_id_index on building_sqft_per_job (zone_id, building_type_id);
create index zone_id_building_type_id_index on building_sqft_per_job_zone (zone_id, building_type_id);
create index building_type_id_index on building_sqft_per_job_region (building_type_id);

update building_sqft_per_job t, building_sqft_per_job_zone b
set t.building_sqft_per_job = b.building_sqft_per_job, t.imputed_flag = 0
where t.zone_id = b.zone_id and t.building_type_id = b.building_type_id;

update building_sqft_per_job t, building_sqft_per_job_region b
set t.building_sqft_per_job = b.building_sqft_per_job, t.imputed_flag = 1
where t.building_sqft_per_job is null and t.building_type_id = b.building_type_id;


#10. create businesses table (view) from tmp_est00_match_bldg2005_flag123457_flag12bldg

alter table tmp_est00_match_bldg2005_flag123457_flag12bldg
add business_id int auto_increment primary key;

drop table if exists businesses;
create table businesses 
select business_id, parcel_id, id_parcel2000, id_parcel2005, jobs00, join_flag, 
home_based, taz_est, building_id, building_sqft_10vac, sector_id, zone_id,
impute_building_sqft_flag from tmp_est00_match_bldg2005_flag123457_flag12bldg;


## place sector 19 businesses (government) in zone 73 and 894 a made-up builidngs (2000001, 2000002)
update businesses set building_id = 2000001, parcel_id = 117628 where zone_id = 73;
update businesses set building_id = 2000002, parcel_id = 579749 where zone_id = 894 and sector_id in (15, 16, 18, 19);
