create table psrc_2005_parcel_baseyear.gridcells
     like GSPSRC_2000_baseyear_change_20061018.gridcells;

insert into psrc_2005_parcel_baseyear.gridcells
     select *
     from GSPSRC_2000_baseyear_change_20061018.gridcells;

create table psrc_2005_parcel_baseyear.jobs
     like GSPSRC_2000_baseyear_change_20060405.jobs;

insert into psrc_2005_parcel_baseyear.jobs
     select *
     from GSPSRC_2000_baseyear_change_20060405.jobs;

