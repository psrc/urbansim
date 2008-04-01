
load("N:\\PSRC\\dev_constr\\workspace.RData")

# Load full set of parcels

parcels.all<-read.delim("n:/psrc/dev_constr/parcels_merged.tab")

comp_plan_types<-aggregate(cbind(parcels.all$DU_AC,
                            parcels.all$FAR_SFR,
                            parcels.all$FAR_MFR,
                            parcels.all$FAR_COM,
                            parcels.all$FAR_IND,
                            parcels.all$FAR_GOV,
                            parcels.all$LTSZ_SFR), 
                      by=list(CPLANID = parcels.all$CPLANID),
                      FUN=quantile, probs=0.75, na.rm=TRUE)
comp_plan_types$DUAC.75   <-comp_plan_types$V1
comp_plan_types$FARSFR.75 <-comp_plan_types$V2
comp_plan_types$FARMFR.75 <-comp_plan_types$V3
comp_plan_types$FARCOM.75 <-comp_plan_types$V4
comp_plan_types$FARIND.75 <-comp_plan_types$V5
comp_plan_types$FARGOV.75 <-comp_plan_types$V6
comp_plan_types$LTSZSFR.75<-comp_plan_types$V7
comp_plan_types$V1<-NULL
comp_plan_types$V2<-NULL
comp_plan_types$V3<-NULL
comp_plan_types$V4<-NULL
comp_plan_types$V5<-NULL
comp_plan_types$V6<-NULL
comp_plan_types$V7<-NULL

# Normalize the.75th percentiles

comp_plan_types$DUAC.75.z<-comp_plan_types$DUAC.75/mean(comp_plan_types$DUAC.75)
comp_plan_types$FARSFR.75.z<-comp_plan_types$FARSFR.75/mean(comp_plan_types$FARSFR.75)
comp_plan_types$FARMFR.75.z<-comp_plan_types$FARMFR.75/mean(comp_plan_types$FARMFR.75)
comp_plan_types$FARCOM.75.z<-comp_plan_types$FARCOM.75/mean(comp_plan_types$FARCOM.75)
comp_plan_types$FARIND.75.z<-comp_plan_types$FARIND.75/mean(comp_plan_types$FARIND.75)
comp_plan_types$FARGOV.75.z<-comp_plan_types$FARGOV.75/mean(comp_plan_types$FARGOV.75)
comp_plan_types$LTSZSFR.75.z<-comp_plan_types$LTSZSFR.75/mean(comp_plan_types$LTSZSFR.75)

# Alternatively, first compute square roots...

comp_plan_types$DUAC.75.sr<-sqrt(comp_plan_types$DUAC.75)
comp_plan_types$FARSFR.75.sr<-sqrt(comp_plan_types$FARSFR.75)
comp_plan_types$FARMFR.75.sr<-sqrt(comp_plan_types$FARMFR.75)
comp_plan_types$FARCOM.75.sr<-sqrt(comp_plan_types$FARCOM.75)
comp_plan_types$FARIND.75.sr<-sqrt(comp_plan_types$FARIND.75)
comp_plan_types$FARGOV.75.sr<-sqrt(comp_plan_types$FARGOV.75)
comp_plan_types$LTSZSFR.75.sr<-sqrt(comp_plan_types$LTSZSFR.75)

# ...and then normalize.

comp_plan_types$DUAC.75.sr.z<-comp_plan_types$DUAC.75.sr/mean(comp_plan_types$DUAC.75.sr)
comp_plan_types$FARSFR.75.sr.z<-comp_plan_types$FARSFR.75.sr/mean(comp_plan_types$FARSFR.75.sr)
comp_plan_types$FARMFR.75.sr.z<-comp_plan_types$FARMFR.75.sr/mean(comp_plan_types$FARMFR.75.sr)
comp_plan_types$FARCOM.75.sr.z<-comp_plan_types$FARCOM.75.sr/mean(comp_plan_types$FARCOM.75.sr)
comp_plan_types$FARIND.75.sr.z<-comp_plan_types$FARIND.75.sr/mean(comp_plan_types$FARIND.75.sr)
comp_plan_types$FARGOV.75.sr.z<-comp_plan_types$FARGOV.75.sr/mean(comp_plan_types$FARGOV.75.sr)
comp_plan_types$LTSZSFR.75.sr.z<-comp_plan_types$LTSZSFR.75.sr/mean(comp_plan_types$LTSZSFR.75.sr[!is.na(comp_plan_types$LTSZSFR.75.sr)])

# Compute centroid distances

