CREATE TABLE land_value_by_type SELECT year, development_type_id, 
  AVG(residential_land_value) + AVG(nonresidential_land_value) as land_value
  FROM gridcells_exported GROUP BY year, development_type_id;