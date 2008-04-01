USE WFRC_1997_output_5yr_2003;

DROP TABLE IF EXISTS accessibilities_transpose;

CREATE TABLE accessibilities_transpose (zone_id int,
  # hae1_97 double, 
  hae1_98 double, hae1_99 double, hae1_00 double, hae1_01 double,
  hae1_02 double, hae1_03 double
  );
  
CREATE INDEX accessibilities_transpose_zone_id
     ON accessibilities_transpose (zone_id);

INSERT INTO accessibilities_transpose
SELECT yr_98.zone_id AS zone_id,
     # yr_97.HOME_ACCESS_TO_EMPLOYMENT_1 AS hae1_97,
     yr_98.HOME_ACCESS_TO_EMPLOYMENT_1 AS hae1_98,
     yr_99.HOME_ACCESS_TO_EMPLOYMENT_1 AS hae1_99,
     yr_00.HOME_ACCESS_TO_EMPLOYMENT_1 AS hae1_00,
     yr_01.HOME_ACCESS_TO_EMPLOYMENT_1 AS hae1_01,
     yr_02.HOME_ACCESS_TO_EMPLOYMENT_1 AS hae1_02,
     yr_03.HOME_ACCESS_TO_EMPLOYMENT_1 AS hae1_03
FROM 
     # accessibilities AS yr_97,
     accessibilities AS yr_98,
     accessibilities AS yr_99,
     accessibilities AS yr_00,
     accessibilities AS yr_01,
     accessibilities AS yr_02,
     accessibilities AS yr_03
WHERE 
      # yr_97.year=1997 AND
      yr_98.year=1998
  AND yr_99.year=1999
  AND yr_00.year=2000
  AND yr_01.year=2001
  AND yr_02.year=2002
  AND yr_03.year=2003
  # AND yr_97.zone_id=yr_98.zone_id
  AND yr_98.zone_id=yr_99.zone_id
  AND yr_98.zone_id=yr_00.zone_id
  AND yr_98.zone_id=yr_01.zone_id
  AND yr_98.zone_id=yr_02.zone_id
  AND yr_98.zone_id=yr_03.zone_id
ORDER BY yr_98.zone_id;
