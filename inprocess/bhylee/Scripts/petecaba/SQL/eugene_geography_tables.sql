#
#  UrbanSim software.
#  Copyright (C) 1998-2003 University of Washington
#  
#  You can redistribute this program and/or modify it under the
#  terms of the GNU General Public License as published by the
#  Free Software Foundation (http://www.gnu.org/copyleft/gpl.html).
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  file LICENSE.htm for copyright and licensing information, and the
#  file ACKNOWLEDGMENTS.htm for funding and other acknowledgments.
#
#  Author: Peter Caballero

# This script creates the geographies, gridcells_in_geography, and geography_names tables 
# The input tables required are outputs from GIS (identity operations) from gridcell coverage
#  and polygon geographies (i.e. TAZ, FAZ, etc.) or other reclassification tables that associate 
#  GRID_ID to POLYGON_UNIQUE_ID.



###########################################
##					 ##
## create geographies table and populate ##
##					 ##
###########################################

## Eugene Baseyear geography tables ##

use Eugene_baseyear;

CREATE TABLE geographies 
	(GEOGRAPHY_TYPE_ID INT, 
	 GEOGRAPHY_TYPE_TITLE TEXT, 
	 SHAPEFILE_PATH TEXT, 
	 COLUMN_NAME TEXT, 
	 POLYGON_ID_VALID_MIN INT,
	 POLYGON_ID_VALID_MAX INT,
	 SHAPEFILE_JOIN_COLUMN TEXT); 

# Insert REGION (1)	 
INSERT INTO geographies 
	(GEOGRAPHY_TYPE_ID, 
	 GEOGRAPHY_TYPE_TITLE, 
	 SHAPEFILE_PATH, 
	 COLUMN_NAME, 
	 POLYGON_ID_VALID_MIN, 
	 POLYGON_ID_VALID_MAX, 
	 SHAPEFILE_JOIN_COLUMN) 
 VALUES (1, 'region', 'null', 'REGION_ID', '1', '1', 'REGION_ID'); 
 
# Insert GRID (2)
INSERT INTO geographies 
	(GEOGRAPHY_TYPE_ID, 
	 GEOGRAPHY_TYPE_TITLE, 
	 SHAPEFILE_PATH, 
	 COLUMN_NAME, 
	 POLYGON_ID_VALID_MIN, 
	 POLYGON_ID_VALID_MAX, 
	 SHAPEFILE_JOIN_COLUMN) 
 VALUES (2, 'grid', 'null', 'GRID_ID', 1, 15518, 'GRID_ID');  

# Insert ZONE (3)
INSERT INTO geographies 
	(GEOGRAPHY_TYPE_ID, 
	 GEOGRAPHY_TYPE_TITLE, 
	 SHAPEFILE_PATH, 
	 COLUMN_NAME, 
	 POLYGON_ID_VALID_MIN, 
	 POLYGON_ID_VALID_MAX, 
	 SHAPEFILE_JOIN_COLUMN) 
 VALUES (3, 'zone', 'null', 'ZONE_ID', 25, 295, 'ZONE_ID');
 
# Insert CITY (4)
INSERT INTO geographies 
	(GEOGRAPHY_TYPE_ID, 
	 GEOGRAPHY_TYPE_TITLE, 
	 SHAPEFILE_PATH, 
	 COLUMN_NAME, 
	 POLYGON_ID_VALID_MIN, 
	 POLYGON_ID_VALID_MAX, 
	 SHAPEFILE_JOIN_COLUMN) 
 VALUES (4, 'city', 'null', 'CITY_ID', 1, 3, 'CITY_ID');
 
# Insert UGB (5)
INSERT INTO geographies 
	(GEOGRAPHY_TYPE_ID, 
	 GEOGRAPHY_TYPE_TITLE, 
	 SHAPEFILE_PATH, 
	 COLUMN_NAME, 
	 POLYGON_ID_VALID_MIN, 
	 POLYGON_ID_VALID_MAX, 
	 SHAPEFILE_JOIN_COLUMN) 
 VALUES (5, 'ugb', 'null', '', 0, 1, 'IS_IN_UGB');
 
