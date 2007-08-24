alter table development_events_exogenous add blklot varchar(9);
update development_events_exogenous set blklot = mapblklot;

#One loose end to take care of: adding zone_id to parcels
alter table parcels add zone_id int(32);
update parcels set zone_id = taz;