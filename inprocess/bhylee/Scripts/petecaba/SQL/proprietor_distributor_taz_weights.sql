# Input table: taz_weight_countyname
# Create TAZ_WEIGHTS table for proprietors distrubutor (pierce county test database)

create table taz_weights (TAZ double, AGRICULTURE DOUBLE, CONSTRUCTION DOUBLE, EDUCATION_HIGHER DOUBLE,
 FEDERAL_CIVILIAN DOUBLE, FEDERAL_MILITARY DOUBLE, FIRES DOUBLE, MANUFACTURING DOUBLE, MINING DOUBLE,
 PUBLIC_ADMINISTRATION DOUBLE, RETAIL_TRADE DOUBLE, STATE_AND_LOCAL DOUBLE, TRANSPORTATION_COMM_ELECT_GAS_SAN DOUBLE,
 WHOLESALE_TRADE DOUBLE, SERVICES DOUBLE, EDUCATION_K_12 DOUBLE, COUNTY varchar(3));

# Be sure to change the name of the taz_weights_countyname table according to the county
insert into taz_weights (TAZ) 
 select distinct TAZ 
 from prelim_taz_weights;
 
alter table taz_weights add unique index tz_index(taz);

update taz_weights set county = '061';

# Agriculture Sector Code 1

create temporary table agriculture select taz, agriculture, 1 as sector_code 
 from prelim_taz_weights
;

update agriculture as a 
inner join control_totals_by_sector as b 
on a.sector_code = b.sector_code
set a.agriculture = a.agriculture/b.job_sum 
where b.sector_code = 1
;

# Construction Sector Code 2

create temporary table construction select taz, construction, 2 as sector_code
 from prelim_taz_weights
;

update construction as a 
inner join control_totals_by_sector as b 
on a.sector_code = b.sector_code
set a.construction = a.construction/b.job_sum 
where b.sector_code = 2;

# Education K-12 Sector Code 3

create temporary table education_k_12 select taz, education_k_12, 3 as sector_code
 from prelim_taz_weights;
 
update education_k_12 as a 
inner join control_totals_by_sector as b 
on a.sector_code = b.sector_code
set a.education_k_12 = a.education_k_12/b.job_sum 
where b.sector_code = 3;

# Federal, Civilian Sector Code 4

create temporary table federal_civilian select taz, federal_civilian, 4 as sector_code
 from prelim_taz_weights;

update federal_civilian as a 
inner join control_totals_by_sector as b 
on a.sector_code = b.sector_code
set a.federal_civilian = a.federal_civilian/b.job_sum 
where b.sector_code = 4;

# Federal, Mililtary Sector Code 5

create temporary table federal_military select taz, federal_military, 5 as sector_code
 from prelim_taz_weights;

update federal_military as a 
inner join control_totals_by_sector as b 
on a.sector_code = b.sector_code
set a.federal_military = a.federal_military/b.job_sum 
where b.sector_code = 5;

# FIRES Sector Code 6

create temporary table fires select taz, fires, 6 as sector_code
 from prelim_taz_weights;

update fires as a 
inner join control_totals_by_sector as b 
on a.sector_code = b.sector_code
set a.fires = a.fires/b.job_sum 
where b.sector_code = 6;

# Manufacturing Sector Code 7

create temporary table manufacturing select taz, manufacturing, 7 as sector_code
 from prelim_taz_weights;

update manufacturing as a 
inner join control_totals_by_sector as b 
on a.sector_code = b.sector_code
set a.manufacturing = a.manufacturing/b.job_sum 
where b.sector_code = 7;

# Public Administration Sector Code 8

create temporary table public_administration select taz, public_administration, 8 as sector_code
 from prelim_taz_weights;

update public_administration as a 
inner join control_totals_by_sector as b 
on a.sector_code = b.sector_code
set a.public_administration = a.public_administration/b.job_sum 
where b.sector_code = 8;

# Retail Trade Sector Code 9 

create temporary table retail_trade select taz, retail_trade, 9 as sector_code
 from prelim_taz_weights;

update retail_trade as a 
inner join control_totals_by_sector as b 
on a.sector_code = b.sector_code
set a.retail_trade = a.retail_trade/b.job_sum 
where b.sector_code = 9;

# Services Sector Code 10

create temporary table services select taz, services, 10 as sector_code
 from prelim_taz_weights;

update services as a 
inner join control_totals_by_sector as b 
on a.sector_code = b.sector_code
set a.services = a.services/b.job_sum 
where b.sector_code = 10;

# State and Local Sector Code 11

create temporary table state_and_local select taz, state_and_local, 11 as sector_code
 from prelim_taz_weights;

update state_and_local as a 
inner join control_totals_by_sector as b 
on a.sector_code = b.sector_code
set a.state_and_local = a.state_and_local/b.job_sum 
where b.sector_code = 11;

# Transportation Comm Sector Code 12

create temporary table transportation_comm_elect_gas_san select taz, transportation_comm_elect_gas_san, 12 as sector_code
 from prelim_taz_weights;

update transportation_comm_elect_gas_san as a 
inner join control_totals_by_sector as b 
on a.sector_code = b.sector_code
set a.transportation_comm_elect_gas_san = a.transportation_comm_elect_gas_san/b.job_sum 
where b.sector_code = 12;

# Wholesale Trade Sector Code 13

create temporary table wholesale_trade select taz, wholesale_trade, 13 as sector_code
 from prelim_taz_weights;

update wholesale_trade as a 
inner join control_totals_by_sector as b 
on a.sector_code = b.sector_code
set a.wholesale_trade = a.wholesale_trade/b.job_sum 
where b.sector_code = 13;

