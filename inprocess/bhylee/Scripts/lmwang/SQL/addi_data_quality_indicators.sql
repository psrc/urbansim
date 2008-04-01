######### additional indicators at web page ##########
######http://trondheim.cs.washington.edu/cgi-bin/BaseQuicki/wiki.cgi?DataQualityIndicators  #####
#   It writes one line per county to the indicators table (indicators_runs), which should already exist.
##########
##Input: parcels,land_use_generic_reclass
##Output: inidicators_runs
##Run: in MySQL

###Parcels missing year built
create temporary table tmp_table1 (COUNTY text, NUM_PARCELS_MISSING_YEAR_BUILT int);
insert into tmp_table1(COUNTY, NUM_PARCELS_MISSING_YEAR_BUILT)
select COUNTY, count(*) from parcels where YEAR_BUILT is null group by COUNTY;

insert into indicators_runs (indicator_name, indicator_result, desired_result)
select concat("Rate of parcels missing year built - ", a.COUNTY), b.NUM_PARCELS_MISSING_YEAR_BUILT/count(a.parcel_id), "0.0" 
  from parcels a inner join tmp_table1 b on a.COUNTY=b.COUNTY
group by a.COUNTY;

drop table tmp_table1;

###Parcels with unreasonable year built
create temporary table tmp_table2 (COUNTY text, NUM_PARCELS_UNREASONABLE_YEAR_BUILT int);
insert into tmp_table2(COUNTY, NUM_PARCELS_UNREASONABLE_YEAR_BUILT)
select COUNTY, count(*) from parcels where YEAR_BUILT not between 1860 and 2003 group by COUNTY;

insert into indicators_runs (indicator_name, indicator_result, desired_result)
select concat("Rate of parcels with unreasonable year built - ", a.COUNTY), b.NUM_PARCELS_UNREASONABLE_YEAR_BUILT/count(a.parcel_id), "0.0" 
  from parcels a inner join tmp_table2 b on a.COUNTY=b.COUNTY
group by a.COUNTY;

drop table tmp_table2;

###Parcels missing zoning 
#lack of data

###Parcels with imputed land use
create temporary table tmp_table4 (COUNTY text, IMPUTED_LAND_USE_PARCELS int);
insert into tmp_table4(COUNTY, IMPUTED_LAND_USE_PARCELS)
select COUNTY, count(*) from parcels where IMPUTED_LAND_USE is not null group by COUNTY;

insert into indicators_runs (indicator_name, indicator_result, desired_result)
select concat("Rate of parcels with imputed land use - ", a.COUNTY), b.IMPUTED_LAND_USE_PARCELS/count(a.parcel_id), "0.0" 
  from parcels a inner join tmp_table4 b on a.COUNTY=b.COUNTY group by a.COUNTY;

drop table tmp_table4;

###Unit - land use integrity indicator
create temporary table tmp_table5 (COUNTY text, PARCELS int);
insert into tmp_table5(COUNTY, PARCELS)
select a.COUNTY, count(*) 
 from parcels a inner join land_use_generic_reclass b on a.COUNTY = b. COUNTY and a.land_use = b.county_land_use_code 
 where a.RESIDENTIAL_UNITS > 0 and (b.generic_land_use_1 = "Multi-Family Residential" or b.generic_land_use_1 = "Single Family Residential")  group by a.COUNTY;

create temporary table tmp_table6 (COUNTY text, PARCELS int);
insert into tmp_table6(COUNTY, PARCELS)
select a.COUNTY, count(*) 
 from parcels a inner join land_use_generic_reclass b on a.COUNTY = b. COUNTY and a.land_use = b.county_land_use_code 
 where b.res_nonres = "RES"  group by a.COUNTY;


insert into indicators_runs (indicator_name, indicator_result, desired_result)
select concat("Unit - land use integrity - ", a.COUNTY), a.PARCELS/b.PARCELS, "1.0" 
  from tmp_table5 a inner join tmp_table6 b on a.COUNTY=b.COUNTY group by a.COUNTY;

drop table tmp_table5;
drop table tmp_table6;

###Year built - land use integrity indicator

create temporary table tmp_table7 (COUNTY text, PARCELS int);
insert into tmp_table7(COUNTY, PARCELS)
select a.COUNTY, count(*) 
 from parcels a inner join land_use_generic_reclass b on a.COUNTY = b. COUNTY and a.land_use = b.county_land_use_code 
 where a.YEAR_BUILT is not null and b.generic_land_use_1 in ("Civic and Quasi-Public", "Commercial", "Government", "Group Quarters", "Hospital, Convalescent Center", "Industrial", "Multi-Family Residential", "Office", "Right-of-Way", "School", "Single Family Residential", "Transportation, Communication, Utilities", "Warehousing") group by a.COUNTY;


