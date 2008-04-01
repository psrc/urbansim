
# This script eliminates duplicate parcel and
# building records, i.e. those with different 
# internal parcel_id's and building_id's,
# but the same "id_parcel" (i.e. the composite
# of county-code and parcel-code).


use psrc_2005_data_workspace;

# Create a list of superfluous parcel records
# and their internal "parcel_id"'s

drop table if exists duplicate_parcels;
create table duplicate_parcels
     select id_parcel,
            max(parcel_id) as parcel_id
     from parcels
     where duplicates > 1
     group by id_parcel;

create index duplicate_parcels_id_parcel
     on duplicate_parcels (id_parcel);
     
create index duplicate_parcels_parcel_id
     on duplicate_parcels (parcel_id);

alter table parcels
     add column is_duplicate int;

alter table buildings
     add column is_duplicate int;

update parcels p, duplicate_parcels d
     set p.is_duplicate = 1
     where p.parcel_id = d.parcel_id;

update buildings b, duplicate_parcels d
     set b.is_duplicate = 1
     where b.parcel_id = d.parcel_id;
     
delete from parcels
     where is_duplicate = 1;

delete from buildings
     where is_duplicate = 1;



