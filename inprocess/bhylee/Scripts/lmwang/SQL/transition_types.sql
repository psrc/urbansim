-- this script will take forever to run in mysql, please use 
-- perl script transition_types.pl instead.

set session tmp_table_size  = 16 * 1024 * 1024 * 1024;
set session max_heap_table_size = 1 * 1024 * 1024 * 1024;

#use PSRC_2000_baseyear_lmwang;

#create index development_event_history_dev_type_index
# 	on development_event_history
# 	(starting_development_type_id, ending_development_type_id)
#; 

drop table if exists tt_temp_units_sqft_impv_means;
create table 
	tt_temp_units_sqft_impv_means
select
	h1.starting_development_type_id,
	h1.ending_development_type_id,
	count(*) as n,
	avg(h1.residential_units) as HOUSING_UNITS_MEAN,
	avg(h1.commercial_sqft) as COMMERCIAL_SQFT_MEAN,
	avg(h1.industrial_sqft) as INDUSTRIAL_SQFT_MEAN,
	avg(h1.governmental_sqft) as GOVERNMENTAL_SQFT_MEAN,
	avg(h1.residential_improvement_value) as HOUSING_IMPROVEMENT_VALUE_MEAN,
	avg(h1.commercial_improvement_value) as COMMERCIAL_IMPROVEMENT_VALUE_MEAN,
	avg(h1.industrial_improvement_value) as INDUSTRIAL_IMPROVEMENT_VALUE_MEAN,
	avg(h1.governmental_improvement_value) as GOVERNMENTAL_IMPROVEMENT_VALUE_MEAN
from
	development_event_history h1
group by 
	h1.starting_development_type_id,
	h1.ending_development_type_id
;

create index tt_temp_units_sqft_impv_means_index
	on tt_temp_units_sqft_impv_means
	(starting_development_type_id, ending_development_type_id)
; 

drop table if exists tt_temp_dev_event_history_w_means_sq_residuals;
create table tt_temp_dev_event_history_w_means_sq_residuals (
	GRID_ID int,
	STARTING_DEVELOPMENT_TYPE_ID int,
	ENDING_DEVELOPMENT_TYPE_ID int,
	RESIDENTIAL_UNITS int,
	COMMERCIAL_SQFT int,
	INDUSTRIAL_SQFT int,
	GOVERNMENTAL_SQFT int,
	RESIDENTIAL_IMPROVEMENT_VALUE int,
	COMMERCIAL_IMPROVEMENT_VALUE int,
	INDUSTRIAL_IMPROVEMENT_VALUE int,
	GOVERNMENTAL_IMPROVEMENT_VALUE int,
	FRACTION_RESIDENTIAL_LAND_VALUE int,
	N int,
	HOUSING_UNITS_MEAN double,
	COMMERCIAL_SQFT_MEAN double,
	INDUSTRIAL_SQFT_MEAN double, 
	GOVERNMENTAL_SQFT_MEAN double,
	HOUSING_IMPROVEMENT_VALUE_MEAN double,
	COMMERCIAL_IMPROVEMENT_VALUE_MEAN double,
	INDUSTRIAL_IMPROVEMENT_VALUE_MEAN double,
	GOVERNMENTAL_IMPROVEMENT_VALUE_MEAN double
);

insert into tt_temp_dev_event_history_w_means_sq_residuals
select
h.GRID_ID,
h.STARTING_DEVELOPMENT_TYPE_ID,
h.ENDING_DEVELOPMENT_TYPE_ID,
h.RESIDENTIAL_UNITS,
h.COMMERCIAL_SQFT,
h.INDUSTRIAL_SQFT,
h.GOVERNMENTAL_SQFT,
h.RESIDENTIAL_IMPROVEMENT_VALUE,
h.COMMERCIAL_IMPROVEMENT_VALUE,
h.INDUSTRIAL_IMPROVEMENT_VALUE,
h.GOVERNMENTAL_IMPROVEMENT_VALUE,
h.FRACTION_RESIDENTIAL_LAND_VALUE,
t.N,
t.HOUSING_UNITS_MEAN,
t.COMMERCIAL_SQFT_MEAN,
t.INDUSTRIAL_SQFT_MEAN,
t.GOVERNMENTAL_SQFT_MEAN,
t.HOUSING_IMPROVEMENT_VALUE_MEAN,
t.COMMERCIAL_IMPROVEMENT_VALUE_MEAN,
t.INDUSTRIAL_IMPROVEMENT_VALUE_MEAN,
t.GOVERNMENTAL_IMPROVEMENT_VALUE_MEAN
from
 development_event_history h
 left outer join tt_temp_units_sqft_impv_means t
 on h.starting_development_type_id = t.starting_development_type_id
    and h.ending_development_type_id = t.ending_development_type_id
