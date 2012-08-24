require("stringr")
require("ggplot2")
require("reshape")
require("gridExtra")
require("RGraphics")
require("scales")
library(directlabels)
library(RColorBrewer)
args <- commandArgs(TRUE)

## grab arguments
args <- c('/home/aksel/Documents/Data/Urbansim/run_134/indicators','2010','2040','134',"TRUE","No_Project")
pth <-args[1]
yrStart <- as.integer(args[2])
yrEnd <- as.integer(args[3])
run_id <- args[4]
travelModelRan <- args[5]
scenario <- args[6]

pdf("/home/aksel/Downloads/test.pdf",height=8.5, width=11,onefile=TRUE)

travelYears <- c('2018','2025','2035')
lCounties <- c('Alameda','Contra Costa','Marin','Napa','San Francisco','San Mateo','Santa Clara','Solano','Sonoma','All')

viewPortFunc <- function(printObject=printObject){
  grid.newpage()
  pushViewport(viewport(height=unit(0.9, "npc"), width=unit(0.95, "npc"), x=0.5, y=0.5, name="vp")) 
  upViewport() 
  print(printObject, vp="vp")
  #print(sprintf("Outputting Chart %s to PDF",title))
}
manyColors <- colorRampPalette(brewer.pal(name = 'Set3',n=10))

##generic line plot function
linePlot <- function(data,name){
  gOut <- ggplot(data=data,
                 aes(
                   x=variable, 
                   y=value, 
                   colour=geography,
                   group=geography,
                   linetype = geography))+
                     geom_line(size=1.75) + 
                     scale_colour_manual(values=manyColors(9)) +
                     geom_point(size=1.8) +
                     opts(title=name)+
                     xlab("Year") + 
                     ylab(name) +
                     opts(axis.text.x=theme_text(angle=90, hjust=0)) +
                     opts(legend.key.width = unit(1, "cm")) +
                     scale_y_continuous(labels=comma) +
                     #scale_linetype_manual(values = lty)      +
                     opts(legend.position="none")
  return(gOut)
}

stackedBarPlot <- function(data,name){
  gOut <- ggplot(data=data,
                 aes(
                   x=variable, 
                   y=value, 
                   fill=geography
                   ))+
                     geom_bar(alpha =.65) + 
                     scale_colour_manual(values=manyColors(9)) +
                     scale_fill_brewer(palette="Set3") +
                     opts(title=name)+
                     xlab("Year") + 
                     ylab(name) +
                     opts(axis.text.x=theme_text(angle=90, hjust=0)) +
                     opts(legend.key.width = unit(.6, "cm")) +
                     scale_y_continuous(labels=comma) +
                     guides(fill = guide_legend(reverse = TRUE))
  #scale_linetype_manual(values = lty)      +
  #opts(legend.position="none")
  return(gOut)
}

#########################################################################
##get county-level population data
countyPopFile <- sprintf('county_table-3_%s-%s_county__county_population.tab',yrStart,yrEnd)
countyPopPth <- file.path(pth,countyPopFile,fsep = .Platform$file.sep)
lCounties <- c('Alameda','Contra Costa','Marin','Napa','San Francisco','San Mateo','Santa Clara','Solano','Sonoma')#,'ALL')
countyPopRaw <- read.csv(countyPopPth,sep="\t")
countyPop <- countyPopRaw[countyPopRaw[,1] %in% c(49,48,43,41,38,28,21,7,1),  ]
ptrn <- "([[:digit:]]{4})"  
names(countyPop) <- c("county",str_extract(names(countyPop)[2:ncol(countyPop)],ptrn))
#countyPop <- rbind(countyPop,c("ALL",colSums(countyPop[,2:ncol(countyPop)])))
countyPop[,1] <-factor(countyPop[,1], labels=lCounties)

##see if travel model years are in run
if(yrEnd==2040){
  #extra=F
  ##check if out years are included 
  #g1 <- makeTable(df.t[c("Indicator","2010","2018","2025","2035","2040")])
  popData <- data.frame(countyPop[,c("county","2018","2025","2035")])
  names(popData) <- c("county",2018,2025,2035)
  extra=T
} else {
  popYearsKeepers <- travelYears<=yrEnd
  popData <- data.frame(countyPop[,c("county",yrStart,travelYears[popYearsKeepers])])
  names(popData) <- c("county",yrStart,travelYears[popYearsKeepers])
  #g1 <- makeTable(df.t[c(1,2,ncol(df.t))])
}
# popData <- structure(runif(27,10000,100000), 
#                      dim = c(9,3),
#                      .Dimnames = list(lCounties,travelYears))
############################################################################
##process EMFAC MTC data
#par(mai=c(.75,.75,.75,2.75))
mtcDataFiles <- ldply(lapply(travelYears,
                             function(x) sprintf("%s/EMFAC2011-SG Summary - Year_%s - Group 1.csv",
                                                 file.path(pth, fsep = .Platform$file.sep),x)))                      
mtcData<-lapply(mtcDataFiles[[1]],read.csv,header = TRUE, sep = ",", quote="\"")
keepers<-8:21  #indices of numeric and relevant columns to plot
for(i in keepers){
  if(i %in% c(9,11)){
    mtcData.f <- data.frame(
      mtcData[[1]][2:10,4], 
      mtcData[[1]][2:10,i]/as.integer(popData[,2]),
      mtcData[[2]][2:10,i]/as.integer(popData[,3]),
      mtcData[[3]][2:10,i]/as.integer(popData[,4]))
    nme <- paste(names(mtcData[[1]])[i],"per capita")
  } else {
  mtcData.f <- data.frame(mtcData[[1]][2:10,4], mtcData[[1]][2:10,i],mtcData[[2]][2:10,i],mtcData[[3]][2:10,i])
  nme <- names(mtcData[[1]])[i]
  }
  names(mtcData.f) <- c("geography",2018,2025,2035)
  #VMT$geography <- c("region",as.vector(substr(x=VMT$geography[2:10],start=1,last=length(VMT$geography[2:10])-5)))
  mtcData.f.m <- melt(mtcData.f,id="geography")
  g8 <- stackedBarPlot(mtcData.f.m,"value") + opts(title=nme)
  g7 <- linePlot(mtcData.f.m,"value") + opts(title=nme)
  g7 <- direct.label(g7, list(last.points, hjust = 0.7, vjust = 1,fontsize=12))
  viewPortFunc(g7)
  viewPortFunc(g8)
  }
#mtcData <- "/var/www/MTC_Model/No_Project/run_139"
garbage <- dev.off()
