#
#  UrbanSim software.
#  Copyright (C) 1998-2003 University of Washington
#  
#  You can redistribute this program and/or modify it under the
#  terms of the GNU General Public License as published by the
#  Free Software Foundation (http://www.gnu.org/copyleft/gpl.html).
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  file LICENSE.htm for copyright and licensing information, and the
#  file ACKNOWLEDGMENTS.htm for funding and other acknowledgments.
#
#  Author: Chris Peak


### King County 

USE job_allocation_king;

Alter table final_employers_matched_to_parcels add column COUNTY varchar(4);
Alter table employers add column COUNTY varchar(4);
Alter table parcels add column COUNTY varchar(4);

update final_employers_matched_to_parcels set COUNTY = '033';
update employers set COUNTY = '033';
update parcels set COUNTY = '033';

### Kitsap County 

USE job_allocation_kitsap;

Alter table final_employers_matched_to_parcels add column COUNTY varchar(4);
Alter table employers add column COUNTY varchar(4);
Alter table parcels add column COUNTY varchar(4);

update final_employers_matched_to_parcels set COUNTY = '035';
update employers set COUNTY = '035';
update parcels set COUNTY = '035';

### Pierce County 

USE job_allocation_pierce;

Alter table final_employers_matched_to_parcels add column COUNTY varchar(4);
Alter table employers add column COUNTY varchar(4);
Alter table parcels add column COUNTY varchar(4);

update final_employers_matched_to_parcels set COUNTY = '053';
update employers set COUNTY = '053';
update parcels set COUNTY = '053';


### Snohomish County 

USE job_allocation_snohomish;

Alter table final_employers_matched_to_parcels add column COUNTY varchar(4);
Alter table employers add column COUNTY varchar(4);
Alter table parcels add column COUNTY varchar(4);


update final_employers_matched_to_parcels set COUNTY = '061';
update employers set COUNTY = '061';
update parcels set COUNTY = '061';

### Collate tables in PSRC_job_allocation_all_counties database.

USE PSRC_job_allocation_all_counties;

DROP TABLE final_employers_matched_to_parcels;
DROP TABLE employers;
DROP TABLE parcels;

CREATE TABLE final_employers_matched_to_parcels 
SELECT * from job_allocation_king.final_employers_matched_to_parcels;

CREATE TABLE parcels 
SELECT * from job_allocation_king.parcels;

CREATE TABLE employers 
SELECT * from job_allocation_king.employers;

ALTER TABLE final_employers_matched_to_parcels add index prcl_indx (parcel_id(10));
ALTER TABLE final_employers_matched_to_parcels add index emp_indx (employer_id(13));
ALTER TABLE parcels add index prcl_indx (parcel_id(10));
ALTER TABLE employers add index emp_indx (employer_id(13));


# Get Kitsap's records
INSERT INTO final_employers_matched_to_parcels 
	(EMPLOYER_ID, PARCEL_ID, CENSUS_BLOCK, DECISION, COUNTY)
SELECT EMPLOYER_ID, PARCEL_ID, CENSUS_BLOCK, DECISION, COUNTY
FROM job_allocation_kitsap.final_employers_matched_to_parcels;

INSERT INTO parcels
	(COUNTY,
	PARCEL_ID, 
	LAND_USE, 
	SQUARE_FOOTAGE,
	CENSUS_BLOCK)
SELECT COUNTY, PARCEL_ID, LAND_USE, SQUARE_FOOTAGE, CENSUS_BLOCK
FROM job_allocation_kitsap.parcels;

INSERT INTO employers
	(COUNTY, 
	EMPLOYER_ID,
	CENSUS_BLOCK,
	SECTOR,
	NUMBER_OF_JOBS,
	SIC)
SELECT COUNTY, EMPLOYER_ID, CENSUS_BLOCK, SECTOR, NUMBER_OF_JOBS, SIC
FROM job_allocation_kitsap.employers;


# Get Pierce's records
INSERT INTO final_employers_matched_to_parcels 
	(EMPLOYER_ID, PARCEL_ID, CENSUS_BLOCK, DECISION, COUNTY)
SELECT EMPLOYER_ID, PARCEL_ID, CENSUS_BLOCK, DECISION, COUNTY
FROM job_allocation_pierce.final_employers_matched_to_parcels;

INSERT INTO parcels
	(COUNTY,
	PARCEL_ID, 
	LAND_USE, 
	SQUARE_FOOTAGE,
	CENSUS_BLOCK)
SELECT COUNTY, PARCEL_ID, LAND_USE, SQUARE_FOOTAGE, CENSUS_BLOCK
FROM job_allocation_pierce.parcels;

INSERT INTO employers
	(COUNTY, 
	EMPLOYER_ID,
	CENSUS_BLOCK,
	SECTOR,
	NUMBER_OF_JOBS,
	SIC)
SELECT COUNTY, EMPLOYER_ID, CENSUS_BLOCK, SECTOR, NUMBER_OF_JOBS, SIC
FROM job_allocation_pierce.employers;


# Get Snohomish's records
INSERT INTO final_employers_matched_to_parcels 
	(EMPLOYER_ID, PARCEL_ID, CENSUS_BLOCK, DECISION, COUNTY)
SELECT EMPLOYER_ID, PARCEL_ID, CENSUS_BLOCK, DECISION, COUNTY
FROM job_allocation_snohomish.final_employers_matched_to_parcels;

INSERT INTO parcels
	(COUNTY,
	PARCEL_ID, 
	LAND_USE, 
	SQUARE_FOOTAGE,
	CENSUS_BLOCK)
SELECT COUNTY, PARCEL_ID, LAND_USE, SQUARE_FOOTAGE, CENSUS_BLOCK
FROM job_allocation_snohomish.parcels;

INSERT INTO employers
	(COUNTY, 
	EMPLOYER_ID,
	CENSUS_BLOCK,
	SECTOR,
	NUMBER_OF_JOBS,
	SIC)
SELECT COUNTY, EMPLOYER_ID, CENSUS_BLOCK, SECTOR, NUMBER_OF_JOBS, SIC
FROM job_allocation_snohomish.employers;



