FILTER OFF.
USE ALL.
SELECT IF(~missing(cplanid)).
EXECUTE .
FILTER OFF.
USE ALL.
SELECT IF(lot_sf  > 0).
EXECUTE .
FILTER OFF.
USE ALL.
SELECT IF(lot_ac  > 0).
EXECUTE .
FILTER OFF.
USE ALL.
SELECT IF(cplanid > 1).
EXECUTE .

COMPUTE lot_ac = max(lot_ac,ftprint/43560) .
COMPUTE lot_sf = max(lot_sf,ftprint) .
EXECUTE .

COMPUTE du_ac = (du_sfr + du_mfr)/lot_ac .
COMPUTE far_sfr = sf_sfr/lot_sf .
COMPUTE far_mfr = sf_mfr/lot_sf .
COMPUTE far_com = sf_com/lot_sf .
COMPUTE far_gov = sf_gov/lot_sf .
COMPUTE far_ind = sf_ind/lot_sf .
VARIABLE LABELS 
	far_sfr 'FAR for Single Family Residential'
	far_mfr 'FAR for Multi-Family Residential'
	far_com 'FAR for Commercial'
	far_gov 'FAR for Governmental'
	far_ind 'FAR for Industrial'
	du_ac 'Dwelling Units per Acre' .
EXECUTE .

IF (du_sfr > 0) ltsz_sfr = lot_sf/du_sfr .
VARIABLE LABELS ltsz_sfr 'Single-Family Lot Size (sqft)' .
EXECUTE .

USE ALL.
COMPUTE filter_$=(yrblt>=1995)&(lot_sf>=ftprint).
VARIABLE LABEL filter_$ 'yrblt>=1995 (FILTER)'.
VALUE LABELS filter_$  0 'Not Selected' 1 'Selected'.
FORMAT filter_$ (f1.0).
FILTER BY filter_$.
EXECUTE .


TABLES
	/OBSERVATION = far_com
	/TABLE = inurbctr>cplanid by far_com
	/STATISTICS = MINIMUM(far_com) 
		PTILE 05(far_com) 
		MEDIAN(far_com)
		PTILE 75(far_com)
		PTILE 95(far_com)
		MAXIMUM(far_com).

TABLES
	/OBSERVATION = far_ind
	/TABLE = inurbctr>cplanid by far_ind
	/STATISTICS = MINIMUM(far_ind) 
		PTILE 05(far_ind) 
		MEDIAN(far_ind)
		PTILE 75(far_ind)
		PTILE 95(far_ind)
		MAXIMUM(far_ind).

COMPUTE rduac = sqrt(du_ac) .
COMPUTE rfarsfr = sqrt(far_sfr) .
COMPUTE rfarmfr = sqrt(far_mfr) .
COMPUTE rfarcom = sqrt(far_com) .
COMPUTE rfarind = sqrt(far_ind) .
COMPUTE rfargov = sqrt(far_gov) .
COMPUTE rltszsfr = sqrt(ltsz_sfr) .
EXECUTE .

