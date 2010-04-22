##create business_for_estimation using random sampling from business table.

drop table if exists business_for_estimation;

create table business_for_estimation
select * from business b
	where building_id > 0 and sector_id = 1 and b.employment>0 and b.sqft>0
	order by rand() limit 5000;

insert into business_for_estimation
select * from business b
	where building_id > 0 and sector_id = 2 and b.employment>0 and b.sqft>0
	order by rand() limit 5000;
	
insert into business_for_estimation
select * from business b
	where building_id > 0 and sector_id = 3 and b.employment>0 and b.sqft>0
	order by rand() limit 5000;	

insert into business_for_estimation
select * from business b
	where building_id > 0 and sector_id = 4 and b.employment>0 and b.sqft>0
	order by rand() limit 5000;	

insert into business_for_estimation
select * from business b
	where building_id > 0 and sector_id = 5 and b.employment>0 and b.sqft>0
	order by rand() limit 5000;

insert into business_for_estimation
select * from business b
	where building_id > 0 and sector_id = 6 and b.employment>0 and b.sqft>0
	order by rand() limit 5000;
