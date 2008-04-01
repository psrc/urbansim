## Percent of units inside UGB by year

create table percent_units_in_ugb (year int, units_in_ugb double, total_units double, percent double)
;
insert into percent_units_in_ugb (year) select distinct year from gridcells_exported_denormalized
;
create temporary table tmp_units_in_ugb
 select year, sum(residential_units) as units
 from gridcells_exported_denormalized
 where IS_OUTSIDE_URBAN_GROWTH_BOUNDARY = 0
 group by year
;

update percent_units_in_ugb a inner join tmp_units_in_ugb b on a.year = b.year 
 set a.units_in_ugb = b.units
;
create temporary table tmp_total_units
 select year, sum(residential_units) as units
 from gridcells_exported_denormalized
 group by year
;

update percent_units_in_ugb a inner join tmp_total_units b on a.year = b.year
 set a.total_units = b.units
; 
update percent_units_in_ugb set percent = ((units_in_ugb / total_units)*100)
;
insert into result (year, geography_id, indicator_value)
 select gc.year,
 	1,
 	percent as INDICATOR_VALUE
 from percent_units_in_ugb
; 

drop table tmp_units_in_ugb;
drop table tmp_total_units;
drop table percent_units_in_ugb;

## Percent of units inside urbans centers by year

create table percent_units_in_urbancenter (year int, units_in_centers double, total_units double, percent double)
;
insert into percent_units_in_urbancenter (year) select distinct year from gridcells_exported_denormalized
;
create temporary table tmp_units_in_center 
 select year, sum(residential_units) as units
 from gridcells_exported a inner join PSRC_2000_reclassification_tables.gridcell_to_urban_centers b 
 on a.grid_id = b.grid_id
 where b.urban_center is not null
 group by year
; 
update percent_units_in_urbancenter a inner join tmp_units_in_center b on a.year = b.year
 set a.units_in_centers = b.units
;
create temporary table tmp_total_units
 select year, sum(residential_units) as units
 from gridcells_exported_denormalized
 group by year
;
update percent_units_in_urbancenter a inner join tmp_total_units b on a.year = b.year
 set a.total_units = b.units
;
update percent_units_in_urbancenter set percent = ((units_in_centers / total_units)*100)
;
drop table tmp_units_in_center;
drop table tmp_total_units;


## 
