##create business_for_estimation using random sampling from business table. 
##Not sure what original critieria were.

drop table if exists business_for_estimation;
create table business_for_estimation
SELECT * FROM business b
ORDER BY RAND()
LIMIT 21000;