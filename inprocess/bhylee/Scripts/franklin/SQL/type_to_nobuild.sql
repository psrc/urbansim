create temporary table tmp_table1(YEAR int, GRID_ID int, TOTAL_SQFT int, RESIDENTIAL_UNITS int, DEVELOPMENT_TYPE_ID int);
create temporary table tmp_table2(YEAR int, GRID_ID int, TOTAL_SQFT int, RESIDENTIAL_UNITS int, DEVELOPMENT_TYPE_ID int);
create temporary table tmp_table3(YEAR int, DEVELOPMENT_TYPE_ID int, EVENTS_CELLS int);
create temporary table tmp_table4(YEAR int, DEVELOPMENT_TYPE_ID int, TOTAL_CELLS int);

insert into tmp_table1(YEAR, GRID_ID, TOTAL_SQFT, RESIDENTIAL_UNITS, DEVELOPMENT_TYPE_ID)
select YEAR, GRID_ID, (INDUSTRIAL_SQFT+COMMERCIAL_SQFT+GOVERNMENTAL_SQFT) as TOTAL_SQFT, 
  RESIDENTIAL_UNITS, DEVELOPMENT_TYPE_ID
from gridcells_exported;

insert into tmp_table2(YEAR, GRID_ID, TOTAL_SQFT, RESIDENTIAL_UNITS, DEVELOPMENT_TYPE_ID)
select * from tmp_table1;

create index tmp_table1_year_grid_id_index on tmp_table1 (YEAR, GRID_ID);
create index tmp_table2_year_grid_id_index on tmp_table2 (YEAR, GRID_ID);

insert into tmp_table3(YEAR, DEVELOPMENT_TYPE_ID, EVENTS_CELLS)
select a.YEAR as YEAR, a.DEVELOPMENT_TYPE_ID as DEVELOPMENT_TYPE_ID, count(*) as EVENTS_CELLS
from tmp_table1 a inner join tmp_table2 b 
  on a.YEAR+1=b.YEAR and a.GRID_ID=b.GRID_ID
where a.TOTAL_SQFT<>b.TOTAL_SQFT or a.RESIDENTIAL_UNITS<>b.RESIDENTIAL_UNITS 
  or a.DEVELOPMENT_TYPE_ID<>b.DEVELOPMENT_TYPE_ID
group by a.YEAR, a.DEVELOPMENT_TYPE_ID
order by a.YEAR, a.DEVELOPMENT_TYPE_ID;

insert into tmp_table4(YEAR, DEVELOPMENT_TYPE_ID, TOTAL_CELLS)
select YEAR, DEVELOPMENT_TYPE_ID, count(*) as TOTAL_CELLS 
from gridcells_exported
group by YEAR, DEVELOPMENT_TYPE_ID;

create table type_to_nobuild select a.YEAR as YEAR, a.DEVELOPMENT_TYPE_ID as INDICATORS_SUBTYPE, (a.TOTAL_CELLS-IFNULL(b.EVENTS_CELLS,0)) as INDICATORS_VALUE
from tmp_table4 a left outer join tmp_table3 b 
  on a.YEAR=b.YEAR and a.DEVELOPMENT_TYPE_ID=b.DEVELOPMENT_TYPE_ID
order by a.YEAR, a.DEVELOPMENT_TYPE_ID;

drop table tmp_table1;
drop table tmp_table2;
drop table tmp_table3;
drop table tmp_table4;
 