AGGREGATE
/OUTFILE='N:\PSRC\dev_constr\reduced_plan_types.SAV'
/BREAK=cplanid
/rduaca  'Average Sqrt DU/ac' = MEAN(rduac) 
/rfarsfa 'Average Sqrt FAR for SFR' = MEAN(rfarsfr) 
/rfarmfa 'Average Sqrt FAR for MFR' = MEAN(rfarmfr) 
/rfarcoa 'Average Sqrt FAR for Com' = MEAN(rfarcom) 
/rfargoa 'Average Sqrt FAR for Gov' = MEAN(rfargov)
/rfarina 'Average Sqrt FAR for Ind' = MEAN(rfarind) 
/rltszsa 'Average Sqrt Lot Size for SFR' = MEAN(rltszsfr) 
/rduacn  'Min Sqrt DU/ac' = MIN(rduac) 
/rfarsfn 'Min Sqrt FAR for SFR' = MIN(rfarsfr) 
/rfarmfn 'Min Sqrt FAR for MFR' = MIN(rfarmfr) 
/rfarcon 'Min Sqrt FAR for Com' = MIN(rfarcom) 
/rfargon 'Min Sqrt FAR for Gov' = MIN(rfargov) 
/rfarinn 'Min Sqrt FAR for Ind' = MIN(rfarind) 
/rltszsn 'Min Sqrt Lot Size for SFR' = MIN(rltszsfr) 
/rduacx  'Max Sqrt DU/ac' = MAX(rduac) 
/rfarsfx 'Max Sqrt FAR for SFR' = MAX(rfarsfr)
/rfarmfx 'Max Sqrt FAR for MFR' = MAX(rfarmfr) 
/rfarcox 'Max Sqrt FAR for Com' = MAX(rfarcom) 
/rfargox 'Max Sqrt FAR for Gov' = MAX(rfargov)
/rfarinx 'Max Sqrt FAR for Ind' = MAX(rfarind) 
/rltszsx 'Max Sqrt Lot Size for SFR' = MAX(rltszsfr).

SAVE OUTFILE='N:\PSRC\dev_constr\parcels_merged.sav'
  /COMPRESSED.
SAVE TRANSLATE OUTFILE='N:\PSRC\dev_constr\parcels_merged.tab'
  /TYPE=TAB /MAP /REPLACE /FIELDNAMES.

FILTER OFF.
USE ALL.
SELECT IF((yrblt>=1995)&(lot_sf>=ftprint)).
EXECUTE .
SAVE TRANSLATE OUTFILE='N:\PSRC\dev_constr\parcels_merged_1995-.tab'
  /TYPE=TAB /MAP /REPLACE /FIELDNAMES.

GET
  FILE='N:\PSRC\dev_constr\reduced_plan_types.SAV'.

DESCRIPTIVES
  VARIABLES=rduaca rfarsfa rfarmfa rfarcoa rfargoa rfarina rltszsa
  rduacn rfarsfn rfarmfn rfarcon rfargon rfarinn rltszsn rduacx
  rfarsfx rfarmfx rfarcox rfargox rfarinx rltszsx  /SAVE
  /STATISTICS=MEAN .

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(2) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_02)
  /PRINT INITIAL.
SORT CASES BY
  qcl_02 (A) .

VALUE LABELS qcl_02
	1 "MFR/Com"
	2 "SFR/Gov".

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(3) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_03)
  /PRINT INITIAL.
SORT CASES BY
  qcl_03 (A) .

VALUE LABELS qcl_03
	1 "Com/Ind"
	2 "SFR"
	3 "MFR/Gov".

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(4) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_04)
  /PRINT INITIAL.
SORT CASES BY
  qcl_04 (A) .

VALUE LABELS qcl_04
	1 "Ind"
	2 "Res"
	3 "Com"
	4 "Gov".

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(5) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_05)
  /PRINT INITIAL.
SORT CASES BY
  qcl_05 (A) .

VALUE LABELS qcl_05
	1 "Com"
	2 "SFR"
	3 "MFR"
	4 "Gov"
	5 "Ind".

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(6) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_06)
  /PRINT INITIAL.
SORT CASES BY
  qcl_06 (A) .

VALUE LABELS qcl_06
	1 "Ind"
	2 "Com"
	3 "MFR"
	4 "Gov"
	5 "SFR"
	6 "Undev".

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(7) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_07)
  /PRINT INITIAL.
SORT CASES BY
  qcl_07 (A) .

VALUE LABELS qcl_07
	1 "Com/Gov"
	2 "SFR"
	3 "MFR"
	4 "Gov"
	5 "Undev"
	6 "Com"
	7 "Ind".

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(8) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_08)
  /PRINT INITIAL.
SORT CASES BY
  qcl_08 (A) .

