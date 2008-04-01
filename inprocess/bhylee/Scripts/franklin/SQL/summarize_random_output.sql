# This script summarized distributed results from several similar runs, labeled "random1" through "random5".

use WFRC_1997_summary_random;

# Integrate the five runs' gridcell data and label using the "instance" field

drop table if exists gridcells_compiled;
create table gridcells_compiled
     select 1 as instance, gc_e.*
     from WFRC_1997_output_random1.gridcells_exported as gc_e;
create index gridcells_compiled_instance_year_grid_id
     on gridcells_compiled (instance, year, grid_id);

insert into gridcells_compiled
     select 2 as instance, gc_e.*
     from WFRC_1997_output_random2.gridcells_exported as gc_e;
     
insert into gridcells_compiled
     select 3 as instance, gc_e.*
     from WFRC_1997_output_random3.gridcells_exported as gc_e;
     
insert into gridcells_compiled
     select 4 as instance, gc_e.*
     from WFRC_1997_output_random4.gridcells_exported as gc_e;
     
insert into gridcells_compiled
     select 5 as instance, gc_e.*
     from WFRC_1997_output_random5.gridcells_exported as gc_e;

# Attach TAZ identifiers to the gridcells data

drop temporary table if exists tmp_gridcells_compiled;
create temporary table tmp_gridcells_compiled
     select gc_c.*, 
          gc_base.zone_id as zone_id
     from gridcells_compiled as gc_c,
          WFRC_1997_baseyear.gridcells as gc_base
     where gc_c.grid_id=gc_base.grid_id;

drop table if exists gridcells_compiled;
create table gridcells_compiled
     select tmp_gc_c.*,
          z.distsml as distsml,
          z.distmed as distmed,
          z.distlrg as distlrg,
          z.county as county
     from tmp_gridcells_compiled as tmp_gc_c,
          WFRC_1997_baseyear.zones as z
     where tmp_gc_c.zone_id=z.zone_id;

# Aggregate over all instances to get gridcell-specific summary statistics for each year

drop table if exists gridwise_stats;
create table gridwise_stats
     select year, grid_id,
          avg(commercial_sqft+industrial_sqft+governmental_sqft) as sfnr_avg,
          min(commercial_sqft+industrial_sqft+governmental_sqft)
               /avg(commercial_sqft+industrial_sqft+governmental_sqft) as sfnr_min_n,
          max(commercial_sqft+industrial_sqft+governmental_sqft)
               /avg(commercial_sqft+industrial_sqft+governmental_sqft) as sfnr_max_n,
          std(ln(commercial_sqft+industrial_sqft+governmental_sqft))
               /avg(ln(commercial_sqft+industrial_sqft+governmental_sqft)) as ln_sfnr_std_n,
          avg(residential_units) as dur_avg,
          min(residential_units)
               /avg(residential_units) as dur_min_n,
          max(residential_units)
               /avg(residential_units) as dur_max_n,
          std(ln(residential_units))
               /avg(ln(residential_units)) as ln_dur_std_n
     from gridcells_compiled
     group by year, grid_id;
create index gridwise_stats_year_grid_id
     on gridwise_stats(year, grid_id);

# Pull out 2003 values from gridwise_stats and create table to be used in map displays

drop table if exists gridwise_stats_2003;
create table gridwise_stats_2003
	select year, grid_id, sfnr_avg, sfnr_min_n, sfnr_max_n, ln_sfnr_std_n,
	dur_avg, dur_min_n, dur_max_n, ln_dur_std_n
from gridwise_stats
where year = 2003
group by year, grid_id;
create index gridwise_stats_2003_year_grid_id
     on gridwise_stats_2003(year, grid_id);

# Aggregate over all gridcells to summarize the summary stats for each year

drop table if exists summary_by_level;
create table summary_by_level
     select year, "gridcell" as level,
          avg(sfnr_avg) as sfnr_avg_avg,
          std(sfnr_avg) as sfnr_avg_std,
          avg(sfnr_min_n) as sfnr_min_n_avg,
          std(sfnr_min_n) as sfnr_min_n_std,
          avg(sfnr_max_n) as sfnr_max_n_avg,
          std(sfnr_max_n) as sfnr_max_n_std,
          avg(ln_sfnr_std_n) as ln_sfnr_std_n_avg,
          std(ln_sfnr_std_n) as ln_sfnr_std_n_std,
          avg(dur_avg) as dur_avg_avg,
          std(dur_avg) as dur_avg_std,
          avg(dur_min_n) as dur_min_n_avg,
          std(dur_min_n) as dur_min_n_std,
          avg(dur_max_n) as dur_max_n_avg,
          std(dur_max_n) as dur_max_n_std,
          avg(ln_dur_std_n) as ln_dur_std_n_avg,
          std(ln_dur_std_n) as ln_dur_std_n_std
     from gridwise_stats
     group by year;
