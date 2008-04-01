##Non-residential sqft added per starting development type

select a.YEAR,a.DEVELOPMENT_TYPE_ID as STARTING_DEVELOPMENT_TYPE_ID,(sum(b.COMMERCIAL_SQFT+b.INDUSTRIAL_SQFT+b.GOVERNMENTAL_SQFT) - sum(a.COMMERCIAL_SQFT+a.INDUSTRIAL_SQFT+a.GOVERNMENTAL_SQFT)) as ADDED_SQFT 
from gridcells_exported a, gridcells_exported b
where a.YEAR=b.YEAR-1 AND a.GRID_ID=b.GRID_ID AND (a.COMMERCIAL_SQFT+a.INDUSTRIAL_SQFT+a.GOVERNMENTAL_SQFT) < (b.COMMERCIAL_SQFT+b.INDUSTRIAL_SQFT+b.GOVERNMENTAL_SQFT)
group by a.YEAR, a.DEVELOPMENT_TYPE_ID;

##Non-residential sqft added per ending development type

select b.YEAR,b.DEVELOPMENT_TYPE_ID as ENDING_DEVELOPMENT_TYPE_ID,(sum(b.COMMERCIAL_SQFT+b.INDUSTRIAL_SQFT+b.GOVERNMENTAL_SQFT) - sum(a.COMMERCIAL_SQFT+a.INDUSTRIAL_SQFT+a.GOVERNMENTAL_SQFT)) as ADDED_SQFT 
from gridcells_exported a, gridcells_exported b
where a.YEAR=b.YEAR-1 AND a.GRID_ID=b.GRID_ID AND (a.COMMERCIAL_SQFT+a.INDUSTRIAL_SQFT+a.GOVERNMENTAL_SQFT) < (b.COMMERCIAL_SQFT+b.INDUSTRIAL_SQFT+b.GOVERNMENTAL_SQFT)
group by b.YEAR, b.DEVELOPMENT_TYPE_ID;

##Residential added per starting development type 

select a.YEAR,a.DEVELOPMENT_TYPE_ID as STARTING_DEVELOPMENT_TYPE_ID,(sum(b.RESIDENTIAL_UNITS) - sum(a.RESIDENTIAL_UNITS)) as ADDED_UNITS 
from gridcells_exported a, gridcells_exported b
where a.YEAR=b.YEAR-1 AND a.GRID_ID=b.GRID_ID AND (a.RESIDENTIAL_UNITS) < (b.RESIDENTIAL_UNITS)
group by a.YEAR, a.DEVELOPMENT_TYPE_ID;

##Residential added per ending development type 

select b.YEAR,b.DEVELOPMENT_TYPE_ID as ENDING_DEVELOPMENT_TYPE_ID,(sum(b.RESIDENTIAL_UNITS) - sum(a.RESIDENTIAL_UNITS)) as ADDED_UNITS 
from gridcells_exported a, gridcells_exported b
where a.YEAR=b.YEAR-1 AND a.GRID_ID=b.GRID_ID AND (a.RESIDENTIAL_UNITS) < (b.RESIDENTIAL_UNITS)
group by b.YEAR, b.DEVELOPMENT_TYPE_ID;

