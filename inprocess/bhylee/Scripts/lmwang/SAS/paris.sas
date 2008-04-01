libname sampling 'c:\workspace\paris\dataset';

/*read-in datasets*/
proc import datafile="W:\users\lmwang\eclipse\opus\sandbox\paris_est.csv"
out=sampling.ds0
dbms=csv
replace;
getnames=yes;
run;

proc import datafile="W:\users\lmwang\eclipse\opus\sandbox\paris_com.tab"
out=sampling.com
dbms=tab
replace;
getnames=yes;
run;

proc mdc data=sampling.ds0;
      model decision = LPImput /*TC VP */
            poor_m rich_m foreign_m LLogRP99 / type=clogit
            choice=(com );
            id id;
            output out=estim0EA p=pred0EA;
      run;

data estim0EA;set estim0EA;keep pred0EA com;run;
proc sort data=estim0EA;by com;run;
proc means data=estim0EA noprint;by com;output out=estim0EAM;run;

data estim0EAM;set estim0EAM;if _STAT_="MEAN";run;
data estim0EAM;set estim0EAM;drop _TYPE_ _STAT_ id ;EA0demand=500*_freq_*pred0EA;run;
data estim0EAM;set estim0EAM;keep com EA0demand pred0EA;run;
proc sort data=estim0EAM;by com;run;

data sampling.estimEAcom;merge sampling.com estim0EAM;by com;run;
data sampling.estimEAcom;set sampling.estimEAcom;
supply=(units9 - unitssec9 - stayers98)*.5+unitsvac9*.5;
SD0ratio=supply/EA0demand;
constraint0EA=(SD0ratio<1);
pred0EAInC=pred0EA*constraint0EA;
pred0EASDInC=pred0EAInC*SD0ratio;
kept=1;
run;

proc means data=sampling.estimEAcom;output out=omega0EA;run;
data omega0EA;set omega0EA;if _STAT_="MEAN";run;
data omega0EA;set omega0EA;omega0EA=(1-1300*pred0EASDInC)/(1-1300*pred0EAInC);run;
data omega0EA;set omega0EA;kept=1;keep kept omega0EA;run;

data sampling.estimEAcom;merge sampling.estimEAcom omega0EA;by kept;run;

data sampling.estimEPcom;set sampling.estimEAcom;
*constraint0EP1=(omega0EA*EA0demand)>supply;
constraint0EP1=SD0ratio<omega0EA;
pred0EP1InC=pred0EA*constraint0EP1;
pred0EP1SDInC=pred0EP1InC*SD0ratio;
run;
proc freq;tables constraint0EA*constraint0EP1;run;

proc means data=sampling.estimEPcom;output out=omega0EP;run;
data omega0EP;set omega0EP;if _STAT_="MEAN";run;
data omega0EP;set omega0EP;omega0EP1=(1-1300*pred0EP1SDInC)/(1-1300*pred0EP1InC);run;
data omega0EP;set omega0EP;kept=1;keep kept omega0EP1;run;

data sampling.estimEPcom;merge sampling.estimEPcom omega0EP;by kept;run;
data sampling.estimEPcom;set sampling.estimEPcom;
constraint0EP2=SD0ratio<omega0EP1;
pred0EP2InC=pred0EA*constraint0EP2;
pred0EP2SDInC=pred0EP2InC*SD0ratio;
run;
proc freq;tables constraint0EP1*constraint0EP2;run;

proc means data=sampling.estimEPcom;output out=omega0EP;run;
data omega0EP;set omega0EP;if _STAT_="MEAN";run;
data omega0EP;set omega0EP;omega0EP2=(1-1300*pred0EP2SDInC)/(1-1300*pred0EP2InC);run;
data omega0EP;set omega0EP;kept=1;keep kept omega0EP2;run;

