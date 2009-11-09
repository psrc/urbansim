create table buildings 
select a.blklot, a.landval, a.strucval, a.priorprice, a.construction, a.lotarea, a.units, a.stories, a.rooms, a.bdrms, a.baths, a.bldgsqft, 
a.bsmtsqft, a.yrbuilt, a.currprice, year(a.currsaledate) as sale_year, l.landuse, l.restype from assessors_data.assr06 a 
inner join san_francisco.luse05 l using (blklot);

alter table buildings add building_id int auto_increment key, add building_use_id int, add unit_price float;
create index landuse_restype_index on buildings (landuse(10), restype(10));

update buildings b, building_use u set b.building_use_id=u.building_use_id where b.landuse = u.building_use;
update buildings b, building_use u set b.building_use_id=u.building_use_id where b.restype = u.building_use;

update buildings set unit_price = currprice / units where landuse='resident' and units > 0;
update buildings set unit_price = currprice / bldgsqft where landuse<>'resident' and bldgsqft > 0;
