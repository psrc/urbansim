

library(foreign)

# Set file locations
parcel_gis_table.loc<-"W:/GIS_Data/PSRC/Parcels2005/2005_centroids.dbf"
parcel_id_lookup.loc<-"W:/GIS_Data/PSRC/Parcels2005/parcel_id.dbf"
indicator_table.loc<-"C:/urbansim_cache/psrc_parcel/run_2472.2007_05_03_12_50/indicators/parcel__tab__total_value.tab"

# Read in data
parcel_gis_table<-read.dbf(parcel_gis_table.loc)
parcel_id_lookup<-read.dbf(parcel_id_lookup.loc)
indicator_table<-read.delim(indicator_table.loc)

# Merge lookup table with gis data

parcel_gis_table.2<-merge(parcel_gis_table, parcel_id_lookup, by.x="parcelid", by.y="id_parcel")

# Merge observed prices with gis data

parcel_gis_table.3<-merge(parcel_gis_table.2, indicator_table, by.x="parcel_id", by.y="parcel_id")

#write.dbf(

