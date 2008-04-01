

## Declaring comparison function
failed.results <- function(result,expected,toler) {
	fails <- 0
	for (i in 1:length(expected)) {
		if (is.na(result[i]) && is.na(expected[i])) {
			print("Missing value")
		}
		else if (abs(expected[i]-result[i])<toler) {
			print("PASS")
		}
		else {
			print("FAIL")
			fails <- fails + 1
		}
	}
	return(fails)
}

mnl.test <- function() {
print("Tests for MNL Likelihood Function")

## Initial values
toler <- 0.001

# Store the starting time
ptm <- proc.time()

# Read the MNL functions
source("C:/eclipse/workspace/Scripts/gfu/R/mnl.R")

# Read the test data
data <- as.matrix(read.table("C:/eclipse/workspace/Scripts/gfu/R/deriv03.csv", header=FALSE, sep=","))

# Define the test MNL model
# The equations matrix is one shorter than the number of data columns
# because the choice vector is removed from the variables matrix
equations <- matrix(nrow=4, ncol=19)
equations[1,] <- c(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
#equations[2,] <- c(0, 1, 0, 0, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14, 0,15)
#equations[3,] <- c(0, 0,16, 0, 2,17, 4, 5, 6,18,19, 9,20,21,22,13,14, 0,23)
#equations[4,] <- c(0, 0, 0,24, 2,25, 4, 5, 6, 0, 0, 9,26,27, 0,13,14, 0, 0)
equations[2,] <- c(0, 1, 0, 0, 4, 5, 8, 9,10,11,13,15,16,19,22,24,25, 0,26)
equations[3,] <- c(0, 0, 2, 0, 4, 6, 8, 9,10,12,14,15,17,20,23,24,25, 0,27)
equations[4,] <- c(0, 0, 0, 3, 4, 7, 8, 9,10, 0, 0,15,18,21, 0,24,25, 0, 0)
equations

fixedcoefficients <- vector(mode="numeric",length=0)
fixedcoefficients

datapack <- list( 
	variables=data[,2:20],
	choice=data[,1],
	equations=equations,
	fixedcoefficients=fixedcoefficients,
	numberofalternatives=4,
	numberofobservations=1878
	)

# Define tests

mnl.test.dataread <- function() {
	print("Test Data Read")
	if (dim(data)[1] == 7512 && dim(data)[2] == 20)  {
		print("PASS")
		return(0)
	}
	else {
		print("FAIL")
		return(1)
	}
}

# Test likelihood at zero
mnl.test.atzero <- function() {
	print("Test Likelihood at Zero")
	coefficients <- rep(0,27)
	return(failed.results(result=mnl.likelihood(coefficients,datapack),expected=2603.461,toler=toler))
}

# Test likelihood at constants
mnl.test.atconstants <- function() {
	print("Test Likelihood at Constants")
	coefficients <- rep(0,27)
	coefficients[1]  <- -1.158687940
	coefficients[2] <- -1.743425822
	coefficients[3] <- -4.493440222
	return(failed.results(result=mnl.likelihood(coefficients,datapack),expected=1661.5463,toler=toler))
}

# Test likelihood at Limdep convergence
mnl.test.atconvergence <- function() {
	print("Test Likelihood at Limdep Convergence")
	coefficients <- c(		
	-15.47261772	,
	-16.21225837	,
	-15.49256599	,
	-0.114970705	,
	0.075254861	,
	0.055402491	,
	0.325171092	,
	-0.019100317	,
	0.008570388	,
	-0.01901187	,
	-0.046301569	,
	-0.033797959	,
	-0.080092776	,
	-0.055547415	,
	-0.028538135	,
	-0.031239995	,
	-0.021907638	,
	-0.088440665	,
	1.369052431	,
	1.371791212	,
	1.057108619	,
	-1.148390404	,
	-1.119260781	,
	0.217460714	,
	-1.679138587	,
	-0.640664769	,
	-1.907013746	
	)	
	return(failed.results(result=mnl.likelihood(coefficients,datapack),expected=1496.083,toler=toler))
}

# Test R optimization, with optim, L-BFGS-B, numerical gradient and Hessian
mnl.test.optim.lbfgsb <- function() {
	print("Test optim 1")
	out <- 0
	firstguess <- rep(0,27)
	coefficients <- c(		
	-15.47261772	,
	-16.21225837	,
	-15.49256599	,
	-0.114970705	,
	0.075254861	,
	0.055402491	,
	0.325171092	,
	-0.019100317	,
	0.008570388	,
	-0.01901187	,
	-0.046301569	,
	-0.033797959	,
	-0.080092776	,
	-0.055547415	,
	-0.028538135	,
	-0.031239995	,
	-0.021907638	,
	-0.088440665	,
	1.369052431	,
	1.371791212	,
	1.057108619	,
	-1.148390404	,
	-1.119260781	,
	0.217460714	,
	-1.679138587	,
	-0.640664769	,
	-1.907013746	
	)	
	control <- list(maxit=20,trace=6,REPORT=1)
	mle <- optim( 	par = firstguess, 
		fn=mnl.likelihood,
		gr=NULL,
		method="L-BFGS-B",
		lower=rep(-20,27),
		upper=rep(2,27),
		hessian=T,
		control=control,
		data = datapack)
	if (failed.results(result=mle$par,expected=coefficients,toler=toler)>0) {
		out <- 1
	}
	return(failed.results(result=mle$value,expected=1496.083,toler=toler)+out)
}

# Test R optimization, with nlm, numerical gradient and Hessian
mnl.test.nlm <- function() {
	print("Test nlm 1")
	out <- 0
	firstguess <- rep(0,27)
	#firstguess <- c(-15,-15,-15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,-1,-1,0,-1,0,-1)
	coefficients <- c(		
	-15.47261772	,
	-16.21225837	,
	-15.49256599	,
	-0.114970705	,
	0.075254861	,
	0.055402491	,
	0.325171092	,
	-0.019100317	,
	0.008570388	,
	-0.01901187	,
	-0.046301569	,
	-0.033797959	,
	-0.080092776	,
	-0.055547415	,
	-0.028538135	,
	-0.031239995	,
	-0.021907638	,
	-0.088440665	,
	1.369052431	,
	1.371791212	,
	1.057108619	,
	-1.148390404	,
	-1.119260781	,
	0.217460714	,
	-1.679138587	,
	-0.640664769	,
	-1.907013746	
	)
	mle <- nlm(f=mnl.likelihood,p=firstguess,print.level=2,fscale=1000,iterlim=1000,data=datapack,check.analyticals=T,hessian=T)
	if (failed.results(result=mle$estimate,expected=coefficients,toler=toler)>0) {
		out <- 1
	}
	return(failed.results(result=mle$minimum,expected=1496.083,toler=toler)+out)
}

# Test R optimization, with newton, numerical gradient and Hessian
mnl.test.newton <- function() {
	print("Test Newton 1")
	out <- 0
	firstguess <- rep(0,27)
	#firstguess <- c(-15,-15,-15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,-1,-1,0,-1,0,-1)
	coefficients <- c(		
	-15.47261772	,
	-16.21225837	,
	-15.49256599	,
	-0.114970705	,
	0.075254861	,
	0.055402491	,
	0.325171092	,
	-0.019100317	,
	0.008570388	,
	-0.01901187	,
	-0.046301569	,
	-0.033797959	,
	-0.080092776	,
	-0.055547415	,
	-0.028538135	,
	-0.031239995	,
	-0.021907638	,
	-0.088440665	,
	1.369052431	,
	1.371791212	,
	1.057108619	,
	-1.148390404	,
	-1.119260781	,
	0.217460714	,
	-1.679138587	,
	-0.640664769	,
	-1.907013746	
	)
	mle <- newton(f=mnl.likelihood,par=firstguess,maxit=1000,step=1,tol.f=0.001,datapack)
	if (failed.results(result=mle,expected=coefficients,toler=toler)>0) {
		out <- 1
	}
	return(failed.results(result=mnl.likelihood(mle,datapack),expected=1496.083,toler=toler)+out)
}
# Test mnl.lm fitting function wrapper
mnl.test.lm <- function() {
	print("Test mnl.lm Fitting Function Wrapper")
	out <- 0
	firstguess <- rep(0,27)
	coeffnames <- c(
	'act3','act4','act5',
	'ltuR','lsa3','lsa4','lsa5',
	'lreR','psaR','preR',
	'pmi3','pmi4','pco3','pco4',
	'pinR','pgo3','pgo4','pgo5',
	'llv3','llv4','llv5',
	'hwy3','hwy4',
	'artR','floR','ugb3','ugb4'
	)
	coefficients <- c(		
	-15.47261772	,
	-16.21225837	,
	-15.49256599	,
	-0.114970705	,
	0.075254861	,
	0.055402491	,
	0.325171092	,
	-0.019100317	,
	0.008570388	,
	-0.01901187	,
	-0.046301569	,
	-0.033797959	,
	-0.080092776	,
	-0.055547415	,
	-0.028538135	,
	-0.031239995	,
	-0.021907638	,
	-0.088440665	,
	1.369052431	,
	1.371791212	,
	1.057108619	,
	-1.148390404	,
	-1.119260781	,
	0.217460714	,
	-1.679138587	,
	-0.640664769	,
	-1.907013746	
	)
	
	mle <- mnl.lm(coefficients,coeffnames,datapack)
#	mle <- mnl.lm(firstguess,coeffnames,datapack)
	mle$loglik.convergence
	mle$loglik.zero
	if (failed.results(result=mle$mle$par,expected=coefficients,toler=toler)>0) {
		out <- out + 1
	}
	out <- out + failed.results(result=mle$loglik.convergence,expected=-1496.083,toler=toler)
	out <- out + failed.results(result=mle$loglik.zero,expected=-2603.461,toler=toler)
	return(out)
}

# Run tests

nrtests <- 0; fails <- 0
nrtests <- nrtests+1; fails <- fails + mnl.test.dataread()
nrtests <- nrtests+1; fails <- fails + mnl.test.atzero()
nrtests <- nrtests+1; fails <- fails + mnl.test.atconstants()
nrtests <- nrtests+1; fails <- fails + mnl.test.atconvergence()
#nrtests <- nrtests+1; fails <- fails + mnl.test.optim.lbfgsb()
#nrtests <- nrtests+2; fails <- fails + mnl.test.nlm()
nrtests <- nrtests+2; fails <- fails + mnl.test.newton()
#nrtests <- nrtests+3; fails <- fails + mnl.test.lm()


# Final test results
print("############# Final test result ###########")
print(list("Successes",nrtests-fails))
print(list("Failures",fails))

time <- proc.time() - ptm
print("Elapsed time")
print(time)

}