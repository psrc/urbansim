/#
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
 #/
 
# Author: Peter Caballero
# Program: SQL Query
# Description: Assigns each grid cell a Development Type Id 1-25 according to certain attributes of the grid cell.

### June 17, 2003

### DEVELOPMENT_TYPE_ID QUERIES: 

# Add column to gridcells table "TOTAL_SQFT" DOUBLE.
# Calculate total square feet for each gridcell based on commercial, industrial, and governmental types.
# Perform query that determines DEVELOPMENT_TYPE_ID's for each gridcell.
# Set DEVELOPMENT_TYPE_ID = 25 for all gridcells containing a >= 50% environmental layers in each cell.
# Set DEVELOPMENT_TYPE_ID = 25 for all gridcells inside a military installation or national forest.
# Set DEVELOPMENT_TYPE_ID = 25 for all gridcells containing a >= 75% undevelopable parcel. 

ALTER TABLE gridcells ADD COLUMN TOTAL_SQFT double;
UPDATE gridcells_12_23_03_wfrc_devtype SET TOTAL_SQFT = (COMMERCIAL_SQFT + INDUSTRIAL_SQFT + GOVERNMENTAL_SQFT);
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 1 where TOTAL_SQFT >= 0 and TOTAL_SQFT <= 999 and RESIDENTIAL_UNITS = 1;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 2 where TOTAL_SQFT >= 0 and TOTAL_SQFT <= 999 and RESIDENTIAL_UNITS >= 2 and RESIDENTIAL_UNITS <= 4;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 3 where TOTAL_SQFT >= 0 and TOTAL_SQFT <= 999 and RESIDENTIAL_UNITS >= 5 and RESIDENTIAL_UNITS <= 9;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 4 where TOTAL_SQFT >= 0 and TOTAL_SQFT <= 2499 and RESIDENTIAL_UNITS >= 10 and RESIDENTIAL_UNITS <= 14;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 5 where TOTAL_SQFT >= 0 and TOTAL_SQFT <= 2499 and RESIDENTIAL_UNITS >= 15 and RESIDENTIAL_UNITS <= 21;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 6 where TOTAL_SQFT >= 0 and TOTAL_SQFT <= 2499 and RESIDENTIAL_UNITS >= 22 and RESIDENTIAL_UNITS <= 30;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 7 where TOTAL_SQFT >= 0 and TOTAL_SQFT <= 4999 and RESIDENTIAL_UNITS >= 31 and RESIDENTIAL_UNITS <= 75;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 8 where TOTAL_SQFT >= 0 and TOTAL_SQFT <= 4999 and RESIDENTIAL_UNITS >= 76 and RESIDENTIAL_UNITS <= 1000;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 9 where COMMERCIAL_SQFT >= 1000 and COMMERCIAL_SQFT <= 4999 and RESIDENTIAL_UNITS >= 1 and RESIDENTIAL_UNITS <= 9;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 10 where COMMERCIAL_SQFT >= 2500 and COMMERCIAL_SQFT <= 4999 and RESIDENTIAL_UNITS >= 10 and RESIDENTIAL_UNITS <= 30;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 11 where COMMERCIAL_SQFT >= 5000 and COMMERCIAL_SQFT <= 24999 and RESIDENTIAL_UNITS >= 10 and RESIDENTIAL_UNITS <= 30;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 12 where COMMERCIAL_SQFT >= 25000 and COMMERCIAL_SQFT <= 49999 and RESIDENTIAL_UNITS >= 10 and RESIDENTIAL_UNITS <= 30;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 13 where COMMERCIAL_SQFT >= 50000 and COMMERCIAL_SQFT <= 3000000 and RESIDENTIAL_UNITS >= 10 and RESIDENTIAL_UNITS <= 30;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 14 where COMMERCIAL_SQFT >= 5000 and COMMERCIAL_SQFT <= 24999 and RESIDENTIAL_UNITS >= 31 and RESIDENTIAL_UNITS <= 1000;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 15 where COMMERCIAL_SQFT >= 25000 and COMMERCIAL_SQFT <= 49999 and RESIDENTIAL_UNITS >= 31 and RESIDENTIAL_UNITS <= 1000;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 16 where COMMERCIAL_SQFT >= 50000 and COMMERCIAL_SQFT <= 3000000 and RESIDENTIAL_UNITS >= 31 and RESIDENTIAL_UNITS <= 1000;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 17 where COMMERCIAL_SQFT >= 5000 and COMMERCIAL_SQFT <= 24999 and RESIDENTIAL_UNITS >= 0 and RESIDENTIAL_UNITS <= 9;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 18 where COMMERCIAL_SQFT >= 25000 and COMMERCIAL_SQFT <= 49999 and RESIDENTIAL_UNITS >= 0 and RESIDENTIAL_UNITS <= 9;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 19 where COMMERCIAL_SQFT >= 50000 and COMMERCIAL_SQFT <= 3000000 and RESIDENTIAL_UNITS >= 0 and RESIDENTIAL_UNITS <= 9;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 20 where INDUSTRIAL_SQFT >= 5000 and INDUSTRIAL_SQFT <= 24999 and RESIDENTIAL_UNITS >= 0 and RESIDENTIAL_UNITS <= 9;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 21 where INDUSTRIAL_SQFT >= 25000 and INDUSTRIAL_SQFT <= 49999 and RESIDENTIAL_UNITS >= 0 and RESIDENTIAL_UNITS <= 9;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 22 where INDUSTRIAL_SQFT >= 50000 and INDUSTRIAL_SQFT <= 500000 and RESIDENTIAL_UNITS >= 0 and RESIDENTIAL_UNITS <= 9;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 23 where GOVERNMENTAL_SQFT >= 5000 and GOVERNMENTAL_SQFT <= 10000000 and RESIDENTIAL_UNITS >= 0 and RESIDENTIAL_UNITS <= 9;
UPDATE gridcells_12_23_03_wfrc_devtype SET DEVELOPMENT_TYPE_ID = 24 where TOTAL_SQFT = 0 and RESIDENTIAL_UNITS = 0;   