;

alter table tt_temp_dev_event_history_w_means_sq_residuals
add HOUSING_UNITS_SR double,
add COMMERCIAL_SQFT_SR double,
add INDUSTRIAL_SQFT_SR double,
add GOVERNMENTAL_SQFT_SR double,
add HOUSING_IMPROVEMENT_VALUE_SR double,
add COMMERCIAL_IMPROVEMENT_VALUE_SR double,
add INDUSTRIAL_IMPROVEMENT_VALUE_SR double,
add GOVERNMENTAL_IMPROVEMENT_VALUE_SR double
;

update tt_temp_dev_event_history_w_means_sq_residuals
set HOUSING_UNITS_SR = POW((RESIDENTIAL_UNITS - HOUSING_UNITS_MEAN), 2),
    COMMERCIAL_SQFT_SR = POW((COMMERCIAL_SQFT - COMMERCIAL_SQFT_MEAN), 2),
    INDUSTRIAL_SQFT_SR = POW((INDUSTRIAL_SQFT - INDUSTRIAL_SQFT_MEAN), 2),
    GOVERNMENTAL_SQFT_SR = POW((GOVERNMENTAL_SQFT - GOVERNMENTAL_SQFT_MEAN), 2),
    HOUSING_IMPROVEMENT_VALUE_SR = POW((RESIDENTIAL_IMPROVEMENT_VALUE - HOUSING_IMPROVEMENT_VALUE_MEAN), 2),
    COMMERCIAL_IMPROVEMENT_VALUE_SR = POW((COMMERCIAL_IMPROVEMENT_VALUE - COMMERCIAL_IMPROVEMENT_VALUE_MEAN), 2),
    INDUSTRIAL_IMPROVEMENT_VALUE_SR = POW((INDUSTRIAL_IMPROVEMENT_VALUE - INDUSTRIAL_IMPROVEMENT_VALUE_MEAN), 2),
    GOVERNMENTAL_IMPROVEMENT_VALUE_SR = POW((GOVERNMENTAL_IMPROVEMENT_VALUE - GOVERNMENTAL_IMPROVEMENT_VALUE_MEAN), 2)
;

drop table if exists transition_types;
create table transition_types (
TRANSITION_ID int(11) AUTO_INCREMENT PRIMARY KEY,
INCLUDE_IN_DEVELOPER_MODEL tinyint(1),
STARTING_DEVELOPMENT_TYPE_ID int(11),
ENDING_DEVELOPMENT_TYPE_ID int(11),
HOUSING_UNITS_MEAN double,
HOUSING_UNITS_STANDARD_DEVIATION double,
HOUSING_UNITS_MIN int(11),
HOUSING_UNITS_MAX int(11),
COMMERCIAL_SQFT_MEAN double,
COMMERCIAL_SQFT_STANDARD_DEVIATION double,
COMMERCIAL_SQFT_MIN int(11),
COMMERCIAL_SQFT_MAX int(11),
INDUSTRIAL_SQFT_MEAN double,
INDUSTRIAL_SQFT_STANDARD_DEVIATION double,
INDUSTRIAL_SQFT_MIN int(11),
INDUSTRIAL_SQFT_MAX int(11),
GOVERNMENTAL_SQFT_MEAN double,
GOVERNMENTAL_SQFT_STANDARD_DEVIATION double,
GOVERNMENTAL_SQFT_MIN int(11),
GOVERNMENTAL_SQFT_MAX int(11),
HOUSING_IMPROVEMENT_VALUE_MEAN double,
HOUSING_IMPROVEMENT_VALUE_STANDARD_DEVIATION double,
HOUSING_IMPROVEMENT_VALUE_MIN int(11),
HOUSING_IMPROVEMENT_VALUE_MAX int(11),
COMMERCIAL_IMPROVEMENT_VALUE_MEAN double,
COMMERCIAL_IMPROVEMENT_VALUE_STANDARD_DEVIATION double,
COMMERCIAL_IMPROVEMENT_VALUE_MIN int(11),
COMMERCIAL_IMPROVEMENT_VALUE_MAX int(11),
INDUSTRIAL_IMPROVEMENT_VALUE_MEAN double,
INDUSTRIAL_IMPROVEMENT_VALUE_STANDARD_DEVIATION double,
INDUSTRIAL_IMPROVEMENT_VALUE_MIN int(11),
INDUSTRIAL_IMPROVEMENT_VALUE_MAX int(11),
GOVERNMENTAL_IMPROVEMENT_VALUE_MEAN double,
GOVERNMENTAL_IMPROVEMENT_VALUE_STANDARD_DEVIATION double,
GOVERNMENTAL_IMPROVEMENT_VALUE_MIN int(11),
GOVERNMENTAL_IMPROVEMENT_VALUE_MAX int(11),
YEARS_TO_BUILD int(11) default 1
);

