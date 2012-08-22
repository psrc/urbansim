##example of connecting with numpy binary files, constructing data frame, generating basic plots
#args <- commandArgs(TRUE)
library(plyr)
library(ggplot2)
library(reshape)
library(plyr)
require(scales)
library(RColorBrewer)

#pth <-args[1]
#outPth <- args[2]
readSingleColumn <- function(pth) {
  setwd(pth)
  fileList = list.files(path=pth)#, pattern=ptrn)
  
  ##get list with file types to enable proper loading of binary.
  ##then transform unwieldy list to get filetypes
  fileAndTypes<- lapply(fileList,function(x) strsplit(x,"\\."))
  fileAndTypes2 = lapply(fileAndTypes, ldply)
  fileTypesClean = ldply(fileAndTypes2)[,1:2]
  fileTypesClean[,2] <- ldply(lapply(fileTypesClean[,2], gsub, pattern="\\d",replacement=""))
  names(fileTypesClean) <- c("variable","binarytype")
  
  ##lookup between binary files and R's categories
  typeMapping <- list("li"= "integer", "lf"= "double", "iS"="character")
  fileTypesClean$filename <- fileList
  
  ##grab binary file
  column <-fileTypesClean$filename[2]
  dat<-readBin(column,endian = "little", 
               what=typeMapping[gsub(pattern="\\d",replacement="",strsplit(column,"\\.")[[1]][[2]])][[1]],
               n=1984716,size=ifelse(sub(".*?(\\d)", "\\1", column, perl=TRUE)<=4,sub(".*?(\\d)", "\\1", column, perl=TRUE),4)) #last argument gets byte-size from filename
  ##throw in data frame, shape properly for ggplot
  dt <-as.data.frame(ldply(dat))
  colnames(dt) <- column
  return(dt)
}

readBinary <- function(pth){
  setwd(pth)
  fileList = list.files(path=pth)#, pattern=ptrn)
  
  ##get list with file types to enable proper loading of binary.
  ##then transform unwieldy list to get filetypes
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
                        endian = "little",                    
                        what=typeMapping[gsub(pattern="\\d",
                                              replacement="",strsplit
                                              (fileList[2],"\\.")[[1]][[2]])][[1]],n=2e5, 
                        size=ifelse(sub(".*?(\\d)", "\\1", x, perl=TRUE)<=4,sub(".*?(\\d)", "\\1", x, perl=TRUE),4)) }) #last argument gets byte-size from filename
  ##throw in data frame, shape properly for ggplot
  dt <-as.data.frame(t(ldply(dat)))
  colnames(dt) <- fileTypesClean[2:nrow(fileTypesClean),1]
  return(dt)
}

################################################################################
##call function#################################################################
################################################################################
pth <-"/home/aksel/Documents/Data/Urbansim/run_139/2040/buildings"
dt<-readBinary(pth)
dtSingle <- readSingleColumn(pth)
names(dt)
names(dtSingle)
length((dtSingle))
dt.m <- melt(dt[,c(1,2,12)], id=c("year_built","building_type_id"),direction = "long")
dt.m <- cast(dt.m,year_built + building_type_id ~ variable, sum)
dt.m2 <- melt(dt[,c(1,2)], id=c("building_type_id"),direction = "long")


##generate histogram w density
#setwd(outPth)
pdf("/home/aksel/Downloads/testChart.pdf",height=8.5, width=11,onefile=TRUE)
ggplot(dt.m2, aes(x=value)) + 
  geom_histogram(aes(y=..density..),      # Histogram with density instead of count on y-axis
                 binwidth=1000,
                 colour="black", fill="steelblue1") +
                   geom_density(alpha=.2,size = 2 ) + #, fill="orange") +
                   xlab("square feet") +
                   opts(title="Dev Events Size Distribution") +
                   opts(legend.position=c(.24, .95), legend.justification = c(1, 1)) +
                   scale_x_continuous(limits=c(0, 1e4))
#scale_y_continuous(labels=percent) 


##generate line plot
ggplot(dt.m, aes(x=year_built,y=building_sqft,
                 fill=as.factor(building_type_id),
                 group=as.factor(building_type_id),
                 )) + 
                   geom_bar(stat = "identity", position = "stack") + scale_fill_brewer(palette = "Set1") + 
                   opts(title = "Sqft by year by type") +
                   labs(x = "Year", y = "Square Feet",
                        fill = NULL)+
                          scale_x_continuous(limits=c(1900, 2040))
dev.off()
