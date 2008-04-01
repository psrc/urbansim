# This creates generic building use for buildings based on its parcel's generic land use
#  It works only on buildings with building_use in (0, NULL).

update ((buildings a 
	inner join parcels b
	on a.parcel_id = b.parcel_id)
	inner join PSRC_2000_data_quality_indicators.land_use_generic_reclass c
	on b.county = c.county and b.land_use = c.county_land_use_code)
	left join PSRC_2000_data_quality_indicators.building_use_generic_reclass bu
	on a.county = bu.county and a.building_use = bu.county_building_use_code
set a.building_use = concat('Imputed - ', c.generic_land_use_1)
where a.building_use is null or a.building_use = '0' or bu.generic_building_use_1 = 'Basement'
;



# Insert 'Imputed - generic_land_use_1' classifications into buildings and land use tables
#  Used for Kitsap County

INSERT INTO building_use_generic_reclass (county_building_use_code, generic_building_use_1, generic_building_use_2, county)
 VALUES ('Imputed - Agriculture', 'Agriculture', 'I', '035'), 
 	('Imputed - Civic and Quasi-Public', 'Civic and Quasi-Public', 'G', '035'),
 	('Imputed - Commercial', 'Commercial', 'C', '035'), 
 	('Imputed - Fisheries', 'Fisheries', 'C', '035'), 
 	('Imputed - Forest - harvestable', 'Forest - harvestable', 'C', '035'), 
 	('Imputed - Forest - protected', 'Forest - protected', 'C', '035'),
 	('Imputed - Government', 'Government', 'G', '035'),
 	('Imputed - Group Quarters', 'Group Quarters', 'R', '035'),
 	('Imputed - Hospital / Convalescent Center', 'Hospital / Convalescent Center', 'G', '035'),
 	('Imputed - Industrial', 'Industrial', 'I', '035'),
 	('Imputed - Military', 'Military', 'G', '035'), 
 	('Imputed - Mining', 'Mining', 'I', '035'),
 	('Imputed - Miscellaneous Use', 'Miscellaneous Use', 'null', '035'),
 	('Imputed - Mobile Home Park', 'Mobile Home Park', 'R', '035'),
 	('Imputed - Multi-Familt Residential', 'Multi-Family Residential', 'R', '035'),
 	('Imputed - No Land Use Code', 'Land Use Code', 'null', '035'),
 	('Imputed - Office', 'Office', 'C', '035'),
 	('Imputed - Park and Open Space', 'Park and Open Space', 'G', '035'),
 	('Imputed - Parking', 'Parking', 'C', '035'),
 	('Imputed - Recreation', 'Recreation', 'C', '035'),
 	('Imputed - Right-of-Way', 'Right-of-Way', 'G', '035'),
 	('Imputed - School', 'School', 'G', '035'),
 	('Imputed - Single Family Residential', 'Single Family Residential', 'R', '035'),
 	('Imputed - Transportation Communication Utilities', 'Transportation Communication Utilities', 'G', '035'),
 	('Imputed - Tribal', 'Tribal', 'G', '035'),
 	('Imputed - Vacant', 'Vacant', 'C', '035'),
 	('Imputed - Warehousing', 'Warehousing', 'I', '035'),
 	('Imputed - Water', 'Water', 'null', '035')
 ;