data sampling.estimEPcom;merge sampling.estimEPcom omega0EP;by kept;run;
data sampling.estimEPcom;set sampling.estimEPcom;
constraint0EP3=SD0ratio<omega0EP2;
pred0EP3InC=pred0EA*constraint0EP3;
pred0EP3SDInC=pred0EP3InC*SD0ratio;
run;
proc freq;tables constraint0EP2*constraint0EP3;run;


proc means data=sampling.estimEPcom;output out=omega0EP;run;
data omega0EP;set omega0EP;if _STAT_="MEAN";run;
data omega0EP;set omega0EP;omega0EP3=(1-1300*pred0EP3SDInC)/(1-1300*pred0EP3InC);run;
data omega0EP;set omega0EP;kept=1;keep kept omega0EP3;run;

data sampling.estimEPcom;merge sampling.estimEPcom omega0EP;by kept;run;
data sampling.estimEPcom;set sampling.estimEPcom;
constraint0EP4=SD0ratio<omega0EP3;
pred0EP4InC=pred0EA*constraint0EP4;
pred0EP4SDInC=pred0EP4InC*SD0ratio;
run;
proc freq;tables constraint0EP3*constraint0EP4;run;

/*convergence achieved*/

data sampling.estimEPcom;set sampling.estimEPcom;
LnPi1=constraint0EP3*log(SD0ratio) + (1-constraint0EP3)*log(omega0EP3);run;

data sampling.pi;set sampling.estimEPcom;lnPi=lnPi1;keep com LnPi;run;
proc sort data=sampling.pi;by com;run;

data sampling.ds0;set sampling.ds0;drop lnPi;run;
proc sort data=sampling.ds0;by com;run;
data sampling.ds0; merge sampling.pi sampling.ds0;by com;run;
proc sort data=sampling.ds0;by id;run;

proc mdc data=sampling.ds0;
      model decision = LPImput /*TC VP */
            poor_m rich_m foreign_m LLogRP99 LnPi / type=clogit
            choice=(com );
            id id;
            output out=estim1EA p=pred1TildeEA;
      run;

data estim1EA;set estim1EA;pred1EA=pred1TildeEA/exp(LnPi);keep pred1EA pred1TildeEA com;run;
proc sort data=estim1EA;by com;run;
proc means data=estim1EA noprint;by com;output out=estim1EAM;run;

data estim1EAM;set estim1EAM;if _STAT_="MEAN";run;
data estim1EAM;set estim1EAM;drop _TYPE_ _STAT_ ;EA1demand=500*_freq_*pred1EA;run;
data estim1EAM;set estim1EAM;keep com EA1demand pred1EA pred1TildeEA;run;

data sampling.estimEPcom;merge sampling.estimEPcom estim1EAM;by com;run;
data sampling.estimEPcom;set sampling.estimEPcom;
SD1ratio=supply/EA1demand;
constraint1EA=(SD1ratio<1);
pred1EAInC=pred1EA*constraint1EA;
pred1EASDInC=pred1EAInC*SD1ratio;
run;
proc freq;tables constraint0EA*constraint1EA;run;

proc means data=sampling.estimEPcom;output out=omega1EA;run;
data omega1EA;set omega1EA;if _STAT_="MEAN";run;
data omega1EA;set omega1EA;omega1EA=(1-1300*pred1EASDInC)/(1-1300*pred1EAInC);run;
data omega1EA;set omega1EA;kept=1;keep kept omega1EA;run;

data sampling.estimEPcom;merge sampling.estimEPcom omega1EA;by kept;run;

data sampling.estimEPcom;set sampling.estimEPcom;
constraint1EP1=SD1ratio<omega1EA;
pred1EP1InC=pred1EA*constraint1EP1;
pred1EP1SDInC=pred1EP1InC*SD1ratio;
run;
proc freq;tables constraint1EA*constraint1EP1;run;
proc freq;tables constraint0EA*constraint1EA;run;
proc freq;tables constraint0EP1*constraint1EP1;run;

