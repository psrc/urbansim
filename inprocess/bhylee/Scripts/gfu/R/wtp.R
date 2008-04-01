############################################################
###   The Likelihood Function                            ###
############################################################

wtp.likelihood <- function(theta,vars0) {
	
	## Unpacking the variables
	
	price <- vars0$price
	X <- vars0$X
	Xfactor <- vars0$Xfactor
	Cat <- vars0$Cat
	N <- vars0$N
	PiC <- vars0$PiC
	noB <- vars0$noB
	n <- vars0$n
	Xwin <- vars0$Xwin
	C <- vars0$C
	noFV <- vars0$noFV
	X.C <- vars0$X.C

	## Re-naming the precision parameter 

	alpha <- theta[1]

	## Setting up the categorical probability numerators

	cat.numerator <- matrix(0,n,C)
	for( i in 1:C){
		cat.numerator[,i] <- PiC[,i]*exp(alpha*(X.C[,,i]%*%theta[-1]))
	}	

	## Calculating the vector or log-likelihoods for each observation
	
	log.like <- rep(0,n)
	log.like <- log(alpha) - alpha*log(price)+alpha*(Xwin%*%theta[-1]) - price^(-alpha) * N*(apply(cat.numerator,1,sum))

	## Returning the log-likelihood for the data

	if( is.finite(sum(log.like))  ) return(sum(log.like)) else  return(-1e+300)
	
}

##########################################################################################
###       The Gradient Function                                                       ####
##########################################################################################

dldtheta <- function(theta,vars0){

	## Unpacking the variables
	
	price <- vars0$price
	X <- vars0$X
	Xfactor <- vars0$Xfactor
	Cat <- vars0$Cat
	N <- vars0$N
	PiC <- vars0$PiC
	noB <- vars0$noB
	n <- vars0$n
	Xwin <- vars0$Xwin
	C <- vars0$C
	noFV <- vars0$noFV  # Does not include the intercept. 
	X.C <- vars0$X.C

	## Settting up variables

	alpha <- theta[1]
	grad <- rep(0,length(theta))
	temp.score <- rep(0,n)

	## The partial derivative for alpha

	cnn <- matrix(0,n,C)
	for( i in 1:C){
		cnn[,i] <- PiC[,i]*N*(X.C[,,i]%*%theta[-1]-log(price))*exp(alpha*(X.C[,,i]%*%theta[-1]-log(price)))
	}	

	temp.score <- 1/alpha - log(price) + Xwin%*%theta[-1] - apply(cnn,1,sum) 
	grad[1] <- sum(temp.score)	# storing the partial for alpha

	## Calculate the partials for the unfactored variables

#	cno <- matrix(0,n,C)
#	for( i in 1:C){
#		cno[,i] <- PiC[,i]*N*exp(alpha*(X.C[,,i]%*%theta[-1]-log(price)))
#	}	


	if( X == 0) noUnFV <- 0 else noUnFV <- dim(X)[2]

	if( noUnFV != 0 ){
		for( i in 1:noUnFV ){

			cno <- matrix(0,n,C)
			for( k in 1:C){
				cno[,k] <- PiC[,k]*N*alpha*X.C[,i,k]*exp(alpha*(X.C[,,k]%*%theta[-1]-log(price)))
			}	

			temp.score <- alpha*X[,i] - apply(cno,1,sum)
			grad[1+i] <- sum(temp.score)	# storing the partials for the unfactored variables
		}
	}

	## Calculate the partials for the factored variables

	for( i in 1:(noFV+1) ){
		for( j in 1:C){
			if( j == 1){
				cn <- matrix(0,n,C)
				for( k in 1:C){
					cn[,k] <- PiC[,k]*N*alpha*X.C[,(i-1)*C+1,k]*exp(alpha*(X.C[,,k]%*%theta[-1]-log(price)))
				}

				temp.score <- alpha*Xfactor[,((i-1)*C+1)] - apply(cn,1,sum)	
				
			}else{
				cnf <- matrix(0,n,C)
				for( k in 1:C){
					cnf[,k] <- PiC[,k]*N*(alpha*X.C[,((i-1)*C)+j,k])*exp(alpha*(X.C[,,k]%*%theta[-1]-log(price)))
				}	
				temp.score <- alpha*Xfactor[,((i-1)*C)+j] - apply(cnf,1,sum)
			}

			grad[1 + noUnFV + ((i-1)*C)+j] <- sum(temp.score)	# storing the partials for the factored variables
		}
	}
	return(grad)
}


