.packageName <- "MNP"
".First.lib" <- function(lib, pkg) {
  cat("\nMNP: R Package for the Multinomial Probit Models")
  cat("\nversion 0.9-11")
  library.dynam("MNP", pkg, lib)
  cat("\n\n")
}

mprobit <- function(formula, data=parent.frame(), choiceX=NULL,
                    cXnames=NULL, base=NULL, n.draws=5000, p.mean=0,
                    p.var="Inf", p.df=n.dim+1, p.scale=1, coef.start=0,
                    cov.start=1, burnin=0, thin=0, verbose=FALSE) {  
  call <- match.call()
  mf <- match.call(expand = FALSE)
  mf$choiceX <- mf$cXnames <- mf$base <- mf$n.draws <- mf$p.mean <-
    mf$p.var <- mf$p.df <- mf$p.scale <- mf$coef.start <- 
      mf$cov.start <- mf$verbose <- mf$burnin <- mf$thin <- NULL 
  mf[[1]] <- as.name("model.frame.default")
  mf$na.action <- 'na.pass'
  mf <- eval.parent(mf)

  ## obtaining Y
  tmp <- ymatrix.mnp(mf, base=base, extra=TRUE, verbose=verbose)
  Y <- tmp$Y
  MoP <- tmp$MoP
  lev <- tmp$lev
  base <- tmp$base
  p <- tmp$p
  n.dim <- p - 1
  if(verbose)
    cat("\nThe base category is `", base, "'.\n\n", sep="") 
  if (p < 3)
    stop(paste("Error: The number of alternatives should be at least 3."))
  if(verbose) 
    cat("The total number of alternatives is ", p, ".\n\n", sep="") 
  
  ### obtaining X
  tmp <- xmatrix.mnp(formula, data=eval.parent(data),
                     choiceX=call$choiceX, cXnames=cXnames, 
                     base=base, n.dim=n.dim, lev=lev, MoP=MoP,
                     verbose=verbose, extra=TRUE)
  X <- tmp$X
  coefnames <- tmp$coefnames
  n.cov <- ncol(X) / n.dim    #?? num of cov = 
  n.obs <- nrow(X)
  if (verbose)
    cat("The dimension of beta is ", n.cov, ".\n\n", sep="")

  ## checking the prior for beta
  p.imp <- FALSE 
  if (p.var == Inf) {
    p.imp <- TRUE
    p.prec <- diag(0, n.cov)
    if (verbose)
      cat("Improper prior will be used for beta.\n\n")
  }
  else if (is.matrix(p.var)) {
    if (ncol(p.var) != n.cov || nrow(p.var) != n.cov)
      stop("Error: The dimension of `p.var' should be ", n.cov, " x ", n.cov, sep="")
    if (sum(sign(eigen(p.var)$values) < 1) > 0)
      stop("Error: `p.var' must be positive definite.")
    p.prec <- solve(p.var)
  }
  else {
    p.var <- diag(p.var, n.cov)
    p.prec <- solve(p.var)
  }
  if (length(p.mean) > 1) {
    if (length(p.mean) != n.cov)
      stop(paste("Error: The dimenstion of `p.mean' must be  ", n.cov, ".", sep=""))
  }
  else
    p.mean <- rep(p.mean, n.cov)
  if (sum(abs(p.mean)) == 0 || p.imp) {
    alg <- 1
    if (verbose)
      cat("Algorithm 1 will be used.\n\n")
  }
  else {
    alg <- 2
    if (MoP)
      stop(paste("Error: The prior for beta has to be improper or mean zero for the Multinomial ordered Probit Model."))
  if (verbose)
      cat("Algorithm 2 will be used.\n\n")
  }

  ## checking prior for Sigma
  p.df <- eval(p.df)
  if (length(p.df) > 1)
    stop(paste("Error: `p.df' must be a positive integer."))
  if (p.df < n.dim)
    stop(paste("Error: `p.df' must be at least ", n.dim, ".", sep=""))
  if (abs(as.integer(p.df) - p.df) > 0)
    stop(paste("Error: `p.df' must be a positive integer."))
  if (!is.matrix(p.scale)) 
    p.scale <- diag(p.scale, n.dim)
  if (ncol(p.scale) != n.dim || nrow(p.scale) != n.dim)
    stop("Error: `p.scale' must be ", n.dim, " x ", n.dim, sep="")
  if (sum(sign(eigen(p.scale)$values) < 1) > 0)
    stop("Error: `p.scale' must be positive definite.")
  Signames <- NULL
  for(j in 1:n.dim)
    for(k in 1:n.dim)
      if (j<=k)
        Signames <- c(Signames, paste(if(MoP) lev[j] else lev[j+1],
                                      ":", if(MoP) lev[k] else lev[k+1], sep="")) 

  ## checking starting values
  if (length(coef.start) == 1)
    coef.start <- rep(coef.start, n.cov)
  else if (length(coef.start) != n.cov)
    stop(paste("Error: The dimenstion of `coef.start' must be  ",
               n.cov, ".", sep=""))
  if (cov.start==1)
    cov.start <- diag(n.dim)
  else if (!is.matrix(cov.start)) 
    stop("Error: `cov.start' must be a positive definite matrix.")
  else if (ncol(cov.start) != n.dim || nrow(cov.start) != n.dim)
    stop("Error: The dimension of `cov.start' must be ", n.dim, " x ", n.dim, sep="")
  else if (sum(sign(eigen(cov.start)$values) < 1) > 0)
    stop("Error: `cov.start' must be a positive definite matrix.")
  else if (cov.start[1,1] != 1)
    stop("Error: cov.start[1,1] should be 1.")

  ## checking thinnig and burnin intervals
  if (burnin < 0)
    stop("Error: `burnin' should be a non-negative integer.") 
  if (thin < 0)
    stop("Error: `thin' should be a non-negative integer.")
  keep <- thin + 1
  
  ## running the algorithm
  n.par <- n.cov + n.dim*(n.dim+1)/2
  if(verbose)
    cat("Starting Gibbs sampler...\n")
  # recoding NA into -1
  Y[is.na(Y)] <- -1 
  param <- .C("cMNPgibbs", as.integer(alg), as.integer(n.dim),
              as.integer(n.cov), as.integer(n.obs), as.integer(n.draws),
              as.double(p.mean), as.double(p.prec), as.integer(p.df),
              as.double(p.scale), as.double(X), as.integer(Y), 
              as.double(coef.start), as.double(cov.start), 
              as.integer(p.imp), as.integer(burnin), as.integer(keep), 
              as.integer(verbose), as.integer(MoP),
              pdStore = double(n.par*(ceiling((n.draws-burnin)/keep)+1)))$pdStore
  param <- matrix(param, ncol=n.par,
                  nrow=(ceiling((n.draws-burnin)/keep)+1), byrow=TRUE)
  colnames(param) <- c(coefnames, Signames)

  ##recoding -1 back into NA
  Y[Y==-1] <- NA
  ## returning the object
  res <- list(param=param, x=X, y=Y, call=call, alg=alg, n.alt=p,
              p.mean= if(p.imp) NULL else p.mean, p.var=p.var,
              p.df=p.df, p.scale=p.scale, 
              burnin=burnin, thin=thin, seed=.Random.seed)
  class(res) <- "mnp"
  return(res)
}
  


