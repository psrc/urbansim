library(RPostgreSQL)
library(ggplot2)
require(scales)
library(plyr)
args <- commandArgs(TRUE)

## grab arguments
args <- c('/home/aksel/Documents/Data/Urbansim/run_179/indicators','2010','2040','134',"TRUE","No_Project")
pth <-args[1]
yrStart <- as.integer(args[2])
yrEnd <- as.integer(args[3])
run_id <- args[4]
travelModelRan <- args[5]
scenario <- args[6]

dbname <- "bayarea"; dbuser <- "********"; dbpass <- "********";
dbhost <- "paris.urbansim.org"; dbport <- 5432;
drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, host=dbhost, port=dbport, dbname=dbname,
                 user=dbuser, password=dbpass)
dbListTables(con)
query_city = dbSendQuery(con, "select id as city_id, county as county_id, name as city from geography_city
                         order by id;")
city_names = fetch(query_city,n=-1)

query_county = dbSendQuery(con, "select id as county_id, name as county 
                           from geography_county where bayarea='t';")
county_names = fetch(query_county,n=-1)

query_pda = dbSendQuery(con, "select pda_id, pda from pdas order by pda_id;")
pda_names = fetch(query_pda,n=-1)

query_tpp = dbSendQuery(con, "select tpp_category_id, tpp_category from tpp_categories order by tpp_category_id;")
tpp_names = fetch(query_tpp,n=-1)

dbDisconnect(con)
queries <- c("query_tpp","query_pda","query_city","query_county")
lapply(queries, postgresqlCloseResult,function(x) x) 
##################################################################################
file='area_permutation_table-1_2010.tab'
summary <- file.path(pth,file,fsep = .Platform$file.sep)
abag <- read.csv(summary,header = TRUE, sep="\t")
#abag[,3]<-factor(abag[,3],labels=c(pda_names[,2])
abag <- merge(abag,pda_names, by.x="pda_id.i8", by.y="pda_id",all.x = T)
abag <- merge(abag,county_names, by.x="county_id.i8", by.y="county_id",all.x = T)
abag <- merge(abag,city_names, by.x="city_id.i8", by.y="city_id",all.x = T)
abag <- merge(abag,tpp_names, by.x="tpp_id.i8", by.y="tpp_category_id",all.x = T)

##shed redundant columns and write to csv
keepers <-c('county','city','pda','tpp_category','total_households_2010.f8','total_population_2010.f8','age_lt_04_2010.f8','age_05_19_2010.f8','age_20_44_2010.f8','age_45_64_2010.f8','age_65_plus_2010.f8','empl_01_farm_nat_res_2010.f8','empl_02_construction_2010.f8','empl_03_manuf_whole_2010.f8','empl_04_retail_2010.f8','empl_05_transp_ware_util_2010.f8','empl_06_information_2010.f8','empl_07_fin_lease_2010.f8','empl_08_prof_2010.f8','empl_09_health_educ_2010.f8','empl_10_art_rec_other_2010.f8','empl_11_government_2010.f8','empl_99_unclassified_2010.f8','employed_residents_2010.f8','multi_family_housholds_2010.f8','multi_family_units_2010.f8','single_family_housholds_2010.f8','single_family_units_2010.f8')
abag.k <- abag[,keepers]

names(abag.k) <- lapply(names(abag.k), gsub, pattern="\\..+|_\\d{4}\\..+",replacement="")
file_out <- file.path(pth, sprintf("db_area_permutation_summary_%s.csv",run_id), fsep = .Platform$file.sep)
write.table(abag.k,file_out, sep="\t", row.names = F)