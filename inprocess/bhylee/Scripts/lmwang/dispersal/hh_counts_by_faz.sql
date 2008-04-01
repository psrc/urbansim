---on aarhus
select f.faz_id, hh.year, count(*) as counts
into outfile 'counts_by_faz_30.tab'
from households_exported as hh 
	left outer join PSRC_2000_baseyear_0510_lmwang.gridcells as gc 
	  on hh.grid_id = gc.grid_id
	left outer join PSRC_2000_baseyear_0510_lmwang.zones_in_faz f
	  on gc.zone_id = f.zone_id
where hh.year= 2030
group by faz_id
;

select f.faz_id, hh.year, count(*) as counts
into outfile 'counts_by_faz_01.tab'
from households_exported as hh 
	left outer join PSRC_2000_baseyear_0510_lmwang.gridcells as gc 
	  on hh.grid_id = gc.grid_id
	left outer join PSRC_2000_baseyear_0510_lmwang.zones_in_faz f
	  on gc.zone_id = f.zone_id
where hh.year= 2001
group by faz_id
;

select gc.zone_id, hh.year, count(*) as counts
into outfile 'counts_by_zone_30.tab'
from households_exported as hh 
	left outer join PSRC_2000_baseyear_0510_lmwang.gridcells as gc 
	  on hh.grid_id = gc.grid_id
where hh.year= 2030
group by zone_id
;

select gc.zone_id, hh.year, count(*) as counts
into outfile 'counts_by_zone_01.tab'
from households_exported as hh 
	left outer join PSRC_2000_baseyear_0510_lmwang.gridcells as gc 
	  on hh.grid_id = gc.grid_id
where hh.year= 2001
group by zone_id
;

---on trondheim
mysql -e 'select f.faz_id, hh.year, count(*) as counts \
from PSRC_2000_test_hlc_output_30yrs.households_exported as hh  \
left outer join GSPSRC_2000_baseyear_flattened.gridcells as gc \
	  on hh.grid_id = gc.grid_id \
	left outer join GSPSRC_2000_baseyear_flattened.zones_in_faz f \
	  on gc.zone_id = f.zone_id \
where hh.year= 2030 \
group by faz_id' > pfaz_30.tab

mysql -e 'select f.faz_id, 2000 as year, count(*) as counts \
from GSPSRC_2000_baseyear_flattened.households as hh  \
left outer join GSPSRC_2000_baseyear_flattened.gridcells as gc \
	  on hh.grid_id = gc.grid_id \
	left outer join GSPSRC_2000_baseyear_flattened.zones_in_faz f \
	  on gc.zone_id = f.zone_id \
group by faz_id' > pfaz_01.tab

