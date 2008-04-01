###This script generate gridcell fields from parcels, parcel_fractions_in_gridcells, 
##and land_use_generic_reclass table. Refer to wiki page:
##http://trondheim.cs.washington.edu/cgi-bin/BaseQuicki/wiki.cgi?GridCellGeneration
##Input: parcels,parcel_fractions_in_gridcells,land_use_generic_reclass
##Output: gridcells table fields - GRID_ID, COMMERCIAL_SQFT, GOVERNMENTAL_SQFT, INDUSTRIAL_SQFT,
##        RESIDENTIAL_UNITS,LAND_VALUE,IMPROVEMENT_VALUE,YEAR_BUILT
##Run: in MySQL 

#create gridcells table if not existing.

create table if not exists gridcells (
GRID_ID int(11) primary key,
CITY_ID int(11),
COUNTY_ID int(11),
DEVELOPMENT_TYPE_ID int(11),
PLAN_TYPE_ID int(11),
ZONE_ID int(11),
COMMERCIAL_SQFT int(11),
GOVERNMENTAL_SQFT int(11),
INDUSTRIAL_SQFT int(11),
COMMERCIAL_IMPROVEMENT_VALUE int(11),
GOVERNMENTAL_IMPROVEMENT_VALUE int(11),
INDUSTRIAL_IMPROVEMENT_VALUE int(11),
NONRESIDENTIAL_LAND_VALUE int(11),
RESIDENTIAL_IMPROVEMENT_VALUE int(11),
RESIDENTIAL_LAND_VALUE int(11),
RESIDENTIAL_UNITS int(11),
YEAR_BUILT int(11),
DISTANCE_TO_ARTERIAL int(11),
DISTANCE_TO_HIGHWAY int(11),
RELATIVE_X int(11),
RELATIVE_Y int(11),
PERCENT_WATER int(11),
PERCENT_STREAM_BUFFER int(11),
PERCENT_FLOODPLAIN int(11),
PERCENT_WETLAND int(11),
PERCENT_SLOPE int(11),
PERCENT_OPEN_SPACE int(11),
PERCENT_PUBLIC_SPACE int(11),
PERCENT_ROADS int(11),
IS_OUTSIDE_URBAN_GROWTH_BOUNDARY smallint(6),
FRACTION_RESIDENTIAL_LAND double
)

##insert GRID_ID from parcel_fractions_in_gridcells table.
insert into table gridcells
select DISTINCT GRID_ID 
from parcel_fractions_in_gridcells;

#UPDATE COMMERCIAL SQFT
CREATE temporary table tmp_table1
SELECT b.GRID_ID AS GRID_ID, sum(a.BUILT_SQFT * b.PARCEL_FRACTION) as COMMERCIAL_SQFT
FROM (parcels a right join parcel_fractions_in_gridcells b on a.PARCEL_ID = b. PARCEL_ID ) 
  inner join land_use_generic_reclass2 c on a.COUNTY = c.COUNTY and a.LAND_USE = c.COUNTY_LAND_USE_CODE
WHERE c.GENERIC_RECLASS_2 = 'COMMERCIAL'
GROUP BY b.GRID_ID;

update gridcells, tmp_table1
set gridcells.COMMERCIAL_SQFT = tmp_table1.COMMERCIAL_SQFT
WHERE gridcells.GRID_ID = tmp_table1.GRID_ID;

#UPDATE GOVERNMENTAL SQFT
CREATE temporary table tmp_table2
SELECT b.GRID_ID AS GRID_ID, sum(a.BUILT_SQFT * b.PARCEL_FRACTION) as GOVERNMENTAL_SQFT
FROM (parcels a inner join parcel_fractions_in_gridcells b on a.PARCEL_ID = b. PARCEL_ID ) 
  inner join land_use_generic_reclass c on a.COUNTY = c.COUNTY and a.LAND_USE = c.COUNTY_LAND_USE_CODE
WHERE c.GENERIC_RECLASS_2 = 'GOVERNMENTAL'
GROUP BY b.GRID_ID;

update gridcells, tmp_table2
set gridcells.GOVERNMENTAL_SQFT = tmp_table2.GOVERNMENTAL_SQFT
WHERE gridcells.GRID_ID = tmp_table2.GRID_ID;