proc means data=sampling.estimEPcom;output out=omega1EP;run;
data omega1EP;set omega1EP;if _STAT_="MEAN";run;
data omega1EP;set omega1EP;omega1EP1=(1-1300*pred1EP1SDInC)/(1-1300*pred1EP1InC);run;
data omega1EP;set omega1EP;kept=1;keep kept omega1EP1;run;

data sampling.estimEPcom; merge sampling.estimEPcom omega1EP;by kept;run;

data sampling.estimEPcom;set sampling.estimEPcom;
constraint1EP2=SD1ratio<omega1EP1;
pred1EP2InC=pred1EA*constraint1EP2;
pred1EP2SDInC=pred1EP2InC*SD1ratio;
run;
proc freq;tables constraint1EP1*constraint1EP2;run;

proc means data=sampling.estimEPcom;output out=omega1EP;run;
data omega1EP;set omega1EP;if _STAT_="MEAN";run;
data omega1EP;set omega1EP;omega1EP2=(1-1300*pred1EP2SDInC)/(1-1300*pred1EP2InC);run;
data omega1EP;set omega1EP;kept=1;keep kept omega1EP2;run;

data sampling.estimEPcom;merge sampling.estimEPcom omega1EP;by kept;run;

data sampling.estimEPcom;set sampling.estimEPcom;
constraint1EP3=SD1ratio<omega1EP2;
pred1EP3InC=pred1EA*constraint1EP3;
pred1EP3SDInC=pred1EP3InC*SD1ratio;
run;
proc freq;tables constraint1EP2*constraint1EP3;run;

/*convergence achieved*/

data sampling.estimEPcom;set sampling.estimEPcom;
LnPi2=constraint1EP2*log(SD1ratio) + (1-constraint1EP2)*log(omega1EP2);run;

data sampling.pi;set sampling.estimEPcom;lnPi=lnPi2;keep com LnPi;run;
proc sort data=sampling.pi;by com;run;

/*******************************************************/
data sampling.ds0;set sampling.ds0;drop lnPi;run;
proc sort data=sampling.ds0;by com;run;
data sampling.ds0;merge sampling.pi sampling.ds0;by com;run;

proc sort data=sampling.ds0;by id;run;
proc mdc data=sampling.ds0;
      model decision = LPImput /*TC VP */
            poor_m rich_m foreign_m LLogRP99 LnPi / type=clogit
            choice=(com );
            id id;
            output out=estim2EA p=pred2TildeEA;
      run;

data estim2EA;set estim2EA;pred2EA=pred2TildeEA/exp(LnPi);keep pred2EA pred2TildeEA com;run;
proc sort data=estim2EA;by com;run;

proc means data=estim2EA noprint;by com;output out=estim2EAM;run;
data estim2EAM;set estim2EAM;if _STAT_="MEAN";run;
data estim2EAM;set estim2EAM;drop _TYPE_ _STAT_ ;EA2demand=500*_freq_*pred2EA;run;
data estim2EAM;set estim2EAM;keep com EA2demand pred2EA pred2TildeEA;run;

data sampling.estimEPcom;merge sampling.estimEPcom estim2EAM;by com;run;
data sampling.estimEPcom;set sampling.estimEPcom;
SD2ratio=supply/EA2demand;
constraint2EA=(SD2ratio<1);
pred2EAInC=pred2EA*constraint2EA;
pred2EASDInC=pred2EAInC*SD2ratio;
run;
proc freq;tables constraint1EA*constraint2EA;run;

proc means data=sampling.estimEPcom;output out=omega2EA;run;
data omega2EA;set omega2EA;if _STAT_="MEAN";run;
data omega2EA;set omega2EA;omega2EA=(1-1300*pred2EASDInC)/(1-1300*pred2EAInC);run;
data omega2EA;set omega2EA;kept=1;keep kept omega2EA;run;

data sampling.estimEPcom;merge sampling.estimEPcom omega2EA;by kept;run;

