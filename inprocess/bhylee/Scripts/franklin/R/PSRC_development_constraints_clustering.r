
# Import parcel data from a tab file
# (why a tab file? this is a legacy of my starting out
# using SPSS, before switching to R. The only vestiges of
# that are that this tab file has only the records for parcels
# with buildings built in 1995 or later, and I took an initial
# cut at consolidating "desc" codes, as descibed below. This 
# could also easily be done in MySQL, then importing directly
# from MySQL to R. However, the full set of parcels is likely 
# too large to be imported into R.)

parcels<-read.delim("n:/psrc/dev_constr/parcels_merged_1995-.tab")


# Aggregate by Reduced Plan Type, computing 95th percentiles
# (Reduced Plan Type is a first-cut simplification
# of the "desc" column from the "regflu" GIS layer. At that
# stage, I simply aggregated "desc"s that have
# very similar names. This was also done in SPSS.)

plan_types<-aggregate(cbind(parcels$DU_AC,
                            parcels$FAR_SFR,
                            parcels$FAR_MFR,
                            parcels$FAR_COM,
                            parcels$FAR_IND,
                            parcels$FAR_GOV,
                            parcels$LTSZ_SFR), 
                      by=list(CPLANID = parcels$CPLANID),
                      FUN=quantile, probs=0.75, na.rm=TRUE)
plan_types$DUAC.75   <-plan_types$V1
plan_types$FARSFR.75 <-plan_types$V2
plan_types$FARMFR.75 <-plan_types$V3
plan_types$FARCOM.75 <-plan_types$V4
plan_types$FARIND.75 <-plan_types$V5
plan_types$FARGOV.75 <-plan_types$V6
plan_types$LTSZSFR.75<-plan_types$V7
plan_types$V1<-NULL
plan_types$V2<-NULL
plan_types$V3<-NULL
plan_types$V4<-NULL
plan_types$V5<-NULL
plan_types$V6<-NULL
plan_types$V7<-NULL

# Assign labels to Reduced Plan Types

plan_type_codes<-c(9, 10, 11, 12, 13, 17, 20, 22, 25, 26, 36, 38, 39, 
    42, 44, 48, 49, 50, 52, 53, 54, 56, 57, 60, 62, 63, 65, 66, 68, 
    70, 71, 74, 76, 77, 87, 88, 93, 94, 96, 99, 100, 112, 114, 116, 
    124, 125, 126, 131, 132, 135, 137, 139, 140, 150, 153, 157, 160, 
    162, 171, 177, 178, 180, 185, 186, 187, 190, 191, 193, 194, 195, 
    196, 201, 204, 209, 210, 213, 217, 221, 228, 229, 233, 240, 241, 
    243, 251, 254, 257, 259, 262, 264, 269, 271, 272, 274, 275, 285, 
    292, 293, 299, 305, 307, 309, 314, 319, 321, 322, 323, 334, 335, 
    339, 344, 345, 350, 357, 358, 359, 360, 362, 366, 369, 375, 376, 
    381, 383, 384, 386, 388, 392, 393, 398, 400, 401, 403, 405, 406, 
    407, 411, 412, 413, 414, 415, 418, 419)

