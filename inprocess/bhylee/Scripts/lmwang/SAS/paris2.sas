libname sampling 'c:\workspace\paris\dataset1pct';

/*read-in datasets*/
proc import datafile="W:\users\lmwang\eclipse\opus\sandbox\paris_est1pct.csv"
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

/******** sampling.com********/
data sampling.com;set sampling.com;j=_n_;
movers98=units9 - stayers98 - unitssec9 - unitsvac9;
dept=75;
if com>76999 & com<78000 then dept=77;
if com>77999 & com<79000 then dept=78;
if com>90999 & com<92000 then dept=91;
if com>91999 & com<93000 then dept=92;
if com>92999 & com<94000 then dept=93;
if com>93999 & com<95000 then dept=94;
if com>94999 & com<96000 then dept=95;
run;

data com;
set sampling.com;
keep com units9;
run;

proc sort data=sampling.ds0;
by com;
run;

proc sort data=com;
by com;
run;

data sampling.ds0;
merge sampling.ds0 com;
by com;
run;

proc sort data=sampling.ds0;
by id com;
run;

data sampling.ds0;
set sampling.ds0;
LLogRP99=Log(units9);
run;

proc means data=sampling.ds0;
run;

data sampling.ds0;set sampling.ds0;
dept=75;
if com>76999 & com<78000 then dept=77;
if com>77999 & com<79000 then dept=78;
if com>90999 & com<92000 then dept=91;
if com>91999 & com<93000 then dept=92;
if com>92999 & com<94000 then dept=93;
if com>93999 & com<95000 then dept=94;
if com>94999 & com<96000 then dept=95;
run;


proc freq data=sampling.ds0;
table dept*decision;
run;


/*****************************************************************/
/******************************** macros *************************/
/*****************************************************************/

%macro lambdaDept;
proc sort data=sampling.com;by dept;run;
proc means data=sampling.com;by dept;
output out=sampling.availabilityDept sum(movers98 stayers98 unitsvac9 units9)=;run;
data sampling.availabilityDept ;set sampling.availabilityDept ;
availabRatio=unitsvac9 / units9;
lambda=units9/(units9-unitsvac9) - unitsvac9 / movers98;
run;

data sampling.availabilityDept;set sampling.availabilityDept;
*keep dept availabratio lambda;run;
proc sort data=sampling.availabilityDept;by dept;run;

proc print data=sampling.availabilityDept;run;

data sampling.comDept;merge sampling.com sampling.availabilityDept; by dept;run;
data sampling.comDept;set sampling.availabilityDept;supply=lambda*movers98+unitsvac9;run;

%mend lambdaDept;

%lambdaDept;
run;


%macro estimHomoEA(tabin,ratio,tabout,tabest,tabOutCom,tabOutCumul,l,j,omegaTab,omegaTabEP);

proc sort data=&tabin;by id;run;
proc mdc data=&tabin outest=&tabest;
      model decision = LPImput TC
            foreign_m LLogRP99 / type=clogit
            choice=(com );
            id id;
            output out=&tabout p=predEA;
      run;

data &tabest;set &tabest;level="dept";ratio=&ratio; l=&l; drop _model_ _type_ _status_ _method_ _name_;run;

data &tabout;set &tabout;keep predEA com;run;
proc sort data=&tabout;by com;run;

proc means data=&tabout noprint;by com;output out=&tabOutCom sum(predEA)=EAdemand&l mean(predEA)=predEA&l;run;

data &tabOutCom;set &tabOutCom;
EAdemand&l = &ratio * EAdemand&l;
keep com EAdemand&l predEA&l;run;

proc sort data=&tabOutCom;by com;run;

data &tabOutCumul;merge sampling.com &tabOutCom;by com;run;

data &tabOutCumul;set &tabOutCumul;
SDratio&l=supply/EAdemand&l;
ConstraintEA&l = (SDratio&l < 1);
predEAInC&l =predEA&l * ConstraintEA&l ;
predEASDInC&l = predEAInC&l * SDratio&l;
kept=1;
run;

proc means noprint data=&tabOutCumul;output out=&omegaTab sum(predEAInC&l predEASDInC&l )=predEAInC&l predEASDInC&l ;run;
data &omegaTab ;set &omegaTab ;omegaEA&l =(1-predEASDInC&l )/(1-predEAInC&l );kept=1;keep kept omegaEA&l;run;
proc print;run;

