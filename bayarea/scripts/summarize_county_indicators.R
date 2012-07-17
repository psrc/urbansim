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
#options(error=utils::recover)
require("stringr")
require("ggplot2")
require("reshape")
require("gridExtra")
require("RGraphics") 

#declare index function
indx <- function(dat, baseRow = 1)
{
  require(plyr)   
  divisors <- dat[baseRow ,]
  adply(dat, 1, function(x) x / divisors*100)
}

#wrap cmd-line arguments to assign to proper names
cmdArgs <- function(a="/home/aksel/Documents/Data/Urbansim/run_139.2012_05_15_21_23/indicators/2010_2035",b=2010,c=2035) 
{
  pth <<- a
  yrStart <<- as.integer(b)
  yrEnd <<- as.integer(c)
}

cmdArgs(a=args[1],b=args[2],c=args[3])
setwd(pth)

#for formating chart titles
TitleCase <- function(string="test string")
{
  first <- toupper(substring(string, 1, 1))
  rest <- tolower(substring(string, 2))
  fString <- sprintf("%s%s",first,rest)
  return(fString)
}

#parse path to get runid, run date
split <- strsplit(args[1],"/")[[1]]
pos <- length(split)-1  #this assumes we are one up from the indicators dir--a regex would be better.
runid <- split[pos]
periodPosition <- regexpr("\\.",runid)[[1]]
tm <- strsplit(substr(runid,periodPosition+1,nchar(runid)),"_")
id <- strsplit(substr(runid,1,periodPosition-1),"_")[[1]][2]
datetime <-sprintf("%s/%s/%s %s:%s:00",tm[[1]][2],tm[[1]][3],tm[[1]][1],tm[[1]][4],tm[[1]][5]) #get from runid string
runDate <- strptime(datetime, "%m/%d/%Y %H:%M:%S")
                                                                                           
#  select folder with indicator files, fetch all beginning with "county..." having proper years in name
ptrn <-sprintf("^%s%s_%s-%s%s","county_table-","[0-9]",yrStart,yrEnd,".+")
fileList = list.files(path=pth, pattern=ptrn)
if (length(fileList) == 0)
{
  stop(sprintf("Failed to find any county indicators in %s", pth))
}

#  "loop" construct, create dataframe, chart for each tab file
dat<-lapply(fileList,read.csv,header=T,sep = "\t")

#start pdf object to store all charts
fp <- file.path(pth, fsep = .Platform$file.sep)
fileNameOut=sprintf("%s/plot_%s_indexChart.pdf",fp,runid)
sprintf("Preparing file %s for charts and figures...", fileNameOut)
pdf(fileNameOut,height=8.5, width=11,onefile=TRUE)