plan_type_labels<-c("Agriculture", "Airport", "Aviation Business Center", 
"Airport Industrial", "Auto Oriented Commercial", "Buffer", "Office Park", 
"Business/Industrial Park", "Center Office Residential", "Center Suburban", 
"Civic-Educational", "Commercial", "Commercial/Recreation", 
"Commercial Medium Intensity", "Commercial, Industrial, Agricultur", 
"Commercial/Light Industrial", "Mixed Use Town Center", 
"Commercial/Mixed Use", "Commerical / Housing", 
"Common Wall Single Family (12)", "Common Wall Single Family (9)", 
"Community Facility", "Community Commercial", "Utility", 
"Constrained Residential", "Convenience Commercial", "Corridor Commercial", 
"Single Family 1du/ac", "Residential 4-12 Unit/Acre", "Design District", 
"Forest Land", "Central Business District", "Downtown Residential Districts", 
"Duplex, Mobile Home,Single Family", "Evergreen Highlands JPA", "Fairgrounds", 
"Government", "Heavy Commercial", "Heavy Industrial", "High Density Multifamily", 
"High Density Residential DD", "Industrial", "Industrial Tourist District Ov", 
"Intensity 1 (Residential)", "Large Lot Residential", "Light Commercial", 
"Light Industrial", "Light Manufacturing", "Commercial Low Intensity", 
"Local Business", "Low Density Multifamily", "Low Density Res 2 Transit Ovly", 
"Low Density Residential", "Low Urban Density Residential", 
"Manufacturing Center", "Master Planned Community", "Medical Facilities", 
"Medium Density Multifamily", "Mid-Rise Office District", 
"High Density Residential Mixed", "Mixed Medium Density Residential/C", 
"Mixed Single and Multi-Family", "MIxed Use", "Mixed Use Office", 
"Mixed Use Planned Development", "Mixed, Limited Multifamily", "Mobile Home Park", 
"Moderate Density Single Family", "Moderate Urban Density", "Mt Rainier Vista SPA", 
"Muckleshoot Tribe of Indians", "Multi-Family (36)", "Multifamily Residential", 
"Multi Family Residential 12-24du/a", "Multi Family Residential 8-12du/ac", 
"Multifamily High Mixed Use 29du-ac", "Medium Density Residential Mix", 
"Neighborhood Commercial", "Office", "Office / Residential", "Office/Multi-Family", 
"Park - Multi-Family Medium Density", "Park - Single Family High Density", 
"Park - Single Family Medium Densit", "Parks/Open Space", 
"Pedestrian Oriented Commercial", "Residential Planned Neighborhood", 
"Potential Annexation Area", "Private Open Space", "Public/Institutional", 
"Public & Quasi-Public", "Public Facility - Multi-Family Med", 
"Public Facility - Office", "Public Facility - Single Family Hi", 
"Public Facility - Single Family Me", "Public/Institutional Mixed-Use", 
"R-30 (30000 sq ft)", "R-40 Single Dwelling Unit", "Regional Commercial", 
"Residential", "Residential 6-10du/ac", "Residential 2 (15,000 Sq. Ft.-8,40", 
"Residential 2-5du/ac, Office-Prof,", "Single Family 5du/ac", 
"Residential 6-10du/ac, Office-Prof", "Residential-Agriculture", 
"Residential Commercial Center", "R-20 Single Dwelling Unit", "Residential Reserve", 
"Residential Urban", "Retirement Facility", "Transit Facility", "Acitvity Center", 
"Rural Protection", "Residential Rural", "Ruston Planned Development", 
"Sand Point Reuse Area", "School", "Sensitive", "Mixed Residential 7.26du-ac", 
"Single Family 2du/ac", "Single Family 3du/ac", "Single Family Estates 1.24du-ac", 
"High Density Residential", "Single Family Institution", "Single Family Low Density", 
"Medium Density Res. Tourist Di", "Single Family Residential", 
"Single Family High Density", "Single Family Urban Residential", 
"Residential 11-15du/ac", "Single Family, R-8.4", "Special Study Area", 
"Stuck River SPA", "Study Area", "Residential Suburban", "Tukwila Valley South", 
"Urban Growth Area", "Urban Growth Reserve", "Urban Housing Densities", "Urban Village", 
"Water/Right of Way", "Waterfront")

plan_types$CPLANTYPE<-factor(plan_types$CPLANID, levels=plan_type_codes, labels=plan_type_labels)

# Normalize the 75th percentiles (in the end, however, these were not used)

plan_types$DUAC.75.z<-plan_types$DUAC.75/mean(plan_types$DUAC.75)
plan_types$FARSFR.75.z<-plan_types$FARSFR.75/mean(plan_types$FARSFR.75)
plan_types$FARMFR.75.z<-plan_types$FARMFR.75/mean(plan_types$FARMFR.75)
plan_types$FARCOM.75.z<-plan_types$FARCOM.75/mean(plan_types$FARCOM.75)
plan_types$FARIND.75.z<-plan_types$FARIND.75/mean(plan_types$FARIND.75)
plan_types$FARGOV.75.z<-plan_types$FARGOV.75/mean(plan_types$FARGOV.75)
plan_types$LTSZSFR.75.z<-plan_types$LTSZSFR.75/mean(plan_types$LTSZSFR.75)

