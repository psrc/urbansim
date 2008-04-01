####This script is used to standardize the street_type in parcels and employers table for
##job allocator;
##Input: employers, parcels
##Output: employers, parcels tables with STANDARDIZED_STREET_TYPE
##Run: in MySQL

#Standardized street type list:
#AVE: <- AVE; AV; AVENUE
#AV CT: <- AV CT; AVCT; AVE CT; AVENUE CT; AVENUE COURT 
#BLVD: <- BLVD; 
#CIR: <- CIR; CR; CIRCLE
#CT: <- CT,COURT,CRT;
#DR: <- DR; DRIVE
#HWY: <- HWY
#I: <- I;
#LN: <- LN; LA; LANE
#LOOP: <- LOOP; LP
#PKE: <- PKE
#PKWY: <- PKWY
#PL: <- PL; PLACE
#RD: <- RD; ROAD;
#ROUTE: <- ROUTE; RT
#ST: <- ST; STREET
#ST CT: <- ST CT: STCT; STREET CT; STREET COURT
#TCE: <- TER;
#TRL: <- TRL; TRAIL
#WALK: <- WALK
#WAY: <- WY; WAY
#[space]: <- NULL

##update parcels table

alter table parcels add STANDARDIZED_STREET_TYPE text;

update parcels set STANDARDIZED_STREET_TYPE = "AVE"
where STREET_TYPE = "AVE" or STREET_TYPE = "AV" or STREET_TYPE = "AVENUE";


update parcels set STANDARDIZED_STREET_TYPE = "AVE CT"
where STREET_TYPE = "AVE CT" or STREET_TYPE = "AV CT" or STREET_TYPE = "AVCT" 
  or STREET_TYPE = "AVENUE CT" or STREET_TYPE = "AVENUE COURT";


update parcels set STANDARDIZED_STREET_TYPE = "BLVD" 
where STREET_TYPE = "BLVD";

update parcels set STANDARDIZED_STREET_TYPE = "CIR"
where STREET_TYPE = "CIR" or STREET_TYPE = "CR" or STREET_TYPE = "CIRCLE";

update parcels set STANDARDIZED_STREET_TYPE = "CT"
where STREET_TYPE = "CT" or STREET_TYPE = "COURT" or STREET_TYPE = "CRT";

update parcels set STANDARDIZED_STREET_TYPE = "DR" 
where STREET_TYPE = "DR" or STREET_TYPE = "DRIVE";

update parcels set STANDARDIZED_STREET_TYPE = "HWY"
where STREET_TYPE = "HWY";

update parcels set STANDARDIZED_STREET_TYPE = "I"
where STREET_TYPE = "I";

update parcels set STANDARDIZED_STREET_TYPE = "LN" 
where STREET_TYPE = "LN" or STREET_TYPE = "LA" or STREET_TYPE = "LANE";

update parcels set STANDARDIZED_STREET_TYPE = "LOOP"
where STREET_TYPE = "LOOP";

update parcels set STANDARDIZED_STREET_TYPE = "PIER"
where STREET_TYPE = "PIER";

update parcels set STANDARDIZED_STREET_TYPE = "PKE"
where STREET_TYPE = "PKE";

update parcels set STANDARDIZED_STREET_TYPE = "PKWY"
where STREET_TYPE = "PKWY";

update parcels set STANDARDIZED_STREET_TYPE = "PL" 
where STREET_TYPE = "PL" or STREET_TYPE = "PLACE";

update parcels set STANDARDIZED_STREET_TYPE = "RD" 
where STREET_TYPE = "RD" or STREET_TYPE = "ROAD";

update parcels set STANDARDIZED_STREET_TYPE = "ROUTE"
where STREET_TYPE = "ROUTE" or STREET_TYPE = "RT";

update parcels set STANDARDIZED_STREET_TYPE = "ST" 
where STREET_TYPE = "ST" or STREET_TYPE = "STREET";

update parcels set STANDARDIZED_STREET_TYPE = "ST CT" 
where STREET_TYPE = "ST CT" or STREET_TYPE = "STCT" or STREET_TYPE = "STREET CT" 
  or STREET_TYPE = "STREET COURT";

update parcels set STANDARDIZED_STREET_TYPE = "TCE"
where STREET_TYPE = "TER";

