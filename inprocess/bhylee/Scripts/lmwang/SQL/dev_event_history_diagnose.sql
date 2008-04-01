############################1. Gaps between buildings table and parcels table
#Diagnostic info:
#num of parcels in parcels table:
#  select county,count(distinct parcel_id) from parcels group by county;
+--------+---------------------------+
| county | count(distinct parcel_id) |
+--------+---------------------------+
| 033    |                    549931 |
| 035    |                    100335 |
| 053    |                    256578 |
| 061    |                    212396 |
+--------+---------------------------+
			     1119240
				
#num of parcels in buildings table:
# select county,count(distinct parcel_id) from temp_sqft_units_impv_by_year group by county;
+--------+---------------------------+
| county | count(distinct parcel_id) |
+--------+---------------------------+
| 033    |                    463983 |
| 035    |                     61566 |
| 053    |                    214274 |
| 061    |                      7804 |
  	                      747627

#num of parcels in parcels table but not in buildings table: 380,861 
select count(distinct p.parcel_id)
from parcels p
	left outer join temp_sqft_units_impv_by_year b
	on p.PARCEL_ID = b.PARCEL_ID
	and p.COUNTY = b.COUNTY
where b.PARCEL_ID is null;

#num of parcels in buildings table but not in parcels table: 9,749
select count(distinct b.parcel_id)
from parcels p
	right outer join temp_sqft_units_impv_by_year b
	on p.PARCEL_ID = b.PARCEL_ID
	and p.COUNTY = b.COUNTY
where p.PARCEL_ID is null;


##########################2.improvement value
#total parcels improvement value not in buildings table: 25,682,305,811 (14.5%)
select sum(p.improvement_value)
from parcels p
	left outer join temp_sqft_units_impv_by_year b
	on p.PARCEL_ID = b.PARCEL_ID
	and p.COUNTY = b.COUNTY
where b.PARCEL_ID is null;

#total improvement value in parcels: 177305898173
select sum(p.improvement_value) from parcels p;

#total improvement value in development_event_history: 151,129,676,851
select 
	sum(residential_improvement_value)+
	sum(commercial_improvement_value)+
	sum(industrial_improvement_value)+
	sum(governmental_improvement_value) as total_impv
from development_event_history;

########################3. residential units
#total parcels residential units not in buildings table: -218113 (16.4%) = 
select sum(p.residential_units)
from parcels p
	left outer join temp_sqft_units_impv_by_year b
	on p.PARCEL_ID = b.PARCEL_ID
	and p.COUNTY = b.COUNTY
where b.PARCEL_ID is null;

#total residential units in parcels: 1332351
select sum(p.residential_units) from parcels p;

#total residential units in development_event_history: 1,099,168
select sum(residential_units) from development_event_history; 


#####################4. built_sqft
#total non_residential built_sqft in buildings: 772678565
select sum(built_sqft) from temp_sqft_units_by_year_full where building_use in ('C', 'I', 'G');

#total non_residential_sqft in development_event_history: 742,465,579
select 
	sum(commercial_sqft)+
	sum(industrial_sqft)+
	sum(governmental_sqft) as total_sqft
from development_event_history;


##################5. other diagnostic info
#parcel with more than one building           #50571/380861 = 13.3%
select parcel_id, count(*) from temp_sqft_units_impv_by_year
group by parcel_id, county having count(*) > 1;


#residential units in parcels with at least 1 residential building ('R'): 1,080,285 (81.1%)
select sum(p.residential_units)
from temp_table_r r
	inner join parcels p
	on r.PARCEL_ID = p.PARCEL_ID
	and r.COUNTY = p.COUNTY
where r.TOTAL_RES_BUILDINGS_IN_PARCEL > 0
;


---- check the gaps in residential_units, non-residential sqft between gridcells and development_event_history table
select 
	g.grid_id, 
	g.year_built, 
	g.residential_units as g_units,
	e.residential_units as e_units,
	g.commercial_sqft as gc_sqft,
	e.commercial_sqft as ec_sqft,
	g.industrial_sqft as gi_sqft,
	e.industrial_sqft as ei_sqft,
	g.governmental_sqft as gg_sqft,
	e.governmental_sqft as eg_sqft
from PSRC_2000_baseyear.gridcells g
inner join PSRC_parcels_all_counties.deh_temp_gridcells_sum_by_grid_id_year e
on g.grid_id = e.grid_id and g.year_built = e.year_built
where g.residential_units <> e.residential_units 
or g.commercial_sqft <> e.commercial_sqft
or g.industrial_sqft <> e.industrial_sqft
or g.governmental_sqft <> e.governmental_sqft
;

-- residential_units
select grid_id, scheduled_year, residential_units
from development_event_history
where grid_id = 484231;

select grid_id, year_built, residential_units
from PSRC_2000_baseyear.gridcells
where grid_id = 484231;

select p.parcel_id,RESIDENTIAL_UNITS, f.PARCEL_FRACTION
from  PSRC_parcels_all_counties.deh_temp_units_impv_by_parcel p inner join PSRC_parcels_all_counties.parcel_fractions_in_gridcells f
	on p.parcel_id = f.parcel_id and p.county = f.county
where f.grid_id = 484231
;

select p.parcel_id,RESIDENTIAL_UNITS_imputed, f.PARCEL_FRACTION
from  PSRC_parcels_all_counties.parcels p inner join PSRC_parcels_all_counties.parcel_fractions_in_gridcells f
	on p.parcel_id = f.parcel_id and p.county = f.county
where f.grid_id = 484231
;


-- nr-sqft
select grid_id, scheduled_year, commercial_sqft, industrial_sqft, governmental_sqft
from development_event_history
where grid_id = 644238;

select grid_id, year_built, commercial_sqft, industrial_sqft, governmental_sqft
from PSRC_2000_baseyear.gridcells
where grid_id = 644238;

select * from parcel_fractions_in_gridcells f
where f.grid_id = 644238;

select 
	b.parcel_id, year_built, 
	BUILT_SQFT, IMPUTED_SQFT, 
	u.generic_building_use_2 as building_use, 
	f.PARCEL_FRACTION as fraction
from  
	PSRC_parcels_kitsap.buildings b 
	  inner join 
	parcel_fractions_in_gridcells f
	  on b.parcel_id = f.parcel_id and b.county = f.county
	  inner join 
	PSRC_2000_data_quality_indicators.building_use_generic_reclass u
	  on u.county = b.county 
          and u.county_building_use_code = b.building_use
where f.grid_id = 644238
;

----------------------------------------------------------------------------------
select grid_id, scheduled_year, commercial_sqft, industrial_sqft, governmental_sqft
from development_event_history
where grid_id = 830639;

select grid_id, year_built, commercial_sqft, industrial_sqft, governmental_sqft
from PSRC_2000_baseyear.gridcells
where grid_id = 830639;

select * from parcel_fractions_in_gridcells f
where f.grid_id = 830639;

select 
	b.parcel_id, year_built, 
	BUILT_SQFT, IMPUTED_SQFT, 
	u.generic_building_use_2 as building_use, 
	f.PARCEL_FRACTION as fraction
from  
	PSRC_parcels_pierce.buildings b 
	  inner join parcel_fractions_in_gridcells f
	  on b.parcel_id = f.parcel_id and b.county = f.county
	  inner join 
	PSRC_2000_data_quality_indicators.building_use_generic_reclass u
	  on u.county = b.county 
          and u.county_building_use_code = b.building_use
where f.grid_id = 830639
;
