--select f.faz_id, 2000 as year, count(*) as counts 
--from GSPSRC_2000_baseyear_flattened.households as hh  
--left outer join GSPSRC_2000_baseyear_flattened.gridcells as gc 
--	  on hh.grid_id = gc.grid_id 
--	left outer join GSPSRC_2000_baseyear_flattened.zones_in_faz f 
--	  on gc.zone_id = f.zone_id 
--group by faz_id


#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

#  Author: Liming Wang

--USE PSRC_2000_data_quality_indicators;

##### Get preliminary values

DROP TABLE IF EXISTS preliminary_values;
CREATE TEMPORARY TABLE preliminary_values (
	group_field_1 int,
	group_field_2 int,
	value double
);

-- # change the field name to be used to create percentile table # --
INSERT INTO preliminary_values
SELECT
	year,
	development_type_id,
	ifnull(residential_land_value,0) + ifnull(nonresidential_land_value,0)
FROM
	gridcells_exported
;	

##### Get ordered list of values, with one column listing row numbers

DROP TABLE IF EXISTS ordered_values;
CREATE TEMPORARY TABLE ordered_values
SELECT 
	group_field_1,
	group_field_2,
	value
FROM 
	preliminary_values
ORDER BY
	group_field_1,
	group_field_2,
	value
;

alter table ordered_values
add rec_number INT AUTO_INCREMENT PRIMARY KEY
--,add descriptive_field varchar(8)
;

########## Construct table of percentiles #################

DROP TABLE IF EXISTS percentiles;
CREATE TEMPORARY TABLE percentiles (PERCENTILE double);

INSERT INTO percentiles (PERCENTILE) 
VALUES
	(0.0),
	(.01),
	(.05),
	(.1),
	(.25),
	(.5),
	(.75),
	(.9),
	(.95),
	(.99),
	(1)
;

# Get list of max, min row values for each group field  in
#	ordered_values

DROP TABLE IF EXISTS group_row_limits;
CREATE TEMPORARY TABLE group_row_limits
SELECT 
	group_field_1, 
	group_field_2, 
	count(*) as num_records,
	min(REC_NUMBER) as min_rec_number,
	max(rec_number) as max_rec_number
FROM ordered_values
GROUP BY 
	group_field_1,
	group_field_2
;

###### Construct table 'group_percentile_rows', listing row number for 
######     summary group-percentile combination.

DROP TABLE IF EXISTS group_percentile_rows;
CREATE TEMPORARY TABLE group_percentile_rows
SELECT 
       grl.group_field_1,
       grl.group_field_2,
       prctl.percentile
FROM 
     group_row_limits grl
     INNER JOIN percentiles prctl
;

alter table group_percentile_rows
add num_records int,
add percentile_row_number int
;

UPDATE group_percentile_rows gpr, group_row_limits grl
SET percentile_row_number =
    (ceiling((grl.max_rec_number - grl.min_rec_number) * gpr.percentile)) + grl.min_rec_number,
    gpr.num_records = grl.num_records
WHERE 
      gpr.group_field_1 = grl.group_field_1
      AND gpr.group_field_2 = grl.group_field_2
;

# Get value of interest from the ordered list of values for the row number 
#    for each summary area-percentile combination

DROP TABLE IF EXISTS result_percentile_by_rows;
CREATE TEMPORARY TABLE result_percentile_by_rows
SELECT
	gpr.group_field_1,
	gpr.group_field_2,
	(gpr.percentile * 100) as percentile,
	round(opv.value,2) as value,
	gpr.num_records as number_of_records
FROM group_percentile_rows gpr 
        INNER JOIN ordered_values opv ON gpr.percentile_row_number = opv.rec_number
ORDER BY 
	gpr.group_field_1,
	gpr.group_field_2,
 	gpr.percentile
;

# Create final percentiles table by columns

CREATE TABLE result_percentiles_tabulated_table
SELECT 
       group_field_1 as group_field_1, 
       group_field_2 as group_field_2, 
       number_of_records,
       sum(IF(percentile=0, value, 0)) as "0_percentile",
       sum(IF(percentile=1, value, 0)) as "1_percentile",
       sum(IF(percentile=5, value, 0)) as "5_percentile",
       sum(IF(percentile=10, value, 0)) as "10_percentile",
       sum(IF(percentile=25, value, 0)) as "25_percentile",
       sum(IF(percentile=50, value, 0)) as "50_percentile",
       sum(IF(percentile=75, value, 0)) as "75_percentile",
       sum(IF(percentile=90, value, 0)) as "90_percentile",
       sum(IF(percentile=95, value, 0)) as "95_percentile",
       sum(IF(percentile=99, value, 0)) as "99_percentile",
       sum(IF(percentile=100, value, 0)) as "100_percentile"
FROM 
     result_percentile_by_rows
GROUP BY 
      group_field_1,
      group_field_2
;

# Delete temp tables
DROP TABLE preliminary_values;
DROP TABLE ordered_values;
DROP TABLE percentiles;
DROP TABLE group_percentile_rows;
DROP TABLE group_row_limits;
DROP TABLE result_percentile_by_rows;

rename table result_percentiles_tabulated_table to impv_dist_