create index summary_by_level
     on summary_by_level(year);
     
# Aggregate over zone_id to sum quantities in each TAZ

drop table if exists zones_compiled;
create table zones_compiled
     select year, zone_id, instance,
          sum(commercial_sqft+industrial_sqft+governmental_sqft) as nrsf,
          sum(residential_units) as dur
     from gridcells_compiled
     group by year, zone_id, instance;
create index zones_compiled_year_zone_id_instance
     on zones_compiled (year, zone_id, instance);

# Aggregate over all instances to get zone-specific summary statistics for each year

drop table if exists zonewise_stats;
create table zonewise_stats
     select year, zone_id,
          avg(nrsf) as sfnr_avg,
          min(nrsf)
               /avg(nrsf) as sfnr_min_n,
          max(nrsf)
               /avg(nrsf) as sfnr_max_n,
          std(ln(nrsf))
               /avg(ln(nrsf)) as ln_sfnr_std_n,
          avg(dur) as dur_avg,
          min(dur)
               /avg(dur) as dur_min_n,
          max(dur)
               /avg(dur) as dur_max_n,
          std(ln(dur))
               /avg(ln(dur)) as ln_dur_std_n
     from zones_compiled
     group by year, zone_id;
create index zonewise_stats_year_zone_id
     on zonewise_stats(year, zone_id);

# Pull out 2003 values from zonewise_stats and create table to be used in map displays

drop table if exists zonewise_stats_2003;
create table zonewise_stats_2003
	select year, zone_id, sfnr_avg, sfnr_min_n, sfnr_max_n, ln_sfnr_std_n,
	dur_avg, dur_min_n, dur_max_n, ln_dur_std_n
from zonewise_stats
where year = 2003
group by year, zone_id;
create index zonewise_stats_2003_year_zone_id
     on zonewise_stats_2003(year, zone_id);

# Aggregate over all zones to summarize the summary stats for each year

insert into summary_by_level
     select year, "zone" as level,
          avg(sfnr_avg) as sfnr_avg_avg,
          std(sfnr_avg) as sfnr_avg_std,
          avg(sfnr_min_n) as sfnr_min_n_avg,
          std(sfnr_min_n) as sfnr_min_n_std,
          avg(sfnr_max_n) as sfnr_max_n_avg,
          std(sfnr_max_n) as sfnr_max_n_std,
          avg(ln_sfnr_std_n) as ln_sfnr_std_n_avg,
          std(ln_sfnr_std_n) as ln_sfnr_std_n_std,
          avg(dur_avg) as dur_avg_avg,
          std(dur_avg) as dur_avg_std,
          avg(dur_min_n) as dur_min_n_avg,
          std(dur_min_n) as dur_min_n_std,
          avg(dur_max_n) as dur_max_n_avg,
          std(dur_max_n) as dur_max_n_std,
          avg(ln_dur_std_n) as ln_dur_std_n_avg,
          std(ln_dur_std_n) as ln_dur_std_n_std
     from zonewise_stats
     group by year;

# Aggregate over distsml to sum quantities in each small district

drop table if exists distsml_compiled;
create table distsml_compiled
     select year, distsml, instance,
          sum(commercial_sqft+industrial_sqft+governmental_sqft) as nrsf,
          sum(residential_units) as dur
     from gridcells_compiled
     group by year, distsml, instance;
create index distsml_compiled_year_distsml_instance
     on distsml_compiled (year, distsml, instance);
     
# Aggregate over all instances to get distsml-specific summary statistics for each year