# Alternatively, first compute square roots...

plan_types$DUAC.75.sr<-sqrt(plan_types$DUAC.75)
plan_types$FARSFR.75.sr<-sqrt(plan_types$FARSFR.75)
plan_types$FARMFR.75.sr<-sqrt(plan_types$FARMFR.75)
plan_types$FARCOM.75.sr<-sqrt(plan_types$FARCOM.75)
plan_types$FARIND.75.sr<-sqrt(plan_types$FARIND.75)
plan_types$FARGOV.75.sr<-sqrt(plan_types$FARGOV.75)
plan_types$LTSZSFR.75.sr<-sqrt(plan_types$LTSZSFR.75)

# ...and then normalize (in the end, however, these were not used)

plan_types$DUAC.75.sr.z<-plan_types$DUAC.75.sr/mean(plan_types$DUAC.75.sr)
plan_types$FARSFR.75.sr.z<-plan_types$FARSFR.75.sr/mean(plan_types$FARSFR.75.sr)
plan_types$FARMFR.75.sr.z<-plan_types$FARMFR.75.sr/mean(plan_types$FARMFR.75.sr)
plan_types$FARCOM.75.sr.z<-plan_types$FARCOM.75.sr/mean(plan_types$FARCOM.75.sr)
plan_types$FARIND.75.sr.z<-plan_types$FARIND.75.sr/mean(plan_types$FARIND.75.sr)
plan_types$FARGOV.75.sr.z<-plan_types$FARGOV.75.sr/mean(plan_types$FARGOV.75.sr)
plan_types$LTSZSFR.75.sr.z<-plan_types$LTSZSFR.75.sr/mean(plan_types$LTSZSFR.75.sr[!is.na(plan_types$LTSZSFR.75.sr)])

# Perform several cluster analyses, varying the number of clusters from 2 to 20

# Do only once: save the random seed in a file (this is a long vector)

#saved.seed<-.Random.seed
#save(saved.seed, file="n:/psrc/dev_constr/saved.seed.RData")

# Import random seed from first run, to get consistent results

load(file="n:/psrc/dev_constr/saved.seed.RData")
.Random.seed<-saved.seed

# Run cluster analysis on square-root-of-75th percentile land use data

pt.cluster<-list()
for (ncl in 2:20) {
    pt.cluster[[ncl]]<-kmeans(x=plan_types[,c("DUAC.75.sr","FARSFR.75.sr","FARMFR.75.sr",
                                              "FARCOM.75.sr","FARIND.75.sr","FARGOV.75.sr")], 
                              centers=ncl, iter.max=1000)
    pt.cluster[[ncl]]$centers
    }

# Give clusters labels

pt.cluster[[2]]$centers
plot(x=cbind(plan_types$DUAC.75,plan_types$FARCOM.75), col=pt.cluster[[2]]$cluster)
labs<-c("Res","Non-Res")
plan_types$cl.02<-factor(pt.cluster[[2]]$cluster, levels=(1:2), labels=labs)


pt.cluster[[3]]$centers
plot(x=cbind(plan_types$DUAC.75,plan_types$FARCOM.75), col=pt.cluster[[3]]$cluster)
labs<-c("SFR","Gov/Ind","MFR/Com")
plan_types$cl.03<-factor(pt.cluster[[3]]$cluster, levels=(1:3), labels=labs)


pt.cluster[[4]]$centers
plot(x=cbind(plan_types$DUAC.75,plan_types$FARCOM.75), col=pt.cluster[[4]]$cluster)
labs<-c("Hi Gov/MFR/Com","Ind","SFR","SFR/MFR/Com")
plan_types$cl.04<-factor(pt.cluster[[4]]$cluster, levels=(1:4), labels=labs)


