library(RPostgreSQL)
library(ggplot2)
require(scales)
library(plyr)

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

query_tpp = dbSendQuery(con, " ")
tpp_names = fetch(query_tpp,n=-1)

dbDisconnect(con)
lapply(c("query_tpp","query_pda","query_city","query_county"), postgresqlCloseResult,function(x) ) 
##################################################################################
file_path='/home/aksel/Documents/Data/Urbansim/run_139/area_permutation_table-1_2010.tab'
summary <- file.path(file_path,fsep = .Platform$file.sep)
abag <- read.csv(summary,header = TRUE, sep="\t")
#abag[,3]<-factor(abag[,3],labels=c(pda_names[,2])
abag <- merge(abag,pda_names, by.x="pda_id.i8", by.y="pda_id")
abag <- merge(abag,county_names, by.x="county_id.i8", by.y="county_id")
abag <- merge(abag,city_names, by.x="city_id.i8", by.y="city_id")
abag <- merge(abag,pda_names, by.x="pda_id.i8", by.y="pda_id")

##shed redundant columns and write to csv
keepers <-c()
write.table(abag,"/home/aksel/abagOut.csv", sep="\t", row.names = T)