drop table if exists distsml_stats;
create table distsml_stats
     select year, distsml,
          avg(nrsf) as sfnr_avg,
          min(nrsf)
               /avg(nrsf) as sfnr_min_n,
          max(nrsf)
               /avg(nrsf) as sfnr_max_n,
          std(ln(nrsf))
               /avg(ln(nrsf)) as ln_sfnr_std_n,
          avg(dur) as dur_avg,
          min(dur)
               /avg(dur) as dur_min_n,
          max(dur)
               /avg(dur) as dur_max_n,
          std(ln(dur))
               /avg(ln(dur)) as ln_dur_std_n
     from distsml_compiled
     group by year, distsml;
create index distsml_stats_year_distsml
     on distsml_stats(year, distsml);

# Pull out 2003 values from distsml_stats and create table to be used in map displays

drop table if exists distsml_stats_2003;
create table distsml_stats_2003
	select year, distsml, sfnr_avg, sfnr_min_n, sfnr_max_n, ln_sfnr_std_n,
	dur_avg, dur_min_n, dur_max_n, ln_dur_std_n
from distsml_stats
where year = 2003
group by year, distsml;
create index distsml_stats_2003_year_distsml
     on distsml_stats_2003(year, distsml);

# Aggregate over all distsml's to summarize the summary stats for each year

insert into summary_by_level
     select year, "distsml" as level,
          avg(sfnr_avg) as sfnr_avg_avg,
          std(sfnr_avg) as sfnr_avg_std,
          avg(sfnr_min_n) as sfnr_min_n_avg,
          std(sfnr_min_n) as sfnr_min_n_std,
          avg(sfnr_max_n) as sfnr_max_n_avg,
          std(sfnr_max_n) as sfnr_max_n_std,
          avg(ln_sfnr_std_n) as ln_sfnr_std_n_avg,
          std(ln_sfnr_std_n) as ln_sfnr_std_n_std,
          avg(dur_avg) as dur_avg_avg,
          std(dur_avg) as dur_avg_std,
          avg(dur_min_n) as dur_min_n_avg,
          std(dur_min_n) as dur_min_n_std,
          avg(dur_max_n) as dur_max_n_avg,
          std(dur_max_n) as dur_max_n_std,
          avg(ln_dur_std_n) as ln_dur_std_n_avg,
          std(ln_dur_std_n) as ln_dur_std_n_std
     from distsml_stats
     group by year;


# Aggregate over distmed to sum quantities in each medium district

drop table if exists distmed_compiled;
create table distmed_compiled
     select year, distmed, instance,
          sum(commercial_sqft+industrial_sqft+governmental_sqft) as nrsf,
          sum(residential_units) as dur
     from gridcells_compiled
     group by year, distmed, instance;
create index distmed_compiled_year_distmed_instance
     on distmed_compiled (year, distmed, instance);

# Aggregate over all instances to get distmed-specific summary statistics for each year

drop table if exists distmed_stats;
create table distmed_stats
     select year, distmed,
          avg(nrsf) as sfnr_avg,
          min(nrsf)
               /avg(nrsf) as sfnr_min_n,
          max(nrsf)
               /avg(nrsf) as sfnr_max_n,
          std(ln(nrsf))
               /avg(ln(nrsf)) as ln_sfnr_std_n,
          avg(dur) as dur_avg,
          min(dur)
               /avg(dur) as dur_min_n,
          max(dur)
               /avg(dur) as dur_max_n,
          std(ln(dur))
               /avg(ln(dur)) as ln_dur_std_n
     from distmed_compiled
     group by year, distmed;
create index distmed_stats_year_distmed
     on distmed_stats(year, distmed);

# Pull out 2003 values from distmed_stats and create table to be used in map displays

drop table if exists distmed_stats_2003;
create table distmed_stats_2003
	select year, distmed, sfnr_avg, sfnr_min_n, sfnr_max_n, ln_sfnr_std_n,
	dur_avg, dur_min_n, dur_max_n, ln_dur_std_n
from distmed_stats
where year = 2003
group by year, distmed;
create index distmed_stats_2003_year_distmed
     on distmed_stats_2003(year, distmed);

# Aggregate over all distmed's to summarize the summary stats for each year

