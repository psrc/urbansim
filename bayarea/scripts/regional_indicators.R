require("stringr")
require("ggplot2")
require("reshape")
require("gridExtra")
require("RGraphics")
## function for formating chart titles
TitleCase <- function(string="test string")
{
  first <- toupper(substring(string, 1, 1))
  rest <- tolower(substring(string, 2))
  fString <- sprintf("%s%s",first,rest)
  return(fString)
}

makeTable <- function(data){    
  tableGrob(
    format(data
           , 
           digits = 2,big.mark = ","), 
    gpar.colfill = gpar(fill=NA,col=NA), 
    gpar.rowfill = gpar(fill=NA,col=NA), 
    #gpar.corefill = gpar(fill="slateblue",alpha=0.5, col=NA), h.even.alpha = 0.5),
    h.even.alpha = 0,
    gpar.rowtext = gpar(col="black", cex=0.8,
                        equal.width = TRUE,
                        show.vlines = TRUE, show.hlines = TRUE, separator="grey")                     
    )
}
regionalProcessor <- function(pth,yrStart,yrEnd){

  ##  select folder with indicator files, fetch all beginning with "county..." having proper years in name
    #pth <- '/home/aksel/Documents/Data/Urbansim/run_134/indicators'
    #yrStart=2010; yrEnd=2018
    setwd(pth)
    ptrn <-sprintf("^%s%s_%s-%s%s","alldata_table-",3,yrStart,yrEnd,".+")
    fileList = list.files(path=pth, pattern=ptrn)
    if (length(fileList) == 0)
    {
    stop(sprintf("Failed to find any regional indicators for years %s to %s in %s", yrStart, yrEnd, pth))
    }
  
  ##  create list with data tables
    dat<-lapply(fileList,read.csv,header=T,sep = "\t")
  
  ## flatten list to something useful
    fileAndTypesLst<- lapply(fileList,function(x) strsplit(x,"\\."))
    fileAndTypesFlattened = lapply(fileAndTypesLst, ldply)
    fileNameClean = ldply(fileAndTypesFlattened)[,1]
    fileNameClean <- ldply(lapply(fileNameClean, gsub, pattern="alldata.+\\d{4}-\\d{4}_",replacement=""))
    title_split <- lapply(fileNameClean,strsplit, "_")
    title_concat <- ldply(lapply(title_split[[1]][1:length(title_split[[1]])],paste, sep=" ", collapse = " "))
    title_concat_short <- ldply(lapply(title_concat,gsub, pattern="alldata  region ",replacement=""))
    #title_proper <- lapply(title_concat,TitleCase)
    #title <- paste(title_concat[[1]], sep=" ", collapse = " ")
    
    names(dat) <- ldply(title_concat_short)[2:ncol(title_concat_short),2]
  
  ## transform appropriately for ease of use
    df.m<-melt(dat, id="alldata_id.i8")
    ptrn <- "([[:digit:]]{4})"  
    df.m[,2] <-as.integer(str_extract(df.m[,2],ptrn)) 
    df.m <- df.m[,c(2:4)]
    df.t <- as.data.frame(cast(df.m))
    names(df.t)[1] <- "Indicator"
  
  ## grob time    
    g1 <- makeTable(df.t[c(1,2,ncol(df.t))])
  ##plot it
    grid.arrange(g1, nrow=1, main=textGrob(paste("\n","TEST RUN ", "Regional Summary"),gp=gpar(fontsize=11,fontface="bold")))
    
    ## start pdf object to store all charts
    fp <- file.path(pth, fsep = .Platform$file.sep)
    fileNameOut=sprintf("%s/%s_plot_%s_indexChart.pdf",fp,"region","134")
    sprintf("Preparing file %s for charts and figures...", fileNameOut)
    pdf(fileNameOut,height=8.5, width=11,onefile=TRUE)
}    
yrStart<-2010
yrEnd<-2018
pth <- "/home/aksel/Documents/Data/Urbansim/run_134/indicators"
regionalProcessor(pth,yrStart,yrEnd)