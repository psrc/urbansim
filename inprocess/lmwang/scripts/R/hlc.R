setwd("C:/eclipse/workspace/Scripts/lmwang/R")
dataset <- read.csv("R:/Projects/PSRC/Estimation/HouseLocChoice/Tables/hlc_est_data.csv",header=F)
var.list <- c("choice", "hh.id", "grid.id", "age", "cars", "prsns", "chldrn",
              "income", "race", "faz", "fazdist", "age.bl", "art", "avinc", "cos.in", "dt.01",
              "dt.02", "dt.03", "dt.04", "dt.05", "dt.06", "dt.07", "dt.08", "durw", "dur.c",
              "e.bw", "e.rew", "e.sew", "hwy", "incival", "inclcw", "inclr", "inclrvu", "incpre",
              "incyrb", "lavurw", "ldu", "lduw", "lduw.0", "lduw.1", "lduw.2", "lduw.3", "lduw.f",
              "ld.hy", "le.w", "livu", "livuw", "llva.w", "lnrsfw", "logip", "lsfcw", "lsfiw",
              "lsfref", "lvu.rw", "nc.hdr", "nc.m", "o.ugb", "phiw", "phiw.h", "phiw.l", "phiw.m",
              "pliw.h", "pliw.l", "pliw.m", "pmiw", "pmiw.h", "pmiw.m", "pmnw", "pmnwmj", "pmnwmn",
              "popen", "pstcw", "s.ldu", "s.lduw", "tt.air", "tt.cbd", "yh.hdr", "yh.m", "acttal",
              "acttso", "acctwk", "accttw", "acctta", "hbwual", "hbwuso", "hbwtrw", "hbwwlk",
              "olhae0", "pj20so", "pj20tw", "pj20wk", "hbnwca", "hbnwtr")

names(dataset) <- var.list

### /*** create new variables

### ***/ end creating variables

attach(dataset)
Y <- NULL;X <- NULL;
X.desired.nchoice <- NULL; X.desired.choice <- NULL

Y.list <-c('choice')
X.nchoice.list <- c('hh.id','age','cars','prsns','chldrn','income','race') # non-choice specific variable list
X.choice.list <- setdiff(var.list,c(Y.list,X.nchoice.list))  # choice specific variable list

#working with desired list to save running time, if the whole set is desired set desired.list = var.list - Y.list
X.desired.list <- c("cos.in", "durw", "dur.c", "e.sew", "incival", "inclcw", "lduw.f", "lsfcw", "lsfref", "phiw.h", "pliw.l", "pmiw.m", "tt.cbd", "yh.hdr", "yh.m", "acttso")

#non-choice-specific 
X.desired.nchoice.list <- intersect(X.nchoice.list, X.desired.list)
X.desired.choice.list <- setdiff(X.desired.list, X.desired.nchoice.list)

alt <- 10 #num of alternatives

for (i in 1:(dim(dataset)[1]/alt)) {
  
  start <- (i-1)*alt + 1
  end <- (i-1)*alt + alt
  # temporary variables to store individual info
  ind <- NULL; Y.ind <- NULL; X.ind.choice <- NULL
  
  ind <- dataset[start:end,]
  
  Y.ind <- cbind(t(ind[,Y.list]))
  Y <- rbind(Y,Y.ind)

  #for non-choice specific variables, pick the first value and store to X.nchoice
  X.desired.nchoice <- cbind(ind[1,X.desired.nchoice.list])
  
  for (j in 1:length(X.desired.choice.list)) {
    X.ind.choice <- cbind(X.ind.choice,t(ind[,X.desired.choice.list[j]]))
  }
  X.desired.choice <- rbind(X.desired.choice, X.ind.choice)
}

Y.namelist <- paste(Y.list,1:alt,sep=".")
X.desired.nchoice.namelist <- X.desired.nchoice.list
X.desired.choice.namelist <- NULL
for (k in 1:length(X.desired.choice.list)) {
  X.desired.choice.namelist <- c(X.desired.choice.namelist,paste(X.desired.choice.list[k],1:alt,sep="."))
}

Y.df <- data.frame(Y)
names(Y.df) <- Y.namelist
X.desired.nchoice.df <- data.frame(X.desired.nchoice)
names(X.desired.nchoice.df) <- X.desired.nchoice.namelist
X.desired.choice.df <- data.frame(X.desired.choice)
names(X.desired.choice.df) <- X.desired.choice.namelist

