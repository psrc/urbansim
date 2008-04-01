from employment_scaler import EmploymentScaler

### Parameters:
sectors = range(14,18)
years = range(2001,2010)
baseyear_db = "PSRC_2000_baseyear_cpeak2"


### Main routine:
for sector in sectors:
    
    for year in years:
    
        print "starting scaling for year %s, sector %s" % (year, sector)
        myScaler = EmploymentScaler(baseyear_db)
        myScaler.GetJobsToAdd(year,sector)
        myScaler.Scale(sector)