create temporary table tmp_table8 (COUNTY text, PARCELS int);
insert into tmp_table8(COUNTY, PARCELS)
select a.COUNTY, count(*) 
 from parcels a inner join land_use_generic_reclass b on a.COUNTY = b. COUNTY and a.land_use = b.county_land_use_code 
 where b.res_nonres = "RES"  group by a.COUNTY;

insert into indicators_runs (indicator_name, indicator_result, desired_result)
select concat("Year built - land use integrity - ", a.COUNTY), a.PARCELS/b.PARCELS, "1.0" 
  from tmp_table7 a inner join tmp_table8 b on a.COUNTY=b.COUNTY group by a.COUNTY;

drop table tmp_table7;
drop table tmp_table8;


###Improvement value - land use integrity

create temporary table tmp_table9 (COUNTY text, PARCELS int);
insert into tmp_table9(COUNTY, PARCELS)
select a.COUNTY, count(*) 
 from parcels a inner join land_use_generic_reclass b on a.COUNTY = b. COUNTY and a.land_use = b.county_land_use_code 
 where a.IMPROVEMENT_VALUE > 0 and b.generic_land_use_1 in ("Civic and Quasi-Public", "Commercial", "Government", "Group Quarters", "Hospital, Convalescent Center", "Industrial", "Multi-Family Residential", "Office", "Right-of-Way", "School", "Single Family Residential", "Transportation, Communication, Utilities", "Warehousing") group by a.COUNTY;


create temporary table tmp_table10 (COUNTY text, PARCELS int);
insert into tmp_table10(COUNTY, PARCELS)
select a.COUNTY, count(*) 
 from parcels a inner join land_use_generic_reclass b on a.COUNTY = b. COUNTY and a.land_use = b.county_land_use_code 
 where b.res_nonres = "RES"  group by a.COUNTY;

insert into indicators_runs (indicator_name, indicator_result, desired_result)
select concat("Improvement value - land use integrity - ", a.COUNTY), a.PARCELS/b.PARCELS, "1.0" 
  from tmp_table9 a inner join tmp_table10 b on a.COUNTY=b.COUNTY group by a.COUNTY;

drop table tmp_table9;
drop table tmp_table10;


###Parcels with street address 
create temporary table tmp_table11 (COUNTY text, PARCELCOUNT int);
insert into tmp_table11 (COUNTY, PARCELCOUNT)
select COUNTY, count(*) from parcels where STREET_NAME is not null and STREET_NUMBER is not null group by COUNTY;

insert into indicators_runs (indicator_name, indicator_result, desired_result)
select concat("Parcels with street address - ", a.COUNTY), b.PARCELCOUNT/count(a.parcel_id), "1.0" 
  from parcels a inner join tmp_table11 b on a.COUNTY=b.COUNTY
group by a.COUNTY;

drop table tmp_table11;

###Sqft-per-parcel by County by Land use
create temporary table tmp_tablea (COUNTY text, GENERIC_LAND_USE text, PARCELS int);
insert into tmp_tablea (COUNTY,GENERIC_LAND_USE, PARCELS)
select a.COUNTY, b.generic_land_use_2, count(*) 
  from parcels a inner join land_use_generic_reclass b on a.COUNTY = b. COUNTY and a.land_use = b.county_land_use_code group by a.county, b.generic_land_use_2;

create temporary table tmp_tableb (COUNTY text, GENERIC_LAND_USE text, SQFT int);
insert into tmp_tableb (COUNTY,GENERIC_LAND_USE, SQFT)
select a.COUNTY, b.generic_land_use_2, SUM(a.BUILT_SQFT) 
  from parcels a inner join land_use_generic_reclass b on a.COUNTY = b. COUNTY and a.land_use = b.county_land_use_code group by a.county, b.generic_land_use_2;

insert into indicators_runs (indicator_name, indicator_result, desired_result)
select concat("SqFt-per-parcel by County by Land Use - ", a.generic_land_use," - ", a.COUNTY), b.SQFT/a.PARCELS, "-" 
  from tmp_tablea a inner join tmp_tableb b on a.COUNTY=b.COUNTY and a.generic_land_use = b.generic_land_use;

drop table tmp_tablea;
drop table tmp_tableb;

###Sqft by County by Land use
insert into data_quality_indicators_cpeak.indicators_runs (indicator_name, indicator_result, desired_result)
select concat("Sqft by County by Land use - Land Use - ", b.generic_land_use_2," - ", a.COUNTY), sum(a.BUILT_SQFT), "-" 
  from parcels a inner join land_use_generic_reclass b on a.COUNTY = b. COUNTY and a.land_use = b.county_land_use_code group by a.county, b.generic_land_use_2;
