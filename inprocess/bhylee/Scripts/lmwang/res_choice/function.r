mosaic <- function(X, main=NA, sort=NA, off=NA, dir=NA, color=FALSE) {
######################################################################
# SPLUS Mosaic Graphical Procedure                                   #
# Jay Emerson, Yale University, February 1998                        #
######################################################################
# See "Mosaic Displays in S-PLUS: A General Implementation and a     #
# Case Study," by J.W. Emerson, _Statistical Computing and           #
# Statistical Graphics Newsletter_, 9(1), 17-23.                     #
######################################################################
# Plot Mosaic                                                        #
#                                                                    #
# DESCRIPTION:                                                       #
#         Plots a mosaic on the current graphics device.             #
#                                                                    #
# USAGE:                                                             #
#         mosaic(X, main=NA, sort=NA, off=NA, dir=NA, color=F)       #
#                                                                    #
# REQUIRED ARGUMENTS:                                                #
# X:      a contingency table, with optional category labels         #
#         specified in the dimnames(X) attribute.  The table is best #
#         created by the table() command, which produces an object   #
#         of type array.                                             #
#                                                                    #
# OPTIONAL ARGUMENTS:                                                #
# main:   character string for the mosaic title.                     #
# sort:   vector ordering of the variables, containing a permutation #
#         of the integers 1:length(dim(X)) (the default).            #
# off:    vector of offsets to determine percentage spacing at each  #
#         level of the mosaic (appropriate values are between 0 and  #
#         20, and the default is 10 at each level).  There should be #
#         one offset for each dimension of the contingency table.    #
# dir:    vector of split directions ("v"=vertical and               #
#         "h"=horizontal) for each level of the mosaic, one          #
#         direction for each dimension of the contingency table.     #
#         The default consists of alternating directions, beginning  #
#         with a vertical split.                                     #
# color:  (TRUE or vector of integer colors) for color shading or    #
#         (FALSE, the default) for empty boxes with no shading.      #
######################################################################
######################################################################
# NOTES:                                                             #
#         1. Use of the par(fin) environment variable can be helpful #
#            when the desired mosaic is not square.                  #
#         2. When using the student version of S-PLUS for Windows,   #
#            limitations on the version may prevent drawing          #
#            high-dimensional mosaics.                               #
#         3. This file should be run (or source("mosaic.code")) with #
#            each new .Data directory.                               # 
######################################################################

    frame()
    par(usr=c(1,1000,1,1000))
    if (is.vector(X)) { X <- array(X) }
    dimd <- length(dim(X))
    if (!is.null(dimnames(X))) { label <- dimnames(X) } else { label <- NA }
    if (dimd>1) {
        Ind <- rep(1:(dim(X)[1]), prod(dim(X)[2:dimd]))
        for (i in 2:dimd) {
            Ind <- cbind(Ind, c(matrix(1:(dim(X)[i]), byrow=T,
                prod(dim(X)[1:(i-1)]), prod(dim(X)[i:dimd]))))
        }
    } else {
        Ind <- 1:(dim(X)[1])
    }
    Ind <- cbind(Ind, c(X))
    if (!is.na(main)) { title(main) }    # Make the title.
    if ((is.na(off[1]))||(length(off)!=dimd)) { # Initialize spacing.
        off <- rep(10,50)[1:dimd]
    }
    if (is.na(dir[1])||(length(dir)!=dimd)) { # Initialize directions.
        dir <- rep(c("v","h"),50)[1:dimd]
    }
    if ((!is.na(sort[1]))&&(length(sort)==dimd)) { # Sort columns.
        Ind <- Ind[,c(sort,dimd+1)]
        off <- off[sort]
        dir <- dir[sort]
        label <- label[sort]
    }
    ncolors <- length(tabulate(Ind[,dimd]))
    if (is.na(color[1])) {
        color <- rep(0, ncolors)
    } else {
        if (length(color) != ncolors) {
            if (!color[1]) { color <- rep(0, ncolors) }
            else { color <- 2:(ncolors+1) }
        }
    }

    mosaic.cell(Ind, 50, 5, 950, 950,
        off/100, dir, color, 2, 2, apply(as.matrix(Ind[,1:dimd]), 2, max),
        1, label)

}


