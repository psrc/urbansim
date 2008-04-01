#t1_bldgs2_GeneralCategory_freq
CREATE TABLE t1_bldgs2_GeneralCategory_freq
SELECT t.GeneralCategory, Count(*) AS Expr1
FROM template_buildings_2 AS t
GROUP BY t.GeneralCategory;

#t2_bldgs2_SFR_parcels
CREATE TABLE t2_bldgs2_SFR_parcels
SELECT t.ID_PARCEL, Count(*) AS Expr1
FROM template_buildings_2 AS t
WHERE t.GeneralCategory="Single Family Residential"
GROUP BY t.ID_PARCEL;

#t2_bldg2_SFR_parcels_1plus_bldg
CREATE TABLE t3_bldg2_SFR_parcels_1plus_bldg
SELECT t.*
FROM t2_bldgs2_SFR_parcels AS t
WHERE t.Expr1>1
ORDER BY t.Expr1 DESC;

#t3_parcels_GenericLandUse1
CREATE TABLE t1_parcels_GenericLandUse1
SELECT t.GenericLandUse1, Count(*) AS Expr1
FROM template_parcels AS t
GROUP BY t.GenericLandUse1;

#t3_parcels_SFR_unique
CREATE TABLE t3_parcels_SFR_unique
SELECT t.ID_PARCEL, Count(*) AS Expr1
FROM template_parcels AS t
WHERE t.GenericLandUse1="Single Family Residential"
GROUP BY t.ID_PARCEL;

#create index for template_buildings_2
CREATE INDEX ID
USING BTREE
ON template_buildings_2 (ID_SUBPARCEL,BuildingID);

#create index for template_parcels
CREATE INDEX ID
USING BTREE
ON template_parcels (ID_PARCEL);

#t4_bldgs2_parcel_SFR
CREATE TABLE t4_bldgs2_parcel_SFR
SELECT b.*, p.NumberofAccounts, p.LandValueParcel, p.ImprValueParcel, p.TaxExemptParcel, p.Jurisdiction,
p.Size_Acres, p.Land_Use, p.LandUseDescription, p.GenericLandUse1, p.GenericLandUse2, p.res_nonres,
p.GIS_area_sf, p.GIS_area_acres, p.X_SP_HARN, p.Y_SP_HARN, p.X_SP, p.Y_SP, p.X_UTM, p.Y_UTM, p.grid_code,
p.taz_id, p.block_id, p.CityName, p.is_in_ugb
FROM template_buildings_2 AS b INNER JOIN template_parcels AS p ON b.ID_PARCEL = p.ID_PARCEL
WHERE (p.GenericLandUse1="Single Family Residential" AND b.GeneralCategory="Single Family Residential");

#t4_bldgs2_parcel_SFR_uniq
CREATE TABLE t4_bldgs2_parcel_SFR_uniq
SELECT t.ID_PARCEL, Count(*) AS Expr1
FROM t4_bldgs2_parcel_SFR as t
GROUP BY t.ID_PARCEL
ORDER BY Count(*) DESC;
#create index
CREATE INDEX ID USING BTREE
ON t4_bldgs2_parcel_SFR_uniq (ID_PARCEL);

#t4_bldgs2_parcel_SFR_plus_SF_ACRE
CREATE TABLE t4_bldgs2_parcel_SFR_plus_SF_ACRE
SELECT t.*, IF(t.Size_SF>0,t.Size_SF,t.GIS_area_sf) AS parcel_sf,
IF(t.Size_Acres>0,t.Size_Acres,t.GIS_area_acres) AS parcel_acre
FROM t4_bldgs2_parcel_SFR AS t;

#t4_bldgs2_parcel_SFR_plus_SF_ACRE_clean
CREATE TABLE t4_bldgs2_parcel_SFR_plus_SF_ACRE_clean
SELECT t.*
FROM t4_bldgs2_parcel_SFR_plus_SF_ACRE AS t
WHERE t.parcel_sf>0 And t.parcel_acre>0 AND t.NumberofUnits<=1 AND t.BldgSF>=100 AND t.Stories<=3
AND t.Bedrooms<=10 AND t.Bathrooms<=10;
#create index
CREATE INDEX ID USING BTREE
ON t4_bldgs2_parcel_SFR_plus_SF_ACRE_clean (ID_SUBPARCEL, BuildingID);

#t5_bldgs2_parcel_SFR_clean
CREATE TABLE t5_bldgs2_parcel_SFR_clean
SELECT a.*
FROM t4_bldgs2_parcel_SFR_plus_SF_ACRE_clean AS a
INNER JOIN t4_bldgs2_parcel_SFR_uniq AS b ON a.ID_PARCEL=b.ID_PARCEL
WHERE b.Expr1=1;

#t6_bldgs2_parcel_plats
CREATE TABLE t6_bldgs2_parcel_plats
SELECT t.ID_PLAT, Count(*) AS PlatUnits, Avg(t.BldgSF) AS AvgBldgSF, Max(t.BldgSF) AS MaxBldgSF,
Min(t.BldgSF) AS MinBldgSF, Avg(t.Bedrooms) AS AvgBedrooms, Max(t.Bedrooms) AS MaxBedrooms,
Min(t.Bedrooms) AS MinBedrooms, Sum(t.parcel_sf) AS SumParcel_sf, Sum(t.parcel_acre) AS SumParcel_acre
FROM t5_bldgs2_parcel_SFR_clean AS t
GROUP BY t.ID_PLAT;

#t6_bldgs2_parcel_plats_UnitsPerAcre
CREATE TABLE t6_bldgs2_parcel_plats_UnitsPerAcre
SELECT t.*, (t.PlatUnits/t.SumParcel_acre) AS UnitsPerAcre
FROM t6_bldgs2_parcel_plats AS t;