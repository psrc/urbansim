library(foreign)
library(Zelig)
template<-read.table("C://Documents and Settings/bhylee/Desktop/template/bldg_parcel_114287.txt",header=TRUE,sep="|")
attach(template)
summary(template)

par(mfrow=c(2,2))
truehist(parcel_acre, nbins=3000)
truehist(parcel_acre, nbins=3000, xlim=c(0,5))
truehist(parcel_acre, nbins=3000, xlim=c(0,1))
truehist(parcel_acre, nbins=3000, xlim=c(0,.5))
dev.off()

detach(template)

plat<-read.table("C://Documents and Settings/bhylee/Desktop/template/plat_3635.txt",header=TRUE,sep=",")
attach(plat)
summary(plat)

plot(SumParcel_acre, UnitsPerAcre, type="p", xlim=c(0,100), ylim=c(0,15), pch=19, cex=.1, col="blue", panel.first=grid(8,8))
dev.off()

plot(SumParcel_acre, AvgBldgSF, type="p", xlim=c(0,100), ylim=c(1000,5000), pch=19, cex=.1, col="blue", panel.first=grid(8,8))
dev.off()

plot(SumParcel_acre, AvgBedrooms, type="p", xlim=c(0,100), ylim=c(0,6), pch=19, cex=.1, col="blue", panel.first=grid(8,8))
dev.off() 

x<-cbind(SumParcel_acre,UnitsPerAcre)
cl<-kmeans(x,2,nstart=25)
plot(x,col=cl$cluster,pch=19, cex=.1,panel.first=grid(8,8),main=paste(length(cl$withinss),"Clusters of sizes",list(cl$size)))
cl$size
cl$centers
cl$withinss #Within cluster sum of squares by cluster


*********************************************
*					    *
*     SINGLE-FAMILY RESIDENTIAL -- PLATS    *
*     ==================================    *
*					    *
*          Including within cluster         *
*      & Percent of Variance Explained      *
*        WITH VARIABLE NORMALIZATION!       *
*					    *
*********************************************

plat<-read.table("C://Documents and Settings/bhylee/Desktop/template/sfr_plat_3635.txt",header=TRUE,sep=",")

plat$LogUnitsPerAcre<-log(plat$UnitsPerAcre)
plat$LogUnitsPerAcre_norm_mean<-plat$LogUnitsPerAcre/mean(plat$LogUnitsPerAcre)
plat$FAR<-plat$PlatUnits*plat$AvgBldgSF/plat$SumParcel_sf
plat$LogFAR<-log(plat$FAR)
plat$LandValPerSF<-plat$PlatUnits*plat$AvgLandVal/plat$SumParcel_sf
plat$LogLandValPerSF<-log(plat$LandValPerSF)

attach(plat)

nclust<-20
x<-data.frame(cbind(UnitsPerAcre,SumParcel_acre,AvgBldgSF,AvgImprVal))
xnorm<-cbind(LogUnitsPerAcre_norm_mean)

tvar<-sum(var(xnorm))
wvar<-rep(0,nclust)
pvar<-rep(0,nclust)

for(i in 13:nclust){
	print("Number of Clusters:",quote=FALSE)
	print(i)
	
	cl<-kmeans(xnorm,i,iter.max=100,nstart=50) #kmeans cluster analysis on xnorm
	size<-(cl$size)
	centers_norm<-(cl$centers)
	centers<-exp((cl$centers)*mean(plat$LogUnitsPerAcre))
	centers_inverse<-1/centers
	cc<-cbind(centers_norm,centers,centers_inverse,size)

	print("Cluster Log Normal Centers, Centers, Centers Inversed & Size:",quote=FALSE)
	print(cc)
	
	xt<-cbind(x,cl$cluster) #binds cl$cluster to dataframe x
	j<-ncol(xt) #number of columns in xt
	
	for(k in 1:(j-1)){ #for the kth column variable in x
		variable_summary<-summary(xt[,k]) #summary for the kth column variable
		
		for(m in 1:i){ #for the mth cluster
			cluster_summary<-summary(xt[xt[,j]==m,k]) #summary for kth column, mth cluster
			variable_summary<-rbind(variable_summary,cluster_summary)
		}
		
		print(names(x)[k])
		print(variable_summary)
	}
	
	cl$withinss #Within cluster sum of squares by cluster
	wvar[i]<-sum(cl$withinss)/(nrow(x)-1) #Within cluster variance
	print("Within Cluster Variance:",quote=FALSE)
	print(wvar[i])
	pvar[i]<-100-wvar[i]/tvar*100 #Percent of variance explained = ratio of within cluster to Percent of Variance Explained
	print("Percent of Variance Explained:",quote=FALSE)
	print(pvar[i])
}

