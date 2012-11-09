require("stringr")
require("ggplot2")
require("reshape")
require("gridExtra")
require("RGraphics")
require("scales")
#library(directlabels)
library(RColorBrewer)
args <- commandArgs(TRUE)

## grab arguments
#args <- c('/home/aksel/workspace/opus/data/bay_area_parcel/runs/run_257.2012_10_03_00_45/indicators','2010','2011','204',"FALSE","No_Project")
pth <-args[1]
yrStart <- as.integer(args[2])
yrEnd <- as.integer(args[3])
run_id <- args[4]
scenario <- args[5]
setwd(pth)

manyColors <- colorRampPalette(brewer.pal(name = 'Set3',n=10))
#theme_set(theme_grey())
##generic line plot function

# define function to create multi-plot setup (nrow, ncol)
vp.setup <- function(x,y){
  # create a new layout with grid
  grid.newpage()
  # define viewports and assign it to grid layout
  pushViewport(viewport(layout = grid.layout(x,y)))  
}
# define function to easily access layout (row, col)
vp.layout <- function(x,y){
  viewport(layout.pos.row=x, layout.pos.col=y)
}

dt.pda<-c(.78,.60,.34,.33,.92,.78,.84,.56,.65,.70,.57,.23,.18,.85,.60,.71,.33,.47)
lCounties <-c('Alameda','Contra Costa','Marin','Napa','San Francisco','San Mateo','Santa Clara','Solano','Sonoma')
targetPDAData <- structure(dt.pda, 
                           dim = c(9,2),
                           .Dimnames = list(lCounties,c('hh','jobs')))


###########################################################################
#PDA matching chart. TODO: could use some cleaning
#TODO: problem if end year is not 2040. Other sections deal, but here we
#only have target data for 2010 and 2040. We could assume the same
#share by 20xx as by 2040.

dt<-c(.78,.60,.34,.33,.92,.78,.84,.56,.65,.70,.57,.23,.18,.85,.60,.71,.33,.47)
lCountiesShort <-c('ala','cnc','mar','nap','sfr','smt','scl','sol','son')
lCountiesShort <-c('Alameda','Contra Costa','Marin','Napa','San Francisco','San Mateo','Santa Clara','Solano','Sonoma')
targetData <- data.frame(structure(dt, dim = c(9,2), .Dimnames = list(lCountiesShort,c('households','employment'))))
targetData$county<-rownames(targetData)
simFiles <- c('county_table-3_2010-2040_county__county_employment.tab','county_table-3_2010-2040_county__county_employment_pda.tab',
              'county_table-3_2010-2040_county__county_households.tab','county_table-3_2010-2040_county__county_households_pda.tab')
targetData.m <-melt(targetData, id.vars='county')
targetData.m$obs_pred <-'target'
targetData.m <- targetData.m[,c(1,4,3,2)] 

##get county-level files from simFiles list, flatten and melt
##  create list with data tables
dat<-lapply(simFiles,read.csv,header=T,sep = "\t")

## flatten list to to get vector with nice variable names
fileAndTypesLst<- lapply(simFiles,function(x) strsplit(x,"\\."))
fileAndTypesFlattened = lapply(fileAndTypesLst, ldply)
fileNameClean <- ldply(fileAndTypesFlattened)[,1]
fileNameClean <- ldply(lapply(fileNameClean, gsub, pattern="county.+\\d{4}-\\d{4}_",replacement=""))
title_split <- lapply(fileNameClean,strsplit, "_")
title_concat <- ldply(lapply(title_split[[1]][1:length(title_split[[1]])],paste, sep="", collapse = " "))
title_concat_short <- ldply(lapply(title_concat,gsub, pattern="county\\s+|region\\s+",replacement=""))
#title <- paste(title_concat[[1]], sep=" ", collapse = " ")
names(dat) <- ldply(title_concat_short)[2:ncol(title_concat_short),2]

##calculate the share of the growth that happens in PDAs
#households
names(dat$"households pda")
dat$households$growth<-(dat$"households pda"$county_households_pda_2040.f8-dat$"households pda"$county_households_pda_2010.f8)/
  (dat$households$county_households_2040.f8-dat$households$county_households_2010.f8)
#employment
dat$employment$growth<-(dat$"employment pda"$county_employment_pda_2040.f8-dat$"employment pda"$county_employment_pda_2010.f8)/
  (dat$employment$county_employment_2040.f8-dat$employment$county_employment_2010.f8)
#lapply(dat,"[[",32)

## 1) transform appropriately for ease of use/ggplot
df.m<-melt(dat, id.vars=c("county_id.i8"))
df.m<-df.m[df.m[,1] %in% c(49,48,43,41,38,28,21,7,1),]
df.m[,1] <-factor(df.m[,1], labels=lCountiesShort)

ptrn <- "([0-9]{4})|growth" #"^[^[:digit:]]*"  
df.m[,2] <-str_extract(df.m[,2],ptrn) 
df.m<-df.m[df.m[,2] %in% c("growth"),]

df.t <- as.data.frame(df.m)
names(df.t) <- c("county","obs_pred","value","variable")
data.mix <- rbind(targetData.m,df.t)

fileNameOut=sprintf("region_run_%s_topsheet.pdf",run_id)
fp <- file.path(pth,fileNameOut, fsep = .Platform$file.sep)
sprintf("Preparing file %s for charts and figures...", fileNameOut)
pdf(fileNameOut,height=8.5, width=11,onefile=TRUE)

stackedBarPlot <- function(data,name){
  gOut <- 
    ggplot(data=data.mix[data.mix$obs_pred=='growth',],
           aes(
             x=county, 
             y=value, 
             fill=obs_pred
           ))+
             geom_bar(stat = "identity", alpha=.55,fill="grey20",color="black") + 
             #labs(title=name)+
             opts(title = name)+
             #ylab("value") +
             opts(axis.text.x=theme_text(angle=90, hjust=0)) +
             #opts(legend.key.width = unit(.6, "cm")) +
             opts(legend.position = "right")+
             #opts(keep = "legend_box")+
             scale_y_continuous(labels=percent)  +
             facet_grid( . ~variable) +
             opts(strip.text.x = theme_text(size = 14, colour = "black", angle = 0))+
             #theme_bw() +
             #opts(panel.margin = unit(4, "lines"))+
             #add targets             
             geom_point(data=data.mix[data.mix$obs_pred!='growth',],aes(
               x=county, 
               y=value, 
               fill=obs_pred
             ),shape=21, size=4, fill="steelblue4",alpha=.55)
  #scale_linetype_manual(values = lty)      +
  #opts(legend.position="none")
  return(gOut)
}
l<-stackedBarPlot(data.mix,"Comparison of Actual to Target PDA Growth")              
print(l)
  
dev.off()