update parcels set STANDARDIZED_STREET_TYPE = "TRL" 
where STREET_TYPE = "TRL" or STREET_TYPE = "TRAIL";

update parcels set STANDARDIZED_STREET_TYPE = "WALK"
where STREET_TYPE = "WALK";

update parcels set STANDARDIZED_STREET_TYPE = "WAY" 
where STREET_TYPE = "WAY" or STREET_TYPE = "WY";

#update parcels set STANDARDIZED_STREET_TYPE = " "
#where STREET_TYPE is NULL;

update parcels set STANDARDIZED_STREET_TYPE = " "
where STANDARDIZED_STREET_TYPE is NULL;


##update employers table

alter table employers add STANDARDIZED_STREET_TYPE text;

update employers set STANDARDIZED_STREET_TYPE = "AVE"
where STREET_TYPE = "AVE" or STREET_TYPE = "AV" or STREET_TYPE = "AVENUE";


update employers set STANDARDIZED_STREET_TYPE = "AVE CT"
where STREET_TYPE = "AVE CT" or STREET_TYPE = "AV CT" or STREET_TYPE = "AVCT" 
  or STREET_TYPE = "AVENUE CT" or STREET_TYPE = "AVENUE COURT";


update employers set STANDARDIZED_STREET_TYPE = "BLVD" 
where STREET_TYPE = "BLVD";

update employers set STANDARDIZED_STREET_TYPE = "CIR"
where STREET_TYPE = "CIR" or STREET_TYPE = "CR" or STREET_TYPE = "CIRCLE";

update employers set STANDARDIZED_STREET_TYPE = "CT"
where STREET_TYPE = "CT" or STREET_TYPE = "COURT" or STREET_TYPE = "CRT";

update employers set STANDARDIZED_STREET_TYPE = "DR" 
where STREET_TYPE = "DR" or STREET_TYPE = "DRIVE";

update employers set STANDARDIZED_STREET_TYPE = "HWY"
where STREET_TYPE = "HWY";

update employers set STANDARDIZED_STREET_TYPE = "I"
where STREET_TYPE = "I";

update employers set STANDARDIZED_STREET_TYPE = "LN" 
where STREET_TYPE = "LN" or STREET_TYPE = "LA" or STREET_TYPE = "LANE";

update employers set STANDARDIZED_STREET_TYPE = "LOOP"
where STREET_TYPE = "LOOP";

update employers set STANDARDIZED_STREET_TYPE = "PIER"
where STREET_TYPE = "PIER";

update employers set STANDARDIZED_STREET_TYPE = "PKE"
where STREET_TYPE = "PKE";

update employers set STANDARDIZED_STREET_TYPE = "PKWY"
where STREET_TYPE = "PKWY";

update employers set STANDARDIZED_STREET_TYPE = "PL" 
where STREET_TYPE = "PL" or STREET_TYPE = "PLACE";

update employers set STANDARDIZED_STREET_TYPE = "RD" 
where STREET_TYPE = "RD" or STREET_TYPE = "ROAD";

update employers set STANDARDIZED_STREET_TYPE = "ROUTE"
where STREET_TYPE = "ROUTE" or STREET_TYPE = "RT";

update employers set STANDARDIZED_STREET_TYPE = "ST" 
where STREET_TYPE = "ST" or STREET_TYPE = "STREET";

update employers set STANDARDIZED_STREET_TYPE = "ST CT" 
where STREET_TYPE = "ST CT" or STREET_TYPE = "STCT" or STREET_TYPE = "STREET CT" 
  or STREET_TYPE = "STREET COURT";

update employers set STANDARDIZED_STREET_TYPE = "TCE"
where STREET_TYPE = "TER";

update employers set STANDARDIZED_STREET_TYPE = "TRL" 
where STREET_TYPE = "TRL" or STREET_TYPE = "TRAIL";

update employers set STANDARDIZED_STREET_TYPE = "WALK"
where STREET_TYPE = "WALK";

update employers set STANDARDIZED_STREET_TYPE = "WAY" 
where STREET_TYPE = "WAY" or STREET_TYPE = "WY";

#update employers set STANDARDIZED_STREET_TYPE = " "
#where STREET_TYPE is NULL;

update employers set STANDARDIZED_STREET_TYPE = " "
where STANDARDIZED_STREET_TYPE is NULL;
