alter table king_apt add column parcel_id varchar(255);
update king_apt set parcel_id = concat("033",Major,Minor);

alter table king_apt add column BuildingNumber varchar(255);
update king_apt set BuildingNumber = left(Address,locate(" ",Address)-1);

alter table king_condo add column parcel_id varchar(255);
update king_condo set parcel_id = concat("033",Major,"0000");

alter table king_res add column parcel_id varchar(255);
update king_res set parcel_id = concat("033",Major,Minor);

alter table pierce add column parcel_id varchar(255);
update pierce set parcel_id = concat("053",AccountNo);

alter table snohomish add column parcel_id varchar(255);
update snohomish set parcel_id = concat("061",PARCEL_NUM);

alter table snohomish add column BuildingNumber varchar(255);
update snohomish set BuildingNumber = left(SITUSLINE1,locate(" ",SITUSLINE1)-1);

create table all_county_parcel_id_buildingnumber
(ID integer unsigned not null default null auto_increment, primary key (ID))
select ka.parcel_id, ka.BuildingNumber from king_apt as ka
union all
select kc.parcel_id, kc.BuildingNumber from king_condo as kc
union all
select kr.parcel_id, kr.BuildingNumber from king_res as kr
union all
select p.parcel_id, p.LocationStreetNo from pierce as p
union all
select s.parcel_id, s.BuildingNumber from snohomish as s
ENGINE = MyISAM;
#1048226 parcel records

select parcel_id, count(*) from psrc_address.all_county_parcel_id_buildingnumber 
group by parcel_id order by count(*) desc;
#1043485 unique parcel_id; 4241 parcel_id with multiple records

alter table hh_matched_parcels add column HOMENUM varchar(255);
update hh_matched_parcels set HOMENUM = left(HOMEADDR,locate(" ",HOMEADDR)-1);

create index id using btree on psrc_activity2006.hh_matched_parcels (parcelid);
create index id using btree on psrc_address.all_county_parcel_id_buildingnumber (parcel_id);

create table hh_matched_parcels_buildingnumber ENGINE = MyISAM
select h.*, a.parcel_id, a.BuildingNumber from hh_matched_parcels as h
left join psrc_address.all_county_parcel_id_buildingnumber as a on h.parcelid = a.parcel_id
where (h.PMATCH=1 and h.parcelid is not null);
#4250 records

select parcelid, count(*) from hh_matched_parcels_buildingnumber 
group by parcelid order by count(*) desc;
#4164 unique parcelid; 72 parcelid with multiple records

select * from hh_matched_parcels_buildingnumber h where parcelid like "035%";
#556 records from Kitsap County where there are no parcel address records

######################################################################################

select * from parcels_matched_hh;
#4171 parcels matched to HH
#note some parcels overlap (i.e., multiple parcels may be matched to a HH)

create table hh01_parcelid ENGINE = MyISAM
select * from hh_matched_parcels where PMATCH=1 and parcelid is not null;
#4231 HH matched to a parcel with parcelid

create table hh02_parcelid_unique ENGINE = MyISAM
select parcelid, count(*) as number from hh01_parcelid
group by parcelid order by number desc;
#4164 unique parcelids matched to HH

create table hh03_parcelid_duplicates ENGINE = MyISAM
select parcelid, number from hh02_parcelid_unique
where number > 1;
#53 parcels with more than 1 HH matched

create table hh04_parcelid_unique_buildingnumber ENGINE = MyISAM
select h.parcelid, a.parcel_id, a.BuildingNumber from hh02_parcelid_unique as h
left join psrc_address.all_county_parcel_id_buildingnumber as a on h.parcelid = a.parcel_id;
#4183 records; 4164 unique parcelid

######################################################################################

create table hh05_parcel_id_not_null ENGINE = MyISAM
select * from hh_matched_parcels_buildingnumber where parcel_id is not null;
#3568 records where parcel is not null

select QNO, count(*) from hh05_parcel_id_not_null group by QNO order by count(*) desc;
#3549 unique HH records; 19 out of 3549 with two records

create table hh06_parcel_id_matched_addrnum ENGINE = MyISAM
select * from hh05_parcel_id_not_null where HOMENUM = BuildingNumber;
#2948 records where the address number match

create table qno1 ENGINE = MyISAM
select QNO, count(*) from hh06_parcel_id_matched_addrnum group by QNO order by count(*) desc;
#2939 unique HH records with address number match; 9 out of 2939 with two records

create table hh07_parcel_id_not_matched_addrnum ENGINE = MyISAM
select * from hh05_parcel_id_not_null where HOMENUM <> BuildingNumber;
#605 records where the address number not match

select QNO, count(*) from hh07_parcel_id_not_matched_addrnum group by QNO order by count(*) desc;
#599 unique HH records with address number not match; 6 out of 599 with two records

create index id using btree on hh01_parcelid (QNO);
create index id using btree on qno1 (QNO);

create table hh08_hh01_not_in_qno1 ENGINE = MyISAM
select h.* from hh01_parcelid as h
left join qno1 as q on h.QNO = q.QNO where q.QNO is null;
#1292 HH matched to a parcel with parcelid but address number not match

create index id using btree on hh08_hh01_not_in_qno1 (parcelid);
create index id using btree on psrc_2005_data_revised_2.parcel (id_parcel);

create table hh09_hh08_matched_workspace_parcels ENGINE = MyISAM
select h.*, p.id_parcel, p.res_nonres from hh08_hh01_not_in_qno1 as h
left join psrc_2005_data_revised_2.parcel as p on h.parcelid = p.id_parcel;
#1293 HH records; 1292 unique QNO's

create table qno2 ENGINE = MyISAM
select QNO, count(*) from hh09_hh08_matched_workspace_parcels where res_nonres = "RES" group by QNO;
#1061 unique HH records matched to residential parcels

create index id using btree on hh06_parcel_id_matched_addrnum (parcelid);

create table hh10_hh06_matched_workspace_parcels ENGINE = MyISAM
select h.*, p.id_parcel, p.res_nonres from hh06_parcel_id_matched_addrnum as h
left join psrc_2005_data_revised_2.parcel as p on h.parcelid = p.id_parcel;
#2948 HH records; 2939 unique QNO's

create table qno3 ENGINE = MyISAM
select QNO, count(*) from hh10_hh06_matched_workspace_parcels where res_nonres="RES" group by QNO;
#2849 unique HH records with address number matched to residential parcels

######################################################################################

create table qno_all
(ID integer unsigned not null default null auto_increment, primary key (ID)) ENGINE = MyISAM
select qno2.QNO from qno2
union all
select qno3.QNO from qno3;
#3910 unique HH records matched to residential parcels

######################################################################################

create table hh11_res ENGINE = MyISAM
select h.* from hh_matched_parcels as h
left join qno_all as q on h.QNO = q.QNO where q.QNO is not null;
#3910 unique HH records matched to residential parcels

create index id using btree on hh11_res (parcelid);

create table hh_res ENGINE = MyISAM
select h.*, p.id_parcel, p.parcel_id from hh11_res as h
left join psrc_2005_data_workspace.parcels as p on h.parcelid = p.id_parcel;
#3910 unique HH records matched to residential parcels with parcel_id