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

# Author: Peter Caballero

# This script sets up the PSRC_2000_scenario_B_dense_centers scenario database


USE PSRC_2000_scenario_B_dense_centers;


# Create new plan_types table which contains duplicate values
DROP TABLE IF EXISTS plan_types;
CREATE TABLE plan_types SELECT * FROM GSPSRC_2000_baseyear_flattened.plan_types;


# Insert into plan_types table the 'in_urban_centers' plu codes
INSERT INTO plan_types (plan_type_id, name) VALUES 
 (12, 'agriculture_centers'),
 (13, 'commercial_centers'),
 (14, 'forests_centers'),
 (15, 'industrial_centers'),
 (16, 'mixed_use_including_residential_centers'),
 (17, 'parks_and_open_space'),
 (18, 'residential_centers'),
 (19, 'right_of_way_centers'),
 (20, 'resource_extraction_centers'),
 (21, 'tribal_government_military_centers'),
 (22, 'water_centers')
;


# Create new land_price_model_coefficients table which duplicates the currenct plu codes' coefficients
#  so that the new 'in urban centers' plu codes use the same coefficients as their matching ones.
DROP TABLE IF EXISTS land_price_model_specification;
DROP TABLE IF EXISTS land_price_model_coefficients;

CREATE TABLE land_price_model_coefficients SELECT * FROM GSPSRC_2000_baseyear_flattened.land_price_model_coefficients;
CREATE TABLE land_price_model_specification SELECT * FROM GSPSRC_2000_baseyear_flattened.land_price_model_specification;


# Insert into new land_price_model_specification and land_price_model_coefficients table the new 
#  'in_urban_centers' plu code specification and coefficients values

# Create and insert new specification values for duplicate plu codes
INSERT INTO land_price_model_specification (sub_model_id, equation_id, variable_name, coefficient_name)
 VALUES 
 (-2, -2, 'plantype_13', 'PT0013'),
 (-2, -2, 'plantype_14', 'PT0014'),
 (-2, -2, 'plantype_15', 'PT0015'),
 (-2, -2, 'plantype_16', 'PT0016'),
 (-2, -2, 'plantype_17', 'PT0017'),
 (-2, -2, 'plantype_18', 'PT0018'),
 (-2, -2, 'plantype_20', 'PT0020')
;

# Create and insert new coefficient values for duplicate plu codes
INSERT INTO land_price_model_coefficients 
 (SUB_MODEL_ID, COEFFICIENT_NAME, ESTIMATE, STANDARD_ERROR, T_STATISTIC, P_VALUE)
 VALUES
 (-2, 'PT0013', 0.7872874905, 0.03098779, 25.406, 0),
 (-2, 'PT0014', -2.031942449, 0.020589837, -98.687, 0),
 (-2, 'PT0015', 0.8742959769, 0.024026097, 36.389, 0),
 (-2, 'PT0016', 0.4919979983, 0.02689215, 18.295, 0),
 (-2, 'PT0017', -0.1808344793, 0.028159888, -6.422, 0),
 (-2, 'PT0018', 0.113500513, 0.014946694, 7.594, 0),
 (-2, 'PT0020', -0.6141998324, 0.057488574, -10.684, 0)
; 


############################################################################################################################
## This section of the script is to have been partially completed using GIS and the exported tables should have been created

ALTER TABLE ucntr_cells_point change column grid_code GRID_ID int;
ALTER TABLE ucntr_cells_point ADD INDEX grid_id_index(GRID_ID);


CREATE TABLE gridcells SELECT * FROM GSPSRC_2000_baseyear_flattened.gridcells;
ALTER TABLE gridcells ADD INDEX grid_id_index(grid_id);

# Ag Centers
UPDATE gridcells a 
 INNER JOIN ucntr_cells_point b ON a.grid_id = b.grid_id
 SET a.PLAN_TYPE_ID = 12
 WHERE a.PLAN_TYPE_ID = 1
;
# Com Centers
UPDATE gridcells a 
 INNER JOIN ucntr_cells_point b ON a.grid_id = b.grid_id
 SET a.PLAN_TYPE_ID = 13
 WHERE a.PLAN_TYPE_ID = 2
;
# Ind Centers
UPDATE gridcells a 
 INNER JOIN ucntr_cells_point b ON a.grid_id = b.grid_id
 SET a.PLAN_TYPE_ID = 15
 WHERE a.PLAN_TYPE_ID = 4
;
# Mixed-Use Centers
UPDATE gridcells a 
 INNER JOIN ucntr_cells_point b ON a.grid_id = b.grid_id
 SET a.PLAN_TYPE_ID = 14
 WHERE a.PLAN_TYPE_ID = 5
;
# Park and Open Space Centers
UPDATE gridcells a 
 INNER JOIN ucntr_cells_point b ON a.grid_id = b.grid_id
 SET a.PLAN_TYPE_ID = 17
 WHERE a.PLAN_TYPE_ID = 6
;
# Residential Centers
UPDATE gridcells a 
 INNER JOIN ucntr_cells_point b ON a.grid_id = b.grid_id
 SET a.PLAN_TYPE_ID = 18
 WHERE a.PLAN_TYPE_ID = 7
;
# Right-of-Way Centers
UPDATE gridcells a 
 INNER JOIN ucntr_cells_point b ON a.grid_id = b.grid_id
 SET a.PLAN_TYPE_ID = 19
 WHERE a.PLAN_TYPE_ID = 8
;
# Tribal-Gov-Military Centers
UPDATE gridcells a 
 INNER JOIN ucntr_cells_point b ON a.grid_id = b.grid_id
 SET a.PLAN_TYPE_ID = 21
 WHERE a.PLAN_TYPE_ID = 10
;
# Water Centers
UPDATE gridcells a 
 INNER JOIN ucntr_cells_point b ON a.grid_id = b.grid_id
 SET a.PLAN_TYPE_ID = 22
 WHERE a.PLAN_TYPE_ID = 11
;

                     
## Update manufacturing and industrial centers
ALTER TABLE manu_cells_point CHANGE COLUMN GRID_CODE GRID_ID INT;
ALTER TABLE manu_cells_point ADD INDEX grid_id_index(GRID_ID);

UPDATE gridcells a 
 INNER JOIN manu_cells_point b ON a.grid_id = b.grid_id
 SET a.PLAN_TYPE_ID = 15
; 
 
 


