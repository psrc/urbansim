create index blklot_index on buildings (blklot(16));
create index blklot_index on business (blklot(16));

update business set building_id = -1;

update business bs, building bl set bs.building_id = bl.building_id
where bs.blklot = bl.blklot;

## create business from estimation
drop table if exists business_for_estimation;

create table business_for_estimation
select * from business 
	where building_id > 0 and sector_id = 1 and b.employment>0 and b.sqft>0
	order by rand() limit 5000;

insert into business_for_estimation
select * from business 
	where building_id > 0 and sector_id = 2 and b.employment>0 and b.sqft>0
	order by rand() limit 5000;
	
insert into business_for_estimation
select * from business 
	where building_id > 0 and sector_id = 3 and b.employment>0 and b.sqft>0
	order by rand() limit 5000;	

insert into business_for_estimation
select * from business 
	where building_id > 0 and sector_id = 4 and b.employment>0 and b.sqft>0
	order by rand() limit 5000;	

insert into business_for_estimation
select * from business 
	where building_id > 0 and sector_id = 5 and b.employment>0 and b.sqft>0
	order by rand() limit 5000;	

insert into business_for_estimation
select * from business 
	where building_id > 0 and sector_id = 6 and b.employment>0 and b.sqft>0
	order by rand() limit 5000;
				