#plat$SumParcel_acre_norm_mean<-plat$SumParcel_acre/mean(plat$SumParcel_acre)
#plat$UnitsPerAcre_norm_mean<-plat$UnitsPerAcre/mean(plat$UnitsPerAcre)
#plat$AvgBldgSF_norm_mean<-plat$AvgBldgSF/mean(plat$AvgBldgSF)
#plat$AvgImprVal_norm_mean<-plat$AvgImprVal/mean(plat$AvgImprVal)


*********************************************
*					    *
*    SINGLE-FAMILY RESIDENTIAL -- PARCELS   *
*    ====================================   *
*					    *
*          Including within cluster         *
*      & Percent of Variance Explained      *
*        WITH VARIABLE NORMALIZATION!       *
*					    *
*********************************************

parcel<-read.table("C://Documents and Settings/bhylee/Desktop/template/sfr_parcel_104255.txt",header=TRUE,sep=",")

parcel$LogParcel_acre<-log(parcel$Parcel_acre)
parcel$LogParcel_acre_norm_mean<-parcel$LogParcel_acre/mean(parcel$LogParcel_acre)

attach(parcel)

nclust<-25
x<-data.frame(cbind(Parcel_acre,BldgSF,ImprValueParcel))
xnorm<-cbind(LogParcel_acre_norm_mean)

tvar<-sum(var(xnorm))
wvar<-rep(0,nclust)
pvar<-rep(0,nclust)

for(i in 21:nclust){
	print("Number of Clusters:",quote=FALSE)
	print(i)
	
	cl<-kmeans(xnorm,i,iter.max=100,nstart=50) #kmeans cluster analysis
	size<-(cl$size)
	centers_norm<-(cl$centers)
	centers<-exp((cl$centers)*mean(parcel$LogParcel_acre))
	cc<-cbind(centers_norm,centers,size)

	print("Cluster Log Normal Centers, Centers & Size:",quote=FALSE)
	print(cc)
	
	xt<-cbind(x,cl$cluster) #binds cl$cluster to dataframe x
	j<-ncol(xt) #number of columns in xt
	
	for(k in 1:(j-1)){ #for the kth column variable in x
		variable_summary<-summary(xt[,k]) #summary for the kth column variable
		
		for(m in 1:i){ #for the mth cluster
			cluster_summary<-summary(xt[xt[,j]==m,k]) #summary for kth column, mth cluster
			variable_summary<-rbind(variable_summary,cluster_summary)
		}
		
		print(names(x)[k])
		print(variable_summary)
	}
		
	cl$withinss #Within cluster sum of squares by cluster
	wvar[i]<-sum(cl$withinss)/(nrow(x)-1) #Within cluster variance
	print("Within Cluster Variance:",quote=FALSE)
	print(wvar[i])
	pvar[i]<-100-wvar[i]/tvar*100 #Percent of variance explained = ratio of within cluster to Percent of Variance Explained
	print("Percent of Variance Explained:",quote=FALSE)
	print(pvar[i])
}

#parcel$Parcel_acre_norm_mean<-parcel$Parcel_acre/mean(parcel$Parcel_acre)
#parcel$BldgSF_norm_mean<-parcel$BldgSF/mean(parcel$BldgSF)
#parcel$ImprValueParcel_norm_mean<-parcel$ImprValueParcel/mean(parcel$ImprValueParcel)


*********************************************
*					    *
*     MULTI-FAMILY RESIDENTIAL -- CONDOS    *
*     ==================================    *
*					    *
*          Including within cluster         *
*      & Percent of Variance Explained      *
*        WITH VARIABLE NORMALIZATION!       *
*					    *
*********************************************

condo<-read.table("C://Documents and Settings/bhylee/Desktop/template/mfr_condo_1320.txt",header=TRUE,sep=",")

condo$LogUnitsPerAcre<-log(condo$UnitsPerAcre)
condo$LogUnitsPerAcre_norm_mean<-condo$LogUnitsPerAcre/mean(condo$LogUnitsPerAcre)

attach(condo)

nclust<-20
x<-data.frame(cbind(UnitsPerAcre,Parcel_Acres,AvgUnitSF,ImprValPerUnit))
xnorm<-cbind(LogUnitsPerAcre_norm_mean)

tvar<-sum(var(xnorm))
wvar<-rep(0,nclust)
pvar<-rep(0,nclust)

