alter table buildings add building_id int auto_increment key, add building_use_id int, add unit_price float;
#create index building_use_restype_index on buildings (building_use(10), restype(10));

update buildings b, building_use u set b.building_use_id=u.building_use_id where b.building_use = u.building_use;
update buildings b, building_use u set b.building_use_id=u.building_use_id where b.restype = u.building_use;

#update building attributes from assessors01
create index blklot_index on san_francisco.assessors01(blklot)
update buildings b, san_francisco.assr01 a 
set b.bedrooms=a.bdrms where b.blklot=a.blklot;

#attach sales data to building
alter table buildings add sale_year int, sale_month int;
update buildings b, assessors_data.sales01 s 
set b.sale_price = s.sale_price, b.sale_year = s.sale_year, b.sale_month=month(s.saledate) 
where b.blklot=s.blklot and s.sale_year=1996;

update buildings set unit_price = sale_price / residential_units where building_use='resident' and residential_units > 0;
update buildings set unit_price = sale_price / building_sqft where building_use<>'resident' and building_sqft > 0;