insert into summary_by_level
     select year, "distmed" as level,
          avg(sfnr_avg) as sfnr_avg_avg,
          std(sfnr_avg) as sfnr_avg_std,
          avg(sfnr_min_n) as sfnr_min_n_avg,
          std(sfnr_min_n) as sfnr_min_n_std,
          avg(sfnr_max_n) as sfnr_max_n_avg,
          std(sfnr_max_n) as sfnr_max_n_std,
          avg(ln_sfnr_std_n) as ln_sfnr_std_n_avg,
          std(ln_sfnr_std_n) as ln_sfnr_std_n_std,
          avg(dur_avg) as dur_avg_avg,
          std(dur_avg) as dur_avg_std,
          avg(dur_min_n) as dur_min_n_avg,
          std(dur_min_n) as dur_min_n_std,
          avg(dur_max_n) as dur_max_n_avg,
          std(dur_max_n) as dur_max_n_std,
          avg(ln_dur_std_n) as ln_dur_std_n_avg,
          std(ln_dur_std_n) as ln_dur_std_n_std
     from distmed_stats
     group by year;


# Aggregate over distlrg to sum quantities in each large district

drop table if exists distlrg_compiled;
create table distlrg_compiled
     select year, distlrg, instance,
          sum(commercial_sqft+industrial_sqft+governmental_sqft) as nrsf,
          sum(residential_units) as dur
     from gridcells_compiled
     group by year, distlrg, instance;
create index distlrg_compiled_year_distlrg_instance
     on distlrg_compiled (year, distlrg, instance);

# Aggregate over all instances to get distlrg-specific summary statistics for each year

drop table if exists distlrg_stats;
create table distlrg_stats
     select year, distlrg,
          avg(nrsf) as sfnr_avg,
          min(nrsf)
               /avg(nrsf) as sfnr_min_n,
          max(nrsf)
               /avg(nrsf) as sfnr_max_n,
          std(ln(nrsf))
               /avg(ln(nrsf)) as ln_sfnr_std_n,
          avg(dur) as dur_avg,
          min(dur)
               /avg(dur) as dur_min_n,
          max(dur)
               /avg(dur) as dur_max_n,
          std(ln(dur))
               /avg(ln(dur)) as ln_dur_std_n
     from distlrg_compiled
     group by year, distlrg;
create index distlrg_stats_year_distlrg
     on distlrg_stats(year, distlrg);

# Pull out 2003 values from distlrg_stats and create table to be used in map displays

drop table if exists distlrg_stats_2003;
create table distlrg_stats_2003
	select year, distlrg, sfnr_avg, sfnr_min_n, sfnr_max_n, ln_sfnr_std_n,
	dur_avg, dur_min_n, dur_max_n, ln_dur_std_n
from distlrg_stats
where year = 2003
group by year, distlrg;
create index distlrg_stats_2003_year_distlrg
     on distlrg_stats_2003(year, distlrg);

# Aggregate over all distlrg's to summarize the summary stats for each year

insert into summary_by_level
     select year, "distlrg" as level,
          avg(sfnr_avg) as sfnr_avg_avg,
          std(sfnr_avg) as sfnr_avg_std,
          avg(sfnr_min_n) as sfnr_min_n_avg,
          std(sfnr_min_n) as sfnr_min_n_std,
          avg(sfnr_max_n) as sfnr_max_n_avg,
          std(sfnr_max_n) as sfnr_max_n_std,
          avg(ln_sfnr_std_n) as ln_sfnr_std_n_avg,
          std(ln_sfnr_std_n) as ln_sfnr_std_n_std,
          avg(dur_avg) as dur_avg_avg,
          std(dur_avg) as dur_avg_std,
          avg(dur_min_n) as dur_min_n_avg,
          std(dur_min_n) as dur_min_n_std,
          avg(dur_max_n) as dur_max_n_avg,
          std(dur_max_n) as dur_max_n_std,
          avg(ln_dur_std_n) as ln_dur_std_n_avg,
          std(ln_dur_std_n) as ln_dur_std_n_std
     from distlrg_stats
     group by year;


# Aggregate over county to sum quantities in each county

drop table if exists county_compiled;
create table county_compiled
     select year, county, instance,
          sum(commercial_sqft+industrial_sqft+governmental_sqft) as nrsf,
          sum(residential_units) as dur
     from gridcells_compiled
     group by year, county, instance;
create index county_compiled_year_county_instance
     on county_compiled (year, county, instance);

# Aggregate over all instances to get county-specific summary statistics for each year