data &tabOutCumul;merge &tabOutCumul &omegaTab;by kept;run;
data &tabOutCumul;set &tabOutCumul;
constraintEP&l&j=SDratio&l<omegaEA&l;
predEPInC&l&j=predEA&l*constraintEP&l&j;
predEPSDInC&l&j=predEPInC&l&j*SDratio&l;
run;

proc freq; tables constraintEA&l*constraintEP&l&j ;
run;

proc means data=&tabOutCumul noprint;output out=&omegaTabEP sum(predEPSDInC&l&j predEPInC&l&j)=predEPSDInC&l&j predEPInC&l&j;run;
data &omegaTabEP;set &omegaTabEP;omegaEP&l&j=(1-predEPSDInC&l&j)/(1-predEPInC&l&j);kept=1;keep kept omegaEP&l&j;run;

%mend estimHomoEA;run;

%macro InLoop(tabin,omega,l,i,j);
data &tabin;merge &tabin &omega;by kept;run;
data &tabin;set &tabin;
constraintEP&l&j=SDratio&l<omegaEP&l&i;
predEPInC&l&j=predEA&l*constraintEP&l&j;
predEPSDInC&l&j=predEPInC&l&j*SDratio&l;
run;

proc freq; tables constraintEP&l&i*constraintEP&l&j ;
run;

proc means data=&tabIn noprint;output out=&omega sum(predEPSDInC&l&j predEPInC&l&j)=predEPSDInC&l&j predEPInC&l&j;run;
data &omega;set &omega;omegaEP&l&j=(1-predEPSDInC&l&j)/(1-predEPInC&l&j);kept=1;keep kept omegaEP&l&j;run;

%mend InLoop;

data sampling.estimComDept1;set sampling.estimComDept1;drop omegaEP02;run;
%inloop(sampling.estimComDept1,omegaEPDept1,0,1,2);
%inloop(sampling.estimComDept1,omegaEPDept1,0,2,3);
%inloop(sampling.estimComDept1,omegaEPDept1,0,3,4);


%macro arretInLoop(tabin,tabOmega,l,count) ;
%do i=1 %to 10;
      %if &count>0 %then %do;
            %let j=%eval(&i+1);
            %inloop(&tabIn,&tabOmega,&l,&i,&j);

            data &tabin;set &tabin;diff&l&i&j=(constraintEP&l&j ne constraintEP&l&i);run;
            proc means data=&tabin;;output out=stop sum(diff&l&i&j)=count;run;

            data stop;set stop;
            call symput('count',count);
            run;

            %put at step i=&i there are &count differences(s) between constraintEP&l&j et constraintEP&l&i;

      %end;
%end;
%mend arretInLoop;

%arretInLoop(sampling.estimComDept1,omegaEPDept1,0,1300);run;


data sampling.estimComDept1;set sampling.estimComDept1;diff012=(constraintEP02 ne constraintEP01);run;
proc means data=sampling.estimComDept1;output out=stop sum(diff012)=count;run;

data sampling.estimComDept1;set sampling.estimComDept1;diff023=(constraintEP03 ne constraintEP02);run;
proc means data=sampling.estimComDept1;output out=stop sum(diff023)=count;run;

data sampling.estimComDept1;set sampling.estimComDept1;diff034=(constraintEP04 ne constraintEP03);run;
proc means data=sampling.estimComDept1;output out=stop sum(diff034)=count;run;

%lambdaDept;run;

%universal(Dept,1);run;

%arretInLoop(sampling.estimCom,count,constraint0EP2,constraint0EP3);

%estimHomoEA(sampling.universalDept1,100,estimEADept1,estDept1,estimEAMDept1,sampling.estimComDept1,0,1,omegaEADept1,omegaEPDept1);
%estimHomoEA(sampling.ds0,500,estimEADept500,estDept500,estimEAMDept500,sampling.estimComDept500,0,1,omegaEADept500,omegaEPDept500);

*estimHomoEA(tabin,                ratio,tabout,      , tabest, tabOutCom,    tabOutCumul,          l,j,omegaTab,    omegaTabEP);
