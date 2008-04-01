

$ Create table of households that move between years
drop table hhmove;
create table hhmove 
select b.year,b.grid_id,count(b.household_id) as numhh 
from households_exported as a, households_exported as b
where a.year = b.year - 1 and a.grid_id <> b.grid_id
	and a.household_id = b.household_id
group by b.grid_id,b.year;


create index hhmove_grid_id_index on hhmove (grid_id);
create index hhmove_grid_id_index on Eugene_1980_output_gfu.hhmove (grid_id);

create table hhinsr
select hhmove.grid_id, 1 as scenario
from hhmove left join Eugene_1980_output_gfu.hhmove as b
	on hhmove.grid_id = b.grid_id
where b.grid_id is NULL
	union
select b.grid_id, -1 as scenario
from hhmove right join Eugene_1980_output_gfu.hhmove as b
	on hhmove.grid_id = b.grid_id
where hhmove.grid_id is NULL ;