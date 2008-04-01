use PSRC_residential_location_choice_lmwang;

create table variables 
select HH_ID, restype, hhsize, income from household;

alter table variables 
    add has_chld int,
    add chld_sch int,
    add workers int,
    add age int,
    add ethn int,
    add primact int,
    add educate int,
    add occup int,
    add age_range varchar(8)
;

update variables as h set h.has_chld = 0,
	h.chld_sch = 0
;

update variables h, person p
set h.has_chld = 1 
where h.hh_id = p.hh_id and
	p.relation = 3 and
	p.age <= 18
;

update variables h, person p, school s
set h.chld_sch = 1
where h.hh_id = p.hh_id and 
	p.hh_id = s.hh_id and
	p.per_id = s.per_id and
	p.relation = 3 and 
	p.age <= 18
;

/*---- begin diagnostic code
SELECT p.*, s.*
FROM person p
right outer join school s 
on p.hh_id = s.hh_id and
p.per_id = s.per_id
where p.per_id is null
;
# there are 93 rows in school table that have no match in person table

SELECT w.*
FROM person p
right outer join work w 
on p.hh_id = w.hh_id and
p.per_id = w.per_id
where p.per_id is null
;
# there are 105 rows in work table that have no match in person table

*/---- end diagnostic code

create temporary table tmp_num_workers
select hh_id, count(*) as workers
from work
group by hh_id
;

update variables h, tmp_num_workers w
set h.workers = w.workers
where h.hh_id = w.hh_id
;

update variables h, person p
set h.age = p.age,
    h.ethn = p.ethn,
    h.primact = p.primact,
    h.educate = p.educate
where h.hh_id = p.hh_id and
      p.per_id = 1
;

update variables h, person p, work w
set h.occup = w.occup
where h.hh_id = p.hh_id and
      p.hh_id = w.hh_id and
      p.per_id = w.per_id and
      p.per_id = 1
;

#set missing value
update variables
  set restype = null where restype = 9;
update variables
  set addlive = null where addlive = 6;
update variables
  set cntylive = null where cntylive = 6;
update variables
  set totveh = null where totveh = 98 or totveh = 99;
update variables
  set income = null where income = 99;
update variables
  set bikes = null where bikes = 98;
update variables
  set age = null where age = 99;
update variables
  set ethn = null where ethn = 9;
update variables
  set educate = null where educate = 9;
update variables
  set primact = null where primact = 99;

delete from variables where restype is null;

--reclassify and create table variable_collapse, refer to var.codebook.txt
create table variables_collapse
select restype, hhsize, income, has_chld, ethn, primact, educate,age, age_range, hh_ct
from variables;

#update variables_collapse set restype = 1
#	where restype = 1;
update variables_collapse set restype = 2 
	where restype = 2 or restype = 3;
#update variables_collapse set restype = 4
#	where restype = 4;
update variables_collapse set restype = 8 
	where restype = 5 or restype = 6 or restype = 8;

update variables_collapse set income = 1 
	where income = 11 or income = 12
	or income = 13 or income = 14
#	or income = 1
;
update variables_collapse set income = 2 
	where income = 15 or income = 16
	or income = 17 or income = 18
#	or income = 2
;

#update variables_collapse set ethn = 1 
#	where ethn = 1;
update variables_collapse set ethn = 6 
	where ethn = 2 or ethn = 3
	or ethn = 4 or ethn = 5
#	or ethn = 6
;

update variables_collapse set primact = 1 
	where primact = 2
#	or primact = 1
;
update variables_collapse set primact = 3
	where primact = 4 or primact = 5
	or primact = 6 or primact = 13
#	or primact = 3
;
update variables_collapse set primact = 7 
	where primact = 8
#	or primact = 7
;
update variables_collapse set primact = 11
	where primact = 9 or primact = 10
	or primact = 12 or primact = 14
#	or primact = 11
;

update variables_collapse set educate = 1
	where educate = 2
#	or educate = 1
;
update variables_collapse set educate = 5
	where educate = 3 or educate = 4
#	or educate = 5
;
#update variables_collapse set educate = 6
#	where educate = 6;

update variables_collapse set age_range = '<=30' 
	where age <= 30;
update variables_collapse set age_range = '31-40' 
	where age between 31 and 40;
update variables_collapse set age_range = '41-50' 
	where age between 41 and 50;
update variables_collapse set age_range = '51-65' 
	where age between 51 and 65;
update variables_collapse set age_range = '>65' 
	where age > 65;

update variables_collapse set hh_ct = FLOOR(hh_ct);

alter table variables_collapse
add ct_ht varchar(16);

update variables_collapse set ct_ht = concat(restype,'@',hh_ct);

#prepare count data for export
create table htbyvars
select 
count(*) as count, 
restype,
hhsize,
income,
has_chld,
ethn,
primact,
educate,
age_range
from variables_collapse
group by 
restype, 
hhsize, 
income,
has_chld,
ethn,
primact,
educate,
age_range
;

#prepare count data for export (including census tract)
create table ctht_byvars
select 
count(*) as count, 
ct_ht,
hhsize,
income,
has_chld,
ethn,
primact,
educate,
age_range
from variables_collapse
group by 
ct_ht, 
hhsize,
income,
has_chld,
ethn,
primact,
educate,
age_range
;


create table htbyvars_simple
select 
count(*) as count, 
restype,
hhsize,
income,
age_range
from variables_collapse
group by 
restype, 
hhsize, 
income,
age_range
;

