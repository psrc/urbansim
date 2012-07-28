#!/usr/bin/r

#script goes to folder with indicator-output county-level files (must be in one file per variable)
#In steps, this is the sequence:
#1) Gets all tab files starting with county in folder, matching passed years (e.g. county_table-3_2010-2035_...)
#2) Loops through data files
#3) --keeps only 9 relevant counties
#4) --transforms dataframe so years are rows, counties columns
#5) --plots chart, writes to global pdf file

##USAGE: Rscript summarize_county_indicators.R \
##            /var/hudson/workspace/MTC_Model/data/bay_area_parcel/runs/run_66.2012_07_07_15_50/indicators \ 
##            2010 2035

args <- commandArgs(TRUE)
options(warn=-1) 
traceback()

#options(error=utils::recover)
require("stringr")
require("ggplot2")
require("reshape")
require("gridExtra")
require("RGraphics") 
library(maptools)
library(RColorBrewer)
library(classInt)
require("rgdal")
gpclibPermit() 

annot <- function(){
  annotate("text", x = Inf, y = -Inf, label = "DRAFT",
           hjust=0, vjust=-8, col="darkgrey", cex=20,
           fontface = "bold", alpha = 0.8, angle=45)
}

##declare index function
indx <- function(dat, baseRow = 1)
{
  require(plyr)   
  divisors <- dat[baseRow ,]
  adply(dat, 1, function(x) x / divisors*100)
}

viewPortFunc <- function(printObject=printObject){
  grid.newpage()
  pushViewport(viewport(height=unit(0.9, "npc"), width=unit(0.95, "npc"), x=0.5, y=0.5, name="vp")) 
  upViewport() 
  print(printObject, vp="vp")
  #print(sprintf("Outputting Chart %s to PDF",title))
}
#wrap cmd-line arguments to assign to proper names
#cmdArgs <- function(a="/home/aksel/Documents/Data/Urbansim/run_139.2012_05_15_21_23/indicators/2010_2035",b=2010,c=2035) 
#{
#  pth <<- a
#  yrStart <<- as.integer(b)
#  yrEnd <<- as.integer(c)
#  return(1)
#}
#cmdArgs(a=args[1],b=args[2],c=args[3])

## grab arguments
pth <-args[1]
yrStart <- as.integer(args[2])
yrEnd <- as.integer(args[3])
setwd(pth)
shp_file <- args[5]
shp_path <- args[4]
qual_shp_file <- file.path(shp_path,shp_file,fsep = .Platform$file.sep)
lyr <- strsplit(shp_file,"\\.")[[1]][1]

## function to render a matrix WITH a regional total if absolute values, otherwise no total
returnMatrix <- function(inputData=inputData,tableName=tableName) {
  if (grepl("average",tableName,ignore.case=TRUE) | grepl("avg",tableName,ignore.case=TRUE)) {
    print("avg")
    inputData$year <- as.integer(rownames(inputData))
    meltedInputData <- melt(inputData,id="year",variable_name = "county")
  }
  else #if (grep("average",fName,ignore.case=FALSE, fixed=T))
  {
    print("not avg")
    inputData$Region <- rowSums(inputData,na.rm = FALSE, dims = 1)
    inputData$year <- as.integer(rownames(inputData))
    meltedInputData <- melt(inputData[,c(1:9,11)],id="year",variable_name = "county")
  }
  return(list(wide=inputData,long=meltedInputData))
}

## function for formating chart titles
TitleCase <- function(string="test string")
{
  first <- toupper(substring(string, 1, 1))
  rest <- tolower(substring(string, 2))
  fString <- sprintf("%s%s",first,rest)
  return(fString)
}

## parse path to get runid, run date
split <- strsplit(args[1],"/")[[1]]
pos <- length(split)-1  #this assumes we are one up from the indicators dir--a regex would be better.
runid <- split[pos]
periodPosition <- regexpr("\\.",runid)[[1]]
tm <- strsplit(substr(runid,periodPosition+1,nchar(runid)),"_")
id <- strsplit(substr(runid,1,periodPosition-1),"_")[[1]][2]
datetime <-sprintf("%s/%s/%s %s:%s:00",tm[[1]][2],tm[[1]][3],tm[[1]][1],tm[[1]][4],tm[[1]][5]) #get from runid string
runDate <- strptime(datetime, "%m/%d/%Y %H:%M:%S")

