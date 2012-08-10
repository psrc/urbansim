create table scheduled_development_events (	
	site varchar(64) default '',
	project varchar(256) default '',
	parcel_id int default -1,
	scheduled_year int default -1,
	action varchar(32),
	building_sqft int default -1,
	building_type_id int default -1,
	building_type_short_name varchar(64) default '',
	non_residential_sqft int default 0,
	residential_units int default 0,
	residential_sqft int default 0,
	tenure varchar(16) default '',
	non_residential_rent int default 0,
	stories int default 0,
	bedrooms int default 0,
	rent int default 0,
	building_id int default -1,
	sale_price int default 0,
	unit_sqft int default 0
);
	
\copy scheduled_development_events from '/home/lmwang/documents/work/mtc/pipe_np.csv' csv header;

create sequence scheduled_event_id_seq;
alter table scheduled_development_events 
	add scheduled_event_id int default -1,
	add scenario_id int default -1
;

update scheduled_development_events 
	set scheduled_event_id = nextval(scheduled_event_id_seq);
update scheduled_development_events
	set scenario_id = scenario.id
	from scenario where scenario.name='No Project'
;

create or replace view urbansim.scheduled_development_events as
	select scheduled_event_id,
	name as scenario_name,
	parcel_id,
	year_built as scheduled_year,
	COALESCE(building_type_id, (-1)) AS building_type_id,
	COALESCE(building_sqft, (0)) AS building_sqft,
	COALESCE(non_residential_sqft, (0)) AS non_residential_sqft,
	COALESCE(residential_units, (0)) AS residential_units,
	COALESCE(residential_sqft, (0)) AS residential_sqft,
	case when tenure='rent' then 1 else 2 end as tenure,
	COALESCE(non_residential_rent, (0)) AS non_residential_rent,
	COALESCE(stories, (1)) AS stories,
	COALESCE(bedrooms, (0)) AS bedrooms,
	COALESCE(rent, (0)) AS rent,
	COALESCE(sale_price, (0)) AS sale_price,
	COALESCE(unit_sqft, (0)) AS unit_sqft 
	from public.scheduled_development_events s inner join scenario on s.scenario_id=scenario.id
  WHERE s.building_type_id IS NOT NULL;


