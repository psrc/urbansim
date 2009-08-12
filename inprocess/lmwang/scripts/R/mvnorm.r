rmvnorm<-function(mu,S){
#generate 1 sample from a mvnorm distribution
#with mean mu and cov matrix Sig2
R<-t(chol(S))
R%*%(rnorm(length(mu),0,1)) +mu }

rinvwish<-function(iS,nu){
#generates a cov matrix from an inverse Wishart distribution
#having nu degrees of freedom and 
#expected value = S/(nu-k-1), k is the dimension
#where S is the inverse of iS

iStmp<-iS*0
for(i in 1:nu){ z<-rmvnorm(rep(0,dim(iS)[1]), iS)
                iStmp<-iStmp+z%*%t(z)  }
solve(iStmp) }



