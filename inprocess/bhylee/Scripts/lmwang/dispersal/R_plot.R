f30 <- read.table("c:/eclipseB/workspace/Scripts/lmwang/dispersal/counts_by_faz_30.tab")
#names(faz30) <- c("fazid","year","counts")
#attach(faz30)
n <- length(f30$V1)
f30$cc[1] <- f30$V3[1]
f30$a[1] <- 1
for (i in 2:n){
f30$cc[i] = f30$cc[i-1] + f30$V3[i]
f30$a[i] <- i
}
plot(f30$V1, f30$cc, type="l")
detach()

f01 <- read.table("c:/eclipseB/workspace/Scripts/lmwang/dispersal/counts_by_faz_01.tab")
#names(f01) <- c("fazid","year","counts")
n <- length(f01$V1)
f01$cc[1] <- f01$V3[1]
f01$a[1] <- 1
#attach(faz01)
for (i in 2:n){
f01$cc[i] = f01$cc[i-1] + f01$V3[i]
f01$a[i] <- i
}

plot(f30$V1, log(f30$cc), type="l")
lines(f01$V1, log(f01$cc))
