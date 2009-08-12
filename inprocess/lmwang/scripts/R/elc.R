etwd("C:/eclipse/workspace/Scripts/lmwang/R")
dataset <- read.csv("R:/Projects/PSRC/Estimation/EmpLocChoice/Tables/elc_est_data_9.csv",header=F)
var.list <- c("choice", "job.id", "lva.w", "e.bw", "age.bl", "sfcwrt", "dt.17", "dt.18",
              "dt.19", "dt.20", "dt.21", "dt.22", "dt.23", "dtc.03", "dtc.02", "dtc.01",
              "dtc.04", "dtc.05", "dt.i.g", "e.10w", "e.11w", "e.12w", "e.13w", "e.14w",
              "e.01w", "e.02w", "e.03w", "e.04w", "e.05w", "e.06w", "e.07w", "e.08w", "e.09w",
              "art", "hwy", "lajl", "lalvaw", "lsfc", "lsfcwr", "ld.hy", "livuw", "lsfiw",
              "llv", "lp.w03", "lp.w02", "lp.w01", "lp.w04", "livu", "ldu", "lduw", "lsfrew",
              "ltjl", "lnrsfw", "lvu.rw", "lv", "lwae.1", "lwap.1", "pfl", "phiw", "pliw",
              "pmiw", "pmnw", "popen", "ppub", "proad", "pstcw", "e.rew", "e.saw", "e.sew",
              "tt.air", "tt.cbd", "vac.03", "vac.02", "vac.01", "vac.04", "tt.sov", "tt.tw",
              "ut.sov", "ut.tw")

names(dataset) <- var.list

### /*** create new variables

### ***/ end creating variables

attach(dataset)
Y <- NULL;X <- NULL; X.nchoice <- NULL; X.choice <- NULL
Y.list <-c('choice')
X.nchoice.list <- c('job.id')                            # non-choice specific variable list
X.choice.list <- setdiff(var.list,c(Y.list,X.nchoice.list))  # choice specific variable list

#X.desired.list <- c('dtc.03', 'dt.i.g', 'art', 'lajl', 'livuw', 'lduw', 'lwae.1', 'lwap.1')

X.desired.list <- c('art','lalvaw','lsfc','lsfiw','livu','lv','lwap.1','pmiw','e.bw','e.saw','tt.cbd')

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
  X.nchoice <- cbind(ind[1,X.nchoice.list])
  
  for (j in 1:length(X.desired.list)) {
    X.ind.choice <- cbind(X.ind.choice,t(ind[,X.desired.list[j]]))
  }
  X.choice <- rbind(X.choice, X.ind.choice)
}

Y.namelist <- paste(Y.list,1:10,sep=".")
X.nchoice.namelist <- X.nchoice.list
X.choice.namelist <- NULL
for (k in 1:length(X.desired.list)) {
  X.choice.namelist <- c(X.choice.namelist,paste(X.desired.list[k],1:10,sep="."))
}

Y.df <- data.frame(Y)
names(Y.df) <- Y.namelist
X.nchoice.df <- data.frame(X.nchoice)
names(X.nchoice.df) <- X.nchoice.namelist
X.choice.df <- data.frame(X.choice)
names(X.choice.df) <- X.choice.namelist

dataset.df <- cbind(Y.df,X.nchoice.df,X.choice.df)
save(dataset.df, file="elc.RData")

attach(dataset.df)

library(MNP)