# Update SHAPEFILE_PATH field fro GEOGRAPHY_TYPE_IDs
#UPDATE geographies SET SHAPEFILE_PATH = '/test-resource/jump-files/.shp' WHERE GEOGRAPHY_TYPE_ID = 1;
UPDATE geographies SET SHAPEFILE_PATH = '/test-resource/jump-files/id150_dd.shp' WHERE GEOGRAPHY_TYPE_ID = 2;
UPDATE geographies SET SHAPEFILE_PATH = '/test-resource/jump-files/zone_dd.shp' WHERE GEOGRAPHY_TYPE_ID = 3;
UPDATE geographies SET SHAPEFILE_PATH = '/projects/urbansim2/GIS/Eugene/Shape/eug_spring_city.shp' WHERE GEOGRAPHY_TYPE_ID = 4;
UPDATE geographies SET SHAPEFILE_PATH = '/projects/urbansim2/GIS/Eugene/Shape/metugb.shp' WHERE GEOGRAPHY_TYPE_ID = 5;


#####################################################################
##								   ##	
## create gridcells_in_geographies and populate table              ##
##								   ##
#####################################################################

CREATE TABLE gridcells_in_geography (GRID_ID int, GEOGRAPHY_TYPE_ID int, GEOGRAPHY_ID int);

# Insert GRID_ID and REGION ID
INSERT INTO gridcells_in_geography (GRID_ID, GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID) 
 SELECT GRID_ID, 1, 1 FROM Eugene_baseyear.gridcells;
 
# Insert GRID_ID and GRID 
INSERT INTO gridcells_in_geography (GRID_ID, GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID) 
 SELECT GRID_ID, 2, GRID_ID FROM Eugene_baseyear.gridcells; 
 
# Insert GRID_ID and ZONE (TAZ)
INSERT INTO gridcells_in_geography (GRID_ID, GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID) 
 SELECT GRID_ID, 3, ZONE_ID FROM Eugene_baseyear.gridcells; 

# Insert GRID_ID and CITY
INSERT INTO gridcells_in_geography (GRID_ID, GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID) 
 SELECT GRID_ID, 4, CITY_ID FROM Eugene_baseyear.gridcells; 
 
# Insert GRID_ID and UGB
INSERT INTO gridcells_in_geography (GRID_ID, GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID)
 SELECT GRID_ID, 5, IS_OUTSIDE_URBAN_GROWTH_BOUNDARY FROM Eugene_baseyear.gridcells; 
 
###############################################
##    					     ##	 
## create geography_names table and populate ## 
##					     ##
###############################################

CREATE TABLE geography_names (GEOGRAPHY_TYPE_ID INT, GEOGRAPHY_ID INT, NAME VARCHAR(100));

# Insert REGION values into geography_names table
INSERT INTO geography_names (GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID, NAME) 
 VALUES (1, 1, 'region')
;

# Insert GRID values into geography_names table
INSERT INTO geography_names (GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID, NAME)
 SELECT 2 AS GEOGRAPHY_TYPE_ID, GRID_ID AS GEOGRAPHY_ID, 'grid' AS NAME
 FROM Eugene_baseyear.gridcells
;

# Insert ZONE values into geography_names table
DROP TABLE IF EXISTS tmp_taz_id;
CREATE TEMPORARY TABLE tmp_taz_id SELECT DISTINCT ZONE_ID FROM Eugene_baseyear.gridcells;

INSERT INTO geography_names (GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID, NAME)
 SELECT 3 AS GEOGRAPHY_TYPE_ID, ZONE_ID AS GEOGRAPHY_ID, 'zone' AS NAME
 FROM tmp_taz_id
;

DROP TABLE tmp_taz_id;

# Insert CITY values into geography_names table
INSERT INTO geography_names (GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID, NAME)
 VALUES (4, 1, 'Eugene'),
 	(4, 2, 'Springfield'),
 	(4, 3, 'Unknown')
; 

# Insert UGB values into geography_names table
DROP TABLE IF EXISTS tmp_ugb;
CREATE TEMPORARY TABLE tmp_ugb SELECT a.GRID_ID, a.IS_OUTSIDE_URBAN_GROWTH_BOUNDARY FROM Eugene_baseyear.gridcells AS a
 WHERE a.IS_OUTSIDE_URBAN_GROWTH_BOUNDARY = 0; 
UPDATE tmp_ugb SET IS_OUTSIDE_URBAN_GROWTH_BOUNDARY = 1;

INSERT INTO geography_names (GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID, NAME)
 SELECT 5 AS GEOGRAPHY_TYPE_ID, IS_OUTSIDE_URBAN_GROWTH_BOUNDARY, 'ugb'
 FROM tmp_ugb
;

DROP TABLE tmp_ugb;