print.summary.mnp <- function(x, digits = max(3, getOption("digits") - 3), ...) {

  cat("\nCall:\n")
  cat(paste(deparse(x$call), sep = "\n", collapse = "\n"), "\n\n",
      sep = "") 

  cat("\nCoefficients:\n")
  printCoefmat(x$coef.table, digits = digits, na.print = "NA", ...)
  
  cat("\nCovariances:\n")
  printCoefmat(x$cov.table, digits = digits, na.print = "NA", ...)
  
  cat("\nNumber of alternatives:", x$n.alt)
  cat("\nNumber of observations:", x$n.obs)
  cat("\n\n")
  invisible(x)
}
summary.mnp <- function(object, CI=c(2.5, 97.5),...){

  p <- object$n.alt
  param <- object$param
  n.cov <- ncol(param) - p*(p-1)/2
  n.draws <- nrow(param)
  param.table <- cbind(apply(param, 2, mean), apply(param, 2, sd),
                       apply(param, 2, quantile, min(CI)/100),
                       apply(param, 2, quantile, max(CI)/100)) 
  colnames(param.table) <- c("mean", "std.dev.", paste(min(CI), "%", sep=""),
                             paste(max(CI), "%", sep=""))
  
  ans <- list(call=object$call, n.alt=p, n.obs=if(is.matrix(object$y))
              nrow(object$y) else length(object$y),
              coef.table=param.table[1:n.cov,],
              cov.table=param.table[(n.cov+1):ncol(param),])  
  class(ans) <- "summary.mnp"
  return(ans)
}
xmatrix.mnp <- function(formula, data = sys.parent(), choiceX=NULL,
                        cXnames=NULL, base=NULL, n.dim, lev,
                        MoP=FALSE, verbose=FALSE, extra=FALSE) {
  call <- match.call()
  mf <- match.call(expand = FALSE)
  mf$choiceX <- mf$cXnames <- mf$base <- mf$n.dim <- mf$lev <-
    mf$MoP <- mf$verbose <- mf$extra <- NULL  
  
  ## get variables
  mf[[1]] <- as.name("model.frame.default")
  mf$na.action <- 'na.pass'
  mf <- eval.parent(mf)
  Terms <- attr(mf, "terms")
  X <- model.matrix.default(Terms, mf)
  xvars <- as.character(attr(Terms, "variables"))[-1]
  if ((yvar <- attr(Terms, "response")) > 0)
    xvars <- xvars[-yvar]
  
  xlev <- if (length(xvars) > 0) {
    xlev <- lapply(mf[xvars], levels)
    xlev[!sapply(xlev, is.null)]
  }

  p <- n.dim + 1
  n.obs <- nrow(X)
  n.cov <- ncol(X)

  ## expanding X
  Xcnames <- colnames(X)
  allvnames <- NULL
  for (i in 1:n.cov) {
    Xv <- X[, pmatch(Xcnames[i], colnames(X))]
    X <- X[, -pmatch(Xcnames[i], colnames(X))]
    Xtmp <- varnames <- NULL
    for (j in 1:n.dim) {
      allvnames <- c(allvnames, paste(Xcnames[i], ":", if(MoP)
                                      lev[j] else lev[j+1], sep=""))
      for (k in 1:n.dim)
        varnames <- c(varnames, paste(Xcnames[i], ":", if(MoP) lev[j]
        else lev[j+1], sep=""))
      tmp <- matrix(0, nrow = n.obs, ncol = n.dim)
      tmp[, j] <- Xv
      Xtmp <- cbind(Xtmp, tmp)
    }
    colnames(Xtmp) <- varnames
    X <- cbind(X, Xtmp)
  }

  ## checking and adding choice-specific variables
  if (!is.null(choiceX)) {
    cX <- eval(choiceX, data)
    cXn <- unique(names(cX))
    if (sum(is.na(pmatch(cXn, lev))) > 0)
      stop(paste("Error: Invalid input for `choiceX.'\n Some variables do not exist."))
    if(MoP) 
      xbase <- as.matrix(cX[[lev[p]]])
    else if (is.na(pmatch(base, cXn)))
      xbase <- NULL
    else
      xbase <- as.matrix(cX[[base]])
    if (length(cXn) < n.dim)
      stop(paste("Error: Invalid input for `choiceX.'\n You must specify the choice-specific varaibles at least for all non-base categories."))
    if (!is.null(xbase) && length(cXn) != p)
      stop(paste("Error: Invalid input for `choiceX.'\n You must specify the choice-specific variables at least for all non-base categories."))
    if(!is.null(xbase) && verbose)
      cat("The choice-specific variables of the base category are subtracted from the corresponding variables of the non-base categories.\n\n")
    for (i in 1:length(cXnames)) 
      for (j in 1:n.dim) {
        if (length(cXnames) != ncol(as.matrix(cX[[if(MoP) lev[j] else lev[j+1]]])))
            stop(paste("Error: The number of variables in `choiceX' and `cXnames' does not match."))  
        tmp <- matrix(as.matrix(cX[[if(MoP) lev[j] else lev[j+1]]])[,i], ncol=1)
        if (!is.null(xbase)) 
          tmp <- tmp - xbase[,i]
        colnames(tmp) <- paste(cXnames[i], ":", if(MoP) lev[j] else lev[j+1], sep="") 
        X <- cbind(X, tmp)
      }
  }
  if(extra)
    return(list(X=X, coefnames=c(allvnames, cXnames)))
  else
    return(X)
}
ymatrix.mnp <- function(data, base=NULL, extra=FALSE, verbose=verbose) { 
  ## checking and formatting Y
  Y <- model.response(data)
  if (is.matrix(Y)) { # Multinomial ordered Probit model
    for (i in 1:nrow(Y))
      Y[i,] <- match(Y[i,], sort(unique(Y[i,]))) - 1
    p <- ncol(Y)
    lev <- colnames(Y)
    MoP <- TRUE
    if(!is.null(base))
      stop("Error: The last column of the response matrix must be the base category.\n No need to specify `base.'") 
    base <- lev[p]
  }
  else { # standard Multinomial Probit model        
    Y <- as.factor(Y)
    lev <- levels(Y)
    if (!is.null(base) && lev[1] != base)
      if (base %in% lev) {
        tmp <- lev
        lev[1] <- base
        lev[pmatch(base, tmp)] <- tmp[1]
        levels(Y) <- lev
      }
      else
        stop(paste("Error: `base' does not exist in the response variable.")) 
    base <- lev[1]
    counts <- table(Y)
    if (any(counts == 0)) {
      warning(paste("group(s)", paste(lev[counts == 0], collapse = " "), "are empty"))
      Y <- factor(Y, levels  = lev[counts > 0])
      lev <- lev[counts > 0]
    }
    p <- length(lev)
    Y <- unclass(Y) - 1
    MoP <- FALSE
  }
  if(extra)
    return(list(Y=Y, MoP=MoP, lev=lev, p=p, base=base))
  else
    return(Y)
}
