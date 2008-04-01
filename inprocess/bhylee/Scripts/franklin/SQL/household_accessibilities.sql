drop table if exists household_accessibilities;
create table household_accessibilities
     select hh.year as year,
          hh.household_id as hhid,
          ac.home_access_to_employment_1 as hae1
     from households_exported as hh
     inner join accessibilities as ac
          on hh.year=ac.year
               and hh.zone_id=ac.zone_id;

     create index household_accessibilities_year_index 
          on household_accessibilities (year);
