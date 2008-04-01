create temporary table tmp_table1(YEAR int, GRID_ID int, TOTAL_SQFT int, RESIDENTIAL_UNITS int, DEVELOPMENT_TYPE_ID int);
create temporary table tmp_table2(YEAR int, GRID_ID int, TOTAL_SQFT int, RESIDENTIAL_UNITS int, DEVELOPMENT_TYPE_ID int);

insert into tmp_table1(YEAR, GRID_ID, TOTAL_SQFT, RESIDENTIAL_UNITS, DEVELOPMENT_TYPE_ID)
select YEAR, GRID_ID, (INDUSTRIAL_SQFT+COMMERCIAL_SQFT+GOVERNMENTAL_SQFT) as TOTAL_SQFT, 
  RESIDENTIAL_UNITS, DEVELOPMENT_TYPE_ID
from gridcells_exported;

insert into tmp_table2(YEAR, GRID_ID, TOTAL_SQFT, RESIDENTIAL_UNITS, DEVELOPMENT_TYPE_ID)
select * from tmp_table1;

create index tmp_table1_year_grid_id_index on tmp_table1 (YEAR, GRID_ID);
create index tmp_table2_year_grid_id_index on tmp_table2 (YEAR, GRID_ID);

create table type_to_build select a.YEAR as YEAR, a.DEVELOPMENT_TYPE_ID as INDICATORS_SUBTYPE, count(*) as INDICATORS_VALUE
from tmp_table1 a inner join tmp_table2 b 
  on a.YEAR+1=b.YEAR and a.GRID_ID=b.GRID_ID
where a.TOTAL_SQFT<>b.TOTAL_SQFT or a.RESIDENTIAL_UNITS<>b.RESIDENTIAL_UNITS 
  or a.DEVELOPMENT_TYPE_ID<>b.DEVELOPMENT_TYPE_ID
group by a.YEAR, a.DEVELOPMENT_TYPE_ID
order by a.YEAR, a.DEVELOPMENT_TYPE_ID;

drop table tmp_table1;
drop table tmp_table2;
