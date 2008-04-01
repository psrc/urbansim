create table landprice_by_devtype
select YEAR, DEVELOPMENT_TYPE_ID,
  avg(RESIDENTIAL_LAND_VALUE + NONRESIDENTIAL_LAND_VALUE) as LAND_VALUE
from gridcells_exported
group by YEAR, DEVELOPMENT_TYPE_ID;

create index landprice_year_devtype on landprice_by_devtype (YEAR, DEVELOPMENT_TYPE_ID);
