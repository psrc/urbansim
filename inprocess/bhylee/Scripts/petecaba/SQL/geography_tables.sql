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

CREATE TABLE geographies
	(GEOGRAPHY_TYPE_ID INT, 
	 GEOGRAPHY_TYPE_TITLE TEXT, 
	 SHAPEFILE_PATH TEXT, 
	 COLUMN_NAME TEXT, 
	 POLYGON_ID_VALID_MIN INT,
	 POLYGON_ID_VALID_MAX INT,
	 SHAPEFILE_JOIN_COLUMN TEXT); 

# Insert REGION (1)
INSERT INTO geographies (GEOGRAPHY_TYPE_ID, GEOGRAPHY_TYPE_TITLE, SHAPEFILE_PATH, COLUMN_NAME, POLYGON_ID_VALID_MIN, POLYGON_ID_VALID_MAX, SHAPEFILE_JOIN_COLUMN) 
 VALUES (1, 'region', 'null', 'REGION_ID', 1, 1, 'REGION_ID');
 
# Insert GRID (2)
INSERT INTO geographies (GEOGRAPHY_TYPE_ID, GEOGRAPHY_TYPE_TITLE, SHAPEFILE_PATH, COLUMN_NAME, POLYGON_ID_VALID_MIN, POLYGON_ID_VALID_MAX, SHAPEFILE_JOIN_COLUMN)
 VALUES (2, 'grid', 'null', 'GRID_ID', 229478, 1284518, 'GRID_ID');
 
# Insert ZONE (3)
INSERT INTO geographies (GEOGRAPHY_TYPE_ID, GEOGRAPHY_TYPE_TITLE, SHAPEFILE_PATH, COLUMN_NAME, POLYGON_ID_VALID_MIN, POLYGON_ID_VALID_MAX, SHAPEFILE_JOIN_COLUMN)
 VALUES (3, 'zone', 'null', 'TAZ', 1, 938, 'TAZ');
 
# Insert FAZ ((4) District)
INSERT INTO geographies (GEOGRAPHY_TYPE_ID, GEOGRAPHY_TYPE_TITLE, SHAPEFILE_PATH, COLUMN_NAME, POLYGON_ID_VALID_MIN, POLYGON_ID_VALID_MAX, SHAPEFILE_JOIN_COLUMN)
 VALUES (4, 'faz', 'null', 'FAZ', 110, 9916, 'FAZ');

# Insert COUNTY (5)
INSERT INTO geographies (GEOGRAPHY_TYPE_ID, GEOGRAPHY_TYPE_TITLE, SHAPEFILE_PATH, COLUMN_NAME, POLYGON_ID_VALID_MIN, POLYGON_ID_VALID_MAX, SHAPEFILE_JOIN_COLUMN)
 VALUES (5, 'county', 'null', 'COUNTY_ID', 33, 61, 'COUNTY_ID');
 
# Insert UGB (6)
INSERT INTO geographies (GEOGRAPHY_TYPE_ID, GEOGRAPHY_TYPE_TITLE, SHAPEFILE_PATH, COLUMN_NAME, POLYGON_ID_VALID_MIN, POLYGON_ID_VALID_MAX, SHAPEFILE_JOIN_COLUMN)
 VALUES (6, 'ugb', 'null', 'IS_IN_UGB', 0, 1, 'IS_IN_UGB');

# Update SHAPEFILE_PATH field for GEOGRAPHY_TYPE_IDs
UPDATE geographies SET SHAPEFILE_PATH = '/projects/urbansim7/GIS_Data/PSRC/Geographies/region.shp' WHERE GEOGRAPHY_TYPE_ID = 1;
UPDATE geographies SET SHAPEFILE_PATH = '/projects/urbansim7/GIS_Data/PSRC/Geographies/id150_4cnty.shp' WHERE GEOGRAPHY_TYPE_ID = 2;
UPDATE geographies SET SHAPEFILE_PATH = '/projects/urbansim7/GIS_Data/PSRC/Geographies/taz.shp' WHERE GEOGRAPHY_TYPE_ID = 3;
UPDATE geographies SET SHAPEFILE_PATH = '/projects/urbansim7/GIS_Data/PSRC/Geographies/faz.shp' WHERE GEOGRAPHY_TYPE_ID = 4;
UPDATE geographies SET SHAPEFILE_PATH = '/projects/urbansim7/GIS_Data/PSRC/Geographies/cnty_outline.shp' WHERE GEOGRAPHY_TYPE_ID = 5;
UPDATE geographies SET SHAPEFILE_PATH = '/projects/urbansim7/GIS_Data/PSRC/Geographies/ugb.shp' WHERE GEOGRAPHY_TYPE_ID = 6;
  
