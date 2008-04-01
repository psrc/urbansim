

# Run a sensitivity analysis on the PSRC-parcel
# real estate price model, using a few sample
# parcels and comparing several representative
# development templates.

library(RMySQL)

# Setup MySQL connections

# Database for workspace data:
cnx.work<-dbConnect(dbDriver("MySQL"), 
                    host="trondheim.cs.washington.edu",
                    user="urbansim",
                    password="UwmYsqlAt.5",
                    dbname="psrc_2005_data_workspace")

# Database for baseyear data:
cnx.base<-dbConnect(dbDriver("MySQL"), 
                    host="trondheim.cs.washington.edu",
                    user="urbansim",
                    password="UwmYsqlAt.5",
                    dbname="psrc_2005_parcel_baseyear")

# Database for model specifications & coefficients:
cnx.est<-dbConnect(dbDriver("MySQL"), 
                   host="trondheim.cs.washington.edu",
                   user="urbansim",
                   password="UwmYsqlAt.5",
                   dbname="psrc_2005_data_workspace_franklin")

# Import specifications & coefficients

repm.spec<-dbReadTable(cnx.est, "real_estate_price_model_specification")
repm.coef<-dbReadTable(cnx.est, "real_estate_price_model_coefficients")

# Merge coefficients into specification

repm<-merge(repm.spec, repm.coef, by=c("sub_model_id", "coefficient_name"))

# Create a small set of sample parcels

parcels<-dbGetQuery(cnx.work, "select * from parcels
                                   where id_parcel = \"0330697000170\"
                                      or id_parcel = \"0351287937\"
                                      or id_parcel = \"0339320900280\"
                                      or id_parcel = \"0333523049102\";")
parcels

n.parcels<-dim(parcels)[1]

# Import development templates

devtplt<-dbReadTable(cnx.work, "development_templates")



# Cycle through sample parcels

parcel.dev<-list()

for (p in 1:n.parcels) {
    parcel.dev[[p]]<-merge(devtplt, parcels[p,])
    
}

