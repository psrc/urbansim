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
library(RColorBrewer)
library(directlabels)

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

viewPortFunc <- function(printObject=printObject,newPage=T){
  if(newPage==T){
    grid.newpage()
  }
  pushViewport(viewport(height=unit(0.9, "npc"), width=unit(0.95, "npc"), x=0.5, y=0.5, name="vp")) 
  upViewport() 
  print(printObject, vp="vp")
  #print(sprintf("Outputting Chart %s to PDF",title))
}

manyColors <- function(n) {
  black <- "#000000"
  if (n <= 9) {
    c(black,brewer.pal(n-1, "Set2"))
  } else {
    c(black,hcl(h=seq(0,(n-2)/(n-1),
                      length=n-1)*360,c=100,l=65,fixup=TRUE))
  }
}

mapStuff <- function(data,shapefile){
  simulation.m <- data
  geography_sp1 <- shapefile
  
  if(range(simulation.m$growth>0, na.rm = TRUE))
  {
    brks=classIntervals(simulation.m$growth,n=6, style="jenks")
    brks=brks$brks
  }
  else 
  {
    brks=rep(0,6)
  }
  geography_ftfy <- fortify(geography_sp1, region="gid")
  geography_sp_data <- merge(geography_ftfy,simulation.m,by.y="geography_id", by.x="id",all.x=TRUE)
  
  ##prep ggplot object
  g5 <-  ggplot(geography_sp_data, aes(map_id = id)) +
    geom_map(aes(fill=growth, group=growth),map =geography_sp_data) + #aes(alpha = growth),
    scale_x_continuous() + 
    scale_fill_gradient(low = "white", high = "black" , guide = "colorbar") + 
    opts(title=paste("Pct. Growth, ",title))+
    #guides(fill = guide_colorbar(colours = topo.colors(10))) +
    #opts(legend.position = "right")+
    opts(panel.background = theme_rect(fill = "lightskyblue3"))+
    #geom_polygon(aes(x = geography_ftfy$long, y = geography_ftfy$lat,group=id), 
    #             fill = NA, colour = 'darkgrey', data = geography_sp_data) +
    #               scale_fill_gradient(low = "antiquewhite", high = "darkred") #+
    expand_limits(x = geography_ftfy$long, y = geography_ftfy$lat)
  return(g5)
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
scenario<-args[6]
geo<-args[7]
pth <-args[1]
yrStart <- as.integer(args[2])
yrEnd <- as.integer(args[3])
setwd(pth)
shp_file <- args[5]
shp_path <- args[4]
qual_shp_file <- file.path(shp_path,shp_file,fsep = .Platform$file.sep)
lyr <- strsplit(shp_file,"\\.")[[1]][1]
geography_sp1 <- readShapeSpatial(qual_shp_file)
correspondence<- as.data.frame((geography_sp1@data[,c(2,ncol(geography_sp1@data))]))  #use for column names of matrix later

## function to render a matrix WITH a regional total if absolute values, otherwise no total
returnMatrix <- function(inputData=inputData,tableName=tableName) {
  if (grepl("average",tableName,ignore.case=TRUE) | grepl("avg",tableName,ignore.case=TRUE)) {
    print("avg")
    inputData$year <- as.integer(rownames(inputData))
    meltedInputData <- melt(inputData,id="year",variable_name = "geography")
  }
  else #if (grep("average",fName,ignore.case=FALSE, fixed=T))
  {
    print("not avg")
    inputData$Region <- rowSums(inputData,na.rm = FALSE, dims = 1)
    inputData$year <- as.integer(rownames(inputData))
    #inputData <- as.data.frame(inputData)
    meltedInputData <- melt(inputData[,c(seq(1,length(names(inputData))-2),length(names(inputData)))],id="year",variable_name = "geography")
    #print(meltedInputData)
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

#geo<-"superdistrict"
##  select folder with indicator files, fetch all beginning with "county..." having proper years in name
ptrn <-sprintf("^%s%s%s_%s-%s%s",geo,"_table-","[0-9]",yrStart,yrEnd,".+")
fileList = list.files(path=pth, pattern=ptrn)
if (length(fileList) == 0)
{
  stop(sprintf("Failed to find any county indicators for years %s to %s in %s", yrStart, yrEnd, pth))
}

##  "loop" construct, create dataframe, chart for each tab file
dat<-lapply(fileList,read.csv,header=T,sep = "\t")

## start pdf object to store all charts
fp <- file.path(pth, fsep = .Platform$file.sep)
fileNameOut=sprintf("%s/%s_plot_%s_indexChart.pdf",fp,geo,runid)
sprintf("Preparing file %s for charts and figures...", fileNameOut)
pdf(fileNameOut,height=11, width=17,onefile=TRUE)

## store each file in a dataframe, process and plot as we go.
for(i in 1:length(dat)) 
{
  simulation <- as.data.frame(dat[i])  #technically redundant; could just use dat list object
  #simulation <- read.csv("/home/aksel/Documents/Data/Urbansim/run_107.2012_07_26_21_39/indicators/superdistrict_table-3_2012-2020_superdistrict__superdistrict_urbanized_acres.tab",header=T,sep = "\t")  
  ## subset to keep only relevant counties (using the arbitrary objectid in geography_county.id)
  if(geo=="county"){
    simulation <- simulation[simulation[,1] %in% c(49,48,43,41,38,28,21,7,1),  ]  
  }
  else if(geo=="superdistrict")  {
    ##posstible subsetting
    #simulation <- simulation[simulation[,1] %in% seq(1:25),  ] 
  }  
  
  ##keep minimal data frame for mapping
  strYrStart<-sprintf("yr_%s",yrStart)
  strYrEnd<-sprintf("yr_%s",yrEnd)
  simulation.m <- simulation[c(1,2,length(names(simulation)))]
  
  n=length(simulation.m)
  simulation.m$growth=(simulation.m[n]-simulation.m[2])/simulation.m[2]
  simulation.m=data.frame(simulation.m[1],simulation.m$growth)
  #replace(simulation.m, simulation.m[n]==Inf, 0)
  simulation.m[is.na(simulation.m)] <- 0
  #simulation.m[simulation.m[n]==Inf] <- 0
  names(simulation.m)=c("geography_id","growth")
  
  ## convert id key to factor levels for more meaningful labeling. Labels are assigned based on factor numerical order.
  #geogr_name <- c('ala','cnc','mar','nap','sfr','smt','scl','sol','son')
  #geogr_name <-  c('Alameda','Contra Costa','Marin','Napa','San Francisco','San Mateo','Santa Clara','Solano','Sonoma')
  #simulation[,1] <-factor(simulation[,1], labels=geogr_name)
  
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
  title <- paste(scenario,title)
  #fileNameOutChart=sprintf("%s/plot_%s_indexChart_%s.pdf",fp,runid,title)
  #fileNameOutTable=sprintf("%s/plot_%s_indexTable_%s.pdf",fp,runid,title)
  
  yrNames <- c('geography',years)
  ## assign new colunn names
  names(simulation) <-yrNames
  
  ## Transpose frame so cols are county series, rows are years
  simulation.t <- t(simulation[,2:ncol(simulation)])
  ## Set column headings as counties
  
  colnames(simulation.t) <- paste(correspondence[,2],"_",simulation[,1],sep="")
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
  simulation_long_index <- melt(simulation.i,id="year",variable_name = "geography")
  
  ## prepare plotting
  ## table object prep for chart
  cols<-ncol(simulation.t)
  end<-(yrEnd - yrStart + 1)
  if (end > 26 ) {
    step <- 2 
  }
  else {
    step <- 1
  }
  if ((cols) > 15 ) {
    endCol <- (cols-1)/2
    print("Splitting Table")
  }
  else {
    endCol <- (cols-1)
  }
  
  g1 <- tableGrob(
    format(
      simulation.t[seq(1,end,step),1:endCol], 
      digits = 2,big.mark = ","), 
    gpar.colfill = gpar(fill=NA,col=NA), 
    gpar.rowfill = gpar(fill=NA,col=NA), 
    h.even.alpha = 0,
    gpar.rowtext = gpar(col="black", cex=0.8,
                        equal.width = TRUE,
                        show.vlines = TRUE, show.hlines = TRUE, separator="darkgrey")                     
    )
  
  if ((cols) > 15 ) {
    endCol <- (cols-1)/2
    print("Splitting Table")
    g2 <- tableGrob(
    
    format(
      simulation.t[seq(1,end,step),(2+endCol):length(names(simulation.t))], 
      digits = 2,big.mark = ","), 
      gpar.colfill = gpar(fill=NA,col=NA), 
      gpar.rowfill = gpar(fill=NA,col=NA), 
      h.even.alpha = 0,
      gpar.rowtext = gpar(col="black", cex=0.8,
      equal.width = TRUE,
      show.vlines = TRUE, show.hlines = TRUE, separator="grey")                     
    )
    
    }
  
  #string <- "
  #placeholder for possible annotation
  #this projection is characterized by xyz...
  #"
  #g2 <- splitTextGrob(string)
  theme_set(theme_grey()); 
  #theme_set(theme_bw());
  
  ## plot object
  stamp <- sprintf("Simulation #%s run on %s\nReport generated on %s",id,format(runDate, "%a %b %d %T"),format(Sys.time(), "%a %b %d %T"))
  ## first send line chart to pdf...
  
  g3 <- ggplot(data=simulation_long_index,
               aes(
                 x=as.factor(year), 
                 y=value, 
                 colour=geography,
                 group=geography)) +
                     geom_line(size=.65) + 
                       scale_colour_manual(values=manyColors(cols)) +
#                        aes(
#                          linetype=geography), size = .65) +       # Thin line, varies by 
#                            scale_fill_brewer(palette="Paired") +
                            geom_point(size=2.5) +
                              scale_colour_manual(values=manyColors(cols)) +
#                                shape=geography) ,  size = 2.5)   +       
#                                  scale_fill_brewer(palette="Paired")+
                                 opts(title=title)+
                                 xlab("Year") + 
                                 ylab(paste("Indexed Value (Rel. to ",yrStart,")")) + 
                                 opts(axis.text.x=theme_text(angle=90, hjust=0))
#                                  
  g3 <- direct.label(g3, list(last.bumpup, hjust = 0.7, vjust = 1))
   #g3 <- qplot(data=simulation_long_index, aes(x=year,y=value, colour=geography)) + geom_line() 
                     
   g4 <- ggplot(data=simulation_long_abs,
               aes(
                 x=as.factor(year), 
                 y=value, 
                 colour=geography,
                 group=geography)) +
                   geom_line(size=.65) + 
                     scale_colour_manual(values=manyColors(cols)) +
#                        aes(
#                          linetype=geography), size = .65) +       # Thin line, varies by 
#                            scale_fill_brewer(palette="Paired") +
                                 geom_point(size=2.5) +
                                 scale_colour_manual(values=manyColors(cols)) +
#                                shape=geography) ,  size = 2.5)   +       
#                                  scale_fill_brewer(palette="Paired")+
                                 opts(title=title)+
                                 xlab("Year") + 
                                 ylab(paste("Value")) + 
                                 opts(axis.text.x=theme_text(angle=90, hjust=0))
  g4 <- direct.label(g4, list(last.bumpup, hjust = 0.7, vjust = 1))
  
  ##non-ggplot mapping
  #county_sp=readOGR(dsn=shp_path,layer=lyr)
  #county_sp@data=merge(county_sp@data,simulation.m,by.x="county_id",by.y="county_id",all.x=TRUE,sort=F)

  ##ggplot map call
  g5<-mapStuff(simulation.m,geography_sp1)
  
  #scale_alpha(range = c(1, 1), na.value = 1)
  
  if(Sys.getenv("HUDSON_DRAFT_RESULTS")=='true') {
    g3 <- g3 + annot()  +opts(title=paste("TEST RUN ",title))
    g4 <- g4 + annot()  +opts(title=paste("TEST RUN ",title))
    g5 <- g5 + annot()  +opts(title=paste("TEST RUN ",title))
    tblOut <- grid.arrange(g1,g2, nrow=2, main=textGrob(paste("\n","TEST RUN ", title),gp=gpar(fontsize=14,fontface="bold"))) #,sub=stamp)
    grid.text(stamp,x=unit(0.85,"npc"),y=unit(0.95,"npc"),gp=gpar(fontsize=7,fontface="italic")) 
    #tblOut2 <- grid.arrange(g2, ncol=1, main=textGrob(paste("\n","TEST RUN ", title),gp=gpar(fontsize=14,fontface="bold"))) #,sub=stamp)
  }
  else
  {
    tblOut <- grid.arrange(g1,g2, nrow=2, main=textGrob(paste("\n", title),gp=gpar(fontsize=14,fontface="bold"))) #,sub=stamp)
  }

  #out <- grid.arrange(g3, ncol=1, main=textGrob(paste("\n",title),gp=gpar(fontsize=14,fontface="bold")))
  viewPortFunc(g3,T)
  print(sprintf("Outputting Chart %s to PDF",title))
  grid.text(stamp,x=unit(0.85,"npc"),y=unit(0.95,"npc"),gp=gpar(fontsize=7,fontface="italic"))  
  
  viewPortFunc(g4,T)
  print(sprintf("Outputting Area Chart %s to PDF",title))
  grid.text(stamp,x=unit(0.85,"npc"),y=unit(0.95,"npc"),gp=gpar(fontsize=7,fontface="italic"))
  
  viewPortFunc(g5,T)
  print(sprintf("Outputting Map %s to PDF",title))
  grid.text(stamp,x=unit(0.85,"npc"),y=unit(0.95,"npc"),gp=gpar(fontsize=7,fontface="italic"))
  
  ## third, send table to pdf  
  print(sprintf("Outputting Table %s to PDF",title))
  print(tblOut)
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
# c25 <- c("dodgerblue2","#E31A1C", # red
#          "green4",
#          "#6A3D9A", # purple
#          "#FF7F00", # orange
#          "black","gold1",
#          "skyblue2","#FB9A99", # lt pink
#          "palegreen2",
#          "#CAB2D6", # lt purple
#          "#FDBF6F", # lt orange
#          "gray70", "khaki2",
#          "maroon","orchid1","deeppink1","blue1","steelblue4",
#          "darkturquoise","green1","yellow4","yellow3",
#          "darkorange4","brown")
# pie(rep(1,25), col=c25)
