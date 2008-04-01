# If this is your first time EVER using RMySQL, make sure 
# you've installed it, as well as the DBI package:

install.packages("DBI")
install.packages("RMySQL")

# If this is the first time you've used RMySQL during this
# R session, call the libraries:

library(DBI)
library(RMySQL)


# Create a new file in your root C: directory, named "my.cnf" 
# and enter connections following the format shown below
# (and remember to take out the comment marks):
# 
# [WFRC_1997_baseyear]
# user = urbansim
# password = ***
# host = trondheim.cs.washington.edu
# dbname=WFRC_1997_baseyear
# database=WFRC_1997_baseyear

# Test out the connection in R:

WFRC.1997.output.2030.LRP <- dbConnect(dbDriver("MySQL"), group="WFRC_1997_output_2030_LRP")  # Note that "group" references the "my.cnf" file discussed above
q.gridcells.DistinctYears <- dbSendQuery(conn=WFRC.1997.output.2030.LRP, 
statement="select distinct year from gridcells_exported")
d.gridcells.DistinctYears <- fetch(q.gridcells.DistinctYears, n=-1)  # to limit the number of records, set "n" to a positive integer
summary(d.gridcells.DistinctYears)

# Now let's get a larger set of data
WFRC.1997.output.2030.LRP <- dbConnect(dbDriver("MySQL"), group="WFRC_1997_output_2030_LRP")  # Note that "group" references the "my.cnf" file discussed above
WFRC.1997.output.2030.const <- dbConnect(dbDriver("MySQL"), group="WFRC_1997_output_2030_const")  # Note that "group" references the "my.cnf" file discussed above
WFRC.1997.output.2030.highway <- dbConnect(dbDriver("MySQL"), group="WFRC_1997_output_2030_highway")  # Note that "group" references the "my.cnf" file discussed above
WFRC.1997.output.2030.transit <- dbConnect(dbDriver("MySQL"), group="WFRC_1997_output_2030_transit")  # Note that "group" references the "my.cnf" file discussed above
WFRC.1997.output.2030.parking <- dbConnect(dbDriver("MySQL"), group="WFRC_1997_output_2030_parking")  # Note that "group" references the "my.cnf" file discussed above
WFRC.1997.output.2030.UGB <- dbConnect(dbDriver("MySQL"), group="WFRC_1997_output_2030_UGB")  # Note that "group" references the "my.cnf" file discussed above

# NOTE: Be sure that the variables' names you are using have no underscores, or you will have syntax conflicts when 
# using them in R.

# Reference distribution
q.zones.LRP.2030 <- dbSendQuery(conn=WFRC.1997.output.2030.LRP, 
statement="select hae1 from household_accessibilities where year=2030")
d.zones.LRP.2030 <- fetch(q.zones.LRP.2030, n=-1)
summary(d.zones.LRP.2030)

# Test distribution
q.zones.other.2030 <- dbSendQuery(conn=WFRC.1997.output.2030.const, 
statement="select hae1 from household_accessibilities where year=2030")
d.zones.other.2030 <- fetch(q.zones.other.2030, n=-1)
summary(d.zones.other.2030)

# Plot a relative distribution

library(reldist)
par(mfrow=c(1,3))
rdresult<-reldist(y=d.zones.other.2030$hae1,
    yo=d.zones.LRP.2030$hae1,
    main="Total",show="none",
    ylim=c(0,3),cdfplot=F,bar="yes",yolabs=seq(0,400000,50000),ci=T)
rdresult<-reldist(y=d.zones.other.2030$hae1,
    yo=d.zones.LRP.2030$hae1,
    main="Shift",show="effect",
    ylim=c(0,3),cdfplot=F,bar="yes",yolabs=seq(0,400000,50000),ci=T)
rdresult<-reldist(y=d.zones.other.2030$hae1,
    yo=d.zones.LRP.2030$hae1,
    main="Residual",show="residual",
    ylim=c(0,3),cdfplot=F,bar="yes",yolabs=seq(0,400000,50000),ci=T)
par(mfrow=c(1,1))




