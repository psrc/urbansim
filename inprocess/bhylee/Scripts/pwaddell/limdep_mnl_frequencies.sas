filename in1 'S:\urban-data\UrbanEst\Cities\Utah\App\dev\dev25\25estdata.csv';
filename out 'S:\urban-data\UrbanEst\Cities\Utah\App\dev\dev25\frequencies.csv';

data d1;
infile in1 delimiter=',';
input obs obs_group alt_num v4-v8 chosen;
proc sort;
by alt_num;
proc means noprint sum;
by alt_num;
var chosen;
output out=t1
sum=chosen;
data temp1;
set t1;
olddev=25;
file out;
put olddev ',' alt_num ',' chosen;
proc print;

*proc print;
*var obs obs_group alt_num chosen;
run;