pt.cluster[[5]]$centers
plot(x=cbind(plan_types$DUAC.75,plan_types$FARCOM.75), col=pt.cluster[[5]]$cluster)
labs<-c("SFR/MFR/Com","SFR/Com/Lo Ind","Hi Ind","Hi Gov/MFR/Com","SFR")
plan_types$cl.05<-factor(pt.cluster[[5]]$cluster, levels=(1:5), labels=labs)


pt.cluster[[6]]$centers
plot(x=cbind(plan_types$DUAC.75,plan_types$FARCOM.75), col=pt.cluster[[6]]$cluster)
labs<-c("Hi MFR/Com","SFR","Hi Ind","Hi Gov/MFR/Com","Mid Com/Ind","SFR/MFR")
plan_types$cl.06<-factor(pt.cluster[[6]]$cluster, levels=(1:6), labels=labs)


pt.cluster[[7]]$centers
plot(x=cbind(plan_types$DUAC.75,plan_types$FARCOM.75), col=pt.cluster[[7]]$cluster)
labs<-c("SFR/Mid MFR","Hi Ind","Lo SFR","Mid Com/Ind","Hi MFR/Com/Mid Ind","Mid MFR/SFR","Gov")
plan_types$cl.07<-factor(pt.cluster[[7]]$cluster, levels=(1:7), labels=labs)


pt.cluster[[8]]$centers
plot(x=cbind(plan_types$DUAC.75,plan_types$FARCOM.75), col=pt.cluster[[8]]$cluster)
labs<-c("Mid MFR/SFR","SFR","Hi Gov/Com/Mid MFR","Mid Com/Ind/SFR","Hi MFR/Com","Undev","Hi Ind/Com","Mid Gov/Ind")
plan_types$cl.08<-factor(pt.cluster[[8]]$cluster, levels=(1:8), labels=labs)


pt.cluster[[9]]$centers
plot(x=cbind(plan_types$DUAC.75,plan_types$FARCOM.75), col=pt.cluster[[9]]$cluster)
labs<-c("Mid MFR/SFR","Mid Com/Ind/SFR","Mid Gov/Ind","SFR","Hi Gov/Com/MFR","Low SFR","Hi Ind/Com","Undev","Hi MFR/Com")
plan_types$cl.09<-factor(pt.cluster[[9]]$cluster, levels=(1:9), labels=labs)


pt.cluster[[10]]$centers
plot(x=cbind(plan_types$DUAC.75.sr.z,plan_types$FARCOM.75.sr.z), col=pt.cluster[[10]]$cluster)
labs<-c("Hi Ind/Mid Gov","Hi Ind/Mid Com","Mid SFR","Hi MFR/Hi Com/Mid Ind","Lo SFR","Mid Gov","Mid MFR/SFR","Undev","Hi Com/Mid MFR","Mid Com/Mid Ind/Low SFR")
plan_types$cl.10<-factor(pt.cluster[[10]]$cluster, levels=(1:10), labels=labs)


pt.cluster[[11]]$centers
plot(x=cbind(plan_types$DUAC.75.sr.z,plan_types$FARCOM.75.sr.z), col=pt.cluster[[11]]$cluster)
labs<-c("Mid Gov/Low Ind","Mid SFR","Mid MFR","Hi SFR","Mid Com/Ind/Lo SFR","Hi Ind/Mid Com","Hi MFR/Hi Com/Lo Ind",
        "Undev","Mid Com/Lo SFR","Hi Gov/Hi Com/Mid MFR","Mid MFR/Hi SFR/Mid Com")
plan_types$cl.11<-factor(pt.cluster[[11]]$cluster, levels=(1:11), labels=labs)


pt.cluster[[12]]$centers
plot(x=cbind(plan_types$DUAC.75.sr.z,plan_types$FARCOM.75.sr.z), col=pt.cluster[[12]]$cluster)
labs<-c("Mid Com/Mid Ind","Hi MFR/Hi Com/Lo Ind","Mid SFR","Mid Ind/Lo MFR/Lo Com","Hi Gov/Hi Com/Mid MFR","Undev",
        "Hi SFR","Hi Ind/Mid Com","Mid Com","Mid MFR/Mid SFR","Mid Gov/Lo Ind","Hi SFR/Lo Com")