create table ctht_byvars_simple
select 
count(*) as count, 
ct_ht,
hhsize,
income,
age_range
from variables_collapse
group by 
ct_ht, 
hhsize, 
income,
age_range
;

/*
delete from htbyvars where 
restype is null or 
hhsize is null or 
income is null or 
has_chld is null or 
ethn is null or 
primact is null or 
educate is null;

delete from ctht_byvars where 
restype is null or 
hhsize is null or 
income is null or 
has_chld is null or 
ethn is null or 
primact is null or 
educate is null or
ct_ht is null;
*/

create table htbyvars_ct
select
hhsize, 
income,
has_chld,
ethn,
primact,
educate,
age_range,
sum(IF(restype=1, count, 0)) as "restype_1",
sum(IF(restype=2, count, 0)) as "restype_2",
#sum(IF(restype=3, count, 0)) as "restype_3",
sum(IF(restype=4, count, 0)) as "restype_4",
#sum(IF(restype=5, count, 0)) as "restype_5",
#sum(IF(restype=6, count, 0)) as "restype_6",
sum(IF(restype=8, count, 0)) as "restype_8"
from htbyvars
group by
hhsize, 
income,
has_chld,
ethn,
primact,
educate,
age_range
;

create table ctht_byvars_ct
select
hhsize, 
income,
has_chld,
ethn,
primact,
educate,
age_range,
sum(IF(restype=1, count, 0)) as "restype_1",
sum(IF(restype=2, count, 0)) as "restype_2",
#sum(IF(restype=3, count, 0)) as "restype_3",
sum(IF(restype=4, count, 0)) as "restype_4",
#sum(IF(restype=5, count, 0)) as "restype_5",
#sum(IF(restype=6, count, 0)) as "restype_6",
sum(IF(restype=8, count, 0)) as "restype_8"
from htbyvars
group by
hhsize, 
income,
has_chld,
ethn,
primact,
educate,
age_range


create table htbyvars_ct_simple
select
hhsize, 
income,
age_range,
sum(IF(restype=1, count, 0)) as "restype_1",
sum(IF(restype=2, count, 0)) as "restype_2",
#sum(IF(restype=3, count, 0)) as "restype_3",
sum(IF(restype=4, count, 0)) as "restype_4",
#sum(IF(restype=5, count, 0)) as "restype_5",
#sum(IF(restype=6, count, 0)) as "restype_6",
sum(IF(restype=8, count, 0)) as "restype_8"
from htbyvars_simple
group by
hhsize, 
income,
age_range
;


#create 2x2 Contingency table
select 
hhsize,
sum(restype_1) as restype_1, 
sum(restype_2) as restype_2, 
#sum(restype_3) as restype_3, 
sum(restype_4) as restype_4, 
#sum(restype_5) as restype_5, 
#sum(restype_6) as restype_6, 
sum(restype_8) as restype_8 
from htbyvars_ct
group by hhsize;

select 
income,
sum(restype_1) as restype_1, 
sum(restype_2) as restype_2, 
#sum(restype_3) as restype_3, 
sum(restype_4) as restype_4, 
#sum(restype_5) as restype_5, 
#sum(restype_6) as restype_6, 
sum(restype_8) as restype_8 
from htbyvars_ct
group by income;

select 
has_chld,
sum(restype_1) as restype_1, 
sum(restype_2) as restype_2, 
#sum(restype_3) as restype_3, 
sum(restype_4) as restype_4, 
#sum(restype_5) as restype_5, 
#sum(restype_6) as restype_6, 
sum(restype_8) as restype_8 
from htbyvars_ct
group by has_chld;

select 
ethn,
sum(restype_1) as restype_1, 
sum(restype_2) as restype_2, 
#sum(restype_3) as restype_3, 
sum(restype_4) as restype_4, 
#sum(restype_5) as restype_5, 
#sum(restype_6) as restype_6, 
sum(restype_8) as restype_8 
from htbyvars_ct
group by ethn;

select 
primact,
sum(restype_1) as restype_1, 
sum(restype_2) as restype_2, 
#sum(restype_3) as restype_3, 
sum(restype_4) as restype_4, 
#sum(restype_5) as restype_5, 
#sum(restype_6) as restype_6, 
sum(restype_8) as restype_8 
from htbyvars_ct
group by primact;

select 
educate,
sum(restype_1) as restype_1, 
sum(restype_2) as restype_2, 
#sum(restype_3) as restype_3, 
sum(restype_4) as restype_4, 
#sum(restype_5) as restype_5, 
#sum(restype_6) as restype_6, 
sum(restype_8) as restype_8 
from htbyvars_ct
group by educate;

select 
age_range,
sum(restype_1) as restype_1, 
sum(restype_2) as restype_2, 
#sum(restype_3) as restype_3, 
sum(restype_4) as restype_4, 
#sum(restype_5) as restype_5, 
#sum(restype_6) as restype_6, 
sum(restype_8) as restype_8 
from htbyvars_ct
group by age_range;


/*
select 
occup,
sum(restype_1) as restype_1, 
sum(restype_2) as restype_2, 
sum(restype_3) as restype_3, 
sum(restype_4) as restype_4, 
sum(restype_5) as restype_5, 
sum(restype_6) as restype_6, 
sum(restype_8) as restype_8 
from htbyvars_ct
group by occup;
*/


