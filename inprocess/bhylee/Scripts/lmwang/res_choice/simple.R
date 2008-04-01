setwd("C:/eclipse/workspace/Scripts/lmwang/res_choice")

pallvar <- read.delim("ex_pois.tab",na.strings = 'NULL')

for (i in 2:dim(pallvar)[2]) {
  pallvar <- pallvar[!is.na(pallvar[,i]),]
}
pallvar$restype = as.factor(pallvar$restype)
pallvar$income = as.factor(pallvar$income)
pallvar$age_range = as.factor(pallvar$age_range)

detach();attach(pallvar)
pallvar$linear.age[age_range == '<=30'] <- 20
pallvar$linear.age[age_range == '31-40'] <- 35
pallvar$linear.age[age_range == '41-50'] <- 45
pallvar$linear.age[age_range == '51-65'] <- 57
pallvar$linear.age[age_range == '>65'] <- 70

pallvar$quadratic.age <- pallvar$linear.age ^ 2
library(MASS)

attach(pallvar)

pfit.a <- glm(count ~ restype + hhsize + income + linear.age + quadratic.age,
             data = pallvar, family = poisson)

pfit.b <- glm(count ~  (restype + hhsize + income + linear.age + quadratic.age)^2,
             data = pallvar, family = poisson)

pfit.c <- glm(count ~ restype + hhsize + income + age_range,
            data = pallvar, family = poisson)

pfit.c1 <- glm(count ~ restype:hhsize + restype:income + restype:age_range,
            data = pallvar, family = poisson)

pfit.c2 <- glm(count ~  restype:hhsize + restype:income + restype:linear.age + restype:quadratic.age,
            data = pallvar, family = poisson)

pfit.d <- glm(count ~  (restype + hhsize + income + age_range)^2,
            data = pallvar, family = poisson)

pfit.e <- glm(count ~  age_range + (restype + hhsize + income + linear.age + quadratic.age)^2,
            data = pallvar, family = poisson)

anova(pfit.c, pfit.c1, test="Chisq")
anova(pfit.c1, pfit.d, test="Chisq")

pstep <- stepAIC(pfit.c1, scope=list(upper = pfit.d, lower = ~1), trace =F)
pstep$anova

par(mfrow=c(2,2))
plot(pfit.c1)

#table(count,predict(pstep)>0)

#multinom
mallvar <- read.delim("ex_multinom.tab",na.strings='NULL')
n.v = dim(mallvar)[2]-4
for (i in 1:n.v) {
  mallvar <- mallvar[!is.na(mallvar[,i]),]
  #mallvar[,i] <- as.factor(mallvar[,i])
}
detach();attach(mallvar)
mallvar$linear.age[age_range == '<= 30'] <- 20
mallvar$linear.age[age_range == '31 - 40'] <- 35
mallvar$linear.age[age_range == '41 - 50'] <- 45
mallvar$linear.age[age_range == '51 - 65'] <- 57
mallvar$linear.age[age_range == '> 80'] <- 70

mallvar$quadratic.age <- mallvar$linear.age ^ 2

#mallvar$restype = as.factor(mallvar$restype)
mallvar$income = as.factor(mallvar$income)
mallvar$age_range = as.factor(mallvar$age_range)

detach();attach(mallvar)
library(MASS)
library(nnet)
choice <- as.matrix(cbind(restype_1,restype_2,restype_4,restype_8))
hhsize.i <- mallvar$hhsize
income.i <- mallvar$income
age.range.i <- mallvar$age_range

attach(mallvar)
mfit <- multinom(choice ~ hhsize.i + income.i + age.range.i, data = mallvar)
mfit
summary(mfit)

#VGAM
detach();attach(mallvar)
library(VGAM)

vfit <- vglm(cbind(restype_2,restype_4,restype_8, restype_1) ~ hhsize + income + age_range, multinomial, mallvar) 

#compare running time

# ps.ptm <- proc.time()
# pfit.d2 <- glm(count ~  restype*hhsize + income*age_range + restype:age_range + restype:income + hhsize:age_range,
#             data = pallvar, family = poisson)
# pe.ptm <- proc.time()
# pe.ptm - ps.ptm

# ms.ptm <- proc.time()
# mfit <- multinom(choice ~ hhsize.i + income.i + age.range.i, data = mallvar)
# me.ptm <- proc.time()
# me.ptm - ms.ptm

# vs.ptm <- proc.time()
# vfit <- vglm(cbind(restype_2,restype_4,restype_8, restype_1) ~
#              hhsize + income + age_range, multinomial, mallvar) 
# ve.ptm <- proc.time()
# ve.ptm - vs.ptm

#mnp
library(MNP)
mnps.ptm <- proc.time()
mnpfit <- mprobit(cbind(restype_2,restype_4,restype_8, restype_1) ~
                  hhsize + income + age_range, data=mallvar, n.draws = 5000,
                  verbose=TRUE)
mnpe.ptm <- proc.time()
mnpe.ptm - mnps.ptm




##################################################################################