data sampling.estimEPcom;set sampling.estimEPcom;
constraint2EP1=SD2ratio<omega2EA;
pred2EP1InC=pred2EA*constraint2EP1;
pred2EP1SDInC=pred2EP1InC*SD2ratio;
run;
proc freq;tables constraint2EA*constraint2EP1;run;
proc freq;tables constraint1EP1*constraint2EP1;run;

proc means data=sampling.estimEPcom;output out=omega2EP;run;
data omega2EP;set omega2EP;if _STAT_="MEAN";run;
data omega2EP;set omega2EP;omega2EP1=(1-1300*pred2EP1SDInC)/(1-1300*pred2EP1InC);run;
data omega2EP;set omega2EP;kept=1;keep kept omega2EP1;run;

data sampling.estimEPcom;merge sampling.estimEPcom omega2EP;by kept;run;

data sampling.estimEPcom;set sampling.estimEPcom;
constraint2EP2=SD2ratio<omega2EP1;
pred2EP2InC=pred2EA*constraint2EP2;
pred2EP2SDInC=pred2EP2InC*SD2ratio;
run;
proc freq;tables constraint2EP1*constraint2EP2;run;

proc means data=sampling.estimEPcom;output out=omega2EP;run;
data omega2EP;set omega2EP;if _STAT_="MEAN";run;
data omega2EP;set omega2EP;omega2EP2=(1-1300*pred2EP2SDInC)/(1-1300*pred2EP2InC);run;
data omega2EP;set omega2EP;kept=1;keep kept omega2EP2;run;
data sampling.estimEPcom;merge sampling.estimEPcom omega2EP;by kept;run;

data sampling.estimEPcom;set sampling.estimEPcom;
constraint2EP3=SD2ratio<omega2EP2;
pred2EP3InC=pred2EA*constraint2EP3;
pred2EP3SDInC=pred2EP3InC*SD2ratio;
run;
proc freq;tables constraint2EP2*constraint2EP3;run;

/*convergence achieved*/

data sampling.estimEPcom;set sampling.estimEPcom;
LnPi3=constraint2EP2*log(SD2ratio) + (1-constraint2EP2)*log(omega2EP2);run;

data sampling.pi;set sampling.estimEPcom;lnPi=lnPi3;keep com LnPi;run;
proc sort data=sampling.pi;by com;run;

proc corr data=sampling.estimEPcom;var lnPi1 lnPi2 lnPi3;run;

/*******************************************************/
data sampling.ds0;set sampling.ds0;drop lnPi;run;
proc sort data=sampling.ds0;by com;run;
data sampling.ds0;merge sampling.pi sampling.ds0;by com;run;

proc sort data=sampling.ds0;by id;run;
proc mdc data=sampling.ds0;
      model decision = LPImput /*TC VP */
            poor_m rich_m foreign_m LLogRP99 LnPi / type=clogit
            choice=(com );
            id id;
            output out=estim3EA p=pred3TildeEA;
      run;

data estim3EA;set estim3EA;pred3EA=pred3TildeEA/exp(LnPi);keep pred3EA pred3TildeEA com;run;
proc sort data=estim3EA;by com;run;
proc means data=estim3EA noprint;by com;output out=estim3EAM;run;

data estim3EAM;set estim3EAM;if _STAT_="MEAN";run;
data estim3EAM;set estim3EAM;drop _TYPE_ _STAT_ ;EA3demand=500*_freq_*pred3EA;run;
data estim3EAM;set estim3EAM;keep com EA3demand pred3EA pred3TildeEA;run;

data sampling.estimEPcom;merge sampling.estimEPcom estim3EAM;by com;run;
data sampling.estimEPcom;set sampling.estimEPcom;
SD3ratio=supply/EA3demand;
constraint3EA=(SD3ratio<1);
pred3EAInC=pred3EA*constraint3EA;
pred3EASDInC=pred3EAInC*SD3ratio;
run;
proc freq;tables constraint2EA*constraint3EA;run;

