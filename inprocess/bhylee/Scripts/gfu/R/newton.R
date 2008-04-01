newton <- function(f,par,maxit,step,tol.f,...) {
	# Purpose: minimize f
	print("Newton Optimization Begins")

	print("Starting values")
	print(par)
	
	i <- 0
	converged <- FALSE
	derstep <- 0.00001
	while (i<maxit && !converged) {
		i <- i+1
		print("Iteration");print(i)
#		mgh <- fdHess(par,f,...)
#		g <- mgh$gradient	# gradient
#		H <- mgh$Hessian	# Hessian
		g <- findiff.gradient(f=f,par=par,step=derstep,...)
		print("Gradient");print(g)
		H <- findiff.Hessian(f=f,par=par,step=derstep,...)
		print("Hessian");print(H)
		P <- -chol2inv(chol(H))%*%g
		newpar <- par + step*P
		if (abs(f(newpar,...)-f(par,...))<tol.f) {
			converged <- TRUE
		}
		par <- newpar
		print("Estimate");print(par)
		print("Function value");print(f(par,...))
	}
	print("Iterations")
	print(i)
	print("Newton Optimization Done")
	return(par)
}

newton.test <- function () {
	
	# Test function
	testf1 <- function(x) {
		# Min at x=1
		return((x-1)^2)
	}

		
	testf2 <- function(x) {
		# Min at x=1
		return((x[1]-1)^2+(x[2]-2)^2)
	}

	if (newton(f=testf1,par=5,maxit=10,step=1,tol.f=0.001) == 1) {
		print("PASS - One dimensional optimization")
	}
	else {
		print("FAIL - One dimensional optimization")
	}
	res <- newton(f=testf2,par=c(5,5),maxit=10,step=1,tol.f=0.001)
	if (res[1] == 1 && res[2] == 2) {
		print("PASS - Two dimensional optimization")
	}
	else {
		print("FAIL - Two dimensional optimization")
	}
}

findiff.gradient <- function(f,par,step,...) {
	print("Calculating gradient")
	n <- length(par)
	res <- rep(0,n)
	for (i in 1:n) {
		lo <- par
		hi <- par
		lo[i] <- lo[i]-step
		hi[i] <- hi[i]+step
		res[i] = ( f(hi,...)-f(lo,...) ) / (2*step)
	}
	return(res)
}

findiff.Hessian <- function(f,par,step,...) {
	print("Calculating Hessian")
	n <- length(par)
	res <- matrix(0,n,n)
	for (i in 1:n) {
		print("row")
		print(i)
		for (j in i:n) {
			#print("column")
			#print(j)
			hi2 <- par
			hi1 <- par
			lo2 <- par
			lo1 <- par
			hi2[i] <- hi2[i] + step
			hi1[i] <- hi1[i] + step
			lo2[i] <- lo2[i] - step
			lo1[i] <- lo1[i] - step
			hi2[j] <- hi2[j] + step
			hi1[j] <- hi1[j] - step
			lo2[j] <- lo2[j] + step
			lo1[j] <- lo1[j] - step
			res[i,j] = res[j,i] = 
				( (f(hi2,...)-f(hi1,...)) - (f(lo2,...)-f(lo1,...)) ) / (4*step*step)
		}
	}
	return(res)
}

findiff.test <- function() {
	tol <- 0.0001
	step <- 0.00001
	
	testf1 <- function(x) {
		return(x[1]*(1-exp(-0.4*x[2])))
	}
	
	findiff.gradient.out <- findiff.gradient(f=testf1,par=c(12.3, 2.34),step=step)
	findiff.Hessian.out <- findiff.Hessian(f=testf1,par=c(12.3, 2.34),step=step)
	fdHess.out <- fdHess(c(12.3, 2.34), testf1)
	
	print(fdHess.out)
	print(findiff.gradient.out)
	print(findiff.Hessian.out)
	for (i in 1:length(findiff.gradient.out)) {
		if (abs(fdHess.out$gradient[i] - findiff.gradient.out[i])<tol) {
			print("PASS - Gradient")
		}
		else {
			print("FAIL - Gradient")
		}
		for (j in 1:length(findiff.gradient.out)) {
			if (abs(fdHess.out$Hessian[i,j] - findiff.Hessian.out[i,j])<tol) {
				print("PASS - Hessian")
			}
			else {
				print("FAIL - Hessian")
			}
		}
	}
}