# Kitsap County missing building_use codes 
INSERT INTO building_use_generic_reclass (county_building_use_code, generic_building_use_1, generic_building_use_2, county)
 VALUES ('Apartment, High Rise, Shell', 'Multi-Family Residential', 'R', '035'),
 	('Barn', 'Agriculture', 'C', '035'),
 	('Church w/ Sunday School', 'Civic and Quasi-Public', 'G', '035'),
 	('City Club', 'Commercial', 'C', '035'),
 	('Classrooms - College', 'School', 'G', '035'),
 	('Community Shopping Center', 'Commercial', 'C', '035'),
 	('Elementary School - Entire', 'School', 'G', '035'),
 	('Equipment -Shop- Building', 'Warehousing', 'C', '035'),
 	('Equipment Shed', 'Warehousing', 'C', '035'),
 	('Farm Implement Shed', 'Warehousing', 'C', '035'),
 	('Fellowship Hall', 'Civic and Quasi-Public', 'G', '035'),
 	('Fraternal Building', 'Civic and Quasi-Public', 'G', '035'),
 	('Guest Cottage', 'Single Family Residential', 'R', '035'),
 	('Gymnasium - College', 'School', 'G', '035'),
 	('Junior High School - Entire', 'School', 'G', '035'),
 	('Light Utility/Storage', 'Warehousing', 'C', '035'),
 	('Material Shelter', 'Warehousing', 'C', '035'),
 	('Material Storage Building', 'Warehousing', 'C', '035'),
 	('Mini-Mart Convenience Store', 'Commercial', 'C', '035'),
 	('Mixed Retail w/ Office Units', 'Commercial', 'C', '035'),
 	('Multiple Res-Low Rise, Shell', 'Multi-Family Residential', 'R', '035'),
 	('Multipurpose Bldg K-12', 'School', 'G', '035'),
 	('Multipurpose Building-College', 'School', 'G', '035'),
 	('Office', 'Office', 'C', '035'),
 	('Parking Level', 'Parking', 'C', '035'),
 	('Relocatable Classroom', 'School', 'G', '035'),
 	('Relocatable Office', 'Office', 'C', '035'),
 	('School Dining Facility', 'School', 'G', '035'),
 	('Service Garage Shed', 'Commercial', 'C', '035'),
 	('Technical Trades Bldg-College', 'School', 'G', '035'),
 	('Vocational School', 'School', 'G', '035')
 ;
 
# PSRC suggested changes for Kitsap County Building Use Codes
UPDATE building_use_generic_reclass 
 SET generic_building_use_2 = 'I' WHERE county = '035' and county_building_use_code in 
 ('Distribution Warehouse', 
 'Hangar', 
 'Light Warehouse', 
 'Loft Warehouse', 
 'Storage Hangar', 
 'Storage Warehouse', 
 'T-Hangar', 
 'Transit Warehouse', 
 'Utility/Storage')
;

##################################################################################

# PSRC Suggested changes for King County Building Use Codes
UPDATE building_use_generic_reclass 
 SET generic_building_use_1 = 'Agriculture' WHERE county_building_use_code = '305' AND county = '033';

UPDATE building_use_generic_reclass 
 SET generic_building_use_2 = 'I' WHERE county_building_use_code = '305' AND county = '033';

UPDATE building_use_generic_reclass 
 SET generic_building_use_1 = 'Commercial' WHERE county_building_use_code in 
 ('303', '304', '317', '318', '319', '320', '340', '419', '531', '532', '534', '573', '830', '848') AND county = '033';

UPDATE building_use_generic_reclass 
 SET generic_building_use_2 = 'I' WHERE county_building_use_code in 
 ('328', '329', '387', '391', '406', '409', '447', '497', '525', '533') AND county = '033';

##################################################################################
# Pierce County missing building use code
INSERT INTO building_use_generic_reclass (county_building_use_code, generic_building_use_1, generic_building_use_2, county)
 VALUES ('Imputed - Transportation Communication Utilities', 'Transportation Communication Utilities', 'G', '053')
;

