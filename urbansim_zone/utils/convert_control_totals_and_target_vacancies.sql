select * from target_vacancies;

alter table target_vacancies
  add is_residential int,
  add target_vacancy float;

update target_vacancies
  set is_residential = 1,
      target_vacancy=target_total_residential_vacancy;

insert into target_vacancies
  (year, is_residential, target_vacancy)
select year, 0, target_total_non_residential_vacancy
  from target_vacancies;

alter table target_vacancies
  drop target_total_residential_vacancy,
  drop target_total_non_residential_vacancy;

SELECT * FROM target_vacancies t;


SELECT * FROM annual_employment_control_totals a;

alter table annual_employment_control_totals
  add home_based_status int,
  add number_of_jobs int;

update annual_employment_control_totals
  set home_based_status = 1,
      number_of_jobs=total_home_based_employment;

insert into annual_employment_control_totals
  (year, sector_id, home_based_status, number_of_jobs)
select year, sector_id, 0, total_non_home_based_employment
  from annual_employment_control_totals;

alter table annual_employment_control_totals
  drop total_home_based_employment,
  drop total_non_home_based_employment;


SELECT * FROM annual_household_control_totals a;
SELECT * FROM household_characteristics_for_ht h;

## re-format annual_household_control_totals is only necessary
## when there are other columns than year and total_number_of_households
## that appear in characteristic field of household_characteristics_for_ht
drop table if exists tmp_household_characteristics_for_ht;

create table tmp_household_characteristics_for_ht (
id int not null auto_increment,
characteristic varchar(32),
`min` int,
`max` int,
primary key(characteristic, id)
);

insert into tmp_household_characteristics_for_ht
 (characteristic, `min`, `max`)
select characteristic, `min`, `max`
  from household_characteristics_for_ht
order by characteristic, `min`, `max`;

update tmp_household_characteristics_for_ht
  set id = id -1;

select * from tmp_household_characteristics_for_ht;

## need to repeat this for every column in annual_household_control_totals
## other than year and total_number_of_households, take age_of_head as an example below
alter table annual_household_control_totals
add age_of_head_min int after age_of_head,
add age_of_head_max int after age_of_head_min;

update annual_household_control_totals t, tmp_household_characteristics_for_ht c
  set t.age_of_head_min = c.`min`, t.age_of_head_max = c.`max`
where t.age_of_head = c.id and c.characteristic = 'age_of_head';

## repeat the last two sql clauses for other columns