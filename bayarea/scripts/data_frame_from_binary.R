##example of connecting with numpy binary files, constructing data frame, generating basic plots
library(plyr)
library(ggplot2)
library(reshape)
library('plyr')
require(scales)
library(RColorBrewer)

pth <-"/home/aksel/Documents/Data/Urbansim/run_134/2010/scheduled_development_events"
setwd(pth)
fileList = list.files(path=pth)#, pattern=ptrn)

##transform unwieldy list to get filetypes
  fileAndTypes<- lapply(fileList,function(x) strsplit(x,"\\."))
  fileAndTypes2 = lapply(fileAndTypes, ldply)
  fileTypesClean = ldply(fileAndTypes2)[,1:2]
  fileTypesClean[,2] <- ldply(lapply(fileTypesClean[,2], gsub, pattern="\\d",replacement=""))
  names(fileTypesClean) <- c("variable","binarytype")

##lookup between binary files and R's categories
  typeMapping <- list("li"= "integer", "lf"= "double", "iS"="character")
  fileTypesClean$filename <- fileList
  
##grab binary files
  dat<-lapply(fileTypesClean[2:nrow(fileTypesClean),3],
              function(x) {
              readBin(x, 
                      endian = "big",                    
                      what=typeMapping[gsub(pattern="\\d",
                                               replacement="",strsplit
                                           (fileList[2],"\\.")[[1]][[2]])][[1]],n=200)})
##throw in data frame, shape properly for ggplot
  dt <-as.data.frame(t(ldply(dat)))
  colnames(dt) <- fileTypesClean[2:nrow(fileTypesClean),1]
  dt.m <- melt(dt[,c(1,2,12)], id=c("scheduled_year","building_type_id"),direction = "long")
  dt.m <- cast(dt.m,scheduled_year + building_type_id ~ variable, sum)
  dt.m2 <- melt(dt[,c(1,2)], id=c("building_type_id"),direction = "long")


##generate histogram w density
  ggplot(dt.m2, aes(x=value)) + 
    geom_histogram(aes(y=..density..),      # Histogram with density instead of count on y-axis
                   binwidth=100000,
                   colour="black", fill="white") +
                     geom_density(alpha=.2, fill="#FF6666") +
                     xlab("square feet") +
                     opts(title="Dev Events Size Distribution") 
                     #scale_y_continuous(labels=percent) 
                     #scale_x_continuous(limits=c(0, 3000))

##generate line plot
  ggplot(dt.m, aes(x=scheduled_year,y=building_sqft,
                   fill=as.factor(building_type_id),
                   group=as.factor(building_type_id),
                   )) + 
                  geom_bar(stat = "identity", position = "stack") + scale_fill_brewer(palette = "Set1") + 
                  opts(title = "Sqft by year by type") +
                  labs(x = "Year", y = "Square Feet",
                       fill = NULL)