for(i in 11:nclust){
	print("Number of Clusters:",quote=FALSE)
	print(i)
	
	cl<-kmeans(xnorm,i,iter.max=100,nstart=50) #kmeans cluster analysis on xnorm
	size<-(cl$size)
	centers_norm<-(cl$centers)
	centers<-exp((cl$centers)*mean(condo$LogUnitsPerAcre))
	cc<-cbind(centers_norm,centers,size)
	
	print("Cluster Log Normal Centers, Centers & Size:",quote=FALSE)
	print(cc)
		
	xt<-cbind(x,cl$cluster) #binds cl$cluster to dataframe x
	j<-ncol(xt) #number of columns in xt
	
	for(k in 1:(j-1)){ #for the kth column variable in xt
		variable_summary<-summary(xt[,k]) #summary for the kth column variable
				
		for(m in 1:i){ #for the mth cluster
					cluster_summary<-summary(xt[xt[,j]==m,k]) #summary for kth column, mth cluster
			variable_summary<-rbind(variable_summary,cluster_summary)
		}

		print(names(x)[k])
		print(variable_summary)
	}
		
	cl$withinss #Within cluster sum of squares by cluster
	wvar[i]<-sum(cl$withinss)/(nrow(x)-1) #Within cluster variance
	print("Within Cluster Variance:",quote=FALSE)
	print(wvar[i])
	pvar[i]<-100-wvar[i]/tvar*100 #Percent of variance explained = ratio of within cluster to Percent of Variance Explained
	print("Percent of Variance Explained:",quote=FALSE)
	print(pvar[i])
}

#condo$Parcel_Acres_norm_mean<-condo$Parcel_Acres/mean(condo$Parcel_Acres)
#condo$UnitsPerAcre_norm_mean<-condo$UnitsPerAcre/mean(condo$UnitsPerAcre)
#condo$AvgUnitSF_norm_mean<-condo$AvgUnitSF/mean(condo$AvgUnitSF)
#condo$ImprValueParcel_norm_mean<-condo$ImprValueParcel/mean(condo$ImprValueParcel)


*********************************************
*					    *
*  MULTI-FAMILY RESIDENTIAL -- APARTMENTS   *
*  =====================================    *
*					    *
*          Including within cluster         *
*      & Percent of Variance Explained      *
*        WITH VARIABLE NORMALIZATION!       *
*					    *
*********************************************

apt<-read.table("C://Documents and Settings/bhylee/Desktop/template/mfr_apt_2710.txt",header=TRUE,sep=",")

apt$LogUnitsPerAcre<-log(apt$UnitsPerAcre)
apt$LogUnitsPerAcre_norm_mean<-apt$LogUnitsPerAcre/mean(apt$LogUnitsPerAcre)

attach(apt)

nclust<-20
x<-data.frame(cbind(UnitsPerAcre,Parcel_Acres,AvgUnitSF,ImprValPerUnit))
xnorm<-cbind(LogUnitsPerAcre_norm_mean) #,ImprValueParcel_norm_mean

tvar<-sum(var(xnorm))
wvar<-rep(0,nclust)
pvar<-rep(0,nclust)

for(i in 16:nclust){
	print("Number of Clusters:",quote=FALSE)
	print(i)
	
	cl<-kmeans(xnorm,i,iter.max=100,nstart=50) #kmeans cluster analysis on xnorm
	size<-(cl$size)
	centers_norm<-(cl$centers)
	centers<-exp((cl$centers)*mean(apt$LogUnitsPerAcre))
	
	cc<-cbind(centers_norm,centers,size)
	
	print("Cluster Log Normal Centers, Centers & Size:",quote=FALSE)
	print(cc)
		
	xt<-cbind(x,cl$cluster) #binds cl$cluster to dataframe x
	j<-ncol(xt) #number of columns in xt
	
	for(k in 1:(j-1)){ #for the kth column variable in xt
		variable_summary<-summary(xt[,k]) #summary for the kth column variable
				
		for(m in 1:i){ #for the mth cluster
					cluster_summary<-summary(xt[xt[,j]==m,k]) #summary for kth column, mth cluster
			variable_summary<-rbind(variable_summary,cluster_summary)
		}

		print(names(x)[k])
		print(variable_summary)
	}
		
	cl$withinss #Within cluster sum of squares by cluster
	wvar[i]<-sum(cl$withinss)/(nrow(x)-1) #Within cluster variance
	print("Within Cluster Variance:",quote=FALSE)
	print(wvar[i])
	pvar[i]<-100-wvar[i]/tvar*100 #Percent of variance explained = ratio of within cluster to Percent of Variance Explained
	print("Percent of Variance Explained:",quote=FALSE)
	print(pvar[i])
}


#apt$Parcel_Acres_norm_mean<-apt$Parcel_Acres/mean(apt$Parcel_Acres)
#apt$UnitsPerAcre_norm_mean<-apt$UnitsPerAcre/mean(apt$UnitsPerAcre)
#apt$AvgUnitSF_norm_mean<-apt$AvgUnitSF/mean(apt$AvgUnitSF)
#apt$ImprValueParcel_norm_mean<-apt$ImprValueParcel/mean(apt$ImprValueParcel)


truehist(xt[xt[,4]==3,1],nbins=100)

plot(pvar,type="b",xlim=c(2,10),ylim=c(0,100),main="SFR - Plats",xlab="Number of Clusters",ylab="Percent of Variance Explained",col="dark red")


fit1<-zelig(FAR~LandValPerSF,model="ls",data=plat)