VALUE LABELS qcl_08
	1 "Gov/Com"
	2 "Ind"
	3 "SFR"
	4 "Com/Ind with some MFR"
	5 "Hi Gov"
	6 "MFR"
	7 "Com/MFR witih some Ind"
	8 "Undev".

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(9) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_09)
  /PRINT INITIAL.
SORT CASES BY
  qcl_09 (A) .

VALUE LABELS qcl_09
	1 "Undev"
	2 "Com with some MFR/Ind"
	3 "Hi Com"
	4 "Hi Ind"
	5 "MFR/Gov"
	6 "Hi Gov"
	7 "Hi MFR"
	8 "Mid MFR"
	9 "SFR".

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(10) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_10)
  /PRINT INITIAL.
SORT CASES BY
  qcl_10 (A) .

VALUE LABELS qcl_10
	1 "Gov with some Com"
	2 "Mid Gov"
	3 "Mid SFR"
	4 "Com/MFR"
	5 "Hi MFR"
	6 "Low SFR"
	7 "Mid Com"
	8 "Hi Gov"
	9 "Hi Com"
	10 "Hi Ind".

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(11) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_11)
  /PRINT INITIAL.
SORT CASES BY
  qcl_11 (A) .

VALUE LABELS qcl_11
	1 "Hi Ind"
	2 "Hi SFR"
	3 "Mid MFR"
	4 "Low Gov"
	5 "Hi Com"
	6 "MFR/Gov/Com"
	7 "Hi MFR"
	8 "Undev"
	9 "Mid Gov"
	10 "Hi Gov"
	11 "Mid SFR".

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(12) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_12)
  /PRINT INITIAL.
SORT CASES BY
  qcl_12 (A) .

VALUE LABELS qcl_12
	1 "Low Com"
	2 "Mid Ind"
	3 "MFR/Gov"
	4 "Hi Com"
	5 "Hi SFR"
	6 "Hi Gov"
	7 "Hi Ind"
	8 "Hi MFR"
	9 "Mid Com"
	10 "Mid MFR"
	11 "Mid Gov"
	12 "Low SFR".

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(13) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_13)
  /PRINT INITIAL.
SORT CASES BY
  qcl_13 (A) .

VALUE LABELS qcl_13
	1 "Hi Ind"
	2 "Hi MFR"
	3 "Hi Gov"
	4 "Hi SFR"
	5 "Mid MFR"
	6 "Low Com/Ind"
	7 "Hi Com"
	8 "Mid Gov"
	9 "Low SFR"
	10 "Mid Gov"
	11 "Com/MFR"
	12 "Undev"
	13 "Hi MFR/Gov".

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(14) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_14)
  /PRINT INITIAL.
SORT CASES BY
  qcl_14 (A) .

VALUE LABELS qcl_14
	1 "Mid Ind"
	2 "Low Com/MFR"
	3 "Mid MFR/Gov"
	4 "Mid MFR"
	5 "Mid Com/MFR"
	6 "Hi Ind"
	7 "Hi Gov"
	8 "Hi Com"
	9 "Undev"
	10 "Hi SFR"
	11 "Hi MFR"
	12 "Hi Gov"
	13 "Low Gov"
	14 "Low SFR".

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(15) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_15)
  /PRINT INITIAL.
SORT CASES BY
  qcl_15 (A) .

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(16) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_16)
  /PRINT INITIAL.
SORT CASES BY
  qcl_16 (A) .

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(17) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_17)
  /PRINT INITIAL.
SORT CASES BY
  qcl_17 (A) .

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(18) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_18)
  /PRINT INITIAL.
SORT CASES BY
  qcl_18 (A) .

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(19) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_19)
  /PRINT INITIAL.
SORT CASES BY
  qcl_19 (A) .

QUICK CLUSTER
  zrduaca zrfarsfa zrfarmfa zrfarcoa zrfargoa zrfarina
  /MISSING=LISTWISE
  /CRITERIA= CLUSTER(20) MXITER(10) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER(qcl_20)
  /PRINT INITIAL.
SORT CASES BY
  qcl_20 (A) .




