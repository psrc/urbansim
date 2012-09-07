# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
           "resacre = zone.aggregate((parcel.shape_area*0.000247105381)*((parcel.shape_area*0.000247105381)<5)*parcel.aggregate(building.residential_units>0))",
           "ciacre = zone.aggregate((parcel.shape_area*0.000247105381)*parcel.aggregate(building.non_residential_sqft>0))",
           "taz = zone.zone_id",
           ##HACK, as the county_id in counties is meaningless and cannot be related to any zone attribute
           "county_id = zone.aggregate(parcel.county_id, function=median)", 
           "alldata_id = 1 + (zone.zone_id * 0)",
           "number_of_jobs = zone.aggregate(establishment.employees, intermediates=[building,parcel])",
           "employment =  zone.aggregate(establishment.employees, intermediates=[building,parcel])",
           "sectorelevenjobs = zone.aggregate(establishment.employees*(establishment.sector_id==11), intermediates=[building,parcel])",
           "sector21jobs = zone.aggregate(establishment.employees*(establishment.sector_id==21), intermediates=[building,parcel])",
           "sector22jobs = zone.aggregate(establishment.employees*(establishment.sector_id==22), intermediates=[building,parcel])",
           "constructionjobs = zone.aggregate(establishment.employees*(establishment.sector_id==23), intermediates=[building,parcel])",
           "manufonejobs = zone.aggregate(establishment.employees*(establishment.sector_id==31), intermediates=[building,parcel])",
           "manuftwojobs = zone.aggregate(establishment.employees*(establishment.sector_id==32), intermediates=[building,parcel])",
           "manufthreejobs = zone.aggregate(establishment.employees*(establishment.sector_id==33), intermediates=[building,parcel])",
           "wholesalejobs = zone.aggregate(establishment.employees*(establishment.sector_id==42), intermediates=[building,parcel])",
           "sector44jobs = zone.aggregate(establishment.employees*(establishment.sector_id==44), intermediates=[building,parcel])",
           "sector45jobs = zone.aggregate(establishment.employees*(establishment.sector_id==45), intermediates=[building,parcel])",
           "transportjobs = zone.aggregate(establishment.employees*(establishment.sector_id==48), intermediates=[building,parcel])",
           "warehousejobs = zone.aggregate(establishment.employees*(establishment.sector_id==49), intermediates=[building,parcel])",
           "sector51jobs = zone.aggregate(establishment.employees*(establishment.sector_id==51), intermediates=[building,parcel])",
           "sector52jobs = zone.aggregate(establishment.employees*(establishment.sector_id==52), intermediates=[building,parcel])",
           "realestatejobs = zone.aggregate(establishment.employees*(establishment.sector_id==53), intermediates=[building,parcel])",
           "professionaljobs = zone.aggregate(establishment.employees*(establishment.sector_id==54), intermediates=[building,parcel])",
           "managementjobs = zone.aggregate(establishment.employees*(establishment.sector_id==55), intermediates=[building,parcel])",
           "adminjobs = zone.aggregate(establishment.employees*(establishment.sector_id==56), intermediates=[building,parcel])",
           "sector61jobs = zone.aggregate(establishment.employees*(establishment.sector_id==61), intermediates=[building,parcel])",
           "sector62jobs = zone.aggregate(establishment.employees*(establishment.sector_id==62), intermediates=[building,parcel])",
           "sector71jobs = zone.aggregate(establishment.employees*(establishment.sector_id==71), intermediates=[building,parcel])",
           "sector72jobs = zone.aggregate(establishment.employees*(establishment.sector_id==72), intermediates=[building,parcel])",
           "sector81jobs = zone.aggregate(establishment.employees*(establishment.sector_id==81), intermediates=[building,parcel])",
           "sector92jobs = zone.aggregate(establishment.employees*(establishment.sector_id==92), intermediates=[building,parcel])",
           "sector7211jobs = zone.aggregate(establishment.employees*(establishment.sector_id==7211), intermediates=[building,parcel])",
           "sector7212jobs = zone.aggregate(establishment.employees*(establishment.sector_id==7212), intermediates=[building,parcel])",
           "sector7213jobs = zone.aggregate(establishment.employees*(establishment.sector_id==7213), intermediates=[building,parcel])",
           "sector7221jobs = zone.aggregate(establishment.employees*(establishment.sector_id==7221), intermediates=[building,parcel])",
           "sector7222jobs = zone.aggregate(establishment.employees*(establishment.sector_id==7222), intermediates=[building,parcel])",
           "sector7223jobs = zone.aggregate(establishment.employees*(establishment.sector_id==7223), intermediates=[building,parcel])",
           "sector7224jobs = zone.aggregate(establishment.employees*(establishment.sector_id==7224), intermediates=[building,parcel])",
           "population = zone.aggregate(household.persons,intermediates=[building,parcel])",
]
