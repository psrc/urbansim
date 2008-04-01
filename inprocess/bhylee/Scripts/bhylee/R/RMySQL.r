library(RMySQL)
library(foreign)
library(Zelig)

act06 <- dbConnect(dbDriver("MySQL"), 
			host="localhost",
			user="root",
			password="fasfas",
			dbname="psrc_activity2006")

hh4est <- dbReadTable(act06, "hh4est_rx", row.names=NULL)

hh4est$avg_bedrooms<-hh4est$number_of_bedrooms/hh4est$residential_units
hh4est$avg_bathrooms<-hh4est$number_of_bathrooms/hh4est$residential_units
hh4est$avg_total_value<-hh4est$total_value/hh4est$residential_units
hh4est$avg_unit_sqft<-hh4est$building_sqft/hh4est$residential_units

attach(hh4est)

