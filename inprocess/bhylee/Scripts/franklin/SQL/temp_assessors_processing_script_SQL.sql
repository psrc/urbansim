-- ----------------------------------------------------------------------
-- DEFINE INITIAL TABLES
-- ----------------------------------------------------------------------

--
-- INITIALIZE
--

FLUSH TABLES;
CREATE DATABASE IF NOT EXISTS workspace;
USE workspace;

--
-- BUILDINGS
--

DROP TABLE IF EXISTS all_buildings;

CREATE TABLE all_buildings (
  all_buildings_id INT(10) unsigned NOT NULL AUTO_INCREMENT,
  County VARCHAR(5) NULL,
  AccountID VARCHAR(25) NULL,
  BuildingID VARCHAR(25) NULL,
  BuildingFlag INT(3) NOT NULL DEFAULT '0',
  OutbuildingFlag INT(3) NOT NULL DEFAULT '0',
  BuildingUseCode VARCHAR(50) NOT NULL DEFAULT '0',
  BldgSF INT(11) NOT NULL DEFAULT '0',
  Stories DOUBLE(5,2) NOT NULL DEFAULT '0',
  Footprint INT(11) NOT NULL DEFAULT '0',
  YearBuilt INT(11) NOT NULL DEFAULT '0',
  BldgQuality VARCHAR(50) NOT NULL DEFAULT '0',
  BldgCondition VARCHAR(50) NOT NULL DEFAULT '0',
  NumberofUnits INT(11) NOT NULL DEFAULT '0',
  Bedrooms INT(3) NOT NULL DEFAULT '0',
  BathFull INT(3) NOT NULL DEFAULT '0',
  Bath3Qtr INT(3) NOT NULL DEFAULT '0',
  BathHalf INT(3) NOT NULL DEFAULT '0',
  Bathrooms DOUBLE(5,2) NOT NULL DEFAULT '0.00',
  BuildingUseDescription VARCHAR(100) NOT NULL DEFAULT '0',
  GeneralCategory VARCHAR(50) NOT NULL DEFAULT '0',
  GeneralCategoryCode INT(5) NOT NULL DEFAULT '0',
  BuildingType INT(1) NOT NULL DEFAULT '0', 
  BuildingTypeDesc VARCHAR(50) NOT NULL DEFAULT '0',
  ID_SUBPARCEL VARCHAR(30) NULL,
  PRIMARY KEY (all_buildings_id),
  INDEX id_buildings (ID_SUBPARCEL)
)
ENGINE = MyISAM
ROW_FORMAT = Dynamic
CHARACTER SET latin1 COLLATE latin1_swedish_ci;

--
-- SUBPARCELS
--

DROP TABLE IF EXISTS all_subparcels;

CREATE TABLE all_subparcels (
  all_subparcels_id INT(10) unsigned NOT NULL AUTO_INCREMENT,
  County CHAR(3) NULL,
  PARCEL_ID VARCHAR(25) NULL,
  AccountID VARCHAR(25) NULL,
  SubparcelFlag INT(1) NULL,
  NumberofBuildings INT(3) NOT NULL DEFAULT '0',
  NumberofOutbuildings INT(3) NOT NULL DEFAULT '0',
  LandValue INT(12) NOT NULL DEFAULT 0,
  ImprValue INT(12) NOT NULL DEFAULT 0,
  TaxExempt INT(5) NOT NULL DEFAULT 0,
  ID_SUBPARCEL VARCHAR(28) NULL,
  ID_PARCEL VARCHAR(28) NULL,
  PRIMARY KEY (all_subparcels_id),
  INDEX id_subparcel (ID_SUBPARCEL),
  INDEX id_parcel (ID_PARCEL)
)
ENGINE = MyISAM
ROW_FORMAT = Dynamic
CHARACTER SET latin1 COLLATE latin1_swedish_ci;

--
-- PARCELS
--

DROP TABLE IF EXISTS all_parcels;
CREATE TABLE all_parcels (
  all_parcels_id INT(10) unsigned NOT NULL AUTO_INCREMENT,
  County CHAR(3) NULL,
  PARCEL_ID VARCHAR(25) NULL,
  PLAT_ID VARCHAR(10) NULL,
  NumberofAccounts INT(11) NOT NULL DEFAULT '0',
  LandValueParcel INT(12) NOT NULL DEFAULT 0,
  ImprValueParcel INT(12) NOT NULL DEFAULT 0,
  TaxExemptParcel INT(5) NOT NULL DEFAULT 0,
  Jurisdiction VARCHAR(50) NOT NULL DEFAULT '0',
  Size_Acres DOUBLE(22,2) NOT NULL DEFAULT '0.00',
  Size_SF INT(11) NOT NULL DEFAULT '0',
  Land_Use VARCHAR(50) NOT NULL,
  Zoning VARCHAR(50) NOT NULL,
  LandUseDescription VARCHAR(100) NOT NULL DEFAULT '0',
  GenericLandUse1 VARCHAR(50) NOT NULL DEFAULT '0',
  GenericLandUse2 VARCHAR(50) NOT NULL DEFAULT '0',
  res_nonres VARCHAR(10) NOT NULL DEFAULT '0',
  ID_PARCEL VARCHAR(28) NULL,
  ID_PLAT VARCHAR(13) NULL,
  PRIMARY KEY (all_parcels_id),
  INDEX id_parcel (ID_PARCEL)
)
ENGINE = MyISAM
ROW_FORMAT = Dynamic
CHARACTER SET latin1 COLLATE latin1_swedish_ci;


--
-- SALES
--

DROP TABLE IF EXISTS all_sales;
CREATE TABLE all_sales (
  all_sales_id INT(10) unsigned NOT NULL AUTO_INCREMENT,
  County CHAR(3) NULL,
  AccountID VARCHAR(25) NULL,
  ExciseTaxNumber VARCHAR(25) NULL,
  NumberofAccounts INT(5) NOT NULL DEFAULT '0',
  SaleDate DATE NULL,
  SalePrice INT(11) NOT NULL DEFAULT '0',
  PPropPrice INT(11) NOT NULL DEFAULT '0',
  BuyerName VARCHAR(255) NOT NULL DEFAULT '0',
  SellerName VARCHAR(255) NOT NULL DEFAULT '0',
  DeedType VARCHAR(50) NOT NULL DEFAULT '0',
  SaleWarnings VARCHAR(50) NOT NULL DEFAULT '0',
  InstrumentDescr VARCHAR(50) NOT NULL DEFAULT '0',
  ValidInstrument INT(11) NOT NULL DEFAULT '0',
  SWarnDescr VARCHAR(150) NOT NULL DEFAULT '0',
  ValidSale INT(1) NOT NULL DEFAULT '0',
  ID_SUBPARCEL VARCHAR(28) NULL,
  ID_SALE VARCHAR(53) NULL,
  PRIMARY KEY (all_sales_id),
  INDEX id_sales (ID_SALE),
  INDEX id_subparcel (ID_SUBPARCEL)
)
ENGINE = MyISAM
ROW_FORMAT = Dynamic
CHARACTER SET latin1 COLLATE latin1_swedish_ci;

FLUSH TABLES;

-- ----------------------------------------------------------------------




-- ----------------------------------------------------------------------
-- KING COUNTY DATA
-- ----------------------------------------------------------------------

--
-- Copy raw data to working directory
--

FLUSH TABLES;
USE workspace;

CREATE TEMPORARY TABLE king_aptcomplex_temp
SELECT * FROM king_20060127.extr_aptcomplex;

CREATE TEMPORARY TABLE king_commbldg_temp
SELECT * FROM king_20060127.extr_commbldg;

CREATE TEMPORARY TABLE king_resbldg_temp
SELECT * FROM king_20060127.extr_resbldg;

CREATE TEMPORARY TABLE king_condounit_temp
SELECT * FROM king_20060127.extr_condounit;

CREATE TEMPORARY TABLE king_condocomplex_temp
SELECT * FROM king_20060127.extr_condocomplex;

CREATE TEMPORARY TABLE king_parcel_temp
SELECT * FROM king_20060127.extr_parcel;

CREATE TEMPORARY TABLE king_sales_temp
SELECT * FROM king_20060127.extr_rpsale; 

CREATE TEMPORARY TABLE king_account_temp
SELECT * FROM king_20060127.extr_rpacct_noname;

CREATE TEMPORARY TABLE spatialdata
SELECT * FROM spatial.spatial_2005;

CREATE TEMPORARY TABLE building_type_king
SELECT * FROM general.building_type_reclass_2005 WHERE County = '033';

CREATE INDEX building_king USING BTREE ON building_type_king (building_use_code);

CREATE INDEX id_spatial USING BTREE ON spatialdata (ID_PARCEL);

CREATE INDEX id_account USING BTREE ON king_condounit_temp (Major);

CREATE INDEX id_account USING BTREE ON king_condocomplex_temp (Major);

--
-- Assembly of building data 
--

-- Organize apartment complex data

CREATE TEMPORARY TABLE king_aptcomplex_presort
SELECT 
CONCAT(a.Major, a.Minor) AS AccountID, 
a.Condition AS BldgCondition, 
a.NbrUnits AS NumberofUnits
FROM king_aptcomplex_temp a;

ALTER TABLE king_aptcomplex_presort 
MODIFY COLUMN AccountID VARCHAR(25) 
CHARACTER SET latin1 COLLATE latin1_swedish_ci;

CREATE INDEX id_account USING BTREE ON king_aptcomplex_presort (AccountID);

-- Organize commercial building data

CREATE TEMPORARY TABLE king_commbldg_presort
SELECT 
'033' AS County, 
CONCAT(e.Major, e.Minor) AS AccountID, 
e.BldgNbr AS BuildingID, 
1 AS BuildingFlag, 
0 AS OutbuildingFlag, 
e.PredominantUse AS BuildingUseCode, 
e.BldgGrossSqFt AS BldgSF, 
e.NbrStories AS Stories, 
IF(e.BldgGrossSqFt IS NOT NULL AND e.NbrStories IS NOT NULL, e.BldgGrossSqFt /e.NbrStories, 0) AS Footprint,
e.YrBuilt AS YearBuilt, 
e.BldgQuality, 
e.NbrBldgs AS NumberofBuildings, 
0 AS Bedrooms, 
0 AS BathFull, 
0 AS Bath3Qtr, 
0 AS BathHalf, 
0 AS Bathrooms
FROM king_commbldg_temp e
WHERE Minor <> '0000';

CREATE INDEX id_account USING BTREE ON king_commbldg_presort (AccountID);

-- Residential building data

CREATE TEMPORARY TABLE king_buildings1
SELECT 
'033' AS County, 
CONCAT(Major, Minor) AS AccountID, 
BldgNbr AS BuildingID, 
1 AS BuildingFlag, 
0 AS OutbuildingFlag, 
IF(NbrLivingUnits = 1, 'SFR', 'MFR') AS BuildingUseCode,
SqFtTotLiving AS BldgSF, 
Stories, 
IF(SqFtTotLiving IS NOT NULL AND Stories IS NOT NULL, SqFtTotLiving/Stories, NULL) AS Footprint, 
YrBuilt AS YearBuilt, 
CONCAT('res-',BldgGrade) AS BldgQuality, 
CONCAT('res-',e.Condition) AS BldgCondition, 
NbrLivingUnits AS NumberofUnits, 
Bedrooms, 
BathFullCount AS BathFull, 
Bath3qtrCount AS Bath3Qtr, 
BathHalfCount AS BathHalf, 
(BathFullCount + 0.5 * BathHalfCount + 0.75 * Bath3qtrCount) AS Bathrooms
FROM king_resbldg_temp e;

-- Apartment and commercial building data

CREATE TEMPORARY TABLE king_buildings2
SELECT 
a.County, 
a.AccountID, 
a.BuildingID, 
a.BuildingFlag, 
a.OutbuildingFlag, 
a.BuildingUseCode, 
a.BldgSF, 
a.Stories, 
a.Footprint, 
a.YearBuilt, 
CONCAT('comm-',a.BldgQuality) AS BldgQuality, 
CONCAT('comm-',b.BldgCondition) AS BldgCondition,
b.NumberofUnits, 
a.Bedrooms, 
a.BathFull, 
a.Bath3Qtr, 
a.BathHalf, 
a.Bathrooms
FROM king_commbldg_presort a
LEFT JOIN king_aptcomplex_presort b ON a.AccountID = b.AccountID;

-- Condo complex data

CREATE TEMPORARY TABLE king_buildings3a
SELECT 
'033' AS County, 
u.Major,
u.Minor,
CONCAT(u.Major, u.Minor) AS AccountID, 
u.UnitNbr AS BuildingID, 
1 AS BuildingFlag, 
0 AS OutbuildingFlag, 
CONCAT('Condo-',u.UnitType) AS BuildingUseCode, 
u.Footage AS BldgSF, 
0 AS Stories, 
0 AS Footprint, 
c.YrBuilt AS YearBuilt, 
CONCAT('condo-',c.BldgQuality) AS BldgQuality, 
CONCAT('condo-',c.Condition) AS BldgCondition, 
IF((u.UnitType >=1 AND u.UnitType<=4) OR u.UnitType=15 OR u.UnitType=16 OR u.UnitType=26,1,0) AS NumberofUnits, 
IF(u.NbrBedrooms='S',0,u.NbrBedrooms) AS Bedrooms, 
u.BathFullCount AS BathFull, 
0 AS Bath3Qtr, 
u.BathHalfCount AS BathHalf, 
(0.5 * u.BathHalfCount + u.BathFullCount) AS Bathrooms
FROM king_condounit_temp u
LEFT JOIN king_condocomplex_temp c ON c.Major = u.Major;

-- Identification of condos with only one unit (apartment uses?)

CREATE TEMPORARY TABLE king_condosandbuildings_1
SELECT * FROM king_commbldg_temp a WHERE Minor = '0000' GROUP BY Major HAVING COUNT(*) = 1;

CREATE TEMPORARY TABLE king_condosandbuildings_2
SELECT Major, Minor FROM king_condounit_temp WHERE PcntOwnership > 99 GROUP BY Major HAVING COUNT(*) = 1;

CREATE INDEX majornumber USING BTREE ON king_condosandbuildings_2 (Major);

CREATE TEMPORARY TABLE king_condosandbuildings_3
SELECT 
a.Major, b.Minor, a.BldgGrossSqFt, a.NbrStories, a.YrBuilt
FROM king_condosandbuildings_1 a
LEFT JOIN king_condosandbuildings_2 b ON a.Major = b.Major WHERE b.Major IS NOT NULL;

CREATE TEMPORARY TABLE king_complexandunits_1
SELECT Major, NbrUnits FROM king_condocomplex_temp a GROUP BY Major HAVING COUNT(*) = 1;

CREATE INDEX units USING BTREE ON king_complexandunits_1 (Major);

CREATE TEMPORARY TABLE king_condosandbuildings_4
SELECT a.*, b.NbrUnits AS Units FROM king_condosandbuildings_3 a
LEFT JOIN king_complexandunits_1 b ON a.Major = b.Major;

CREATE INDEX parcelid USING BTREE ON king_condosandbuildings_4 (Major, Minor);

-- On with the show!

CREATE TEMPORARY TABLE king_buildings3
SELECT
a.County,
a.AccountID,
a.BuildingID,
a.BuildingFlag,
a.OutbuildingFlag,
a.BuildingUseCode,
IF(a.BldgSF = 0, b.BldgGrossSqFt, a.BldgSF) AS BldgSF,
IF(a.Stories = 0, b.NbrStories, a.Stories) AS Stories,
IF(a.Footprint = 0 AND b.NbrStories > 0, b.BldgGrossSqFt / b.NbrStories, a.Footprint) AS Footprint,
IF(a.YearBuilt = 0, b.YrBuilt, a.YearBuilt) AS YearBuilt,
a.BldgQuality,
a.BldgCondition,
IF(b.Units IS NOT NULL AND b.Units > a.NumberofUnits, b.Units, a.NumberofUnits) AS NumberofUnits,
a.Bedrooms,
a.BathFull,
a.Bath3Qtr,
a.BathHalf,
a.Bathrooms
FROM king_buildings3a a
LEFT JOIN king_condosandbuildings_4 b ON a.Major = b.Major AND a.Minor = b.Minor;


-- Ensure that data corresponds to common format

ALTER TABLE king_buildings1 CONVERT TO CHARACTER SET latin1 COLLATE latin1_swedish_ci;
ALTER TABLE king_buildings2 CONVERT TO CHARACTER SET latin1 COLLATE latin1_swedish_ci;
ALTER TABLE king_buildings3 CONVERT TO CHARACTER SET latin1 COLLATE latin1_swedish_ci;

-- Concatenate tables

CREATE TEMPORARY TABLE king_buildings
SELECT * FROM king_buildings1
UNION
SELECT * FROM king_buildings2
UNION
SELECT * FROM king_buildings3;

CREATE INDEX building_codes USING BTREE ON king_buildings (BuildingUseCode);

-- Add additional columns

CREATE TEMPORARY TABLE king_buildings_2
SELECT 
a.*, 
b.building_use_description AS BuildingUseDescription, 
b.general_category AS GeneralCategory, 
b.general_category_code AS GeneralCategoryCode,
b.building_type AS BuildingType, 
b.building_type_desc AS BuildingTypeDesc,
CONCAT(a.County,a.AccountID) AS ID_SUBPARCEL
FROM king_buildings a
LEFT JOIN building_type_king b ON a.BuildingUseCode = b.building_use_code;

-- Change variables