#store each file in a dataframe, process and plot as we go.
for(i in 1:length(dat)) 
{
  sim_start_end <- as.data.frame(dat[i])  #technically redundant; could just use dat list object
  
  #subset to keep only relevant counties (using the arbitrary objectid in geography_county.id)
  sim_start_end <- sim_start_end[sim_start_end$county_id.i8 %in% c(49,48,43,41,38,28,21,7,1),  ]
  
  #convert id key to factor levels for more meaningful labeling. Labels are assigned based on factor numerical order.
  #cnty <- c('ala','cnc','mar','nap','sfr','smt','scl','sol','son')
  cnty <-  c('Alameda','Contra Costa','Marin','Napa','San Francisco','San Mateo','Santa Clara','Solano','Sonoma')
  sim_start_end$county_id.i8 <-factor(sim_start_end$county_id.i8, labels=cnty)
  
  #rename col names, retaining only year part, extract column name to use in chart name later. Each column has year embedded
  regexp <- "([[:digit:]]{4})"  
  maxCol <- length(sim_start_end)
  years <-str_extract(names(sim_start_end)[2:maxCol],regexp) 
  pos <- regexpr(pattern = regexp, text = names(sim_start_end)[2:maxCol])  #where does year start in col name?
  yrEnd <-max(as.integer(years))  #overwrites passed years and uses actual outer years in tab files 
  yrStart <- min(as.integer(years))
  
  #extract field name representing variable for use in chart
  title_prelim <- substr(names(sim_start_end)[2],1,pos-2)
  title_split <- strsplit(title_prelim,"_")
  title_proper <- lapply(title_split,TitleCase)
  title <- paste(title_proper[[1]], sep=" ", collapse = " ")
  #fileNameOutChart=sprintf("%s/plot_%s_indexChart_%s.pdf",fp,runid,title)
  #fileNameOutTable=sprintf("%s/plot_%s_indexTable_%s.pdf",fp,runid,title)
  
  yrNames <- c('county',years)
  #assign new colunn names
  names(sim_start_end) <-yrNames
  
  # Transpose frame so cols are county series, rows are years
  sim_start_end.t <- t(sim_start_end[,2:ncol(sim_start_end)])
  
  # Set column headings as counties
  colnames(sim_start_end.t) <- sim_start_end[,1]
  sim_start_end.t <-as.data.frame(sim_start_end.t)
  
  #add regional total
  sim_start_end.t$Region <- rowSums(sim_start_end.t,na.rm = FALSE, dims = 1)
  sim_start_end.t$year <- as.integer(rownames(sim_start_end.t))
  sim_start_end_long_abs <- melt(sim_start_end.t,id="year",variable_name = "county")
  
  # call index function to convert absolutes to indices (2010= index 100), replace NAs
  sim_start_end.i <-indx(sim_start_end.t, 1)
  sim_start_end.i <- replace(sim_start_end.i, is.na(sim_start_end.i), 0) 
  
  #add two digit years for easier plotting
  rownames(sim_start_end.i) <- yrNames[2:maxCol]
  #attach(sim_start_end.i)
  
  #   convert to long format for ggplot
  sim_start_end.i$year <- as.integer(rownames(sim_start_end.i))
  sim_start_end_long <- melt(sim_start_end.i,id="year",variable_name = "county")
  
  
  
  #plotting object pdf target
  #ticks <- as.factor(seq(yrStart,yrEnd,1)) 
  
  #table object prep for chart
  end <- yrEnd - yrStart + 1
  if (end > 26 ) {
    step <- 2 
  }
  else {
    step <- 1
  }
  
  g1 <- tableGrob(
            format(
                   sim_start_end.t[seq(1,end,step),c(1:9,11)], 
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

  #plot object
  stamp <- sprintf("Simulation #%s run on %s\nReport generated on %s",id,format(runDate, "%a %b %d %T"),format(Sys.time(), "%a %b %d %T"))
  #first send line chart to pdf...
  
  g3 <- ggplot(data=sim_start_end_long,
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
  
  
  #out <- grid.arrange(g3, ncol=1, main=textGrob(paste("\n",title),gp=gpar(fontsize=14,fontface="bold")))
  grid.newpage()
  pushViewport(viewport(height=unit(0.9, "npc"), width=unit(0.95, "npc"), x=0.5, y=0.5, name="vp")) 
  upViewport() 
  print(g3, vp="vp")
  print(sprintf("Outputting Chart %s to PDF",title))
  grid.text(stamp,x=unit(0.85,"npc"),y=unit(0.95,"npc"),gp=gpar(fontsize=7,fontface="italic"))
  
  #second send area chart to pdf...
  g4 <- ggplot(data=sim_start_end_long_abs,
               aes(x=(year), y=value)) +
                 geom_area(aes(fill=county, group = county), position='stack', alpha=.5) + scale_fill_brewer(palette="Paired")+ # scale_fill_hue(l=40) #scale_fill_brewer() +
                 opts(title=title)+
                 xlab("Year") + 
                 #ylab(paste("Count")) + 
                 opts(axis.text.x=theme_text(angle=90, hjust=0)) + #guides(colour = guide_legend(override.aes = list(alpha = 1))) +
                 #opts(panel.border  = theme_rect(colour = 'black')) + 
                 #opts(panel.grid.major = theme_line(colour = 'grey', size = .25, linetype = 'solid')) +
                 #opts(panel.grid.minor = theme_line(colour = 'grey', size = .1, linetype = 'dashed')) +
                 guides(fill = guide_legend(reverse = TRUE)) 
                 #scale_y_continuous(labels="comma")
                 
  
  grid.newpage()
  pushViewport(viewport(height=unit(0.9, "npc"), width=unit(0.95, "npc"), x=0.5, y=0.5, name="vp")) 
  upViewport() 
  print(g4, vp="vp")
  print(sprintf("Outputting Area Chart %s to PDF",title))
  grid.text(stamp,x=unit(0.85,"npc"),y=unit(0.95,"npc"),gp=gpar(fontsize=7,fontface="italic"))
  
  #third, send table to pdf  
  out <- grid.arrange(g1, ncol=1, main=textGrob(paste("\n",title),gp=gpar(fontsize=14,fontface="bold"))) #,sub=stamp)
  print(sprintf("Outputting Table %s to PDF",title))
  grid.text(stamp,x=unit(0.85,"npc"),y=unit(0.95,"npc"),gp=gpar(fontsize=7,fontface="italic")) 
  print(out)
  #dev.off()  
  
}

garbage <- dev.off()
sprintf("File is ready: %s", fileNameOut)
#warnings()

##county ids used in data
#1  Alameda  ala
#7  Contra Costa  cnc
#21	Marin	mar
#28	Napa	nap
#38	San Francisco	sfr
#41	San Mateo	smt
#43	Santa Clara	scl
#48	Solano	sol
#49	Sonoma	son
###