if (dim(X.desired.nchoice.df)[2] == 0) {
  dataset.df <- cbind(Y.df,X.desired.choice.df)
} else {
  dataset.df <- cbind(Y.df,X.desired.nchoice.df,X.desired.choice.df)
}

save(dataset.df, file="hlc.RData")

attach(dataset.df)

library(MNP)


res0 <- mprobit(cbind(choice.1, choice.2,choice.3,choice.4,choice.5,choice.6,choice.7,choice.8,choice.9,choice.10) ~ 1,
               choiceX = list(
                 choice.1 = cbind(cos.in.1, durw.1, dur.c.1, e.sew.1, incival.1, inclcw.1, lduw.f.1, lsfcw.1, lsfref.1, phiw.h.1,
                   pliw.l.1, pmiw.m.1, tt.cbd.1, yh.hdr.1, yh.m.1, acttso.1),
                 choice.2 = cbind(cos.in.2, durw.2, dur.c.2, e.sew.2, incival.2, inclcw.2, lduw.f.2, lsfcw.2, lsfref.2, phiw.h.2,
                   pliw.l.2, pmiw.m.2, tt.cbd.2, yh.hdr.2, yh.m.2, acttso.2),
                 choice.3 = cbind(cos.in.3, durw.3, dur.c.3, e.sew.3, incival.3, inclcw.3, lduw.f.3, lsfcw.3, lsfref.3, phiw.h.3,
                   pliw.l.3, pmiw.m.3, tt.cbd.3, yh.hdr.3, yh.m.3, acttso.3),
                 choice.4 = cbind(cos.in.4, durw.4, dur.c.4, e.sew.4, incival.4, inclcw.4, lduw.f.4, lsfcw.4, lsfref.4, phiw.h.4,
                   pliw.l.4, pmiw.m.4, tt.cbd.4, yh.hdr.4, yh.m.4, acttso.4),
                 choice.5 = cbind(cos.in.5, durw.5, dur.c.5, e.sew.5, incival.5, inclcw.5, lduw.f.5, lsfcw.5, lsfref.5, phiw.h.5,
                   pliw.l.5, pmiw.m.5, tt.cbd.5, yh.hdr.5, yh.m.5, acttso.5),
                 choice.6 = cbind(cos.in.6, durw.6, dur.c.6, e.sew.6, incival.6, inclcw.6, lduw.f.6, lsfcw.6, lsfref.6, phiw.h.6,
                   pliw.l.6, pmiw.m.6, tt.cbd.6, yh.hdr.6, yh.m.6, acttso.6),
                 choice.7 = cbind(cos.in.7, durw.7, dur.c.7, e.sew.7, incival.7, inclcw.7, lduw.f.7, lsfcw.7, lsfref.7, phiw.h.7,
                   pliw.l.7, pmiw.m.7, tt.cbd.7, yh.hdr.7, yh.m.7, acttso.7),
                 choice.8 = cbind(cos.in.8, durw.8, dur.c.8, e.sew.8, incival.8, inclcw.8, lduw.f.8, lsfcw.8, lsfref.8, phiw.h.8,
                   pliw.l.8, pmiw.m.8, tt.cbd.8, yh.hdr.8, yh.m.8, acttso.8),
                 choice.9 = cbind(cos.in.9, durw.9, dur.c.9, e.sew.9, incival.9, inclcw.9, lduw.f.9, lsfcw.9, lsfref.9, phiw.h.9,
                   pliw.l.9, pmiw.m.9, tt.cbd.9, yh.hdr.9, yh.m.9, acttso.9),
                 choice.10 = cbind(cos.in.10, durw.10, dur.c.10, e.sew.10, incival.10, inclcw.10, lduw.f.10, lsfcw.10, lsfref.10,
                   phiw.h.10, pliw.l.10, pmiw.m.10, tt.cbd.10, yh.hdr.10, yh.m.10, acttso.10)
                 ),
               data=dataset.df, cXnames=c("cos.in", "durw", "dur.c", "e.sew", "incival", "inclcw", "lduw.f", "lsfcw", "lsfref",
                                  "phiw.h", "pliw.l", "pmiw.m", "tt.cbd", "yh.hdr", "yh.m", "acttso"), verbose=TRUE)

k

###/*** test simpler models


###***/ complex models

               
