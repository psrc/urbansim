
##  This script tabulates parcel_level data from the King County Assesor's extracts.
##  It works in the PSRC_king_assessors_cpeak database,
##    which contains the assessor's extract tables for King County.
##  After running this script, the new data must be copied to the parcels
##    table in PSRC_parcels_king.


USE PSRC_king_assessors_cpeak;


#############################################################
## Update parcel fields {RES_UNITS, SQFT, YEAR_BUILT} with AptComplex data

## Is this an appropriate way to get SQFT?
CREATE TEMPORARY TABLE tmp_apts
SELECT 
	Major, 
	Minor, 
	NbrUnits as UNITS, 
	(NbrUnits * AvgUnitSize) as SQFT,
	YrBuilt 
FROM AptComplex;

ALTER TABLE tmp_apts add index id1 (Major(6), Minor(4));

UPDATE Parcel p inner join tmp_apts a 
	ON p.major = a.major and p.minor = a.minor
SET 
	p.RES_UNITS = a.UNITS,
	p.SQFT = a.SQFT,
	p.YEAR_BUILT = a.YrBuilt;



##########################################################
## Update parcel fields {RES_UNITS, SQFT, YEAR_BUILT} with ResBldg data 

## Note: There are roughly 4000 duplicate major, minor combinations in ResBldg.  
##	 How to deal with this?  Sum living units and SqFt?  The queries below
## 	 sum living units and square footage, and take the highest year_built.

CREATE TEMPORARY TABLE tmp_resbldg
SELECT 
	Major, 
	Minor, 
	sum(NbrLivingUnits) as UNITS, 
	sum(SqFtTotLiving) as SQFT,
	max(YrBuilt) as YrBuilt
FROM ResBldg
GROUP BY Major, Minor;

ALTER TABLE tmp_resbldg add index id1 (Major(6), Minor(4));

UPDATE Parcel p inner join tmp_resbldg r 
	ON p.major = r.major and p.minor = r.minor
SET 
	p.RES_UNITS = r.UNITS,
	p.SQFT = r.SQFT,
	p.YEAR_BUILT = r.YrBuilt
WHERE p.PropType = 'R';


##############################################################
## Update parcel fields {RES_UNITS, SQFT, YEAR_BUILT} with Condo data

## How to make distinguish between res and nonres condos?  
##   Is this through the 'ComplexType' field?

# Get residential condos from CondoComplex table
CREATE TEMPORARY TABLE tmp_condos_residential
SELECT 
	Major, 
	NbrUnits as UNITS, 
	(NbrUnits * AvgUnitSize) as SQFT,
	YrBuilt
FROM CondoComplex
WHERE ComplexType <> 3 AND ComplexType <> 8;

# Get nonresidential condos from CondoComplex table
CREATE TEMPORARY TABLE tmp_condos_nonresidential
SELECT 
	Major, 
	(NbrUnits * AvgUnitSize) as SQFT,
	YrBuilt
FROM CondoComplex
WHERE ComplexType = 3 OR ComplexType = 8;

ALTER TABLE tmp_condos_residential add index id1 (Major(6));
ALTER TABLE tmp_condos_nonresidential add index id1 (Major(6));

# Update parcel table with residential condo data
UPDATE Parcel p inner join tmp_condos_residential a 
	ON p.major = a.major 
SET 
	p.RES_UNITS = a.UNITS,
	p.SQFT = a.SQFT,
	p.YEAR_BUILT = a.YrBuilt
WHERE p.PropType = 'K';

# Update parcel table with nonresidential condo data
UPDATE Parcel p inner join tmp_condos_nonresidential a 
	ON p.major = a.major 
SET 
	p.SQFT = a.SQFT,
	p.YEAR_BUILT = a.YrBuilt
WHERE p.PropType = 'K';


##############################################################
## Update parcel fields {RES_UNITS, SQFT, YEAR_BUILT} with CommBldg data

CREATE TEMPORARY TABLE tmp_commercial
SELECT 
	Major, 
	Minor, 
	sum(BldgNetSqFt) as SQFT,
	max(YrBuilt) as YrBuilt
FROM CommBldg
GROUP BY Major, Minor;

ALTER TABLE tmp_commercial add index id1 (Major(6), Minor(4));

UPDATE Parcel p INNER JOIN tmp_commercial c 
	ON p.major = c.major and p.minor = c.minor
SET 
	p.SQFT = c.SQFT,
	p.YEAR_BUILT = c.YrBuilt;

	
######################################################################
### Update parcel fields {LAND_VALUE, IMP_VALUE} from RPAcct table

## Get fields from condo records in RPAcct

CREATE TEMPORARY TABLE tmp_values_condos
SELECT
	a.Major,
	sum(a.ApprLandVal) as LAND_VALUE,
	sum(a.ApprImpsVal) as IMP_VALUE
FROM RPAcct a INNER JOIN Parcel p ON a.Major = p.Major
WHERE p.PropType  = 'K'
GROUP BY a.Major;	

ALTER TABLE tmp_values_condos ADD INDEX majindx (Major(6));

UPDATE Parcel p INNER JOIN tmp_values_condos v
	ON p.major = v.major 
SET 
	p.LAND_VALUE = v.LAND_VALUE,	
	p.IMP_VALUE = v.IMP_VALUE
WHERE p.PropType = 'K';
			

## Get fields from noncondo records in RPAcct
## Note: some PINs appear multiple times in this table, and their data are therefor
##   summed by Major and Minor.
CREATE TEMPORARY TABLE tmp_values_allpins
SELECT
	Major,
	Minor,
	sum(ApprLandVal) as LAND_VALUE,
	SUM(ApprImpsVal) as IMP_VALUE
FROM RPAcct
GROUP BY Major, Minor;

ALTER TABLE tmp_values_allpins add index id1 (Major(6), Minor(4));

UPDATE Parcel p INNER JOIN tmp_values_allpins v
	ON p.major = v.major and p.minor = v.minor
SET 
	p.LAND_VALUE = v.LAND_VALUE,	
	p.IMP_VALUE = v.IMP_VALUE;
		

DROP TABLE tmp_apts;
DROP TABLE tmp_resbldg;
DROP TABLE tmp_condos_residential;
DROP TABLE tmp_condos_nonresidential;
DROP TABLE tmp_commercial;
DROP TABLE tmp_values_condos;
DROP TABLE tmp_values_allpins;

## Remaining checks:
##	Link Condo RPAccts through CondoUnit table to check for inconsistencies.
##  Link Parcel to CommBldg on Major where proptype = 'K' to check for
##		inconsistencies with CondoComplex table.  If either join yields more records,
##  	that may be a better method of getting condo information.