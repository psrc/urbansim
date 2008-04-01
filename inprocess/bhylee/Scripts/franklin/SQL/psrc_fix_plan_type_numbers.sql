
create table plan_types_new like plan_types;
insert into plan_types_new select * from plan_types;

update plan_types_new set GPT = "Low Density Single Family" where GPTCODE = 1;
update plan_types_new set GPT = "Undevelopable" where GPTCODE = 2;
update plan_types_new set GPT = "Very Low Density Single Family" where GPTCODE = 3;
update plan_types_new set GPT = "Very High Density Single Family" where GPTCODE = 4;
update plan_types_new set GPT = "Civic with Some Commercial" where GPTCODE = 5;
update plan_types_new set GPT = "CBD Commercial/Multi-Family" where GPTCODE = 6;
update plan_types_new set GPT = "Medium-Low Density Single Family" where GPTCODE = 7;
update plan_types_new set GPT = "Medium-High Density Single Family" where GPTCODE = 8;
update plan_types_new set GPT = "Medium Density Mixed Residential" where GPTCODE = 9;
update plan_types_new set GPT = "Low Density Commercial/Industrial" where GPTCODE = 10;
update plan_types_new set GPT = "Rural Single Family" where GPTCODE = 11;
update plan_types_new set GPT = "Low Density Mixed Commercial/Single Family" where GPTCODE = 12;
update plan_types_new set GPT = "High Density Mixed Residential" where GPTCODE = 13;
update plan_types_new set GPT = "High Density Commercial/Industrial" where GPTCODE = 14;
update plan_types_new set GPT = "Heavy Industrial" where GPTCODE = 15;
update plan_types_new set GPT = "Low Density Mixed Commercial/Multi-Family" where GPTCODE = 16;
update plan_types_new set GPT = "Medium Density Single Family" where GPTCODE = 17;
update plan_types_new set GPT = "Mid-Rise Commercial" where GPTCODE = 18;
update plan_types_new set GPT = "High Density Single Family" where GPTCODE = 19;
update plan_types_new set GPT = "High Density Mixed Commercial/Single Family" where GPTCODE = 20;