insert into transition_types (
INCLUDE_IN_DEVELOPER_MODEL,
STARTING_DEVELOPMENT_TYPE_ID,
ENDING_DEVELOPMENT_TYPE_ID,
HOUSING_UNITS_MEAN,
HOUSING_UNITS_STANDARD_DEVIATION,
HOUSING_UNITS_MIN,
HOUSING_UNITS_MAX,
COMMERCIAL_SQFT_MEAN,
COMMERCIAL_SQFT_STANDARD_DEVIATION,
COMMERCIAL_SQFT_MIN,
COMMERCIAL_SQFT_MAX,
INDUSTRIAL_SQFT_MEAN,
INDUSTRIAL_SQFT_STANDARD_DEVIATION,
INDUSTRIAL_SQFT_MIN,
INDUSTRIAL_SQFT_MAX,
GOVERNMENTAL_SQFT_MEAN,
GOVERNMENTAL_SQFT_STANDARD_DEVIATION,
GOVERNMENTAL_SQFT_MIN,
GOVERNMENTAL_SQFT_MAX,
HOUSING_IMPROVEMENT_VALUE_MEAN,
HOUSING_IMPROVEMENT_VALUE_STANDARD_DEVIATION,
HOUSING_IMPROVEMENT_VALUE_MIN,
HOUSING_IMPROVEMENT_VALUE_MAX,
COMMERCIAL_IMPROVEMENT_VALUE_MEAN,
COMMERCIAL_IMPROVEMENT_VALUE_STANDARD_DEVIATION,
COMMERCIAL_IMPROVEMENT_VALUE_MIN,
COMMERCIAL_IMPROVEMENT_VALUE_MAX,
INDUSTRIAL_IMPROVEMENT_VALUE_MEAN,
INDUSTRIAL_IMPROVEMENT_VALUE_STANDARD_DEVIATION,
INDUSTRIAL_IMPROVEMENT_VALUE_MIN,
INDUSTRIAL_IMPROVEMENT_VALUE_MAX,
GOVERNMENTAL_IMPROVEMENT_VALUE_MEAN,
GOVERNMENTAL_IMPROVEMENT_VALUE_STANDARD_DEVIATION,
GOVERNMENTAL_IMPROVEMENT_VALUE_MIN,
GOVERNMENTAL_IMPROVEMENT_VALUE_MAX
)
select
	1,
	hms1.starting_development_type_id,
	hms1.ending_development_type_id,
	hms1.HOUSING_UNITS_MEAN,
	sqrt(sum(hms1.housing_units_sr)/(N-1)),
	min(hms1.residential_units),
	max(hms1.residential_units),
	hms1.COMMERCIAL_SQFT_MEAN,
	sqrt(sum(hms1.commercial_sqft_sr)/(N-1)),
	min(hms1.commercial_sqft),
	max(hms1.commercial_sqft),
	hms1.INDUSTRIAL_SQFT_MEAN,
	sqrt(sum(hms1.industrial_sqft_sr)/(N-1)),
	min(hms1.industrial_sqft),
	max(hms1.industrial_sqft),
	hms1.GOVERNMENTAL_SQFT_MEAN,
	sqrt(sum(hms1.governmental_sqft_sr)/(N-1)),
	min(hms1.governmental_sqft),
	max(hms1.governmental_sqft),
	hms1.HOUSING_IMPROVEMENT_VALUE_MEAN,
	sqrt(sum(hms1.housing_improvement_value_sr)/(N-1)),
	min(hms1.residential_improvement_value),
	max(hms1.residential_improvement_value),
	hms1.COMMERCIAL_IMPROVEMENT_VALUE_MEAN,
	sqrt(sum(hms1.commercial_improvement_value_sr)/(N-1)),
	min(hms1.commercial_improvement_value),
	max(hms1.commercial_improvement_value),
	hms1.INDUSTRIAL_IMPROVEMENT_VALUE_MEAN,
	sqrt(sum(hms1.industrial_improvement_value_sr)/(N-1)),
	min(hms1.industrial_improvement_value),
	max(hms1.industrial_improvement_value),
	hms1.GOVERNMENTAL_IMPROVEMENT_VALUE_MEAN,
	sqrt(sum(hms1.governmental_improvement_value_sr)/(N-1)),
	min(hms1.governmental_improvement_value),
	max(hms1.governmental_improvement_value)
from
	tt_temp_dev_event_history_w_means_sq_residuals hms1
group by 
hms1.starting_development_type_id,
hms1.ending_development_type_id
;

delete from transition_types
where ending_development_type_id >= 24;

drop table tt_temp_units_sqft_impv_means;
drop table tt_temp_dev_event_history_w_means_sq_residuals;
