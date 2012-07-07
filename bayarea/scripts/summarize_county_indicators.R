#script goes to folder with indicator-output county-level files (must be in one file per variable)
#In steps, this is the sequence:
#1) Gets all tab files starting with county in folder
#2) Loops through data files
#3) --keeps only 9 relevant counties
#4) --transforms dataframe so years are rows, counties columns
#5) --plots chart, writes to pdf file

#USAGE: Rscript /home/aksel/Documents/Scripts/r/county_indicator_plots_index_ggplotfinal_arg.R "/home/aksel/Documents/Data/Urbansim/run_139.2012_05_15_21_23/indicators/2010_2035" 2010 2035
#TODO: clean so that select counties can be toggled on/off. Now this is MANUALLY set. 

args <- commandArgs(TRUE)
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
  adply(dat, 1, function(x) x / divisors)
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

#viewport function--not needed right now
#my.vp <- function(just="topright"){
#  
#switch(just,
#         "topright" = viewport(x=1,y=1,width=1/2,height=1/2,just=c("right","top")),
#         "botleft" = viewport(x=0,y=0,width=1/2,height=1/2,just=c("left","bottom")),
#         viewport(x=1,y=1,width=1/2,height=1/2,just=c("right","top")))
#  
#}

#parse path to get runid
split <- strsplit(args[1],"/")[[1]]
pos <- length(split)-2  #this assumes we are two up from the indicators dir--a regex would be better.
runid <- split[pos]

#  select folder with indicator files, fetch all beginning with "county..." having proper years in name
ptrn <-sprintf("^%s%s_%s-%s%s","county_table-","[0-9]",yrStart,yrEnd,".+")
fileList = list.files(path=pth, pattern=ptrn)

#  "loop" construct, create dataframe, chart for each tab file
dat<-lapply(fileList,read.csv,header=T,sep = "\t")

#store each file in a dataframe, process and plot as we go.
for(i in 1:length(dat)) 
{
  sim_start_end <- as.data.frame(dat[i])  #technically redundant; could just use dat list object
  
  #subset to keep only relevant counties (using the arbitrary objectid in geography_county.id)
  sim_start_end <- sim_start_end[sim_start_end$county_id.i8 %in% c(49,48,43,41,38,28,21,7,1),  ]
  
  #convert id key to factor levels for more meaningful labeling. Labels are assigned based on factor numerical order.
  sim_start_end$county_id.i8 <-factor(sim_start_end$county_id.i8, labels=c('ala','cnc','mar','nap','sfr','smt','scl','sol','son'))
  
  #rename col names, retaining only year part, extract column name to use in chart name later. Each column has year embedded
  regexp <- "([[:digit:]]{4})"  
  maxCol <- length(sim_start_end)
  years <-str_extract(names(sim_start_end)[2:maxCol],regexp) 
  pos <- regexpr(pattern = regexp, text = names(sim_start_end)[2:maxCol])  #where does year start in col name?
  yrEnd <-max(as.integer(years))  #overwrites passed years and uses actual outer years in tab files 
  yrStart <- min(as.integer(years))
  
  #extract field name representing variable for use in chart
  title <- substr(names(sim_start_end)[2],1,pos-2)
  fp <- file.path(pth, fsep = .Platform$file.sep)
  fileNameOutChart=sprintf("%s/plot_%s_indexChart_%s.pdf",fp,runid,title)
  fileNameOutTable=sprintf("%s/plot_%s_indexTable_%s.pdf",fp,runid,title)
  
  yrNames <- c('county',years)
  #assign new colunn names
  names(sim_start_end) <-yrNames
  
  # Transpose frame so cols are county series, rows are years
  sim_start_end.t <- t(sim_start_end[,2:ncol(sim_start_end)])
  
  # Set column headings as counties
  colnames(sim_start_end.t) <- sim_start_end[,1]
  sim_start_end.t <-as.data.frame(sim_start_end.t)
  
  #add regional total
  sim_start_end.t$region <- rowSums(sim_start_end.t,na.rm = FALSE, dims = 1)
  
  # call index function to convert absolutes to indices (2010= index 100), replace NAs
  sim_start_end.i <-indx(sim_start_end.t, 1)
  sim_start_end.i <- replace(sim_start_end.i, is.na(sim_start_end.i), 0) 
  
  #add two digit years for easier plotting
  rownames(sim_start_end.i) <- yrNames[2:maxCol]
  attach(sim_start_end.i)
  
  #   convert to long format for ggplot
  sim_start_end.i$year <- as.integer(rownames(sim_start_end.i))
  sim_start_end_long <- melt(sim_start_end.i,id="year",variable_name = "county")
  
  #plotting object pdf target
  pdf(fileNameOutChart,height=8.5, width=11)
  ticks <- as.factor(seq(yrStart,yrEnd,1)) 
  
  #determine range for plot
  #g_range <- range(min(ala,cnc,mar,nap,sfr,smt,scl,sol,son), ala,cnc,mar,nap,sfr,smt,scl,sol,son)
  #rangeMean <- tapply(g_range, c(1,1),mean)
  
  #make table object for use as annotation on plot
  #tb <- tableGrob(sim_start_end[1,1:9],  show.rownames = TRUE,gpar.corefill = gpar(fill="white"))
  
  #table object prep for chart
  end <- yrEnd - yrStart + 1
  g1 <- tableGrob(
            format(
                   sim_start_end.t[seq(1,end,1),1:10], 
                   digits = 2,big.mark = ","), 
                   gpar.colfill = gpar(fill=NA,col=NA), 
                   gpar.rowfill = gpar(fill=NA,col=NA), 
                   h.even.alpha = 0
                   )
  #string <- "
  #placeholder for possible annotation
  #"
  #g2 <- splitTextGrob(string)
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
                                          ylab(paste("Indexed Value (Rel. to ",yrStart,")")) + opts(axis.text.x=theme_text(angle=90, hjust=0))

  
  #combine in grid, send to print() function, chart
  out <- grid.arrange(g3, ncol=1, main=paste("\n",title))
  print(out)
  dev.off()  
  
  #combine in grid, send to print() function, table
  #plotting object pdf target
  pdf(fileNameOutTable,height=8.5, width=11)
  out <- grid.arrange(g1, ncol=1, main=paste("\n",title))
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