plan_types$cl.12<-factor(pt.cluster[[12]]$cluster, levels=(1:12), labels=labs)


pt.cluster[[13]]$centers
plot(x=cbind(plan_types$DUAC.75.sr.z,plan_types$FARCOM.75.sr.z), col=pt.cluster[[13]]$cluster)
labs<-c()
plan_types$cl.13<-factor(pt.cluster[[13]]$cluster, levels=(1:13), labels=labs)


pt.cluster[[14]]$centers
plot(x=cbind(plan_types$DUAC.75.sr.z,plan_types$FARCOM.75.sr.z), col=pt.cluster[[14]]$cluster)
labs<-c()
plan_types$cl.14<-factor(pt.cluster[[14]]$cluster, levels=(1:14), labels=labs)


pt.cluster[[15]]$centers
plot(x=cbind(plan_types$DUAC.75.sr.z,plan_types$FARCOM.75.sr.z), col=pt.cluster[[15]]$cluster)
labs<-c()
plan_types$cl.15<-factor(pt.cluster[[15]]$cluster, levels=(1:15), labels=labs)


pt.cluster[[16]]$centers
plot(x=cbind(plan_types$DUAC.75.sr.z,plan_types$FARCOM.75.sr.z), col=pt.cluster[[16]]$cluster)
labs<-c()
plan_types$cl.16<-factor(pt.cluster[[16]]$cluster, levels=(1:16), labels=labs)


pt.cluster[[17]]$centers
plot(x=cbind(plan_types$DUAC.75.sr.z,plan_types$FARCOM.75.sr.z), col=pt.cluster[[17]]$cluster)
labs<-c()
plan_types$cl.17<-factor(pt.cluster[[17]]$cluster, levels=(1:17), labels=labs)


pt.cluster[[18]]$centers
plot(x=cbind(plan_types$DUAC.75.sr.z,plan_types$FARCOM.75.sr.z), col=pt.cluster[[18]]$cluster)
labs<-c()
plan_types$cl.18<-factor(pt.cluster[[18]]$cluster, levels=(1:18), labels=labs)


pt.cluster[[19]]$centers
plot(x=cbind(plan_types$FARSFR.75.sr.z,plan_types$FARMFR.75.sr.z), col=pt.cluster[[19]]$cluster)
labs<-c()
plan_types$cl.19<-factor(pt.cluster[[19]]$cluster, levels=(1:19), labels=labs)


pt.cluster[[20]]$centers
plot(x=cbind(plan_types$DUAC.75.sr.z,plan_types$FARCOM.75.sr.z), col=pt.cluster[[20]]$cluster)
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
plan_types$cl.20<-factor(pt.cluster[[20]]$cluster, levels=(1:20), labels=labs)

# Display plan types with cluster memberships

plan_types[sort.list(plan_types[,"cl.20"]),c("CPLANID","CPLANTYPE","cl.20")]


# Use 20 clusters, but do some reassignment for cases where the cluster
# that a cplanid is assigned to doesn't make sense:
plan_types$GPT<-plan_types$cl.20