proc means data=sampling.estimEPcom;output out=omega3EA;run;
data omega3EA;set omega3EA;if _STAT_="MEAN";run;
data omega3EA;set omega3EA;omega3EA=(1-1300*pred3EASDInC)/(1-1300*pred3EAInC);run;
data omega3EA;set omega3EA;kept=1;keep kept omega3EA;run;

data sampling.estimEPcom;merge sampling.estimEPcom omega3EA;by kept;run;

data sampling.estimEPcom;set sampling.estimEPcom;
constraint3EP1=SD3ratio<omega3EA;
pred3EP1InC=pred3EA*constraint3EP1;
pred3EP1SDInC=pred3EP1InC*SD3ratio;
run;
proc freq;tables constraint3EA*constraint3EP1;run;
proc freq;tables constraint2EP1*constraint3EP1;run;

proc means data=sampling.estimEPcom;output out=omega3EP;run;
data omega3EP;set omega3EP;if _STAT_="MEAN";run;
data omega3EP;set omega3EP;omega3EP1=(1-1300*pred3EP1SDInC)/(1-1300*pred3EP1InC);run;
data omega3EP;set omega3EP;kept=1;keep kept omega3EP1;run;

data sampling.estimEPcom;merge sampling.estimEPcom omega3EP;by kept;run;

data sampling.estimEPcom;set sampling.estimEPcom;
constraint3EP2=SD3ratio<omega3EP1;
pred3EP2InC=pred3EA*constraint3EP2;
pred3EP2SDInC=pred3EP2InC*SD3ratio;
run;
proc freq;tables constraint3EP1*constraint3EP2;run;


proc means data=sampling.estimEPcom;output out=omega3EP;run;
data omega3EP;set omega3EP;if _STAT_="MEAN";run;
data omega3EP;set omega3EP;omega3EP2=(1-1300*pred3EP2SDInC)/(1-1300*pred3EP2InC);run;
data omega3EP;set omega3EP;kept=1;keep kept omega3EP2;run;
data sampling.estimEPcom;merge sampling.estimEPcom omega3EP;by kept;run;

data sampling.estimEPcom;set sampling.estimEPcom;
constraint3EP3=SD3ratio<omega3EP2;
pred3EP3InC=pred3EA*constraint3EP3;
pred3EP3SDInC=pred3EP3InC*SD3ratio;
run;
proc freq;tables constraint3EP2*constraint3EP3;run;


proc means data=sampling.estimEPcom;output out=omega3EP;run;
data omega3EP;set omega3EP;if _STAT_="MEAN";run;
data omega3EP;set omega3EP;omega3EP3=(1-1300*pred3EP3SDInC)/(1-1300*pred3EP3InC);run;
data omega3EP;set omega3EP;kept=1;keep kept omega3EP3;run;
data sampling.estimEPcom;merge sampling.estimEPcom omega3EP;by kept;run;

data sampling.estimEPcom;set sampling.estimEPcom;
constraint3EP4=SD3ratio<omega3EP3;
pred3EP4InC=pred3EA*constraint3EP4;
pred3EP4SDInC=pred3EP4InC*SD3ratio;
run;
proc freq;tables constraint3EP3*constraint3EP4;run;

/* convergence achieved */

data sampling.estimEPcom;set sampling.estimEPcom;
LnPi4=constraint3EP3*log(SD3ratio) + (1-constraint3EP3)*log(omega3EP3);
*LnPi5=constraint3EP3*log(SD2ratio) + (1-constraint3EP3)*log(omega3EP3);
run;

data sampling.pi;set sampling.estimEPcom;lnPi=lnPi4;keep com LnPi;run;
proc sort data=sampling.pi;by com;run;
proc corr data=sampling.estimEPcom;var lnPi1 lnPi2 lnPi3 lnpi4;run;