comp_plan_types$cl.20.d01<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[ 1,])^2)
comp_plan_types$cl.20.d02<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[ 2,])^2)
comp_plan_types$cl.20.d03<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[ 3,])^2)
comp_plan_types$cl.20.d04<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[ 4,])^2)
comp_plan_types$cl.20.d05<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[ 5,])^2)
comp_plan_types$cl.20.d06<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[ 6,])^2)
comp_plan_types$cl.20.d07<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[ 7,])^2)
comp_plan_types$cl.20.d08<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[ 8,])^2)
comp_plan_types$cl.20.d09<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[ 9,])^2)
comp_plan_types$cl.20.d10<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[10,])^2)
comp_plan_types$cl.20.d11<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[11,])^2)
comp_plan_types$cl.20.d12<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[12,])^2)
comp_plan_types$cl.20.d13<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[13,])^2)
comp_plan_types$cl.20.d14<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[14,])^2)
comp_plan_types$cl.20.d15<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[15,])^2)
comp_plan_types$cl.20.d16<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[16,])^2)
comp_plan_types$cl.20.d17<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[17,])^2)
comp_plan_types$cl.20.d18<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[18,])^2)
comp_plan_types$cl.20.d19<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[19,])^2)
comp_plan_types$cl.20.d20<-rowSums((comp_plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                             "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")]
                               - pt.cluster[[20]]$centers[20,])^2)

# Determine the shortest centroid distance

comp_plan_types$cl.20.dmin<-apply(comp_plan_types[,30:49], 1, min)

# Assign cluster membership based on the centroid with the shortest distance

comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d01] <- 01
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d02] <- 02
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d03] <- 03
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d04] <- 04
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d05] <- 05
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d06] <- 06
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d07] <- 07
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d08] <- 08
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d09] <- 09
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d10] <- 10
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d11] <- 11
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d12] <- 12
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d13] <- 13
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d14] <- 14
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d15] <- 15
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d16] <- 16
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d17] <- 17
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d18] <- 18
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d19] <- 19
comp_plan_types$GPTCODE[comp_plan_types$cl.20.dmin == comp_plan_types$cl.20.d20] <- 20

labs<-c("Low Density Single Family", #1
        "Undevelopable", #2
        "Very Low Density Single Family", #3
        "Very High Density Single Family", #4
        "Civic with Some Commercial", #5
        "CBD Commercial/Multi-Family", #6
        "Medium-Low Density Single Family", #7
        "Medium-High Density Single Family", #8
        "Medium Density Mixed Residential", #9
        "Low Density Commercial/Industrial", #10
        "Rural Single Family", #11
        "Low Density Mixed Commercial/Single Family", #12
        "High Density Mixed Residential", #13
        "High Density Commercial/Industrial", #14
        "Heavy Industrial", #15
        "Low Density Mixed Commercial/Multi-Family", #16
        "Medium Density Single Family", #17
        "Mid-Rise Commercial", #18
        "High Density Single Family", #19
        "High Density Mixed Commercial/Single Family") #20        
comp_plan_types$GPT<-labs[comp_plan_types$GPTCODE]

summary(as.factor(comp_plan_types$GPTCODE))
summary(as.factor(comp_plan_types$GPT))

# Assign to parcels

parcels.all.new<-merge(parcels.all, comp_plan_types[,c("CPLANID", "GPTCODE", "GPT")])
parcels.all<-parcels.all.new
rm(parcels.all.new)

summary(as.factor(parcels.all$GPTCODE))
summary(as.factor(parcels.all$GPT))

# Send tables to MySQL

library(RMySQL)
cnx<-dbConnect(dbDriver("MySQL"), 
               host="trondheim.cs.washington.edu",
               user="urbansim",
               password="UwmYsqlAt.5",
               dbname="psrc_2005_data_workspace")

if(dbExistsTable(cnx, "parcel_plan_types")) {dbRemoveTable(cnx, "parcel_plan_types")}
dbWriteTable(cnx, "parcel_plan_types", parcels.all, row.names=F)


# In MySQL, attach GPT and GPTCODE to the real parcels table
dbSendQuery(cnx, "
create index parcel_plan_types_gptcode on parcel_plan_types (GPTCODE);
")

dbSendQuery(cnx, "
create index parcel_plan_types_id_parcel on parcel_plan_types (ID_PARCE);
")

dbSendQuery(cnx, "
create index parcels_id_parcel on parcels (id_parcel);
")

    dbSendQuery(cnx, "
    update parcels as p, parcel_plan_types as t
        set p.plan_type_id = t.GPTCODE,
            p.plan_type_description = t.GPT
        where p.id_parcel = t.ID_PARCE;
    ")




