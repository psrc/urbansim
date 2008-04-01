create index households_constants_household_id_index on households_constants (HOUSEHOLD_ID);

create temporary table 
  tmp_jobs_by_year 
  (year int, jobs int);

#  Aggregate total jobs by year
insert into 
  tmp_jobs_by_year
select 
  YEAR, 
  count(*) as jobs
from 
  jobs_exported
group by 
  YEAR;

create index 
  tmp_jobs_by_year_year_index 
on 
  tmp_jobs_by_year 
  (YEAR);

create temporary table 
  tmp_households_by_year 
  (year int, households int, population int);

# Aggregate total households by year, bringing in sums of persons-per-household as well
insert into 
  tmp_households_by_year
select 
  a.YEAR as year, 
  count(a.household_id) as households, 
  sum(b.persons) as population
from 
  households_exported as a 
  inner join 
    households_constants as b 
    on a.household_id=b.household_id
group by 
  a.YEAR;

create index 
  tmp_households_by_year_year_index 
on 
  tmp_households_by_year 
  (YEAR);

create table 
  demographics_with_history 
  (year int, jobs int, households int, population int, predicted bit);

# Combine jobs, households, and population, by year
insert into 
  demographics_with_history
select 
  a.year as year, 
  a.jobs as jobs, 
  b.households as households, 
  b.population as population, 
  1 as predicted
from 
  tmp_jobs_by_year as a 
  inner join 
    tmp_households_by_year as b 
    on a.year=b.year;

drop table 
  tmp_jobs_by_year;
drop table 
  tmp_households_by_year;

# Add in historical data
insert into 
  demographics_with_history
select 
  year, 
    employment as jobs, 
    households, 
    population, 
    0 as predicted
from 
  WFRC_1997_baseyear.historical_annual_totals;

create index 
  demographics_with_history_year 
on 
  demographics_with_history 
  (YEAR);
