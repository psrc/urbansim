CREATE TABLE test_average_land_value_per_acre_by_land_use
SELECT 
	c.COUNTY_NAME AS COUNTY,
	b.generic_land_use_1 as LAND_USE,
	round((sum(a.land_value))/(sum(a.lot_sqft/43560)),2)AS AVG_LAND_VAL_PER_ACRE,
	count(*) as PARCEL_COUNT
FROM (PSRC_parcels_all_counties.parcels a inner join PSRC_parcels_all_counties.land_use_generic_reclass b 
	ON a.county = b.county and a.land_use = b.county_land_use_code)
	INNER JOIN county_names c ON a.county = c.county_code
GROUP BY a.county, b.generic_land_use_1;
