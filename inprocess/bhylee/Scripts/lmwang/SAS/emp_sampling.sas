/*
sas program used to sample agents and non-repeat alternative set for 
each sampled agent 
*/

/*-create  sample dataset */
data emp;
  input emp_id faz;
  datalines;
1 2 
3 4 
9 16
;
run;
data faz;
  input faz @@@@;
  datalines;
1 2 3 4
5 6 7 8
9 10 11 12
13 14 15 16
;
run;


/*sampling process begins here */
proc surveyselect data=emp
   method=srs samplesize=2      /*replace with number of samples wanted*/
   out=_SampleEmp noprint;
run;
data SampleEmp;
set _SampleEmp;
Replicate + 1;
run;
proc surveyselect data=faz
   method=srs samplesize=10      /*replace with number of alternatives*/
   out=SampleFaz noprint rep=2;  /*replace with number of samples wanted*/
run;
data merged;
  merge SampleEmp (rename = (faz = locate)) 
        SampleFaz;
  by Replicate;
run; 
proc sort data=merged;
by Replicate;
run;
data matched;
  set merged;
  by Replicate;
  if first.Replicate then 
    do;
	  place = 0;
	  matched = 0;
	end;
  place + 1;
  matched + 0;
  if locate = faz then
     do;
      matched = place;
	  output;
	 end;
  if last.Replicate and matched = 0 then 
     do;
                      /*replace 9 with number of alternatives - 1*/
	   matched = round(1 + ranuni(-1)* 9);  
       output;
	 end;
  keep Replicate matched;
run;
data matched_sample;
  merge merged
        matched;
  by Replicate;
run;
data sample;
  set matched_sample;
  by Replicate;
  if first.Replicate then place = 0;
  place + 1;
  choice = 0;
  faz_id = faz;
  if place = matched then 
    do;
      faz_id = locate;
	  choice = 1;
	end;
  keep Replicate emp_id faz_id choice;
run; 
proc sort data=sample;
by Replicate descending choice;
run;