INSERT INTO building_use_generic_reclass (county_building_use_code, generic_building_use_1, generic_building_use_2, county)
 VALUES 
 	('Imputed - Agriculture', 'Agriculture', 'I', '053'),
 	('Imputed - Civic and Quasi-Public', 'Civic and Quasi-Public', 'G', '053'),
 	('Imputed - Commercial', 'Commercial', 'C', '053'), 
 	('Imputed - Fisheries', 'Fisheries', 'C', '053'), 
 	('Imputed - Forest - harvestable', 'Forest - harvestable', 'C', '053'), 
 	('Imputed - Government', 'Government', 'G', '053'),
 	('Imputed - Group Quarters', 'Group Quarters', 'R', '053'),
 	('Imputed - Hospital / Convalescent Center', 'Hospital / Convalescent Center', 'G', '053'),
 	('Imputed - Industrial', 'Industrial', 'I', '053'),
 	('Imputed - Military', 'Military', 'G', '053'), 
 	('Imputed - Mining', 'Mining', 'I', '053'),
 	('Imputed - Office', 'Office', 'C', '053'),
 	('Imputed - Park and Open Space', 'Park and Open Space', 'G', '053'),
 	('Imputed - Parking', 'Parking', 'C', '053'),
 	('Imputed - Recreation', 'Recreation', 'C', '053'),
 	('Imputed - Right-of-Way', 'Right-of-Way', 'G', '053'),
 	('Imputed - School', 'School', 'G', '053'),
 	('Imputed - Vacant', 'Vacant', 'C', '053'),
 	('Imputed - Warehousing', 'Warehousing', 'I', '053'),
 	('Imputed - Water', 'Water', 'null', '053')
; 	
 
# PSRC suggested changes for Pierce County Building Use Codes
UPDATE building_use_generic_reclass 
 SET generic_building_use_1 = 'Agriculture' WHERE county_building_use_code = '397' AND county = '053';
 
UPDATE building_use_generic_reclass
 SET generic_building_use_2 = 'I' WHERE county_building_use_code = '397' AND county = '053';

UPDATE building_use_generic_reclass 
 SET generic_building_use_1 = 'Commercial' WHERE county_building_use_code = '228' AND county = '053';
 
UPDATE building_use_generic_reclass 
 SET generic_building_use_2 = 'C' WHERE county_building_use_code = '228' AND county = '053';
 
UPDATE building_use_generic_reclass 
 SET generic_building_use_1 = 'Commercial' WHERE county_building_use_code = '680' AND county = '053'; 

UPDATE building_use_generic_reclass 
 SET generic_building_use_2 = 'C' WHERE county_building_use_code = '680' AND county = '053';
 
UPDATE building_use_generic_reclass 
 SET generic_building_use_1 = 'Commercial' WHERE county_building_use_code = '304' AND county = '053'; 
 
UPDATE building_use_generic_reclass 
 SET generic_building_use_2 = 'I' WHERE county_building_use_code in
 ('1468', '1473', '204', '328', '406', '409', '523') AND county = '053';

##################################################################################
# Snohomish County missing building use code
INSERT INTO building_use_generic_reclass (county_building_use_code, generic_building_use_1, generic_building_use_2, county)
 VALUES ('SERVICEB', 'Commercial', 'C', '061'),
 	('SCHADMIN', 'School', 'G', '061'),
 	('LOBBY', 'Commercial', 'C', '061')
;

# PSRC suggested changed for Snohomish County Building Use Codes
UPDATE building_use_generic_reclass 
 SET generic_building_use_1 = 'Commercial' WHERE county_building_use_code = 'BANK' AND county = '061'; 

UPDATE building_use_generic_reclass 
 SET generic_building_use_2 = 'I' WHERE county_building_use_code in 
 ('525', 'HANGAR', 'HUTLSTOR', 'Imputed - Warehousing', 'LFTWRHSE', 'LUTLSTOR', 'LWRHSE','UTLSTOR') AND county = '061';

##################################################################################

CREATE TABLE buildings_sqft_snohomish
 SELECT b.COUNTY_BUILDING_USE_CODE, b.BUILDING_DESCRIPTION, b.GENERIC_BUILDING_USE_1, b.GENERIC_BUILDING_USE_2,
 SUM(a.BUILT_SQFT) AS BUILT_SQFT, SUM(a.IMPUTED_SQFT) AS IMPUTED_SQFT 
 FROM buildings AS a 
 INNER JOIN PSRC_2000_data_quality_indicators.building_use_generic_reclass AS b 
  ON a.county = b.county and a.building_use = b.county_building_use_code
 GROUP BY b.COUNTY_BUILDING_USE_CODE, b.BUILDING_DESCRIPTION, b.GENERIC_BUILDING_USE_1, b.GENERIC_BUILDING_USE_2
 ORDER BY b.GENERIC_BUILDING_USE_1
; 

 

 

 	