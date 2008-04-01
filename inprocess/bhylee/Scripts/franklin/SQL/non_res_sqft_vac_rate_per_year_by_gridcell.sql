create temporary table tmp_table1(YEAR int, GRID_ID int, JOBS int);
create temporary table tmp_table2(YEAR int, GRID_ID int, TOTAL_SQFT int, DEVELOPMENT_TYPE_ID int, SQFT int);

insert into tmp_table1(YEAR, GRID_ID, JOBS)
select YEAR,GRID_ID,count(JOB_ID) as JOBS
from jobs_exported
where HOME_BASED=0 and YEAR=2001
group by GRID_ID,YEAR;

insert into tmp_table2(YEAR, GRID_ID, TOTAL_SQFT, DEVELOPMENT_TYPE_ID, SQFT)
select a.YEAR, a.GRID_ID, (a.COMMERCIAL_SQFT+a.INDUSTRIAL_SQFT+a.GOVERNMENTAL_SQFT) as TOTAL_SQFT,
  a.DEVELOPMENT_TYPE_ID, b.SQFT
from gridcells_exported as a, WFRC_1997_baseyear.sqft_for_non_home_based_jobs as b 
where a.DEVELOPMENT_TYPE_ID=b.DEVELOPMENT_TYPE_ID and YEAR=2001;

create index tmp_table1_year_grid_id_index on tmp_table1 (YEAR,GRID_ID);
create index tmp_table2_year_grid_id_dev_type_index on tmp_table2 (YEAR,GRID_ID,DEVELOPMENT_TYPE_ID);

drop table non_res_sqft_vac_rate_by_gridcell;
create table non_res_sqft_vac_rate_by_gridcell
select a.YEAR as YEAR, a.GRID_ID as GRID_ID,
  round(100*(1-sum(b.JOBS*a.SQFT)/sum(a.TOTAL_SQFT)),2) as VACANCY_RATE 
from tmp_table2 as a left outer join tmp_table1 as b 
  on a.YEAR=b.YEAR and a.GRID_ID=b.GRID_ID 
group by a.YEAR, a.GRID_ID
order by a.YEAR, a.GRID_ID;

create index nrsfvrgc_year_gridid on non_res_sqft_vac_rate_by_gridcell (YEAR,GRID_ID);

drop table tmp_table1;
drop table tmp_table2;
