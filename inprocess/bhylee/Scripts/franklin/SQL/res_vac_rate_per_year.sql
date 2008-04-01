create temporary table tmp_table1(YEAR int, GRID_ID int, HOUSEHOLDS int);

insert into tmp_table1(YEAR, GRID_ID, HOUSEHOLDS)
select YEAR,GRID_ID,count(HOUSEHOLD_ID) as HOUSEHOLDS
from households_exported
group by GRID_ID,YEAR;

create index tmp_table1_year_grid_id_index on tmp_table1 (YEAR,GRID_ID);

create table res_vac_rate_per_year
select a.YEAR as YEAR,
  round(100*(1-SUM(HOUSEHOLDS)/sum(RESIDENTIAL_UNITS)),2) as residential_vacancy_rate
from gridcells_exported as a left outer join tmp_table1 as b 
  on a.YEAR=b.YEAR and a.GRID_ID=b.GRID_ID
group by a.YEAR
order by a.YEAR;

drop table tmp_table1;