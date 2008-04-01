

library(RMySQL)
library(foreign)

cnx_bldg <- dbConnect(dbDriver("MySQL"), 
                      host="trondheim.cs.washington.edu",
                      user="urbansim",
                      password="UwmYsqlAt.5",
                      dbname="psrc_2005_data_workspace")

bldg_coll <- dbReadTable(cnx_bldg, "all_buildings_collapsed", row.names=NULL)


parcelpt <- read.dbf("W:/GIS_Data/PSRC/Parcel/merged/point_Spatia1.dbf")
parcelpt <- read.spss("N:/PSRC/dev_constr/parcels_with_regflu.sav", 
                      to.data.frame=TRUE, max.value.labels=1000)
                      
# Read parcel-comp plan file into MySQL

q.result <- dbSendQuery(conn=cnx_bldg,
                        paste("create table all_parcels_with_cplan_jpf ",
                              "(parc_ce int, ",
                              " parc_ce1 int, ",
                              " parc_id char(16), ",
                              " county char(3), ",
                              " inurbctr int, ",
                              " regf_ce int, ",
                              " regf_ce1 int, ",
                              " genuse char(4), ",
                              " desc_ char(50), ",
                              " resdenl int, ",
                              " resdenh int);",
                              sep=""))

q.result <- dbSendQuery(conn=cnx_bldg,
                        paste("load data infile 'parcels_with_regflu.tab' ",
                              "into table all_parcels_with_cplan_jpf;",sep=""))

q.result <- dbSendQuery(conn=cnx_bldg, "create index apwcpjpf_county_parcel_id on all_parcels_with_cplan_jpf (county, parc_id);")

# Aggregate building parts to parcels

q.result <- dbSendQuery(conn=cnx_bldg, 
                        paste("create table all_buildings_by_parcel_jpf ",
                              "select PARCEL_ID, ",
                                      "min(County) as County, ",
                                      "group_concat(BuildingUseCode) as BuildingUseCodes, ",
                                      "sum(BldgSF) as BldgSF, ",
                                      "avg(Stories) as Stories, ",
                                      "sum(Footprint) as Footprint, ",
                                      "max(YearBuilt) as YearBuilt, ",
                                      "sum(NumberofUnits) as NumberofUnits, ",
                                      "sum(Bedrooms) as Bedrooms, ",
                                      "sum(BathFull) as BathFull, ",
                                      "sum(Bath3Qtr) as Bath3Qtr, ",
                                      "sum(BathHalf) as BathHalf, ",
                                      "sum(Bathrooms) as Bathrooms, ",
                                      "group_concat(BuildingUseDescription) as BuildingUseDescriptions, ",
                                      "group_concat(GeneralCategory) as GeneralCategories, ",
                                      "sum(NumberofBuildingsParcel) as NumberofBuildingsParcel, ",
                                      "sum(NumberofOutbuildingsParcel) as NumberofOutbuildingsParcel ",
                               "from all_buildings_collapsed ",
                               "group by PARCEL_ID;",sep=""))

q.result <- dbSendQuery(conn=cnx_bldg, "create index abbpjpf_county_parcel_id on all_buildings_by_parcel_jpf (County, PARCEL_ID);")

q.result <- dbSendQuery(conn=cnx_bldg, "delete from all_buildings_by_parcel_jpf where PARCEL_ID=\"0\";")

#parcelbg <- dbReadTable(cnx_bldg, "all_buildings_by_parcel_jpf", row.names=NULL)


#parcelbg <- aggregate(bldg_coll, by=list(ParcelID = bldg_coll$AccountID), FUN=sum)

# Merge parcelpt data into parcelbg


q.result <- dbSendQuery(conn=cnx_bldg,
                        paste("create table all_parcels_merged_jpf ",
                              "select bg.PARCEL_ID as PARCEL_ID, ",
                                     "bg.County as County, ",
                                     "bg.BuildingUseCodes as BuildingUseCodes, ",
                                     "bg.BldgSF as BldgSF, ",
                                     "bg.Stories as Stories, ",
                                     "bg.Footprint as Footprint, ",
                                     "bg.YearBuilt as YearBuilt, ",
                                     "bg.NumberofUnits as NumberofUnits, ",
                                     "bg.Bedrooms as Bedrooms, ",
                                     "bg.BathFull as BathFull, ",
                                     "bg.Bath3Qtr as Bath3Qtr, ",
                                     "bg.BathHalf as BathHalf, ",
                                     "bg.Bathrooms as Bathrooms, ",
                                     "bg.BuildingUseDescriptions as BuildingUseDescriptions, ",
                                     "bg.GeneralCategories as GeneralCategories, ",
                                     "bg.NumberofBuildingsParcel as NumberofBuildingsParcel, ",
                                     "bg.NumberofOutbuildingsParcel as NumberofOutbuildingsParcel, ",
                                     "pt.inurbctr as InUrbanCenter, ",
                                     "pt.genuse as GenericUse, ",
                                     "pt.desc_ as Description, ",
                                     "pt.resdenl as MinResDensity, ",
                                     "pt.resdenh as MaxResDensity, ",
                                     "pc.Size_Acres as SizeAcres, ",
                                     "pc.Size_SF as SizeSF ",
                                     "from all_buildings_by_parcel_jpf as bg ",
                                     "left join all_parcels_gis as pc ",
                                     "on bg.County = pc.County and bg.PARCEL_ID = pc.PARCEL_ID ",
                                     "left join all_parcels_with_cplan_jpf as pt ",
                                     "on bg.County = pt.County and bg.PARCEL_ID = pt.parc_id;",
                               sep=""))

# Merge 

#parcel.all <- merge(x=parcelpt, y=parcelbg, by.x="PARC_ID", by.y="PARCEL_ID")

# Read in merged table from MySQL

parcels <- dbReadTable(cnx_bldg, "all_parcels_merged_jpf", row.names=NULL)

# or export to file

q.result <- dbSendQuery(conn=cnx_bldg, "select * from all_parcels_merged_jpf into outfile 'parcels_merged.tab';")
