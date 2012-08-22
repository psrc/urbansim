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
args <- c('/home/aksel/Documents/Data/Urbansim/run_134/indicators','2010','2018')
pth <-args[1]
yrStart <- as.integer(args[2])
yrEnd <- as.integer(args[3])

## parse path to get runid, run date
split <- strsplit(args[1],"/")[[1]]
pos <- length(split)-1  #this assumes we are one up from the indicators dir--a regex would be better.
runid <- split[pos]
periodPosition <- regexpr("\\.",runid)[[1]]
tm <- strsplit(substr(runid,periodPosition+1,nchar(runid)),"_")
id <- strsplit(substr(runid,1,periodPosition-1),"_")[[1]][2]

manyColors <- colorRampPalette(brewer.pal(name = 'Set3',n=10))
theme_set(theme_grey())
##generic line plot function
linePlot <- function(data,name){
  theme_set(theme_grey(10))
  gOut <- ggplot(data=data,
       aes(
         x=variable, 
         y=value, 
         colour=geography,
         group=geography,
         linetype = geography))+
           geom_line(size=1) + 
           scale_colour_manual(values=manyColors(10)) +
           geom_point(size=1.8) +
           opts(title=name) +#, theme_text(size = 25))+
           xlab("Year") + 
           ylab("Million Tons ???") +
           opts(axis.title.x = theme_text(size = 8, vjust = 0.5)) +
           opts(axis.title.y = theme_text(size = 8, vjust = 0.5,angle=90)) +
           opts(plot.title = theme_text(size = 10, vjust = 0.5)) +
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
                     #scale_colour_manual(values=manyColors(12)) +
                     scale_fill_brewer(palette="Set3") +
                     opts(title=name)+
                     xlab("Year") + 
                     ylab(name) +
                     opts(axis.title.x = theme_text(size = 8, vjust = 0.5)) +
                     opts(axis.title.y = theme_text(size = 8, vjust = 0.5,angle=90)) +
                     opts(plot.title = theme_text(size = 10, vjust = 0.5)) +
                     #opts(axis.text.x=theme_text(angle=90, hjust=0)) +
                     opts(legend.key.width = unit(.6, "cm")) +
                     scale_y_continuous(labels=comma) 
                     #scale_linetype_manual(values = lty)      +
                     #opts(legend.position="none")
  return(gOut)
}

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
    core.just="left",
    col.just="left",
    gpar.coretext=gpar(fontsize=8), 
    gpar.coltext=gpar(fontsize=9, fontface='bold'), 
    gpar.colfill = gpar(fill=NA,col=NA), 
    gpar.rowfill = gpar(fill=NA,col=NA), 
    show.rownames = F,
    h.even.alpha = 0,
    gpar.rowtext = gpar(col="black", cex=0.7,
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
    title_concat <- ldply(lapply(title_split[[1]][1:length(title_split[[1]])],paste, sep="", collapse = " "))
    title_concat_short <- ldply(lapply(title_concat,gsub, pattern="alldata\\s+|region\\s+",replacement=""))
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
    containTest <- '2035' %in% names(df.t)
    extra=F
    ##check if 
    if (T %in% containTest){
      g1 <- makeTable(df.t[c("Indicator","2010","2018","2025","2035","2040")])
      extra=T
    } else {
      g1 <- makeTable(df.t[c(1,2,ncol(df.t))])
    }
    ############################################################################
    ##process EMFAC MTC data
    travelYears <- c('2018','2025','2035')
    mtcDataFiles <- ldply(lapply(travelYears,function(x) sprintf("%s/EMFAC2011-SG Summary - Year_%s - Group 1.csv",file.path(pth, fsep = .Platform$file.sep),x)))                      
    mtcData<-lapply(mtcDataFiles[[1]],read.csv,header = TRUE, sep = ",", quote="\"")
    TOG <- data.frame(mtcData[[1]][,4], mtcData[[1]][,11],mtcData[[2]][,11],mtcData[[3]][,11])
    names(TOG) <- c("geography",2018,2025,2035)
    #TOG$geography <- c("region",as.vector(substr(x=TOG$geography[2:10],start=1,last=length(TOG$geography[2:10])-5)))
    TOG.m <- melt(TOG[2:10,],id="geography")
    
    g2 <- makeTable(TOG[2:10,])
    ############################################################################
    ## start pdf object to store all charts
    fp <- file.path(pth, fsep = .Platform$file.sep)
    fileNameOut=sprintf("%s_topsheet.pdf","region",id)
    sprintf("Preparing file %s for charts and figures...", fileNameOut)
    ##plot it
    pdf(fileNameOut,height=8.5, width=11,onefile=TRUE)
    print(fileNameOut)
    #multiplot(tb1, tb1, cols=1)
    set.seed(2)
    #q1 <- ggplot(data.frame(x=rnorm(50)), aes(x)) + geom_density()
    #q2 <- ggplot(data.frame(x=rnorm(50)), aes(x)) + geom_density()
    
    g6 <- linePlot(TOG.m,"Total Organic Gases")
    g6 <- direct.label(g6, list(last.points, cex=.6, hjust = 0.7, vjust = 1,fontsize=12))
    
    g7 <- stackedBarPlot(TOG.m,"Vehicle Miles Traveled")
    
#     tb1 <- grid.arrange(g1,g2,g6,g7, nrow=2, 
#                         widths = c(1/2,1/2),
#                         heights = c(1/3,2/3), 
#                         main=textGrob(paste("\n","Topsheet Example"),
#                                       gp=gpar(fontsize=11,fontface="bold")))
#     #grid.text("test",x=unit(0.85,"npc"),y=unit(0.95,"npc"),gp=gpar(fontsize=7,fontface="italic")) 
#    sub=textGrob("test sub", gp=gpar(font=2))

    #multiplot(q1, q2, q3, q4, q5, q6, cols=3)
#      vp.setup(2,2)
#      print(g1, vp=vp.layout(1, 1:2))
#      print(g2, vp=vp.layout(2,2))
#      print(g6, vp=vp.layout(2,1))
#   
    note <- "
    This 'No Project' run with id number xxx represents the baseline scenario and is in a draft state until further notice.
    "
    g3 <- splitTextGrob(note,gp=gpar(fontsize=10, col="grey",just = "left"))
    grid.newpage() 
    #grid.text("Title 1", vp = viewport(layout.pos.row = 1, layout.pos.col = 1:2))
    
    vp <- viewport(layout = grid.layout(nrow=4, ncol=2, 
                                        heights = unit(c(0.25, 3.5, 0.25, 3.5),"inches"), 
                                        widths = unit(c(4.5,4.5), "inches")))
    pushViewport(vp)
    #grid.rect(gp=gpar(col="blue")) #,fill="blue"))
    grid.rect(gp=gpar(col="grey"))#,fill="black"))
    #grid.border(1, vp=viewport)
    #upViewport()
    #pushViewport(viewport(layout=grid.layout(nrow=2, ncol=2, widths=unit(c(5,4), "inches"),heights=unit(c(3.5,3.5), "inches"))))
    grid.text("Table 1\nKey UrbanSim Indicators", vp = viewport(layout.pos.row = 1, layout.pos.col = 2))
    grid.text("Table 2\nEMFAC Total Organic Gases", vp = viewport(layout.pos.row = 3, layout.pos.col = 1))
    grid.text("Configuration Details", vp = viewport(layout.pos.row = 1, layout.pos.col = 1))
    grid.text("Figure 1", vp = viewport(layout.pos.row = 3, layout.pos.col = 2))
    
    pushViewport(viewport(layout.pos.col=2, layout.pos.row=4)) 
    print(g6, newpage=FALSE) 
    popViewport()
    #par(mar = c(2, 2,2, 2))
    
    pushViewport(viewport(layout.pos.col=1, layout.pos.row=2)) 
    #print(g7, newpage=FALSE) 
    #grid.text(note, gp=gpar(fontsize=20, col="grey"))
    grid.draw(g3)
    popViewport(1)
    
    pushViewport(viewport(layout.pos.col=1, layout.pos.row=4, clip="off"))
    grid.draw(g2)
    popViewport()
    
    pushViewport(viewport(layout.pos.col=2, layout.pos.row=2, clip="off"))
    grid.draw(g1)
    popViewport()
    
    dev.off()
    }   

#yrStart<-2010
#yrEnd<-2018
#pth <- "/home/aksel/Documents/Data/Urbansim/run_134/indicators"
#mtcData <- "/var/www/MTC_Model/No_Project/run_139"
regionalProcessor(pth,yrStart,yrEnd)
#garbage <- dev.off()