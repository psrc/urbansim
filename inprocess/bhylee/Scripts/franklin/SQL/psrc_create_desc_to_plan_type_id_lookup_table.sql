

use psrc_2005_data_workspace;

# extract "id_parcel"s with "Description"s

drop table if exists temp_parcel_descriptions;
create table temp_parcel_descriptions
     select ID_PARCEL,
            Description
     from all_parcels_merged_jpf;

create index temp_p_d_id_parcel
     on temp_parcel_descriptions (ID_PARCEL);
     
# extract "id_parcel"s with "plan_type_id"s

drop table if exists temp_parcel_plan_type_ids;
create table temp_parcel_plan_type_ids
     select id_parcel,
            plan_type_id
     from parcels;

create index temp_p_pti_id_parcel
     on temp_parcel_plan_type_ids (id_parcel);

# merge them

drop table if exists temp_p_desc_plan_type;
create table temp_p_desc_plan_type
     select d.ID_PARCEL,
            d.Description,
            t.plan_type_id
     from temp_parcel_descriptions as d
     left join temp_parcel_plan_type_ids as t
          on d.ID_PARCEL = t.id_parcel;

# reduce to distinct Descriptions & plan_type_ids, and count frequencies

drop table if exists temp_descriptions_plan_types;
create table temp_descriptions_plan_types
     select Description,
            plan_type_id,
            count(*) as freq
     from temp_p_desc_plan_type
     group by Description,
              plan_type_id;

drop table if exists temp_desc_max_freq;
create table temp_desc_max_freq
     select Description,
            max(freq) as max_freq
     from temp_descriptions_plan_types
          group by Description;

drop table if exists regflu_descriptions;
create table regflu_descriptions
     select d.Description,
            d.plan_type_id,
            d.freq,
            m.max_freq
     from temp_descriptions_plan_types as d
     left join temp_desc_max_freq as m
          on d.Description = m.Description;

delete from regflu_descriptions
     where freq != max_freq;

delete from regflu_descriptions
     where plan_type_id is null;

alter table regflu_descriptions
     drop column freq,
     drop column max_freq;

# Clean up

drop table if exists temp_parcel_descriptions;
drop table if exists temp_parcel_plan_type_ids;
drop table if exists temp_p_desc_plan_type;
drop table if exists temp_descriptions_plan_types;
drop table if exists temp_desc_max_freq;
drop table if exists regflu_descriptions;