plan_types$GPT[plan_types$CPLANID==210]<-"Medium Density Mixed Residential"
plan_types$GPT[plan_types$CPLANID==314]<-"Low Density Mixed Commercial/Single Family"
plan_types$GPT[plan_types$CPLANID==135]<-"Low Density Mixed Commercial/Single Family"
plan_types$GPT[plan_types$CPLANID==  9]<-"Rural Single Family"
plan_types$GPT[plan_types$CPLANID==400]<-"Medium-Low Density Single Family"
plan_types$GPT[plan_types$CPLANID== 12]<-"Low Density Commercial/Industrial"
plan_types$GPT[plan_types$CPLANID== 11]<-"Low Density Commercial/Industrial"
plan_types$GPT[plan_types$CPLANID==187]<-"Low Density Mixed Commercial/Single Family"
plan_types$GPT[plan_types$CPLANID==323]<-"High Density Mixed Commercial/Single Family"
plan_types$GPT[plan_types$CPLANID==274]<-"Low Density Mixed Commercial/Single Family"
plan_types$GPT[plan_types$CPLANID== 38]<-"High Density Mixed Commercial/Single Family"
plan_types$GPT[plan_types$CPLANID==251]<-"Undevelopable"
plan_types$GPT[plan_types$CPLANID==381]<-"Low Density Single Family"
plan_types$GPT[plan_types$CPLANID==177]<-"High Density Mixed Residential"
plan_types$GPT[plan_types$CPLANID== 65]<-"High Density Mixed Commercial/Single Family"
plan_types$GPT[plan_types$CPLANID==221]<-"Low Density Mixed Commercial/Single Family"
plan_types$GPT[plan_types$CPLANID==418]<-"Undevelopable"
plan_types$GPT[plan_types$CPLANID==190]<-"Low Density Mixed Commercial/Multi-Family"
plan_types$GPT[plan_types$CPLANID==233]<-"Low Density Mixed Commercial/Multi-Family"
plan_types$GPT[plan_types$CPLANID==180]<-"High Density Mixed Residential"
plan_types$GPT[plan_types$CPLANID==137]<-"Medium Density Mixed Residential"
plan_types$GPT[plan_types$CPLANID== 74]<-"CBD Commercial/Multi-Family"

plan_types[sort.list(plan_types[,"GPT"]),c("CPLANID","CPLANTYPE","GPT")]

# merge back into parcels
parcels$GPT<-NULL
parcels.new<-merge(x=parcels, y=plan_types[,c("CPLANID","GPT")], by="CPLANID")
parcels<-parcels.new
rm(parcels.new)

# Summarize 95th percentiles by Generic Parcel Types

parcels.na<-parcels
parcels.na[parcels.na==0]<-NA

generic_plan_types<-aggregate(cbind(parcels.na$DU_AC,
                                    parcels.na$FAR_SFR,
                                    parcels.na$FAR_MFR,
                                    parcels.na$FAR_COM,
                                    parcels.na$FAR_IND,
                                    parcels.na$FAR_GOV), 
                              by=list(GPT = parcels$GPT),
                              FUN=quantile, probs=0.95, na.rm=TRUE)
generic_plan_types$DUAC.95<-generic_plan_types$V1
generic_plan_types$FARSFR.95<-generic_plan_types$V2
generic_plan_types$FARMFR.95<-generic_plan_types$V3
generic_plan_types$FARCOM.95<-generic_plan_types$V4
generic_plan_types$FARIND.95<-generic_plan_types$V5
generic_plan_types$FARGOV.95<-generic_plan_types$V6
generic_plan_types$LTSZSFR.95<-generic_plan_types$V7
generic_plan_types$V1<-NULL
generic_plan_types$V2<-NULL
generic_plan_types$V3<-NULL
generic_plan_types$V4<-NULL
generic_plan_types$V5<-NULL
generic_plan_types$V6<-NULL
generic_plan_types$V7<-NULL

# Summarize the 25th percentile of DU/ac for SFR

du_ac.25<-aggregate(parcels.na$DU_AC, by=list(GPT = parcels$GPT), FUN=quantile, probs=0.25, na.rm=TRUE)
du_ac.25$DUAC.25<-du_ac.25$x
du_ac.25$x<-NULL

# Merge into generic plan types

generic_plan_types.new<-merge(x=generic_plan_types, y=du_ac.25)
generic_plan_types<-generic_plan_types.new
rm(generic_plan_types.new)
generic_plan_types$GPTCODE<-unclass(generic_plan_types$GPT)

# Write out table that can be imported into MS Excel

write.table(generic_plan_types, file="n:/psrc/dev_constr/generic_plan_types.tab", sep="\t")

# Merge GPT Codes into plan types

plan_types.new<-merge(x=plan_types, y=generic_plan_types[,c("GPT","GPTCODE")])
plan_types<-plan_types.new
rm(plan_types.new)

# After inspection of Generic Plan Types in MS Excel, some rounding, and subjective
# judgment, create final table of nonresidential constraints

