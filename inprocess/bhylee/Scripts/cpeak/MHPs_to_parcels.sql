use PSRC_parcels_kitsap;

update parcels a inner join PSRC_parcels_all_counties.mhps b
on a.parcel_id = b.pin and a.county = b.cnty
set a.RESIDENTIAL_UNITS = b.units_tot;

update parcels a inner join PSRC_parcels_all_counties.mhps b
on a.parcel_id = b.pin2 and a.county = b.cnty
set a.RESIDENTIAL_UNITS = b.units_tot;

use PSRC_parcels_king;

update parcels a inner join PSRC_parcels_all_counties.mhps b
on a.parcel_id = b.pin and a.county = b.cnty
set a.RESIDENTIAL_UNITS = b.units_tot;

update parcels a inner join PSRC_parcels_all_counties.mhps b
on a.parcel_id = b.pin2 and a.county = b.cnty
set a.RESIDENTIAL_UNITS = b.units_tot;

use PSRC_parcels_pierce;

update parcels a inner join PSRC_parcels_all_counties.mhps b
on a.parcel_id = b.pin and a.county = b.cnty
set a.RESIDENTIAL_UNITS = b.units_tot;

update parcels a inner join PSRC_parcels_all_counties.mhps b
on a.parcel_id = b.pin2 and a.county = b.cnty
set a.RESIDENTIAL_UNITS = b.units_tot;

use PSRC_parcels_snohomish;

update parcels a inner join PSRC_parcels_all_counties.mhps b
on a.mhp_id = b.pin and a.county = b.cnty
set a.RESIDENTIAL_UNITS = b.units_tot
where b.pin <> '';

update parcels a inner join PSRC_parcels_all_counties.mhps b
on a.mhp_id = b.pin2 and a.county = b.cnty
set a.RESIDENTIAL_UNITS = b.units_tot
where b.pin <> '';