drop table if exists county_stats;
create table county_stats
     select year, county,
          avg(nrsf) as sfnr_avg,
          min(nrsf)
               /avg(nrsf) as sfnr_min_n,
          max(nrsf)
               /avg(nrsf) as sfnr_max_n,
          std(ln(nrsf))
               /avg(ln(nrsf)) as ln_sfnr_std_n,
          avg(dur) as dur_avg,
          min(dur)
               /avg(dur) as dur_min_n,
          max(dur)
               /avg(dur) as dur_max_n,
          std(ln(dur))
               /avg(ln(dur)) as ln_dur_std_n
     from county_compiled
     group by year, county;
create index county_stats_year_county
     on county_stats(year, county);

# Pull out 2003 values from county_stats and create table to be used in map displays

drop table if exists county_stats_2003;
create table county_stats_2003
	select year, county, sfnr_avg, sfnr_min_n, sfnr_max_n, ln_sfnr_std_n,
	dur_avg, dur_min_n, dur_max_n, ln_dur_std_n
from county_stats
where year = 2003
group by year, county;
create index county_stats_2003_year_county
     on county_stats_2003(year, county);

# Aggregate over all county's to summarize the summary stats for each year

insert into summary_by_level
     select year, "county" as level,
          avg(sfnr_avg) as sfnr_avg_avg,
          std(sfnr_avg) as sfnr_avg_std,
          avg(sfnr_min_n) as sfnr_min_n_avg,
          std(sfnr_min_n) as sfnr_min_n_std,
          avg(sfnr_max_n) as sfnr_max_n_avg,
          std(sfnr_max_n) as sfnr_max_n_std,
          avg(ln_sfnr_std_n) as ln_sfnr_std_n_avg,
          std(ln_sfnr_std_n) as ln_sfnr_std_n_std,
          avg(dur_avg) as dur_avg_avg,
          std(dur_avg) as dur_avg_std,
          avg(dur_min_n) as dur_min_n_avg,
          std(dur_min_n) as dur_min_n_std,
          avg(dur_max_n) as dur_max_n_avg,
          std(dur_max_n) as dur_max_n_std,
          avg(ln_dur_std_n) as ln_dur_std_n_avg,
          std(ln_dur_std_n) as ln_dur_std_n_std
     from county_stats
     group by year;
     
# Aggregate over county to sum quantities in the entire region

drop table if exists region_compiled;
create table region_compiled
     select year, instance,
          sum(commercial_sqft+industrial_sqft+governmental_sqft) as nrsf,
          sum(residential_units) as dur
     from gridcells_compiled
     group by year, instance;
create index  region_compiled_year_instance
     on region_compiled(year, instance);

# Aggregate over all instances to get region-wide summary statistics for each year

drop table if exists region_stats;
create table region_stats
     select year,
          avg(nrsf) as sfnr_avg,
          min(nrsf)
               /avg(nrsf) as sfnr_min_n,
          max(nrsf)
               /avg(nrsf) as sfnr_max_n,
          std(ln(nrsf))
               /avg(ln(nrsf)) as ln_sfnr_std_n,
          avg(dur) as dur_avg,
          min(dur)
               /avg(dur) as dur_min_n,
          max(dur)
               /avg(dur) as dur_max_n,
          std(ln(dur))
               /avg(ln(dur)) as ln_dur_std_n
     from region_compiled
     group by year;
create index region_stats_year
     on region_stats(year);

# Move data to summary table

insert into summary_by_level
     select year, "region" as level,
          sfnr_avg as sfnr_avg_avg,
          NULL as sfnr_avg_std,
          sfnr_min_n as sfnr_min_n_avg,
          NULL as sfnr_min_n_std,
          sfnr_max_n as sfnr_max_n_avg,
          NULL as sfnr_max_n_std,
          ln_sfnr_std_n as ln_sfnr_std_n_avg,
          NULL as ln_sfnr_std_n_std,
          dur_avg as dur_avg_avg,
          NULL as dur_avg_std,
          dur_min_n as dur_min_n_avg,
          NULL as dur_min_n_std,
          dur_max_n as dur_max_n_avg,
          NULL as dur_max_n_std,
          ln_dur_std_n as ln_dur_std_n_avg,
          NULL as ln_dur_std_n_std
     from region_stats
     group by year;

# Show some key results

select level, sfnr_min_n_avg, sfnr_max_n_avg, dur_min_n_avg, dur_max_n_avg
     from summary_by_level;

select level, ln_sfnr_std_n_avg, ln_dur_std_n_avg
     from summary_by_level;