#####################################################################
##								   ##	
## create gridcells_in_geographies and populate table              ##
##								   ##
#####################################################################

CREATE TABLE gridcells_in_geography (GRID_ID int, GEOGRAPHY_TYPE_ID int, GEOGRAPHY_ID int);

# Insert GRID_ID and REGION ID
INSERT INTO gridcells_in_geography (GRID_ID, GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID) 
 SELECT GRID_ID, 1, 1 FROM PSRC_2000_baseyear.gridcells;

# Insert GRID_ID and GRID 
INSERT INTO gridcells_in_geography (GRID_ID, GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID) 
 SELECT GRID_ID, 2, GRID_ID FROM PSRC_2000_baseyear.gridcells;

# Insert GRID_ID and ZONE (TAZ)
INSERT INTO gridcells_in_geography (GRID_ID, GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID) 
 SELECT GRID_ID, 3, ZONE_ID FROM PSRC_2000_baseyear.gridcells;

# Insert GRID_ID and FAZ
DROP TABLE IF EXISTS tmp_grid_to_faz;
CREATE TEMPORARY TABLE tmp_grid_to_faz SELECT GRID_ID, FAZ FROM PSRC_2000_reclassification_tables.gridcell_faz_fazdistrict;
DELETE FROM tmp_grid_to_faz WHERE GRID_ID = -9999;

INSERT INTO gridcells_in_geography (GRID_ID, GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID) 
 SELECT GRID_ID, 4, FAZ FROM PSRC_2000_baseyear_petecaba.tmp_grid_to_faz;

DROP TABLE tmp_grid_to_faz;
 
# Insert GRID_ID and COUNTY
INSERT INTO gridcells_in_geography (GRID_ID, GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID) 
 SELECT GRID_ID, 5, COUNTY_ID FROM PSRC_2000_baseyear.gridcells;
 
# Insert GRID_ID and UGB
INSERT INTO gridcells_in_geography (GRID_ID, GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID)
 SELECT GRID_ID, 6, IS_OUTSIDE_URBAN_GROWTH_BOUNDARY FROM PSRC_2000_baseyear.gridcells;

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
 FROM PSRC_2000_baseyear.gridcells
;

# Insert ZONE values into geography_names table
DROP TABLE IF EXISTS tmp_taz_id;
CREATE TEMPORARY TABLE tmp_taz_id SELECT DISTINCT ZONE_ID FROM PSRC_2000_baseyear.gridcells;

INSERT INTO geography_names (GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID, NAME)
 SELECT 3 AS GEOGRAPHY_TYPE_ID, ZONE_ID AS GEOGRAPHY_ID, 'zone' as NAME
 FROM tmp_taz_id
;

DROP TABLE tmp_taz_id;

# Insert FAZ values into geography_names table
DROP TABLE IF EXISTS tmp_distinct_faz;
CREATE TEMPORARY TABLE tmp_distinct_faz SELECT DISTINCT FAZ FROM PSRC_2000_reclassification_tables.gridcell_faz_fazdistrict;
DELETE FROM tmp_distinct_faz WHERE FAZ = 0;

INSERT INTO geography_names (GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID, NAME)
 SELECT 4 AS GEOGRAPHY_TYPE_ID, FAZ AS GEOGRAPHY_ID, 'faz' AS NAME
 FROM tmp_distinct_faz
;

DROP TABLE tmp_distinct_faz;
 
# Insert COUNTY values into geography_names table
INSERT INTO geography_names (GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID, NAME)
 VALUES (5, 33, 'King'),
 	(5, 35, 'Kitsap'),
 	(5, 53, 'Pierce'),
 	(5, 61, 'Snohomish')
;	

# Insert UGB values into geography_names table
DROP TABLE IF EXISTS tmp_grid_to_ugb;
CREATE TEMPORARY TABLE tmp_grid_to_ugb SELECT a.GRID_ID, a.IS_OUTSIDE_URBAN_GROWTH_BOUNDARY FROM PSRC_2000_baseyear.gridcells AS a
 WHERE a.IS_OUTSIDE_URBAN_GROWTH_BOUNDARY = 0; 
UPDATE tmp_grid_to_ugb SET IS_OUTSIDE_URBAN_GROWTH_BOUNDARY = 1;

INSERT INTO geography_names (GEOGRAPHY_TYPE_ID, GEOGRAPHY_ID, NAME)
 SELECT 6 AS GEOGRAPHY_TYPE_ID, IS_OUTSIDE_URBAN_GROWTH_BOUNDARY, 'ugb'
 FROM tmp_grid_to_ugb
; 

DROP TABLE tmp_grid_to_ugb; 
 