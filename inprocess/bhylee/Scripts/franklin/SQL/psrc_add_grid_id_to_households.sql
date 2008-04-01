
# Attach grid_ids to households in the PSRC 2005 baseyear,
# using associations from the GSPSRC 2000 baseyear chain.

use psrc_2005_parcel_baseyear_change_20070515

create table households
     like psrc_2005_data_workspace.households;

alter table households
     add column grid_id int;

insert into households
     select h.*,
            p.grid_id
     from psrc_2005_data_workspace.households as h
     left join psrc_2005_data_workspace.parcels p
          on h.parcel_id = p.parcel_id;

update households
     set grid_id = -1 where grid_id is null;