mosaic.cell <- function(X, x1, y1, x2, y2, off, dir, color, lablevx, lablevy,
                 maxdim, currlev, label) {

    if (dir[1] == "v") {                # split here on the X-axis.
        xdim <- maxdim[1]
        XP <- rep(0, xdim)
        for (i in 1:xdim) {
            XP[i] <- sum(X[X[,1]==i,ncol(X)]) / sum(X[,ncol(X)])
        }
        white <- off[1] * (x2 - x1) / (max(1, xdim-1))
        x.l <- x1
        x.r <- x1 + (1 - off[1]) * XP[1] * (x2 - x1)
        if (xdim > 1) {
            for (i in 2:xdim) {
                x.l <- c(x.l, x.r[i-1] + white)
                x.r <- c(x.r, x.r[i-1] + white +
                        (1 - off[1]) * XP[i] * (x2 - x1))
            }
        }
        if (lablevx > 0) {
            if (is.na(label[[1]][1])) {
                this.lab <- paste(rep(as.character(currlev), length(currlev)),
                        as.character(1:xdim), sep=".")
            } else { this.lab <- label[[1]] }
            text(x=(x.l + (x.r - x.l) / 2), y=(965 + 22 * (lablevx - 1)),
                    srt=0,adj=.5, cex=.5, this.lab)
        }
        if (ncol(X) > 2) {        # recursive call.
            for (i in 1:xdim) {
                if (XP[i] > 0) {
                    mosaic.cell(as.matrix(X[X[,1]==i,2:ncol(X)]), x.l[i], y1, x.r[i],
                            y2, off[2:length(off)], dir[2:length(dir)], color,
                            lablevx-1, (i==1)*lablevy, maxdim[2:length(maxdim)],
                            currlev+1, label[2:ncol(X)])
                } else {
                    segments(rep(x.l[i],3), y1+(y2-y1)*c(0,2,4)/5,
                            rep(x.l[i],3), y1+(y2-y1)*c(1,3,5)/5)
                }
            }
        } else {
            for (i in 1:xdim) {
                if (XP[i] > 0) {
                    polygon(c(x.l[i], x.r[i], x.r[i], x.l[i]),
                        c(y1, y1, y2, y2), col=color[i])
                    segments(c(rep(x.l[i],3),x.r[i]), c(y1,y1,y2,y2),
                        c(x.r[i],x.l[i],x.r[i],x.r[i]), c(y1,y2,y2,y1))
                } else {
                    segments(rep(x.l[i],3), y1+(y2-y1)*c(0,2,4)/5,
                            rep(x.l[i],3), y1+(y2-y1)*c(1,3,5)/5)
                }
            }
        }
    } else {                # split here on the Y-axis.
        ydim <- maxdim[1]
        YP <- rep(0, ydim)
        for (j in 1:ydim) {
            YP[j] <- sum(X[X[,1]==j,ncol(X)]) / sum(X[,ncol(X)])
        }
        white <- off[1] * (y2 - y1) / (max(1, ydim - 1))
        y.b <- y2 - (1 - off[1]) * YP[1] * (y2 - y1)
        y.t <- y2
        if (ydim > 1) {
            for (j in 2:ydim) {
                y.b <- c(y.b, y.b[j-1] - white -
                        (1 - off[1]) * YP[j] * (y2 - y1))
                y.t <- c(y.t, y.b[j-1] - white)
            }
        }
        if (lablevy > 0) {
            if (is.na(label[[1]][1])) {
                this.lab <- paste(rep(as.character(currlev), length(currlev)),
                        as.character(1:ydim), sep=".")
            } else { this.lab <- label[[1]] }
            text(x=(35 - 20 * (lablevy - 1)), y=(y.b + (y.t - y.b) / 2),
                    srt=90, adj=.5, cex=.5, this.lab)
        }
        if (ncol(X) > 2) {        # recursive call.
            for (j in 1:ydim) {
                if (YP[j] > 0) {
                    mosaic.cell(as.matrix(X[X[,1]==j,2:ncol(X)]),
                            x1, y.b[j], x2, y.t[j], off[2:length(off)],
                            dir[2:length(dir)], color, (j==1)*lablevx,
                            lablevy-1, maxdim[2:length(maxdim)],
                            currlev+1, label[2:ncol(X)])
                } else {
                    segments(x1+(x2-x1)*c(0,2,4)/5, rep(y.b[j],3),
                            x1+(x2-x1)*c(1,3,5)/5, rep(y.b[j],3))
                }
            }
        } else{                        # final split polygon and segments.
            for (j in 1:ydim) {
                if (YP[j] > 0) {
                    polygon(c(x1,x2,x2,x1),
                        c(y.b[j],y.b[j],y.t[j],y.t[j]), col=color[j])
                    segments(c(x1,x1,x1,x2), c(y.b[j],y.b[j],y.t[j],y.t[j]),
                        c(x2,x1,x2,x2), c(y.b[j],y.t[j],y.t[j],y.b[j]))
                } else {
                    segments(x1+(x2-x1)*c(0,2,4)/5, rep(y.b[j],3),
                            x1+(x2-x1)*c(1,3,5)/5, rep(y.b[j],3))
                }
            }
        }
    }

} # end(function mosaic.cell)
#

