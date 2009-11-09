create table jobs_for_estimation like jobs;
insert into jobs_for_estimation select * from jobs where sector_id = 1 order by rand() limit 5000;
insert into jobs_for_estimation select * from jobs where sector_id = 2 order by rand() limit 5000;
insert into jobs_for_estimation select * from jobs where sector_id = 3 order by rand() limit 5000;
insert into jobs_for_estimation select * from jobs where sector_id = 4 order by rand() limit 5000;
insert into jobs_for_estimation select * from jobs where sector_id = 5 order by rand() limit 5000;
insert into jobs_for_estimation select * from jobs where sector_id = 6 order by rand() limit 5000;
insert into jobs_for_estimation select * from jobs where sector_id = 7 order by rand() limit 5000;
insert into jobs_for_estimation select * from jobs where sector_id = 8 order by rand() limit 5000;
insert into jobs_for_estimation select * from jobs where sector_id = 9 order by rand() limit 5000;
insert into jobs_for_estimation select * from jobs where sector_id = 10 order by rand() limit 5000;
insert into jobs_for_estimation select * from jobs where sector_id = 11 order by rand() limit 5000;
insert into jobs_for_estimation select * from jobs where sector_id = 12 order by rand() limit 5000;
insert into jobs_for_estimation select * from jobs where sector_id = 13 order by rand() limit 5000;
insert into jobs_for_estimation select * from jobs where sector_id = 14 order by rand() limit 5000;
insert into jobs_for_estimation select * from jobs where sector_id = 15 order by rand() limit 5000;
insert into jobs_for_estimation select * from jobs where sector_id = 16 order by rand() limit 5000;
 