load data local infile 'Z:/Research/Projects/San Francisco/data/luse00.csv'
  into table luse00
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES;
