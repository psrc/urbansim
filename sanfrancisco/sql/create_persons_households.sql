create table persons_temp (
household_id int,
person_id int,
homestaz int,
homemtaz int
household_size int,
adults int,
nage65up int,
nage5064 int,
nage2534 int,
nage1824 int,
nage1217 int,
nage511 int,
nageund5 int,
nfulltime int,
nparttime int,
autos int,
household_income int,
gender int,
age int,
relation int,
race int,
employ int,
education int,
occupation int,
industry int,
workstaz int,
worktime double
);

load data infile "C://tourdc_dos.txt" into table san_francisco.persons_temp fields terminated by " ";

create table persons select household_id, person_id, gender, age, relation,
race, employ, education, occupation, industry, workstaz, worktime
from persons_temp;

create table households select household_id, homestaz, homemtaz,
household_size, adults, nfulltime, nparttime, autos, household_income
from persons_temp group by household_id;