powdivind <- function(obs, lambda = 2/3, statonly = F)
{
	#
	# Function to calculate Cressie-Read power divergence goodness-of-fit statistic for independence in
	# two-dimensional table
	#
	# Input parameters
	#
	#   obs      - two-dimensional matrix of observed counts
	#   lambda   - power for statistic
	#                lambda = 1    : Pearson statistic
	#                lambda = 2/3  : Cressie-Read statistic
	#                lambda = 0    : likelihood ratio statistic
	#                lambda = -1/2 : Freeman-Tukey statistic
	#                lambda = -2   : Neyman-modified statistic
	#   statonly - set equal to T if want only statistic output
	#
	# Output parameters
	#
	#   stat    - statistic
	#   df      - degrees of freedom for statistic
	#   pval    - p-value for statistic based on a chi-squared distribution with
	#             degrees of freedom equal to df
	#   exp     - expected counts under independence
	#   resid   - matrix of residuals derived from test statistic
	#
	# Note: For all statistics except the Pearson statistic, cells with observed counts
	#       equal to zero do not contribute to the test statistic (effectively this
	#       means that 0 * log(0) and 0 * Infinity are taken to be zero). This can lead to
	#       strange values of the statistic (such as negative values) for lambda less
	#       than zero.
	#
	rowmarg <- apply(obs, 1, sum)
	colmarg <- apply(obs, 2, sum)
	n <- sum(obs)
	exp <- outer(rowmarg, colmarg)/n
	if(lambda == 0) {
		resid <- sqrt(2 * (obs * log(ifelse((obs > 0 & exp > 0), obs/exp, 1))  +  exp - obs)) * sign(obs - exp)
	}
	else {
		resid <- sqrt(2/(lambda * (lambda  +  1)) * (obs * ((obs/exp)^lambda - 1)  +  lambda * (exp - obs))) * sign(obs - exp)
	}
	stat <- sum(resid^2)
	df <- cumprod(dim(obs) - c(1, 1))[2]
	pval <- 1 - pchisq(stat, df)
	if(statonly)
		return(stat)
	else return(list(stat = stat, df = df, pval = pval, exp = exp, resid = resid))}
#


