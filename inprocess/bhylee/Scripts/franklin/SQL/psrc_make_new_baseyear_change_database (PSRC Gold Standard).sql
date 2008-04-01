

# (1) Setup database chain for year 2000 [Should only ever do this once]

## If not done already:
#create database GSPSRC_2000_baseyear_start;
#use GSPSRC_2000_baseyear_start;
#drop table if exists scenario_information;
#create table scenario_information (
#     END_YEAR int,
#     DESCRIPTION char(255),
#     PARENT_DATABASE_URL char(255),
#     CONTINUATION tinyint(4));
#insert into scenario_information
#     values (2030, "GSPSRC_2000_baseyear", NULL, 0);
#create database GSPSRC_2000_baseyear;


# (2) Update the baseyear databse for newest changes [ Should do this each day that a table is updated ]

use GSPSRC_2000_baseyear;

select * from scenario_information;

update scenario_information
     set PARENT_DATABASE_URL = 
          "jdbc:mysql://trondheim.cs.washington.edu/GSPSRC_2000_baseyear_change_20070510"; # <- *** update with new date ***

select * from scenario_information;

# (3) Create new change database [ Also do this each day that a table is updated ]

create database GSPSRC_2000_baseyear_change_20070510; # <- *** update with new date ***

use GSPSRC_2000_baseyear_change_20070510; # <- *** update with new date ***

create table scenario_information
     like GSPSRC_2000_baseyear.scenario_information;

insert into scenario_information
     select * from GSPSRC_2000_baseyear.scenario_information;

update scenario_information
     set PARENT_DATABASE_URL = 
          "jdbc:mysql://trondheim.cs.washington.edu/GSPSRC_2000_baseyear_change_20070504"; # <- *** update with PREVIOUS date in chain ***

# IN HERE: add your updated tables to this database.


# Enter info into a change log

create table change_log
     like GSPSRC_2000_baseyear_change_20070411.change_log; # <- *** update with PREVIOUS date in chain ***

insert into change_log
     values ("operation", # <- what operation? (e.g. insert, update, delete, create, etc.)
             "table", # <- what table?
             "Joel Franklin", # <- your name?
             "description"); # <- describe what you did

             



