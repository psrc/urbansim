set session tmp_table_size  = 16 * 1024 * 1024 * 1024;
set session max_heap_table_size = 1 * 1024 * 1024 * 1024;

#use PSRC_parcels_all_counties;
UPDATE deh_temp_gridcells_by_grid_id_year g, PSRC_2000_baseyear_reestimation.development_types dt
SET 	g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND dt.NAME IN ('R1','R2','R3','R4','R5','R6','R7','R8','M1','M2','M3','M4','M5','M6','M7','M8')
; 

UPDATE deh_temp_gridcells_by_grid_id_year g, PSRC_2000_baseyear_reestimation.development_types dt
SET 	g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND (g.COMMERCIAL_SQFT >= g.INDUSTRIAL_SQFT) 
	AND (g.COMMERCIAL_SQFT >= g.GOVERNMENTAL_SQFT)
	AND dt.NAME IN ('C1','C2','C3')
;


UPDATE deh_temp_gridcells_by_grid_id_year g, PSRC_2000_baseyear_reestimation.development_types dt
SET 	g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND (g.INDUSTRIAL_SQFT > g.COMMERCIAL_SQFT) 
	AND (g.INDUSTRIAL_SQFT > g.GOVERNMENTAL_SQFT)
	AND dt.NAME IN ('I1','I2','I3')
;


