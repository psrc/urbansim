alter table development_events_exogenous add blklot varchar(9);
update development_events_exogenous set blklot = mapblklot;

