#load in functions rmvnorm and rinvwish
source("mvnorm.r")

S.true<-matrix(c(3,-1,-1,2),nrow=2,ncol=2)  # "true" cov matrix
mu.true<-c(5,4)

y<-NULL
n<-50
for(i in 1:n){  y<-rbind(y, t(rmvnorm(mu.true,S.true)) ) }

###ok, lets try to recover the parameters generating the data

#prior params
S0<-matrix(c(4,0,0,4),nrow=2,ncol=2)
iS0<-solve(S0)                
mu0<-c(4.5,4.5)

k0<-4
v0<-5

#if you sample repeatedly from rinvwish(iS0,v0)
# the mean should be S0/(v0-2-1). Lets check:

S.tot<-S0*0
for(i in 1:1000){ S.tot <-S.tot+rinvwish(iS0,v0) }
S.tot/1000  #should be close to 
S0/(v0-2-1) #this

#now lets do the posterior analysis

#posterior params
ybar<-t(y)%*%rep(1/n,n)

Sn<-S0+(n-1)*cov(y)+ k0*n*(ybar-mu0)%*%t(ybar-mu0)/(k0+n)
iSn<-solve(Sn)
mun<-k0*mu0/(k0+n) + n*ybar/(k0+n)

#draw samples
mu.post<-NULL
S.post.mean<-matrix(0,nrow=2,ncol=2)

for(i in 1:1000){

S.tmp<-rinvwish(iSn,v0+n)
mu.post<-rbind(mu.post , t(rmvnorm(mun,S.tmp/(k0+n) ) ) )
S.post.mean<-S.post.mean + S.tmp               
}

mean(mu.post[,1])
mean(mu.post[,2])
S.post.mean/1000

plot(mu.post,xlim=range(c(mu0[1],mu.post[,1]) ), 
             ylim=range(c(mu0[2],mu.post[,2]) ) )
abline(v=mu0[1],col="red" ) ;abline(h=mu0[2],col="red") #prior
abline(v=mean(y[,1]),col="yellow") ; abline(h=mean(y[,2]),col="yellow")
abline(v=mean(mu.post[,1])) ; abline(h=mean(mu.post[,2]))
abline(v=mu.true[1],col="blue" ) ;abline(h=mu.true[2],col="blue") #truth

ybar

mu0