################################################################
###        The Model Fitting Function                        ###
################################################################


wtp.lm <- function( par,price,formulaUnF,formulaF,Cat,N,PiC,control=list(maxit=10000,fnscale=-1)) {

	ptm <- proc.time()	# Store the starting time

	## Set up the data matrices

	Xfactor <- model.matrix(formulaF)

	if(formulaUnF != 0){
		X <- as.matrix(model.matrix(formulaUnF)[,-1])
		noB <- dim(X)[2] + dim(Xfactor)[2] 
		Xwin <- cbind(X,Xfactor) 
	}else{
		X <- 0
		noB <- dim(Xfactor)[2]
		Xwin <- Xfactor
	}

	## Setting up variables needed later

	n <- length(price) 			# number of observations
	C <- max(Cat)
	noFV <- ((dim(Xfactor)[2])/C)-1  	# number of factored variables

	## Set up the array of matrices for the categorical numerators

	X.C <- array(0,dim = c(n,noB,C))
	for( i in 1:C){
		X.cat <- Xfactor
		X.cat[,2:C] <- 0			

		if( noFV !=0 ){
			X.cat[,(C + noFV + 1):(dim(Xfactor)[2])] <- 0	
		}
		X.cat[,i] <- X.cat[,1]		

		if( noFV != 0 ) {
			if( i != 1 ){
				for(j in 1:noFV){
					X.cat[,C+noFV+j*(i-1)] <- X.cat[,C+j]	
				}
			}
		}

		if( X != 0){
			X.cat <- cbind(X,X.cat) 
		}
		X.C[,,i] <- X.cat
	}
	
	## Package the variables

	vars0= list(	price=price,
			X=X,
			Xfactor=Xfactor,
			Cat=Cat,
			N=N,
			PiC=PiC,
			noB=noB,
			n=n,
			Xwin=Xwin,
			C=C,
			noFV=noFV,
			X.C=X.C )

	## Fit the model by maximum likelihood estimation

	mle <- optim( 	par = par, 
			fn=wtp.likelihood,
			gr=dldtheta,
			method="L-BFGS-B",
			lower=c(.001,rep(-Inf,length(par-1))),
			upper=rep(Inf,length(par)),
			hessian=T,
			control=control,
			vars0 = vars0)


	## Create and format the output 

	coefficients <- matrix(0,nrow=length(par),ncol=4) 
	coefficients[,1] <- mle$par
	if( det(-mle$hessian) == 0 ){
		coefficients[,2] <- rep("NA",length(par))
		coefficients[,3] <- rep("NA",length(par))
		coefficients[,4] <- rep("NA",length(par))
	} 
	else {
		coefficients[,2]<- sqrt(diag(solve(-mle$hessian)))
		coefficients[,3] <- coefficients[,1]/coefficients[,2]
		coefficients[,4] <- 2*pt(abs(coefficients[,3]),n-noB-2,lower.tail=F)	
	}
	
	colnames(coefficients) <- c("estimates","Std Err","t-statistic","p-val")

	rownames(coefficients) <- 1:length(par)
	rownames(coefficients)[1] <- "precision"
	for( i in 2:length(par)) {
		rownames(coefficients)[i] <- colnames(Xwin)[i-1]
	}

	value <- wtp.likelihood(mle$par,vars0)
	base.value <- wtp.likelihood(c(1,rep(0,length(par)-1)),vars0)
	guess.value <- wtp.likelihood(par,vars0)
	time <- proc.time() - ptm
	convergence <- mle$convergence
	message <- mle$message
	function.calls <- mle$counts


	out <- list(	value=value,
			base.value=base.value,
			guess.value=guess.value,
			time=time,
			convergence=convergence,
			message=message,
			function.calls=function.calls,
			mle=mle)

	cat("Coefficients:\n")
    	print.default(format(coefficients, digits = 3),quote = FALSE)
	
	out 

}