new_constraints<-data.frame(GPTCODE=1:20, 
#                                                 --- P l a n   T y p e ---
#              1  2     3     4      5      6     7     8      9     10   11    12   13    14    15   16   17   18  19 20
    DUACRL =c( 6, 0   , 0   , 0   ,  4   , 15  ,  6   , 0   ,  5   ,  2  , 0  ,  4  , 0  ,  3   , 3  , 0  , 0  , 0, 10, 0  ),
    DUACRH =c(50, 0.5 , 0   , 0   , 25   , 50  , 17   , 0   , 12   , 15  , 2  , 12  , 4  , 24   , 8  , 0  , 0.5, 0, 25, 1  ),
    FARSFRH=c( 0, 0.05, 0   , 0   ,  0.55,  1.4,  0.75, 0   ,  0   ,  0.5, 0.3,  0.6, 0.4,  0.65, 0.5, 0  , 0.3, 0,  1, 0.3),
    FARMFRH=c( 7, 0   , 0   , 0   ,  2   ,  3  ,  0   , 0   ,  0.65,  0  , 0  ,  0  , 0  ,  0.65, 0  , 0  , 0  , 0,  0, 0  ),
    FARMIXH=c( 0, 0   , 0   , 0   ,  7   ,  1.5,  1   , 0.7 ,  0   ,  0  , 0  ,  0  , 0  ,  0   , 0  , 0  , 0  , 0,  0, 0  ),
    FARCOMH=c( 7, 0.05, 0.8 , 1.25,  1   ,  0  ,  0   , 0.35,  1.5 ,  0.7, 0  ,  0  , 0  ,  0   , 0  , 1.5, 0  , 0,  0, 0  ),
    FAROFFH=c( 7, 0.05, 0.8 , 1.25,  1   ,  0  ,  0   , 0.35,  1.5 ,  0.7, 0  ,  0  , 0  ,  0   , 0  , 1.5, 0  , 0,  0, 0  ),
    FARINDH=c( 0, 0   , 0.65, 1   ,  0   ,  0  ,  0   , 0.45,  0   ,  0  , 0  ,  0  , 0  ,  0   , 0  , 0.6, 0  , 0,  0, 0  ))

# Merge new constraints into generic plan types

generic_plan_types$FARCOMH<-NULL
generic_plan_types$FAROFFH<-NULL
generic_plan_types$FARINDH<-NULL
generic_plan_types$FARMFRH<-NULL
generic_plan_types$FARSFRH<-NULL
generic_plan_types$FARMIXH<-NULL
generic_plan_types$DUACRH<-NULL
generic_plan_types$DUACRL<-NULL
generic_plan_types.new<-merge(x=generic_plan_types, y=new_constraints, by="GPTCODE")
generic_plan_types<-generic_plan_types.new
rm(generic_plan_types.new)

# Merge new constraints into plan types

plan_types$FARCOMH<-NULL
plan_types$FAROFFH<-NULL
plan_types$FARINDH<-NULL
plan_types$FARMFRH<-NULL
plan_types$FARSFRH<-NULL
plan_types$FARMIXH<-NULL
plan_types$DUACRH<-NULL
plan_types$DUACRL<-NULL
plan_types.new<-merge(x=plan_types, y=new_constraints)
plan_types<-plan_types.new
rm(plan_types.new)

# Merge plan_types data into parcels

parcels$GPTCODE<-NULL
parcels$CPLANTYPE<-NULL
parcels$FARCOMH<-NULL
parcels$FAROFFH<-NULL
parcels$FARINDH<-NULL
parcels$FARMFRH<-NULL
parcels$FARSFRH<-NULL
parcels$FARMIXH<-NULL
parcels$DUACRH<-NULL
parcels$DUACRL<-NULL
parcels.new<-merge(x=parcels, 
                   y=plan_types[,c("GPTCODE","CPLANID","CPLANTYPE","DUACRL","DUACRH",
                                   "FARSFRH","FARMFRH","FARMIXH","FARCOMH","FAROFFH","FARINDH")], 
                   by="CPLANID")
parcels<-parcels.new
rm(parcels.new)

# Make table of constraint types

generic_building_types<-data.frame(generic_building_type_id=1:9, 
                                         description=c("Single Family Residential",
                                                       "Multi-Family Residential",
                                                       "Mixed Residential/Commercial",
                                                       "Commercial",
                                                       "Office",
                                                       "Industrial",
                                                       "Government",
                                                       "Other",
                                                       "No Building"))