##  select folder with indicator files, fetch all beginning with "county..." having proper years in name
ptrn <-sprintf("^%s%s_%s-%s%s","county_table-","[0-9]",yrStart,yrEnd,".+")
fileList = list.files(path=pth, pattern=ptrn)
if (length(fileList) == 0)
{
  stop(sprintf("Failed to find any county indicators in %s", pth))
}

##  "loop" construct, create dataframe, chart for each tab file
dat<-lapply(fileList,read.csv,header=T,sep = "\t")

## start pdf object to store all charts
fp <- file.path(pth, fsep = .Platform$file.sep)
fileNameOut=sprintf("%s/plot_%s_indexChart.pdf",fp,runid)
sprintf("Preparing file %s for charts and figures...", fileNameOut)
pdf(fileNameOut,height=8.5, width=11,onefile=TRUE)

## store each file in a dataframe, process and plot as we go.
for(i in 1:length(dat)) 
{
  simulation <- as.data.frame(dat[i])  #technically redundant; could just use dat list object
  #simulation <- read.csv("/home/aksel/Documents/Data/Urbansim/run_139.2012_05_15_21_23/indicators/2010_2035/county_table-3_2010-2035_county__county_population.tab",header=T,sep = "\t")  
  ## subset to keep only relevant counties (using the arbitrary objectid in geography_county.id)
  simulation <- simulation[simulation$county_id.i8 %in% c(49,48,43,41,38,28,21,7,1),  ]
  #print(simulation[1:2,1:3])
  
  ##keep for mapping
  strYrStart<-sprintf("yr_%s",yrStart)
  strYrEnd<-sprintf("yr_%s",yrEnd)
  simulation.m <- simulation[c(1,2,length(names(simulation)))]
  #colnames(simulation.m) <- c("county_id",strYrStart,strYrEnd)
  n=length(simulation.m)
  index=is.na(simulation.m[n])|simulation.m[n]==Inf
  simulation.m[n][index]=0
  index=is.na(simulation.m[2])|simulation.m[2]==Inf 
  simulation.m[2][index]=0
  
  simulation.m$growth=(simulation.m[n]-simulation.m[2])/simulation.m[2]
  simulation.m=data.frame(simulation.m[1],simulation.m$growth)
  names(simulation.m)=c("county_id","growth")
  
  ## convert id key to factor levels for more meaningful labeling. Labels are assigned based on factor numerical order.
  #cnty <- c('ala','cnc','mar','nap','sfr','smt','scl','sol','son')
  cnty <-  c('Alameda','Contra Costa','Marin','Napa','San Francisco','San Mateo','Santa Clara','Solano','Sonoma')
  simulation$county_id.i8 <-factor(simulation$county_id.i8, labels=cnty)
  
  ## rename col names, retaining only year part, extract column name to use in chart name later. Each column has year embedded
  regexp <- "([[:digit:]]{4})"  
  maxCol <- length(simulation)
  years <-str_extract(names(simulation)[2:maxCol],regexp) 
  pos <- regexpr(pattern = regexp, text = names(simulation)[2:maxCol])  #where does year start in col name?
  yrEnd <-max(as.integer(years))  #overwrites passed years and uses actual outer years in tab files 
  yrStart <- min(as.integer(years))
  
  ## extract field name representing variable for use in chart
  title_prelim <- substr(names(simulation)[2],1,pos-2)
  title_split <- strsplit(title_prelim,"_")
  title_proper <- lapply(title_split,TitleCase)
  title <- paste(title_proper[[1]], sep=" ", collapse = " ")
  #fileNameOutChart=sprintf("%s/plot_%s_indexChart_%s.pdf",fp,runid,title)
  #fileNameOutTable=sprintf("%s/plot_%s_indexTable_%s.pdf",fp,runid,title)
  
  yrNames <- c('county',years)
  ## assign new colunn names
  names(simulation) <-yrNames
  
  ## Transpose frame so cols are county series, rows are years
  simulation.t <- t(simulation[,2:ncol(simulation)])
  
  ## Set column headings as counties
  colnames(simulation.t) <- simulation[,1]
  simulation.t <-as.data.frame(simulation.t)
  
  ## add regional total for non-average tables
  ## get matrices; chck if average in name. if so, treat total differently.
  returnMatrices <- returnMatrix(simulation.t,title_prelim)
  simulation.t <- returnMatrices$wide 
  simulation_long_abs <- returnMatrices$long
  
  ## call index function to convert absolutes to indices (2010= index 100), replace NAs
  simulation.i <-indx(simulation.t, 1)
  simulation.i <- replace(simulation.i, is.na(simulation.i), 0) 
  
  ##add two digit years for easier plotting
  rownames(simulation.i) <- yrNames[2:maxCol]
  #attach(simulation.i)
  
  ##   convert to long format for ggplot
  simulation.i$year <- as.integer(rownames(simulation.i))
  simulation_long_index <- melt(simulation.i,id="year",variable_name = "county")
  
  ## prepare plotting
  ## table object prep for chart
  end <- yrEnd - yrStart + 1
  if (end > 26 ) {
    step <- 2 
  }
  else {
    step <- 1
  }
  
  g1 <- tableGrob(
    format(
      simulation.t[seq(1,end,step),1:length(names(simulation.t))-1], 
      digits = 2,big.mark = ","), 
    gpar.colfill = gpar(fill=NA,col=NA), 
    gpar.rowfill = gpar(fill=NA,col=NA), 
    h.even.alpha = 0,
    gpar.rowtext = gpar(col="black", cex=0.8,
                        equal.width = TRUE,
                        show.vlines = TRUE, show.hlines = TRUE, separator="grey")                     
    )
  
  
  #string <- "
  #placeholder for possible annotation
  #"
  #g2 <- splitTextGrob(string)
  theme_set(theme_grey()); 
  #theme_set(theme_bw());
  
  ## plot object
  stamp <- sprintf("Simulation #%s run on %s\nReport generated on %s",id,format(runDate, "%a %b %d %T"),format(Sys.time(), "%a %b %d %T"))
  ## first send line chart to pdf...
  
  g3 <- ggplot(data=simulation_long_index,
               aes(x=as.factor(year), 
                   y=value, 
                   group=county,
                   colour=county)) +
                     geom_line(
                       aes(
                         linetype=county), size = .65) +       # Thin line, varies by county
                           scale_fill_brewer(palette="Paired") +
                           geom_point(
                             aes(
                               shape=county) ,  size = 2.5)   +       
                                 scale_fill_brewer(palette="Paired")+
                                 opts(title=title)+
                                 xlab("Year") + 
                                 ylab(paste("Indexed Value (Rel. to ",yrStart,")")) + 
                                 opts(axis.text.x=theme_text(angle=90, hjust=0))
                                 
  
   g4 <- ggplot(data=simulation_long_abs,
                aes(x=as.factor(year), 
                    y=value, 
                    group=county,
                    colour=county)) +
                      geom_line(
                        aes(
                          linetype=county), size = .65) +       # Thin line, varies by county
                            scale_fill_brewer(palette="Paired") +
                            geom_point(
                              aes(
                                shape=county) ,  size = 2.5)   +       
                                  scale_fill_brewer(palette="Paired")+
                                  opts(title=title)+
                                  xlab("Year") + 
                                  ylab(paste("Value")) + 
                                  opts(axis.text.x=theme_text(angle=90, hjust=0))                                  

  ##regular mapping
  #county_sp=readOGR(dsn=shp_path,layer=lyr)
  #county_sp@data=merge(county_sp@data,simulation.m,by.x="county_id",by.y="county_id",all.x=TRUE,sort=F)
  #print(county_sp@data)
  brks=classIntervals(simulation.m$growth,n=2, style="jenks")
  brks=brks$brks
  #colors=brewer.pal(length(brks)-1,"Blues")
  #label=rep(0,length(brks)-1)
  #for (i in 1:length(brks)-1)
  #{
  #  temp=paste(as.character(round(brks[i])),"-",as.character(round(brks[i+1])),sep=" ")
  #  label[i]=temp
  #}
  #interval <- findInterval(county_sp@data$growth, brks,all.inside=T)
  #col<- colors[interval]
  #map<-plot(county_sp,col=col, axes=T,lwd=0.1,lty=3)
  #title(title)
  #text(y=county_sp@data$lat,x=county_sp@data$long,labels=county_sp@data$growth)
  #print(sprintf("Outputting Map %s to PDF",title))
  #viewPortFunc(map)
  #print(names(county_sp))
  
  ##ggplot map  
  county_sp1 <- readShapeSpatial(qual_shp_file)
  county_ftfy <- fortify(county_sp1, region="id")
  county_sp_data <- merge(county_ftfy,simulation.m,by.x="id", by.y="county_id")
  
  g5 <-  ggplot(county_sp_data, aes(map_id = id)) +
    geom_map(aes(fill=growth, group=growth),map =county_sp_data) + #aes(alpha = growth),
    scale_x_continuous() + 
    scale_fill_gradient(low = "white", high = "black" , guide = "colorbar") + 
    opts(title=paste("Pct. Growth, ",title))+
    #guides(fill = guide_colorbar(colours = topo.colors(10))) +
    #opts(legend.position = "right")+
    #opts(panel.background = theme_rect(fill = "lightgrey"))+
    #geom_polygon(aes(x = county_ftfy$long, y = county_ftfy$lat,group=id), 
    #             fill = NA, colour = 'darkgrey', data = county_sp_data) +
    #               scale_fill_gradient(low = "antiquewhite", high = "darkred") #+
    expand_limits(x = county_ftfy$long, y = county_ftfy$lat)
  
  #scale_alpha(range = c(1, 1), na.value = 1)
  
  #print(p1)
  
  if(Sys.getenv("HUDSON_DRAFT_RESULTS")=='true') {
    g3 <- g3 + annot()  +opts(title=paste("TEST RUN ",title))
    g4 <- g4 + annot()  +opts(title=paste("TEST RUN ",title))
    g5 <- g5 + annot()  +opts(title=paste("TEST RUN ",title))
    tblOut <- grid.arrange(g1, ncol=1, main=textGrob(paste("\n","TEST RUN ", title),gp=gpar(fontsize=14,fontface="bold"))) #,sub=stamp)
  }
  else
  {
    tblOut <- grid.arrange(g1, ncol=1, main=textGrob(paste("\n", title),gp=gpar(fontsize=14,fontface="bold"))) #,sub=stamp)
  }

  #out <- grid.arrange(g3, ncol=1, main=textGrob(paste("\n",title),gp=gpar(fontsize=14,fontface="bold")))
  viewPortFunc(g3)
  print(sprintf("Outputting Chart %s to PDF",title))
  grid.text(stamp,x=unit(0.85,"npc"),y=unit(0.95,"npc"),gp=gpar(fontsize=7,fontface="italic"))  
  
  viewPortFunc(g4)
  print(sprintf("Outputting Area Chart %s to PDF",title))
  grid.text(stamp,x=unit(0.85,"npc"),y=unit(0.95,"npc"),gp=gpar(fontsize=7,fontface="italic"))
  
  viewPortFunc(g5)
  print(sprintf("Outputting Map %s to PDF",title))
  
  ## third, send table to pdf  
  #out <- grid.arrange(g1, ncol=1, main=textGrob(paste("\n",title),gp=gpar(fontsize=14,fontface="bold"))) #,sub=stamp)
  print(sprintf("Outputting Table %s to PDF",title))
  grid.text(stamp,x=unit(0.85,"npc"),y=unit(0.95,"npc"),gp=gpar(fontsize=7,fontface="italic")) 
  print(tblOut)
  #dev.off()  
  
}

