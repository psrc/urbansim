

use psrc_2005_data_workspace;

# Create a plan_types table that includes constraints data

drop table if exists plan_types_new;
create table plan_types_new (
     plan_type_id int primary key,
     min_res_density int,
     max_res_density int,
     max_far_sfr double,
     max_far_mfr double,
     max_far_com double,
     max_far_ind double);

insert into plan_types_new (plan_type_id)
     select plan_type_id
     from plan_types;

update plan_types_new as p, development_constraints as d
     set p.min_res_density = d.minimum_units_per_acre,
         p.max_res_density = d.maximum_units_per_acre,
         p.max_far_sfr = d.maximum_far
     where p.plan_type_id = d.plan_type_id
          and d.development_constraint_type_id = 1;

update plan_types_new as p, development_constraints as d
     set p.max_far_mfr = d.maximum_far
     where p.plan_type_id = d.plan_type_id
          and d.development_constraint_type_id = 2;

update plan_types_new as p, development_constraints as d
     set p.max_far_com = d.maximum_far
     where p.plan_type_id = d.plan_type_id
          and d.development_constraint_type_id = 3;

update plan_types_new as p, development_constraints as d
     set p.max_far_ind = d.maximum_far
     where p.plan_type_id = d.plan_type_id
          and d.development_constraint_type_id = 4;

# Replace original plan_types table

drop table if exists plan_types;
rename table plan_types_new
     to plan_types;

# Attach plan_types_ids to parcel_plan_types

alter table parcel_plan_types
     add column plan_type_id int;

update parcel_plan_types p, plan_types t
     set p.plan_type_id = t.plan_type_id
     where p.MINRESD = t.min_res_density
          and p.MAXRESD = t.min_res_density
          and p.