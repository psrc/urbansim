update buildout set Softsite2005 = 0 where Softsite2005 is null;
update buildout set Ressqft = 0 where Ressqft is null;
alter table parcels add residential_units_capacity int(32);
alter table parcels add building_sqft_capacity int(32);
alter table parcels add index (mapblklot);
alter table buildout add index (Mapblklot2001);
update parcels p, buildout b set p.residential_units_capacity = b.pot_units where p.mapblklot = b.Mapblklot2001;
update parcels p, buildout b set p.building_sqft_capacity = b.tot_pot_sqft where p.mapblklot = b.Mapblklot2001;
update parcels set residential_units_capacity = 0 where residential_units_capacity is null;
update parcels set building_sqft_capacity = 0 where building_sqft_capacity is null;

#There are 861 records that apparently do not find a match between 2000 and 2001, and end up with no parcel_id - delete for now:
delete from parcels where parcel_id is null;
delete from buildings where parcel_id is null;