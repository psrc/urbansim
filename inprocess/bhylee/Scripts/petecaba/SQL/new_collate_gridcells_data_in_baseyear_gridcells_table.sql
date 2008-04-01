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
#  Author: Liming Wang, modified by Chris Peak and Peter Caballero

###This script generate gridcell fields from parcels, parcel_fractions_in_gridcells, 
##and PSRC_2000_data_quality_indicators.land_use_generic_reclass table. Refer to wiki page:
##http://www.urbansim.org/projects/dataprep/tables/input_tables_parcel_to_grid.shtml
##Input: parcels,parcel_fractions_in_gridcells,PSRC_2000_data_quality_indicators.land_use_generic_reclass
##Output: new gridcells table from PSRC_parcels_all_counties.gridcells database
##        
##Run: in MySQL 


# New Gridcell collation process for PSRC_2000_baseyear generated from PSRC_parcels_all_counties.gridcells table

USE peters_playground;

SET SESSION big_tables = 1;

# create backup copy of gridcells table in case something goes wrong during script execution. 
DROP TABLE if exists gridcells_bak;
CREATE TABLE gridcells_bak select * from gridcells;

## Set gridcell fields to 0
UPDATE gridcells SET 
  COMMERCIAL_SQFT = 0,
  GOVERNMENTAL_SQFT = 0,
  INDUSTRIAL_SQFT = 0,
  COMMERCIAL_IMPROVEMENT_VALUE = 0,
  INDUSTRIAL_IMPROVEMENT_VALUE = 0,
  GOVERNMENTAL_IMPROVEMENT_VALUE = 0,
  NONRESIDENTIAL_LAND_VALUE = 0,
  RESIDENTIAL_LAND_VALUE = 0,
  RESIDENTIAL_IMPROVEMENT_VALUE = 0,
  RESIDENTIAL_UNITS = 0,
  YEAR_BUILT = 0,
  FRACTION_RESIDENTIAL_LAND = 0,
  PERCENT_UNDEVELOPABLE = 0,
  TOTAL_NONRES_SQFT = 0,
  TOTAL_UNDEVELOPABLE_SQFT = 0;
  
 CREATE TEMPORARY TABLE tmp_gridcells
 SELECT 
	A.GRID_ID,
	IFNULL(A.COMMERCIAL_SQFT,0) + IFNULL(B.COMMERCIAL_SQFT,0) AS COMMERCIAL_SQFT,
	IFNULL(A.GOVERNMENTAL_SQFT,0) + IFNULL(B.GOVERNMENTAL_SQFT,0) AS GOVERNMENTAL_SQFT,
	IFNULL(A.INDUSTRIAL_SQFT,0) + IFNULL(B.INDUSTRIAL_SQFT,0) AS INDUSTRIAL_SQFT,
	IFNULL(A.COMMERCIAL_IMPROVEMENT_VALUE,0) + IFNULL(B.COMMERCIAL_IMPROVEMENT_VALUE,0) AS COMMERCIAL_IMPROVEMENT_VALUE,
	IFNULL(A.INDUSTRIAL_IMPROVEMENT_VALUE,0) + IFNULL(B.INDUSTRIAL_IMPROVEMENT_VALUE,0) AS INDUSTRIAL_IMPROVEMENT_VALUE,
	IFNULL(A.GOVERNMENTAL_IMPROVEMENT_VALUE,0) + IFNULL(B.GOVERNMENTAL_IMPROVEMENT_VALUE,0) AS GOVERNMENTAL_IMPROVEMENT_VALUE,
	IFNULL(A.NONRESIDENTIAL_LAND_VALUE,0) + IFNULL(B.NONRESIDENTIAL_LAND_VALUE,0) AS NONRESIDENTIAL_LAND_VALUE,
	IFNULL(A.RESIDENTIAL_LAND_VALUE,0) + IFNULL(B.RESIDENTIAL_LAND_VALUE,0) AS RESIDENTIAL_LAND_VALUE,
	IFNULL(A.RESIDENTIAL_IMPROVEMENT_VALUE,0) + IFNULL(B.RESIDENTIAL_IMPROVEMENT_VALUE,0) AS RESIDENTIAL_IMPROVEMENT_VALUE,
	IFNULL(A.RESIDENTIAL_UNITS,0) + IFNULL(B.RESIDENTIAL_UNITS,0) AS RESIDENTIAL_UNITS,
	A.YEAR_BUILT,
	(IFNULL(A.FRACTION_RESIDENTIAL_LAND,0) + IFNULL(B.FRACTION_RESIDENTIAL_LAND,0)) AS FRACTION_RESIDENTIAL_LAND,
	0 AS PERCENT_UNDEVELOPABLE,
	IFNULL(A.TOTAL_NONRES_SQFT,0) + IFNULL(B.TOTAL_NONRES_SQFT,0) AS TOTAL_NONRES_SQFT,
	IFNULL(A.TOTAL_UNDEVELOPABLE_SQFT,0) + IFNULL(B.TOTAL_UNDEVELOPABLE_SQFT,0) AS TOTAL_UNDEVELOPABLE_SQFT,
	0 AS DEVELOPMENT_TYPE_ID,
	A.DISTANCE_TO_ARTERIAL,
	A.DISTANCE_TO_HIGHWAY,
	A.RELATIVE_X,
	A.RELATIVE_Y,
	A.PLAN_TYPE_ID,
	A.PERCENT_WATER,                       
	A.PERCENT_WETLAND,                     
	A.PERCENT_STREAM_BUFFER,               
	A.PERCENT_FLOODPLAIN,                  
	A.PERCENT_SLOPE,                       
	A.PERCENT_OPEN_SPACE,                  
	A.PERCENT_PUBLIC_SPACE,                
	A.PERCENT_ROADS,                       
	A.IS_OUTSIDE_URBAN_GROWTH_BOUNDARY,    
	A.IS_INSIDE_NATIONAL_FOREST,           
	A.IS_INSIDE_TRIBAL_LAND,               
	A.IS_INSIDE_MILITARY_BASE,             
	A.ZONE_ID,                             
	A.CITY_ID,                             
	A.COUNTY_ID,            
	A.PERCENT_AGRICULTURAL_PROTECTED_LANDS,
	A.ACRES
FROM 
	gridcells A
	LEFT JOIN peters_playhouse.gridcells B ON A.GRID_ID = B.GRID_ID
;

UPDATE gridcells SET total_nonres_sqft = round(total_nonres_sqft);

DROP TABLE gridcells;
CREATE TABLE gridcells SELECT * FROM tmp_gridcells;
DROP TABLE tmp_gridcells;
