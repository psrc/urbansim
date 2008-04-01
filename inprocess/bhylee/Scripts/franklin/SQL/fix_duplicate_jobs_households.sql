
# Calculate average grid_id as a check that the deleted rows are duplicates

select year, avg(grid_id)
     from households_exported
     group by year;

# Aggregate entries by year and household_id

create temporary table tmp_households_exported
     select year,
          household_id,
          max(grid_id) as grid_id,
          max(zone_id) as zone_id
     from households_exported
     group by year, household_id;
create index tmp_households_exported_year_household_id
     on tmp_households_exported (year, household_id);

# Compare average grid_id to original table

select year, avg(grid_id)
     from tmp_households_exported
     group by year;

# Put the remaining entries into the emptied original table

delete from households_exported;
insert into households_exported
     select * from tmp_households_exported;

# Calculate average grid_id as a check that the deleted rows are duplicates

select year, avg(grid_id)
     from jobs_exported
     group by year;

# Aggregate entries by year and job_id

create temporary table tmp_jobs_exported
     select year,
          job_id,
          max(grid_id) as grid_id,
          max(home_based) as home_based,
          max(zone_id) as zone_id
     from jobs_exported
     group by year, job_id;
create index tmp_jobs_exported_year_job_id
     on tmp_jobs_exported (year, job_id);

# Compare average grid_id to original table

select year, avg(grid_id)
     from tmp_jobs_exported
     group by year;

# Put the remaining entries into the emptied original table

delete from jobs_exported;
insert into jobs_exported
     select * from tmp_jobs_exported;

