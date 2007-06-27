-- These are the synthesized buildings created to house military households
insert into buildings
  (
    building_id,
    parcel_id,
    stories,
    land_area,
    year_built,
    residential_units,
    building_type_id,
    county,
    assessors_parcel_id,
    tax_exempt,
    zone_id,
    non_residential_sqft,
    sqft_per_unit,
    building_quality_id,
    building_sqft)
values
 (-1, 693060, 1, -1, 2000, 1170, 6, '053', '0530219121000', -1, 847, 0, -1, -1, -1),
 (-1, 681592, 1, -1, 2000, 1170, 6, '053', '0530119353002', -1, 850, 0, -1, -1, -1),
 (-1, 681316, 1, -1, 2000, 1170, 6, '053', '0530119132001', -1, 848, 0, -1, -1, -1),
 (-1, 656173, 1, -1, 2000, 1170, 6, '035', '0352187029', -1, 888, 0, -1, -1, -1),
 (-1, 592578, 1, -1, 2000, 1170, 6, '035', '0351337203', -1, 899, 0, -1, -1, -1);