res0 <- mprobit(cbind(choice.1, choice.2,choice.3,choice.4,choice.5,choice.6,choice.7,choice.8,choice.9,choice.10) ~ 1,
               choiceX = list(
                 choice.1 = cbind (art.1, lalvaw.1, lsfc.1, lsfiw.1, livu.1, lv.1, lwap.1.1, pmiw.1, e.bw.1 ),
                 choice.2 = cbind (art.2, lalvaw.2, lsfc.2, lsfiw.2, livu.2, lv.2, lwap.1.2, pmiw.2, e.bw.2 ),
                 choice.3 = cbind (art.3, lalvaw.3, lsfc.3, lsfiw.3, livu.3, lv.3, lwap.1.3, pmiw.3, e.bw.3 ),
                 choice.4 = cbind (art.4, lalvaw.4, lsfc.4, lsfiw.4, livu.4, lv.4, lwap.1.4, pmiw.4, e.bw.4 ),
                 choice.5 = cbind (art.5, lalvaw.5, lsfc.5, lsfiw.5, livu.5, lv.5, lwap.1.5, pmiw.5, e.bw.5 ),
                 choice.6 = cbind (art.6, lalvaw.6, lsfc.6, lsfiw.6, livu.6, lv.6, lwap.1.6, pmiw.6, e.bw.6 ),
                 choice.7 = cbind (art.7, lalvaw.7, lsfc.7, lsfiw.7, livu.7, lv.7, lwap.1.7, pmiw.7, e.bw.7 ),
                 choice.8 = cbind (art.8, lalvaw.8, lsfc.8, lsfiw.8, livu.8, lv.8, lwap.1.8, pmiw.8, e.bw.8 ),
                 choice.9 = cbind (art.9, lalvaw.9, lsfc.9, lsfiw.9, livu.9, lv.9, lwap.1.9, pmiw.9, e.bw.9 ),
                 choice.10 = cbind (art.10, lalvaw.10, lsfc.10, lsfiw.10, livu.10, lv.10, lwap.1.10, pmiw.10, e.bw.10)
                 ),
               data=dataset.df, cXnames=c('art', 'lalvaw', 'lsfc', 'lsfiw', 'livu', 'lv', 'lwap.1','pmiw','e.bw'), verbose=TRUE)



res0 <- mprobit(cbind(choice.1, choice.2,choice.3,choice.4,choice.5,choice.6,choice.7,choice.8,choice.9,choice.10) ~ 1,
               choiceX = list(
                 choice.1 = cbind (art.1, lalvaw.1, lsfc.1, lsfiw.1, livu.1, lv.1, lwap.1.1, pmiw.1, e.bw.1, e.saw.1, tt.cbd.1),
                 choice.2 = cbind (art.2, lalvaw.2, lsfc.2, lsfiw.2, livu.2, lv.2, lwap.1.2, pmiw.2, e.bw.2, e.saw.2, tt.cbd.2),
                 choice.3 = cbind (art.3, lalvaw.3, lsfc.3, lsfiw.3, livu.3, lv.3, lwap.1.3, pmiw.3, e.bw.3, e.saw.3, tt.cbd.3),
                 choice.4 = cbind (art.4, lalvaw.4, lsfc.4, lsfiw.4, livu.4, lv.4, lwap.1.4, pmiw.4, e.bw.4, e.saw.4, tt.cbd.4),
                 choice.5 = cbind (art.5, lalvaw.5, lsfc.5, lsfiw.5, livu.5, lv.5, lwap.1.5, pmiw.5, e.bw.5, e.saw.5, tt.cbd.5),
                 choice.6 = cbind (art.6, lalvaw.6, lsfc.6, lsfiw.6, livu.6, lv.6, lwap.1.6, pmiw.6, e.bw.6, e.saw.6, tt.cbd.6),
                 choice.7 = cbind (art.7, lalvaw.7, lsfc.7, lsfiw.7, livu.7, lv.7, lwap.1.7, pmiw.7, e.bw.7, e.saw.7, tt.cbd.7),
                 choice.8 = cbind (art.8, lalvaw.8, lsfc.8, lsfiw.8, livu.8, lv.8, lwap.1.8, pmiw.8, e.bw.8, e.saw.8, tt.cbd.8),
                 choice.9 = cbind (art.9, lalvaw.9, lsfc.9, lsfiw.9, livu.9, lv.9, lwap.1.9, pmiw.9, e.bw.9, e.saw.9, tt.cbd.9),
                 choice.10 = cbind (art.10, lalvaw.10, lsfc.10, lsfiw.10, livu.10, lv.10, lwap.1.10, pmiw.10, e.bw.10, e.saw.10, tt.cbd.10)
                 ),
               data=dataset.df, cXnames=c('art', 'lalvaw', 'lsfc', 'lsfiw', 'livu', 'lv', 'lwap.1', 'pmiw', 'e.bw', 'e.saw', 'tt.cbd'), verbose=TRUE)



###/*** test simpler models


###***/ complex models

               
