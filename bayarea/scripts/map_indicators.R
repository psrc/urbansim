#################  Script  Descriptions ###########

### This scirpt can generate zone level indicators for urbansim model outputs, in form of maps and data histograms; 

### Three command lines are required: 
	# (1) specify input directory where the tab files are located;
	# (2) output directory
	# (3) directory for the shapefile

### install the mapping
#install.packages("maptools")
#install.packages("RColorBrewer")
#install.packages("classInt")
#install.packages("rgdal")

## install packages used in the scripts
library(maptools)
library(RColorBrewer)
library(classInt)
require("rgdal")


####################################################
### Self coded function that generate zone indicators
zone_growth=function(Tabfilename,input,output,zones)
{	

## read in the urbansim data and calculate growth rate
	setwd(input)
	#Tabfilename=filist[13]
	urbansim_raw=read.table(Tabfilename,header=T,sep="\t")
	n=length(urbansim_raw)
	index=is.na(urbansim_raw[n])|urbansim_raw[n]==Inf
	urbansim_raw[n][index]=0
	index=is.na(urbansim_raw[2])|urbansim_raw[2]==Inf 
	urbansim_raw[2][index]=0
	
	urbansim_raw$growth=urbansim_raw[n]-urbansim_raw[2]
	indicator=data.frame(urbansim_raw[1],urbansim_raw$growth)
	names(indicator)[1]="zone_id"
	names(indicator)[2]="growth"
	names(indicator)

## Join urbansim data with zones and map out 
	zones_temp=zones
	zones_temp@data=merge(zones_temp@data,indicator,by.x="zone_id",by.y="zone_id",all.x=TRUE,sort=F)
	
	## set up map braeks
	n=10
	min_g=min(zones_temp@data$growth)
	max_g=max(zones_temp@data$growth)
	
	## print the file name and do not return maps when the growth values are all 0
	if (length(zones_temp@data$growth[zones_temp@data$growth!=0])<=10) 
	{
		print(paste(Tabfilename," cannot be mapped because there are less than 10 growth values other than 0",sep=""))
		return()
	}
	if (min_g==max_g) 
	{
		print(paste(Tabfilename," cannot be mapped because all the growth values are all constants",sep=""))
		return()
	}




	if (min_g==0) 
	{
		g=seq(0,n-2,by=1)
		interval=max_g/(n-2)
		breaks=c(round(interval*g))
	}
	if (min_g<0) 
	{
		g=seq(0,n-3,by=1)
		interval=max_g/(n-3)
		temp=round(interval*g)
		breaks=c(min_g,temp)
	}
	if (min_g>0) 
	{
		g=seq(0,n-2,by=1)
		interval=(max_g-min_g)/(n-2)
		breaks=round(interval*g)
	}	
	if (breaks[n-1]<=max_g){breaks[n-1]=round(max_g+1)}
	brks=classIntervals(zones_temp@data$growth,style="fixed", fixedBreaks=breaks)
	brks=brks$brks
	colors=brewer.pal(length(brks)-1,"Reds")
	label=rep(0,length(brks)-1)
	for (i in 1:length(brks)-1)
	{
		temp=paste(as.character(round(brks[i])),"-",as.character(round(brks[i+1])),sep=" ")
		label[i]=temp
	}
	
## plot map
	setwd(output)	
	Title1=paste("Growth of",substr(Tabfilename,1,(nchar(Tabfilename)-4)),sep=" ")
	savename=paste(Title1,".pdf",sep="")
	pdf(savename)
	par(mar=c(1.8,1,1.5,1))
	plot(zones_temp,col=colors[findInterval(zones_temp@data$growth, brks,all.inside=T)], axes=F,lwd=0.1,lty=3)
	title(Title1)
	legend("bottomleft", legend=label, fill=colors, x.intersp =1, y.intersp=1)
	dev.off()
## plot histogram	
	
	Title2=paste("Data Plots",substr(Tabfilename,1,(nchar(Tabfilename)-4)),sep=" ")
	savename=paste(Title2,".pdf",sep="")
	pdf(savename)
	hist(zones_temp@data$growth,main=Title2)
	dev.off()	
}

#################################################################



### command line parameters
args <- commandArgs(trailingOnly=TRUE)
input=args[1]
output=args[2]
shp=args[3]

## create output dir if it does not exist
if (!file.exists(output)){
    dir.create(output)
}
## read in the shapefile data
zones=readOGR(shp,"zones")## read in the shapefile data 

## invoke the main function, zone_growth
filist=list.files(path=input,pattern="zone.tab")
for (i in 1:length(filist))
{zone_growth(filist[i],input,output,zones)}


### end 