#UPDATE INDUSTRIAL SQFT
CREATE temporary table tmp_table3
SELECT b.GRID_ID AS GRID_ID, sum(a.BUILT_SQFT * b.PARCEL_FRACTION) as INDUSTRIAL_SQFT
FROM (parcels a inner join parcel_fractions_in_gridcells b on a.PARCEL_ID = b. PARCEL_ID ) 
  inner join land_use_generic_reclass c on a.COUNTY = c.COUNTY and a.LAND_USE = c.COUNTY_LAND_USE_CODE
WHERE c.GENERIC_RECLASS_2 = 'INDUSTRIAL'
GROUP BY b.GRID_ID;

update gridcells, tmp_table3
set gridcells.INDUSTRIAL_SQFT = tmp_table3.INDUSTRIAL_SQFT
WHERE gridcells.GRID_ID = tmp_table3.GRID_ID;

#UPDATE RESIDENTIAL_UNITS
CREATE temporary table tmp_table4
SELECT b.GRID_ID AS GRID_ID, round(sum(RESIDENTIAL_UNITS_IMPUTED * b.PARCEL_FRACTION)) as RESIDENTIAL_UNITS
FROM parcels a inner join parcel_fractions_in_gridcells b on a.PARCEL_ID = b. PARCEL_ID
GROUP BY b.GRID_ID;

update gridcells, tmp_table4
set gridcells.RESIDENTIAL_UNITS = tmp_table4.RESIDENTIAL_UNITS
WHERE gridcells.GRID_ID = tmp_table4.GRID_ID;

#UPDATE LAND_VALUE
CREATE temporary table tmp_table5
SELECT b.GRID_ID AS GRID_ID, sum(LAND_VALUE* b.PARCEL_FRACTION) as LAND_VALUE
FROM parcels a inner join parcel_fractions_in_gridcells b on a.PARCEL_ID = b. PARCEL_ID
GROUP BY b.GRID_ID;

update gridcells, tmp_table5
set gridcells.LAND_VALUE = tmp_table5.LAND_VALUE
WHERE gridcells.GRID_ID = tmp_table5.GRID_ID;

#UPDATE IMPROVEMENT_VALUE
CREATE temporary table tmp_table6
SELECT b.GRID_ID AS GRID_ID, sum(IMPROVEMENT_VALUE* b.PARCEL_FRACTION) as IMPROVEMENT_VALUE
FROM parcels a inner join parcel_fractions_in_gridcells b on a.PARCEL_ID = b. PARCEL_ID
GROUP BY b.GRID_ID;

update gridcells, tmp_table6
set gridcells.IMPROVEMENT_VALUE = tmp_table6.IMPROVEMENT_VALUE
WHERE gridcells.GRID_ID = tmp_table6.GRID_ID;

#UPDATE YEAR_BUILT
CREATE table tmp_table7
SELECT b.GRID_ID AS GRID_ID, a.YEAR_BUILT AS YEAR_BUILT
FROM parcels a inner join parcel_fractions_in_gridcells b on a.PARCEL_ID = b. PARCEL_ID;

CREATE table tmp_table8
SELECT a.GRID_ID AS GRID_ID, a.YEAR_BUILT AS YEAR_BUILT
FROM tmp_table7 a inner join tmp_table7 b on a.GRID_ID = b.GRID_ID
GROUP BY a.GRID_ID, a.YEAR_BUILT
HAVING SUM(SIGN(1-SIGN(b.YEAR_BUILT-a.YEAR_BUILT))) = FLOOR((COUNT(*)+1)/2);

update gridcells, tmp_table8
set gridcells.YEAR_BUILT = tmp_table8.YEAR_BUILT
WHERE gridcells.GRID_ID = tmp_table8.GRID_ID;

DROP TABLE tmp_table1;
DROP TABLE tmp_table2;
DROP TABLE tmp_table3;
DROP TABLE tmp_table4;
DROP TABLE tmp_table5;
DROP TABLE tmp_table6;
DROP TABLE tmp_table7;
DROP TABLE tmp_table8;
