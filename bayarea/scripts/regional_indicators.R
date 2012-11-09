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
#args <- c('/home/aksel/workspace/opus/data/bay_area_parcel/runs/run_257.2012_10_03_00_45/indicators','2010','2040','257',"FALSE","No_Project")
pth <-args[1]
yrStart <- as.integer(args[2])
yrEnd <- as.integer(args[3])
run_id <- args[4]
travelModelRan <- args[5]
scenario <- args[6]

travelYears <- c(2018,2025,2035)
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
           ylab("Tons GHG per Weekday") +
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
##function for making tablegrob objects
makeTable <- function(data){    
  tableGrob(
    format(data, digits = 1,#nsmall=sample(c(1,0),11,replace=T),
           scientific=F,big.mark = ","),
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

dt.pda<-c(.78,.60,.34,.33,.92,.78,.84,.56,.65,.70,.57,.23,.18,.85,.60,.71,.33,.47)
lCounties <-c('Alameda','Contra Costa','Marin','Napa','San Francisco','San Mateo','Santa Clara','Solano','Sonoma')
targetPDAData <- structure(dt.pda, 
                        dim = c(9,2),
                        .Dimnames = list(lCounties,c('hh','jobs')))

##main processor function
regionalProcessor <- function(pth,yrStart,yrEnd){
    setwd(pth)
    ptrn <-sprintf("^%s%s_%s-%s%s","alldata_table-",3,yrStart,yrEnd,".+")
    fileList = list.files(path=pth, pattern=ptrn)
    if (length(fileList) == 0)
    {
    stop(sprintf("Failed to find any regional indicators for years %s to %s in %s", yrStart, yrEnd, pth))
    }
  
  ##  create list with data tables
    dat<-lapply(fileList,read.csv,header=T,sep = "\t")
  
  ## flatten list to to get vector with nice variable names
    fileAndTypesLst<- lapply(fileList,function(x) strsplit(x,"\\."))
    fileAndTypesFlattened = lapply(fileAndTypesLst, ldply)
    fileNameClean <- ldply(fileAndTypesFlattened)[,1]
    fileNameClean <- ldply(lapply(fileNameClean, gsub, pattern="alldata.+\\d{4}-\\d{4}_",replacement=""))
    title_split <- lapply(fileNameClean,strsplit, "_")
    title_concat <- ldply(lapply(title_split[[1]][1:length(title_split[[1]])],paste, sep="", collapse = " "))
    title_concat_short <- ldply(lapply(title_concat,gsub, pattern="alldata\\s+|region\\s+",replacement=""))
    #title_proper <- lapply(title_concat,TitleCase)
    #title <- paste(title_concat[[1]], sep=" ", collapse = " ")
    names(dat) <- ldply(title_concat_short)[2:ncol(title_concat_short),2]
  
  ## transform appropriately for ease of use/ggplot
    df.m<-melt(dat, id="alldata_id.i8")
    ptrn <- "([0-9]{4})" #"^[^[:digit:]]*"  
    df.m[,2] <-as.integer(str_extract(df.m[,2],ptrn)) 
    df.m <- df.m[,c(2:4)]
    df.t <- as.data.frame(cast(df.m))
    names(df.t)[1] <- "Indicator"
    df.t$index<-((df.t[,ncol(df.t)]/df.t[,2])*100)
    
    ########get separate dataframe for comparison with targets###############
    #comparisonVars <- c("jobs in pda","hh in pda","households","employment")
    #df.t.pda<- df.t[df.t[,1] %in% comparisonVars,]
    
    #########################################################################
    ##get county-level population data
    countyPopFile <- sprintf('county_table-3_%s-%s_county__county_population.tab',yrStart,yrEnd)
    countyPopPth <- file.path(pth,countyPopFile,fsep = .Platform$file.sep)
    lCounties <- c('Alameda','Contra Costa','Marin','Napa','San Francisco','San Mateo','Santa Clara','Solano','Sonoma','ALL')
    countyPopRaw <- read.csv(countyPopPth,sep="\t")
    countyPop <- countyPopRaw[countyPopRaw[,1] %in% c(49,48,43,41,38,28,21,7,1),  ]
    #ptrn <- "([[:digit:]]{4})"  
    names(countyPop) <- c("county",str_extract(names(countyPop)[2:ncol(countyPop)],ptrn))
    countyPop <- rbind(countyPop,c("ALL",colSums(countyPop[,2:ncol(countyPop)])))
    countyPop[,1] <-factor(countyPop[,1], labels=lCounties)
    
    
  ## grob time    
    #containTest <- '2035' %in% names(df.t)
    popYearsKeepers <- travelYears<=yrEnd
    
    if(yrEnd==2040){
    #extra=F
    ##check if out years are included 
      g1 <- makeTable(df.t[c("Indicator","2010","2018","2025","2035","2040","index")])
      g8 <- makeTable(df.t[c("Indicator","2010","2018","2025","2035","2040","index")])
      popData <- data.frame(countyPop[,c("county","2018","2025","2035")])
      names(popData) <- c("county",2018,2025,2035)
      extra=T
    } else {
      popData <- data.frame(countyPop[,c("county",yrStart,travelYears[popYearsKeepers])])
      names(popData) <- c("county",yrStart,travelYears[popYearsKeepers])
      g1 <- makeTable(df.t[c(1,2,ncol(df.t))])
    }
    ############################################################################
    ##process EMFAC MTC data
    if(travelModelRan==T){
      mtcDataFiles <- ldply(lapply(travelYears,
                                   function(x) sprintf("%s/EMFAC2011-SG Summary - Year_%s - Group 1.csv",
                                                       file.path(pth, fsep = .Platform$file.sep),x)))                      
      mtcData<-lapply(mtcDataFiles[[1]],read.csv,header = TRUE, sep = ",", quote="\"")
      GHGFields <- c('Total.TOG','Total.ROG','Total.CO','Total.NOx','Total.CO2')
      GHG2018 <- rowSums(as.matrix(mtcData[[1]][,GHGFields]))
      GHG2025 <- rowSums(as.matrix(mtcData[[2]][,GHGFields]))
      GHG2035 <- rowSums(as.matrix(mtcData[[3]][,GHGFields]))
      GHG <- data.frame(mtcData[[1]][,4], GHG2018,GHG2025,GHG2035)
      names(GHG) <- c("geography",2018,2025,2035)
      GHG[,1] <- gsub(pattern=" (SF)", x=GHG[,1],replacement="",fixed = T)
      GHG.merge <- merge(GHG,popData, by.y="county", by.x="geography")
      
      ##add ghg per cap for each urbansim year that is also in travel model run years
      yrKeep <- travelYears[popYearsKeepers]
      for(i in yrKeep){
        GHG$newVar <- GHG.merge[,sprintf("%s.x",i)] / 
          as.integer(GHG.merge[,sprintf("%s.y",i)])
        names(GHG)[ncol(GHG)] <- sprintf("GHGPerCap%s", i)
      }
      GHG.m <- melt(GHG[2:10, 1:ncol(GHG)-length(yrKeep)],id="geography")
      g2 <- makeTable(GHG)
      g6 <- linePlot(GHG.m,"Total Greenhouse Gases")
      g6 <- direct.label(g6, list(last.points, cex=.6, hjust = 0.7, vjust = 1,fontsize=12))
      g7 <- stackedBarPlot(GHG.m,"Vehicle Miles Traveled")
      }
    ############################################################################
    ## start pdf object to store all charts
    fp <- file.path(pth, fsep = .Platform$file.sep)
    fileNameOut=sprintf("region_run_%s_topsheet.pdf",run_id)
    sprintf("Preparing file %s for charts and figures...", fileNameOut)
    ##plot it
    pdf(fileNameOut,height=8.5, width=11,onefile=TRUE)
    print(fileNameOut)
    #set.seed(2)
    #q1 <- ggplot(data.frame(x=rnorm(50)), aes(x)) + geom_density()
    #q2 <- ggplot(data.frame(x=rnorm(50)), aes(x)) + geom_density()
    
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
    note <- sprintf("\nThis '%s' run with id number %s represents the baseline scenario and is in a draft state until further notice.",scenario, run_id)
        g3 <- splitTextGrob(note,gp=gpar(fontsize=10, col="grey",just = "left"))
    grid.newpage() 
    #grid.text("Title 1", vp = viewport(layout.pos.row = 1, layout.pos.col = 1:2))
    
    vp <- viewport(layout = grid.layout(nrow=4, ncol=2, 
                                        heights = unit(c(0.25, 3.5, 0.25, 3.5),"inches"), 
                                        widths = unit(c(4.5,4.5), "inches")))
    pushViewport(vp)
    grid.rect(gp=gpar(col="grey"))#,fill="black"))
    #grid.border(1, vp=viewport)
    #upViewport()
    #pushViewport(viewport(layout=grid.layout(nrow=2, ncol=2, widths=unit(c(5,4), "inches"),heights=unit(c(3.5,3.5), "inches"))))
    
    if(travelModelRan==T){
      grid.text("Figure 1", vp = viewport(layout.pos.row = 3, layout.pos.col = 2))
      grid.text("Table 2\nEMFAC Total Greenhouse Gases", vp = viewport(layout.pos.row = 3, layout.pos.col = 1))
      
      ##GHG table
      pushViewport(viewport(layout.pos.col=1, layout.pos.row=4, clip="off"))
      grid.draw(g2)
      popViewport()
    
      ##GHG chart
      pushViewport(viewport(layout.pos.col=2, layout.pos.row=4)) 
      print(g6, newpage=FALSE) 
      popViewport()
      #par(mar = c(2, 2,2, 2))
    } else {
      noteTM <- "Travel model was not run for this simulation. This panel left blank intentionally."
      gt <- splitTextGrob(noteTM,gp=gpar(fontsize=14, col="grey",fontface="italic", just = "center"))
      pushViewport(viewport(layout.pos.col=1:2, layout.pos.row=4)) 
      grid.draw(gt)
      popViewport(1)
    }
    
    grid.text("Configuration Details", vp = viewport(layout.pos.row = 1, layout.pos.col = 1))
    grid.text("Table 1\nKey UrbanSim Indicators", vp = viewport(layout.pos.row = 1, layout.pos.col = 2))
    
    ##Note grob
    pushViewport(viewport(layout.pos.col=1, layout.pos.row=2)) 
    #print(g7, newpage=FALSE) 
    #grid.text(note, gp=gpar(fontsize=20, col="grey"))
    grid.draw(g3)
    popViewport(1)
    
    ##key indicators
    pushViewport(viewport(layout.pos.col=2, layout.pos.row=2, clip="off"))
    grid.draw(g1)
    popViewport()
    
    ###########################################################################
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
    #title_proper <- lapply(title_concat,TitleCase)
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
    
    garbage <- dev.off()
    }   

#yrStart<-2010
#yrEnd<-2018
#pth <- "/home/aksel/Documents/Data/Urbansim/run_134/indicators"
#mtcData <- "/var/www/MTC_Model/No_Project/run_139"
regionalProcessor(pth,yrStart,yrEnd)

#garbage <- dev.off()
