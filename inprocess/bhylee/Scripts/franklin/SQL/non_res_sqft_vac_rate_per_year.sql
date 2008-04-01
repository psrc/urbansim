create temporary table tmp_table1(YEAR int, GRID_ID int, JOBS int);
create temporary table tmp_table2(YEAR int, GRID_ID int, TOTAL_SQFT int, DEVELOPMENT_TYPE_ID int, SQFT int);

insert into tmp_table1(YEAR, GRID_ID, JOBS)
select YEAR,GRID_ID,count(JOB_ID) as JOBS
from jobs_exported
where HOME_BASED=0   
group by GRID_ID,YEAR;

insert into tmp_table2(YEAR, GRID_ID, TOTAL_SQFT, DEVELOPMENT_TYPE_ID, SQFT)
select a.YEAR, a.GRID_ID, (a.COMMERCIAL_SQFT+a.INDUSTRIAL_SQFT+a.GOVERNMENTAL_SQFT) as TOTAL_SQFT,
  a.DEVELOPMENT_TYPE_ID, b.SQFT
from gridcells_exported as a, wfrc_1997_baseyear.sqft_for_non_home_based_jobs as b 
where a.DEVELOPMENT_TYPE_ID=b.DEVELOPMENT_TYPE_ID;

create index tmp_table1_year_grid_id_index on tmp_table1 (YEAR,GRID_ID);
create index tmp_table2_year_grid_id_dev_type_index on tmp_table2 (YEAR,GRID_ID,DEVELOPMENT_TYPE_ID);

create table nonres_vac_rate_per_year
select a.YEAR as YEAR,
  round(100*(1-sum(b.JOBS*a.SQFT)/sum(a.TOTAL_SQFT)),2) as nonresidential_vacancy_rate 
from tmp_table2 as a left outer join tmp_table1 as b 
  on a.YEAR=b.YEAR and a.GRID_ID=b.GRID_ID 
group by a.YEAR
order by a.YEAR;

drop table tmp_table1;
drop table tmp_table2;
