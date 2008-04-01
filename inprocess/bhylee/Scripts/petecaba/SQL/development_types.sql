
 # UrbanSim software.
 # Copyright (C) 1998-2003 University of Washington
 #
 # You can redistribute this program and/or modify it under the
 # terms of the GNU General Public License as published by the
 # Free Software Foundation (http://www.gnu.org/copyleft/gpl.html).
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # file LICENSE.htm for copyright and licensing information, and the
 # file ACKNOWLEDGMENTS.htm for funding and other acknowledgments.
 #
 #
 
# Author: Peter Caballero and Chris Peak
# Program: SQL Query
# Description: Assigns each grid cell a Development Type Id 1-25 according to certain attributes of the grid cell.

### June 17, 2003

### DEVELOPMENT_TYPE_ID QUERIES: 

# Add column to gridcells table "TOTAL_SQFT" DOUBLE.
# Calculate total square feet for each gridcell based on commercial, industrial, and governmental types.
# Perform query that determines DEVELOPMENT_TYPE_IDs for each gridcell.
# Set DEVELOPMENT_TYPE_ID = 25 for all gridcells containing a >= 50% environmental layers in each cell.
# Set DEVELOPMENT_TYPE_ID = 25 for all gridcells inside a military installation or national forest.
# Set DEVELOPMENT_TYPE_ID = 25 for all gridcells containing a >= 75% undevelopable parcel. 

USE PSRC_2000_baseyear;

#ALTER TABLE gridcells ADD COLUMN TOTAL_NONRES_SQFT int;
CREATE INDEX TNS_RU_indx on gridcells (TOTAL_NONRES_SQFT, RESIDENTIAL_UNITS);

#UPDATE gridcells SET TOTAL_NONRES_SQFT = (COMMERCIAL_SQFT + INDUSTRIAL_SQFT + GOVERNMENTAL_SQFT);

UPDATE gridcells g, development_types dt
SET 	g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND dt.NAME IN ('R1','R2','R3','R4','R5','R6','R7','R8','M1','M2','M3','M4','M5','M6','M7','M8')
;

UPDATE gridcells g, development_types dt
SET 	g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND (g.COMMERCIAL_SQFT >= g.INDUSTRIAL_SQFT) 
	AND (g.COMMERCIAL_SQFT >= g.GOVERNMENTAL_SQFT)
	AND dt.NAME IN ('C1','C2','C3')
;

UPDATE gridcells g, development_types dt
SET 	g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND (g.INDUSTRIAL_SQFT > g.COMMERCIAL_SQFT) 
	AND (g.INDUSTRIAL_SQFT > g.GOVERNMENTAL_SQFT)
	AND dt.NAME IN ('I1','I2','I3')
;

UPDATE gridcells g, development_types dt
SET g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND (g.GOVERNMENTAL_SQFT > g.COMMERCIAL_SQFT) 
	AND (g.GOVERNMENTAL_SQFT >= g.INDUSTRIAL_SQFT)
	AND g.GOVERNMENTAL_SQFT > 0
	AND dt.NAME = 'GV'
;

UPDATE gridcells SET DEVELOPMENT_TYPE_ID = 24 where TOTAL_NONRES_SQFT = 0 and RESIDENTIAL_UNITS = 0;

UPDATE gridcells set DEVELOPMENT_TYPE_ID = 25 
WHERE (
	PERCENT_WATER >= 50
	OR PERCENT_OPEN_SPACE >= 50
	OR PERCENT_FLOODPLAIN >= 50
	OR PERCENT_WETLAND >= 50
	OR PERCENT_UNDEVELOPABLE >= 75
	) and (
	DEVELOPMENT_TYPE_ID NOT BETWEEN 1, 23
;

# Reclassified Development Types

 UPDATE gridcells SET DEVELOPMENT_TYPE_ID = 26 
 WHERE PERCENT_PUBLIC_LAND >= 50;

 UPDATE gridcells SET DEVELOPMENT_TYPE_ID = 27
 WHERE PERCENT_ROW >= 50;
 
 UPDATE gridcells SET DEVELOPMENT_TYPE_ID = 28
 WHERE PERCENT_MINING >= 50

 UPDATE gridcells SET DEVELOPMENT_TYPE_ID = 29
 WHERE PERCENT_FOREST >= 50;

 UPDATE gridcells SET DEVELOPMENT_TYPE_ID = 30
 WHERE PERCENT_AGRICULTURE >= 50;

#ALTER TABLE gridcells drop column TOTAL_NONRES_SQFT;


