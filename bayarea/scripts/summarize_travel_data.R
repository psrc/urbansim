require("stringr")
require("ggplot2")
require("reshape")
require("gridExtra")
require("RGraphics")
require("scales")
library(directlabels)
library(RColorBrewer)
yrStart<-2010
yrEnd<-2040
pth <- "/home/aksel/Documents/Data/Urbansim/run_134/indicators"

viewPortFunc <- function(printObject=printObject){
  grid.newpage()
  pushViewport(viewport(height=unit(0.9, "npc"), width=unit(0.95, "npc"), x=0.5, y=0.5, name="vp")) 
  upViewport() 
  print(printObject, vp="vp")
  #print(sprintf("Outputting Chart %s to PDF",title))
}
manyColors <- colorRampPalette(brewer.pal(name = 'Set3',n=9))

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
                     scale_colour_manual(values=manyColors(12)) +
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
countyPopFile <- 'county_table-3_2010-2040_county__county_population.tab'
countyPopPth <- file.path(pth,countyPopFile,fsep = .Platform$file.sep)
countyPopRaw <- read.csv(countyPopPth,sep="\t")
countyPop <- countyPopRaw[countyPopRaw[,1] %in% c(49,48,43,41,38,28,21,7,1),  ]
countyPop[,1] <-factor(countyPop[,1], labels=lCounties)
ptrn <- "([[:digit:]]{4})"  
names(countyPop) <- c("county",str_extract(names(countyPop)[2:ncol(countyPop)],ptrn))
##see if travel model years are in run
if(yrEnd>=2035){
  popData <- data.frame(countyPop[,c("county","2018","2025","2035")])
  names(popData) <- c("county",2018,2025,2035)
}
travelYears <- c('2018','2025','2035')
lCounties <- c('Alameda','Contra Costa','Marin','Napa','San Francisco','San Mateo','Santa Clara','Solano','Sonoma')
# popData <- structure(runif(27,10000,100000), 
#                      dim = c(9,3),
#                      .Dimnames = list(lCounties,travelYears))
############################################################################
##process EMFAC MTC data
pdf("/home/aksel/Downloads/test.pdf",height=8.5, width=11,onefile=TRUE)
mtcDataFiles <- ldply(lapply(travelYears,function(x) sprintf("/home/aksel/Downloads/EMFAC2011-SG Summary - Year_%s - Group 1.csv",x)))                      
mtcData<-lapply(mtcDataFiles[[1]],read.csv,header = TRUE, sep = ",", quote="\"")
keepers<-8:21  #indices of numeric and relevant columns to plot
for(i in keepers){
  if(i %in% c(9,11)){
    mtcData.f <- data.frame(
      mtcData[[1]][2:10,4], 
      mtcData[[1]][2:10,i]/popData[,2],
      mtcData[[2]][2:10,i]/popData[,3],
      mtcData[[3]][2:10,i]/popData[,4])
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