UPDATE deh_temp_gridcells_by_grid_id_year g, PSRC_2000_baseyear_reestimation.development_types dt
SET g.DEVELOPMENT_TYPE_ID = dt.DEVELOPMENT_TYPE_ID 
WHERE (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
	AND (g.GOVERNMENTAL_SQFT > g.COMMERCIAL_SQFT) 
	AND (g.GOVERNMENTAL_SQFT >= g.INDUSTRIAL_SQFT)
	AND g.GOVERNMENTAL_SQFT > 0
	AND dt.NAME = 'GV'
;


UPDATE deh_temp_gridcells_by_grid_id_year SET DEVELOPMENT_TYPE_ID = 24 where TOTAL_NONRES_SQFT = 0 and RESIDENTIAL_UNITS = 0;

-- UPDATE deh_temp_gridcells_sum_by_grid_id_year SET DEVELOPMENT_TYPE_ID = 23
-- WHERE PERCENT_PUBLIC_SPACE >= 50;

-- UPDATE deh_temp_gridcells_sum_by_grid_id_year SET DEVELOPMENT_TYPE_ID = 25
-- WHERE PERCENT_AGR >= 50;

-- UPDATE deh_temp_gridcells_sum_by_grid_id_year SET DEVELOPMENT_TYPE_ID = 26
-- WHERE IS_INSIDE_NATIONAL_FOREST = 1;

-- UPDATE deh_temp_gridcells_sum_by_grid_id_year SET DEVELOPMENT_TYPE_ID = 28
-- WHERE PERCENT_MINING >= 50;

-- UPDATE deh_temp_gridcells_sum_by_grid_id_year SET DEVELOPMENT_TYPE_ID = 27
-- WHERE IS_INSIDE_MILITARY_BASE = 1;

-- UPDATE deh_temp_gridcells_sum_by_grid_id_year set DEVELOPMENT_TYPE_ID = 29
-- WHERE (PERCENT_WATER >= 75 OR PERCENT_UNDEVELOPABLE >= 75) 
-- and (DEVELOPMENT_TYPE_ID NOT BETWEEN 1 and 23)
-- and (residential_units = 0)
-- and (total_nonres_sqft = 0)
-- ;


---- redundant script to work around 'table full error' 

-- create table deh_temp_gridcells_sum_by_grid_id_year_dt
-- select 
-- 	g.GRID_ID,
-- 	g.YEAR_BUILT,
-- 	g.COMMERCIAL_SQFT,
-- 	g.COMMERCIAL_IMPROVEMENT_VALUE,
-- 	g.INDUSTRIAL_SQFT,
-- 	g.INDUSTRIAL_IMPROVEMENT_VALUE,
-- 	g.GOVERNMENTAL_SQFT,
-- 	g.GOVERNMENTAL_IMPROVEMENT_VALUE,
-- 	g.RESIDENTIAL_UNITS,
-- 	g.RESIDENTIAL_IMPROVEMENT_VALUE,
-- 	g.TOTAL_NONRES_SQFT,
-- 	dt.DEVELOPMENT_TYPE_ID
-- from 
-- 	deh_temp_gridcells_sum_by_grid_id_year g,
-- 	PSRC_2000_baseyear_reestimation.development_types dt
-- where (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
-- 	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
-- 	AND dt.NAME IN ('R1','R2','R3','R4','R5','R6','R7','R8','M1','M2','M3','M4','M5','M6','M7','M8')
-- ; 

-- insert into deh_temp_gridcells_sum_by_grid_id_year_dt
-- select 
-- 	g.GRID_ID,
-- 	g.YEAR_BUILT,
-- 	g.COMMERCIAL_SQFT,
-- 	g.COMMERCIAL_IMPROVEMENT_VALUE,
-- 	g.INDUSTRIAL_SQFT,
-- 	g.INDUSTRIAL_IMPROVEMENT_VALUE,
-- 	g.GOVERNMENTAL_SQFT,
-- 	g.GOVERNMENTAL_IMPROVEMENT_VALUE,
-- 	g.RESIDENTIAL_UNITS,
-- 	g.RESIDENTIAL_IMPROVEMENT_VALUE,
-- 	g.TOTAL_NONRES_SQFT,
-- 	dt.DEVELOPMENT_TYPE_ID
-- from 
-- 	deh_temp_gridcells_sum_by_grid_id_year g,
-- 	PSRC_2000_baseyear_reestimation.development_types dt
-- where (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
-- 	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
-- 	AND (g.COMMERCIAL_SQFT >= g.INDUSTRIAL_SQFT) 
-- 	AND (g.COMMERCIAL_SQFT >= g.GOVERNMENTAL_SQFT)
-- 	AND dt.NAME IN ('C1','C2','C3')
-- ;

-- insert into deh_temp_gridcells_sum_by_grid_id_year_dt
-- select 
-- 	g.GRID_ID,
-- 	g.YEAR_BUILT,
-- 	g.COMMERCIAL_SQFT,
-- 	g.COMMERCIAL_IMPROVEMENT_VALUE,
-- 	g.INDUSTRIAL_SQFT,
-- 	g.INDUSTRIAL_IMPROVEMENT_VALUE,
-- 	g.GOVERNMENTAL_SQFT,
-- 	g.GOVERNMENTAL_IMPROVEMENT_VALUE,
-- 	g.RESIDENTIAL_UNITS,
-- 	g.RESIDENTIAL_IMPROVEMENT_VALUE,
-- 	g.TOTAL_NONRES_SQFT,
-- 	dt.DEVELOPMENT_TYPE_ID
-- from 
-- 	deh_temp_gridcells_sum_by_grid_id_year g,
-- 	PSRC_2000_baseyear_reestimation.development_types dt
-- where (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
-- 	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
-- 	AND (g.INDUSTRIAL_SQFT > g.COMMERCIAL_SQFT) 
-- 	AND (g.INDUSTRIAL_SQFT > g.GOVERNMENTAL_SQFT)
-- 	AND dt.NAME IN ('I1','I2','I3')
-- ;

-- insert into deh_temp_gridcells_sum_by_grid_id_year_dt
-- select 
-- 	g.GRID_ID,
-- 	g.YEAR_BUILT,
-- 	g.COMMERCIAL_SQFT,
-- 	g.COMMERCIAL_IMPROVEMENT_VALUE,
-- 	g.INDUSTRIAL_SQFT,
-- 	g.INDUSTRIAL_IMPROVEMENT_VALUE,
-- 	g.GOVERNMENTAL_SQFT,
-- 	g.GOVERNMENTAL_IMPROVEMENT_VALUE,
-- 	g.RESIDENTIAL_UNITS,
-- 	g.RESIDENTIAL_IMPROVEMENT_VALUE,
-- 	g.TOTAL_NONRES_SQFT,
-- 	dt.DEVELOPMENT_TYPE_ID
-- from 
-- 	deh_temp_gridcells_sum_by_grid_id_year g,
-- 	PSRC_2000_baseyear_reestimation.development_types dt
-- where (g.TOTAL_NONRES_SQFT between dt.MIN_SQFT AND dt.MAX_SQFT)
-- 	AND (g.RESIDENTIAL_UNITS between dt.MIN_UNITS AND dt.MAX_UNITS)
-- 	AND (g.GOVERNMENTAL_SQFT > g.COMMERCIAL_SQFT) 
-- 	AND (g.GOVERNMENTAL_SQFT >= g.INDUSTRIAL_SQFT)
-- 	AND g.GOVERNMENTAL_SQFT > 0
-- 	AND dt.NAME = 'GV'
-- ;

