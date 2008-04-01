#number of children in each household
create table h01a_children (index QNO_id using btree (QNO)) ENGINE = MyISAM
select QNO, count(*) as children from pshhts_pers_021507 
where age < 18 group by QNO order by QNO;
#1265 households with children

create table h01b_children_unknown (index QNO_id using btree (QNO)) ENGINE = MyISAM
select QNO from pshhts_pers_021507
where age = 998 or age = 999 group by QNO order by QNO;
#44 households with person whose age is unknown or refused

alter table h01b_children_unknown add column children bigint(21);
update h01b_children_unknown set children = -1;

select a.* from h01a_children as a left join h01b_children_unknown as b
on a.QNO = b.QNO where b.QNO is not null;
#7 households with children have person whose age is unknown or refused

create table h01c_children_known (index QNO_id using btree (QNO)) ENGINE = MyISAM
select a.* from h01a_children as a left join h01b_children_unknown as b
on a.QNO = b.QNO where b.QNO is null;
#1258 households with known ages have children

create table h01d_children_none (index QNO_id using btree (QNO)) ENGINE = MyISAM
select a.QNO from pshhts_hh_021507 as a 
left join h01b_children_unknown as b on a.QNO = b.QNO
left join h01c_children_known as c on a.QNO = c.QNO
where b.QNO is null and c.QNO is null;
#3444 households with known ages have no children

alter table h01d_children_none add column children bigint(21);
update h01d_children_none set children = 0;

create table h01_children (index QNO_id using btree (QNO)) ENGINE = MyISAM
select a.* from h01b_children_unknown as a
union all
select b.* from h01c_children_known as b
union all
select c.* from h01d_children_none as c;


#household total income (TOTALINC) categories
	1  Less than $10,000
	2  $10,000 to less than $20,000
	3  $20,000 to less than $30,000
	4  $30,000 to less than $40,000
	5  $40,000 to less than $50,000
	6  $50,000 to less than $60,000
	7  $60,000 to less than $70,000
	8  $70,000 to less than $80,000
	9  $80,000 to less than $90,000
	10  $90,000 to less than $100,000
	11  $100,000 to less than $110,000
	12  $110,000 to less than $120,000
	13  $120,000 to less than $130,000
	14  $130,000 to less than $140,000
	15  $140,000 to less than $150,000
	16  $150,000 or more
	17  Below $50,000 - Dont know/Refused
	18  $50,000 to $100,000 - Dont know/Refused
	19  Above $100,000 - Dont know/Refused
	98  Dont Know
	99  Refused

#translate household total income from categorical to nominal variable
create table h02_income (index QNO_id using btree (QNO)) ENGINE = MyISAM
select QNO, TOTALINC from pshhts_hh_021507;

alter table h02_income add column income double;

update h02_income set income = 5000 where TOTALINC = 1;
update h02_income set income = 15000 where TOTALINC = 2;
update h02_income set income = 25000 where TOTALINC = 3;
update h02_income set income = 35000 where TOTALINC = 4;
update h02_income set income = 45000 where TOTALINC = 5;
update h02_income set income = 55000 where TOTALINC = 6;
update h02_income set income = 65000 where TOTALINC = 7;
update h02_income set income = 75000 where TOTALINC = 8;
update h02_income set income = 85000 where TOTALINC = 9;
update h02_income set income = 95000 where TOTALINC = 10;
update h02_income set income = 105000 where TOTALINC = 11;
update h02_income set income = 115000 where TOTALINC = 12;
update h02_income set income = 125000 where TOTALINC = 13;
update h02_income set income = 135000 where TOTALINC = 14;
update h02_income set income = 145000 where TOTALINC = 15;
update h02_income set income = 175000 where TOTALINC = 16;
update h02_income set income = 25000 where TOTALINC = 17;
update h02_income set income = 75000 where TOTALINC = 18;
update h02_income set income = 125000 where TOTALINC = 19;
update h02_income set income = -1 where TOTALINC = 98 or TOTALINC = 99;

select TOTALINC, income, count(*) as number from h02_income h group by TOTALINC order by TOTALINC;
#count of households in each income category
	1.00000, 5000, 102
	2.00000, 15000, 244
	3.00000, 25000, 331
	4.00000, 35000, 379
	5.00000, 45000, 476
	6.00000, 55000, 440
	7.00000, 65000, 412
	8.00000, 75000, 373
	9.00000, 85000, 266
	10.00000, 95000, 288
	11.00000, 105000, 177
	12.00000, 115000, 163
	13.00000, 125000, 121
	14.00000, 135000, 66
	15.00000, 145000, 68
	16.00000, 175000, 293
	17.00000, 25000, 100
	18.00000, 75000, 123
	19.00000, 125000, 79
	98.00000, -1, 74
	99.00000, -1, 171

