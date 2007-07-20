-- Import exlu.dbf into MySQL database
-- Prerequisites:
-- 1. opened exlu.dbf in MS Excel and saved as tab delimited
-- 2. opened exlu.txt in a text editor and deleted the top line
-- that contained field names

-- Create exlu table
-- These fields were copied from exlu.dbf
-- If your exlu.dbf differs from this one, this will need to be modified
create table exlu
(
 area double,
 perimeter double,
 lupolyid int,
 lucode int,
 mpa varchar(10),
 lucodempa varchar(10),
 lastupdate varchar (15)
);

-- Load data from tab delimited file into exlu table
-- The fields below will need to be modified if your table does not match
-- this exactly
load data local infile 'd:/testing/exlu.txt'
into table exlu
fields terminated by '\t' -- change \t to ',' for comma delimited
lines terminated by '\r\n'
(
 area,
 perimeter,
 lupolyid,
 lucode,
 mpa,
 lucodempa,
 lastupdate
);

-- Repeats the above procedure with exluc table
create table exluc
(
 taz int,
 adjor double,
 pphh double,
 lupolyid int,
 lucode2 int,
 sector varchar(10),
 pct int,
 units varchar(10),
 tgtmag double,
 minmag double,
 maxmag double,
 tgtmpa double,
 orig_dens double,
 dudens double,
 hhdens double,
 actpopdens double,
 bopopdens double
);

load data local infile 'd:/testing/exluc.txt'
into table exluc
fields terminated by '\t' -- change \t to ',' for comma delimited
lines terminated by '\r\n'
(
 taz,
 adjor,
 pphh,
 lupolyid,
 lucode2,
 sector,
 pct,
 units,
 tgtmag,
 minmag,
 maxmag,
 tgtmpa,
 orig_dens,
 dudens,
 hhdens,
 actpopdens,
 bopopdens
);

-- Create indexes in preparation for join
create index lupolyid_index1 on exlu(lupolyid);
create index lupolyid_index2 on exluc(lupolyid);

-- Join exlu and exluc together
create table test
select e.area, e.lupolyid as exlu_lupolyid, e.lucode, c.lupolyid as exluc_lupolyid, c.sector, c.pct, c.tgtmag, c.hhdens
from exlu e
left join exluc c
on e.lupolyid = c.lupolyid;

-- calculate variables
-- add num_employees column
alter table test
add column num_employees int;

-- calculate num_employees
update test
set num_employees = round((((.01*pct)*area)*tgtmag));

-- update num_employees where the sector is residential
update test
set num_employees = 0
where num_employees is null or sector = 'RSF' or sector = 'RMF';

-- add num_du column
alter table test
add column num_du int;

-- calculate num_du where the sector is residential
update test
set num_du = round((((.01*pct)*area)*tgtmag))
where sector = 'RSF' or sector = 'RMF';

-- update num_du where sector is not residential
update test
set num_du = 0
where num_du is null;

-- add num_hh column
alter table test
add column num_hh int;

-- calculate num_hh column where the sector is residential
update test
set num_hh = round((((.01*pct)*area)*hhdens))
where sector = 'RSF' or sector = 'RMF';

-- update num_hh where sector is not residential
update test
set num_hh = 0
where num_hh is null;

/*
-- Totals
-- total number of employees
select sum(num_employees) from test;
-- total number of dwelling units
select sum(num_du) from test;
-- total number of households
select sum(num_hh) from test;

-- Totals by sector
-- number of employees by sector
select sector, sum(num_employees) from test where num_employees > 0 group by sector;
-- number of dwelling units by sector
select sector, sum(num_du) from test where num_du > 0 group by sector;
-- number of households by sector
select sector, sum(num_hh) from test where num_hh > 0 group by sector;
*/
