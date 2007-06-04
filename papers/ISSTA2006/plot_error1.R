# Figure 1
postscript(file="error1.ps")
par(mfrow=c(1,2))
data <- read.table("error1data.tab")
max <- max(data[,c(2,4,6,8)], na.rm=TRUE)
min <- min(data[,c(2,4,6,8)], na.rm=TRUE)
par(cex=1.3, cex.lab=1.5, cex.axis=1.3)
plot(data[,1],data[,2], type="b", pch=1, ylim=c(min, max), ylab="frequency of type I error", xlab="R", main="alpha=0.05")
lines(data[,1],data[,4], type="b", pch=2)
lines(data[,1],data[,6], type="b", pch=3)
lines(data[,1],data[,8], type="b", pch=4)
abline(h=0.05,lty=2)
legend(data[nrow(data)-3,1], max, legend="T1: LRTS(normal)",pch=1, bty="n", lty=1, cex=1.1)
legend(data[nrow(data)-3,1], max-(max-min)/10, legend="T1: LRTS(poisson)",pch=2, bty="n", lty=1, cex=1.1)
legend(data[nrow(data)-3,1], max-2*(max-min)/10, legend="T1: Pearson(poisson)",pch=3, bty="n", lty=1, cex=1.1)
legend(data[nrow(data)-3,1], max-3*(max-min)/10, legend="T2: LRTS(normal)",pch=4, bty="n", lty=1, cex=1.1)

data <- read.table("error1data.tab")
max <- max(data[,c(3,5,7, 9)], na.rm=TRUE)
min <- min(data[,c(3,5,7, 9)], na.rm=TRUE)
plot(data[,1],data[,3], type="b", pch=1, ylim=c(min, max), ylab="frequency of type I error", xlab="R", main="alpha=0.01")
lines(data[,1],data[,5], type="b", pch=2)
lines(data[,1],data[,7], type="b", pch=3)
lines(data[,1],data[,9], type="b", pch=4)
abline(h=0.01,lty=2)
legend(data[nrow(data)-3,1], max, legend="T1: LRTS(normal)",pch=1, bty="n", lty=1, cex=1.1)
legend(data[nrow(data)-3,1], max-(max-min)/10, legend="T1: LRTS(poisson)",pch=2, bty="n", lty=1, cex=1.1)
legend(data[nrow(data)-3,1], max-2*(max-min)/10, legend="T1: Pearson(poisson)",pch=3, bty="n", lty=1, cex=1.1)
legend(data[nrow(data)-3,1], max-3*(max-min)/10, legend="T2: LRTS(normal)",pch=4, bty="n", lty=1, cex=1.1)
dev.off()

# Figure 2
postscript(file="error1_k_agents.ps")
#par(mfrow=c(1,2))
par(cex=1.7, cex.lab=1.5, cex.axis=1.3)
data <- read.table("error1data_k.tab")
max<-max(data[,2:3],0.05,0.2)
min <- min(data[,2:3],0.05)
plot(data[,1],data[,2], type="b", pch=1, ylab="frequency of type I error", xlab="K", log="x", ylim=c(min, max))
lines(data[,1],data[,3], type="b", pch=2, log="x")
legend(10,max, legend="T1: LRTS(poisson)", pch=1, bty="n", lty=1, cex=1.4)
legend(10,max-(max-min)/10, legend="T1: Pearson(poisson)", pch=2, bty="n", lty=1, cex=1.4)
abline(h=0.05,lty=2)
#data <- read.table("error1data_agents.tab")
#plot(data[,1],data[,2], type="b", pch=1, ylab="frequency of type I error", xlab="\#agents/K (K=50)")
#abline(h=0.05,lty=2)
dev.off()

R<-c(2,5,10,15,20)

# Figure 3
postscript(file="power_poisson.ps")
par(mfrow=c(1,2))
par(cex=1.3, cex.lab=1.5, cex.axis=1.3)
data <- read.table("power_poisson.tab")
max <- max(data[,2:ncol(data)], na.rm=TRUE)
min <- min(data[,2:ncol(data)], na.rm=TRUE)
plot(data[,1],data[,2], type="b", pch=1, ylab="power", xlab="increment in #agents",
     ylim=c(min,max), main="alpha=0.05")
for (i in 2:5) {
  lines(data[,1],data[,i+1], type="b", pch=i)
}
for (i in 1:5) {
  legend(data[nrow(data)-2,1], min+(11-i)*(max-min)/18, legend=paste("LR (",R[i],")",sep=""),pch=i, bty="n", lty=1, cex=1.1)
}

data2 <- read.table("power_pearson.tab")

for (i in 1:5) {
  lines(data2[,1],data2[,i+1], type="b", pch=i, lty=2)
}
for (i in 1:5) {
  legend(data2[nrow(data)-2,1], min+(6-i)*(max-min)/18, legend=paste("Pe (",R[i],")",sep=""),pch=i, bty="n", lty=2, cex=1.1)
}

plot(data[,1],data[,7], type="b", pch=1, ylab="power", xlab="increment in #agents",
     ylim=c(min,max), main="alpha=0.01")
for (i in 2:5) {
  lines(data[,1],data[,6+i], type="b", pch=i)
}
for (i in 1:5) {
  legend(data[nrow(data)-2,1], min+(11-i)*(max-min)/18, legend=paste("LR (",R[i],")",sep=""),pch=i, bty="n", lty=1, cex=1.1)
}

data2 <- read.table("power_pearson.tab")

for (i in 1:5) {
  lines(data2[,1],data2[,6+i], type="b", pch=i, lty=2)
}
for (i in 1:5) {
  legend(data2[nrow(data)-2,1], min+(6-i)*(max-min)/18, legend=paste("Pe (",R[i],")",sep=""),pch=i, bty="n", lty=2, cex=1.1)
}
dev.off()

# Figure 4
postscript(file="power_normal.ps")
par(mfrow=c(1,2))
par(cex=1.3, cex.lab=1.5, cex.axis=1.3)
data <- read.table("power_normal.tab")
max <- max(data[,2:ncol(data)], na.rm=TRUE)
min <- min(data[,2:ncol(data)], na.rm=TRUE)

plot(data[,1],data[,2], type="b", pch=1, ylab="power", xlab="age increment",
     ylim=c(min,max), main="alpha=0.05")
for (i in 2:5) {
  lines(data[,1],data[,(i+1)], type="b", pch=i)
}
for (i in 1:5) {
  legend(data[nrow(data)-2,1], min+(6-i)*(max-min)/15, legend=paste("R=",R[i],sep=""),
         pch=i, bty="n", lty=1, cex=1.2)
}

plot(data[,1],data[,7], type="b", pch=1, ylab="power", xlab="age increment",
     ylim=c(min,max), main="alpha=0.01")
for (i in 2:5) {
  lines(data[,1],data[,(i+6)], type="b", pch=i)
}
for (i in 1:5) {
  legend(data[nrow(data)-2,1], min+(6-i)*(max-min)/15, legend=paste("R=",R[i],sep=""),
         pch=i, bty="n", lty=1, cex=1.2)
}
dev.off()
