

# (1) Setup database chain for year 2005 [Should only ever do this once]

## If not done already:
#create database psrc_2005_parcel_baseyear_start;
#use psrc_2005_parcel_baseyear_start;
#drop table if exists scenario_information;
#create table scenario_information (
#     END_YEAR int,
#     DESCRIPTION char(255),
#     PARENT_DATABASE_URL char(255),
#     CONTINUATION tinyint(4));
#insert into scenario_information
#     values (2030, "psrc_2005_parcel_baseyear", NULL, 0);
#create database psrc_2005_parcel_baseyear;


# (2) Update the baseyear databse for newest changes [Should do this each day that a table is updated]

use psrc_2005_parcel_baseyear;

update scenario_information
     set PARENT_DATABASE_URL = 
             "jdbc:mysql://trondheim.cs.washington.edu/psrc_2005_parcel_baseyear_change_20070518"; # <- *** update with new date ***

# (3) Create new change database [ Also do this each day that a table is updated ]

create database psrc_2005_parcel_baseyear_change_20070518; # <- *** update with new date ***

use psrc_2005_parcel_baseyear_change_20070518; # <- *** update with new date ***

create table scenario_information
     like psrc_2005_parcel_baseyear.scenario_information;

insert into scenario_information
     select * from psrc_2005_parcel_baseyear.scenario_information;

update scenario_information
     set PARENT_DATABASE_URL = 
          "jdbc:mysql://trondheim.cs.washington.edu/psrc_2005_parcel_baseyear_change_20070517"; # <- *** update with PREVIOUS date in chain ***

# IN HERE: add your updated tables to this database.

create table change_log
     like GSPSRC_2000_baseyear_change_20070411.change_log; # <- *** update with PREVIOUS date in chain ***

insert into change_log
     values ("add column", # <- what operation? (e.g. insert, update, delete, create, etc.)
             "households", # <- what table?
             "Joel Franklin", # <- your name?
             "added grid_id to households"); # <- describe what you did