garbage <- dev.off()
sprintf("File is ready: %s", fileNameOut)
#warnings()

##county ids used in data
#1  Alameda  ala
#7  Contra Costa  cnc
#21  Marin	mar
#28	Napa	nap
#38	San Francisco	sfr
#41	San Mateo	smt
#43	Santa Clara	scl
#48	Solano	sol
#49	Sonoma	son
###

## second send area chart to pdf...
#g4 <- ggplot(data=simulation_long_abs,
#             aes(x=(year), y=value)) +
#               geom_area(aes(fill=county, group = county), position='stack', alpha=.5) + scale_fill_brewer(palette="Paired")+ # scale_fill_hue(l=40) #scale_fill_brewer() +
#               opts(title=title)+
#               xlab("Year") + 
#ylab(paste("Count")) + 
#               opts(axis.text.x=theme_text(angle=90, hjust=0)) + #guides(colour = guide_legend(override.aes = list(alpha = 1))) +
#opts(panel.border  = theme_rect(colour = 'black')) + 
#opts(panel.grid.major = theme_line(colour = 'grey', size = .25, linetype = 'solid')) +
#opts(panel.grid.minor = theme_line(colour = 'grey', size = .1, linetype = 'dashed')) +
#              guides(fill = guide_legend(reverse = TRUE)) 
#scale_y_continuous(labels="comma")
