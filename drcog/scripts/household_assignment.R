  ##this R script assigns households to buildings according to matched zone_id, tenure, and building_type_id
  ##author(s): Yujiang Mou

  setwd("/Users/yujiangmou/Desktop/updating hh_table")

	load("hhtable_newbuilding.rda")
	load("building_newbuilding.rda")
	save(sub.bds,file="building_newbuilding.rda")
	library("foreach")
	ls()

	zone_ids=as.vector(unique(hh.pums.new$TAZ_id))

	temp <- foreach(zone_id=zone_ids, .combine='rbind') %do% process_zone(hh.pums.new,sub.bds,zone_id)
	process_zone=function(hh,bd,zone_id)
	{
		hh.zone=subset(hh,hh$TAZ_id==zone_id) 
		bd.zone=subset(bd,bd$TAZ_id==zone_id)
		for (i in 1: nrow(hh.zone))
		{
			tenure=hh.zone$tenure[i]
			building_type=hh.zone$building_type[i]
			index=bd.zone$tenure==tenure & bd.zone$building_type==building_type & bd.zone$units!=0
			idsample=bd.zone$building_id[index]
			if (is.na(idsample[1])) next
			id=sample(idsample,1)
			hh.zone$building_id[i]=id
			bd.zone$units[bd.zone$building_id==id]=bd.zone$units[bd.zone$building_id==id]-1
			print (i)
		}
		new.hh=cbind(hh.zone$household_id,hh.zone$building_id)
		return (new.hh)
	
	}

	temp=data.frame(temp)
	names(temp)[names(temp)=="X1"]="household_id"
	names(temp)[names(temp)=="X2"]="building_id"
	names(temp)
	
# look at the data 
	load("new_pums.rda")
	nrow(temp2)
	index=temp2$building_id==-1
	sum(index)
	(nrow(temp2)-sum(index))/nrow(temp2)#2371127
	table(temp2$building_type)
	names(temp2)
	
	
# uploaded to paris

	library('RPostgreSQL')
	conn<-dbConnect(PostgreSQL(),user='urbanvision',password='***',dbname='bayarea',host='paris.urbansim.org')
	dbListTables(conn)
	table_name <- "hh_table_updated_bdID"
	temp=read
hh <- read.csv('hh_pums_new.csv', header=T)

dbWriteTable(conn, table_name, hh, row.names = F)
	ls()
	
	hh.bats<-dbReadTable(conn,'hh_table_updated_bdID')
	
	