# Education Higher Sector Code 14

create temporary table education_higher select taz, education_higher, 14 as sector_code
 from prelim_taz_weights;

update education_higher as a 
inner join control_totals_by_sector as b 
on a.sector_code = b.sector_code
set a.education_higher = a.education_higher/b.job_sum 
where b.sector_code = 14;

# Mining Sector Code 15

create temporary table mining select taz, mining, 15 as sector_code
 from prelim_taz_weights;

update mining as a 
inner join control_totals_by_sector as b 
on a.sector_code = b.sector_code
set a.mining = a.mining/b.job_sum 
where b.sector_code = 15;

# Update individual taz sector weights to one table (taz_weights)

update taz_weights as a inner join agriculture as b
 on a.taz = b.taz
 set a.agriculture = b.agriculture;

update taz_weights as a inner join construction as b
 on a.taz = b.taz
 set a.construction = b.construction;

update taz_weights as a inner join education_higher as b
 on a.taz = b.taz 
 set a.education_higher = b.education_higher;
 
update taz_weights as a inner join federal_civilian as b
 on a.taz = b.taz
 set a.federal_civilian = b.federal_civilian;
 
update taz_weights as a inner join federal_military as b
 on a.taz = b.taz
 set a.federal_military = b.federal_military;
 
update taz_weights as a inner join fires as b
 on a.taz = b.taz 
 set a.fires = b.fires;
 
update taz_weights as a inner join manufacturing as b
 on a.taz = b.taz 
 set a.manufacturing = b.manufacturing;
 
update taz_weights as a inner join mining as b
 on a.taz = b.taz
 set a.mining = b.mining;

update taz_weights as a inner join public_administration as b
 on a.taz = b.taz
 set a.public_administration = b.public_administration;
 
update taz_weights as a inner join retail_trade as b
 on a.taz = b.taz
 set a.retail_trade = b.retail_trade;
 
update taz_weights as a inner join state_and_local as b
 on a.taz = b.taz 
 set a.state_and_local = b.state_and_local;

update taz_weights as a inner join transportation_comm_elect_gas_san as b
 on a.taz = b.taz
 set a.transportation_comm_elect_gas_san = b.transportation_comm_elect_gas_san;
 
update taz_weights as a inner join wholesale_trade as b
 on a.taz = b.taz
 set a.wholesale_trade = b.wholesale_trade;
 
update taz_weights as a inner join services as b
 on a.taz = b.taz 
 set a.services = b.services;

update taz_weights as a inner join education_k_12 as b
 on a.taz = b.taz 
 set a.education_k_12 = b.education_k_12;

drop table agriculture;
drop table construction;
drop table education_higher;
drop table federal_civilian;
drop table federal_military;
drop table fires;
drop table manufacturing;
drop table mining;
drop table public_administration;
drop table retail_trade;
drop table state_and_local;
drop table transportation_comm_elect_gas_san;
drop table wholesale_trade;
drop table services;
drop table education_k_12;

# Create new ZONE_WEIGHTS table
# Input tables: taz_weights
# Output tables: ZONE_WEIGHTS

create table ZONE_WEIGHTS select COUNTY, TAZ, 1 as SECTOR, AGRICULTURE as WEIGHT from taz_weights;

insert into ZONE_WEIGHTS (county, taz, sector, weight) select county, taz, 2, CONSTRUCTION from taz_weights;
insert into ZONE_WEIGHTS (county, taz, sector, weight) select county, taz, 3, EDUCATION_K_12 from taz_weights;
insert into ZONE_WEIGHTS (county, taz, sector, weight) select county, taz, 4, FEDERAL_CIVILIAN from taz_weights;
insert into ZONE_WEIGHTS (county, taz, sector, weight) select county, taz, 5, FEDERAL_MILITARY from taz_weights;
insert into ZONE_WEIGHTS (county, taz, sector, weight) select county, taz, 6, FIRES from taz_weights;
insert into ZONE_WEIGHTS (county, taz, sector, weight) select county, taz, 7, MANUFACTURING from taz_weights;
insert into ZONE_WEIGHTS (county, taz, sector, weight) select county, taz, 8, PUBLIC_ADMINISTRATION from taz_weights;
insert into ZONE_WEIGHTS (county, taz, sector, weight) select county, taz, 9, RETAIL_TRADE from taz_weights;
insert into ZONE_WEIGHTS (county, taz, sector, weight) select county, taz, 10, SERVICES from taz_weights;
insert into ZONE_WEIGHTS (county, taz, sector, weight) select county, taz, 11, STATE_AND_LOCAL from taz_weights;
insert into ZONE_WEIGHTS (county, taz, sector, weight) select county, taz, 12, TRANSPORTATION_COMM_ELECT_GAS_SAN from taz_weights;
insert into ZONE_WEIGHTS (county, taz, sector, weight) select county, taz, 13, WHOLESALE_TRADE from taz_weights;
insert into ZONE_WEIGHTS (county, taz, sector, weight) select county, taz, 14, EDUCATION_HIGHER from taz_weights;
insert into ZONE_WEIGHTS (county, taz, sector, weight) select county, taz, 15, MINING from taz_weights;

alter table ZONE_WEIGHTS change column TAZ ZONE double;
alter table ZONE_WEIGHTS change column WEIGHT ZONE_WEIGHT_HOMEBASED double;
alter table ZONE_WEIGHTS add column ZONE_WEIGHT_NONHOMEBASED double;

update ZONE_WEIGHTS set ZONE_WEIGHT_NONHOMEBASED = ZONE_WEIGHT_HOMEBASED;



