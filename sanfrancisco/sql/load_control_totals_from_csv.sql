drop table if exists annual_household_control_totals_backup;
drop table if exists annual_business_control_totals_backup;

create table annual_household_control_totals_backup SELECT * FROM annual_household_control_totals a;
create table annual_business_control_totals_backup SELECT * FROM annual_business_control_totals a;

drop table if exists annual_household_control_totals;
drop table if exists annual_business_control_totals;

create table annual_household_control_totals
  (year int, total_number_of_households int);

create table annual_business_control_totals
  (year int, sector_id int, total_number_of_businesses int);

load data local infile 'Z:/Research/Projects/San Francisco/data/Control Totals/annual_household_control_totals.csv'
  into table annual_household_control_totals
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES;

load data local infile 'Z:/Research/Projects/San Francisco/data/Control Totals/annual_business_control_totals.csv'
  into table annual_business_control_totals
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES;
