############################################################
###   The Multinomial Logit Likelihood Function          ###
############################################################

mnl.likelihood <- function(coefficients,data) {
	# Returns MNL log-likelihood(coefficients | data)
	# coefficients is a vector of k coefficients
	# data is a data frame with the following:
	#	variables is a N*I by K matrix of observations
	#		for each of the K variables, for each
	#		individual obseration n in N and alternative i in I.
	#	choice is a N*I vector which is 1 if n chose i, 0 otherwise
	#	equations is a I by K matrix of coefficient indicies
	#		one row for each equation, and one column for each variable
	#		0 values mean that variable is omitted for that equation
	#		positive values mean an index to the coefficient vector
	#		negative values mean an -index to the fixed coefficient vector
	#	fixedcoefficients is a vector of k* fixed coefficients
	#	number_of_alternatives is == I the number of alternatives
	#		for each observation n
	#	number_of_observations is == N the number of observations
	
	vars <- data$variables
	cho <- data$choice
	nalt <- data$numberofalternatives
	nobs <- data$numberofobservations
	eqs <- data$equations
	fix <- data$fixedcoefficients

	# Return error if (nrow(vars) != nrow(cho))
	
	
	# Build coefficient matrix
	coeffs <- matrix(nrow=nalt,ncol=ncol(vars))
	for ( i in 1:nalt ) {
		for ( j in 1:ncol(vars) ) {
			if (eqs[i,j]>0) {
				coeffs[i,j] <- coefficients[eqs[i,j]]
			}
			else if (eqs[i,j] == 0) {
				coeffs[i,j] <- 0
			}
			else if (eqs[i,j] < 0) {
				coeffs[i,j] <- fix[-eqs[i,j]]
			}
		}
	}
	
	# Initialize the log-likelihood
	loglik <- rep(0,nobs)
	# Calculating the vector or log-likelihoods for each observation
	for ( n in 1:nobs ) {
		denom <- 0
		numer <- 0
		# Return error if (sum(cho[(n-1)*nalt+1:n*nalt]) != 1)
		for ( i in 1:nalt) {
			denom <- denom + exp(coeffs[i,]%*%vars[(n-1)*nalt+i,])
			if ( cho[(n-1)*nalt+i] > 0 ) {
				numer <- coeffs[i,]%*%vars[(n-1)*nalt+i,]
			}
		}
		denom <- log(denom)
		loglik[n] = numer - denom
	}
	
	# Returning the -log-likelihood for the data
	# since the R optimizers are minimizers
	res <- -sum(loglik)
	if( !is.finite(res)  ) {
		res <- 1e+300
	}
	else {
#		attr(res,"gradient") <- mnl.gradient(coefficients,data)
	}
	return(res)
}

##########################################################################################
###       The Gradient Function                                                       ####
##########################################################################################

#mnl.gradient <- function(coefficients,data){
#
#	return(0)
#}


################################################################
###        The Model Fitting Function                        ###
################################################################


mnl.lm <- function( firstguess,coeffnames,datapack,control=list(maxit=10000,fnscale=1,trace=2,REPORT=1)) {

	ptm <- proc.time()	# Store the starting time

#	datapack <- list( 
#		variables=data[,2:20],
#		choice=data[,1],
#		equations=equations,
#		fixedcoefficients=fixedcoefficients,
#		numberofalternatives=4,
#		numberofobservations=1878
#	)

	# Return error if length(firstguess) != length(coeffnames) != largest number in datapack$equations
	# Return error if length(datapack$fixedcoefficients) != largest negative number in datapack$equations
	# Return error if datapack$numberofalternatives != nrow(datapack$equations)
	# Return error if datapack$numberofobservations*datapack$numberofalternatives 
	#	!= nrow(datapack$variables) != nrow(choice)
	# Return error if ncol(datapack$variables) != ncol(datapack$equations)
	
	n <- datapack$numberofobservations
	K <- length(datapack$firstguess)
	
	## Fit the model by maximum likelihood estimation

print("Optimizing")
	mle <- optim( 	par = firstguess, 
			fn=mnl.likelihood,
			gr=NULL,
			method="BFGS",
			hessian=T,
			control=control,
			data = datapack)
print("After optimization")
	## Create and format the output 

	coefficients <- matrix(0,nrow=K,ncol=4) 
	coefficients[,1] <- mle$par
	if( det(-mle$hessian) == 0 ){
		coefficients[,2] <- rep("NA",K)
		coefficients[,3] <- rep("NA",K)
		coefficients[,4] <- rep("NA",K)
	} 
	else {
		coefficients[,2]<- sqrt(diag(solve(-mle$hessian)))
		coefficients[,3] <- coefficients[,1]/coefficients[,2]
		coefficients[,4] <- 2*pt(abs(coefficients[,3]),n-K-2,lower.tail=F)	
	}
	
	colnames(coefficients) <- c("Estimate","Std. Err.","t-statistic","p-value")

	rownames(coefficients) <- 1:length(K)
	rownames(coefficients) <- coeffnames
#	for( i in 1:length(K)) {
#		rownames(coefficients)[i] <- colnames(????)[i]
#	}

	loglik.convergence <- mle$value
	# Should be equal to mnl.likelihood(mle$par,datapack)

	loglik.zero <- mnl.likelihood(rep(0,K),data)
	loglik.firstguess <- mnl.likelihood(firstguess,data)
	convergence <- mle$convergence
	message <- mle$message
	function.calls <- mle$counts
	time <- proc.time() - ptm

	out <- list(
			loglik.convergence=-loglik.convergence,
			loglik.zero=-loglik.zero,
			loglik.firstguess=-loglik.firstguess,
			time=time,
			convergence=convergence,
			message=message,
			function.calls=function.calls,
			mle=mle)

	cat("Coefficients:\n")
    	print.default(format(coefficients, digits = 3),quote = FALSE)
	
	out 
}



