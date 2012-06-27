#script goes to folder with indicator-output county-level files (must be in one file per variable)
#In steps, this is the sequence:
#1) Gets all tab files starting with county in folder
#2) Loops through data files
#3) --keeps only 9 relevant counties
#4) --transforms dataframe so years are rows, counties columns
#5) --plots chart, writes to pdf file

#USAGE: Rscript county_indicator_plots_index_ggplotfinal_arg.R "/home/aksel/Documents/Data/Urbansim/run_139.2012_05_15_21_23/indicators/2010_2035" 2010 2035
#TODO: clean so that select counties can be toggled on/off. Now this is MANUALLY set. 

# Load the ggplot2 library
args <- commandArgs(TRUE)
#options(error=utils::recover)
library(ggplot2)
require("reshape")
library(gridExtra)
library(RGraphics) # support of the "R graphics" book, on CRAN


#viewport function
my.vp <- function(just="topright"){
  
  switch(just,
         "topright" = viewport(x=1,y=1,width=1/2,height=1/2,just=c("right","top")),
         "botleft" = viewport(x=0,y=0,width=1/2,height=1/2,just=c("left","bottom")),
         viewport(x=1,y=1,width=1/2,height=1/2,just=c("right","top")))
  
}

#declare index function for later use
indx <- function(dat, baseRow = 1){
  require(plyr)   
  divisors <- dat[baseRow ,]
  adply(dat, 1, function(x) x / divisors)
}
#runid <- "run_139.2012_05_15_21_23"
split <- strsplit(args[1],"/")[[1]]
pos <- length(split)-2  #this assumes we are two up from the indicators dir--a regex would be better.
runid <- split[pos]

#  select folder with indicator files
pth <- args[1]
yrStart <- as.integer(args[2])
yrEnd <- as.integer(args[3])
setwd(pth)
filist = list.files(path=pth, pattern="^[county]")
#nfiles = length(filist)

#  "loop" construct, create dataframe, chart for each
dat<-lapply(filist,read.csv,header=T,sep = "\t")

for(i in 1:length(dat)) {
  sim_start_end <- as.data.frame(dat[i])
  
  #subset to keep only relevant counties (using the arbitrary objectid in geography_county.id)
  sim_start_end <- sim_start_end[sim_start_end$county_id.i8 %in% c(49,48,43,41,38,28,21,7,1),  ]
  
  #convert id to factor levels
  sim_start_end$county_id.i8 <-factor(sim_start_end$county_id.i8, labels=c('ala','cnc','mar','nap','sfr','smt','scl','sol','son'))
  
  #rename col names, retaining only year part, extract column name to use in chart name later
  library("stringr")
  regexp <- "([[:digit:]]{4})"
  maxCol <- length(sim_start_end)
  years <-str_extract(names(sim_start_end)[2:maxCol],regexp)
  pos <- regexpr(pattern = regexp, text = names(sim_start_end)[2:maxCol])  #where does year start in col name?
  title <- substr(names(sim_start_end)[2],1,pos-2)                   #extract field name for use in chart
  filenameout=sprintf("/home/aksel/plot_run139_index_%s.pdf",title)
  print(filenameout)
  yrNames <- c('county',years)
  names(sim_start_end) <-yrNames                                  #assign new names
  
  # Transpose table so cols are county series, rows are years
  sim_start_end.t <- t(sim_start_end[,2:ncol(sim_start_end)])
  
  # Set column headings as just year portion of variable
  colnames(sim_start_end.t) <- sim_start_end[,1]
  sim_start_end <-as.data.frame(sim_start_end.t)
  names(sim_start_end)
  
  # call index function to convert absolutes to indices (2010= index 100)
  sim_start_end.i <-indx(sim_start_end, 1)
  sim_start_end.i <- replace(sim_start_end.i, is.na(sim_start_end.i), 0)
  attach(sim_start_end.i)
  
  #plotting object
  pdf(filenameout,height=6, width=9)
  
  #   convert to long format for ggplot
  sim_start_end.i$year <- as.integer(rownames(sim_start_end.i))
  sim_start_end_long <- melt(sim_start_end.i,id="year",variable_name = "county")
  
  #ticks <- as.factor(seq(2010,2035,1))
  ticks <- as.factor(seq(yrStart,yrEnd,1))
  #annot <- as.string(format(sim_start_end[1,], big.mark = ","))
  g_range <- range(min(ala,cnc,mar,nap,sfr,smt,scl,sol,son), ala,cnc,mar,nap,sfr,smt,scl,sol,son)
  rangeMean <- tapply(g_range, c(1,1),mean)
  
  #make table object for use as annotation on plot
  tb <- tableGrob(sim_start_end[1,1:9],  show.rownames = TRUE,
                  gpar.corefill = gpar(fill="white"))
  
  #plot function
  library(RGraphics)
  library(gridExtra)
  
  #table object prep for chart
  end <- yrEnd - yrStart + 4
  g1 <- tableGrob(format(sim_start_end[seq(1,end,5),1:9], digits = 2,big.mark = ","), gpar.colfill = gpar(fill=NA,col=NA), gpar.rowfill = gpar(fill=NA,col=NA), h.even.alpha = 0)
  string <- "
  placeholder for possible annotation
  "
  g2 <- splitTextGrob(string)
  #theme_set(theme_bw()); 
  
  #plot object
  g3 <- ggplot(data=sim_start_end_long,
               aes(x=as.factor(year), y=value, group=county,colour=county)) +
                 #geom_line()+
                 #scale_x_discrete(breaks=seq(2010,2035,5), labels=seq(2010,2035,5)) + 
                 geom_line(aes(linetype=county), # Line type depends on county
                           size = .5) +       # Thin line
                             geom_point(aes(shape=county) ,   # Shape depends on county
                                        size = 1)   +       # points
                                          opts(title=paste(title,"\n",runid))+
                                          xlab("Year") + 
                                          ylab(paste("Indexed Value (Rel. to ",yrStart,")"))
  
  #combine in grid, send to print() function
  out <- grid.arrange(g1, g3, ncol=1, main=title)
  print(out)
  dev.off()  
  
}

###
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