ALTER TABLE king_buildings_2
MODIFY COLUMN County VARCHAR(5) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
MODIFY COLUMN AccountID VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
MODIFY COLUMN BuildingID VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
MODIFY COLUMN BuildingFlag INTEGER UNSIGNED DEFAULT 0,
MODIFY COLUMN OutbuildingFlag INTEGER UNSIGNED DEFAULT 0,
MODIFY COLUMN BuildingUseCode VARCHAR(50) CHARACTER SET latin1 NOT NULL DEFAULT '0' COLLATE latin1_swedish_ci,
MODIFY COLUMN BldgSF INT UNSIGNED NOT NULL DEFAULT 0,
MODIFY COLUMN Stories DOUBLE(5,2) NOT NULL DEFAULT 0,
MODIFY COLUMN Footprint INTEGER UNSIGNED DEFAULT 0,
MODIFY COLUMN YearBuilt INTEGER UNSIGNED DEFAULT 0,
MODIFY COLUMN BldgQuality VARCHAR(50) CHARACTER SET latin1 DEFAULT '0' COLLATE latin1_swedish_ci,
MODIFY COLUMN BldgCondition VARCHAR(50) CHARACTER SET latin1 DEFAULT '0' COLLATE latin1_swedish_ci,
MODIFY COLUMN NumberofUnits INT UNSIGNED DEFAULT 0,
MODIFY COLUMN Bedrooms INT UNSIGNED DEFAULT 0,
MODIFY COLUMN BathFull INT UNSIGNED DEFAULT 0,
MODIFY COLUMN Bath3Qtr INT UNSIGNED DEFAULT 0,
MODIFY COLUMN BathHalf INT UNSIGNED DEFAULT 0,
MODIFY COLUMN Bathrooms DOUBLE(5,2) DEFAULT 0,
MODIFY COLUMN BuildingUseDescription VARCHAR(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN GeneralCategory VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN GeneralCategoryCode INT(5) NOT NULL DEFAULT 0, 
MODIFY COLUMN BuildingType INT(1) NOT NULL DEFAULT 0, 
MODIFY COLUMN BuildingTypeDesc VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN ID_SUBPARCEL VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

-- Add to final table

INSERT INTO all_buildings 
(County, AccountID, BuildingID, BuildingFlag, OutbuildingFlag, BuildingUseCode, BldgSF, Stories, Footprint, YearBuilt, BldgQuality, BldgCondition, NumberofUnits, Bedrooms, BathFull, Bath3Qtr, BathHalf, Bathrooms, BuildingUseDescription, GeneralCategory, GeneralCategoryCode, BuildingType, BuildingTypeDesc, ID_SUBPARCEL) 
SELECT County, AccountID, BuildingID, BuildingFlag, OutbuildingFlag, BuildingUseCode, BldgSF, Stories, Footprint, YearBuilt, BldgQuality, BldgCondition, NumberofUnits, Bedrooms, BathFull, Bath3Qtr, BathHalf, Bathrooms, BuildingUseDescription, GeneralCategory, GeneralCategoryCode, BuildingType, BuildingTypeDesc, ID_SUBPARCEL 
FROM king_buildings_2;

--
-- Assembly of subparcel data
--

-- Combine parcel IDs with condo IDs for full subparcel relation table

CREATE TEMPORARY TABLE king_subparcels
SELECT
'033' AS County,
CONCAT(p.Major, p.Minor) AS PARCEL_ID,
CONCAT(p.Major, p.Minor) AS AccountID,
0 AS SubparcelFlag,
CONCAT('033',p.Major, p.Minor) AS ID_SUBPARCEL
FROM king_parcel_temp p
WHERE p.Minor <> '0000'
UNION
SELECT
'033' AS County,
CONCAT(c.Major, '0000') AS PARCEL_ID,
CONCAT(c.Major, c.Minor) AS AccountID,
1 AS SubparcelFlag,
CONCAT('033',c.Major, c.Minor) AS ID_SUBPARCEL
FROM king_condounit_temp c;

ALTER TABLE king_subparcels
MODIFY COLUMN ID_SUBPARCEL VARCHAR(28) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

CREATE INDEX id_subparcels USING BTREE ON king_subparcels (ID_SUBPARCEL);

-- Assess number of buildings per subparcel

CREATE TEMPORARY TABLE king_building_sums
SELECT ID_SUBPARCEL, SUM(BuildingFlag) AS NumberofBuildings, SUM(OutbuildingFlag) AS NumberofOutbuildings
FROM king_buildings_2
GROUP BY ID_SUBPARCEL;

ALTER TABLE king_building_sums
MODIFY COLUMN ID_SUBPARCEL VARCHAR(28) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

CREATE INDEX id_buildingsums USING BTREE ON king_building_sums (ID_SUBPARCEL);

-- Merge building counts with subparcel data

CREATE TEMPORARY TABLE king_subparcels_2
SELECT a.County, a.PARCEL_ID, a.AccountID, a.SubparcelFlag, IFNULL(b.NumberofBuildings,0) AS NumberofBuildings, IFNULL(b.NumberofOutbuildings,0) AS NumberofOutbuildings, a.ID_SUBPARCEL, CONCAT(a.County, a.PARCEL_ID) AS ID_PARCEL
FROM king_subparcels a
LEFT JOIN king_building_sums b ON a.ID_SUBPARCEL = b.ID_SUBPARCEL;

-- Add assessed values

CREATE TEMPORARY TABLE king_values_2006_1
SELECT CONCAT('033',Major,Minor) AS ID_SUBPARCEL, IF(TaxValReason IS NULL OR TaxValReason = 'FS',0,1) AS TaxExempt, IF(ApprLandVal = 0, TaxableLandVal, ApprLandVal) AS LandValue, IF(ApprImpsVal=0, TaxableImpsVal, ApprImpsVal) AS ImprValue
FROM king_account_temp
WHERE BillYr = 2006 AND Major IS NOT NULL AND Minor IS NOT NULL
GROUP BY Major, Minor;

CREATE TEMPORARY TABLE king_values_2006_2
SELECT ID_SUBPARCEL, IF(SUM(TaxExempt) > 0, 1, 0) AS TaxExempt, SUM(LandValue) AS LandValue, SUM(ImprValue) AS ImprValue
FROM king_values_2006_1
GROUP BY ID_SUBPARCEL;

ALTER TABLE king_values_2006_2
MODIFY COLUMN TaxExempt VARCHAR(10) NOT NULL DEFAULT 0,
MODIFY COLUMN LandValue INT(12) NOT NULL DEFAULT 0,
MODIFY COLUMN ImprValue INT(12) NOT NULL DEFAULT 0,
MODIFY COLUMN ID_SUBPARCEL VARCHAR(28) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

CREATE INDEX id_values USING BTREE ON king_values_2006_2 (ID_SUBPARCEL);

CREATE TEMPORARY TABLE king_subparcels_3
SELECT a.*, b.TaxExempt, b.LandValue, b.ImprValue
FROM king_subparcels_2 a
LEFT JOIN king_values_2006_2 b ON a.ID_SUBPARCEL = b.ID_SUBPARCEL;

CREATE INDEX id_subparcels USING BTREE ON king_subparcels_3 (ID_SUBPARCEL);

-- Add to final table

INSERT INTO all_subparcels
(County, PARCEL_ID, AccountID, SubparcelFlag, NumberofBuildings, NumberofOutbuildings, LandValue, ImprValue, TaxExempt, ID_SUBPARCEL, ID_PARCEL)
SELECT County, PARCEL_ID, AccountID, SubparcelFlag, NumberofBuildings, NumberofOutbuildings, LandValue, ImprValue, TaxExempt, ID_SUBPARCEL, ID_PARCEL FROM king_subparcels_3;

--
-- Assembly of parcel data
--

-- Assess value, number of subparcels per parcel

CREATE TEMPORARY TABLE king_master
SELECT PARCEL_ID, COUNT(PARCEL_ID) AS Subparcels, IF(SUM(TaxExempt) > 0, 1, 0) AS TaxExemptParcel, SUM(LandValue) AS LandValueParcel, SUM(ImprValue) AS ImprValueParcel
FROM king_subparcels_3
WHERE PARCEL_ID IS NOT NULL
GROUP BY PARCEL_ID;

CREATE INDEX id_master USING BTREE ON king_master (PARCEL_ID);

-- Presort parcel data

CREATE TEMPORARY TABLE king_parcel_presort 
SELECT '033' AS County, CONCAT(e.Major, e.Minor) AS PARCEL_ID, e.Major AS PLAT_ID, e.DistrictName AS Jurisdiction, (e.SqFtLot / 43560) AS Size_Acres, e.SqFtLot AS Size_SF, e.PresentUse AS Land_Use, e.CurrentZoning AS Zoning
FROM king_parcel_temp e;

ALTER TABLE king_parcel_presort 
MODIFY COLUMN PARCEL_ID VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN PLAT_ID VARCHAR(10) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

CREATE INDEX id_presort USING BTREE ON king_parcel_presort (PARCEL_ID);

-- Assemble parcel data

CREATE TEMPORARY TABLE parcels_king
SELECT p.County, p.PARCEL_ID, p.PLAT_ID, k.Subparcels AS NumberofAccounts, k.TaxExemptParcel, k.LandValueParcel, k.ImprValueParcel, p.Jurisdiction, p.Size_Acres, p.Size_SF, p.Land_Use, p.Zoning
FROM king_master k
LEFT JOIN king_parcel_presort p ON p.PARCEL_ID = k.PARCEL_ID
WHERE p.PARCEL_ID IS NOT NULL;

ALTER TABLE parcels_king
MODIFY COLUMN County VARCHAR(5) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN Land_Use VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

CREATE INDEX id_code USING BTREE ON parcels_king (County, Land_Use);

-- Add additional columns

CREATE TEMPORARY TABLE parcels_king_2
SELECT a.County, a.PARCEL_ID, a.PLAT_ID, a.NumberofAccounts, a.TaxExemptParcel, a.LandValueParcel, a.ImprValueParcel, a.Jurisdiction, a.Size_Acres, a.Size_SF, a.Land_Use, a.Zoning, b.land_use_description AS LandUseDescription, b.generic_land_use_1 AS GenericLandUse1, b.generic_land_use_2 AS GenericLandUse2, b.res_nonres, CONCAT(a.County, a.PARCEL_ID) AS ID_PARCEL, CONCAT(a.County, a.PLAT_ID) AS ID_PLAT
FROM parcels_king a
LEFT JOIN general.land_use_generic_reclass_2005 b ON (b.county = a.County AND b.county_land_use_code = a.Land_Use);

ALTER TABLE parcels_king_2
MODIFY COLUMN Jurisdiction VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN LandUseDescription VARCHAR(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN GenericLandUse1 VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN GenericLandUse2 VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN res_nonres VARCHAR(10) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN ID_PARCEL VARCHAR(28) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN ID_PLAT VARCHAR(13) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

-- Add to final table

INSERT INTO all_parcels
(County, PARCEL_ID, PLAT_ID, NumberofAccounts, LandValueParcel, ImprValueParcel, TaxExemptParcel, Jurisdiction, Size_Acres, Size_SF, Land_Use, Zoning, LandUseDescription, GenericLandUse1, GenericLandUse2, res_nonres, ID_PARCEL, ID_PLAT)
SELECT County, PARCEL_ID, PLAT_ID, NumberofAccounts, LandValueParcel, ImprValueParcel, TaxExemptParcel, Jurisdiction, Size_Acres, Size_SF, Land_Use, Zoning, LandUseDescription, GenericLandUse1, GenericLandUse2, res_nonres, ID_PARCEL, ID_PLAT
FROM parcels_king_2;

--
-- Assembly of sales data
--

-- Collect initial variables

CREATE TEMPORARY TABLE sales_king
SELECT '033' AS County, CONCAT(Major, Minor) AS AccountID, ExciseTaxNbr AS ExciseTaxNumber,
SaleDate, SalePrice, PersPropPrice AS PPropPrice, BuyerName, SellerName, SaleInstrument AS DeedType,
IF(SaleWarning IS NULL, ' 0 ', CONCAT(' ', SaleWarning, ' ')) AS SaleWarnings
FROM king_sales_temp e
WHERE YEAR(SaleDate) > 1996;

CREATE INDEX id_excise USING BTREE ON sales_king (ExciseTaxNumber);

-- Count number of accounts per sale

CREATE TEMPORARY TABLE sales_king_counts
SELECT ExciseTaxNumber, COUNT(ExciseTaxNumber) AS NumberofAccounts
FROM sales_king GROUP BY ExciseTaxNumber;

CREATE INDEX id_excise USING BTREE ON sales_king_counts (ExciseTaxNumber);

-- Join counts to main table

ALTER TABLE sales_king 
MODIFY COLUMN ExciseTaxNumber VARCHAR(25) NULL,
MODIFY COLUMN DeedType VARCHAR(50) NOT NULL DEFAULT '0',
MODIFY COLUMN SaleWarnings VARCHAR(50) NOT NULL DEFAULT '0';

CREATE TEMPORARY TABLE sales_king_2
SELECT s.County, s.AccountID, s.ExciseTaxNumber, c.NumberofAccounts, s.SaleDate, s.SalePrice, s.PPropPrice, s.BuyerName, s.SellerName, s.DeedType, s.SaleWarnings
FROM sales_king s
LEFT JOIN sales_king_counts c ON c.ExciseTaxNumber = s.ExciseTaxNumber;

-- Add descriptions of sales instruments

CREATE TEMPORARY TABLE sales_king_3
SELECT a.*, i.InstrumentDescr, i.ValidInstrument
FROM sales_king_2 a
LEFT JOIN general.instrumenttypes i ON (a.County = i.County AND a.DeedType = i.InstrumentType);

-- Add descriptions of sales warnings

CREATE TEMPORARY TABLE sales_king_4
SELECT a.*, IF(s.SWarnDescr IS NULL, '', s.SWarnDescr) AS SWarnDescr, IF(s.ValidSale IS NULL, 0, s.ValidSale) AS ValidSale, CONCAT(a.County, a.AccountID) AS ID_SUBPARCEL, CONCAT(a.County,a.ExciseTaxNumber,a.AccountID) AS ID_SALE
FROM sales_king_3 a
LEFT JOIN general.salewarnings s ON (a.County = s.County AND a.SaleWarnings = s.SaleWarnings);

ALTER TABLE sales_king_4
MODIFY COLUMN InstrumentDescr VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN ValidInstrument INT NOT NULL DEFAULT 0,
MODIFY COLUMN SWarnDescr VARCHAR(150) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN ValidSale INT NOT NULL DEFAULT 0;

-- Add to final table

INSERT INTO all_sales
(County, AccountID, ExciseTaxNumber, NumberofAccounts, SaleDate, SalePrice, PPropPrice, BuyerName, SellerName, DeedType, SaleWarnings, InstrumentDescr, ValidInstrument, SWarnDescr, ValidSale, ID_SUBPARCEL, ID_SALE)
SELECT County, AccountID, ExciseTaxNumber, NumberofAccounts, SaleDate, SalePrice, PPropPrice, BuyerName, SellerName, DeedType, SaleWarnings, InstrumentDescr, ValidInstrument, SWarnDescr, ValidSale, ID_SUBPARCEL, ID_SALE
FROM sales_king_4;

FLUSH TABLES;

-- ----------------------------------------------------------------------







-- ----------------------------------------------------------------------
-- KITSAP COUNTY DATA 
-- ----------------------------------------------------------------------

--
-- Copy raw data to working directory 
--

FLUSH TABLES;
USE workspace;

CREATE TEMPORARY TABLE kitsap_buildings_temp
SELECT * FROM kitsap_20060323.building;

CREATE TEMPORARY TABLE kitsap_main_temp
SELECT * FROM kitsap_20060323.main;

CREATE TEMPORARY TABLE kitsap_address_temp
SELECT * FROM kitsap_20060323.flatats;

CREATE TEMPORARY TABLE kitsap_land_temp
SELECT * FROM kitsap_20060323.land;

CREATE TEMPORARY TABLE kitsap_sale_temp
SELECT * FROM kitsap_20060323.sale;

CREATE TEMPORARY TABLE spatialdata
SELECT * FROM spatial.spatial_2005;

CREATE TEMPORARY TABLE building_type_kitsap
SELECT * FROM general.building_type_reclass_2005 WHERE County = '035';

CREATE INDEX building_kitsap USING BTREE ON building_type_kitsap (building_use_code);

CREATE INDEX id_spatial USING BTREE ON spatialdata (ID_PARCEL);

--
-- Assembly of building data 
--

-- Collect all building data

CREATE TEMPORARY TABLE kitsap_buildings
SELECT
'035' AS County,
CONCAT(TRUNCATE(b.RP_ACCT_ID,0)) AS AccountID,
0 AS BuildingID,
IF(IMPROV_TYP = 'OTHER', 0, 1) AS BuildingFlag,
IF(IMPROV_TYP = 'OTHER', 1, 0) AS OutbuildingFlag,
IFNULL(b.USE_DESC,'') AS BuildingUseCode,
TRUNCATE(b.FLR_TOT_SF, 0) AS BldgSF,
TRUNCATE(b.STORIES,0) AS Stories,
IF(b.FLR_TOT_SF IS NOT NULL AND b.STORIES IS NOT NULL, b.FLR_TOT_SF/b.STORIES, 0) AS Footprint,
TRUNCATE(b.YEAR_BUILT,0) AS YearBuilt,
IF(q.Quality IS NULL, '', q.Quality) AS BldgQuality,
IF(b.COND_CD IS NULL, '', b.COND_CD) AS BldgCondition,
1 AS NumberofUnits,
b.BEDROOMS AS Bedrooms,
b.FULL_BATHS AS BathFull,
0 AS Bath3Qtr,
b.HALF_BATHS AS BathHalf,
(b.FULL_BATHS + 0.5 * b.HALF_BATHS) AS Bathrooms
FROM kitsap_buildings_temp b
LEFT JOIN general.kitsap_quality q ON (q.BLDG_TYP = b.BLDG_TYP);

CREATE INDEX building_codes USING BTREE ON kitsap_buildings (BuildingUseCode);

-- Add additional columns

CREATE TEMPORARY TABLE kitsap_buildings_2
SELECT 
a.*, 
b.building_use_description AS BuildingUseDescription, 
b.general_category AS GeneralCategory, 
b.general_category_code AS GeneralCategoryCode,
b.building_type AS BuildingType, 
b.building_type_desc AS BuildingTypeDesc,
CONCAT(a.County,a.AccountID) AS ID_SUBPARCEL
FROM kitsap_buildings a
LEFT JOIN building_type_kitsap b ON a.BuildingUseCode = b.building_use_code;

-- Ensure that data corresponds to common format

ALTER TABLE kitsap_buildings_2
MODIFY COLUMN County VARCHAR(5) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
MODIFY COLUMN AccountID VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
MODIFY COLUMN BuildingID VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
MODIFY COLUMN BuildingFlag INTEGER UNSIGNED DEFAULT 0,
MODIFY COLUMN OutbuildingFlag INTEGER UNSIGNED DEFAULT 0,
MODIFY COLUMN BuildingUseCode VARCHAR(50) CHARACTER SET latin1 NOT NULL DEFAULT '0' COLLATE latin1_swedish_ci,
MODIFY COLUMN BldgSF INT UNSIGNED NOT NULL DEFAULT 0,
MODIFY COLUMN Stories DOUBLE(5,2) NOT NULL DEFAULT 0,
MODIFY COLUMN Footprint INTEGER UNSIGNED DEFAULT 0,
MODIFY COLUMN YearBuilt INTEGER UNSIGNED DEFAULT 0,
MODIFY COLUMN BldgQuality VARCHAR(50) CHARACTER SET latin1 DEFAULT '0' COLLATE latin1_swedish_ci,
MODIFY COLUMN BldgCondition VARCHAR(50) CHARACTER SET latin1 DEFAULT '0' COLLATE latin1_swedish_ci,
MODIFY COLUMN NumberofUnits INT UNSIGNED DEFAULT 0,
MODIFY COLUMN Bedrooms INT UNSIGNED DEFAULT 0,
MODIFY COLUMN BathFull INT UNSIGNED DEFAULT 0,
MODIFY COLUMN Bath3Qtr INT UNSIGNED DEFAULT 0,
MODIFY COLUMN BathHalf INT UNSIGNED DEFAULT 0,
MODIFY COLUMN Bathrooms DOUBLE(5,2) DEFAULT 0,
MODIFY COLUMN BuildingUseDescription VARCHAR(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN GeneralCategory VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN GeneralCategoryCode INT(5) NOT NULL DEFAULT 0, 
MODIFY COLUMN BuildingType INT(1) NOT NULL DEFAULT 0, 
MODIFY COLUMN BuildingTypeDesc VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN ID_SUBPARCEL VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

-- Add to final table

INSERT INTO all_buildings 
(County, AccountID, BuildingID, BuildingFlag, OutbuildingFlag, BuildingUseCode, BldgSF, Stories, Footprint, YearBuilt, BldgQuality, BldgCondition, NumberofUnits, Bedrooms, BathFull, Bath3Qtr, BathHalf, Bathrooms, BuildingUseDescription, GeneralCategory, GeneralCategoryCode, BuildingType, BuildingTypeDesc, ID_SUBPARCEL) 
SELECT County, AccountID, BuildingID, BuildingFlag, OutbuildingFlag, BuildingUseCode, BldgSF, Stories, Footprint, YearBuilt, BldgQuality, BldgCondition, NumberofUnits, Bedrooms, BathFull, Bath3Qtr, BathHalf, Bathrooms, BuildingUseDescription, GeneralCategory, GeneralCategoryCode, BuildingType, BuildingTypeDesc, ID_SUBPARCEL 
FROM kitsap_buildings_2;

--
-- Assembly of subparcels 
--

-- Identify mobile homes in Kitsap data

CREATE TEMPORARY TABLE kitsap_mh
SELECT 
'035' AS County,
CONCAT(TRUNCATE(LD_ACCT_ID,0)) AS PARCEL_ID,
CONCAT(TRUNCATE(RP_ACCT_ID,0)) AS AccountID,
1 AS SubparcelFlag
FROM kitsap_main_temp m
WHERE (LD_ACCT_ID <> RP_ACCT_ID AND ACCT_STAT <> 'D' AND LEFT(ACCT_NO,1) <> '8');

-- Identify noncondos in Kitsap data

CREATE TEMPORARY TABLE kitsap_nocondo
SELECT
'035' AS County,
CONCAT(TRUNCATE(RP_ACCT_ID,0)) AS PARCEL_ID,
CONCAT(TRUNCATE(RP_ACCT_ID,0)) AS AccountID,
0 AS SubparcelFlag
FROM kitsap_main_temp m
WHERE (LD_ACCT_ID = RP_ACCT_ID AND ACCT_STAT <> 'D' AND LEFT(ACCT_NO,1) <> '8');

-- Identify condos and correspondences in Kitsap data 

CREATE TEMPORARY TABLE kitsap_condos_all
SELECT CONCAT(TRUNCATE(RP_ACCT_ID,0)) AS AccountID, ACCT_NO, LEFT(ACCT_NO,4) AS CODE1, LEFT(ACCT_NO,8) AS CODE2
FROM kitsap_main_temp m
WHERE LEFT(ACCT_NO,1) = '8' AND ACCT_STAT <> 'D'
ORDER BY ACCT_NO;

CREATE TEMPORARY TABLE kitsap_condos_mainparcel_1
SELECT CONCAT(TRUNCATE(RP_ACCT_ID,0)) AS PARCEL_ID, ACCT_NO, LEFT(ACCT_NO,4) AS CODE1
FROM kitsap_main_temp m
WHERE LEFT(ACCT_NO,1) = '8' AND ACCT_STAT <> 'D' AND SUBSTRING(ACCT_NO,10,3) = '000'
GROUP BY LEFT(ACCT_NO,4)
HAVING COUNT(*) = 1;

CREATE INDEX condo1 USING BTREE ON kitsap_condos_mainparcel_1 (CODE1);

CREATE TEMPORARY TABLE kitsap_condos_mainparcel_2
SELECT CONCAT(TRUNCATE(RP_ACCT_ID,0)) AS PARCEL_ID, ACCT_NO, LEFT(ACCT_NO,8) AS CODE2
FROM kitsap_main_temp m
WHERE LEFT(ACCT_NO,1) = '8' AND ACCT_STAT <> 'D' AND SUBSTRING(ACCT_NO,10,3) = '000'
GROUP BY LEFT(ACCT_NO,8);

CREATE INDEX condo1 USING BTREE ON kitsap_condos_mainparcel_2 (CODE2);

CREATE TEMPORARY TABLE kitsap_condosandparcel_1
SELECT 
'035' AS County,
b.PARCEL_ID,
a.AccountID,
a.ACCT_NO,
b.ACCT_NO AS ACCT_NO_MASTER,
a.CODE1,
a.CODE2
FROM kitsap_condos_all a
LEFT JOIN kitsap_condos_mainparcel_1 b ON a.CODE1 = b.CODE1;

CREATE TEMPORARY TABLE kitsap_condosandparcel_2
SELECT
County,
IF(a.PARCEL_ID IS NULL, b.PARCEL_ID, a.PARCEL_ID) AS PARCEL_ID,
a.AccountID,
a.ACCT_NO,
IF(a.ACCT_NO_MASTER IS NULL, b.ACCT_NO, a.ACCT_NO_MASTER) AS ACCT_NO_MASTER,
a.CODE1,
a.CODE2
FROM kitsap_condosandparcel_1 a
LEFT JOIN kitsap_condos_mainparcel_2 b ON a.CODE2 = b.CODE2;

-- CREATE TEMPORARY TABLE general.kitsap_condosandparcels_missing
-- SELECT PARCEL_ID, AccountID, ACCT_NO, ACCT_NO_MASTER, CODE2
-- FROM kitsap_condosandparcel_2 WHERE PARCEL_ID IS NULL
-- GROUP BY CODE2;

-- ALTER TABLE general.kitsap_condosandparcels_missing ADD ID INT(10) unsigned NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY(ID);

-- Alter the missing table!!

CREATE INDEX condo2 USING BTREE ON general.kitsap_condosandparcels_missing (CODE2);

CREATE TEMPORARY TABLE kitsap_condosandparcel_3
SELECT
County,
IF(a.PARCEL_ID IS NULL, b.PARCEL_ID, a.PARCEL_ID) AS PARCEL_ID,
a.AccountID,
a.ACCT_NO,
IF(a.ACCT_NO_MASTER IS NULL, b.ACCT_NO_MASTER, a.ACCT_NO_MASTER) AS ACCT_NO_MASTER,
a.CODE1,
a.CODE2
FROM kitsap_condosandparcel_2 a
LEFT JOIN general.kitsap_condosandparcels_missing b ON a.CODE2 = b.CODE2;

-- CREATE TABLE general.kitsap_condo_2006
-- SELECT * FROM kitsap_condosandparcel_3;

-- Collate condo records - note that the source data may be processed by hand

CREATE TEMPORARY TABLE kitsap_condos_collate
SELECT
'035' AS County, 
CONCAT(PARCEL_ID) AS PARCEL_ID,
CONCAT(AccountID) AS AccountID,
1 AS SubparcelFlag
FROM general.kitsap_condo_2006;

-- Collect all records

CREATE TEMPORARY TABLE kitsap_subparcels
SELECT County, PARCEL_ID, AccountID, SubparcelFlag, CONCAT(County, AccountID) AS ID_SUBPARCEL FROM kitsap_mh
UNION
SELECT County, PARCEL_ID, AccountID, SubparcelFlag, CONCAT(County, AccountID) AS ID_SUBPARCEL FROM kitsap_condos_collate
UNION
SELECT County, PARCEL_ID, AccountID, SubparcelFlag, CONCAT(County, AccountID) AS ID_SUBPARCEL FROM kitsap_nocondo;

ALTER TABLE kitsap_subparcels
MODIFY COLUMN ID_SUBPARCEL VARCHAR(28) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL;

CREATE INDEX id_buildingsums USING BTREE ON kitsap_subparcels (ID_SUBPARCEL);

-- Assess number of buildings per subparcel

CREATE TEMPORARY TABLE kitsap_building_sums
SELECT ID_SUBPARCEL, SUM(BuildingFlag) AS NumberofBuildings, SUM(OutbuildingFlag) AS NumberofOutbuildings
FROM kitsap_buildings_2
GROUP BY ID_SUBPARCEL;

ALTER TABLE kitsap_building_sums
MODIFY COLUMN ID_SUBPARCEL VARCHAR(28) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL;

CREATE INDEX id_buildingsums USING BTREE ON kitsap_building_sums (ID_SUBPARCEL);

-- Merge building counts with subparcel data

CREATE TEMPORARY TABLE kitsap_subparcels_2
SELECT a.County, a.PARCEL_ID, a.AccountID, a.SubparcelFlag, IF(b.NumberofBuildings IS NULL,0, b.NumberofBuildings) AS NumberofBuildings, IF(b.NumberofOutbuildings IS NULL,0, b.NumberofOutbuildings) AS NumberofOutbuildings, a.ID_SUBPARCEL, CONCAT(a.County, a.PARCEL_ID) AS ID_PARCEL
FROM kitsap_subparcels a
LEFT JOIN kitsap_building_sums b ON a.ID_SUBPARCEL = b.ID_SUBPARCEL;

-- Assemble land and building values

CREATE TEMPORARY TABLE kitsap_values
SELECT a.* FROM
(SELECT f.RP_ACCT_ID, f.BLDG_VALUE, f.LAND_VALUE FROM kitsap_address_temp f ORDER BY RP_ACCT_ID, BLDG_VALUE desc) a
GROUP BY RP_ACCT_ID;

CREATE INDEX id_values USING BTREE ON kitsap_values (RP_ACCT_ID);

CREATE TEMPORARY TABLE kitsap_tax_status
SELECT RP_ACCT_ID, IF(TAX_STATUS = 'X', 1, 0) AS TaxExempt FROM kitsap_main_temp where ACCT_STAT = 'A' and TAX_YEAR = 2005 GROUP BY RP_ACCT_ID;

CREATE INDEX id_values USING BTREE ON kitsap_tax_status (RP_ACCT_ID);

CREATE TEMPORARY TABLE kitsap_subparcels_3
SELECT a.*, b.BLDG_VALUE AS ImprValue, b.LAND_VALUE AS LandValue
FROM kitsap_subparcels_2 a
LEFT JOIN kitsap_values b ON a.AccountID = b.RP_ACCT_ID;

CREATE TEMPORARY TABLE kitsap_subparcels_4
SELECT a.*, IF(b.TaxExempt IS NULL, 0, 1) AS TaxExempt
FROM kitsap_subparcels_3 a
LEFT JOIN kitsap_tax_status b ON a.AccountID = b.RP_ACCT_ID;

-- Add to final table

INSERT INTO all_subparcels
(County, PARCEL_ID, AccountID, SubparcelFlag, NumberofBuildings, NumberofOutbuildings, LandValue, ImprValue, TaxExempt, ID_SUBPARCEL, ID_PARCEL)
SELECT County, PARCEL_ID, AccountID, SubparcelFlag, NumberofBuildings, NumberofOutbuildings, LandValue, ImprValue, TaxExempt, ID_SUBPARCEL, ID_PARCEL 
FROM kitsap_subparcels_4;

--
-- Assembly of parcel data 
--

-- Assess jurisdiction

CREATE TEMPORARY TABLE kitsap_address
SELECT CONCAT(TRUNCATE(RP_ACCT_ID,0)) AS RP_ACCT_ID, JURISDICT AS Jurisdiction, LEFT(ACCT_NO,LOCATE('-',ACCT_NO)-1) AS PLAT_ID
FROM kitsap_address_temp a
GROUP BY a.RP_ACCT_ID;

CREATE INDEX id_address USING BTREE ON kitsap_address (RP_ACCT_ID);

-- Assess number of subparcels per parcel

CREATE TEMPORARY TABLE kitsap_parents
SELECT PARCEL_ID, COUNT(PARCEL_ID) AS Subparcels , IF(SUM(TaxExempt) > 0, 1, 0) AS TaxExemptParcel, SUM(LandValue) AS LandValueParcel, SUM(ImprValue) AS ImprValueParcel
FROM kitsap_subparcels_4
WHERE PARCEL_ID IS NOT NULL
GROUP BY PARCEL_ID;

CREATE INDEX id_parents USING BTREE ON kitsap_parents (PARCEL_ID);

-- Presort parcel data

CREATE TEMPORARY TABLE kitsap_parcel_presort
SELECT '035' AS County, CONCAT(TRUNCATE(l.RP_ACCT_ID,0)) AS PARCEL_ID, l.ACRES AS Size_Acres, (l.ACRES * 43560) AS Size_SF, l.PROP_CLASS AS Land_Use, l.ZONE_CODE as Zoning
FROM kitsap_land_temp l;

CREATE INDEX id_presort USING BTREE ON kitsap_parcel_presort (PARCEL_ID);

-- Assemble parcel data

CREATE TEMPORARY TABLE kitsap_parcel_presort_2
SELECT p.County, p.PARCEL_ID, a.PLAT_ID, a.Jurisdiction, p.Size_Acres, p.Size_SF, p.Land_Use, p.Zoning
FROM kitsap_parcel_presort p
LEFT JOIN kitsap_address a ON a.RP_ACCT_ID = p.PARCEL_ID;

CREATE INDEX id_presort2 USING BTREE ON kitsap_parcel_presort_2 (PARCEL_ID);

-- Add subparcel counts

CREATE TEMPORARY TABLE parcels_kitsap
SELECT p.County, p.PARCEL_ID, p.PLAT_ID, k.Subparcels AS NumberofAccounts, k.TaxExemptParcel, k.LandValueParcel, k.ImprValueParcel, p.Jurisdiction, p.Size_Acres, p.Size_SF, p.Land_Use, p.Zoning
FROM kitsap_parents k
LEFT JOIN kitsap_parcel_presort_2 p ON p.PARCEL_ID = k.PARCEL_ID
WHERE p.PARCEL_ID IS NOT NULL;

ALTER TABLE parcels_kitsap
MODIFY COLUMN County VARCHAR(5) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN PLAT_ID VARCHAR(10) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN Land_Use VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

CREATE INDEX id_code USING BTREE ON parcels_kitsap (County, Land_Use);

-- Add additional columns

CREATE TEMPORARY TABLE parcels_kitsap_2
SELECT a.County, a.PARCEL_ID, a.PLAT_ID, a.NumberofAccounts, a.TaxExemptParcel, a.LandValueParcel, a.ImprValueParcel, IF(a.Jurisdiction IS NULL, '', a.Jurisdiction) AS Jurisdiction, a.Size_Acres, a.Size_SF, a.Land_Use, a.Zoning, b.land_use_description AS LandUseDescription, b.generic_land_use_1 AS GenericLandUse1, b.generic_land_use_2 AS GenericLandUse2, b.res_nonres, CONCAT(a.County, a.PARCEL_ID) AS ID_PARCEL, CONCAT(a.County, a.PLAT_ID) AS ID_PLAT
FROM parcels_kitsap a
LEFT JOIN general.land_use_generic_reclass_2005 b ON (b.county = a.County AND b.county_land_use_code = a.Land_Use);

ALTER TABLE parcels_kitsap_2
MODIFY COLUMN Jurisdiction VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN LandUseDescription VARCHAR(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN GenericLandUse1 VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN GenericLandUse2 VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN res_nonres VARCHAR(10) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN ID_PARCEL VARCHAR(28) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN ID_PLAT VARCHAR(13) CHARACTER SET latin1 COLLATE latin1_swedish_ci;


-- Add to final table

INSERT INTO all_parcels
(County, PARCEL_ID, PLAT_ID, NumberofAccounts, LandValueParcel, ImprValueParcel, TaxExemptParcel, Jurisdiction, Size_Acres, Size_SF, Land_Use, Zoning, LandUseDescription, GenericLandUse1, GenericLandUse2, res_nonres, ID_PARCEL, ID_PLAT)
SELECT County, PARCEL_ID, PLAT_ID, NumberofAccounts, LandValueParcel, ImprValueParcel, TaxExemptParcel, Jurisdiction, Size_Acres, Size_SF, Land_Use, Zoning, LandUseDescription, GenericLandUse1, GenericLandUse2, res_nonres, ID_PARCEL, ID_PLAT
FROM parcels_kitsap_2;

--
-- Assembly of sales 
--

-- Collect initial variables

CREATE TEMPORARY TABLE sales_kitsap
SELECT '035' AS County, CONCAT(TRUNCATE(RP_ACCT_ID,0)) AS AccountID, EXCISE_NO AS ExciseTaxNumber, SALE_DATE AS SaleDate, PRICE AS SalePrice, 0 AS PPropPrice, '' AS BuyerName, '' AS SellerName, IF(DEED_TYPE IS NULL, '', DEED_TYPE) AS DeedType, IF(INVALID_CD IS NULL, '', INVALID_CD) AS SaleWarnings
FROM kitsap_sale_temp s
WHERE YEAR(SALE_DATE) > 1996;

CREATE INDEX id_excise USING BTREE ON sales_kitsap (ExciseTaxNumber);

-- Count number of accounts per sale

CREATE TEMPORARY TABLE sales_kitsap_counts
SELECT ExciseTaxNumber, COUNT(ExciseTaxNumber) AS NumberofAccounts FROM sales_kitsap GROUP BY ExciseTaxNumber;

CREATE INDEX id_excise USING BTREE ON sales_kitsap_counts (ExciseTaxNumber);

-- Join counts to main table

ALTER TABLE sales_kitsap
MODIFY COLUMN ExciseTaxNumber VARCHAR(25) NULL,
MODIFY COLUMN DeedType VARCHAR(50) NOT NULL DEFAULT '0',
MODIFY COLUMN SaleWarnings VARCHAR(50) NOT NULL DEFAULT '0';

CREATE TEMPORARY TABLE sales_kitsap_2
SELECT s.County, s.AccountID, s.ExciseTaxNumber, c.NumberofAccounts, s.SaleDate, s.SalePrice, s.PPropPrice, s.BuyerName, s.SellerName, s.DeedType, s.SaleWarnings
FROM sales_kitsap s
LEFT JOIN sales_kitsap_counts c ON c.ExciseTaxNumber = s.ExciseTaxNumber;

-- Add descriptions of sales instruments

CREATE TEMPORARY TABLE sales_kitsap_3
SELECT a.*, IF(i.InstrumentDescr IS NULL, '', i.InstrumentDescr) AS InstrumentDescr, IF(i.ValidInstrument IS NULL, '', i.ValidInstrument) AS ValidInstrument
FROM sales_kitsap_2 a
LEFT JOIN general.instrumenttypes i ON (a.County = i.County AND a.DeedType = i.InstrumentType);

ALTER TABLE sales_kitsap_3
MODIFY COLUMN DeedType VARCHAR(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0';

CREATE INDEX id_salewarnings USING BTREE ON sales_kitsap_3 (County, SaleWarnings);

-- Add descriptions of sales warnings

CREATE TEMPORARY TABLE sales_kitsap_4
SELECT a.*, IF(s.SWarnDescr IS NULL, '', s.SWarnDescr) AS SWarnDescr,
IF(s.ValidSale IS NULL, '0', s.ValidSale) AS ValidSale, CONCAT(a.County, a.AccountID) AS ID_SUBPARCEL,
CONCAT(a.County,a.ExciseTaxNumber,a.AccountID) AS ID_SALE
FROM sales_kitsap_3 a
LEFT JOIN general.salewarnings s ON (a.County = s.County AND a.SaleWarnings = s.SaleWarnings);

ALTER TABLE sales_kitsap_4
MODIFY COLUMN InstrumentDescr VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN ValidInstrument INT NOT NULL DEFAULT 0,
MODIFY COLUMN SWarnDescr VARCHAR(150) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN ValidSale INT NOT NULL DEFAULT 0;

-- Add to final table

INSERT INTO all_sales
(County, AccountID, ExciseTaxNumber, NumberofAccounts, SaleDate, SalePrice, PPropPrice, BuyerName, SellerName, DeedType, SaleWarnings, InstrumentDescr, ValidInstrument, SWarnDescr, ValidSale, ID_SUBPARCEL, ID_SALE)
SELECT County, AccountID, ExciseTaxNumber, NumberofAccounts, SaleDate, SalePrice, PPropPrice, BuyerName, SellerName, DeedType, SaleWarnings, InstrumentDescr, ValidInstrument, SWarnDescr, ValidSale, ID_SUBPARCEL, ID_SALE
FROM sales_kitsap_4;

FLUSH TABLES;

-- ----------------------------------------------------------------------




-- ----------------------------------------------------------------------
-- PIERCE COUNTY DATA 
-- ----------------------------------------------------------------------

--
-- Copy raw data to working directory 
--

FLUSH TABLES;
USE workspace;

CREATE TEMPORARY TABLE pierce_buildings_temp
SELECT * FROM pierce_20051115.improvement;

CREATE TEMPORARY TABLE pierce_account_temp
SELECT * FROM pierce_20051115.account;

CREATE TEMPORARY TABLE pierce_valuedetail_temp
SELECT * FROM pierce_20051115.valuedetail;

CREATE TEMPORARY TABLE pierce_sales_temp
SELECT * FROM pierce_20051115.sales;

CREATE TEMPORARY TABLE spatialdata
SELECT * FROM spatial.spatial_2005;

CREATE TEMPORARY TABLE pierce_value_temp
SELECT * FROM pierce_200603_gis.taxpar;

CREATE TEMPORARY TABLE building_type_pierce
SELECT * FROM general.building_type_reclass_2005 WHERE County = '053';

CREATE INDEX building_pierce USING BTREE ON building_type_pierce (building_use_code);

CREATE INDEX id_spatial USING BTREE ON spatialdata (ID_PARCEL);

--
-- Assembly of building data 
--

-- Collect all building data

CREATE TEMPORARY TABLE pierce_buildings
SELECT 
'053' AS County, 
AccountNo AS AccountID, 
BldgID AS BuildingID, 
IF(PropType = 'Out Building', 0, 1) AS BuildingFlag, 
IF(PropType = 'Out Building', 1, 0) AS OutbuildingFlag, 
OccCode AS BuildingUseCode, 
SF AS BldgSF, 
Stories, 
IF(i.SF IS NOT NULL AND i.Stories IS NOT NULL AND i.Stories <> 0, i.SF/i.Stories, NULL) AS Footprint,
YrBuilt AS YearBuilt, 
Quality AS BldgQuality, 
i.Condition AS BldgCondition, 
Units, 
Bedrooms, 
0 AS BathFull, 
0 AS Bath3Qtr, 
0 AS BathHalf, 
Baths AS Bathrooms 
FROM pierce_buildings_temp i;

-- Add additional columns

CREATE TEMPORARY TABLE pierce_buildings_2
SELECT
a.*,
IF((b.general_category <> 'Single Family Residential' AND b.general_category <> 'Multi-Family Residential' AND b.general_category <> 'Condo Residential' AND b.general_category <> 'Mobile Home'),0,IF(b.general_category = 'Condo Residential' OR b.general_category = 'Mobile Home' OR (a.Units = 0 AND a.Bedrooms > 0), 1, a.Units)) AS NumberofUnits,
b.building_use_description AS BuildingUseDescription,
b.general_category AS GeneralCategory,
b.general_category_code AS GeneralCategoryCode,
b.building_type AS BuildingType,
b.building_type_desc AS BuildingTypeDesc,
CONCAT(a.County,a.AccountID) AS ID_SUBPARCEL
FROM pierce_buildings  a
LEFT JOIN building_type_pierce b ON a.BuildingUseCode = b.building_use_code;

-- Ensure that data corresponds to common format

ALTER TABLE pierce_buildings_2
MODIFY COLUMN County VARCHAR(5) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
MODIFY COLUMN AccountID VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL, 
MODIFY COLUMN BuildingID VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL, 
MODIFY COLUMN BuildingFlag INTEGER UNSIGNED DEFAULT 0, 
MODIFY COLUMN OutbuildingFlag INTEGER UNSIGNED DEFAULT 0,
MODIFY COLUMN BuildingUseCode VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN BldgSF INTEGER(20),
MODIFY COLUMN Stories DOUBLE(5,2) NOT NULL DEFAULT 0,
MODIFY COLUMN Footprint INTEGER UNSIGNED DEFAULT 0,
MODIFY COLUMN YearBuilt INTEGER UNSIGNED DEFAULT 0,
MODIFY COLUMN BldgQuality VARCHAR(50) CHARACTER SET latin1 DEFAULT '0' COLLATE latin1_swedish_ci,
MODIFY COLUMN BldgCondition VARCHAR(50) CHARACTER SET latin1 DEFAULT '0' COLLATE latin1_swedish_ci,
MODIFY COLUMN NumberofUnits INT UNSIGNED DEFAULT 0,
MODIFY COLUMN Bedrooms INT UNSIGNED NOT NULL DEFAULT 0, 
MODIFY COLUMN BathFull INT UNSIGNED NOT NULL DEFAULT 0,
MODIFY COLUMN Bath3Qtr INT UNSIGNED NOT NULL DEFAULT 0,
MODIFY COLUMN BathHalf INT UNSIGNED NOT NULL DEFAULT 0,
MODIFY COLUMN Bathrooms DOUBLE(5,2) DEFAULT 0,
MODIFY COLUMN BuildingUseDescription VARCHAR(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN GeneralCategory VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN GeneralCategoryCode INT(5) NOT NULL DEFAULT 0, 
MODIFY COLUMN BuildingType INT(1) NOT NULL DEFAULT 0, 
MODIFY COLUMN BuildingTypeDesc VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN ID_SUBPARCEL VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

-- Add to final table

INSERT INTO all_buildings 
(County, AccountID, BuildingID, BuildingFlag, OutbuildingFlag, BuildingUseCode, BldgSF, Stories, Footprint, YearBuilt, BldgQuality, BldgCondition, NumberofUnits, Bedrooms, BathFull, Bath3Qtr, BathHalf, Bathrooms, BuildingUseDescription, GeneralCategory, GeneralCategoryCode, BuildingType, BuildingTypeDesc, ID_SUBPARCEL) 
SELECT County, AccountID, BuildingID, BuildingFlag, OutbuildingFlag, BuildingUseCode, BldgSF, Stories, Footprint, YearBuilt, BldgQuality, BldgCondition, NumberofUnits, Bedrooms, BathFull, Bath3Qtr, BathHalf, Bathrooms, BuildingUseDescription, GeneralCategory, GeneralCategoryCode, BuildingType, BuildingTypeDesc, ID_SUBPARCEL FROM pierce_buildings_2;

--
-- Assembly of subparcel data
--

-- -----------------
-- Leaseholds / mobile homes have inconsistent Parcel / Account Numbers.  Query formed where 
-- AccountNo, ParcelNB not equal.  Other subparcels obtained from GIS shapefile:  condos located 
-- with circles on reference parcels (pierce_condos_2005).  
-- -----------------

-- Extract mobile homes from Pierce data

CREATE TEMPORARY TABLE pierce_mh
SELECT
'053' AS County,
ParcelNB AS PARCEL_ID,
AccountNo AS AccountID,
1 AS SubparcelFlag
FROM pierce_account_temp a WHERE AccountNo <> ParcelNB;

-- Extract condos from Pierce data (note that this must be done with GIS shapefiles)

-- Select parcels with AREA = 78.35938, export features
-- Select parcels without AREA = 78.35938, export features
-- Plot centroids for condo units
-- Spatial join to nearest noncondo parcel
-- Check distance to nearest parcel (should be ~4.949747)

CREATE TEMPORARY TABLE pierce_condos_sort
SELECT
'053' AS County,
c.PARCEL_ID,
c.ACCOUNT_ID AS AccountID,
1 AS SubparcelFlag
FROM general.pierce_condos_2005 c;

CREATE INDEX id_condo USING BTREE ON pierce_condos_sort (AccountID);

-- Collate non-MH parcels

CREATE TEMPORARY TABLE pierce_subparcel_presort
SELECT 
'053' AS County, 
ParcelNB AS PARCEL_ID, 
AccountNo AS AccountID
FROM pierce_account_temp a WHERE AccountNo = ParcelNB;

CREATE INDEX id_parc USING BTREE ON pierce_subparcel_presort (PARCEL_ID);

-- Identify main parcels

CREATE TEMPORARY TABLE pierce_mainparcels
SELECT
a.County,
a.PARCEL_ID,
a.AccountID,
0 AS SubparcelFlag
FROM pierce_subparcel_presort a
LEFT JOIN pierce_condos_sort b ON a.PARCEL_ID = b.AccountID
WHERE b.AccountID IS NULL;

-- Collect all subparcels

CREATE TEMPORARY TABLE pierce_subparcels
SELECT County, PARCEL_ID, AccountID, SubparcelFlag, CONCAT(County, AccountID) AS ID_SUBPARCEL  FROM pierce_mh
UNION
SELECT County, PARCEL_ID, AccountID, SubparcelFlag, CONCAT(County, AccountID) AS ID_SUBPARCEL  FROM pierce_condos_sort
UNION
SELECT County, PARCEL_ID, AccountID, SubparcelFlag, CONCAT(County, AccountID) AS ID_SUBPARCEL  FROM pierce_mainparcels;

ALTER TABLE pierce_subparcels
MODIFY COLUMN ID_SUBPARCEL VARCHAR(28) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL;

-- Assess number of buildings per subparcel

CREATE TEMPORARY TABLE pierce_building_sums
SELECT ID_SUBPARCEL, SUM(BuildingFlag) AS NumberofBuildings, SUM(OutbuildingFlag) AS NumberofOutbuildings
FROM pierce_buildings_2
GROUP BY ID_SUBPARCEL;

ALTER TABLE pierce_building_sums
MODIFY COLUMN ID_SUBPARCEL VARCHAR(28) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL;

CREATE INDEX id_buildingsums USING BTREE ON pierce_building_sums (ID_SUBPARCEL);

-- Merge building counts with subparcel data

CREATE TEMPORARY TABLE pierce_subparcels_2
SELECT a.County, a.PARCEL_ID, a.AccountID, a.SubparcelFlag, IF(b.NumberofBuildings IS NULL,0, b.NumberofBuildings) AS NumberofBuildings, IF(b.NumberofOutbuildings IS NULL,0, b.NumberofOutbuildings) AS NumberofOutbuildings, a.ID_SUBPARCEL, CONCAT(a.County, a.PARCEL_ID) AS ID_PARCEL
FROM pierce_subparcels a
LEFT JOIN pierce_building_sums b ON a.ID_SUBPARCEL = b.ID_SUBPARCEL;

-- Assemble land and building values

CREATE TEMPORARY TABLE pierce_values
SELECT f.TAX_PARCEL, f.IMPR_VALUE, f.LAND_VALUE, f.EXEMPT_CD FROM pierce_value_temp f ORDER BY TAX_PARCEL;

CREATE INDEX id_values USING BTREE ON pierce_values (TAX_PARCEL);

CREATE TEMPORARY TABLE pierce_subparcels_3
SELECT a.*, IF(b.IMPR_VALUE IS NULL, 0, b.IMPR_VALUE) AS ImprValue, IF(b.LAND_VALUE IS NULL, 0, LAND_VALUE) AS LandValue, IF(b.EXEMPT_CD IS NULL, 0, 1) AS TaxExempt
FROM pierce_subparcels_2 a
LEFT JOIN pierce_values b ON a.AccountID = b.TAX_PARCEL;

-- Add to final table

INSERT INTO all_subparcels
(County, PARCEL_ID, AccountID, SubparcelFlag, NumberofBuildings, NumberofOutbuildings, LandValue, ImprValue, TaxExempt, ID_SUBPARCEL, ID_PARCEL)
SELECT County, PARCEL_ID, AccountID, SubparcelFlag, NumberofBuildings, NumberofOutbuildings, LandValue, ImprValue, TaxExempt, ID_SUBPARCEL, ID_PARCEL FROM pierce_subparcels_3;

--
-- Assembly of parcel data
--

-- Assess land use

CREATE TEMPORARY TABLE pierce_landuse_presort
SELECT '053' AS County, ParcelNB AS PARCEL_ID, SUBSTRING(AbstCode,1,4) AS AbstCode, SqFt
FROM pierce_valuedetail_temp
WHERE AccountNo = ParcelNB AND Status = 'A'
ORDER BY ParcelNB, SqFt DESC;

CREATE TEMPORARY TABLE pierce_landuse
SELECT a.*, SUM(SqFt) AS TotalSqFt
FROM pierce_landuse_presort a
GROUP BY PARCEL_ID
ORDER BY PARCEL_ID, SqFt DESC;

ALTER TABLE pierce_landuse
MODIFY COLUMN County VARCHAR(3) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN PARCEL_ID VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

CREATE INDEX parcel USING BTREE ON pierce_landuse (PARCEL_ID);

-- Assess number of subparcels per parcel

CREATE TEMPORARY TABLE pierce_parents
SELECT PARCEL_ID, COUNT(PARCEL_ID) AS Subparcels, IF(SUM(TaxExempt) > 0, 1, 0) AS TaxExemptParcel, SUM(LandValue) AS LandValueParcel, SUM(ImprValue) AS ImprValueParcel
FROM pierce_subparcels_3
WHERE PARCEL_ID IS NOT NULL
GROUP BY PARCEL_ID;

ALTER TABLE pierce_parents
MODIFY COLUMN PARCEL_ID VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

CREATE INDEX id_parents USING BTREE ON pierce_parents (PARCEL_ID);

-- Presort parcel data

CREATE TEMPORARY TABLE pierce_parcel_presort
SELECT '053' AS County, a.ParcelNB AS PARCEL_ID, a.LocationCity AS Jurisdiction, a.Zoning
FROM pierce_account_temp a
WHERE a.ParcelNB = a.AccountNo;

CREATE INDEX id_presort USING BTREE ON pierce_parcel_presort (PARCEL_ID);

ALTER TABLE pierce_parcel_presort
MODIFY COLUMN PARCEL_ID VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

-- Include land use and area

CREATE TEMPORARY TABLE pierce_parcel_presort_2
SELECT a.*, b.AbstCode AS Land_Use, b.TotalSqFt AS Size_SF, (b.TotalSqFt / 43560) AS Size_Acres
FROM pierce_parcel_presort a
LEFT JOIN pierce_landuse b ON a.PARCEL_ID = b.PARCEL_ID;

CREATE INDEX parcel USING BTREE ON pierce_parcel_presort_2 (PARCEL_ID);

-- Assemble parcel data and subparcel counts

CREATE TEMPORARY TABLE parcels_pierce
SELECT p.County, p.PARCEL_ID, k.Subparcels AS NumberofAccounts, k.TaxExemptParcel, k.LandValueParcel, k.ImprValueParcel, p.Jurisdiction, p.Size_Acres, p.Size_SF, p.Land_Use, p.Zoning
FROM pierce_parents k
LEFT JOIN pierce_parcel_presort_2 p ON p.PARCEL_ID = k.PARCEL_ID
WHERE p.PARCEL_ID IS NOT NULL;

ALTER TABLE parcels_pierce
MODIFY COLUMN County VARCHAR(5) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN Land_Use VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

CREATE INDEX id_code USING BTREE ON parcels_pierce (County, Land_Use);

-- Add additional columns

CREATE TEMPORARY TABLE parcels_pierce_2
SELECT a.County, a.PARCEL_ID, LEFT(a.PARCEL_ID,6) AS PLAT_ID, a.NumberofAccounts, a.TaxExemptParcel, a.LandValueParcel, a.ImprValueParcel, IF(a.Jurisdiction IS NULL, '', a.Jurisdiction) as Jurisdiction, a.Size_Acres, a.Size_SF, a.Land_Use, IF(a.Zoning IS NULL, '', a.Zoning) AS Zoning, IF(b.land_use_description IS NULL, '', b.land_use_description) AS LandUseDescription, IF(b.generic_land_use_1 IS NULL, '', b.generic_land_use_1) AS GenericLandUse1, IF(b.generic_land_use_2 IS NULL, '', b.generic_land_use_2) AS GenericLandUse2, IF(b.res_nonres IS NULL, '', b.res_nonres) AS res_nonres, CONCAT(a.County, a.PARCEL_ID) AS ID_PARCEL, CONCAT(a.County, LEFT(a.PARCEL_ID,6)) AS ID_PLAT
FROM parcels_pierce a
LEFT JOIN general.land_use_generic_reclass_2005 b ON (b.county = a.County AND b.county_land_use_code = a.Land_Use);

ALTER TABLE parcels_pierce_2
MODIFY COLUMN PLAT_ID VARCHAR(10) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN Jurisdiction VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN LandUseDescription VARCHAR(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN GenericLandUse1 VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN GenericLandUse2 VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN res_nonres VARCHAR(10) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN ID_PARCEL VARCHAR(28) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN ID_PLAT VARCHAR(13) CHARACTER SET latin1 COLLATE latin1_swedish_ci;


-- Add to final table

INSERT INTO all_parcels
(County, PARCEL_ID, PLAT_ID, NumberofAccounts, LandValueParcel, ImprValueParcel, TaxExemptParcel, Jurisdiction, Size_Acres, Size_SF, Land_Use, Zoning, LandUseDescription, GenericLandUse1, GenericLandUse2, res_nonres, ID_PARCEL, ID_PLAT)
SELECT County, PARCEL_ID, PLAT_ID, NumberofAccounts, LandValueParcel, ImprValueParcel, TaxExemptParcel, Jurisdiction, Size_Acres, Size_SF, Land_Use, Zoning, LandUseDescription, GenericLandUse1, GenericLandUse2, res_nonres, ID_PARCEL, ID_PLAT
FROM parcels_pierce_2;

--
-- Assembly of sales data
--

-- Collect initial variables

CREATE TEMPORARY TABLE sales_pierce
SELECT '053' AS County, AccountNo AS AccountID, RecptNo AS ExciseTaxNumber, SaleDate, SalePrice, 0 AS PPropPrice, Grantee AS BuyerName, Grantor AS SellerName, IF(DeedType IS NULL, '', DeedType) as DeedType, IF(ExcludeReason IS NULL, '', ExcludeReason) AS SaleWarnings
FROM pierce_sales_temp a;

ALTER TABLE sales_pierce
MODIFY COLUMN ExciseTaxNumber VARCHAR(25) NULL,
MODIFY COLUMN DeedType VARCHAR(50) NOT NULL DEFAULT '0',
MODIFY COLUMN SaleWarnings VARCHAR(50) NOT NULL DEFAULT '0';

CREATE INDEX id_excise USING BTREE ON sales_pierce (ExciseTaxNumber);

-- Count number of accounts per sale

CREATE TEMPORARY TABLE sales_pierce_counts
SELECT ExciseTaxNumber, COUNT(ExciseTaxNumber) AS NumberofAccounts FROM sales_pierce GROUP BY ExciseTaxNumber;

CREATE INDEX id_excise USING BTREE ON sales_pierce_counts (ExciseTaxNumber);

-- Join counts to main table

CREATE TEMPORARY TABLE sales_pierce_2
SELECT s.County, s.AccountID, s.ExciseTaxNumber, c.NumberofAccounts, s.SaleDate, s.SalePrice, s.PPropPrice, s.BuyerName, s.SellerName, s.DeedType, s.SaleWarnings
FROM sales_pierce s
LEFT JOIN sales_pierce_counts c ON c.ExciseTaxNumber = s.ExciseTaxNumber;

-- Add descriptions of sales instruments

CREATE TEMPORARY TABLE sales_pierce_3
SELECT a.*, IF(i.InstrumentDescr IS NULL, '', i.InstrumentDescr) AS InstrumentDescr, IF(i.ValidInstrument IS NULL, 0 ,i.ValidInstrument) AS ValidInstrument
FROM sales_pierce_2 a
LEFT JOIN general.instrumenttypes i ON (a.County = i.County AND a.DeedType = i.InstrumentType);

ALTER TABLE sales_pierce_3
MODIFY COLUMN DeedType VARCHAR(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0';

CREATE INDEX id_salewarnings USING BTREE ON sales_pierce_3 (County, SaleWarnings);

-- Add descriptions of sales warnings

CREATE TEMPORARY TABLE sales_pierce_4
SELECT a.*, IF(s.SWarnDescr IS NULL, '', s.SWarnDescr) AS SWarnDescr,
IF(s.ValidSale IS NULL, 1, s.ValidSale) AS ValidSale, CONCAT(a.County, a.AccountID) AS ID_SUBPARCEL,
CONCAT(a.County,a.ExciseTaxNumber,a.AccountID) AS ID_SALE
FROM sales_pierce_3 a
LEFT JOIN general.salewarnings s ON (a.County = s.County AND a.SaleWarnings = s.SaleWarnings);

ALTER TABLE sales_pierce_4
MODIFY COLUMN InstrumentDescr VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN ValidInstrument INT NOT NULL DEFAULT 0,
MODIFY COLUMN SWarnDescr VARCHAR(150) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN ValidSale INT NOT NULL DEFAULT 0;

-- Add to final table

INSERT INTO all_sales
(County, AccountID, ExciseTaxNumber, NumberofAccounts, SaleDate, SalePrice, PPropPrice, BuyerName, SellerName, DeedType, SaleWarnings, InstrumentDescr, ValidInstrument, SWarnDescr, ValidSale, ID_SUBPARCEL, ID_SALE)
SELECT County, AccountID, ExciseTaxNumber, NumberofAccounts, SaleDate, SalePrice, PPropPrice, BuyerName, SellerName, DeedType, SaleWarnings, InstrumentDescr, ValidInstrument, SWarnDescr, ValidSale, ID_SUBPARCEL, ID_SALE
FROM sales_pierce_4;

FLUSH TABLES;

-- ----------------------------------------------------------------------





-- ----------------------------------------------------------------------
-- SNOHOMISH COUNTY
-- ----------------------------------------------------------------------

--
-- Copy raw data to working directory 
--

FLUSH TABLES;
USE workspace;

CREATE TEMPORARY TABLE snohomish_buildings_temp
SELECT * FROM snohomish_20060101.improvementrecord;

CREATE TEMPORARY TABLE snohomish_masterrecord_temp
SELECT * FROM snohomish_20060101.masterrecord;

CREATE TEMPORARY TABLE snohomish_commfloors_temp
SELECT * FROM snohco_data_2006.tblcommfloors;

CREATE TEMPORARY TABLE snohomish_parcelbase_temp
SELECT * FROM snohco_data_2006.tblparcel_base t order by lrsn;

CREATE TEMPORARY TABLE snohomish_sales_temp
SELECT * FROM snohco_data_2006.allsales;

CREATE TEMPORARY TABLE snohomish_value_temp
SELECT * FROM snohomish_20060331.maindata; 

CREATE TEMPORARY TABLE snohomish_exemptions_temp
SELECT * FROM snohomish_20060331.exemptions; 

CREATE TEMPORARY TABLE spatialdata
SELECT * FROM spatial.spatial_2005;

CREATE TEMPORARY TABLE snohomish_city_1
SELECT PARCEL_NUM AS PARCEL_ID, IF(SITUSCITY = 'UNKNOWN', NULL, SITUSCITY) AS CITY, LEFT(USECODE,3) AS USECODE FROM snohomish_20060331.maindata m
GROUP BY PARCEL_NUM;

CREATE TEMPORARY TABLE snohomish_city_2
SELECT PARCEL_ID, CITY, USECODE FROM snohomish_20050923.masterrecord m
GROUP BY PARCEL_ID;

CREATE TEMPORARY TABLE building_type_snohomish
SELECT * FROM general.building_type_reclass_2005 WHERE County = '061';

CREATE INDEX building_snohomish USING BTREE ON building_type_snohomish (building_use_code);

CREATE INDEX id_parcel USING BTREE ON snohomish_city_1 (PARCEL_ID); 
CREATE INDEX id_parcel USING BTREE ON snohomish_city_2 (PARCEL_ID);

CREATE INDEX id_spatial USING BTREE ON spatialdata (ID_PARCEL);

CREATE INDEX id_parcel USING BTREE ON snohomish_parcelbase_temp (PARCEL_ID);
CREATE INDEX id_lrsn USING BTREE ON snohomish_parcelbase_temp (lrsn);

CREATE INDEX id_parcel USING BTREE ON snohomish_value_temp (PARCEL_NUM);

CREATE INDEX id_parcel USING BTREE ON snohomish_exemptions_temp (PARCEL_NUM);

CREATE INDEX id_parcel USING BTREE ON snohomish_20060331.maindata (PARCEL_NUM);

--
-- Assembly of building data 
--

-- Organize main data

CREATE TEMPORARY TABLE snohomish_buildings_presort
SELECT 
'061' AS County, 
PARCEL_ID AS AccountID, 
REC_TYPE AS BuildingID, 
IMP_TYPE, 
ST_USECODE AS BuildingUseCode, 
BLDG_SQFT AS BldgSF, 
ROUND(STORIES,2) AS Stories, 
YRBUILT AS YearBuilt, 
Quality AS BldgQuality, 
COND_CODE AS BldgCondition, 
NUM_BDRMS AS Bedrooms, 
NUM_FBATH AS BathFull, 
0 AS Bath3Qtr,
NUM_HBATH AS BathHalf, 
(0.5 * NUM_HBATH + NUM_FBATH) AS Bathrooms
FROM snohomish_buildings_temp i
GROUP BY PARCEL_ID, REC_TYPE;

CREATE INDEX id_buildings USING BTREE ON snohomish_buildings_presort (AccountID, BuildingID);

-- Attach commercial data from special extract

CREATE TEMPORARY TABLE snohomish_commercialSF_temp
SELECT lrsn, extension, SUM(base_area) AS base_area
FROM snohomish_commfloors_temp a
WHERE lrsn <> 0 AND lrsn <> 1 AND lrsn IS NOT NULL
GROUP BY lrsn, extension;

CREATE TEMPORARY TABLE snohomish_buildings_addendum
SELECT a.parcel_id, t.lrsn, t.extension, t.base_area AS BldgSF 
FROM snohomish_commercialSF_temp t 
LEFT JOIN snohomish_parcelbase_temp a ON a.lrsn = t.lrsn;

CREATE INDEX building USING BTREE ON snohomish_buildings_addendum (parcel_id, extension);

CREATE TEMPORARY TABLE snohomish_buildings_presort2
SELECT
a.County,
a.AccountID,
a.BuildingID,
IF(a.IMP_TYPE = 'OTHER', 0, 1) AS BuildingFlag,
IF(a.IMP_TYPE = 'OTHER', 1, 0) AS OutbuildingFlag,
a.BuildingUseCode,
IF(a.BldgSF IS NULL, b.BldgSF, a.BldgSF) AS BldgSF,
a.Stories,
IF(a.YearBuilt IS NULL, 0, a.YearBuilt) AS YearBuilt,
a.BldgQuality,
a.BldgCondition,
IF(a.Bedrooms IS NULL,0,a.Bedrooms) AS Bedrooms,
IF(a.BathFull IS NULL,0,a.BathFull) AS BathFull,
IF(a.Bath3Qtr IS NULL,0,a.Bath3Qtr) AS Bath3Qtr,
IF(a.BathHalf IS NULL,0,a.BathHalf) AS BathHalf,
IF(a.Bathrooms IS NULL,0,a.Bathrooms) AS Bathrooms
FROM snohomish_buildings_presort a
LEFT JOIN snohomish_buildings_addendum b ON a.AccountID = b.parcel_id AND a.BuildingID = b.extension;

-- Final calculation

CREATE TEMPORARY TABLE snohomish_buildings
SELECT County, AccountID, BuildingID, BuildingFlag, OutbuildingFlag, BuildingUseCode, BldgSF, Stories, IF(BldgSF IS NOT NULL AND Stories IS NOT NULL, BldgSF/Stories, 0) AS Footprint, YearBuilt, BldgQuality, BldgCondition, Bedrooms, BathFull, Bath3Qtr, BathHalf, Bathrooms
FROM snohomish_buildings_presort2 a;

-- Add additional columns

CREATE TABLE snohomish_buildings_2
SELECT
a.*,
b.building_use_description AS BuildingUseDescription, 
b.general_category AS GeneralCategory, 
b.general_category_code AS GeneralCategoryCode,
b.building_type AS BuildingType, 
b.building_type_desc AS BuildingTypeDesc,
     b.housing_units_snohomish AS NumberofUnits,
CONCAT(a.County,a.AccountID) AS ID_SUBPARCEL
FROM snohomish_buildings a
LEFT JOIN building_type_snohomish b ON a.BuildingUseCode = b.building_use_code;

-- Ensure that data corresponds to common format

ALTER TABLE snohomish_buildings_2
MODIFY COLUMN County VARCHAR(5) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
MODIFY COLUMN AccountID VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL, 
MODIFY COLUMN BuildingID VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL, 
MODIFY COLUMN BuildingFlag INTEGER UNSIGNED DEFAULT 0,
MODIFY COLUMN OutbuildingFlag INTEGER UNSIGNED DEFAULT 0, 
MODIFY COLUMN BuildingUseCode VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN BldgSF INTEGER DEFAULT 0,
MODIFY COLUMN Stories DOUBLE(5,2),
MODIFY COLUMN Footprint INTEGER, 
MODIFY COLUMN YearBuilt INTEGER UNSIGNED DEFAULT 0,
MODIFY COLUMN BldgQuality VARCHAR(50) CHARACTER SET latin1 DEFAULT '0' COLLATE latin1_swedish_ci,
MODIFY COLUMN BldgCondition VARCHAR(50) CHARACTER SET latin1 DEFAULT '0' COLLATE latin1_swedish_ci,
MODIFY COLUMN NumberofUnits INT UNSIGNED DEFAULT 0,
MODIFY COLUMN Bedrooms INT UNSIGNED DEFAULT 0,
MODIFY COLUMN BathFull INT UNSIGNED DEFAULT 0,
MODIFY COLUMN Bath3Qtr INT UNSIGNED DEFAULT 0, 
MODIFY COLUMN BathHalf INT UNSIGNED DEFAULT 0,
MODIFY COLUMN Bathrooms DOUBLE(5,2) DEFAULT 0,
MODIFY COLUMN BuildingUseDescription VARCHAR(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN GeneralCategory VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN GeneralCategoryCode INT(5) NOT NULL DEFAULT 0, 
MODIFY COLUMN BuildingType INT(1) NOT NULL DEFAULT 0, 
MODIFY COLUMN BuildingTypeDesc VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN ID_SUBPARCEL VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

-- Add to final table

INSERT INTO all_buildings 
(County, AccountID, BuildingID, BuildingFlag, OutbuildingFlag, BuildingUseCode, BldgSF, Stories, Footprint, YearBuilt, BldgQuality, BldgCondition, NumberofUnits, Bedrooms, BathFull, Bath3Qtr, BathHalf, Bathrooms, BuildingUseDescription, GeneralCategory, GeneralCategoryCode, BuildingType, BuildingTypeDesc, ID_SUBPARCEL) 
SELECT County, AccountID, BuildingID, BuildingFlag, OutbuildingFlag, BuildingUseCode, BldgSF, Stories, Footprint, YearBuilt, BldgQuality, BldgCondition, NumberofUnits, Bedrooms, BathFull, Bath3Qtr, BathHalf, Bathrooms, BuildingUseDescription, GeneralCategory, GeneralCategoryCode, BuildingType, BuildingTypeDesc, ID_SUBPARCEL FROM snohomish_buildings_2;


--
-- Assembly of subparcel data 
--

-- -------------------------------------------
-- -------------------------------------------
-- -------------------------------------------

-- Note that subparcels are layered in parcel GIS layer, must be extracted.  
-- Import allparcels shapefile table into SQL

-- Identify unique parcels within database

CREATE TEMPORARY TABLE snohomish_allparcels_id
SELECT PARCEL_ID FROM snohomish_masterrecord_temp m WHERE PARCEL_ID IS NOT NULL GROUP BY PARCEL_ID;
CREATE INDEX allparcels USING BTREE ON snohomish_allparcels_id (PARCEL_ID);

-- Identify unique parcels in both database and shapefiles

CREATE TEMPORARY TABLE snohomish_parcels_existing
SELECT a.* FROM allparc a
LEFT JOIN snohomish_allparcels_id b ON a.PARCEL_ID = b.PARCEL_ID WHERE a.PARCEL_ID IS NOT NULL AND b.PARCEL_ID IS NOT NULL;

-- Separate parcels with only one object within shapefile

CREATE TEMPORARY TABLE snohomish_parcels_singleentry
SELECT PARCEL_ID FROM snohomish_parcels_existing GROUP BY PARCEL_ID HAVING COUNT(*) = 1;

CREATE INDEX id USING BTREE ON snohomish_parcels_singleentry (PARCEL_ID);

CREATE TABLE snohomish_parcels_singleentry_records
SELECT a.* FROM allparc a
LEFT JOIN snohomish_parcels_singleentry b ON a.PARCEL_ID = b.PARCEL_ID WHERE a.PARCEL_ID IS NOT NULL AND b.PARCEL_ID IS NOT NULL;

-- Identify multiple incidences of parcels in shapefile

CREATE TEMPORARY TABLE snohomish_parcels_multipleentry
SELECT PARCEL_ID FROM snohomish_parcels_existing GROUP BY PARCEL_ID HAVING COUNT(*) > 1;

CREATE INDEX id USING BTREE ON snohomish_parcels_multipleentry (PARCEL_ID);

CREATE TEMPORARY TABLE snohomish_parcels_multipleentry_records
SELECT a.* FROM allparc a
LEFT JOIN snohomish_parcels_multipleentry b ON a.PARCEL_ID = b.PARCEL_ID WHERE a.PARCEL_ID IS NOT NULL AND b.PARCEL_ID IS NOT NULL;

-- FILTER:  Cases where only one parcel has valid create / delete date values

CREATE TABLE snohomish_parcels_multipleentry_records_filtered1
SELECT * FROM snohomish_parcels_multipleentry_records
WHERE CREATEDATE <= date '2006-01-01' AND (DELETEDATE = date '1850-01-01' OR DELETEDATE > date '2006-01-01')
GROUP BY PARCEL_ID HAVING COUNT(*) = 1;

CREATE TEMPORARY TABLE snohomish_parcels_multipleentry_records_remove1
SELECT PARCEL_ID FROM snohomish_parcels_multipleentry_records_filtered1;

CREATE INDEX parcel USING BTREE ON snohomish_parcels_multipleentry_records_remove1 (PARCEL_ID);

CREATE TEMPORARY TABLE snohomish_parcels_multipleentry_records_remaining1
SELECT a.* FROM snohomish_parcels_multipleentry_records a
LEFT JOIN snohomish_parcels_multipleentry_records_remove1 b ON a.PARCEL_ID = b.PARCEL_ID
WHERE b.PARCEL_ID IS NULL;

-- FILTER:  Obtain parcel records where at least one parcel has not been deleted, latest create date?

CREATE TEMPORARY TABLE snohomish_parcels_multipleentry_records_filter2
SELECT PARCEL_ID FROM snohomish_parcels_multipleentry_records_remaining1 WHERE DELETEDATE = date '1850-01-01'
GROUP BY PARCEL_ID;
CREATE INDEX parcel USING BTREE ON snohomish_parcels_multipleentry_records_filter2 (PARCEL_ID);

CREATE TABLE snohomish_parcels_multipleentry_records_filtered2
SELECT x.* FROM (SELECT a.* FROM snohomish_parcels_multipleentry_records_remaining1 a
LEFT JOIN snohomish_parcels_multipleentry_records_filter2 b ON a.PARCEL_ID = b.PARCEL_ID
WHERE b.PARCEL_ID IS NULL
ORDER BY CREATEDATE desc) x
GROUP BY PARCEL_ID;

CREATE TEMPORARY TABLE snohomish_parcels_multipleentry_records_remove2
SELECT PARCEL_ID FROM snohomish_parcels_multipleentry_records_filtered2;
CREATE INDEX parcel USING BTREE ON snohomish_parcels_multipleentry_records_remove2 (PARCEL_ID);
 
CREATE TEMPORARY TABLE snohomish_parcels_multipleentry_records_remaining2
SELECT a.* FROM snohomish_parcels_multipleentry_records_remaining1 a
LEFT JOIN snohomish_parcels_multipleentry_records_remove2 b ON a.PARCEL_ID = b.PARCEL_ID
WHERE b.PARCEL_ID IS NULL;

-- FILTER:  Remaining - just delete invalid delete dates

CREATE TABLE snohomish_parcels_multipleentry_records_filtered3
SELECT * FROM snohomish_parcels_multipleentry_records_remaining2 a
WHERE (DELETEDATE = date '1850-01-01' OR DELETEDATE > date '2006-01-01');

-- Assemble data from the filtering phases

CREATE TEMPORARY TABLE snohomish_parcels_sorted
SELECT a.* FROM snohomish_parcels_singleentry_records a
UNION
SELECT b.* FROM snohomish_parcels_multipleentry_records_filtered1 b
UNION
SELECT c.* FROM snohomish_parcels_multipleentry_records_filtered2 c
UNION 
SELECT d.* FROM snohomish_parcels_multipleentry_records_filtered3 d;

DROP TABLE snohomish_parcels_singleentry_records;
DROP TABLE snohomish_parcels_multipleentry_records_filtered1;
DROP TABLE snohomish_parcels_multipleentry_records_filtered2;
DROP TABLE snohomish_parcels_multipleentry_records_filtered3;

-- Separate mobile homes from subparcel list

CREATE TABLE snohomish_parcels_MH
SELECT * FROM snohomish_parcels_sorted WHERE LEFT(PARCEL_ID,4) = '0096';

CREATE TABLE snohomish_parcels_nonMH
SELECT * FROM snohomish_parcels_sorted WHERE LEFT(PARCEL_ID,4) <> '0096';

-- Find coincident parcels (index by centroids, area), assign tag to first in numerical order

CREATE TEMPORARY TABLE snohomish_parcels_multiplelayers
SELECT x.PARCEL_ID, x.AREA, x.x_coord, x.y_coord 
FROM (SELECT a.* FROM snohomish_parcels_nonMH a ORDER BY PARCEL_ID) x 
GROUP BY AREA, x_coord, y_coord HAVING COUNT(*) > 1;

CREATE INDEX parcelmatch USING BTREE ON snohomish_parcels_multiplelayers (AREA, x_coord, y_coord);

-- Assemble preliminary base parcel layer

CREATE TABLE snohomish_base
SELECT a.* FROM snohomish_parcels_nonMH a
LEFT JOIN snohomish_parcels_multiplelayers b ON a.AREA = b.AREA AND a.x_coord = b.x_coord AND a.y_coord = b.y_coord
WHERE b.PARCEL_ID IS NULL OR a.PARCEL_ID = b.PARCEL_ID; 

CREATE TABLE snobase
SELECT TRUNCATE(TAXACCT_,0) AS TAXACCT_ FROM snohomish_base;
 
-- ArcGIS: export snobase to ArcGIS, index, obtain intersections for subparcel files, reimport into MySQL

DROP TABLE snobase;

CREATE TABLE snohomish_deletefrombase
SELECT * FROM snoint WHERE DELETEDATE < '2006-01-01' AND DELETEDATE <> '1850-01-01' GROUP BY PARCEL_ID;
CREATE INDEX deleteparcel USING BTREE ON snohomish_deletefrombase (PARCEL_ID);

-- DROP TABLE snoint;

CREATE TABLE snohomish_base_2
SELECT a.* FROM snohomish_base a
LEFT JOIN snohomish_deletefrombase b ON a.PARCEL_ID = b.PARCEL_ID WHERE b.PARCEL_ID IS NULL;

DROP TABLE snohomish_base;

CREATE INDEX baseparcel USING BTREE ON snohomish_base_2 (x_coord, y_coord, AREA);

CREATE TABLE snobase2
SELECT TRUNCATE(TAXACCT_,0) AS TAXACCT_ FROM snohomish_base_2;
 
CREATE TABLE snomh
SELECT PARCEL_ID, x_coord, y_coord FROM snohomish_parcels_MH GROUP BY PARCEL_ID;

-- ArcGIS: join MH points to base file, import correspondences to MySQL

DROP TABLE snohomish_parcels_mh;
DROP TABLE snobase2;
DROP TABLE snomh;

CREATE TABLE snohomish_subparcels_mh
SELECT a.PARCEL_I_1 AS PARCEL_ID, a.PARCEL_ID AS AccountID, 1 AS SubparcelFlag
FROM snmhjoin a; 

-- DROP TABLE snmhjoin;

CREATE TEMPORARY TABLE snohomish_subparcels_other_presort
SELECT a.* FROM snohomish_parcels_nonMH a
LEFT JOIN snohomish_deletefrombase b ON a.PARCEL_ID = b.PARCEL_ID 
WHERE b.PARCEL_ID IS NULL;

DROP TABLE snohomish_parcels_nonMH;

CREATE TEMPORARY TABLE snohomish_subparcels_other_prelim
SELECT a.PARCEL_ID AS AccountID, b.PARCEL_ID AS PARCEL_ID 
FROM snohomish_subparcels_other_presort a
LEFT JOIN snohomish_base_2 b ON a.AREA = b.AREA AND a.x_coord = b.x_coord AND a.y_coord = b.y_coord;

CREATE TEMPORARY TABLE snohomish_subparcels_id
SELECT PARCEL_ID from snohomish_subparcels_other_prelim WHERE PARCEL_ID IS NOT NULL GROUP BY PARCEL_ID HAVING COUNT(*)>1;

CREATE INDEX subparcelid USING BTREE ON snohomish_subparcels_id (PARCEL_ID);

CREATE TABLE snohomish_subparcels_other
SELECT a.*, IF(b.PARCEL_ID IS NOT NULL, 1, 0) AS SubparcelFlag
FROM snohomish_subparcels_other_prelim a
LEFT JOIN snohomish_subparcels_id b ON a.PARCEL_ID = b.PARCEL_ID;

DROP TABLE snohomish_base_2;

-- Sort subparcel table

CREATE TABLE snohomish_subparcels_temp
SELECT '061' AS County, PARCEL_ID, AccountID, SubparcelFlag, CONCAT('061',AccountID) AS ID_SUBPARCEL
FROM snohomish_subparcels_mh a
WHERE PARCEL_ID IS NOT NULL AND AccountID IS NOT NULL
UNION
SELECT '061' AS County, PARCEL_ID, AccountID, SubparcelFlag, CONCAT('061',AccountID) AS ID_SUBPARCEL
FROM snohomish_subparcels_other a
WHERE PARCEL_ID IS NOT NULL AND AccountID IS NOT NULL;

ALTER TABLE snohomish_subparcels_temp
MODIFY COLUMN ID_SUBPARCEL VARCHAR(28) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL;

DROP TABLE snohomish_subparcels_mh;
DROP TABLE snohomish_subparcels_other;
-- DROP TABLE allparc;

-- -------------------------------------------
-- -------------------------------------------
-- -------------------------------------------


CREATE TEMPORARY TABLE snohomish_subparcels_2
SELECT a.*, IF(b.MKIMP IS NULL, 0, b.MKIMP) AS ImprValue, IF(b.MKLND IS NULL, 0, b.MKLND) AS LandValue
FROM snohomish_subparcels_temp a
LEFT JOIN snohomish_value_temp b ON a.AccountID = b.PARCEL_NUM;

CREATE TEMPORARY TABLE snohomish_subparcels_3
SELECT a.*, IF(b.XMPTDESCR IS NOT NULL, 1, 0) AS TaxExempt
FROM snohomish_subparcels_2 a
LEFT JOIN snohomish_exemptions_temp b ON a.PARCEL_ID = b.PARCEL_NUM;

CREATE INDEX id_buildingsums USING BTREE ON snohomish_subparcels_3 (ID_SUBPARCEL);

-- Assess number of buildings per subparcel

CREATE TEMPORARY TABLE snohomish_building_sums
SELECT ID_SUBPARCEL, SUM(BuildingFlag) AS NumberofBuildings, SUM(OutbuildingFlag) AS NumberofOutbuildings
FROM snohomish_buildings_2
GROUP BY ID_SUBPARCEL;

DROP TABLE snohomish_buildings_2;

ALTER TABLE snohomish_building_sums
MODIFY COLUMN ID_SUBPARCEL VARCHAR(28) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL;

CREATE INDEX id_buildingsums USING BTREE ON snohomish_building_sums (ID_SUBPARCEL);

-- Merge building counts with subparcel data

CREATE TEMPORARY TABLE snohomish_subparcels_4
SELECT a.County, a.PARCEL_ID, a.AccountID, a.SubparcelFlag, IF(b.NumberofBuildings IS NULL,0, b.NumberofBuildings) AS NumberofBuildings, IF(b.NumberofOutbuildings IS NULL,0, b.NumberofOutbuildings) AS NumberofOutbuildings, a.LandValue, a.ImprValue, a.TaxExempt, a.ID_SUBPARCEL, CONCAT(a.County, a.PARCEL_ID) AS ID_PARCEL
FROM snohomish_subparcels_3 a
LEFT JOIN snohomish_building_sums b ON a.ID_SUBPARCEL = b.ID_SUBPARCEL;

-- Add to final table

INSERT INTO all_subparcels
(County, PARCEL_ID, AccountID, SubparcelFlag, NumberofBuildings, NumberofOutbuildings, LandValue, ImprValue, TaxExempt, ID_SUBPARCEL, ID_PARCEL)
SELECT County, PARCEL_ID, AccountID, SubparcelFlag, NumberofBuildings, NumberofOutbuildings, LandValue, ImprValue, TaxExempt, ID_SUBPARCEL, ID_PARCEL FROM snohomish_subparcels_4;


--
-- Assembly of parcel data
--

-- Assess number of subparcels per parcel

CREATE TEMPORARY TABLE snohomish_parents
SELECT PARCEL_ID, COUNT(PARCEL_ID) AS Subparcels, SUM(LandValue) AS LandValueParcel, SUM(ImprValue) AS ImprValueParcel, IF(SUM(TaxExempt) > 0, 1,0) AS TaxExemptParcel
FROM snohomish_subparcels_4
WHERE PARCEL_ID IS NOT NULL
GROUP BY PARCEL_ID;

CREATE INDEX id_parents USING BTREE ON snohomish_parents (PARCEL_ID);

-- Presort parcel data

CREATE TEMPORARY TABLE snohomish_parcel_presort
SELECT '061' AS County, m.PARCEL_ID, m.ACRES AS Size_Acres, (m.ACRES * 43560) AS Size_SF, m.ZONE_DESC AS Zoning
FROM snohomish_masterrecord_temp m;

CREATE TEMPORARY TABLE snohomish_parcel_presort_2
SELECT a.*, b.CITY AS Jurisdiction, b.USECODE AS Land_Use FROM snohomish_parcel_presort a
LEFT JOIN snohomish_city_1 b ON a.PARCEL_ID = b.PARCEL_ID;

CREATE TEMPORARY TABLE snohomish_parcel_presort_3
SELECT a.County, a.PARCEL_ID, IF(a.Jurisdiction IS NULL, b.CITY, a.Jurisdiction) AS Jurisdiction, a.Size_Acres, a.Size_SF, IF(a.Land_Use IS NULL, b.USECODE, a.Land_Use) AS Land_Use, a.Zoning
FROM snohomish_parcel_presort_2 a
LEFT JOIN snohomish_city_2 b ON a.PARCEL_ID = b.PARCEL_ID;

CREATE INDEX id_parcel USING BTREE ON snohomish_parcel_presort_3 (PARCEL_ID);

-- Add subparcel counts

CREATE TEMPORARY TABLE parcels_snohomish
SELECT m.County, m.PARCEL_ID, k.Subparcels AS NumberofAccounts, k.TaxExemptParcel, k.LandValueParcel, k.ImprValueParcel, m.Jurisdiction, m.Size_Acres, m.Size_SF, m.Land_Use, m.Zoning
FROM snohomish_parents k
LEFT JOIN snohomish_parcel_presort_3 m ON m.PARCEL_ID = k.PARCEL_ID
WHERE m.PARCEL_ID IS NOT NULL;

ALTER TABLE parcels_snohomish
MODIFY COLUMN County VARCHAR(5) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN Land_Use VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

CREATE INDEX id_code USING BTREE ON parcels_snohomish (County, Land_Use);

-- Add additional columns

CREATE TEMPORARY TABLE parcels_snohomish_2
SELECT a.County, a.PARCEL_ID, LEFT(a.PARCEL_ID, 6) AS PLAT_ID, a.NumberofAccounts, a.TaxExemptParcel, a.LandValueParcel, a.ImprValueParcel, IF(a.Jurisdiction IS NULL, '', a.Jurisdiction) AS Jurisdiction, a.Size_Acres, a.Size_SF, a.Land_Use, IF(a.Zoning IS NULL, '', a.Zoning) AS Zoning, IF(b.land_use_description IS NULL, '', b.land_use_description) AS LandUseDescription, IF(b.generic_land_use_1 IS NULL, '', b.generic_land_use_1) AS GenericLandUse1, IF(b.generic_land_use_2 IS NULL, '', b.generic_land_use_2) AS GenericLandUse2, IF(b.res_nonres IS NULL, '', b.res_nonres) AS res_nonres, CONCAT(a.County, a.PARCEL_ID) AS ID_PARCEL, CONCAT(a.County, LEFT(a.PARCEL_ID,6)) AS ID_PLAT
FROM parcels_snohomish a
LEFT JOIN general.land_use_generic_reclass_2005 b ON (b.county = a.County AND b.county_land_use_code = a.Land_Use);

ALTER TABLE parcels_snohomish_2
MODIFY COLUMN PLAT_ID VARCHAR(13) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN Jurisdiction VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN LandUseDescription VARCHAR(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN GenericLandUse1 VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN GenericLandUse2 VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN res_nonres VARCHAR(10) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN ID_PARCEL VARCHAR(28) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN ID_PLAT VARCHAR(13) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

-- Add to final table

INSERT INTO all_parcels
(County, PARCEL_ID, PLAT_ID, NumberofAccounts, LandValueParcel, ImprValueParcel, TaxExemptParcel, Jurisdiction, Size_Acres, Size_SF, Land_Use, Zoning, LandUseDescription, GenericLandUse1, GenericLandUse2, res_nonres, ID_PARCEL, ID_PLAT)
SELECT County, PARCEL_ID, PLAT_ID, NumberofAccounts, LandValueParcel, ImprValueParcel, TaxExemptParcel, Jurisdiction, Size_Acres, Size_SF, Land_Use, Zoning, LandUseDescription, GenericLandUse1, GenericLandUse2, res_nonres, ID_PARCEL, ID_PLAT
FROM parcels_snohomish_2;

DROP TABLE snohomish_deletefrombase;
DROP TABLE snohomish_subparcels_temp;


--
-- Assembly of sales data
--

-- Collect initial variables

CREATE TEMPORARY TABLE sales_snohomish
SELECT '061' AS County, `Parcel Id` AS AccountID, CONCAT(YEAR(`Sale Date`),`Excise Nbr`) AS ExciseTaxNumber, `Sale Date` AS SaleDate, `Sale Price` AS SalePrice, 0 AS PPropPrice, "" AS BuyerName, Grantor AS SellerName, `Deed Type` AS DeedType, `Sale Qual Code` AS SaleWarnings
FROM snohomish_sales_temp c;

CREATE INDEX id_excise USING BTREE ON sales_snohomish (ExciseTaxNumber);

-- Count number of accounts per sale

CREATE TEMPORARY TABLE sales_snohomish_counts
SELECT ExciseTaxNumber, COUNT(ExciseTaxNumber) AS NumberofAccounts FROM sales_snohomish GROUP BY ExciseTaxNumber;

CREATE INDEX id_excise USING BTREE ON sales_snohomish_counts (ExciseTaxNumber);

-- Join counts to main table

ALTER TABLE sales_snohomish
MODIFY COLUMN ExciseTaxNumber VARCHAR(25) NULL,
MODIFY COLUMN DeedType VARCHAR(50) NOT NULL DEFAULT '0',
MODIFY COLUMN SaleWarnings VARCHAR(50) NOT NULL DEFAULT '0';

CREATE TEMPORARY TABLE sales_snohomish_2
SELECT s.County, s.AccountID, s.ExciseTaxNumber, c.NumberofAccounts, s.SaleDate, s.SalePrice, s.PPropPrice, s.BuyerName, s.SellerName, s.DeedType, s.SaleWarnings
FROM sales_snohomish s
LEFT JOIN sales_snohomish_counts c ON c.ExciseTaxNumber = s.ExciseTaxNumber;

-- Add descriptions of sales instruments

CREATE TEMPORARY TABLE sales_snohomish_3
SELECT a.*, IF(i.InstrumentDescr IS NULL, '', i.InstrumentDescr) AS InstrumentDescr, IF(i.ValidInstrument IS NULL, 0, i.ValidInstrument) AS ValidInstrument
FROM sales_snohomish_2 a
LEFT JOIN general.instrumenttypes i ON (a.County = i.County AND a.DeedType = i.InstrumentType);

ALTER TABLE sales_snohomish_3
MODIFY COLUMN DeedType VARCHAR(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0';

CREATE INDEX id_salewarnings USING BTREE ON sales_snohomish_3 (County, SaleWarnings);

-- Add descriptions of sales warnings

CREATE TEMPORARY TABLE sales_snohomish_4
SELECT a.*, IF(s.SWarnDescr IS NULL, '', s.SWarnDescr) AS SWarnDescr,
IF(s.ValidSale IS NULL, '0', s.ValidSale) AS ValidSale, CONCAT(a.County, a.AccountID) AS ID_SUBPARCEL,
CONCAT(a.County,a.ExciseTaxNumber,a.AccountID) AS ID_SALE
FROM sales_snohomish_3 a
LEFT JOIN general.salewarnings s ON (a.County = s.County AND a.SaleWarnings = s.SaleWarnings);

ALTER TABLE sales_snohomish_4
MODIFY COLUMN InstrumentDescr VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN ValidInstrument INT NOT NULL DEFAULT 0,
MODIFY COLUMN SWarnDescr VARCHAR(150) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
MODIFY COLUMN ValidSale INT NOT NULL DEFAULT 0;

-- Add to final table

INSERT INTO all_sales
(County, AccountID, ExciseTaxNumber, NumberofAccounts, SaleDate, SalePrice, PPropPrice, BuyerName, SellerName, DeedType, SaleWarnings, InstrumentDescr, ValidInstrument, SWarnDescr, ValidSale, ID_SUBPARCEL, ID_SALE)
SELECT County, AccountID, ExciseTaxNumber, NumberofAccounts, SaleDate, SalePrice, PPropPrice, BuyerName, SellerName, DeedType, SaleWarnings, InstrumentDescr, ValidInstrument, SWarnDescr, ValidSale, ID_SUBPARCEL, ID_SALE
FROM sales_snohomish_4;

FLUSH TABLES;

-- ----------------------------------------------------------------------


-- ----------------------------------------------------------------------
-- ADD GIS DATA TO PARCELS
-- ----------------------------------------------------------------------


--
-- PARCELS (plus GIS data)
--

DROP TABLE IF EXISTS all_parcels_gis;
CREATE TABLE all_parcels_gis (
  all_parcels_gis_id INT(10) unsigned NOT NULL AUTO_INCREMENT,
  County CHAR(3) NULL,
  PARCEL_ID VARCHAR(25) NULL,
  PLAT_ID VARCHAR(10) NULL,
  NumberofAccounts INT(11) NOT NULL DEFAULT '0',
  LandValueParcel INT(12) NOT NULL DEFAULT 0,
  ImprValueParcel INT(12) NOT NULL DEFAULT 0,
  TaxExemptParcel INT(5) NOT NULL DEFAULT 0,
  Jurisdiction VARCHAR(50) NOT NULL DEFAULT 'Unknown',
  Size_Acres DOUBLE(22,2) NOT NULL DEFAULT '0.00',
  Size_SF INT(11) NOT NULL DEFAULT '0',
  Land_Use VARCHAR(50) NOT NULL,
  Zoning VARCHAR(50) NOT NULL,
  LandUseDescription VARCHAR(100) NOT NULL DEFAULT '0',
  GenericLandUse1 VARCHAR(50) NOT NULL DEFAULT '0',
  GenericLandUse2 VARCHAR(50) NOT NULL DEFAULT '0',
  res_nonres VARCHAR(10) NOT NULL DEFAULT '0',
  ID_PARCEL VARCHAR(28) NULL,
  ID_PLAT VARCHAR(13) NULL,
  GIS_area_sf INT(20) NOT NULL DEFAULT '0',
  GIS_area_acres DOUBLE(15,2) NOT NULL DEFAULT '0.00',
  X_SP_HARN DOUBLE(15,5) NOT NULL DEFAULT '0.00000',
  Y_SP_HARN DOUBLE(15,5) NOT NULL DEFAULT '0.00000',
  X_SP DOUBLE(15,5) NOT NULL DEFAULT '0.00000',
  Y_SP DOUBLE(15,5) NOT NULL DEFAULT '0.00000',
  X_UTM DOUBLE(15,5) NOT NULL DEFAULT '0.00000',
  Y_UTM DOUBLE(15,5) NOT NULL DEFAULT '0.00000',
  grid_code INT(10) NOT NULL DEFAULT '0',
  taz_id INT(4) NOT NULL DEFAULT '0',
  block_id VARCHAR(20) NOT NULL DEFAULT '0',
  is_in_ugb INT(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (all_parcels_gis_id),
  INDEX id_parcel (ID_PARCEL)
)
ENGINE = MyISAM
ROW_FORMAT = Dynamic
CHARACTER SET latin1 COLLATE latin1_swedish_ci;

CREATE TEMPORARY TABLE spatialdata
SELECT * FROM spatial.spatial_2005;

CREATE INDEX parcelid USING BTREE ON spatialdata (ID_PARCEL);

CREATE TEMPORARY TABLE citydata
SELECT *, CONCAT(county, city, city_alt, parcel_zoning) AS indexvalue FROM general.city_reclass_2005;

ALTER TABLE citydata
MODIFY COLUMN indexvalue VARCHAR(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '';

CREATE INDEX city USING BTREE ON citydata (indexvalue);

CREATE TEMPORARY TABLE all_parcels_gis_temp
SELECT a.County, a.PARCEL_ID, a.PLAT_ID, a.NumberofAccounts, a.LandValueParcel, a.ImprValueParcel, a.TaxExemptParcel, a.Jurisdiction, a.Size_Acres, a.Size_SF, a.Land_Use, a.Zoning, a.LandUseDescription, a.GenericLandUse1, a.GenericLandUse2, a.res_nonres, a.ID_PARCEL, a.ID_PLAT, b.GIS_area_sf, b.GIS_area_acres, b.X_SP_HARN, b.Y_SP_HARN, b.X_SP, b.Y_SP, b.X_UTM, b.Y_UTM, b.grid_code, b.taz_id, b.block_id, b.CityName, b.is_in_ugb, CONCAT(a.County, a.Jurisdiction, b.CityName, a.Zoning) AS indexvalue
FROM all_parcels a
LEFT JOIN spatialdata b ON a.ID_PARCEL = b.ID_PARCEL;

ALTER TABLE all_parcels_gis_temp
MODIFY COLUMN indexvalue VARCHAR(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '';

CREATE TEMPORARY TABLE all_parcels_gis_temp_2
SELECT a.*, IF(b.city_name IS NULL, 'Unknown', b.city_name) AS Jurisdiction_final FROM all_parcels_gis_temp a
LEFT JOIN citydata b ON a.indexvalue = b.indexvalue;

INSERT INTO all_parcels_gis
(County, PARCEL_ID, PLAT_ID, NumberofAccounts, LandValueParcel, ImprValueParcel, TaxExemptParcel, Jurisdiction, Size_Acres, Size_SF, Land_Use, Zoning, LandUseDescription, GenericLandUse1, GenericLandUse2, res_nonres, ID_PARCEL, ID_PLAT, GIS_area_sf, GIS_area_acres, X_SP_HARN, Y_SP_HARN, X_SP, Y_SP, X_UTM, Y_UTM, grid_code, taz_id, block_id, is_in_ugb)
SELECT County, PARCEL_ID, PLAT_ID, NumberofAccounts, LandValueParcel, ImprValueParcel, TaxExemptParcel, Jurisdiction_final, Size_Acres, Size_SF, Land_Use, Zoning, LandUseDescription, GenericLandUse1, GenericLandUse2, res_nonres, ID_PARCEL, ID_PLAT, GIS_area_sf, GIS_area_acres, X_SP_HARN, Y_SP_HARN, X_SP, Y_SP, X_UTM, Y_UTM, grid_code, taz_id, block_id, is_in_ugb
FROM all_parcels_gis_temp_2;

-- -------------------------------------------------------------------




-- ----------------------------------------------------------------------
-- COLLAPSE BUILDINGS TO PARCEL (ELIMINATE SUBPARCELS), COMBINE CONDOS, ADD PROPORTIONS
-- ----------------------------------------------------------------------


FLUSH TABLES;
USE workspace;

DROP TABLE IF EXISTS all_buildings_collapsed_prelim;
DROP TABLE IF EXISTS all_buildings_collapsed;


CREATE TABLE all_buildings_collapsed_prelim (
  all_buildings_collapsed_id INT(10) unsigned NOT NULL AUTO_INCREMENT,
  County VARCHAR(5) NULL,
  AccountID VARCHAR(25) NULL,
  BuildingID VARCHAR(25) NULL,
  BuildingFlag INT(3) NOT NULL DEFAULT '0',
  OutbuildingFlag INT(3) NOT NULL DEFAULT '0',
  BuildingUseCode VARCHAR(50) NOT NULL DEFAULT '0',
  BldgSF INT(11) NOT NULL DEFAULT '0',
  Stories DOUBLE(5,2) NOT NULL DEFAULT '0',
  Footprint INT(11) NOT NULL DEFAULT '0',
  YearBuilt INT(11) NOT NULL DEFAULT '0',
  BldgQuality VARCHAR(50) NOT NULL DEFAULT '0',
  BldgCondition VARCHAR(50) NOT NULL DEFAULT '0',
  NumberofUnits INT(11) NOT NULL DEFAULT '0',
  Bedrooms INT(3) NOT NULL DEFAULT '0',
  BathFull INT(3) NOT NULL DEFAULT '0',
  Bath3Qtr INT(3) NOT NULL DEFAULT '0',
  BathHalf INT(3) NOT NULL DEFAULT '0',
  Bathrooms DOUBLE(5,2) NOT NULL DEFAULT '0.00',
  BuildingUseDescription VARCHAR(100) NOT NULL DEFAULT '0',
  GeneralCategory VARCHAR(50) NOT NULL DEFAULT '0',
  GeneralCategoryCode INT(5) NOT NULL DEFAULT '0',
  BuildingType INT(1) NOT NULL DEFAULT '0', 
  BuildingTypeDesc VARCHAR(50) NOT NULL DEFAULT '0',
  ID_SUBPARCEL VARCHAR(30) NULL,
  PARCEL_ID VARCHAR(25) NULL,
  SubparcelFlag INT(11) NULL,
  ID_PARCEL VARCHAR(28) NULL,
  NumberofBuildingsParcel DOUBLE(17,0) NULL,
  NumberofOutbuildingsParcel DOUBLE(17,0) NULL,
  PRIMARY KEY (all_buildings_collapsed_id),
  INDEX id_subparcel (ID_SUBPARCEL),
  INDEX id_parcel (ID_PARCEL)
)
ENGINE = MyISAM
ROW_FORMAT = Dynamic
CHARACTER SET latin1 COLLATE latin1_swedish_ci;


CREATE TABLE all_buildings_collapsed (
  all_buildings_collapsed_id INT(10) unsigned NOT NULL AUTO_INCREMENT,
  County VARCHAR(5) NULL,
  AccountID VARCHAR(25) NULL,
  BuildingID VARCHAR(25) NULL,
  BuildingFlag INT(3) NOT NULL DEFAULT '0',
  OutbuildingFlag INT(3) NOT NULL DEFAULT '0',
  BuildingUseCode VARCHAR(50) NOT NULL DEFAULT '0',
  BldgSF INT(11) NOT NULL DEFAULT '0',
  Stories DOUBLE(5,2) NOT NULL DEFAULT '0',
  Footprint INT(11) NOT NULL DEFAULT '0',
  YearBuilt INT(11) NOT NULL DEFAULT '0',
  BldgQuality VARCHAR(50) NOT NULL DEFAULT '0',
  BldgCondition VARCHAR(50) NOT NULL DEFAULT '0',
  NumberofUnits INT(11) NOT NULL DEFAULT '0',
  Bedrooms INT(3) NOT NULL DEFAULT '0',
  BathFull INT(3) NOT NULL DEFAULT '0',
  Bath3Qtr INT(3) NOT NULL DEFAULT '0',
  BathHalf INT(3) NOT NULL DEFAULT '0',
  Bathrooms DOUBLE(5,2) NOT NULL DEFAULT '0.00',
  BuildingUseDescription VARCHAR(100) NOT NULL DEFAULT '0',
  GeneralCategory VARCHAR(50) NOT NULL DEFAULT '0',
  GeneralCategoryCode INT(5) NOT NULL DEFAULT '0',
  BuildingType INT(1) NOT NULL DEFAULT '0', 
  BuildingTypeDesc VARCHAR(50) NOT NULL DEFAULT '0',
  ID_SUBPARCEL VARCHAR(30) NULL,
  PARCEL_ID VARCHAR(25) NULL,
  SubparcelFlag INT(11) NULL,
  ID_PARCEL VARCHAR(28) NULL,
  all_parcels_gis_id INT(10) unsigned NOT NULL DEFAULT '0',
  NumberofBuildingsParcel DOUBLE(17,0) NULL,
  NumberofOutbuildingsParcel DOUBLE(17,0) NULL,
  ParcelAreaPortion INT(11) NOT NULL DEFAULT '0',
  ParcelValuePortion INT(11) NOT NULL DEFAULT '0',
  TaxExemptParcel INT(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (all_buildings_collapsed_id),
  INDEX id_subparcel (ID_SUBPARCEL),
  INDEX id_parcel (ID_PARCEL)
)
ENGINE = MyISAM
ROW_FORMAT = Dynamic
CHARACTER SET latin1 COLLATE latin1_swedish_ci;


CREATE TEMPORARY TABLE all_buildings_collapsed_temp
SELECT a.*, b.PARCEL_ID, b.SubparcelFlag, b.ID_PARCEL
FROM all_buildings a
LEFT JOIN all_subparcels b ON (a.ID_SUBPARCEL = b.ID_SUBPARCEL)
WHERE b.PARCEL_ID IS NOT NULL;

CREATE TEMPORARY TABLE all_buildings_collapsed_temp_2
SELECT a.*, '0' AS PARCEL_ID, 0 AS SubparcelFlag, '0' AS ID_PARCEL
FROM all_buildings a
LEFT JOIN all_subparcels b ON (a.ID_SUBPARCEL = b.ID_SUBPARCEL)
WHERE b.PARCEL_ID IS NULL;

CREATE TEMPORARY TABLE all_buildingsonparcel
SELECT SUM(NumberofBuildings) AS NumberofBuildingsParcel, SUM(NumberofOutbuildings) AS NumberofOutbuildingsParcel, ID_PARCEL
FROM all_subparcels b
WHERE PARCEL_ID IS NOT NULL
GROUP BY ID_PARCEL;

CREATE INDEX id_parcel USING BTREE ON all_buildingsonparcel (ID_PARCEL);

CREATE TEMPORARY TABLE all_buildings_collapsed_temp_combined
SELECT a.County, a.AccountID, a.BuildingID, a.BuildingFlag, a.OutbuildingFlag, a.BuildingUseCode, a.BldgSF, a.Stories, a.Footprint, a.YearBuilt, a.BldgQuality, a.BldgCondition, a.NumberofUnits, a.Bedrooms, a.BathFull, a.Bath3Qtr, a.BathHalf, a.Bathrooms, a.BuildingUseDescription, a.GeneralCategory, a.GeneralCategoryCode, a.BuildingType, a.BuildingTypeDesc, a.ID_SUBPARCEL, a.PARCEL_ID, a.SubparcelFlag, a.ID_PARCEL, b.NumberofBuildingsParcel, b.NumberofOutbuildingsParcel
FROM all_buildings_collapsed_temp a
LEFT JOIN all_buildingsonparcel b ON a.ID_PARCEL = b.ID_PARCEL;

ALTER TABLE all_buildings_collapsed_temp_combined ADD ID INT UNSIGNED NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (ID);

CREATE TEMPORARY TABLE all_buildings_collapsed_temp_combined_2
SELECT a.County, a.AccountID, a.BuildingID, a.BuildingFlag, a.OutbuildingFlag, a.BuildingUseCode, a.BldgSF, a.Stories, a.Footprint, a.YearBuilt, a.BldgQuality, a.BldgCondition, a.NumberofUnits, a.Bedrooms, a.BathFull, a.Bath3Qtr, a.BathHalf, a.Bathrooms, a.BuildingUseDescription, a.GeneralCategory, a.GeneralCategoryCode, a.BuildingType, a.BuildingTypeDesc, a.ID_SUBPARCEL, a.PARCEL_ID, a.SubparcelFlag, a.ID_PARCEL,  0 AS NumberofBuildingsParcel, 0 AS NumberofOutbuildingsParcel
FROM all_buildings_collapsed_temp_2 a;

ALTER TABLE all_buildings_collapsed_temp_combined_2 ADD ID INT UNSIGNED NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (ID);

CREATE TEMPORARY TABLE all_buildings_collapsed_combined
SELECT a.* FROM all_buildings_collapsed_temp_combined a
UNION
SELECT a.* FROM all_buildings_collapsed_temp_combined_2 a;

INSERT INTO all_buildings_collapsed_prelim
(County, AccountID, BuildingID, BuildingFlag, OutbuildingFlag, BuildingUseCode, BldgSF, Stories, Footprint, YearBuilt, BldgQuality, BldgCondition, NumberofUnits, Bedrooms, BathFull, Bath3Qtr, BathHalf, Bathrooms, BuildingUseDescription, GeneralCategory, GeneralCategoryCode, BuildingType, BuildingTypeDesc, ID_SUBPARCEL, PARCEL_ID, SubparcelFlag, ID_PARCEL, NumberofBuildingsParcel, NumberofOutbuildingsParcel)
SELECT a.County, a.AccountID, a.BuildingID, a.BuildingFlag, a.OutbuildingFlag, a.BuildingUseCode, a.BldgSF, a.Stories, a.Footprint, a.YearBuilt, a.BldgQuality, a.BldgCondition, a.NumberofUnits, a.Bedrooms, a.BathFull, a.Bath3Qtr, a.BathHalf, a.Bathrooms, a.BuildingUseDescription, a.GeneralCategory, a.GeneralCategoryCode, a.BuildingType, a.BuildingTypeDesc, a.ID_SUBPARCEL, a.PARCEL_ID, a.SubparcelFlag, a.ID_PARCEL, a.NumberofBuildingsParcel, a.NumberofOutbuildingsParcel
FROM all_buildings_collapsed_combined a;

CREATE TEMPORARY TABLE all_buildings_collapsed_prelim_step2
SELECT a.*, b.all_parcels_gis_id, b.Size_SF, (b.LandValueParcel + b.ImprValueParcel) AS TotalValueParcel, b.TaxExemptParcel FROM all_buildings_collapsed_prelim a
LEFT JOIN all_parcels_gis b ON a.ID_PARCEL = b.ID_PARCEL;

CREATE TEMPORARY TABLE all_buildings_collapsed_prelim_step3
SELECT ID_PARCEL, SUM(BldgSF) AS SumBldgSF
FROM all_buildings_collapsed_prelim
GROUP BY ID_PARCEL;

CREATE INDEX parcel USING BTREE ON all_buildings_collapsed_prelim_step3 (ID_PARCEL);

CREATE TEMPORARY TABLE all_buildings_collapsed_prelim_step4
SELECT a.*, b.SumBldgSF
FROM all_buildings_collapsed_prelim_step2 a
LEFT JOIN all_buildings_collapsed_prelim_step3 b ON a.ID_PARCEL = b.ID_PARCEL;

CREATE TEMPORARY TABLE all_buildings_collapsed_prelim_step5a
SELECT a.*, IF(SumBldgSF = 0, 0, FLOOR(Size_SF * (BldgSF / SumBldgSF)) ) AS ParcelAreaPortion, IF(SumBldgSF = 0, 0, FLOOR(TotalValueParcel * (BldgSF / SumBldgSF)) ) AS ParcelValuePortion
FROM all_buildings_collapsed_prelim_step4 a
WHERE SubparcelFlag = 0 OR GeneralCategoryCode = 11;

CREATE TEMPORARY TABLE all_buildings_collapsed_prelim_step5b
SELECT 
County, AccountID, 'comb' AS BuildingID, 1 AS BuildingFlag, 0 AS OutbuildingFlag, BuildingUseCode, SUM(a.BldgSF) AS BldgSF, Stories, SUM(a.BldgSF)/a.Stories AS Footprint, YearBuilt, BldgQuality, BldgCondition, SUM(a.NumberofUnits) AS NumberofUnits, SUM(a.Bedrooms) AS Bedrooms, SUM(a.BathFull) AS BathFull, SUM(a.Bath3Qtr) AS Bath3Qtr, SUM(a.BathHalf) AS BathHalf, SUM(a.Bathrooms) AS Bathrooms, BuildingUseDescription, GeneralCategory, GeneralCategoryCode, BuildingType, BuildingTypeDesc, ID_SUBPARCEL, PARCEL_ID, SubparcelFlag, ID_PARCEL, all_parcels_gis_id, NumberofBuildingsParcel, NumberofOutbuildingsParcel, IF(SumBldgSF = 0, 0, FLOOR(Size_SF * (SUM(a.BldgSF) / SumBldgSF)) ) AS ParcelAreaPortion, IF(SumBldgSF = 0, 0, FLOOR(TotalValueParcel * (SUM(a.BldgSF) / SumBldgSF)) ) AS ParcelValuePortion, TaxExemptParcel
FROM all_buildings_collapsed_prelim_step4 a
WHERE SubparcelFlag = 1 AND GeneralCategoryCode <> 11
GROUP BY ID_PARCEL, GeneralCategoryCode;

INSERT INTO all_buildings_collapsed
(County, AccountID, BuildingID, BuildingFlag, OutbuildingFlag, BuildingUseCode, BldgSF, Stories, Footprint, YearBuilt, BldgQuality, BldgCondition, NumberofUnits, Bedrooms, BathFull, Bath3Qtr, BathHalf, Bathrooms, BuildingUseDescription, GeneralCategory, GeneralCategoryCode, BuildingType, BuildingTypeDesc, ID_SUBPARCEL, PARCEL_ID, SubparcelFlag, ID_PARCEL, all_parcels_gis_id, NumberofBuildingsParcel, NumberofOutbuildingsParcel, ParcelAreaPortion, ParcelValuePortion, TaxExemptParcel)
SELECT County, AccountID, BuildingID, BuildingFlag, OutbuildingFlag, BuildingUseCode, BldgSF, Stories, Footprint, YearBuilt, BldgQuality, BldgCondition, NumberofUnits, Bedrooms, BathFull, Bath3Qtr, BathHalf, Bathrooms, BuildingUseDescription, GeneralCategory, GeneralCategoryCode, BuildingType, BuildingTypeDesc, ID_SUBPARCEL, PARCEL_ID, SubparcelFlag, ID_PARCEL, all_parcels_gis_id, NumberofBuildingsParcel, NumberofOutbuildingsParcel, ParcelAreaPortion, ParcelValuePortion, TaxExemptParcel
FROM all_buildings_collapsed_prelim_step5a
UNION
SELECT County, AccountID, BuildingID, BuildingFlag, OutbuildingFlag, BuildingUseCode, BldgSF, Stories, Footprint, YearBuilt, BldgQuality, BldgCondition, NumberofUnits, Bedrooms, BathFull, Bath3Qtr, BathHalf, Bathrooms, BuildingUseDescription, GeneralCategory, GeneralCategoryCode, BuildingType, BuildingTypeDesc, ID_SUBPARCEL, PARCEL_ID, SubparcelFlag, ID_PARCEL, all_parcels_gis_id, NumberofBuildingsParcel, NumberofOutbuildingsParcel, ParcelAreaPortion, ParcelValuePortion, TaxExemptParcel
FROM all_buildings_collapsed_prelim_step5b;

DROP TABLE all_buildings_collapsed_prelim;

-- ----------------------------------------------------------------------




-- ----------------------------------------------------------------------
-- DEFINE OUTPUT TABLES
-- ----------------------------------------------------------------------

FLUSH TABLES;
USE workspace;

# JPF: some name changes marked below:

DROP TABLE IF EXISTS building; # buildings

CREATE TABLE building # buildings
SELECT 
 all_buildings_collapsed_id as building_id,
 all_parcels_gis_id AS parcel_id,
 OutbuildingFlag AS outbuilding_flag,
 BldgSF as building_sf, # building_sqft
 Stories AS stories,
 Footprint AS footprint, # footprint_sqft
 YearBuilt AS year_built,
 BldgQuality AS building_quality,
 BldgCondition AS building_condition,
 NumberofUnits AS number_of_units, # residential_units
 Bedrooms AS bedrooms,
 Bathrooms AS bathrooms,
 BuildingUseCode AS building_use,
 BuildingUseDescription building_use_description,
 GeneralCategoryCode AS general_type_1, # building_type_id (or unified_building_type_id?)
 GeneralCategory AS general_type_1_description, # building_type_description (or unified_building_type_description?)
 BuildingType AS general_type_2, # generic_building_type_id
 BuildingTypeDesc AS general_type_2_description, # generic_building_type_description
 County AS county,
 ID_SUBPARCEL AS id_subparcel,
 ID_PARCEL AS id_parcel,
 SubparcelFlag AS subparcel_flag,
 ParcelAreaPortion AS area_portion, # maybe attributed_parcel_area?
 ParcelValuePortion AS value_portion, # maybe attributed_parcel_value?
 TaxExemptParcel AS tax_exempt
FROM all_buildings_collapsed;

ALTER TABLE building # buildings
MODIFY COLUMN building_id INTEGER UNSIGNED NOT NULL DEFAULT NULL AUTO_INCREMENT, 
ADD PRIMARY KEY (building_id);

CREATE TABLE parcel # parcels
SELECT 
 all_parcels_gis_id as parcel_id,
 LandValueParcel AS land_value_parcel, # land_value
 ImprValueParcel AS improvement_value_parcel, # improvement_value
 TaxExemptParcel AS tax_exempt_flag,
 Size_SF AS parcel_size_sf, # parcel_size_sqft
 Land_Use AS parcel_land_use,
 Zoning AS parcel_zoning,
 GenericLandUse1 AS general_use_1,
 GenericLandUse2 AS general_use_2,
 res_nonres,
 GIS_area_sf AS parcel_size_sf_gis, # parcel_size_sqft_in_gis
 X_SP_HARN AS x_coord_sp,
 Y_SP_HARN AS y_coord_sp,
 X_UTM AS x_utm,
 Y_UTM AS y_utm,
 grid_code AS grid_id,
 taz_id AS taz_id, # zone_id (grumble grumble)
 block_id AS block_id,
 Jurisdiction AS city, # we will have county and city tables with IDs...eventually the IDs should be included
 is_in_ugb as ugb_flag,
 County as county,
 ID_PARCEL as id_parcel,
 ID_PLAT as id_plat
FROM all_parcels_gis;

ALTER TABLE parcel # parcels
MODIFY COLUMN parcel_id
 INTEGER UNSIGNED NOT NULL DEFAULT NULL AUTO_INCREMENT, 
ADD PRIMARY KEY (parcel_id);

CREATE TABLE sale # sales
SELECT
 x.sale_id,
 x.accounts_in_transaction,
 y.all_parcels_gis_id AS parcel_id,
 x.partial_parcel_flag,
 x.date,
 x.price,
 x.personal_property_price,
 x.valid_sale,
 x.county,
 x.id_subparcel,
 x.id_parcel,
 x.id_sale
FROM (
SELECT
 a.all_sales_id AS sale_id,
 a.NumberofAccounts as accounts_in_transaction,
 b.SubparcelFlag AS partial_parcel_flag,
 a.SaleDate as date,
 a.SalePrice as price,
 a.PPropPrice as personal_property_price,
 a.ValidSale as valid_sale,
 a.County as county,
 a.ID_SUBPARCEL AS id_subparcel,
 b.ID_PARCEL AS id_parcel,
 a.ID_SALE AS id_sale
FROM all_sales a
LEFT JOIN all_subparcels b ON a.ID_SUBPARCEL = b.ID_SUBPARCEL) x
LEFT JOIN all_parcels_gis y ON x.id_parcel = y.ID_PARCEL
GROUP BY sale_id;

ALTER TABLE sale # sales
MODIFY COLUMN sale_id INTEGER UNSIGNED NOT NULL DEFAULT NULL AUTO_INCREMENT, 
ADD PRIMARY KEY (sale_id);

-- ----------------------------------------------------------------------






CREATE TEMPORARY TABLE buildings_and_plats
SELECT a.*, b.Size_SF, b.Zoning, b.ID_PLAT
FROM all_buildings_collapsed a
LEFT JOIN all_parcels_gis b ON a.ID_PARCEL = b.ID_PARCEL
WHERE OutbuildingFlag = 0;

CREATE TEMPORARY TABLE buildings_and_plats_1
SELECT ID_PLAT, COUNT(*) AS Number1990 FROM buildings_and_plats WHERE YearBuilt >= 1990
GROUP BY ID_PLAT;

CREATE TEMPORARY TABLE buildings_and_plats_2
SELECT ID_PLAT, COUNT(*) AS NumberAll FROM buildings_and_plats
GROUP BY ID_PLAT;

CREATE INDEX id_plat USING BTREE ON buildings_and_plats_1 (ID_PLAT);

CREATE TEMPORARY TABLE platbuildings_all
SELECT b.ID_PLAT, a.Number1990, b.NumberAll
FROM buildings_and_plats_2 b
LEFT JOIN buildings_and_plats_1 a ON a.ID_PLAT = b.ID_PLAT;

CREATE TABLE template_plat_listings
SELECT p.ID_PLAT 
FROM platbuildings_all p 
WHERE Number1990 IS NOT NULL AND Number1990 = NumberAll;

CREATE INDEX id_plat USING BTREE ON template_plat_listings (ID_PLAT);

CREATE TEMPORARY TABLE template_buildings_temp
SELECT a.* FROM buildings_and_plats a
LEFT JOIN template_plat_listings b ON a.ID_PLAT = b.ID_PLAT WHERE b.ID_PLAT IS NOT NULL;

CREATE TABLE template_buildings
SELECT County, AccountID, BuildingID, BuildingFlag, OutbuildingFlag, BuildingUseCode, BldgSF, Stories, Footprint, YearBuilt, BldgQuality, BldgCondition, NumberofUnits, Bedrooms, BathFull, Bath3Qtr, BathHalf, Bathrooms, BuildingUseDescription, GeneralCategory, ID_SUBPARCEL, PARCEL_ID, SubparcelFlag, ID_PARCEL, NumberofBuildingsParcel, NumberofOutbuildingsParcel, Size_SF, Zoning, ID_PLAT
FROM template_buildings_temp
ORDER BY ID_PARCEL;

CREATE TABLE template_parcels
SELECT a.* FROM workspace.all_parcels_gis a
LEFT JOIN template_plat_listings b ON a.ID_PLAT = b.ID_PLAT WHERE b.ID_PLAT IS NOT NULL;


CREATE TEMPORARY TABLE buildings_and_parcel
SELECT a.*, b.Size_SF, b.Zoning, b.ID_PLAT
FROM all_buildings_collapsed a
LEFT JOIN all_parcels_gis b ON a.ID_PARCEL = b.ID_PARCEL
WHERE OutbuildingFlag = 0;

CREATE TEMPORARY TABLE buildings_and_parcels_1
SELECT ID_PARCEL, ID_PLAT, COUNT(*) AS Number1990 FROM buildings_and_parcel WHERE YearBuilt >= 1990
GROUP BY ID_PARCEL;

CREATE TEMPORARY TABLE buildings_and_parcels_2
SELECT ID_PARCEL, ID_PLAT, COUNT(*) AS NumberAll FROM buildings_and_parcel
GROUP BY ID_PARCEL;

CREATE INDEX id_parcel USING BTREE ON buildings_and_parcels_1 (ID_PARCEL);

CREATE TEMPORARY TABLE parcellistings_all
SELECT b.ID_PARCEL, b.ID_PLAT, a.Number1990, b.NumberAll
FROM buildings_and_parcels_2 b
LEFT JOIN buildings_and_parcels_1 a ON a.ID_PARCEL = b.ID_PARCEL
WHERE a.Number1990 = b.NumberAll;

CREATE INDEX id_parcel USING BTREE ON template_parcels (ID_PARCEL);

CREATE TEMPORARY TABLE parcellistings_all_2
SELECT a.ID_PARCEL, IF(b.ID_PLAT IS NOT NULL, 1, 0) AS FullPlatFlag
FROM parcellistings_all a
LEFT JOIN template_parcels b ON a.ID_PARCEL = b.ID_PARCEL;

CREATE INDEX id_parcel USING BTREE ON parcellistings_all_2 (ID_PARCEL);

CREATE TABLE template_parcels_all
SELECT a.*, b.FullPlatFlag
FROM all_parcels_gis a LEFT JOIN parcellistings_all_2 b ON a.ID_PARCEL = b.ID_PARCEL
WHERE b.ID_PARCEL IS NOT NULL;

CREATE TABLE template_buildings_all
SELECT a.*, b.FullPlatFlag
FROM buildings_and_parcel a LEFT JOIN parcellistings_all_2 b ON a.ID_PARCEL = b.ID_PARCEL
WHERE b.ID_PARCEL IS NOT NULL;

CREATE INDEX id_parcel USING BTREE ON template_parcels_all (ID_PARCEL);


-- -------------------------------
-- END OF REGULAR CODE
-- -------------------------------


-- -------------------------------
-- Appendix: Make tables for 
-- building_types and 
-- generic_building_types
-- -------------------------------

CREATE TABLE building_types




















































-- 2001 Parcel data -- temporary, with spatial data

-- ----------------------------------------------------------------------
-- Using 2001 parcel data on network...
-- ----------------------------------------------------------------------

CREATE TABLE parcels_2001_alt
SELECT County, IF((mid(PARCEL_ID,7,4)='8888' AND County = '033'),CONCAT(mid(PARCEL_ID,1,6),'0000'),PARCEL_ID) AS PARCEL_ID, Land_Use, Built_SF, Improvement_Value, Land_Value, Lot_SF, Lot_Acres, Residential_Units, Residential_Units_Imputed, Year_Built, Land_Use_Imputed, Year_Built_Imputed, Tax_Exempt, Undevelopable
FROM table_temp.2001_alt;

CREATE TABLE parcels_2001_alt2
SELECT a.*, CONCAT(County, PARCEL_ID) AS ID_PARCEL  
FROM all_parcels_2001_alt a;

CREATE INDEX id_parcel USING BTREE ON parcels_2001_alt2 (ID_PARCEL);

CREATE TABLE parcels_2001_alldata
SELECT a.*, s.GIS_area_sf, s.GIS_area_acres, s.grid_code, s.taz_id, s.block_id, s.CityName, s.is_in_ugb
FROM parcels_2001_alt2 a
LEFT JOIN spatial.spatial_2001 s
ON s.ID_PARCEL = a.ID_PARCEL
where s.PARCEL_ID is not null and a.PARCEL_ID is not null;

CREATE TABLE all_parcelsdata_spatial_2005_final
SELECT a.*, s.county_land_use_code, s.land_use_description, s.generic_land_use_1, s.generic_land_use_2, s.res_nonres
FROM parcels_2001_alldata a
LEFT JOIN table_temp.land_use_generic_reclass s ON (a.County = s.County AND a.Land_Use = s.county_land_use_code);

ALTER TABLE all_parceldata_spatial_2001_final
MODIFY COLUMN County VARCHAR(3) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN PARCEL_ID VARCHAR(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN Land_Use VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
MODIFY COLUMN Built_SF INT(15),
MODIFY COLUMN Improvement_Value INT(15),
MODIFY COLUMN Land_Value INT(15),
MODIFY COLUMN Built_SF INT(15),
MODIFY COLUMN Lot_SF INT(15),
MODIFY COLUMN Lot_Acres DOUBLE(15,2),
MODIFY COLUMN Residential_Units DOUBLE(15,2),
MODIFY COLUMN Residential_Units_Imputed DOUBLE(15,2),
MODIFY COLUMN Year_Built INT(5),
MODIFY COLUMN Land_Use_Imputed INT(1),
MODIFY COLUMN Year_Built_Imputed INT(1),
MODIFY COLUMN Tax_Exempt INT(1),
MODIFY COLUMN Undevelopable INT(1);

DROP TABLE parcels_2001_alt;
DROP TABLE parcels_2001_alt2;
DROP TABLE parcels_2001_alldata;

CREATE INDEX id_parcel USING BTREE ON all_parceldata_spatial_2001_final (ID_PARCEL);

ALTER TABLE all_parceldata_spatial_2001_final ADD ID INT UNSIGNED NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (ID);


-- Comparisons between 2001 and 2005: analysis of subdivisions

-- ----------------------------------------------------------------------
-- Creating tables for comparisons
-- ----------------------------------------------------------------------

CREATE TABLE parcels_not_found_in_2005
SELECT a.County, a.PARCEL_ID, a.GIS_area_acres, a.res_nonres, a.ID_PARCEL
FROM all_parceldata_spatial_2001_final a
LEFT JOIN all_parceldata_spatial_2005_final b ON (a.ID_PARCEL = b.ID_PARCEL)
WHERE b.ID_PARCEL IS NULL;

CREATE TABLE parcels_not_found_in_2001
SELECT a.County, a.PARCEL_ID, a.GIS_area_acres, a.res_nonres, a.ID_PARCEL
FROM all_parceldata_spatial_2005_final a
LEFT JOIN all_parceldata_spatial_2001_final b ON (a.ID_PARCEL = b.ID_PARCEL)
WHERE b.ID_PARCEL IS NULL;

CREATE TABLE parcels_in_2005_and_2001
SELECT a.County, a.PARCEL_ID, a.GIS_area_acres AS area_2001, b.GIS_area_acres AS area_2005, (b.GIS_area_acres - a.GIS_area_acres) AS area_change, a.res_nonres AS res_nonres_2001, b.res_nonres AS res_nonres_2005, a.ID_PARCEL
FROM all_parceldata_spatial_2001_final a
LEFT JOIN all_parceldata_spatial_2005_final b ON (a.ID_PARCEL = b.ID_PARCEL)
WHERE b.ID_PARCEL IS NOT NULL;

CREATE INDEX size USING BTREE ON parcels_in_2005_and_2001 (area_change);

CREATE TABLE parcels_lost_area_2005
SELECT a.County, a.PARCEL_ID, a.area_2001 AS GIS_area_acres, a.area_change, a.res_nonres_2001 AS res_nonres, a.ID_PARCEL
FROM parcels_in_2005_and_2001 a
WHERE (area_change < -0.009) ;

CREATE TABLE parcels_gained_area_2005
SELECT a.County, a.PARCEL_ID, a.area_2001 AS GIS_area_acres, a.area_change, a.res_nonres_2001 AS res_nonres, a.ID_PARCEL
FROM parcels_in_2005_and_2001 a
WHERE (area_change > 0.009) ;

CREATE TABLE possible_parents_presort
SELECT ID_PARCEL FROM parcels_lost_area_2005
UNION
SELECT ID_PARCEL FROM parcels_not_found_in_2005;

CREATE TABLE possible_parents
SELECT ID_PARCEL FROM possible_parents_presort WHERE ID_PARCEL IS NOT NULL
GROUP BY ID_PARCEL;

CREATE TABLE possible_children_presort
SELECT ID_PARCEL FROM parcels_gained_area_2005
UNION
SELECT ID_PARCEL FROM parcels_not_found_in_2001;

CREATE TABLE possible_children
SELECT ID_PARCEL FROM possible_children_presort WHERE ID_PARCEL IS NOT NULL
GROUP BY ID_PARCEL;

DROP TABLE parcels_lost_area_2005;
DROP TABLE parcels_gained_area_2005;
DROP TABLE possible_parents_presort;
DROP TABLE possible_children_presort;


-- ----------------------------------------------------------------------
-- Data processed for correspondences
-- ----------------------------------------------------------------------

CREATE TABLE parcels_correspondence
SELECT ID_PARCEL AS parent_parcel, ID_PARCEL AS child_parcel, 0 AS newparcel
FROM parcels_in_2005_and_2001 a
WHERE (area_change < -0.009 OR area_change > 0.009);

CREATE TABLE new_parcels
SELECT parcelid AS parent_parcel, ID_PARCEL AS child_parcel, 1 AS newparcel
FROM table_temp.parcel_new;

CREATE TABLE missing_parcels
SELECT ID_PARCEL AS parent_parcel, parcelid AS child_parcel, 0 AS newparcel
FROM table_temp.parcel_missing;

CREATE TABLE parcels_correspondences_all
SELECT parent_parcel, child_parcel, newparcel FROM parcels_correspondence
UNION
SELECT parent_parcel, child_parcel, newparcel FROM new_parcels
UNION
SELECT parent_parcel, child_parcel, newparcel FROM missing_parcels;

CREATE TABLE parcels_correspondences_all_2
SELECT * FROM parcels_correspondences_all
WHERE (SUBSTRING(parent_parcel,1,3) <> '033' OR SUBSTRING(parent_parcel,10,4) <> '7777') AND parent_parcel IS NOT NULL AND child_parcel IS NOT NULL;

CREATE TABLE parcels_correspondences_all_3
SELECT parent_parcel, child_parcel
FROM parcels_correspondences_all_2
GROUP BY parent_parcel, child_parcel;

CREATE INDEX parent USING BTREE ON parcels_correspondences_all_3 (parent_parcel);
CREATE INDEX child USING BTREE ON parcels_correspondences_all_3 (child_parcel);

CREATE TABLE parcels_count_parents
SELECT parent_parcel, COUNT(*) AS parent_number
FROM parcels_correspondences_all_3 WHERE parent_parcel IS NOT NULL
GROUP BY parent_parcel;

CREATE TABLE parcels_count_children
SELECT child_parcel, COUNT(*) AS child_number
FROM parcels_correspondences_all_3 WHERE child_parcel IS NOT NULL
GROUP BY child_parcel;

CREATE INDEX parent USING BTREE ON parcels_count_parents (parent_parcel);
CREATE INDEX child USING BTREE ON parcels_count_children (child_parcel);

CREATE TABLE parcels_correspondences_all_4
SELECT a.parent_parcel, b.parent_number, a.child_parcel
FROM parcels_correspondences_all_3 a
LEFT JOIN parcels_count_parents b ON a.parent_parcel = b.parent_parcel;

CREATE TABLE parcels_correspondences_all_5
SELECT a.parent_parcel, a.parent_number, a.child_parcel, b.child_number
FROM parcels_correspondences_all_4 a
LEFT JOIN parcels_count_children b ON a.child_parcel = b.child_parcel;

CREATE TABLE parcels_correspondences_all_6
SELECT * FROM parcels_correspondences_all_5
WHERE parent_number > 1 AND child_number = 1;

CREATE TABLE parcels_correspondences_all_7
SELECT a.* FROM parcels_correspondences_all_6 a
LEFT JOIN table_temp.exclude_children b ON (a.parent_parcel = b.PARENT_PAR AND a.child_parcel = b.CHILD_PARC)
WHERE b.PARENT_PAR IS NULL;

CREATE TABLE parent_parcel_sums
SELECT parent_parcel, COUNT(*) AS numparents FROM parcels_correspondences_all_7
GROUP BY parent_parcel;

CREATE INDEX parent USING BTREE ON parent_parcel_sums (parent_parcel);

CREATE TABLE parcels_correspondences_all_8
SELECT a.parent_parcel, a.child_parcel, b.numparents
FROM parcels_correspondences_all_7 a
LEFT JOIN parent_parcel_sums b ON a.parent_parcel = b.parent_parcel
WHERE b.numparents > 1;

DROP TABLE parcels_correspondence;
DROP TABLE new_parcels;
DROP TABLE missing_parcels;
DROP TABLE parcels_correspondences_all;
DROP TABLE parcels_correspondences_all_2;
DROP TABLE parcels_correspondences_all_3;
DROP TABLE parcels_correspondences_all_4;
DROP TABLE parcels_correspondences_all_5;
DROP TABLE parcels_correspondences_all_6;
DROP TABLE parcels_correspondences_all_7;
DROP TABLE parent_parcel_sums;
DROP TABLE parcels_count_parents;
DROP TABLE parcels_count_children;


-- ----------------------------------------------------------------------
-- Assessment of child parcels
-- ----------------------------------------------------------------------

CREATE TABLE subdivision_assessment_1
SELECT a.*, b.GIS_area_sf, b.GIS_area_acres, b.Land_Use, b.Zoning, b.LandUseDescription, b.GenericLandUse1, b.GenericLandUse2, b.res_nonres
FROM parcels_correspondences_all_8 a
LEFT JOIN all_parceldata_spatial_2005_final b ON b.ID_PARCEL = a.child_parcel

CREATE INDEX child_parcel USING BTREE ON subdivision_assessment_1 (child_parcel);

ID_PARCEL, BUILDINGUS, 

CREATE TABLE quick_pierce_reclass_1
SELECT q.*, b.GENERALCAT AS general_category, b.ID_PARCEL
FROM table_temp.pierce_reclass q;

CREATE INDEX parcel USING BTREE ON quick_pierce_reclass_1 (ID_PARCEL);

CREATE TABLE subdivision_assessment_2
SELECT a.parent_parcel, a.child_parcel, a.numparents, a.GIS_area_sf, a.GIS_area_acres, a.Land_Use, a.Zoning, LandUseDescription, IF(SUBSTRING(ID_PARCEL,1,3) = '053', NULL(q.general_category, 'Vacant'), a.GenericLandUse1) AS GenericLandUse1, a.GenericLandUse2, a.res_nonres
FROM subdivision_assessment_1 a
LEFT JOIN quick_pierce_reclass_1 q ON q.ID_PARCEL = a.child_parcel;

CREATE TABLE subdivision_assessment_3
SELECT parent_parcel, child_parcel, numparents, GIS_area_sf, GIS_area_acres, Land_Use, Zoning, LandUseDescription, IFNULL(GenericLandUse1, 'Vacant') AS GenericLandUse1, GenericLandUse2, res_nonres
FROM subdivision_assessment_2;

ALTER TABLE subdivision_assessment_3 MODIFY COLUMN GenericLandUse1 VARCHAR(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT 'No Code';

ALTER TABLE `table_temp`.`itemized_chart` 
CHANGE COLUMN `GENERAL_CA` `general_category` VARCHAR(33) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
 MODIFY COLUMN `AGRIC` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `CIVIC` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `COMME` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `FISHE` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `FORES` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `GOVER` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `GROUP` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `HOSPI` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `INDUS` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `MININ` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `MOBIL` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `MULTI` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `NOCODE` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `OFFIC` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `OUTBU` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `PARK` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `PARKI` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `RECRE` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `RIGHT` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `SCHOO` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `SINGL` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `TRANS` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `VACAN` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `WAREH` INTEGER(25) UNSIGNED,
 MODIFY COLUMN `WATER` INTEGER(25) UNSIGNED;

ALTER TABLE `table_temp`.`itemized_chart` ADD INDEX `gencat`(`general_category`);

CREATE TABLE subdivision_assessment_4
SELECT a.parent_parcel, a.child_parcel, a.numparents, a.GIS_area_sf, a.GIS_area_acres, a.Land_Use, a.Zoning, a.LandUseDescription, a.GenericLandUse1, a.GenericLandUse2, a.res_nonres, b.AGRIC, b.CIVIC, b.COMME, b.FISHE, b.FORES, b.GOVER, b.GROUP AS GRP, b.HOSPI, b.INDUS, b.MININ, b.MOBIL, b.MULTI, b.NOCODE, b.OFFIC, b.OUTBU, b.PARK, b.PARKI, b.RECRE, b.RIGHT AS RGHT, b.SCHOO, b.SINGL, b.TRANS, b.VACAN, b.WAREH, b.WATER, (b.AGRIC * a.GIS_area_sf) AS AGRICarea, (b.CIVIC * a.GIS_area_sf) AS CIVICarea, (b.COMME * a.GIS_area_sf) AS COMMEarea, (b.FISHE * a.GIS_area_sf) AS FISHEarea, (b.FORES * a.GIS_area_sf) AS FORESarea, (b.GOVER * a.GIS_area_sf) AS GOVERarea, (b.GROUP * a.GIS_area_sf) AS GROUParea, (b.HOSPI * a.GIS_area_sf) AS HOSPIarea, (b.INDUS * a.GIS_area_sf) AS INDUSarea, (b.MININ * a.GIS_area_sf) AS MININarea, (b.MOBIL * a.GIS_area_sf) AS MOBILarea, (b.MULTI * a.GIS_area_sf) AS MULTIarea, (b.NOCODE * a.GIS_area_sf) AS NOCODEarea, (b.OFFIC * a.GIS_area_sf) AS OFFICarea, (b.OUTBU * a.GIS_area_sf) AS OUTBUarea, (b.PARK * a.GIS_area_sf) AS PARKarea, (b.PARKI * a.GIS_area_sf) AS PARKIarea, (b.RECRE * a.GIS_area_sf) AS RECREarea, (b.RIGHT * a.GIS_area_sf) AS RIGHTarea, (b.SCHOO * a.GIS_area_sf) AS SCHOOarea, (b.SINGL * a.GIS_area_sf) AS SINGLarea, (b.TRANS * a.GIS_area_sf) AS TRANSarea, (b.VACAN * a.GIS_area_sf) AS VACANarea, (b.WAREH * a.GIS_area_sf) AS WAREHarea, (b.WATER * a.GIS_area_sf) AS WATERarea
FROM subdivision_assessment_3 a
LEFT JOIN table_temp.itemized_chart b ON b.general_category = a.GenericLandUse1;

CREATE TABLE subdivision_assessment_5
SELECT parent_parcel, numparents AS totalchildren, sum(AGRIC),sum(CIVIC),sum(COMME),sum(FISHE),sum(FORES),sum(GOVER),sum(GRP),sum(HOSPI),sum(INDUS),sum(MININ),sum(MOBIL),sum(MULTI),sum(NOCODE),sum(OFFIC),sum(OUTBU),sum(PARK),sum(PARKI),sum(RECRE),sum(RGHT),sum(SCHOO),sum(SINGL),sum(TRANS),sum(VACAN),sum(WAREH),sum(AGRICarea),sum(CIVICarea),sum(COMMEarea),sum(FISHEarea),sum(FORESarea),sum(GOVERarea),sum(GROUParea),sum(HOSPIarea),sum(INDUSarea),sum(MININarea),sum(MOBILarea),sum(MULTIarea),sum(NOCODEarea),sum(OFFICarea),sum(OUTBUarea),sum(PARKarea),sum(PARKIarea),sum(RECREarea),sum(RIGHTarea),sum(SCHOOarea),sum(SINGLarea),sum(TRANSarea),sum(VACANarea),sum(WAREHarea)
FROM subdivision_assessment_4
GROUP BY parent_parcel;

CREATE TABLE subdivision_assessment_6
SELECT *, IFNULL((`sum(MOBILarea)`/`sum(MOBIL)`),0) AS avgMOBIL, IFNULL((`sum(MULTIarea)`/`sum(MULTI)`),0) AS avgMULTI, IFNULL((`sum(SINGLarea)`/`sum(SINGL)`),0) AS avgSINGL
FROM subdivision_assessment_5;

CREATE TABLE subdivision_assessment_7
SELECT a.*, b.GIS_area_sf AS original_area_sf, b.generic_land_use_1 AS original_land_use, 1 AS EventFlag
FROM subdivision_assessment_6 a
LEFT JOIN all_parceldata_spatial_2001_final b ON a.parent_parcel = b.ID_PARCEL
WHERE a.`sum(SINGL)` > 0 AND b.GIS_area_sf  > 43560 AND a.avgSINGL < 500000 AND a.`sum(SINGL)` > 2 AND a.`sum(MOBIL)` = 0 AND a.`sum(MULTI)` = 0;



-- -------------------
-- Assessing parcels with new buildings; possible distribution of new lot sizes
-- -------------------

CREATE TABLE 2005_new_residential_presort_1
SELECT a.* FROM all_buildings_condensed_2005_final a
WHERE NumberofBuildingsParcel = 1 AND GeneralCategory = 'Single Family Residential' AND YearBuilt > 2001;
CREATE INDEX id_parcel USING BTREE ON 2005_new_residential_presort_1 (ID_PARCEL);

CREATE TABLE 2005_new_residential_parcels
SELECT a.*, b.GIS_area_sf, b.GIS_area_acres, b.Zoning, b.CityName, b.is_in_ugb, b.taz_id
FROM 2005_new_residential_presort_1 a
LEFT JOIN all_parceldata_spatial_2005_final b ON a.ID_PARCEL = b.ID_PARCEL
WHERE b.ID_PARCEL IS NOT NULL;

CREATE TABLE 2005_new_residential_parcels_final
SELECT a.*, b.drive_alone AS access_drive_alone, b.walk AS access_walk
FROM 2005_new_residential_parcels a
LEFT JOIN table_temp.travel_time_access b ON a.taz_id = b.taz_id;

CREATE INDEX id_parcel USING BTREE ON 2005_new_residential_parcels_final (ID_PARCEL);

CREATE TABLE 2001_new_residential_parcels
SELECT a.* FROM all_parceldata_spatial_2001_final a
WHERE Residential_Units = 1 AND generic_land_use_1 = 'Single Family Residential' AND Year_Built > 1995;

CREATE TABLE 2001_new_residential_parcels_final
SELECT a.*, b.drive_alone AS access_drive_alone, b.walk AS access_walk
FROM 2001_new_residential_parcels a
LEFT JOIN table_temp.travel_time_access b ON a.taz_id = b.taz_id;

CREATE INDEX id_parcel USING BTREE ON 2001_new_residential_parcels_final (ID_PARCEL);

DROP TABLE 2005_new_residential_presort_1;
DROP TABLE 2005_new_residential_parcels;
DROP TABLE 2001_new_residential_parcels;







-- --------------------
-- Tracking changes in plats?
-- --------------------

CREATE TABLE plats_2001
SELECT PlatName, COUNT(*) AS numprop FROM king_20011103.extr_parcel e WHERE PlatName IS NOT NULL GROUP BY PlatName;

CREATE INDEX platname USING BTREE ON plats_2001 (PlatName);

CREATE TABLE plats_2005
SELECT PlatName, COUNT(*) AS numprop FROM king_20051216.extr_parcel e WHERE PlatName IS NOT NULL GROUP BY PlatName;

CREATE INDEX platname USING BTREE ON plats_2005 (PlatName);

CREATE TABLE new_plats_2005
SELECT a.PlatName, a.numprop FROM plats_2005 a
LEFT JOIN plats_2001 b ON a.PlatName = b.PlatName WHERE b.PlatName IS NULL;

SELECT * FROM new_plats_2005 n WHERE numprop > 1;

CREATE INDEX platname USING BTREE ON new_plats_2005 (PlatName);

CREATE TABLE new_plats_with_parcels_2005
SELECT CONCAT(a.Major, a.Minor) AS PARCEL_ID, a.PlatName, a.PlatLot, a.SqFtLot, a.CurrentZoning, a.DistrictName, a.PresentUse, CONCAT('033', a.Major, a.Minor) AS ID_PARCEL
FROM king_20051216.extr_parcel a
LEFT JOIN new_plats_2005 b ON a.PlatName = b.PlatName
WHERE b.PlatName IS NOT NULL AND b.numprop > 1;

ALTER TABLE new_plats_with_parcels_2005 
MODIFY COLUMN ID_PARCEL VARCHAR(28) CHARACTER SET latin1 COLLATE latin1_swedish_ci;

CREATE INDEX id_parcel USING BTREE ON new_plats_with_parcels_2005 (ID_PARCEL);

CREATE TABLE new_plats_with_parcels_joined_2005
SELECT b.ID_PARCEL, a.* FROM new_plats_with_parcels_2005 a
LEFT JOIN all_parceldata_spatial_2005_final b ON a.ID_PARCEL = b.ID_PARCEL;

-- -------------------
-- Summary stats for TAZs
-- -------------------

CREATE TABLE temp_2001_taz_aggregation_1
SELECT taz_id, 
SUM(Land_Value)/SUM(GIS_area_sf) AS average_land_price, 
SUM(IF(generic_land_use_2 = 'R',GIS_area_sf,0))/SUM(GIS_area_sf) AS residential_area_proportion,
SUM(IF(generic_land_use_2 = 'C',GIS_area_sf,0))/SUM(GIS_area_sf) AS commercial_area_proportion,
SUM(IF(generic_land_use_2 = 'I',GIS_area_sf,0))/SUM(GIS_area_sf) AS industrial_area_proportion,
SUM(IF(generic_land_use_2 = 'G',GIS_area_sf,0))/SUM(GIS_area_sf) AS government_area_proportion,
SUM(IF(generic_land_use_2 = 'NR',GIS_area_sf,0))/SUM(GIS_area_sf) AS nonresidential_area_proportion,
SUM(IF(generic_land_use_1 = 'Vacant',GIS_area_sf,0))/SUM(GIS_area_sf) AS vacant_area_proportion,
SUM(IF(generic_land_use_1 = 'Agriculture',GIS_area_sf,0))/SUM(GIS_area_sf) AS agriculture_area_proportion, 
SUM(IF(generic_land_use_1 = 'Park and Open Space',GIS_area_sf,0))/SUM(GIS_area_sf) AS open_space_area_proportion,
SUM(IF(Tax_Exempt = 1,GIS_area_sf,0))/SUM(GIS_area_sf) AS tax_exempt_proportion,
SUM(IF(Undevelopable = 1,GIS_area_sf,0))/SUM(GIS_area_sf) AS undevelopable_proportion,
IFNULL(AVG(IF(Year_Built < 1800, NULL, Year_Built)),0) AS average_year_built,
SUM(Built_SF)/SUM(GIS_area_sf) AS total_intensity,
IF(SUM(IF(generic_land_use_2 = 'R',GIS_area_sf,0)) > 0, SUM(IF(generic_land_use_2 = 'R',Built_SF,0))/SUM(IF(generic_land_use_2 = 'R',GIS_area_sf,0)), 0)  AS residential_intensity,
IF(SUM(IF(generic_land_use_2 = 'C',GIS_area_sf,0)) > 0, SUM(IF(generic_land_use_2 = 'C',Built_SF,0))/SUM(IF(generic_land_use_2 = 'C',GIS_area_sf,0)), 0)  AS commercial_intensity,
IF(SUM(IF(generic_land_use_2 = 'I',GIS_area_sf,0)) > 0, SUM(IF(generic_land_use_2 = 'I',Built_SF,0))/SUM(IF(generic_land_use_2 = 'I',GIS_area_sf,0)), 0)  AS industrial_intensity,
IF(SUM(IF(generic_land_use_2 = 'G',GIS_area_sf,0)) > 0, SUM(IF(generic_land_use_2 = 'G',Built_SF,0))/SUM(IF(generic_land_use_2 = 'G',GIS_area_sf,0)), 0)  AS government_intensity,
SUM(Residential_Units)/SUM(GIS_area_acres) AS residential_density_per_acre
FROM all_parceldata_spatial_2001_final
GROUP BY taz_id;

CREATE TABLE temp_2001_taz_aggregation_2
SELECT a.*, b.drive_alone
FROM temp_2001_taz_aggregation_1 a
LEFT JOIN table_temp.travel_time_access b ON a.taz_id = b.taz_id;

CREATE TABLE dc_development_numbers
SELECT taz_id,
SUM(IF(GROUP2 = 1,1,0)) AS GROUP21,
SUM(IF(GROUP2 = 2,1,0)) AS GROUP22,
SUM(IF(GROUP5 = 1,1,0)) AS GROUP51,
SUM(IF(GROUP5 = 2,1,0)) AS GROUP52,
SUM(IF(GROUP5 = 3,1,0)) AS GROUP53,
SUM(IF(GROUP5 = 4,1,0)) AS GROUP54,
SUM(IF(GROUP5 = 5,1,0)) AS GROUP55
FROM table_temp.new_housing GROUP BY taz_id;




CREATE TABLE kitsapplats
SELECT x.* FROM
(SELECT CONCAT('035',TRUNCATE(RP_ACCT_ID,0)) AS RP_ACCT_ID, CONCAT('035',LEFT(ACCT_NO,LOCATE('-',ACCT_NO)-1)) as PLAT_ID FROM kitsap_20051230.main m WHERE LEFT(ACCT_NO,1) <> '9'
UNION
SELECT CONCAT('035', TRUNCATE(RP_ACCT_ID,0)) AS RP_ACCT_ID, CONCAT('035',LEFT(ACCT_NO,LOCATE('-',ACCT_NO)-1)) as PLAT_ID FROM kitsap_20060323.main m WHERE LEFT(ACCT_NO,1) <> '9') x
GROUP BY RP_ACCT_ID, PLAT_ID;


CREATE TEMPORARY TABLE revised_parcels
SELECT a.*, IF(County <> '035', LEFT(ID_PARCEL,9), '') AS PLAT_ID_1 FROM workspace.all_parcels_gis a;

CREATE TEMPORARY TABLE revised_parcels_2
SELECT a.*, IF(a.PLAT_ID_1 = '', b.PLAT_ID, a.PLAT_ID_1) AS PLAT_ID
FROM revised_parcels a
LEFT JOIN kitsapplats b ON a.ID_PARCEL = b.RP_ACCT_ID;

CREATE TABLE all_parcels_gis_with_plats
SELECT County, PARCEL_ID, SUBSTRING(a.PLAT_ID,4,20) AS PLAT_ID, NumberofAccounts, LandValueParcel, ImprValueParcel, TaxExemptParcel, Jurisdiction, Size_Acres, Size_SF, Land_Use, Zoning, LandUseDescription, GenericLandUse1, GenericLandUse2, res_nonres, ID_PARCEL, a.PLAT_ID AS ID_PLAT, GIS_area_sf, GIS_area_acres, X_SP_HARN, Y_SP_HARN, X_SP, Y_SP, X_UTM, Y_UTM, grid_code, taz_id, block_id, CityName, is_in_ugb FROM revised_parcels_2 a;

ALTER TABLE all_parcels_gis_with_plats ADD ID INT UNSIGNED NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (ID);