# Make table of constraints, indexed by 
# combined_plan_type and generic_building_type
npt<-length(generic_plan_types$GPTCODE)
development_constraints<-data.frame(plan_type_id = rep(generic_plan_types$GPTCODE,9),
                                    generic_building_type_id = c(rep(1,npt*2),rep(2,npt*2),rep(3,npt*2),
                                                                       rep(4,npt),rep(5,npt),rep(6,npt)),
                                    constraint_name = c(rep("units_per_acre",npt),
                                                        rep("far",npt),
                                                        rep("units_per_acre",npt),
                                                        rep("far",npt),
                                                        rep("units_per_acre",npt),
                                                        rep("far",npt),
                                                        rep("far",npt),
                                                        rep("far",npt),
                                                        rep("far",npt)),
                                    minimum = c(generic_plan_types$DUACRL, rep(0,npt),
                                                generic_plan_types$DUACRL, rep(0,npt),
                                                generic_plan_types$DUACRL, rep(0,npt),
                                                rep(0,npt),
                                                rep(0,npt),
                                                rep(0,npt)),
                                    maximum = c(generic_plan_types$DUACRH,
                                                generic_plan_types$FARSFRH,
                                                generic_plan_types$DUACRH,
                                                generic_plan_types$FARMFRH,
                                                generic_plan_types$DUACRH,
                                                generic_plan_types$FARMIXH,
                                                generic_plan_types$FARCOMH,
                                                generic_plan_types$FAROFFH,
                                                generic_plan_types$FARINDH))

# Send tables to MySQL
library(RMySQL)
cnx<-dbConnect(dbDriver("MySQL"), 
               host="trondheim.cs.washington.edu",
               user="urbansim",
               password="UwmYsqlAt.5",
               dbname="psrc_2005_data_workspace")

#if(dbExistsTable(cnx, "generic_building_types")) {dbRemoveTable(cnx, "generic_building_types")}
#dbWriteTable(cnx, "generic_building_types", generic_building_types, row.names=F)

if(dbExistsTable(cnx, "development_constraints")) {dbRemoveTable(cnx, "development_constraints")}
dbWriteTable(cnx, "development_constraints", development_constraints, row.names=F)

if(dbExistsTable(cnx, "plan_types")) {dbRemoveTable(cnx, "plan_types")}
dbWriteTable(cnx, "plan_types", 
             generic_plan_types[,c("GPTCODE","GPT","DUACRL","DUACRH","FARSFRH","FARMFRH","FARCOMH","FARINDH")], 
             row.names=F)

if(dbExistsTable(cnx, "parcel_plan_types")) {dbRemoveTable(cnx, "parcel_plan_types")}
dbWriteTable(cnx, "parcel_plan_types", parcels, row.names=F)


# Save RData File

save.image("N:\\PSRC\\dev_constr\\workspace.RData")

# Clean up the workspace a bit

rm(parcels.na)
parcels.gpt<-data.frame(PARCELID=parcels$ID_PARCE, GPTCODE=parcels$GPTCODE)
rm(parcels)

# Prepare data for GIS

parcels.gpt$PARCELID.c<-format(parcels.gpt$PARCELID, nsmall=0, trim=F,
                               scientific=F, width=13, justify="right", digits=13)
parcels.gpt$PARCELID.c<-sub("    ","0", parcels.gpt$PARCELID.c)

# Import parcels dbf from GIS layer

library(foreign)
parcels_regflu<-read.dbf("W:/GIS_Data/PSRC/Parcels2005/2005_centroids_regflu.dbf")

parcels_regflu$parcelid.n<-as.numeric(parcels_regflu$parcelid)


# merge parcel data into parcels_regflu

parcels_regflu.new<-merge(x=parcels_regflu, y=parcels.gpt, 
                          by.x="parcelid", by.y="PARCELID.c")


# Export parcels as dbf

write.dbf(parcels_regflu, "W:/GIS_Data/PSRC/Parcels2005/2005_centroids_regflu.dbf")
