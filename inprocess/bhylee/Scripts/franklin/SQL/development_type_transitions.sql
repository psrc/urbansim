drop table if exists tmp_gridcells_1997;
create temporary table tmp_gridcells_1997
     select grid_id,
          development_type_id
     from gridcells_exported
     where year=1997;
create index tmp_gridcells_1997_grid_id_index on tmp_gridcells_1997 (grid_id);

drop table if exists tmp_gridcells_2030;
create temporary table tmp_gridcells_2030
     select grid_id,
          development_type_id
     from gridcells_exported
     where year=2030;
create index tmp_gridcells_2030_grid_id_index on tmp_gridcells_2030 (grid_id);

drop table if exists development_type_transitions;
create table development_type_transitions
     select gc1997.grid_id as grid_id,
          gc1997.development_type_id as development_type_1997,
          gc2030.development_type_id as development_type_2030
     from tmp_gridcells_1997 as gc1997
     inner join tmp_gridcells_2030 as gc2030
          on gc1997.grid_id=gc2030.grid_id;
create index development_type_transitions_grid_id_index on development_type_transitions (grid_id);

drop table if exists development_type_transition_summary;
create table development_type_transition_summary
     select development_type_1997,
          development_type_2030,
          count(*) as number_of_transitions
     from development_type_transitions
     group by development_type_1997,
          development_type_2030;
