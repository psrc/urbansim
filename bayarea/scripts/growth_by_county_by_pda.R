library(ggplot2)
library(scales)
#library(RPostgreSQL)
library(plyr)
#require("rgdal")

args <- commandArgs(TRUE)
###############################################################################
#TODO: HAS NO CHECK ON ACCEPTABLE INPUT YEARS YET
###############################################################################
## grab arguments
#args <- c('/home/aksel/workspace/opus/data/bay_area_parcel/runs/run_391','2010','2040','391',"No_Project")
##hard coded path is immaterial--when invoked, overwritten by commandArgs
pth <-args[1]
yrStart <- as.integer(args[2])
yrEnd <- as.integer(args[3])
run_id <- args[4]
#travelModelRan <- args[5]
scenario <- args[5]

##load stuff
#filist<-list.files(path=pth,pattern='area_permutation_table-1_2010_2015_2020_2025_2030_2035_2040.tab')
file<-'area_permutation_table-1_2010_2015_2020_2025_2030_2035_2040.tab'
summary <- file.path(pth,file,fsep = .Platform$file.sep)
abag <- read.csv(summary,header = TRUE, sep="\t")

##discard extraneous identifier columns
abag.s<-abag[,grep("_id",colnames(abag))[seq(-2,-5)]]
to.remove <- colnames(abag)[grep("_id",colnames(abag))[seq(-2,-5)]]
`%ni%` <- Negate(`%in%`)
abag.s<-subset(abag,select = names(abag) %ni% to.remove)

##keep only three key variables, and recode pda to dummy
abag.s.short<-abag.s[, grep('^(total_emp.+|total_hou+|total_pop.+|coun.+|pda_i)', names(abag.s), invert=F)]
abag.s.short$is_pda<-ifelse(abag$pda_id.i8 >0, c("in pda"), c("not in pda"))

##keep relevant counties and convert to factor
abag.s.short <- abag.s.short[abag.s.short[,"county_id.i8"] %in% c(49,48,43,41,38,28,21,7,1),  ]
lCounties <- c('Alameda','Contra Costa','Marin','Napa','San Francisco','San Mateo','Santa Clara','Solano','Sonoma')
abag.s.short[,"county_id.i8"] <-factor(abag.s.short[,"county_id.i8"], labels=lCounties)

##aggregate by county_id, is_pda
#abag.agg<-ddply(abag.s,~abag.s$county_id.i8+abag.s$pda_id.i8,summarise,
# sum=sum(total_households_2010.f8))#,mean=mean(total_households_2010.f8),sd=sd(total_households_2010.f8))
abag.agg<-aggregate(.~county_id.i8+is_pda,data=abag.s.short,FUN=sum)

##melt stuff
abag.agg.m<- melt(abag.agg,id.vars=c("county_id.i8", "is_pda" ))

##fix stuff (separate variable name from year)
num_ptrn <- "([0-9]{4})"  
non_num_ptrn <-"^[^[:digit:]{4}]*"
#txt<-levels(abag.agg.m$variable)
#substr(str_extract(txt,non_num_ptrn),1,length(str_extract(txt,non_num_ptrn)))
#str_extract(txt[3:length(txt)],non_num_ptrn)
#str_extract(txt[3:length(txt)],num_ptrn)
year<-ldply(lapply(abag.agg.m$variable, str_extract, pattern=num_ptrn))
variable<-ldply(lapply(abag.agg.m$variable, str_extract, pattern=non_num_ptrn))

##prep object for plotting
abag.agg.m<-data.frame(abag.agg.m[,c(1,2,4)],year,variable)
names(abag.agg.m)<-c("county_id", "is_pda",  "value","year","variable")

## start pdf object to store all charts
fp <- file.path(pth, fsep = .Platform$file.sep)
fileNameOut=sprintf("%s/run_%splot_pda_summary.pdf",fp,run_id)
sprintf("Preparing file %s for charts and figures...", fileNameOut)
pdf(fileNameOut,height=8.5, width=11,onefile=TRUE)

elements<-c('total_households_','total_population_','total_employment_')
for(elem in elements){
  abag.plot<-abag.agg.m[abag.agg.m$variable==elem,]
  
  #count--this seems to work for now
  gp<-ggplot(abag.plot, aes(x=as.factor(year),y=value)) + geom_bar(stat = "identity",fill="dodgerblue4")+ #colour="black") +
    facet_grid(is_pda~county_id)+
    #facet_grid(.~county_id)+
    scale_y_continuous(labels = comma_format(digits = 5)) +
    labs(title=sprintf("%s for_run_391_%s_%s_to%s",elem,scenario,yrStart,yrEnd))+theme(axis.text.x=element_text(angle = -90, hjust = 0))
  
  print(gp)
  #qplot(variable, data=abag.plot, geom="bar", weight=value,colour="black") +facet_grid(as.factor(year) ~county_id) +
  #  labs('title'='compare stuff')+scale_y_continuous(labels = comma_format(digits = 5)) +theme(axis.text.x=element_text(angle = -90, hjust = 0))  
}
garb<-dev.off()